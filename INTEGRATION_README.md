# 🎓 Eye Music + Google Sheets + AI 整合專案

> **完整的音樂視覺化自動生成教學系統**
> 整合 Google Sheets、GAS、Gemini 3.5、GPT-5.6 Terra/5、Flask 與 Python

---

## 🌟 專案特色

本專案在原有的 Eye Music 音樂視覺化平台基礎上，新增了完整的 AI 自動化與 Google Sheets 整合功能：

### ✨ 新增功能亮點

1. **🤖 AI 智能分析**
   - Gemini 3.5 Flash：快速音樂風格分析（< 2秒）
   - Gemini 3.1 Pro：深度創意建議
   - GPT-5.6 Terra：專業影片描述生成
   - GPT-5.6 Terra：多平台社群媒體文案

2. **📊 Google Sheets 任務管理**
   - 視覺化任務清單介面
   - 即時狀態追蹤與統計
   - 批次處理自動化
   - 完整執行日誌

3. **🔗 Google Apps Script 中間層**
   - 自訂選單操作
   - 無縫串接 AI API
   - 自動呼叫 Flask 後端
   - 錯誤處理與重試機制

4. **🚀 擴充的 Flask API**
   - GAS 專用端點
   - 批次狀態查詢
   - 任務管理功能
   - RESTful API 設計

---

## 📁 專案結構

```
Eye_Music/
├── src/
│   ├── app.py                      # Flask 主應用（已整合 API 擴充）
│   ├── api_extensions.py           # 🆕 GAS 整合 API 端點
│   ├── services/                   # 🆕 服務模組
│   │   ├── __init__.py
│   │   └── ai_service.py           # 🆕 AI 服務整合（Gemini + GPT）
│   ├── core/
│   │   └── visualizer.py           # 視覺化核心引擎
│   ├── templates/
│   └── static/
│
├── gas/                             # 🆕 Google Apps Script
│   └── Code.gs                      # 🆕 完整 GAS 程式碼
│
├── docs/                            # 🆕 教學文件
│   ├── google-sheets-template.md   # 🆕 Google Sheets 模板說明
│   └── INTEGRATION_TUTORIAL.md     # 🆕 完整整合教學（15-20小時課程）
│
├── requirements.txt                 # Python 依賴（已更新 AI 套件）
├── .env.example                     # 🆕 完整環境變數範例（含 AI API Keys）
├── README.md                        # 原專案說明
├── INTEGRATION_README.md            # 🆕 本文件
└── ...
```

---

## 🚀 快速開始

### 1️⃣ 環境準備

#### 安裝 Python 依賴

```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安裝依賴（已包含 AI API 套件）
pip install -r requirements.txt
```

#### 設定環境變數

```bash
# 複製環境變數範例
cp .env.example .env

# 編輯 .env，填入你的 API Keys：
# - GOOGLE_AI_API_KEY（Gemini）
# - OPENAI_API_KEY（GPT）
```

### 2️⃣ 申請 AI API Keys（擇一即可）

> **重要**：你只需要選擇以下**其中一個** AI 服務，不需要兩個都申請！

#### 選項 A：Google AI Studio - Gemini（推薦新手）✅

**優點**：免費額度高、速度快、無需儲值

1. 前往 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 建立 API Key
3. 複製金鑰（格式：`AIzaSy...`）

#### 選項 B：OpenAI Platform - GPT（進階使用者）

**優點**：品質極高、創意性強

**注意**：需要儲值至少 $5 USD

