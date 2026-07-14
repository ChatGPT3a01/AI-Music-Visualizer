# 🎵 Eye Music - AI 音樂視覺化生成平台

一個基於 Web 的音樂視覺化工具，能夠將音頻檔案轉換成精美的視覺化影片。

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## ✨ 功能特色

- 🎨 **多種視覺化類型**
  - 頻譜能量條
  - 圓形放射狀頻譜
  - 鋼琴瀑布流

- 🌈 **豐富的色彩方案**
  - 彩虹色
  - 火焰色
  - 海洋色
  - 紫色系

- ⚙️ **靈活的參數設定**
  - 自訂影片解析度（720p - 4K）
  - 可調整幀率（24-60 FPS）
  - 頻譜高度倍率調整
  - 透明度控制
  - 自訂背景顏色

- 🚀 **現代化的 Web 界面**
  - 拖放檔案上傳
  - 即時參數預覽
  - 進度條顯示
  - WebSocket 即時通知

- 📱 **響應式設計**
  - 支援桌面和移動設備
  - 流暢的使用者體驗

## 🖥️ 系統需求

### 最低需求
- Windows 10/11, macOS 10.14+, 或 Linux
- Python 3.12 或更高版本
- 4GB RAM
- 5GB 可用磁碟空間

### 推薦配置
- Windows 11, macOS 12+, 或 Linux
- Python 3.12+
- 8GB+ RAM
- 10GB+ 可用磁碟空間
- 支援硬體加速的顯示卡

## 📦 安裝步驟

### 1. 克隆或下載專案

```bash
git clone https://github.com/yourusername/eye-music.git
cd eye-music
```

### 2. 建立虛擬環境（推薦）

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 4. 安裝 FFmpeg

**Windows:**
1. 下載 FFmpeg: https://ffmpeg.org/download.html
2. 解壓縮到 `C:\ffmpeg`
3. 將 `C:\ffmpeg\bin` 加入系統 PATH

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 5. 環境變數設定（可選）

複製 `.env.example` 為 `.env` 並根據需要修改：

```bash
cp .env.example .env
```

## 🚀 啟動應用程式

### Windows

雙擊執行 `start_windows.bat`，或在命令提示字元中執行：

```bash
start_windows.bat
```

### macOS/Linux

執行啟動腳本：

```bash
chmod +x start.sh
./start.sh
```

### 手動啟動

```bash
cd src
python app.py
```

## 📖 使用說明

1. **開啟瀏覽器**
   - 訪問 `http://localhost:5000`

2. **上傳音樂檔案**
   - 拖放音頻檔案到上傳區域
   - 或點擊選擇檔案
   - 支援格式：MP3, WAV, FLAC, OGG, M4A, AAC

3. **設定視覺化參數**
   - 選擇視覺化類型
   - 調整色彩方案
   - 設定影片解析度和幀率
   - 調整頻譜高度和透明度

4. **生成影片**
   - 點擊「開始生成」按鈕
   - 等待處理完成
   - 下載生成的視覺化影片

## 📁 專案結構

```
Eye_Music/
├── src/
│   ├── app.py                 # Flask 主應用程式
│   ├── core/
│   │   ├── __init__.py
│   │   └── visualizer.py      # 視覺化核心引擎
│   ├── templates/
│   │   └── index.html         # 前端頁面
│   └── static/
│       ├── css/
│       │   └── style.css      # 樣式表
│       ├── js/
│       │   └── app.js         # 前端邏輯
│       ├── uploads/           # 上傳檔案目錄
│       └── outputs/           # 輸出影片目錄
├── old/                       # 舊版本檔案
├── requirements.txt           # Python 依賴套件
├── .env.example              # 環境變數範例
├── .gitignore
├── start_windows.bat         # Windows 啟動腳本
├── start.sh                  # macOS/Linux 啟動腳本
└── README.md                 # 本文件
```

## 🎨 視覺化類型說明

### 頻譜能量條
經典的頻譜視覺化，將音頻的頻率能量顯示為垂直的能量條，適合節奏感強的音樂。

### 圓形頻譜
將頻譜以圓形放射狀的方式呈現，創造出動感十足的視覺效果。

### 鋼琴瀑布流
以音符瀑布的方式展示音樂的音高變化，適合旋律性強的音樂。

## 🛠️ 進階設定

### 自訂 FFmpeg 路徑

在 `.env` 檔案中設定：

```env
FFMPEG_BINARY=C:\path\to\ffmpeg.exe
IMAGEIO_FFMPEG_EXE=C:\path\to\ffmpeg.exe
```

### 修改上傳限制

在 `src/app.py` 中修改：

```python
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB
```

### 自訂預設模板

在 `src/app.py` 的 `get_presets()` 函數中新增或修改預設配置。

## 🐛 故障排除

### FFmpeg 找不到

**Windows:**
```bash
where ffmpeg
```
如果沒有輸出，請確認 FFmpeg 已正確安裝並加入 PATH。

**macOS/Linux:**
```bash
which ffmpeg
```

### 套件安裝失敗

嘗試升級 pip：
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 影片生成失敗

1. 檢查磁碟空間是否足夠
2. 確認音頻檔案格式正確
3. 查看日誌輸出中的錯誤訊息

### Port 5000 已被占用

修改 `src/app.py` 最後一行：
```python
socketio.run(app, host='0.0.0.0', port=8080, debug=True)
```

## 📝 更新日誌

### Version 1.0.0 (2025-01-06)
- ✨ 初始版本發布
- 🎨 支援三種視覺化類型
- 🌈 四種色彩方案
- 🚀 Web 界面
- 📊 即時進度顯示
- 📱 響應式設計

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 授權

MIT License

## 👨‍💻 作者資訊

**阿亮老師（曾慶良）**

- 📘 Facebook: [https://www.facebook.com/iddmail](https://www.facebook.com/iddmail)
- 🎥 YouTube: [https://www.youtube.com/@Liang-yt02](https://www.youtube.com/@Liang-yt02)
- 🔬 3A科技研究室: [https://www.facebook.com/groups/2754139931432955](https://www.facebook.com/groups/2754139931432955)
- 💬 Line 社群: [https://line.me/ti/g2/v5KVFRhsemEXe8de3llc9HEdrJTiaiT62P52yA](https://line.me/ti/g2/v5KVFRhsemEXe8de3llc9HEdrJTiaiT62P52yA)

---

© 2025 AI MUSIC 可視化生成平台
Made with ❤️ by 阿亮老師（曾慶良）
