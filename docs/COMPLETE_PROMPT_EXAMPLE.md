# 🎯 完整提示詞範例 - AI 音樂視覺化專案

> 這是一個可以直接提供給 AI 助手（如 Claude、ChatGPT）的完整提示詞範例

---

## 📝 基礎版提示詞（原始需求）

```
我要創作一個音樂視覺化 Web 專案，需求如下：

1. 使用 Python + Flask 建立後端（Port 5000）

2. 提供 Web 界面讓使用者上傳音樂檔案

3. 可以在瀏覽器中設定視覺化參數（色彩方案、解析度、幀率等）

4. 支援三種視覺化效果：
   - 頻譜能量條
   - 圓形頻譜
   - 鋼琴瀑布流

5. 使用 librosa 分析音頻、moviepy 生成影片

6. 加入 WebSocket 即時顯示生成進度

7. 生成完成後可下載 MP4 影片

請幫我：
- 建立完整的專案結構
- 實作所有功能
- 提供安裝和啟動說明
```

---

## 🚀 進階版提示詞（加入 AI 整合）

```
我要創作一個 AI 驅動的音樂視覺化自動生成系統，需求如下：

【核心功能】
1. 使用 Python + Flask 建立後端（Port 5000）

2. 提供 Web 界面讓使用者上傳音樂檔案

3. 可以在瀏覽器中設定視覺化參數（色彩方案、解析度、幀率等）

4. 支援三種視覺化效果：
   - 頻譜能量條（Spectrum Bars）
   - 圓形頻譜（Circular Spectrum）
   - 鋼琴瀑布流（Piano Roll）

5. 使用 librosa 分析音頻、moviepy 生成影片

6. 加入 WebSocket 即時顯示生成進度

7. 生成完成後可下載 MP4 影片

【AI 整合功能】⭐ 新增
8. 整合 Google Gemini 3.5 API（Flash/Pro）：
   - 快速分析音樂風格
   - 自動推薦最適合的視覺化參數
   - 生成影片描述文字

9. 整合 OpenAI GPT API（4.1/5）（選用）：
   - 生成專業影片描述
   - 自動產生社群媒體文案（YouTube、Instagram、Facebook、TikTok）

【Google Sheets 任務管理】⭐ 新增
10. 建立 Google Sheets 任務管理系統：
    - Task_List（任務清單）
    - API_Config（API 設定）
    - Dashboard（統計儀表板）
    - AI_Prompts（AI 提示詞模板）
    - Execution_Log（執行日誌）

11. 實作 Google Apps Script (GAS) 自動化：
    - 自訂選單功能
    - AI 分析自動化
    - 批次處理功能
    - 呼叫 Flask API 生成影片
    - 結果自動回寫 Google Sheets

【API 擴充】⭐ 新增
12. 擴充 Flask API 端點：
    - /api/health（健康檢查）
    - /api/gas/generate（GAS 專用生成端點）
    - /api/gas/status/<job_id>（任務狀態查詢）
    - /api/gas/batch/status（批次狀態查詢）
    - /api/gas/tasks（任務列表）

【AI 服務模組】⭐ 新增
13. 建立統一的 AI 服務模組（src/services/ai_service.py）：
    - 支援 Gemini 3.5 Flash/Pro
    - 支援 GPT-5.6 Terra/GPT-5.6 Terra
    - 智能模型路由
    - 自動備援機制
    - 成本優化策略

【技術要求】
- Python 3.12+
- Flask + Flask-SocketIO
- Librosa（音頻分析）
- MoviePy（影片生成）
- FFmpeg（影片處理）
- Google Generative AI SDK
- OpenAI Python SDK
- 環境變數管理（.env）

【完整工作流程】
使用者在 Google Sheets 輸入歌名
    ↓
GAS 呼叫 Gemini API 分析音樂風格
    ↓
自動填入推薦的視覺化參數
    ↓
GAS 呼叫 Flask API 生成影片
    ↓
GPT API 生成影片描述與社群文案
    ↓
所有結果自動回寫 Google Sheets

【請提供】
1. 完整的專案結構（包含 src、gas、docs 目錄）
2. 所有功能的實作程式碼
3. GAS 完整程式碼（gas/Code.gs）
4. AI 服務整合模組（src/services/ai_service.py）
5. Flask API 擴充（src/api_extensions.py）
6. Google Sheets 模板設計文件
7. 環境變數設定範例（.env.example）
8. requirements.txt（包含所有依賴）
9. 安裝和啟動說明（README.md）
10. 完整教學文件（15-20 小時課程內容）
11. 快速啟動指南（QUICKSTART.md）

【特別要求】
- 支援擇一使用 AI API（Gemini 或 OpenAI，不強制兩個都要）
- 內建智能備援機制（一個 API 失敗自動切換）
- 成本優化設計（優先使用免費的 Gemini Flash）
- 完整的錯誤處理與日誌記錄
- 模組化設計，易於擴充
- 詳細的中文註解
- 包含測試函數

【文件要求】
- README.md（專案概述）
- QUICKSTART.md（5分鐘快速上手）
- INTEGRATION_TUTORIAL.md（完整教學，包含5個模組）
- README_AI_OPTIONS.md（AI 服務選擇指南）
- google-sheets-template.md（Sheets 模板說明）
- CHANGELOG.md（更新日誌）

【教學課程結構】
Module 1: Google Sheets 基礎（2-3小時）
Module 2: Google Apps Script 自動化（3-4小時）
Module 3: AI API 整合（3-4小時）
Module 4: Flask 後端擴充（2-3小時）
Module 5: 完整整合實作（4-5小時）

請幫我建立一個完整的、可用於教學的專案。
```

