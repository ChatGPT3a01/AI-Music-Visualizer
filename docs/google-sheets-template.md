# 📊 Google Sheets 模板結構設計

## 🎯 整體架構

本專案使用 Google Sheets 作為任務管理與數據中心，整合 AI 模型進行智能化音樂視覺化生成。

---

## 📋 工作表結構

### 1️⃣ 工作表：**任務清單** (Task_List)

| 欄位 | 說明 | 資料類型 | 範例 |
|------|------|----------|------|
| A: 序號 | 自動編號 | 數字 | 1 |
| B: 歌曲名稱 | 音樂名稱 | 文字 | 夜曲 - 周杰倫 |
| C: 音樂檔案連結 | Google Drive 或本地路徑 | URL/路徑 | https://drive.google.com/... |
| D: 視覺化類型 | bars/circular/piano | 下拉選單 | circular |
| E: 色彩方案 | rainbow/fire/ocean/purple | 下拉選單 | rainbow |
| F: 解析度 | 720p/1080p/2K/4K | 下拉選單 | 1080p |
| G: FPS | 24/30/60 | 下拉選單 | 30 |
| H: AI 模型選擇 | Gemini 3.5 Flash/Pro, GPT-5.6 Terra/5 | 下拉選單 | Gemini 3.5 Flash |
| I: 狀態 | 待處理/AI分析中/生成中/已完成/失敗 | 狀態 | 已完成 |
| J: AI 參數建議 | AI 分析後的建議參數 | 文字 | 建議使用火焰色系... |
| K: 生成時間 | 任務完成時間 | 時間戳記 | 2025-01-07 14:30 |
| L: 耗時(秒) | 生成所需時間 | 數字 | 45.2 |
| M: 影片連結 | 生成影片的下載連結 | URL | https://... |
| N: AI 描述文字 | AI 生成的影片描述 | 文字 | 這是一段充滿活力的... |
| O: 錯誤訊息 | 失敗時的錯誤資訊 | 文字 | FFmpeg error... |

**資料驗證規則：**
- D欄：={"bars", "circular", "piano"}
- E欄：={"rainbow", "fire", "ocean", "purple"}
- F欄：={"720p", "1080p", "2K", "4K"}
- G欄：={"24", "30", "60"}
- H欄：={"Gemini 3.5 Flash", "Gemini 3.1 Pro", "GPT-5.6 Terra", "GPT-5.6 Terra"}

---

### 2️⃣ 工作表：**API 設定** (API_Config)

| 欄位 | 說明 | 範例 |
|------|------|------|
| A: API 名稱 | API 服務名稱 | Gemini API |
| B: API Key | API 金鑰（建議加密） | AIzaSy... |
| C: 模型名稱 | 使用的模型 | gemini-3.5-flash |
| D: 每日限額 | API 每日呼叫上限 | 1000 |
| E: 當前用量 | 今日已使用次數 | 45 |
| F: 每次費用(USD) | 單次呼叫成本 | 0.002 |
| G: 狀態 | 啟用/停用 | 啟用 |
| H: 備註 | 其他說明 | 用於快速分析 |

**預設 API 設定行：**
1. Gemini 3.5 Flash (快速分析用)
2. Gemini 3.1 Pro (深度分析用)
3. GPT-5.6 Terra (創意描述生成)
4. GPT-5.6 Terra (複雜任務處理)

---

### 3️⃣ 工作表：**統計儀表板** (Dashboard)

#### 📊 區塊 A: 即時統計

| 指標 | 公式/說明 |
|------|----------|
| 總任務數 | =COUNTA(Task_List!A:A)-1 |
| 已完成 | =COUNTIF(Task_List!I:I,"已完成") |
| 進行中 | =COUNTIF(Task_List!I:I,"生成中")+COUNTIF(Task_List!I:I,"AI分析中") |
| 失敗數 | =COUNTIF(Task_List!I:I,"失敗") |
| 成功率(%) | =已完成/(總任務數-待處理)*100 |

#### 📊 區塊 B: AI 使用統計

| AI 模型 | 呼叫次數 | 總費用 |
|---------|----------|--------|
| Gemini 3.5 Flash | =COUNTIF(Task_List!H:H,"Gemini 3.5 Flash") | 自動計算 |
| Gemini 3.1 Pro | =COUNTIF(Task_List!H:H,"Gemini 3.1 Pro") | 自動計算 |
| GPT-5.6 Terra | =COUNTIF(Task_List!H:H,"GPT-5.6 Terra") | 自動計算 |
| GPT-5.6 Terra | =COUNTIF(Task_List!H:H,"GPT-5.6 Terra") | 自動計算 |

