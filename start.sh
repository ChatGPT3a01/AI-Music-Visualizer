#!/bin/bash

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║               🎵 Eye Music 音樂視覺化器 🎵                ║"
echo "║                                                          ║"
echo "║              © 2025 AI MUSIC 可視化生成平台               ║"
echo "║              Made with ❤️ by 阿亮老師（曾慶良）           ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# 檢查 Python 是否已安裝
if ! command -v python3 &> /dev/null; then
    echo "[錯誤] 未偵測到 Python3！請先安裝 Python 3.8 或更高版本。"
    exit 1
fi

echo "[✓] Python 已安裝"
echo ""

# 檢查虛擬環境
if [ ! -d "venv" ]; then
    echo "[!] 未偵測到虛擬環境，正在建立..."
    python3 -m venv venv
    echo "[✓] 虛擬環境建立完成"
    echo ""
fi

# 啟動虛擬環境
echo "[*] 啟動虛擬環境..."
source venv/bin/activate

# 檢查依賴套件
echo "[*] 檢查依賴套件..."
if ! pip show flask &> /dev/null; then
    echo "[!] 正在安裝依賴套件..."
    pip install -r requirements.txt
    echo "[✓] 依賴套件安裝完成"
    echo ""
fi

# 檢查 FFmpeg
echo "[*] 檢查 FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "[警告] 未偵測到 FFmpeg！"
    echo "請確保已安裝 FFmpeg"
    echo ""
    echo "macOS: brew install ffmpeg"
    echo "Ubuntu/Debian: sudo apt install ffmpeg"
    echo ""
    read -p "按 Enter 繼續（可能會導致影片生成失敗）..."
else
    echo "[✓] FFmpeg 已安裝"
    echo ""
fi

# 建立必要的目錄
mkdir -p src/static/uploads
mkdir -p src/static/outputs

echo "[*] 啟動 Eye Music 伺服器..."
echo ""
echo "════════════════════════════════════════════════════════════"
echo " 📡 伺服器地址: http://localhost:5000"
echo " 🌐 請在瀏覽器中開啟上述網址"
echo " ⚡ 按 Ctrl+C 停止伺服器"
echo "════════════════════════════════════════════════════════════"
echo ""

# 啟動應用程式
cd src
python3 app.py