---

## 🎓 教學專案版提示詞（最完整）

```
我要創作一個「AI 音樂視覺化自動生成系統」的完整教學專案，目標是讓學生能夠學習以下技術：

【教學目標】
1. Python Flask Web 開發
2. 音視訊處理（Librosa + MoviePy）
3. Google Sheets 資料管理
4. Google Apps Script 自動化
5. AI API 整合（Gemini + GPT）
6. 完整的前後端整合
7. RESTful API 設計

【專案架構】
```
Eye_Music/
├── src/
│   ├── app.py                  # Flask 主應用
│   ├── api_extensions.py       # GAS 整合 API
│   ├── services/
│   │   ├── __init__.py
│   │   └── ai_service.py       # AI 服務整合
│   ├── core/
│   │   └── visualizer.py       # 視覺化引擎
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       ├── js/
│       ├── uploads/
│       └── outputs/
├── gas/
│   └── Code.gs                 # Google Apps Script
├── docs/
│   ├── google-sheets-template.md
│   ├── INTEGRATION_TUTORIAL.md
│   └── CHANGELOG.md
├── requirements.txt
├── .env.example
├── README.md
├── QUICKSTART.md
├── README_AI_OPTIONS.md
└── INTEGRATION_README.md
```

【功能需求清單】

## 1. Web 界面（Flask + HTML/CSS/JS）
- [ ] 拖放上傳音樂檔案
- [ ] 視覺化參數設定表單
  - [ ] 視覺化類型選擇（bars/circular/piano）
  - [ ] 色彩方案選擇（rainbow/fire/ocean/purple）
  - [ ] 解析度選擇（720p/1080p/2K/4K）
  - [ ] FPS 選擇（24/30/60）
  - [ ] 頻譜高度倍率調整
  - [ ] 透明度控制
  - [ ] 背景顏色選擇
- [ ] 即時預覽功能
- [ ] 進度條顯示
- [ ] 影片下載功能
- [ ] 響應式設計（支援手機）

## 2. Flask 後端功能
- [ ] 檔案上傳端點（/api/upload）
- [ ] 音頻分析端點（/api/analyze）
- [ ] 影片生成端點（/api/generate）
- [ ] 任務狀態查詢（/api/task/<task_id>）
- [ ] 影片下載端點（/api/download/<filename>）
- [ ] 預設模板端點（/api/presets）
- [ ] WebSocket 即時通知
- [ ] 背景任務處理

## 3. GAS 整合 API（新增）
- [ ] 健康檢查（/api/health）
- [ ] GAS 專用生成端點（/api/gas/generate）
  - [ ] 支援 Google Drive URL
  - [ ] 自動下載音檔
  - [ ] 解析 Sheets 參數格式
- [ ] 任務狀態查詢（/api/gas/status/<job_id>）
- [ ] 批次狀態查詢（/api/gas/batch/status）
- [ ] 任務列表（/api/gas/tasks）
- [ ] 任務刪除（/api/gas/task/<job_id>）

## 4. 視覺化引擎（core/visualizer.py）
- [ ] 頻譜能量條（Spectrum Bars）
  - [ ] FFT 頻譜分析
  - [ ] 動態能量條繪製
  - [ ] 顏色映射
- [ ] 圓形頻譜（Circular Spectrum）
  - [ ] 極座標轉換
  - [ ] 放射狀繪製
  - [ ] 旋轉效果
- [ ] 鋼琴瀑布流（Piano Roll）
  - [ ] MIDI 音符檢測
  - [ ] 瀑布流動畫
  - [ ] 音高可視化
- [ ] 色彩方案系統
  - [ ] 彩虹色漸變
  - [ ] 火焰色效果
  - [ ] 海洋色調
  - [ ] 紫色系
- [ ] 影片合成功能
  - [ ] 音視訊同步
  - [ ] FFmpeg 編碼
  - [ ] 進度回調

## 5. AI 服務模組（services/ai_service.py）
- [ ] Gemini API 整合
  - [ ] Gemini 3.5 Flash（快速分析）
  - [ ] Gemini 3.1 Pro（深度分析）
  - [ ] JSON 結構化輸出
  - [ ] 錯誤處理與重試
- [ ] OpenAI API 整合
  - [ ] GPT-5.6 Terra（描述生成）
  - [ ] GPT-5.6 Terra（社群文案）
  - [ ] 多輪對話支援
- [ ] 智能路由功能
  - [ ] 自動選擇最佳模型
  - [ ] 成本優化
  - [ ] 備援切換
- [ ] AI 功能實作
  - [ ] 音樂風格分析
  - [ ] 參數推薦
  - [ ] 影片描述生成
  - [ ] 社群媒體文案生成
  - [ ] 創意建議

## 6. Google Apps Script（gas/Code.gs）
- [ ] 初始化與設定
  - [ ] onOpen() 建立自訂選單
  - [ ] 腳本屬性管理
  - [ ] API Key 安全儲存
- [ ] AI API 呼叫函數
  - [ ] callGeminiAPI()
  - [ ] callGPTAPI()
  - [ ] analyzeMusicStyle()
  - [ ] getCreativeSuggestion()
  - [ ] generateVideoDescription()
  - [ ] generateSocialMediaContent()
- [ ] Flask API 呼叫函數
  - [ ] callFlaskGenerate()
  - [ ] checkTaskStatus()
- [ ] Sheets 操作函數
  - [ ] getSelectedTasks()
  - [ ] updateTaskStatus()
  - [ ] logExecution()
- [ ] 主要功能函數
  - [ ] analyzeSelectedTasks()
  - [ ] generateSelectedTasks()
  - [ ] batchProcessAllTasks()
  - [ ] updateAllTaskStatus()
  - [ ] cleanFailedTasks()
  - [ ] showUsageStats()
- [ ] 測試函數
  - [ ] testGeminiConnection()
  - [ ] testOpenAIConnection()
  - [ ] testFlaskConnection()

## 7. Google Sheets 模板設計
- [ ] Task_List 工作表
  - [ ] 15 個欄位定義
  - [ ] 資料驗證規則
  - [ ] 條件格式設定
  - [ ] 範例資料
- [ ] API_Config 工作表
  - [ ] API 服務設定
  - [ ] 用量追蹤
  - [ ] 成本計算
- [ ] Dashboard 工作表
  - [ ] 即時統計圖表
  - [ ] AI 使用分析
  - [ ] 效能分析
- [ ] AI_Prompts 工作表
  - [ ] Prompt 模板管理
  - [ ] 版本控制
- [ ] Execution_Log 工作表
  - [ ] 詳細執行日誌
  - [ ] 錯誤追蹤

## 8. 文件系統
- [ ] README.md
  - [ ] 專案簡介
  - [ ] 功能特色
  - [ ] 安裝步驟
  - [ ] 使用說明
  - [ ] 專案結構
  - [ ] 故障排除
- [ ] QUICKSTART.md
  - [ ] 5 分鐘快速上手
  - [ ] 步驟 1-7 清單
  - [ ] 常見問題排查
- [ ] INTEGRATION_TUTORIAL.md
  - [ ] 完整 15-20 小時教學
  - [ ] 5 個教學模組
  - [ ] 實戰專案
  - [ ] 延伸學習
- [ ] README_AI_OPTIONS.md
  - [ ] AI 服務比較
  - [ ] 選擇建議
  - [ ] 成本計算
  - [ ] 設定方式
- [ ] google-sheets-template.md
  - [ ] 詳細欄位說明
  - [ ] 設定步驟
  - [ ] 公式範例
- [ ] CHANGELOG.md
  - [ ] 版本歷史
  - [ ] 功能更新
  - [ ] 未來計劃

## 9. 環境設定
- [ ] requirements.txt
  - [ ] Flask + SocketIO
  - [ ] Librosa + MoviePy
  - [ ] Google AI SDK
  - [ ] OpenAI SDK
  - [ ] 其他依賴
- [ ] .env.example
  - [ ] AI API Keys
  - [ ] Flask 設定
  - [ ] FFmpeg 路徑
  - [ ] 預設參數
  - [ ] 進階選項
- [ ] start.sh（macOS/Linux）
- [ ] start_windows.bat（Windows）

## 10. 測試與範例
- [ ] 測試音檔（< 1 分鐘）
- [ ] 測試資料（Google Sheets）
- [ ] API 測試腳本
- [ ] 單元測試（選用）

【教學內容要求】

## Module 1: Google Sheets 基礎（2-3 小時）
- 建立試算表
- 設定工作表結構
- 資料驗證
- 條件格式
- 基礎公式
- 統計圖表

## Module 2: Google Apps Script（3-4 小時）
- GAS 基礎語法
- 讀寫 Sheets 資料
- UrlFetchApp API 呼叫
- 自訂選單與對話框
- 觸發器設定
- 錯誤處理

## Module 3: AI API 整合（3-4 小時）
- Gemini API 申請與使用
- OpenAI API 申請與使用
- Prompt Engineering 技巧
- JSON 結構化輸出
- 成本優化策略
- 錯誤處理與重試

## Module 4: Flask 後端擴充（2-3 小時）
- Flask Blueprint 架構
- RESTful API 設計
- 非同步任務處理
- WebSocket 整合
- 檔案上傳處理
- 錯誤處理與日誌

## Module 5: 完整整合實作（4-5 小時）
- 端到端流程測試
- 批次處理實作
- 錯誤處理與重試
- 成本追蹤
- 效能優化
- 部署準備

【實戰專案】
1. 自動化社群媒體發布流程
2. 智能參數優化系統
3. 成本追蹤儀表板
4. YouTube API 自動上傳

【技術細節要求】
- 所有程式碼需要詳細中文註解
- 變數名稱使用有意義的英文
- 函數需要文件字串（docstring）
- 錯誤訊息需要清楚易懂
- 日誌輸出需要適當分級
- 支援 Windows/macOS/Linux
- 相容 Python 3.12+

【AI API 使用策略】
- 優先使用 Gemini Flash（免費、快速）
- 重要任務使用 Gemini Pro 或 GPT
- 支援單一 API 運作（不強制兩個都要）
- 自動備援機制
- 成本追蹤與限制

【成本優化】
- Gemini 用於批次處理（免費額度高）
- GPT 用於關鍵任務（品質優先）
- 快取常見結果
- 批次查詢減少 API 呼叫
- 錯誤重試機制（避免浪費）

【安全性】
- API Keys 環境變數儲存
- GAS 腳本屬性保護
- 敏感資訊不上傳 Git
- CORS 設定
- 檔案類型驗證
- 檔案大小限制

【使用者體驗】
- 清楚的進度顯示
- 友善的錯誤訊息
- 即時狀態更新
- 快速回應
- 行動裝置支援

【教學方法】
- 循序漸進的難度設計
- 豐富的範例程式碼
- 詳細的步驟說明
- 常見問題與解答
- 實戰專題練習
- 延伸學習資源

請幫我建立這個完整的教學專案，包含：
1. 所有程式碼檔案
2. 完整的文件系統
3. 教學課程內容
4. 實戰專案範例
5. 測試與驗證步驟

目標是讓學生能夠透過這個專案，學會：
- Python Web 開發
- 音視訊處理技術
- Google Workspace 自動化
- AI API 整合應用
- 完整的專案開發流程
```