#### 📊 區塊 C: 效能分析

| 視覺化類型 | 平均耗時(秒) | 使用次數 |
|------------|--------------|----------|
| bars | =AVERAGEIF(Task_List!D:D,"bars",Task_List!L:L) | =COUNTIF(Task_List!D:D,"bars") |
| circular | =AVERAGEIF(Task_List!D:D,"circular",Task_List!L:L) | =COUNTIF(Task_List!D:D,"circular") |
| piano | =AVERAGEIF(Task_List!D:D,"piano",Task_List!L:L) | =COUNTIF(Task_List!D:D,"piano") |

---

### 4️⃣ 工作表：**AI Prompt 模板** (AI_Prompts)

儲存不同場景的 AI Prompt 範本，方便管理與優化。

| 欄位 | 說明 | 範例 |
|------|------|------|
| A: Prompt 名稱 | 用途描述 | 音樂風格分析 |
| B: AI 模型 | 建議使用的模型 | Gemini 3.5 Flash |
| C: Prompt 內容 | 完整提示詞 | 請分析以下歌曲... |
| D: 輸出格式 | JSON/純文字 | JSON |
| E: 最後更新時間 | 更新記錄 | 2025-01-07 |

**預設 Prompt 範本：**

1. **音樂風格分析** (Gemini 3.5 Flash)
```
分析歌曲「{歌名}」的音樂風格，並以 JSON 格式回傳最適合的視覺化參數：
{
  "visualization_type": "bars/circular/piano",
  "color_scheme": "rainbow/fire/ocean/purple",
  "reason": "選擇理由",
  "recommended_fps": 24/30/60
}
```

2. **深度創意建議** (Gemini 3.1 Pro)
```
針對歌曲「{歌名}」生成創意視覺化方案，包含：
1. 視覺化類型與理由
2. 色彩心理學分析
3. 特殊效果建議
4. 目標觀眾群
```

3. **影片描述生成** (GPT-5.6 Terra)
```
為以下音樂視覺化影片生成吸引人的描述文字（100-150字）：
- 歌曲：{歌名}
- 視覺化類型：{類型}
- 色彩方案：{色彩}
請使用生動、有感染力的語言。
```

4. **社群媒體文案** (GPT-5.6 Terra)
```
生成適合 YouTube/Instagram 的影片發布文案：
- 標題（吸睛、SEO 友善）
- 描述（包含 hashtag）
- 標籤建議（10個）
```

---

### 5️⃣ 工作表：**執行日誌** (Execution_Log)

記錄每次 GAS 執行的詳細日誌。

| 欄位 | 說明 |
|------|------|
| A: 時間戳記 | 執行時間 |
| B: 任務序號 | 對應任務清單 |
| C: 動作類型 | AI分析/生成請求/狀態更新 |
| D: AI 模型 | 使用的模型 |
| E: 執行狀態 | 成功/失敗 |
| F: 回應時間(ms) | API 響應時間 |
| G: Token 用量 | AI API Token 消耗 |
| H: 詳細訊息 | 完整日誌 |

---

## 🎨 條件格式設定

### 任務清單狀態顏色

- **待處理**: 灰色背景 (#E8E8E8)
- **AI分析中**: 淺藍色背景 (#CCE5FF)
- **生成中**: 黃色背景 (#FFF4CC)
- **已完成**: 綠色背景 (#D9EAD3)
- **失敗**: 紅色背景 (#F4CCCC)

### API 用量警示

- 用量 > 80%：橙色背景
- 用量 > 95%：紅色背景

---

## 🔐 安全性建議

1. **API Key 保護**
   - 使用 PropertiesService 儲存在 GAS 腳本屬性
   - 不直接顯示在 Sheet 中（顯示為 ****）

2. **存取權限**
   - 工作表設為「僅限特定人員編輯」
   - API_Config 工作表設為「隱藏」

3. **資料備份**
   - 每日自動備份到另一個 Sheet
   - 保留最近 30 天的歷史記錄

---

## 📥 建立步驟

1. 複製此模板到你的 Google Drive
2. 設定資料驗證規則
3. 套用條件格式
4. 安裝 GAS 程式碼（見 gas-integration.gs）
5. 設定 API Key（工具 > 腳本編輯器 > 專案設定 > 腳本屬性）

---

## 🔗 相關文件

- [GAS 程式碼教學](./gas-integration-guide.md)
- [AI API 整合說明](./ai-api-integration.md)
- [Flask 後端擴充](./flask-api-extension.md)
