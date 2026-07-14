@echo off
chcp 65001 > nul
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║               🎵 Eye Music 音樂視覺化器 🎵                ║
echo ║                                                          ║
echo ║              © 2025 AI MUSIC 可視化生成平台               ║
echo ║              Made with ❤️ by 阿亮老師（曾慶良）           ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM 檢查 Python 是否已安裝
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [錯誤] 未偵測到 Python！請先安裝 Python 3.8 或更高版本。
    echo 下載位置: https://www.python.org/downloads/
    echo.
    echo 按任意鍵退出...
    pause > nul
    exit /b 1
)

echo [✓] Python 已安裝
echo.

REM 檢查虛擬環境
if not exist "venv\" (
    echo [!] 未偵測到虛擬環境，正在建立...
    python -m venv venv
    echo [✓] 虛擬環境建立完成
    echo.
)

REM 啟動虛擬環境
echo [*] 啟動虛擬環境...
call venv\Scripts\activate.bat

REM 檢查依賴套件
echo [*] 檢查依賴套件...
pip show flask > nul 2>&1
if %errorlevel% neq 0 (
    echo [!] 正在安裝依賴套件...
    pip install -r requirements.txt
    echo [✓] 依賴套件安裝完成
    echo.
)

REM 檢查 FFmpeg
echo [*] 檢查 FFmpeg...
ffmpeg -version > nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 未偵測到 FFmpeg！
    echo 請確保已安裝 FFmpeg 並加入系統 PATH
    echo 下載位置: https://ffmpeg.org/download.html
    echo.
    echo 按任意鍵繼續（可能會導致影片生成失敗）...
    pause > nul
) else (
    echo [✓] FFmpeg 已安裝
    echo.
)

REM 建立必要的目錄
if not exist "src\static\uploads\" mkdir src\static\uploads
if not exist "src\static\outputs\" mkdir src\static\outputs

echo [*] 啟動 Eye Music 伺服器...
echo.
echo ════════════════════════════════════════════════════════════
echo  📡 伺服器地址: http://localhost:5000
echo  🌐 請在瀏覽器中開啟上述網址
echo  ⚡ 按 Ctrl+C 停止伺服器
echo ════════════════════════════════════════════════════════════
echo.

REM 檢查 src 目錄是否存在
if not exist "src\" (
    echo.
    echo [錯誤] 找不到 src 目錄！
    echo 請確認你在正確的專案目錄中執行此腳本。
    echo.
    echo 按任意鍵退出...
    pause > nul
    exit /b 1
)

REM 檢查 app.py 是否存在
if not exist "src\app.py" (
    echo.
    echo [錯誤] 找不到 src\app.py 檔案！
    echo 請確認專案檔案是否完整。
    echo.
    echo 按任意鍵退出...
    pause > nul
    exit /b 1
)

REM 啟動應用程式
cd src
echo [*] 正在啟動 Flask 應用程式...
echo.
python app.py

REM 如果程式異常退出
echo.
echo.
echo [!] 程式已停止運行
echo.
pause
