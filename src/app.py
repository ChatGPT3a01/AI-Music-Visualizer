"""
Eye Music - Web 音樂視覺化應用程式
Flask 後端服務器
"""
from flask import Flask, render_template, request, jsonify, send_from_directory, session
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import os
import json
import uuid
from pathlib import Path
from datetime import datetime
import threading
import logging

from core.visualizer import create_visualizer
from api_extensions import api_ext

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 Flask 應用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'eye-music-secret-key-2024'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB 上傳限制

# 初始化 SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=500 * 1024 * 1024)

# 註冊 API 擴充 Blueprint
app.register_blueprint(api_ext)

# 路徑配置
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = BASE_DIR / 'src' / 'static' / 'uploads'
OUTPUT_FOLDER = BASE_DIR / 'src' / 'static' / 'outputs'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'ogg', 'm4a', 'aac'}

# 確保資料夾存在
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# 任務狀態存儲
tasks = {}


def allowed_file(filename):
    """檢查檔案類型是否允許"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """處理音頻檔案上傳"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': '沒有檔案被上傳'}), 400

        file = request.files['audio']

        if file.filename == '':
            return jsonify({'error': '沒有選擇檔案'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': f'不支援的檔案類型。支援的格式: {", ".join(ALLOWED_EXTENSIONS)}'}), 400

        # 生成唯一檔案名
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
        file_path = UPLOAD_FOLDER / unique_filename

        # 儲存檔案
        file.save(str(file_path))

        logger.info(f"檔案上傳成功: {unique_filename}")

        return jsonify({
            'success': True,
            'filename': unique_filename,
            'original_filename': file.filename,
            'file_size': os.path.getsize(file_path)
        })

    except Exception as e:
        logger.error(f"檔案上傳失敗: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_audio():
    """分析音頻並返回基本資訊"""
    try:
        data = request.json
        filename = data.get('filename')

        if not filename:
            return jsonify({'error': '未提供檔案名'}), 400

        file_path = UPLOAD_FOLDER / filename

        if not file_path.exists():
            return jsonify({'error': '檔案不存在'}), 404

        # 使用 librosa 分析音頻
        import librosa
        y, sr = librosa.load(str(file_path), sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        return jsonify({
            'success': True,
            'duration': float(duration),
            'sample_rate': int(sr),
            'tempo': float(tempo),
            'channels': 1 if y.ndim == 1 else y.shape[0]
        })

    except Exception as e:
        logger.error(f"音頻分析失敗: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate', methods=['POST'])
def generate_video():
    """生成音樂視覺化影片"""
    try:
        data = request.json
        filename = data.get('filename')

        if not filename:
            return jsonify({'error': '未提供檔案名'}), 400

        # 生成任務 ID
        task_id = uuid.uuid4().hex

        # 配置參數
        config = {
            'audio_path': str(UPLOAD_FOLDER / filename),
            'output_path': str(OUTPUT_FOLDER / f"{task_id}.mp4"),
            'visualization_type': data.get('visualization_type', 'spectrum_bars'),
            'fps': int(data.get('fps', 30)),
            'resolution': tuple(data.get('resolution', [1920, 1080])),
            'spectrum_height_multiplier': float(data.get('spectrum_height_multiplier', 1.0)),
            'spectrum_opacity': float(data.get('spectrum_opacity', 0.8)),
            'color_scheme': data.get('color_scheme', 'rainbow'),
            'background_color': tuple(data.get('background_color', [0, 0, 0])),
            'blur_effect': data.get('blur_effect', False),
            'n_fft': int(data.get('n_fft', 2048)),
            'hop_length': int(data.get('hop_length', 512)),
            'n_mels': int(data.get('n_mels', 128)),
        }

        # 進度回調函數
        def progress_callback(progress, message):
            socketio.emit('progress', {
                'task_id': task_id,
                'progress': progress,
                'message': message
            }, namespace='/')

        config['progress_callback'] = progress_callback

        # 初始化任務狀態
        tasks[task_id] = {
            'status': 'processing',
            'progress': 0,
            'message': '初始化...',
            'created_at': datetime.now().isoformat(),
            'output_file': None,
            'error': None
        }

        # 在背景執行緒中生成影片
        def generate_task():
            try:
                logger.info(f"開始生成任務: {task_id}")
                visualizer = create_visualizer(config)
                output_path = visualizer.generate_video()

                tasks[task_id]['status'] = 'completed'
                tasks[task_id]['progress'] = 100
                tasks[task_id]['message'] = '完成！'
                tasks[task_id]['output_file'] = f"{task_id}.mp4"

                socketio.emit('complete', {
                    'task_id': task_id,
                    'output_file': f"{task_id}.mp4",
                    'download_url': f"/api/download/{task_id}.mp4"
                }, namespace='/')

                logger.info(f"任務完成: {task_id}")

            except Exception as e:
                logger.error(f"任務失敗: {task_id} - {e}")
                tasks[task_id]['status'] = 'failed'
                tasks[task_id]['error'] = str(e)
                socketio.emit('error', {
                    'task_id': task_id,
                    'error': str(e)
                }, namespace='/')

        thread = threading.Thread(target=generate_task)
        thread.daemon = True
        thread.start()

        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '影片生成任務已啟動'
        })

    except Exception as e:
        logger.error(f"生成影片失敗: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """查詢任務狀態"""
    if task_id not in tasks:
        return jsonify({'error': '任務不存在'}), 404

    return jsonify({
        'success': True,
        'task': tasks[task_id]
    })


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """下載生成的影片"""
    try:
        return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)
    except Exception as e:
        logger.error(f"檔案下載失敗: {e}")
        return jsonify({'error': '檔案不存在'}), 404


@app.route('/api/presets', methods=['GET'])
def get_presets():
    """獲取預設配置列表"""
    presets = [
        {
            'id': 'default',
            'name': '預設',
            'description': '標準的頻譜能量條視覺化',
            'config': {
                'visualization_type': 'spectrum_bars',
                'color_scheme': 'rainbow',
                'spectrum_height_multiplier': 1.0,
                'spectrum_opacity': 0.8
            }
        },
        {
            'id': 'circular',
            'name': '圓形頻譜',
            'description': '圓形放射狀頻譜視覺化',
            'config': {
                'visualization_type': 'circular_spectrum',
                'color_scheme': 'purple',
                'spectrum_height_multiplier': 1.5,
                'spectrum_opacity': 0.9
            }
        },
        {
            'id': 'piano',
            'name': '鋼琴瀑布流',
            'description': '音符瀑布流視覺化',
            'config': {
                'visualization_type': 'piano_roll',
                'color_scheme': 'ocean',
                'spectrum_height_multiplier': 1.0,
                'spectrum_opacity': 0.7
            }
        },
        {
            'id': 'fire',
            'name': '火焰效果',
            'description': '火焰色系頻譜',
            'config': {
                'visualization_type': 'spectrum_bars',
                'color_scheme': 'fire',
                'spectrum_height_multiplier': 1.3,
                'spectrum_opacity': 0.85
            }
        }
    ]

    return jsonify({
        'success': True,
        'presets': presets
    })


@app.route('/api/cleanup', methods=['POST'])
def cleanup_files():
    """清理舊檔案"""
    try:
        data = request.json
        filename = data.get('filename')

        if filename:
            # 刪除特定檔案
            upload_path = UPLOAD_FOLDER / filename
            if upload_path.exists():
                os.remove(upload_path)
                logger.info(f"已刪除檔案: {filename}")

        return jsonify({'success': True})

    except Exception as e:
        logger.error(f"清理檔案失敗: {e}")
        return jsonify({'error': str(e)}), 500


# WebSocket 事件處理
@socketio.on('connect')
def handle_connect():
    """客戶端連接"""
    logger.info('客戶端已連接')
    emit('connected', {'message': '已連接到伺服器'})


@socketio.on('disconnect')
def handle_disconnect():
    """客戶端斷開連接"""
    logger.info('客戶端已斷開')


@socketio.on('ping')
def handle_ping():
    """心跳檢測"""
    emit('pong', {'timestamp': datetime.now().isoformat()})


if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║               🎵 Eye Music 音樂視覺化器 🎵                ║
    ║                                                          ║
    ║              Web 版本 - 正在啟動服務器...                 ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝

    📡 伺服器地址: http://localhost:5000
    🌐 網頁界面: http://localhost:5000

    按 Ctrl+C 停止服務器
    """)

    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
