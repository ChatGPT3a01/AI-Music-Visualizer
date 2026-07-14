# 🎓 Eye Music + Google Sheets + AI 整合教學完整指南

> **作者**：阿亮老師（曾慶良）
> **版本**：1.0.0
> **更新日期**：2025-01-07

---

## 📚 目錄

1. [課程概述](#課程概述)
2. [技術架構](#技術架構)
3. [環境準備](#環境準備)
4. [Module 1: Google Sheets 基礎](#module-1-google-sheets-基礎)
5. [Module 2: Google Apps Script 自動化](#module-2-google-apps-script-自動化)
6. [Module 3: AI API 整合](#module-3-ai-api-整合)
7. [Module 4: Flask 後端擴充](#module-4-flask-後端擴充)
8. [Module 5: 完整整合實作](#module-5-完整整合實作)
9. [實戰專案](#實戰專案)
10. [常見問題](#常見問題)

---

## 🎯 課程概述

### 學習目標

本教學將帶你完成一個完整的**音樂視覺化自動生成系統**，整合以下技術：

- ✅ **Google Sheets**：任務管理與數據中心
- ✅ **Google Apps Script (GAS)**：自動化中間層
- ✅ **Gemini 3.5 Flash/Pro**：快速音樂分析與深度創意
- ✅ **GPT-5.6 Terra/GPT-5.6 Terra**：影片描述與社群媒體文案生成
- ✅ **Flask + Python**：音樂視覺化生成後端
- ✅ **完整 API 整合**：前後端串接

### 適合對象

- Python 基礎開發者
- 想學習 Google Apps Script 的工程師
- 對 AI API 整合有興趣的開發者
- 多媒體創作者、音樂工作者

### 預計學習時間

**總時數：15-20 小時**
- Module 1: 2-3 小時
- Module 2: 3-4 小時
- Module 3: 3-4 小時
- Module 4: 2-3 小時
- Module 5: 4-5 小時
- 實戰專案: 2-3 小時

---

## 🏗️ 技術架構

```
┌─────────────────────────────────────────────────────────────┐
│                     使用者介面層                              │
│              Google Sheets + 自訂選單                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   自動化中間層                                │
│         Google Apps Script (GAS)                             │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│   │ Gemini 3.5   │  │ GPT-5.6 Terra/5    │  │ Flask API    │    │
│   │ Flash/Pro    │  │ Integration  │  │ Caller       │    │
│   └──────────────┘  └──────────────┘  └──────────────┘    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   AI 服務層                                   │
│   ┌────────────────────┐    ┌─────────────────────┐        │
│   │  Google AI Studio  │    │  OpenAI Platform    │        │
│   │  Gemini 3.5 API    │    │  GPT-5.6 Terra/5 API      │        │
│   └────────────────────┘    └─────────────────────┘        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   應用後端層                                  │
│              Flask + Python                                  │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│   │ API 端點     │  │ AI 服務模組  │  │ 視覺化引擎   │    │
│   │ Extensions   │  │ ai_service   │  │ Visualizer   │    │
│   └──────────────┘  └──────────────┘  └──────────────┘    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   輸出層                                      │
│              視覺化影片 + 描述文案                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 環境準備

### 1. 系統需求

- **作業系統**：Windows 10/11, macOS 10.14+, Linux
- **Python**：3.12 或以上
- **記憶體**：建議 8GB 以上
- **硬碟空間**：10GB 以上

### 2. 必要軟體安裝

#### 安裝 Python
```bash
# Windows (使用 winget)
winget install Python.Python.3.11

# macOS (使用 Homebrew)
brew install python@3.11

# 驗證安裝
python --version
```

#### 安裝 FFmpeg
```bash
# Windows (使用 Chocolatey)
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install ffmpeg

# 驗證安裝
ffmpeg -version
```

### 3. Python 套件安裝

```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安裝依賴套件
cd Eye_Music
pip install -r requirements.txt
```

### 4. API Keys 申請

#### Google AI Studio (Gemini API)

1. 前往 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登入 Google 帳號
3. 點選「Create API Key」
4. 選擇專案（或建立新專案）
5. 複製 API Key（格式：`AIzaSy...`）

**重要提示**：
- Gemini 3.5 Flash：適合快速分析，成本低
- Gemini 3.1 Pro：適合深度分析，功能強大

#### OpenAI API (GPT-5.6 Terra/GPT-5.6 Terra)

1. 前往 [OpenAI Platform](https://platform.openai.com/api-keys)
2. 登入或註冊帳號
3. 點選「Create new secret key」
4. 設定名稱並複製 API Key（格式：`sk-...`）
5. 儲存金鑰（只會顯示一次！）

**計費提示**：
- 需要先儲值至少 $5 USD
- GPT-5.6 Terra 約 $0.03 / 1K tokens
- GPT-5.6 Terra 約 $0.06 / 1K tokens（預估）

### 5. 環境變數設定

在專案根目錄建立 `.env` 檔案：

```env
# Flask 設定
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Google AI Studio API (Gemini)
GOOGLE_AI_API_KEY=AIzaSy...

# OpenAI API (GPT)
OPENAI_API_KEY=sk-...

# FFmpeg 路徑（如需自訂）
# FFMPEG_BINARY=C:\path\to\ffmpeg.exe
# IMAGEIO_FFMPEG_EXE=C:\path\to\ffmpeg.exe

# 其他設定
MAX_UPLOAD_SIZE=500
DEFAULT_FPS=30
DEFAULT_RESOLUTION=1920x1080
```

---

## 📖 Module 1: Google Sheets 基礎

### 1.1 建立 Google Sheets 工作簿

1. 前往 [Google Sheets](https://sheets.google.com)
2. 建立新試算表，命名為「Eye Music 任務管理」
3. 建立以下工作表：
   - `Task_List`（任務清單）
   - `API_Config`（API 設定）
   - `Dashboard`（統計儀表板）
   - `AI_Prompts`（AI 提示詞模板）
   - `Execution_Log`（執行日誌）

### 1.2 設定任務清單工作表

在 `Task_List` 工作表建立以下欄位（第 1 行）：

| A | B | C | D | E | F | G | H | I | J | K | L | M | N | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 序號 | 歌曲名稱 | 音樂檔案連結 | 視覺化類型 | 色彩方案 | 解析度 | FPS | AI模型 | 狀態 | AI建議 | 生成時間 | 耗時(秒) | 影片連結 | AI描述 | 錯誤訊息 |

**範例資料**（第 2 行）：
```
1 | 夜曲-周杰倫 | https://... | circular | purple | 1080p | 30 | Gemini 3.5 Flash | 待處理 | | | | | |
```

### 1.3 設定資料驗證

選取 D 欄（視覺化類型），設定資料驗證：
- 資料範圍：`D2:D1000`
- 準則：清單來自範圍
- 項目：`bars, circular, piano`

重複以上步驟設定其他欄位：
- E 欄（色彩方案）：`rainbow, fire, ocean, purple`
- F 欄（解析度）：`720p, 1080p, 2K, 4K`
- G 欄（FPS）：`24, 30, 60`
- H 欄（AI 模型）：`Gemini 3.5 Flash, Gemini 3.1 Pro, GPT-5.6 Terra, GPT-5.6 Terra`

### 1.4 設定條件格式

選取 I 欄（狀態），設定條件格式：

1. **待處理**：背景色 `#E8E8E8`（灰色）
2. **AI分析中**：背景色 `#CCE5FF`（淺藍色）
3. **生成中**：背景色 `#FFF4CC`（黃色）
4. **已完成**：背景色 `#D9EAD3`（綠色）
5. **失敗**：背景色 `#F4CCCC`（紅色）

### 1.5 建立統計儀表板

在 `Dashboard` 工作表建立即時統計：

**A1: 總任務數**
```
=COUNTA(Task_List!A:A)-1
```

**A2: 已完成**
```
=COUNTIF(Task_List!I:I,"已完成")
```

**A3: 成功率**
```
=IF(A1>0, A2/A1*100, 0) & "%"
```

---

## 📝 Module 2: Google Apps Script 自動化

### 2.1 開啟腳本編輯器

1. 在 Google Sheets 中，點選「擴充功能」→「Apps Script」
2. 刪除預設的 `function myFunction() {}`
3. 複製 `gas/Code.gs` 的內容貼上

### 2.2 設定腳本屬性（儲存 API Keys）

1. 在 Apps Script 編輯器中，點選左側「專案設定」⚙️
2. 滾動到「腳本屬性」區塊
3. 點選「新增腳本屬性」
4. 新增以下屬性：
   - `GEMINI_API_KEY`：你的 Gemini API Key
   - `OPENAI_API_KEY`：你的 OpenAI API Key
   - `FLASK_URL`：`http://localhost:5000`（或你的伺服器 URL）

### 2.3 測試 GAS 功能

#### 測試 1：測試 Gemini 連接

在 Apps Script 編輯器中：
1. 選擇函數 `testGeminiConnection`
2. 點選「執行」▶️
3. 首次執行需要授權（按照提示完成）
4. 查看執行日誌（Ctrl/Cmd + Enter）

**預期輸出**：
```
✅ Gemini API 連接成功！

回應：連接成功
```

#### 測試 2：測試音樂分析

1. 在 `Task_List` 輸入測試資料：
   ```
   1 | 告白氣球-周杰倫 | (留空) | | | 1080p | 30 | Gemini 3.5 Flash | 待處理
   ```
2. 選取該行
3. 點選選單「🎵 Eye Music」→「🤖 AI 分析選中任務」
4. 等待執行完成（約 3-5 秒）

**預期結果**：
- D 欄自動填入：`circular`
- E 欄自動填入：`rainbow`
- J 欄顯示 AI 建議

### 2.4 建立自訂選單

GAS 程式碼中的 `onOpen()` 函數會自動建立選單，刷新頁面後可看到：

```
🎵 Eye Music
├── 🤖 AI 分析選中任務
├── ▶️ 生成選中任務
├── ────────────────
├── 📊 批次處理所有待處理任務
├── ────────────────
├── 🔄 更新任務狀態
├── 🧹 清理失敗任務
├── ────────────────
├── ⚙️ 設定 API Keys
└── 📋 查看使用統計
```

---

## 🤖 Module 3: AI API 整合

### 3.1 Gemini API 基礎

#### 理解 Gemini 模型差異

| 特性 | Gemini 3.5 Flash | Gemini 3.1 Pro |
|------|------------------|----------------|
| **速度** | 極快（< 2 秒） | 較慢（5-10 秒） |
| **成本** | 低 | 中等 |
| **適用場景** | 快速分析、參數推薦 | 深度分析、創意建議 |
| **Context 長度** | 32K tokens | 128K tokens |
| **推薦用途** | 批次處理 | 單一深度任務 |

#### 範例：基本呼叫

```javascript
// GAS 中呼叫 Gemini
function callGeminiAPI(prompt, modelType = 'flash') {
  const apiKey = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
  const model = modelType === 'pro' ? 'gemini-3.1-pro-preview' : 'gemini-3.5-flash';
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

  const payload = {
    contents: [{
      parts: [{ text: prompt }]
    }]
  };

  const response = UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  });

  return JSON.parse(response.getContentText());
}
```

### 3.2 OpenAI GPT API 整合

#### GPT-5.6 Terra vs GPT-5.6 Terra

| 特性 | GPT-5.6 Terra | GPT-5.6 Terra |
|------|---------|--------|
| **推理能力** | 強 | 極強 |
| **創意性** | 高 | 極高 |
| **成本** | $0.03/1K tokens | $0.06/1K tokens（預估） |
| **適用場景** | 描述生成 | 複雜文案創作 |
| **Context 長度** | 128K tokens | 200K tokens（預估） |

#### 範例：GPT 呼叫

```javascript
// GAS 中呼叫 OpenAI GPT
function callGPTAPI(prompt, model = 'gpt-5.6-terra') {
  const apiKey = PropertiesService.getScriptProperties().getProperty('OPENAI_API_KEY');
  const url = 'https://api.openai.com/v1/chat/completions';

  const payload = {
    model: model,
    messages: [
      { role: 'system', content: '你是音樂視覺化專家' },
      { role: 'user', content: prompt }
    ]
  };

  const response = UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    headers: { 'Authorization': `Bearer ${apiKey}` },
    payload: JSON.stringify(payload)
  });

  return JSON.parse(response.getContentText());
}
```

### 3.3 Prompt Engineering 技巧

#### 技巧 1：結構化輸出

❌ **不好的 Prompt**：
```
分析這首歌的風格
```

✅ **好的 Prompt**：
```
分析歌曲「{歌名}」，以 JSON 格式回傳：
{
  "visualization_type": "bars/circular/piano",
  "color_scheme": "rainbow/fire/ocean/purple",
  "reason": "選擇理由"
}
```

#### 技巧 2：Few-Shot Learning

```javascript
const prompt = `
範例 1：
歌曲：安靜 - 周杰倫
回應：{"visualization_type": "piano", "color_scheme": "ocean"}

範例 2：
歌曲：雙節棍 - 周杰倫
回應：{"visualization_type": "bars", "color_scheme": "fire"}

現在請分析：
歌曲：${songName}
回應：
`;
```

#### 技巧 3：溫度控制

```javascript
// 需要穩定結果（參數推薦）
temperature: 0.3

// 需要創意內容（文案生成）
temperature: 0.8
```

### 3.4 成本優化策略

#### 策略 1：快速任務用 Flash

```javascript
// 批次處理：使用 Gemini Flash
for (task of tasks) {
  const analysis = callGeminiAPI(prompt, 'flash');  // 快速且便宜
}
```

#### 策略 2：重要任務用 Pro/GPT

```javascript
// 單一重要任務：使用 Gemini Pro 或 GPT
const creativeIdea = callGeminiAPI(prompt, 'pro');  // 深度分析
```

#### 策略 3：結果快取

```javascript
// 快取常見歌曲的分析結果
const cache = CacheService.getScriptCache();
const cacheKey = `analysis_${songName}`;
let result = cache.get(cacheKey);

if (!result) {
  result = callGeminiAPI(prompt);
  cache.put(cacheKey, JSON.stringify(result), 3600);  // 快取 1 小時
}
```

---

## 🔧 Module 4: Flask 後端擴充

### 4.1 理解新增的 API 端點

專案已新增 `src/api_extensions.py`，提供以下端點：

#### 端點清單

| 端點 | 方法 | 用途 |
|------|------|------|
| `/api/health` | GET | 健康檢查 |
| `/api/gas/generate` | POST | GAS 專用生成端點 |
| `/api/gas/status/<job_id>` | GET | 查詢任務狀態 |
| `/api/gas/batch/status` | POST | 批次查詢狀態 |
| `/api/gas/tasks` | GET | 列出所有任務 |
| `/api/gas/task/<job_id>` | DELETE | 刪除任務 |

### 4.2 啟動 Flask 伺服器

```bash
# 確保在 Eye_Music 目錄下
cd Eye_Music

# 啟動伺服器
# Windows:
start_windows.bat

# macOS/Linux:
./start.sh

# 或手動啟動
cd src
python app.py
```

**預期輸出**：
```
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║               🎵 Eye Music 音樂視覺化器 🎵                ║
    ║                                                          ║
    ║              Web 版本 - 正在啟動服務器...                 ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝

    📡 伺服器地址: http://localhost:5000
    🌐 網頁界面: http://localhost:5000
```

### 4.3 測試 API 端點

#### 測試 1：健康檢查

```bash
curl http://localhost:5000/api/health
```

**預期回應**：
```json
{
  "status": "healthy",
  "service": "Eye Music API",
  "version": "1.0.0",
  "timestamp": "2025-01-07T10:30:00"
}
```

#### 測試 2：GAS 生成端點

使用 Postman 或 curl：

```bash
curl -X POST http://localhost:5000/api/gas/generate \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test_001",
    "song_name": "測試歌曲",
    "audio_url": "path/to/audio.mp3",
    "visualization_type": "circular",
    "color_scheme": "rainbow",
    "resolution": "1080p",
    "fps": 30
  }'
```

**預期回應**：
```json
{
  "success": true,
  "job_id": "test_001",
  "message": "任務已接收並開始處理",
  "estimated_time": 45,
  "status_url": "/api/gas/status/test_001"
}
```

### 4.4 整合 AI 服務模組

Flask 後端已建立 `src/services/ai_service.py`，使用方式：

```python
from services import analyze_music_style, generate_video_description

# 分析音樂風格（使用 Gemini Flash）
analysis = analyze_music_style("夜曲 - 周杰倫")
print(analysis)
# 輸出：{'visualization_type': 'piano', 'color_scheme': 'purple', ...}

# 生成影片描述（使用 GPT-5.6 Terra）
description = generate_video_description("夜曲", "piano", "purple")
print(description)
# 輸出：「沉浸在周杰倫《夜曲》的視覺詩篇中...」
```

---

## 🚀 Module 5: 完整整合實作

### 5.1 端到端流程測試

#### 步驟 1：準備測試資料

在 Google Sheets 的 `Task_List` 輸入：

```
1 | 稻香-周杰倫 | [本地音檔路徑或 URL] | | | 1080p | 30 | Gemini 3.5 Flash | 待處理
```

#### 步驟 2：執行 AI 分析

1. 選取該行
2. 點選「🎵 Eye Music」→「🤖 AI 分析選中任務」
3. 等待 3-5 秒

**結果**：
- D 欄自動填入視覺化類型
- E 欄自動填入色彩方案
- J 欄顯示 AI 建議原因

#### 步驟 3：生成視覺化影片

1. 確保 Flask 伺服器正在執行
2. 選取同一行
3. 點選「🎵 Eye Music」→「▶️ 生成選中任務」

**過程**：
- GAS 呼叫 Flask API
- Flask 處理音訊並生成影片
- 完成後自動更新 Sheets（狀態、下載連結、描述）

#### 步驟 4：查看結果

- I 欄狀態變為「已完成」
- M 欄顯示下載連結
- N 欄顯示 AI 生成的影片描述

### 5.2 批次處理演練

#### 準備 10 筆測試資料

在 `Task_List` 輸入 10 首不同風格的歌曲：

```
2 | 七里香-周杰倫 | ... | | | 1080p | 30 | Gemini 3.5 Flash | 待處理
3 | 青花瓷-周杰倫 | ... | | | 1080p | 30 | Gemini 3.5 Flash | 待處理
4 | 雙節棍-周杰倫 | ... | | | 1080p | 30 | Gemini 3.5 Flash | 待處理
... (共 10 筆)
```

#### 執行批次處理

點選「🎵 Eye Music」→「📊 批次處理所有待處理任務」

**流程**：
1. GAS 自動逐行處理
2. 每筆先 AI 分析
3. 然後呼叫 Flask 生成
4. 更新狀態並寫回 Sheets
5. 完成後顯示統計

**預期耗時**：
- 10 筆任務約 5-10 分鐘（取決於音檔長度）

### 5.3 錯誤處理與重試

#### 情境 1：AI API 失敗

如果 Gemini API 失敗：
- GAS 會自動使用預設參數
- 在 O 欄記錄錯誤訊息
- 任務仍可繼續生成

#### 情境 2：Flask 伺服器無回應

如果 Flask 無法連接：
- GAS 會回傳錯誤
- 任務狀態標記為「失敗」
- 可使用「🧹 清理失敗任務」重置

#### 情境 3：影片生成失敗

如果影片生成失敗：
- Flask 回傳錯誤訊息
- GAS 寫入 O 欄
- 可檢查錯誤原因並重試

---

## 💡 實戰專案

### 專案 1：自動化社群媒體發布流程

**目標**：生成影片後自動產生多平台文案

**實作步驟**：

1. 在 `Task_List` 新增欄位：
   - P: YouTube 標題
   - Q: Instagram 文案
   - R: Facebook 貼文

2. 修改 GAS 的 `generateSelectedTasks()` 函數：

```javascript
// 在生成完成後，呼叫 GPT-5.6 Terra 生成社群媒體內容
const socialContent = generateSocialMediaContent(task.songName, description);

// 寫入 Sheets
sheet.getRange(task.row, 16).setValue(socialContent.youtube_title);      // P欄
sheet.getRange(task.row, 17).setValue(socialContent.instagram_caption);  // Q欄
sheet.getRange(task.row, 18).setValue(socialContent.facebook_post);      // R欄
```

3. 測試完整流程

### 專案 2：智能參數優化系統

**目標**：根據歷史數據優化參數推薦

**實作步驟**：

1. 在 `Dashboard` 建立「最受歡迎組合」統計
2. 分析哪些視覺化類型 + 色彩方案組合最常用
3. 將統計結果加入 AI Prompt，提升推薦準確度

```javascript
// 在 AI 分析時加入歷史數據
const popularCombos = getPopularCombinations();
const enhancedPrompt = `
${basePrompt}

參考歷史數據，最受歡迎的組合：
${JSON.stringify(popularCombos)}
`;
```

### 專案 3：成本追蹤儀表板

**目標**：即時追蹤 AI API 使用成本

**實作步驟**：

1. 在 `API_Config` 設定每個 API 的單價
2. 在 `Execution_Log` 記錄每次呼叫的 Token 用量
3. 在 `Dashboard` 建立成本統計圖表
4. 設定預算警示（超過每日限額時發送通知）

---

## ❓ 常見問題

### Q1: Gemini API 回應「429 Too Many Requests」

**原因**：超過免費額度或速率限制

**解決方案**：
1. 在 GAS 中加入重試機制：
```javascript
function callGeminiAPIWithRetry(prompt, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return callGeminiAPI(prompt);
    } catch (e) {
      if (i === maxRetries - 1) throw e;
      Utilities.sleep(2000 * (i + 1));  // 指數退避
    }
  }
}
```

2. 升級到付費方案（Gemini Pro）

### Q2: OpenAI API 顯示「Insufficient credits」

**原因**：帳戶餘額不足

**解決方案**：
1. 前往 [OpenAI Billing](https://platform.openai.com/account/billing)
2. 儲值至少 $5 USD
3. 檢查每月用量限制

### Q3: GAS 執行逾時（6 分鐘限制）

**原因**：批次處理太多任務

**解決方案**：
1. 分批處理，每次最多 5 筆
2. 使用觸發器（Trigger）設定定時執行：
```javascript
function setupHourlyTrigger() {
  ScriptApp.newTrigger('batchProcessAllTasks')
    .timeBased()
    .everyHours(1)
    .create();
}
```

### Q4: Flask 生成影片很慢

**原因**：CPU 渲染影片耗時

**優化方案**：
1. 降低解析度（1080p → 720p）
2. 降低 FPS（30 → 24）
3. 使用 GPU 加速（需安裝 CUDA）
4. 部署到更強大的伺服器

### Q5: Google Sheets 公式錯誤

**常見錯誤**：`#REF!`、`#VALUE!`

**檢查項目**：
1. 工作表名稱是否正確
2. 欄位範圍是否正確
3. 資料類型是否匹配

---

## 📚 延伸學習資源

### 官方文件

- [Google Apps Script 文件](https://developers.google.com/apps-script)
- [Gemini API 文件](https://ai.google.dev/docs)
- [OpenAI API 文件](https://platform.openai.com/docs)
- [Flask 文件](https://flask.palletsprojects.com/)

### 推薦影片教學

- [Google Sheets 進階技巧](https://www.youtube.com/@Liang-yt02)
- [GAS 自動化實戰](https://www.youtube.com/@Liang-yt02)

### 社群支援

- [3A科技研究室 Facebook 社團](https://www.facebook.com/groups/2754139931432955)
- [Line 社群](https://line.me/ti/g2/v5KVFRhsemEXe8de3llc9HEdrJTiaiT62P52yA)

---

## 🎓 結業專題建議

完成本教學後，可挑戰以下專題：

1. **音樂串流整合**：整合 Spotify/YouTube API 自動抓取音樂
2. **自動上傳功能**：影片生成後自動上傳到 YouTube
3. **A/B 測試系統**：生成多個版本，分析哪個效果最好
4. **商業化方案**：接單系統 + 付款整合

---

## 👨‍💻 關於作者

**阿亮老師（曾慶良）**

- 📘 Facebook: [https://www.facebook.com/iddmail](https://www.facebook.com/iddmail)
- 🎥 YouTube: [https://www.youtube.com/@Liang-yt02](https://www.youtube.com/@Liang-yt02)
- 🔬 3A科技研究室: [https://www.facebook.com/groups/2754139931432955](https://www.facebook.com/groups/2754139931432955)

---

**© 2025 Eye Music 整合教學 | Made with ❤️ by 阿亮老師**
