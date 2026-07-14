"""
Eye Music - API 擴充模組
提供與 Google Sheets/GAS 整合的 API 端點
"""
from flask import Blueprint, request, jsonify
import uuid
from datetime import datetime
import logging
from pathlib import Path
import os

logger = logging.getLogger(__name__)

# 建立 Blueprint
api_ext = Blueprint('api_ext', __name__, url_prefix='/api')

# 全域任務儲存（實際應使用資料庫或 Redis）
gas_tasks = {}

# 路徑配置
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = BASE_DIR / 'src' / 'static' / 'uploads'
OUTPUT_FOLDER = BASE_DIR / 'src' / 'static' / 'outputs'


@api_ext.route('/health', methods=['GET'])
def health_check():
    """
    健康檢查端點
    供 GAS 測試連接使用
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Eye Music API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


@api_ext.route('/gas/generate', methods=['POST'])
def gas_generate_video():
    """
    GAS 專用的影片生成端點
    接收來自 Google Sheets 的任務請求

    請求格式：
    {
        "task_id": "Sheet 中的任務序號",
        "song_name": "歌曲名稱",
        "audio_url": "音樂檔案 URL 或本地路徑",
        "visualization_type": "bars/circular/piano",
        "color_scheme": "rainbow/fire/ocean/purple",
        "resolution": "1080p",
        "fps": 30,
        "ai_model": "使用的 AI 模型名稱（紀錄用）"
    }

    回應格式：
    {
        "success": true,
        "job_id": "生成的任務 ID",
        "message": "任務已接收",
        "estimated_time": 120 (預估秒數)
    }
    """
    try:
        data = request.json

        # 驗證必要參數
        required_fields = ['song_name', 'audio_url', 'visualization_type', 'color_scheme']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'缺少必要參數: {field}'
                }), 400

        # 生成內部任務 ID
        job_id = data.get('task_id', uuid.uuid4().hex)

        # 處理音檔路徑或 URL
        audio_path = data['audio_url']

        # 如果是 Google Drive URL，需要轉換成下載連結
        if 'drive.google.com' in audio_path:
            audio_path = convert_gdrive_url(audio_path)
            # 下載檔案到本地
            audio_path = download_file_from_url(audio_path, job_id)
        elif audio_path.startswith('http'):
            # 其他 URL，直接下載
            audio_path = download_file_from_url(audio_path, job_id)
        else:
            # 本地路徑，檢查是否存在
            audio_path = UPLOAD_FOLDER / audio_path
            if not audio_path.exists():
                return jsonify({
                    'success': False,
                    'error': f'音檔不存在: {audio_path}'
                }), 404

        # 解析解析度
        resolution = parse_resolution(data.get('resolution', '1080p'))

        # 映射視覺化類型名稱
        viz_type_map = {
            'bars': 'spectrum_bars',
            'circular': 'circular_spectrum',
            'piano': 'piano_roll'
        }
        visualization_type = viz_type_map.get(
            data['visualization_type'],
            'spectrum_bars'
        )

        # 建立任務配置
        config = {
            'audio_path': str(audio_path),
            'output_path': str(OUTPUT_FOLDER / f"{job_id}.mp4"),
            'visualization_type': visualization_type,
            'fps': int(data.get('fps', 30)),
            'resolution': resolution,
            'spectrum_height_multiplier': float(data.get('spectrum_height_multiplier', 1.0)),
            'spectrum_opacity': float(data.get('spectrum_opacity', 0.8)),
            'color_scheme': data['color_scheme'],
            'background_color': (0, 0, 0),
            'blur_effect': data.get('blur_effect', False),
            'n_fft': 2048,
            'hop_length': 512,
            'n_mels': 128
        }

        # 儲存任務資訊
        gas_tasks[job_id] = {
            'status': 'queued',
            'progress': 0,
            'message': '任務已加入佇列',
            'created_at': datetime.now().isoformat(),
            'song_name': data['song_name'],
            'config': config,
            'ai_model': data.get('ai_model', 'N/A'),
            'output_file': None,
            'error': None,
            'download_url': None
        }

        # 啟動背景任務
        from threading import Thread
        thread = Thread(target=process_gas_task, args=(job_id,))
        thread.daemon = True
        thread.start()

        # 預估處理時間（根據經驗值）
        estimated_time = estimate_processing_time(config)

        logger.info(f"GAS 任務已接收: {job_id} - {data['song_name']}")

        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': '任務已接收並開始處理',
            'estimated_time': estimated_time,
            'status_url': f'/api/gas/status/{job_id}'
        })

    except Exception as e:
        logger.error(f"GAS 任務建立失敗: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_ext.route('/gas/status/<job_id>', methods=['GET'])
def gas_task_status(job_id):
    """
    查詢任務狀態
    供 GAS 輪詢使用

    回應格式：
    {
        "success": true,
        "job_id": "任務 ID",
        "status": "queued/processing/completed/failed",
        "progress": 0-100,
        "message": "狀態訊息",
        "download_url": "下載連結（完成時）",
        "error": "錯誤訊息（失敗時）"
    }
    """
    if job_id not in gas_tasks:
        return jsonify({
            'success': False,
            'error': '任務不存在'
        }), 404

    task = gas_tasks[job_id]

    response = {
        'success': True,
        'job_id': job_id,
        'status': task['status'],
        'progress': task['progress'],
        'message': task['message'],
        'song_name': task.get('song_name', 'Unknown'),
        'created_at': task['created_at']
    }

    # 如果任務完成，提供下載連結
    if task['status'] == 'completed':
        response['download_url'] = f"/api/download/{job_id}.mp4"
        response['output_file'] = f"{job_id}.mp4"

    # 如果任務失敗，提供錯誤訊息
    if task['status'] == 'failed':
        response['error'] = task.get('error', 'Unknown error')

    return jsonify(response)


@api_ext.route('/gas/batch/status', methods=['POST'])
def gas_batch_status():
    """
    批次查詢多個任務狀態
    減少 GAS 的 API 呼叫次數

    請求格式：
    {
        "job_ids": ["job1", "job2", "job3"]
    }

    回應格式：
    {
        "success": true,
        "tasks": {
            "job1": {...},
            "job2": {...}
        }
    }
    """
    try:
        data = request.json
        job_ids = data.get('job_ids', [])

        if not job_ids:
            return jsonify({
                'success': False,
                'error': '未提供任務 ID'
            }), 400

        results = {}
        for job_id in job_ids:
            if job_id in gas_tasks:
                task = gas_tasks[job_id]
                results[job_id] = {
                    'status': task['status'],
                    'progress': task['progress'],
                    'message': task['message'],
                    'download_url': f"/api/download/{job_id}.mp4" if task['status'] == 'completed' else None,
                    'error': task.get('error') if task['status'] == 'failed' else None
                }
            else:
                results[job_id] = {
                    'status': 'not_found',
                    'error': '任務不存在'
                }

        return jsonify({
            'success': True,
            'tasks': results
        })

    except Exception as e:
        logger.error(f"批次查詢失敗: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_ext.route('/gas/tasks', methods=['GET'])
def gas_list_tasks():
    """
    列出所有任務（分頁）
    供管理用途

    查詢參數：
    - page: 頁碼（預設 1）
    - per_page: 每頁數量（預設 20）
    - status: 篩選狀態（可選）
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        status_filter = request.args.get('status')

        # 篩選任務
        filtered_tasks = []
        for job_id, task in gas_tasks.items():
            if status_filter and task['status'] != status_filter:
                continue

            filtered_tasks.append({
                'job_id': job_id,
                'song_name': task.get('song_name', 'Unknown'),
                'status': task['status'],
                'progress': task['progress'],
                'created_at': task['created_at'],
                'ai_model': task.get('ai_model', 'N/A')
            })

        # 排序（最新的在前）
        filtered_tasks.sort(key=lambda x: x['created_at'], reverse=True)

        # 分頁
        total = len(filtered_tasks)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_tasks = filtered_tasks[start:end]

        return jsonify({
            'success': True,
            'tasks': paginated_tasks,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': (total + per_page - 1) // per_page
            }
        })

    except Exception as e:
        logger.error(f"列出任務失敗: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_ext.route('/gas/task/<job_id>', methods=['DELETE'])
def gas_delete_task(job_id):
    """
    刪除任務及相關檔案
    """
    try:
        if job_id not in gas_tasks:
            return jsonify({
                'success': False,
                'error': '任務不存在'
            }), 404

        task = gas_tasks[job_id]

        # 刪除輸出檔案
        output_file = OUTPUT_FOLDER / f"{job_id}.mp4"
        if output_file.exists():
            os.remove(output_file)
            logger.info(f"已刪除檔案: {output_file}")

        # 刪除任務記錄
        del gas_tasks[job_id]

        return jsonify({
            'success': True,
            'message': '任務已刪除'
        })

    except Exception as e:
        logger.error(f"刪除任務失敗: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ====================================
# 輔助函數
# ====================================

def process_gas_task(job_id):
    """
    處理 GAS 任務的背景函數
    """
    try:
        from core.visualizer import create_visualizer

        task = gas_tasks[job_id]
        task['status'] = 'processing'
        task['message'] = '正在生成視覺化影片...'

        logger.info(f"開始處理任務: {job_id}")

        # 進度回調
        def progress_callback(progress, message):
            task['progress'] = progress
            task['message'] = message
            logger.info(f"任務 {job_id} 進度: {progress}% - {message}")

        # 加入進度回調到配置
        config = task['config']
        config['progress_callback'] = progress_callback

        # 生成影片
        visualizer = create_visualizer(config)
        output_path = visualizer.generate_video()

        # 更新任務狀態
        task['status'] = 'completed'
        task['progress'] = 100
        task['message'] = '生成完成！'
        task['output_file'] = f"{job_id}.mp4"
        task['download_url'] = f"/api/download/{job_id}.mp4"
        task['completed_at'] = datetime.now().isoformat()

        logger.info(f"任務完成: {job_id}")

    except Exception as e:
        logger.error(f"任務處理失敗: {job_id} - {e}")
        task['status'] = 'failed'
        task['error'] = str(e)
        task['message'] = '生成失敗'
        task['failed_at'] = datetime.now().isoformat()


def convert_gdrive_url(url):
    """
    轉換 Google Drive 分享連結為直接下載連結
    """
    if '/file/d/' in url:
        file_id = url.split('/file/d/')[1].split('/')[0]
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return url


def download_file_from_url(url, job_id):
    """
    從 URL 下載檔案到本地
    """
    import requests

    try:
        logger.info(f"開始下載檔案: {url}")

        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        # 猜測副檔名（從 Content-Type 或 URL）
        content_type = response.headers.get('Content-Type', '')
        if 'audio/mpeg' in content_type or url.endswith('.mp3'):
            ext = 'mp3'
        elif 'audio/wav' in content_type or url.endswith('.wav'):
            ext = 'wav'
        elif url.endswith('.flac'):
            ext = 'flac'
        else:
            ext = 'mp3'  # 預設

        filename = f"{job_id}_downloaded.{ext}"
        file_path = UPLOAD_FOLDER / filename

        # 下載檔案
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logger.info(f"檔案下載完成: {file_path}")
        return file_path

    except Exception as e:
        logger.error(f"下載檔案失敗: {e}")
        raise


def parse_resolution(resolution_str):
    """
    解析解析度字串為 tuple
    """
    resolution_map = {
        '720p': (1280, 720),
        '1080p': (1920, 1080),
        '2k': (2560, 1440),
        '4k': (3840, 2160)
    }
    return resolution_map.get(resolution_str.lower(), (1920, 1080))


def estimate_processing_time(config):
    """
    預估處理時間（秒）
    根據解析度和 FPS
    """
    resolution = config['resolution']
    fps = config['fps']

    # 基礎時間（假設 1 分鐘音樂）
    base_time = 30

    # 解析度影響
    pixels = resolution[0] * resolution[1]
    resolution_factor = pixels / (1920 * 1080)

    # FPS 影響
    fps_factor = fps / 30

    estimated = base_time * resolution_factor * fps_factor

    return int(estimated)
