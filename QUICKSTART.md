# 🚀 Eye Music AI 整合 - 快速啟動指南

> 5 分鐘快速上手完整 AI 音樂視覺化系統

---

## ⚡ 快速檢查清單

在開始之前，確認以下項目：

- [ ] Python 3.12+ 已安裝
- [ ] FFmpeg 已安裝並在 PATH 中
- [ ] Google 帳號（用於 Sheets 和 AI Studio）
- [ ] OpenAI 帳號並已儲值（至少 $5 USD）

---

## 📝 步驟 1：安裝依賴（2 分鐘）

```bash
# 1. 進入專案目錄
cd Eye_Music

# 2. 建立虛擬環境
python -m venv venv

# 3. 啟動虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. 安裝依賴
pip install -r requirements.txt
```

**驗證安裝**：
```bash
python -c "import flask, openai, google.generativeai; print('✅ 套件安裝成功')"
```

---

## 🔑 步驟 2：設定 API Keys（3 分鐘）

> **重要提示**：你只需要選擇以下**其中一個** AI 服務，不需要兩個都申請！

### 選項 A：使用 Google Gemini（推薦新手）✅

**優點**：
- ✅ **免費額度高**（每日 60 次請求）
- ✅ 速度快（2-3 秒）
- ✅ 無需儲值

**申請步驟**：
1. 前往 https://makersuite.google.com/app/apikey
2. 登入 Google 帳號
3. 點選「Create API Key」
4. 複製金鑰（`AIzaSy...`）

**適合對象**：初學者、測試用途、預算有限

---

### 選項 B：使用 OpenAI GPT（進階使用者）

**優點**：
- ✅ 文字品質極高
- ✅ 創意性強
- ✅ 支援 GPT-5.6 Terra 最新模型

**缺點**：
- ⚠️ **需要儲值**（至少 $5 USD）
- ⚠️ 成本較高（約 $0.02-0.05/任務）

**申請步驟**：
1. 前往 https://platform.openai.com/api-keys
2. 登入或註冊
3. 點選「Create new secret key」
4. 複製金鑰（`sk-...`）
5. **重要**：前往 Billing 儲值至少 $5

**適合對象**：商業用途、追求最佳品質、預算充足

---

### 🎯 我的建議

- **學習/測試**：選擇 Gemini（免費且夠用）
- **正式專案**：兩個都申請，互相備援
- **商業應用**：優先 GPT-5.6 Terra，輔以 Gemini 降低成本

---

### 2.3 設定環境變數

```bash
# Windows:
copy .env.example .env

# macOS/Linux:
cp .env.example .env
```

編輯 `.env` 檔案，填入你的 API Key：

**如果你選擇 Gemini（選項 A）**：
```env
# 只需填入 Gemini
GOOGLE_AI_API_KEY=AIzaSy你的金鑰

# OpenAI 留空或註解掉
# OPENAI_API_KEY=

# 選填（保持預設即可）
FLASK_ENV=development
DEFAULT_FPS=30
```

**如果你選擇 OpenAI（選項 B）**：
```env
# Gemini 留空或註解掉
# GOOGLE_AI_API_KEY=

# 只需填入 OpenAI
OPENAI_API_KEY=sk-你的金鑰

# 選填（保持預設即可）
FLASK_ENV=development
DEFAULT_FPS=30
```

**如果你兩個都申請了**：
```env
# 兩個都填入，系統會優先使用 Gemini（省錢）
GOOGLE_AI_API_KEY=AIzaSy你的金鑰
OPENAI_API_KEY=sk-你的金鑰
```

**驗證設定**：
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Gemini:', 'OK' if os.getenv('GOOGLE_AI_API_KEY') else '未設定'); print('OpenAI:', 'OK' if os.getenv('OPENAI_API_KEY') else '未設定')"
```

---

## 🎵 步驟 3：測試 Flask 後端（1 分鐘）

```bash
# 啟動伺服器
cd src
python app.py
```

**預期輸出**：
```
    ╔══════════════════════════════════════════════════════════╗
    ║               🎵 Eye Music 音樂視覺化器 🎵                ║
    ╚══════════════════════════════════════════════════════════╝

    📡 伺服器地址: http://localhost:5000