---

## 📊 提示詞版本比較

| 特性 | 基礎版 | 進階版 | 教學版 |
|------|-------|-------|-------|
| **行數** | ~20 行 | ~100 行 | ~300 行 |
| **功能數量** | 7 個 | 13 個 | 60+ 個 |
| **AI 整合** | ❌ | ✅ | ✅ |
| **Google Sheets** | ❌ | ✅ | ✅ |
| **教學內容** | ❌ | ❌ | ✅ |
| **文件要求** | 簡單 | 詳細 | 完整 |
| **適用對象** | 快速原型 | 完整專案 | 教學課程 |

---

## 💡 使用建議

### 情境 1：快速開發原型
使用 **基礎版提示詞**
- ✅ 快速取得可運作的原型
- ✅ 適合驗證想法
- ⚠️ 功能較陽春

### 情境 2：正式專案開發
使用 **進階版提示詞**
- ✅ 功能完整
- ✅ AI 整合
- ✅ 自動化管理
- ✅ 可擴充性高

### 情境 3：教學課程設計
使用 **教學版提示詞**
- ✅ 完整的教學內容
- ✅ 分模組設計
- ✅ 實戰專案
- ✅ 詳細文件

---

## 🎯 提示詞優化技巧

### 1. 明確性
❌ **不好**：「我要一個音樂視覺化專案」
✅ **好**：「使用 Python Flask + Librosa + MoviePy 建立音樂視覺化系統，支援三種視覺化類型...」