1. 前往 [OpenAI API Keys](https://platform.openai.com/api-keys)
2. 建立 Secret Key
3. 儲值至少 $5 USD
4. 複製金鑰（格式：`sk-...`）

#### 選項 C：兩個都申請（最佳方案）

- **Gemini** 用於快速批次處理（省錢）
- **OpenAI** 用於重要任務（品質優先）
- 互相備援，一個故障時自動切換

### 3️⃣ 建立 Google Sheets

1. 前往 [Google Sheets](https://sheets.google.com)
2. 建立新試算表：「Eye Music 任務管理」
3. 依照 `docs/google-sheets-template.md` 建立工作表：
   - `Task_List`（任務清單）
   - `API_Config`（API 設定）
   - `Dashboard`（儀表板）
   - `AI_Prompts`（提示詞模板）
   - `Execution_Log`（執行日誌）

### 4️⃣ 安裝 GAS 程式碼

1. 在 Google Sheets 中，點選「擴充功能」→「Apps Script」
2. 複製 `gas/Code.gs` 的內容貼上
3. 設定腳本屬性（儲存 API Keys）：
   - 點選「專案設定」⚙️
   - 新增腳本屬性：
     - `GEMINI_API_KEY`
     - `OPENAI_API_KEY`
     - `FLASK_URL`（預設：`http://localhost:5000`）

### 5️⃣ 啟動 Flask 伺服器

```bash
# Windows
start_windows.bat

# macOS/Linux
./start.sh

# 或手動啟動
cd src
python app.py
```

### 6️⃣ 測試完整流程

1. 在 Google Sheets `Task_List` 輸入測試資料：
   ```
   1 | 夜曲-周杰倫 | [音檔路徑] | | | 1080p | 30 | Gemini 3.5 Flash | 待處理
   ```

2. 選取該行，點選「🎵 Eye Music」→「🤖 AI 分析選中任務」

3. AI 自動填入參數後，點選「▶️ 生成選中任務」

4. 等待生成完成，查看結果：
   - 影片下載連結
   - AI 生成的描述文字

---

## 📚 完整教學

請參閱 **[docs/INTEGRATION_TUTORIAL.md](docs/INTEGRATION_TUTORIAL.md)**，包含：

### 課程模組（總時數 15-20 小時）

- **Module 1**：Google Sheets 基礎（2-3 小時）
- **Module 2**：Google Apps Script 自動化（3-4 小時）
- **Module 3**：AI API 整合（3-4 小時）
- **Module 4**：Flask 後端擴充（2-3 小時）
- **Module 5**：完整整合實作（4-5 小時）
- **實戰專案**：延伸應用（2-3 小時）

### 教學內容

- ✅ 詳細步驟說明
- ✅ 程式碼範例
- ✅ 常見問題解答
- ✅ Prompt Engineering 技巧
- ✅ 成本優化策略
- ✅ 實戰專題建議

---

## 🤖 AI 模型使用指南

### Gemini 3.5 Flash

**適用場景**：
- ✅ 快速音樂風格分析
- ✅ 批次任務處理
- ✅ 參數推薦
- ✅ 成本敏感型應用

**特性**：
- 速度極快（< 2 秒）
- 成本低廉
- 32K Context

### Gemini 3.1 Pro

**適用場景**：
- ✅ 深度創意分析
- ✅ 複雜音樂理論
- ✅ 色彩心理學研究
- ✅ 目標觀眾分析

**特性**：
- 推理能力強
- 128K Context
- 回應品質高

### GPT-5.6 Terra

**適用場景**：
- ✅ 影片描述生成
- ✅ 專業文案撰寫
- ✅ SEO 優化內容
- ✅ 多語言支援

**特性**：
- 創意性高
- 文字流暢
- 128K Context

### GPT-5.6 Terra

**適用場景**：
- ✅ 多平台文案生成
- ✅ 複雜推理任務
- ✅ 創意內容產出
- ✅ 情感分析

**特性**：
- 最強推理能力
- 極高創意性
- 200K Context（預估）

---

## 🎯 實戰應用範例

### 範例 1：自動批次處理 100 首歌曲

```javascript
// 在 Google Sheets 中
// 1. 輸入 100 筆歌曲資料
// 2. 點選「📊 批次處理所有待處理任務」
// 3. GAS 自動逐筆執行：
//    - AI 分析（Gemini Flash）
//    - 參數填入
//    - 呼叫 Flask 生成
//    - 回寫結果
```

### 範例 2：多平台文案一鍵生成

```javascript
// 生成影片後自動產生：
// - YouTube 標題與描述
// - Instagram 貼文
// - Facebook 文案
// - Twitter 推文
// - TikTok 標籤
```

### 範例 3：成本追蹤與預算控制

```javascript
// Dashboard 自動統計：
// - AI API 呼叫次數
// - 各模型使用分佈
// - 預估總費用
// - 超過預算警示
```

---

## 📊 API 端點總覽

### 原有端點

- `GET /` - 網頁界面
- `POST /api/upload` - 上傳音檔
- `POST /api/generate` - 生成影片
- `GET /api/task/<task_id>` - 查詢任務狀態
- `GET /api/download/<filename>` - 下載影片

### 🆕 新增端點（GAS 整合）

- `GET /api/health` - 健康檢查
- `POST /api/gas/generate` - GAS 專用生成端點
- `GET /api/gas/status/<job_id>` - 查詢任務狀態
- `POST /api/gas/batch/status` - 批次查詢狀態
- `GET /api/gas/tasks` - 列出所有任務
- `DELETE /api/gas/task/<job_id>` - 刪除任務

---

## 💰 成本預估

### Gemini 3.5 API

| 模型 | 輸入 | 輸出 | 單次分析 |
|------|------|------|----------|
| Flash | 免費額度內 | 免費額度內 | ~$0.001 |
| Pro | $0.00025/1K tokens | $0.0005/1K tokens | ~$0.005 |

### OpenAI GPT API

| 模型 | 輸入 | 輸出 | 單次生成 |
|------|------|------|----------|
| GPT-5.6 Terra | $0.015/1K tokens | $0.03/1K tokens | ~$0.02 |
| GPT-5.6 Terra | $0.03/1K tokens（預估） | $0.06/1K tokens（預估） | ~$0.05 |

### 建議成本策略

```
單一任務完整流程：
- AI 分析（Gemini Flash）: $0.001
- 描述生成（GPT-5.6 Terra）: $0.02
- 社群文案（GPT-5.6 Terra）: $0.05（選用）

總計：約 $0.02-0.07 / 任務
批次 100 首：約 $2-7
```

---

## 🔧 進階功能

### Celery 非同步任務處理（選用）

```bash
# 安裝 Redis
# Windows: 下載 Redis for Windows
# macOS: brew install redis
# Linux: sudo apt install redis-server

# 啟動 Redis
redis-server

# 啟動 Celery Worker
celery -A src.celery_worker worker --loglevel=info
```

### Google Sheets API 直接存取（選用）

```python
# 使用 gspread 直接操作 Sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Eye Music 任務管理').sheet1
```

---

## 🐛 常見問題

### Q1: GAS 執行逾時（6 分鐘限制）

**解決方案**：
- 分批處理，每次最多 5 筆
- 使用時間觸發器定時執行

### Q2: Gemini API 回應 429 錯誤

**解決方案**：
- 加入重試機制與指數退避
- 升級到付費方案

### Q3: Flask 伺服器連接失敗

**檢查項目**：
- Flask 是否正在運行
- 防火牆設定
- GAS 中 FLASK_URL 設定是否正確

### Q4: AI 回應格式錯誤

**解決方案**：
- 優化 Prompt（要求「直接回傳 JSON」）
- 加入 JSON 清理邏輯
- 使用 try-catch 錯誤處理

---

## 🤝 貢獻與支援

### 學習資源

- 📘 [阿亮老師 Facebook](https://www.facebook.com/iddmail)
- 🎥 [阿亮老師 YouTube](https://www.youtube.com/@Liang-yt02)
- 🔬 [3A科技研究室](https://www.facebook.com/groups/2754139931432955)
- 💬 [Line 社群](https://line.me/ti/g2/v5KVFRhsemEXe8de3llc9HEdrJTiaiT62P52yA)

### 問題回報

如遇到問題，請提供以下資訊：
1. 錯誤訊息截圖
2. 執行環境（作業系統、Python 版本）
3. 完整的錯誤堆疊（Error Stack）
4. 重現步驟

---

## 📄 授權

MIT License

---

## 👨‍💻 作者

**阿亮老師（曾慶良）**

專業技術講師，專注於：
- Python 全端開發
- AI 應用整合
- Google Workspace 自動化
- 音視訊多媒體處理

---

**© 2025 Eye Music 整合專案 | Made with ❤️ by 阿亮老師**

🎵 讓 AI 為你的音樂創作視覺魔法 ✨