```

**測試 API**：
開啟新終端機，執行：
```bash
curl http://localhost:5000/api/health
```

**預期回應**：
```json
{
  "status": "healthy",
  "service": "Eye Music API",
  "version": "1.0.0"
}
```

✅ **如果看到以上輸出，Flask 後端啟動成功！**

---

## 📊 步驟 4：建立 Google Sheets（5 分鐘）

### 4.1 建立試算表

1. 前往 https://sheets.google.com
2. 建立新試算表，命名為「**Eye Music 任務管理**」

### 4.2 建立工作表

建立以下 5 個工作表（底部點選「+」新增）：
1. `Task_List`
2. `API_Config`
3. `Dashboard`
4. `AI_Prompts`
5. `Execution_Log`

### 4.3 設定 Task_List 欄位

在 `Task_List` 工作表的第 1 行輸入以下標題：

| A | B | C | D | E | F | G | H | I | J | K | L | M | N | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 序號 | 歌曲名稱 | 音樂檔案連結 | 視覺化類型 | 色彩方案 | 解析度 | FPS | AI模型 | 狀態 | AI建議 | 生成時間 | 耗時(秒) | 影片連結 | AI描述 | 錯誤訊息 |

### 4.4 輸入測試資料（第 2 行）

```
1 | 測試歌曲 | (空白) | | | 1080p | 30 | Gemini 3.5 Flash | 待處理 | | | | | |
```

---

## 🔧 步驟 5：安裝 GAS 程式碼（3 分鐘）

### 5.1 開啟 Apps Script

在 Google Sheets 中：
1. 點選「擴充功能」→「Apps Script」
2. 刪除預設的 `function myFunction() {}`

### 5.2 複製程式碼

1. 開啟專案中的 `gas/Code.gs` 檔案
2. 全選複製（Ctrl+A → Ctrl+C）
3. 貼上到 Apps Script 編輯器

### 5.3 儲存並命名

1. 點選「儲存」（磁片圖示）
2. 專案名稱改為「**Eye Music Integration**」

### 5.4 設定腳本屬性（API Keys）

1. 點選左側「專案設定」⚙️
2. 滾動到「腳本屬性」區塊
3. 點選「新增腳本屬性」

**必須設定**：
- `FLASK_URL` = `http://localhost:5000`

**依你的選擇設定（擇一或兩個都填）**：

**選項 A：只用 Gemini**
- `GEMINI_API_KEY` = 你的 Gemini API Key
- `OPENAI_API_KEY` = 留空（不用新增）

**選項 B：只用 OpenAI**
- `GEMINI_API_KEY` = 留空（不用新增）
- `OPENAI_API_KEY` = 你的 OpenAI API Key

**選項 C：兩個都用（互相備援）**
- `GEMINI_API_KEY` = 你的 Gemini API Key
- `OPENAI_API_KEY` = 你的 OpenAI API Key

5. 點選「儲存腳本屬性」

### 5.5 授權執行

1. 回到「編輯器」頁面
2. 點選「執行」按鈕（▶️）
3. 選擇函數 `testGeminiConnection`
4. 首次執行會要求授權：
   - 點選「審查權限」
   - 選擇你的 Google 帳號
   - 點選「進階」
   - 點選「前往 Eye Music Integration (不安全)」
   - 點選「允許」

---

## ✅ 步驟 6：測試完整流程（2 分鐘）

### 6.1 測試 AI 連接

在 Apps Script 編輯器中：
1. 選擇函數 `testGeminiConnection`
2. 點選「執行」▶️
3. 查看日誌（Ctrl/Cmd + Enter）

**預期輸出**：
```
Gemini 測試成功：連接成功
```

### 6.2 測試音樂分析