### 2. 結構化
```
【功能需求】
【技術要求】
【文件要求】
【請提供】
```

### 3. 檢查清單
- [ ] 使用 checklist 讓 AI 不遺漏功能

### 4. 範例提供
```
【完整工作流程】
步驟 1 → 步驟 2 → 步驟 3
```

### 5. 限制條件
```
【特別要求】
- 支援擇一使用 AI API
- Python 3.8+
- 詳細中文註解
```

---

## 🔄 迭代改進流程

### 第一輪：基礎功能
```
使用基礎版提示詞 → 取得原型 → 測試功能
```

### 第二輪：功能擴充
```
使用進階版提示詞 → 加入 AI 整合 → 測試完整流程
```

### 第三輪：教學包裝
```
使用教學版提示詞 → 完整文件 → 課程設計
```

---

## 📚 實際使用範例

### 與 Claude Code 對話

**使用者**：
```
（貼上「進階版提示詞」）
```

**Claude**：
```
我會幫你建立這個專案。讓我先建立專案結構...

（開始建立檔案）
- src/app.py
- src/api_extensions.py
- src/services/ai_service.py
- gas/Code.gs
- docs/...
...
```

### 與 ChatGPT 對話

**使用者**：
```
（貼上「教學版提示詞」）

另外請特別注意：
1. 我的作業系統是 Windows
2. 我想重點學習 AI API 整合
3. 預算有限，優先使用 Gemini
```

