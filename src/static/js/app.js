// Eye Music - 前端應用程式邏輯

// 全局變數
let socket = null;
let currentStep = 1;
let uploadedFile = null;
let audioInfo = null;
let currentTaskId = null;

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    console.log('Eye Music 初始化中...');

    // 初始化 Socket.IO
    initializeSocket();

    // 初始化上傳功能
    initializeUpload();

    // 初始化設定控件
    initializeSettings();

    // 載入預設模板
    loadPresets();

    showToast('歡迎使用 Eye Music！', 'success');
}

// Socket.IO 連接
function initializeSocket() {
    socket = io();

    socket.on('connect', function() {
        console.log('已連接到伺服器');
    });

    socket.on('disconnect', function() {
        console.log('與伺服器斷開連接');
    });

    socket.on('progress', function(data) {
        updateProgress(data.progress, data.message);
    });

    socket.on('complete', function(data) {
        onGenerationComplete(data);
    });

    socket.on('error', function(data) {
        onGenerationError(data.error);
    });
}

// 上傳功能初始化
function initializeUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('audioFile');

    // 點擊上傳區域
    uploadArea.addEventListener('click', function(e) {
        if (e.target === uploadArea || e.target.tagName === 'P' || e.target.tagName === 'I') {
            fileInput.click();
        }
    });

    // 拖放功能
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    // 檔案選擇
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });
}

// 處理檔案選擇
function handleFileSelect(file) {
    const allowedTypes = ['audio/mpeg', 'audio/wav', 'audio/flac', 'audio/ogg', 'audio/m4a', 'audio/aac'];
    const allowedExtensions = ['mp3', 'wav', 'flac', 'ogg', 'm4a', 'aac'];

    const fileExtension = file.name.split('.').pop().toLowerCase();

    if (!allowedExtensions.includes(fileExtension)) {
        showToast('不支援的檔案格式！', 'error');
        return;
    }

    showLoading(true);

    // 上傳檔案
    const formData = new FormData();
    formData.append('audio', file);

    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            uploadedFile = data.filename;
            displayFileInfo(file.name, data.file_size);
            analyzeAudio(data.filename);
        } else {
            showToast(data.error, 'error');
            showLoading(false);
        }
    })
    .catch(error => {
        console.error('上傳失敗:', error);
        showToast('檔案上傳失敗！', 'error');
        showLoading(false);
    });
}

// 顯示檔案資訊
function displayFileInfo(filename, filesize) {
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const fileMeta = document.getElementById('fileMeta');

    fileName.textContent = filename;
    fileMeta.textContent = `大小: ${formatFileSize(filesize)}`;

    fileInfo.style.display = 'block';
    document.getElementById('uploadArea').style.display = 'none';
}

// 分析音頻
function analyzeAudio(filename) {
    fetch('/api/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filename: filename })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            audioInfo = data;
            const fileMeta = document.getElementById('fileMeta');
            fileMeta.textContent += ` | 時長: ${formatDuration(data.duration)} | BPM: ${Math.round(data.tempo)}`;

            showLoading(false);
            showToast('音頻分析完成！', 'success');

            // 自動跳轉到設定步驟
            setTimeout(() => goToStep(2), 1000);
        } else {
            showToast(data.error, 'error');
            showLoading(false);
        }
    })
    .catch(error => {
        console.error('分析失敗:', error);
        showToast('音頻分析失敗！', 'error');
        showLoading(false);
    });
}

// 移除檔案
function removeFile() {
    if (uploadedFile) {
        fetch('/api/cleanup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename: uploadedFile })
        });
    }

    uploadedFile = null;
    audioInfo = null;
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('uploadArea').style.display = 'flex';
    document.getElementById('audioFile').value = '';
}

// 初始化設定控件
function initializeSettings() {
    // FPS 滑桿
    const fpsSlider = document.getElementById('fps');
    const fpsValue = document.getElementById('fpsValue');
    fpsSlider.addEventListener('input', function() {
        fpsValue.textContent = this.value;
    });

    // 高度倍率滑桿
    const heightSlider = document.getElementById('heightMultiplier');
    const heightValue = document.getElementById('heightMultiplierValue');
    heightSlider.addEventListener('input', function() {
        heightValue.textContent = parseFloat(this.value).toFixed(1);
    });

    // 透明度滑桿
    const opacitySlider = document.getElementById('opacity');
    const opacityValue = document.getElementById('opacityValue');
    opacitySlider.addEventListener('input', function() {
        opacityValue.textContent = parseFloat(this.value).toFixed(1);
    });
}

// 載入預設模板
function loadPresets() {
    fetch('/api/presets')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayPresets(data.presets);
        }
    })
    .catch(error => {
        console.error('載入預設失敗:', error);
    });
}