回到 Google Sheets：
1. 刷新頁面（會看到新選單「🎵 Eye Music」）
2. 選取第 2 行（測試資料）
3. 點選「🎵 Eye Music」→「🤖 AI 分析選中任務」
4. 等待 3-5 秒

**預期結果**：
- D 欄自動填入：`circular` 或其他類型
- E 欄自動填入：`rainbow` 或其他色彩
- J 欄顯示 AI 建議原因

✅ **如果看到以上結果，整合成功！**

---

## 🎬 步驟 7：生成第一個視覺化影片（選用）

### 7.1 準備音樂檔案

1. 準備一個測試音檔（MP3/WAV，建議 < 1 分鐘）
2. 放到 `Eye_Music/src/static/uploads/` 目錄
3. 記住檔名，例如：`test.mp3`

### 7.2 更新 Sheets

在 `Task_List` 第 2 行，C 欄填入：
```
test.mp3
```

### 7.3 生成影片

1. 確保 Flask 伺服器正在運行
2. 在 Sheets 選取第 2 行
3. 點選「🎵 Eye Music」→「▶️ 生成選中任務」
4. 等待生成（約 30-60 秒）

**查看結果**：
- I 欄狀態變為「已完成」
- M 欄顯示下載連結
- N 欄顯示 AI 生成的描述

---

## 🎓 下一步學習

### 完整教學

閱讀 `docs/INTEGRATION_TUTORIAL.md` 學習：
- Module 1: Google Sheets 進階功能
- Module 2: GAS 自動化技巧
- Module 3: AI API 深度應用
- Module 4: Flask 後端擴充
- Module 5: 完整整合實戰

### 實戰應用

1. **批次處理**：輸入 10 首歌曲，使用「批次處理」功能
2. **社群文案**：修改 GAS 程式碼，自動生成多平台文案
3. **成本追蹤**：在 Dashboard 建立 AI 使用統計

---

## 🐛 常見問題快速排查

### Q: Flask 啟動失敗

```bash
# 檢查 Python 版本
python --version  # 應為 3.8+

# 檢查套件
pip list | grep -i flask

# 重新安裝
pip install --upgrade flask flask-socketio
```

### Q: GAS 執行錯誤「未授權」

**解決方案**：
1. Apps Script 編輯器 → 執行任何函數
2. 完成授權流程
3. 刷新 Sheets 頁面

### Q: AI API 回應錯誤

**Gemini 429 錯誤**：
- 超過免費額度，等待重置或升級付費

**OpenAI 401 錯誤**：
- API Key 錯誤或未儲值
- 檢查 `.env` 和 GAS 腳本屬性

### Q: Sheets 選單沒出現

**解決方案**：
1. 確認 GAS 程式碼已儲存
2. 刷新 Sheets 頁面（F5）
3. 清除瀏覽器快取

---

## 📞 需要協助？

- 📘 Facebook: https://www.facebook.com/iddmail
- 🎥 YouTube: https://www.youtube.com/@Liang-yt02
- 🔬 3A科技研究室: https://www.facebook.com/groups/2754139931432955
- 💬 Line 社群: https://line.me/ti/g2/v5KVFRhsemEXe8de3llc9HEdrJTiaiT62P52yA

---

## 🎉 恭喜！

你已經成功建立了一個完整的 AI 驅動音樂視覺化自動生成系統！

**系統能力**：
- ✅ AI 自動分析音樂風格
- ✅ 智能推薦視覺化參數
- ✅ 自動生成影片
- ✅ AI 撰寫影片描述
- ✅ 批次處理大量任務
- ✅ 完整任務管理與統計

**繼續探索**：
- 調整 AI Prompt 優化分析品質
- 整合 YouTube API 自動上傳
- 建立自動化工作流程
- 開發商業化應用

---

**© 2025 Eye Music AI 整合 | Made with ❤️ by 阿亮老師**

🎵 讓 AI 為你的音樂創作視覺魔法 ✨