**ChatGPT**：
```
我會為你建立這個完整的教學專案...

（提供詳細的實作）
```

---

## 🎓 教師使用指南

### 如何將此專案用於教學

#### 1. 課前準備（1 週前）
- [ ] 確認所有學生都有 Google 帳號
- [ ] 準備測試音檔
- [ ] 建立示範 Google Sheets
- [ ] 申請教學用 API Keys

#### 2. 第一堂課（3 小時）
- [ ] 專案介紹與演示
- [ ] 環境設定（Python、FFmpeg）
- [ ] 基礎功能測試
- [ ] Google Sheets 模板建立

#### 3. 第二堂課（3 小時）
- [ ] GAS 基礎教學
- [ ] API 呼叫實作
- [ ] 自訂選單建立

#### 4. 第三堂課（3 小時）
- [ ] AI API 申請
- [ ] Gemini/GPT 整合
- [ ] Prompt Engineering

#### 5. 第四堂課（3 小時）
- [ ] Flask 後端擴充
- [ ] API 端點設計
- [ ] 錯誤處理

#### 6. 第五堂課（3 小時）
- [ ] 完整整合測試
- [ ] 批次處理實作
- [ ] 成本優化

#### 7. 期末專題（課外）
- [ ] 學生選擇實戰專案
- [ ] 獨立開發
- [ ] 成果展示

---

## 💼 企業內訓使用

### 適合的訓練課程

1. **Python Web 開發實戰**（2 天）
   - Flask 框架
   - RESTful API
   - WebSocket 應用

2. **AI API 整合應用**（2 天）
   - Gemini API 實戰
   - OpenAI API 應用
   - Prompt Engineering
   - 成本優化

3. **Google Workspace 自動化**（1 天）
   - Google Sheets 進階
   - Apps Script 開發
   - 工作流程自動化

4. **完整專案開發**（5 天）
   - 需求分析
   - 架構設計
   - 開發實作
   - 測試部署
   - 維護優化

---

## 📞 需要協助？

如果你在使用這些提示詞時遇到問題：

1. **AI 回應不符合預期**
   - 提供更具體的範例
   - 增加限制條件
   - 分階段提問

2. **功能不完整**
   - 使用 checklist 逐項確認
   - 要求 AI 補充缺失的部分

3. **文件不夠詳細**
   - 明確要求「詳細中文註解」
   - 要求「步驟說明」
   - 要求「範例程式碼」

---

## 🎉 總結

這個專案提供了三個層次的提示詞範例：

1. **基礎版**：適合快速原型開發
2. **進階版**：適合完整專案實作
3. **教學版**：適合課程教學設計

選擇適合你需求的版本，開始你的 AI 音樂視覺化專案吧！

---

**© 2025 Eye Music | Made with ❤️ by 阿亮老師**

🎵 用 AI 讓提示詞更強大 ✨