// 顯示預設模板
function displayPresets(presets) {
    const presetGrid = document.getElementById('presetGrid');
    presetGrid.innerHTML = '';

    presets.forEach(preset => {
        const card = document.createElement('div');
        card.className = 'preset-card';
        card.innerHTML = `
            <h4>${preset.name}</h4>
            <p>${preset.description}</p>
        `;
        card.addEventListener('click', function() {
            applyPreset(preset);
            document.querySelectorAll('.preset-card').forEach(c => c.classList.remove('active'));
            card.classList.add('active');
        });
        presetGrid.appendChild(card);
    });
}

// 應用預設
function applyPreset(preset) {
    const config = preset.config;

    if (config.visualization_type) {
        document.getElementById('visualizationType').value = config.visualization_type;
    }
    if (config.color_scheme) {
        document.getElementById('colorScheme').value = config.color_scheme;
    }
    if (config.spectrum_height_multiplier !== undefined) {
        document.getElementById('heightMultiplier').value = config.spectrum_height_multiplier;
        document.getElementById('heightMultiplierValue').textContent = config.spectrum_height_multiplier.toFixed(1);
    }
    if (config.spectrum_opacity !== undefined) {
        document.getElementById('opacity').value = config.spectrum_opacity;
        document.getElementById('opacityValue').textContent = config.spectrum_opacity.toFixed(1);
    }

    showToast(`已應用預設: ${preset.name}`, 'success');
}

// 步驟導航
function goToStep(step) {
    // 驗證
    if (step === 2 && !uploadedFile) {
        showToast('請先上傳音頻檔案！', 'warning');
        return;
    }

    if (step === 3 && !uploadedFile) {
        showToast('請先上傳音頻檔案！', 'warning');
        return;
    }

    currentStep = step;

    // 更新步驟指示器
    document.querySelectorAll('.step').forEach((el, idx) => {
        if (idx + 1 <= step) {
            el.classList.add('active');
        } else {
            el.classList.remove('active');
        }
    });

    // 顯示對應區域
    document.getElementById('upload').style.display = step === 1 ? 'block' : 'none';
    document.getElementById('settings').style.display = step === 2 ? 'block' : 'none';
    document.getElementById('generate').style.display = step === 3 ? 'block' : 'none';

    // 滾動到頂部
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 開始生成
function startGeneration() {
    if (!uploadedFile) {
        showToast('請先上傳音頻檔案！', 'warning');
        return;
    }

    // 收集配置
    const resolution = document.getElementById('resolution').value.split(',').map(Number);
    const backgroundColor = hexToRgb(document.getElementById('backgroundColor').value);

    const config = {
        filename: uploadedFile,
        visualization_type: document.getElementById('visualizationType').value,
        color_scheme: document.getElementById('colorScheme').value,
        resolution: resolution,
        fps: parseInt(document.getElementById('fps').value),
        spectrum_height_multiplier: parseFloat(document.getElementById('heightMultiplier').value),
        spectrum_opacity: parseFloat(document.getElementById('opacity').value),
        background_color: backgroundColor
    };

    // 隱藏生成按鈕，顯示進度條
    document.getElementById('generateBtn').style.display = 'none';
    document.getElementById('progressContainer').style.display = 'block';

    showLoading(true);

    // 發送生成請求
    fetch('/api/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(config)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentTaskId = data.task_id;
            showLoading(false);
            showToast('開始生成視覺化影片...', 'success');
        } else {
            showToast(data.error, 'error');
            showLoading(false);
            resetGenerationUI();
        }
    })
    .catch(error => {
        console.error('生成失敗:', error);
        showToast('生成請求失敗！', 'error');
        showLoading(false);
        resetGenerationUI();
    });
}

// 更新進度
function updateProgress(progress, message) {
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');

    progressFill.style.width = progress + '%';
    progressFill.textContent = progress + '%';
    progressText.textContent = message;
}

// 生成完成
function onGenerationComplete(data) {
    document.getElementById('progressContainer').style.display = 'none';
    document.getElementById('resultContainer').style.display = 'block';

    const downloadBtn = document.getElementById('downloadBtn');
    downloadBtn.onclick = function() {
        window.location.href = data.download_url;
    };

    showToast('影片生成完成！', 'success');
}

// 生成錯誤
function onGenerationError(error) {
    showToast('生成失敗: ' + error, 'error');
    resetGenerationUI();
}

// 重置生成界面
function resetGenerationUI() {
    document.getElementById('generateBtn').style.display = 'inline-flex';
    document.getElementById('progressContainer').style.display = 'none';
    document.getElementById('resultContainer').style.display = 'none';
}

// 重新開始
function resetAll() {
    if (confirm('確定要重新開始嗎？這將清除所有已上傳的檔案和設定。')) {
        removeFile();
        currentTaskId = null;
        resetGenerationUI();
        goToStep(1);
        showToast('已重置所有設定', 'success');
    }
}

// 工具函數
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function formatDuration(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? [
        parseInt(result[1], 16),
        parseInt(result[2], 16),
        parseInt(result[3], 16)
    ] : [0, 0, 0];
}

function showLoading(show) {
    document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = 'toast show ' + type;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
