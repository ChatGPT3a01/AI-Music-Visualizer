/**
 * ========================================
 * Eye Music - Google Apps Script 整合程式
 * ========================================
 *
 * 功能：
 * 1. 整合 Gemini 3.5 Flash/Pro API
 * 2. 整合 GPT-5.6 Terra/GPT-5.6 Terra API
 * 3. 與 Flask 後端通訊
 * 4. 自動化任務管理
 *
 * 作者：阿亮老師（曾慶良）
 * 版本：1.0.0
 * 日期：2025-01-07
 */

// ====================================
// 全域變數與設定
// ====================================

const CONFIG = {
  // 工作表名稱
  SHEETS: {
    TASK_LIST: 'Task_List',
    API_CONFIG: 'API_Config',
    DASHBOARD: 'Dashboard',
    AI_PROMPTS: 'AI_Prompts',
    EXECUTION_LOG: 'Execution_Log'
  },

  // Flask 後端 API 端點
  FLASK_API: {
    BASE_URL: 'http://localhost:5000',
    ENDPOINTS: {
      GENERATE: '/api/generate',
      STATUS: '/api/status',
      DOWNLOAD: '/api/download'
    }
  },

  // AI 模型設定
  AI_MODELS: {
    GEMINI_FLASH: 'gemini-3.5-flash',
    GEMINI_PRO: 'gemini-3.1-pro-preview',
    GPT_41: 'gpt-5.6-terra',
    GPT_5: 'gpt-5.6-terra'
  }
};

// ====================================
// 初始化與設定
// ====================================

/**
 * 建立自訂選單
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🎵 Eye Music')
    .addItem('🤖 AI 分析選中任務', 'analyzeSelectedTasks')
    .addItem('▶️ 生成選中任務', 'generateSelectedTasks')
    .addSeparator()
    .addItem('📊 批次處理所有待處理任務', 'batchProcessAllTasks')
    .addSeparator()
    .addItem('🔄 更新任務狀態', 'updateAllTaskStatus')
    .addItem('🧹 清理失敗任務', 'cleanFailedTasks')
    .addSeparator()
    .addItem('⚙️ 設定 API Keys', 'showApiKeyDialog')
    .addItem('📋 查看使用統計', 'showUsageStats')
    .addToUi();
}

/**
 * 顯示 API Key 設定對話框
 */
function showApiKeyDialog() {
  const html = HtmlService.createHtmlOutput(`
    <style>
      body { font-family: Arial, sans-serif; padding: 20px; }
      input { width: 100%; padding: 8px; margin: 5px 0 15px 0; }
      button { padding: 10px 20px; background: #4285f4; color: white; border: none; cursor: pointer; }
      button:hover { background: #357ae8; }
      label { font-weight: bold; }
    </style>
    <h3>🔐 API Key 設定</h3>
    <form>
      <label>Google AI Studio API Key (Gemini):</label>
      <input type="password" id="geminiKey" placeholder="AIzaSy...">

      <label>OpenAI API Key (GPT):</label>
      <input type="password" id="openaiKey" placeholder="sk-...">

      <label>Flask 後端 URL:</label>
      <input type="text" id="flaskUrl" placeholder="http://localhost:5000" value="http://localhost:5000">

      <br><br>
      <button type="button" onclick="saveKeys()">💾 儲存設定</button>
    </form>

    <script>
      function saveKeys() {
        const geminiKey = document.getElementById('geminiKey').value;
        const openaiKey = document.getElementById('openaiKey').value;
        const flaskUrl = document.getElementById('flaskUrl').value;

        google.script.run
          .withSuccessHandler(() => {
            alert('✅ API Keys 已儲存！');
            google.script.host.close();
          })
          .withFailureHandler((error) => {
            alert('❌ 儲存失敗：' + error);
          })
          .saveApiKeys(geminiKey, openaiKey, flaskUrl);
      }
    </script>
  `).setWidth(500).setHeight(400);

  SpreadsheetApp.getUi().showModalDialog(html, '⚙️ API 設定');
}

/**
 * 儲存 API Keys 到腳本屬性（安全存儲）
 */
function saveApiKeys(geminiKey, openaiKey, flaskUrl) {
  const props = PropertiesService.getScriptProperties();

  if (geminiKey) props.setProperty('GEMINI_API_KEY', geminiKey);
  if (openaiKey) props.setProperty('OPENAI_API_KEY', openaiKey);
  if (flaskUrl) props.setProperty('FLASK_URL', flaskUrl);

  Logger.log('API Keys 已安全儲存');
}

/**
 * 取得 API Keys
 */
function getApiKeys() {
  const props = PropertiesService.getScriptProperties();
  return {
    gemini: props.getProperty('GEMINI_API_KEY'),
    openai: props.getProperty('OPENAI_API_KEY'),
    flaskUrl: props.getProperty('FLASK_URL') || CONFIG.FLASK_API.BASE_URL
  };
}

// ====================================
// AI 整合功能
// ====================================

/**
 * 呼叫 Gemini API (2.5 Flash/Pro)
 */
function callGeminiAPI(prompt, modelType = 'flash') {
  const apiKey = getApiKeys().gemini;
  if (!apiKey) {
    throw new Error('請先設定 Gemini API Key');
  }

  const model = modelType === 'pro' ? CONFIG.AI_MODELS.GEMINI_PRO : CONFIG.AI_MODELS.GEMINI_FLASH;
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

  const payload = {
    contents: [{
      parts: [{
        text: prompt
      }]
    }],
    generationConfig: {
      temperature: 0.7,
      topK: 40,
      topP: 0.95,
      maxOutputTokens: 2048,
    }
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  try {
    const startTime = new Date().getTime();
    const response = UrlFetchApp.fetch(url, options);
    const responseTime = new Date().getTime() - startTime;

    const result = JSON.parse(response.getContentText());

    // 記錄日誌
    logExecution('AI分析', model, '成功', responseTime, result);

    if (result.candidates && result.candidates[0].content) {
      return result.candidates[0].content.parts[0].text;
    } else {
      throw new Error('Gemini API 回應格式錯誤');
    }
  } catch (error) {
    logExecution('AI分析', model, '失敗', 0, error.toString());
    throw error;
  }
}

/**
 * 呼叫 OpenAI GPT API (GPT-5.6 Terra/GPT-5.6 Terra)
 */
function callGPTAPI(prompt, modelType = 'gpt-5.6-terra') {
  const apiKey = getApiKeys().openai;
  if (!apiKey) {
    throw new Error('請先設定 OpenAI API Key');
  }

  const model = modelType === 'gpt-5.6-terra' ? CONFIG.AI_MODELS.GPT_5 : CONFIG.AI_MODELS.GPT_41;
  const url = 'https://api.openai.com/v1/chat/completions';

  const payload = {
    model: model,
    messages: [
      {
        role: 'system',
        content: '你是一位音樂視覺化專家，精通音樂分析與視覺設計。'
      },
      {
        role: 'user',
        content: prompt
      }
    ],
    temperature: 0.8,
    max_tokens: 2000
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'Authorization': `Bearer ${apiKey}`
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  try {
    const startTime = new Date().getTime();
    const response = UrlFetchApp.fetch(url, options);
    const responseTime = new Date().getTime() - startTime;

    const result = JSON.parse(response.getContentText());

    // 記錄日誌
    logExecution('AI分析', model, '成功', responseTime, result);

    if (result.choices && result.choices[0].message) {
      return result.choices[0].message.content;
    } else {
      throw new Error('OpenAI API 回應格式錯誤: ' + response.getContentText());
    }
  } catch (error) {
    logExecution('AI分析', model, '失敗', 0, error.toString());
    throw error;
  }
}

/**
 * AI 音樂風格分析（快速分析用 Gemini 3.5 Flash）
 */
function analyzeMusicStyle(songName) {
  const prompt = `分析歌曲「${songName}」的音樂風格，並以 JSON 格式回傳最適合的視覺化參數。

回傳格式：
{
  "visualization_type": "bars/circular/piano 三選一",
  "color_scheme": "rainbow/fire/ocean/purple 四選一",
  "fps": 24/30/60 三選一（數字）,
  "reason": "選擇理由（繁體中文，50字內）",
  "style_tags": ["標籤1", "標籤2", "標籤3"]
}

請直接回傳 JSON，不要有其他文字。`;

  try {
    const response = callGeminiAPI(prompt, 'flash');

    // 清理回應文字（移除可能的 markdown 標記）
    let cleanResponse = response.trim();
    cleanResponse = cleanResponse.replace(/```json\n?/g, '').replace(/```\n?/g, '');

    const result = JSON.parse(cleanResponse);
    return result;
  } catch (error) {
    Logger.log('AI 分析失敗：' + error);
    // 回傳預設值
    return {
      visualization_type: 'circular',
      color_scheme: 'rainbow',
      fps: 30,
      reason: 'AI 分析失敗，使用預設參數',
      style_tags: ['預設']
    };
  }
}

/**
 * AI 深度創意建議（使用 Gemini 3.1 Pro）
 */
function getCreativeSuggestion(songName, currentParams) {
  const prompt = `針對歌曲「${songName}」提供深度創意視覺化建議。

目前參數：
- 視覺化類型：${currentParams.visualizationType}
- 色彩方案：${currentParams.colorScheme}

請提供：
1. 視覺化優化建議（考慮音樂心理學）
2. 色彩心理學分析
3. 目標觀眾群分析
4. 特殊效果建議

請用繁體中文回答，結構化且具體。`;

  try {
    return callGeminiAPI(prompt, 'pro');
  } catch (error) {
    return '深度分析功能暫時無法使用：' + error;
  }
}

/**
 * AI 生成影片描述（使用 GPT-5.6 Terra）
 */
function generateVideoDescription(songName, visualizationType, colorScheme) {
  const prompt = `為音樂視覺化影片生成吸引人的描述文字（100-150字，繁體中文）：

- 歌曲：${songName}
- 視覺化類型：${visualizationType}
- 色彩方案：${colorScheme}

要求：
- 使用生動、有感染力的語言
- 突出視覺效果特色
- 引發觀眾興趣
- 適合 YouTube 影片描述`;

  try {
    return callGPTAPI(prompt, 'gpt-5.6-terra');
  } catch (error) {
    return `體驗${songName}的視覺饗宴！採用${visualizationType}視覺化效果與${colorScheme}色彩方案，讓音樂與視覺完美結合。`;
  }
}

/**
 * AI 生成社群媒體文案（使用 GPT-5.6 Terra）
 */
function generateSocialMediaContent(songName, description) {
  const prompt = `為音樂視覺化影片生成社群媒體發布文案：

歌曲：${songName}
影片描述：${description}

請生成以 JSON 格式回傳：
{
  "title": "YouTube 標題（吸睛、SEO友善、50字內）",
  "description": "YouTube 描述（包含適當換行）",
  "hashtags": ["tag1", "tag2", ...（10個標籤）],
  "instagram_caption": "Instagram 文案（含 emoji）"
}

請直接回傳 JSON，不要有其他文字。`;

  try {
    const response = callGPTAPI(prompt, 'gpt-5.6-terra');
    let cleanResponse = response.trim();
    cleanResponse = cleanResponse.replace(/```json\n?/g, '').replace(/```\n?/g, '');
    return JSON.parse(cleanResponse);
  } catch (error) {
    return {
      title: `${songName} - 音樂視覺化`,
      description: description,
      hashtags: ['音樂視覺化', '視覺藝術', songName],
      instagram_caption: `🎵 ${songName} 視覺化作品 ✨`
    };
  }
}

// ====================================
// Flask 後端整合
// ====================================

/**
 * 呼叫 Flask API 生成影片
 */
function callFlaskGenerate(taskData) {
  const flaskUrl = getApiKeys().flaskUrl;
  const url = flaskUrl + CONFIG.FLASK_API.ENDPOINTS.GENERATE;

  const payload = {
    song_name: taskData.songName,
    audio_url: taskData.audioUrl,
    visualization_type: taskData.visualizationType,
    color_scheme: taskData.colorScheme,
    resolution: taskData.resolution,
    fps: taskData.fps,
    task_id: taskData.taskId
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(url, options);
    const result = JSON.parse(response.getContentText());

    logExecution('生成請求', 'Flask', '成功', 0, result);
    return result;
  } catch (error) {
    logExecution('生成請求', 'Flask', '失敗', 0, error.toString());
    throw new Error('Flask API 呼叫失敗：' + error);
  }
}

/**
 * 查詢任務狀態
 */
function checkTaskStatus(jobId) {
  const flaskUrl = getApiKeys().flaskUrl;
  const url = `${flaskUrl}${CONFIG.FLASK_API.ENDPOINTS.STATUS}/${jobId}`;

  try {
    const response = UrlFetchApp.fetch(url);
    return JSON.parse(response.getContentText());
  } catch (error) {
    Logger.log('查詢狀態失敗：' + error);
    return null;
  }
}

// ====================================
// 工作表操作
// ====================================

/**
 * 取得選中的任務行
 */
function getSelectedTasks() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEETS.TASK_LIST);
  const selection = sheet.getActiveRange();
  const startRow = selection.getRow();
  const numRows = selection.getNumRows();

  const tasks = [];
  for (let i = 0; i < numRows; i++) {
    const row = startRow + i;
    if (row === 1) continue; // 跳過標題行

    const rowData = sheet.getRange(row, 1, 1, 15).getValues()[0];
    tasks.push({
      row: row,
      taskId: rowData[0],
      songName: rowData[1],
      audioUrl: rowData[2],
      visualizationType: rowData[3],
      colorScheme: rowData[4],
      resolution: rowData[5],
      fps: rowData[6],
      aiModel: rowData[7],
      status: rowData[8]
    });
  }

  return tasks;
}

/**
 * 更新任務狀態
 */
function updateTaskStatus(row, status, aiSuggestion = '', videoUrl = '', description = '', errorMsg = '') {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEETS.TASK_LIST);

  // I欄：狀態
  sheet.getRange(row, 9).setValue(status);

  // J欄：AI 建議
  if (aiSuggestion) {
    sheet.getRange(row, 10).setValue(aiSuggestion);
  }

  // K欄：生成時間
  if (status === '已完成' || status === '失敗') {
    sheet.getRange(row, 11).setValue(new Date());
  }

  // M欄：影片連結
  if (videoUrl) {
    sheet.getRange(row, 13).setValue(videoUrl);
  }

  // N欄：AI 描述
  if (description) {
    sheet.getRange(row, 14).setValue(description);
  }

  // O欄：錯誤訊息
  if (errorMsg) {
    sheet.getRange(row, 15).setValue(errorMsg);
  }
}

// ====================================
// 主要功能函數
// ====================================

/**
 * AI 分析選中任務
 */
function analyzeSelectedTasks() {
  const tasks = getSelectedTasks();

  if (tasks.length === 0) {
    SpreadsheetApp.getUi().alert('請先選擇要分析的任務！');
    return;
  }

  tasks.forEach(task => {
    try {
      // 更新狀態
      updateTaskStatus(task.row, 'AI分析中');

      // 呼叫 AI 分析
      const analysis = analyzeMusicStyle(task.songName);

      // 更新參數建議
      const suggestion = `建議：${analysis.visualization_type} + ${analysis.color_scheme} @ ${analysis.fps}FPS\n理由：${analysis.reason}`;
      updateTaskStatus(task.row, '待處理', suggestion);

      // 自動填入建議參數（可選）
      const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEETS.TASK_LIST);
      sheet.getRange(task.row, 4).setValue(analysis.visualization_type); // D欄
      sheet.getRange(task.row, 5).setValue(analysis.color_scheme); // E欄
      sheet.getRange(task.row, 7).setValue(analysis.fps); // G欄

    } catch (error) {
      updateTaskStatus(task.row, '待處理', '', '', '', 'AI 分析失敗：' + error);
    }
  });

  SpreadsheetApp.getUi().alert(`✅ 已完成 ${tasks.length} 個任務的 AI 分析！`);
}

/**
 * 生成選中任務
 */
function generateSelectedTasks() {
  const tasks = getSelectedTasks();

  if (tasks.length === 0) {
    SpreadsheetApp.getUi().alert('請先選擇要生成的任務！');
    return;
  }

  let successCount = 0;
  let failCount = 0;

  tasks.forEach(task => {
    try {
      // 更新狀態
      updateTaskStatus(task.row, '生成中');

      // 呼叫 Flask API
      const result = callFlaskGenerate(task);

      if (result.success) {
        // 生成 AI 描述
        const description = generateVideoDescription(
          task.songName,
          task.visualizationType,
          task.colorScheme
        );

        updateTaskStatus(
          task.row,
          '已完成',
          '',
          result.video_url || result.download_url,
          description
        );
        successCount++;
      } else {
        updateTaskStatus(task.row, '失敗', '', '', '', result.error || '生成失敗');
        failCount++;
      }

    } catch (error) {
      updateTaskStatus(task.row, '失敗', '', '', '', error.toString());
      failCount++;
    }
  });

  SpreadsheetApp.getUi().alert(`生成完成！\n✅ 成功：${successCount}\n❌ 失敗：${failCount}`);
}

/**
 * 批次處理所有待處理任務
 */
function batchProcessAllTasks() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEETS.TASK_LIST);
  const data = sheet.getDataRange().getValues();

  let processCount = 0;

  for (let i = 1; i < data.length; i++) { // 從第2行開始（跳過標題）
    const status = data[i][8]; // I欄：狀態

    if (status === '待處理' || status === '') {
      const task = {
        row: i + 1,
        taskId: data[i][0],
        songName: data[i][1],
        audioUrl: data[i][2],
        visualizationType: data[i][3],
        colorScheme: data[i][4],
        resolution: data[i][5],
        fps: data[i][6],
        aiModel: data[i][7]
      };

      try {
        // 先 AI 分析
        updateTaskStatus(task.row, 'AI分析中');
        const analysis = analyzeMusicStyle(task.songName);

        // 更新參數
        sheet.getRange(task.row, 4).setValue(analysis.visualization_type);
        sheet.getRange(task.row, 5).setValue(analysis.color_scheme);
        sheet.getRange(task.row, 7).setValue(analysis.fps);

        // 更新任務資料
        task.visualizationType = analysis.visualization_type;
        task.colorScheme = analysis.color_scheme;
        task.fps = analysis.fps;

        // 生成影片
        updateTaskStatus(task.row, '生成中');
        const result = callFlaskGenerate(task);

        if (result.success) {
          const description = generateVideoDescription(
            task.songName,
            task.visualizationType,
            task.colorScheme
          );

          updateTaskStatus(
            task.row,
            '已完成',
            `AI建議：${analysis.reason}`,
            result.video_url || result.download_url,
            description
          );
          processCount++;
        } else {
          updateTaskStatus(task.row, '失敗', '', '', '', result.error);
        }

      } catch (error) {
        updateTaskStatus(task.row, '失敗', '', '', '', error.toString());
      }

      // 避免超過 Google API 限制，每處理一個任務暫停 2 秒
      Utilities.sleep(2000);
    }
  }

  SpreadsheetApp.getUi().alert(`✅ 批次處理完成！共處理 ${processCount} 個任務。`);
}

/**
 * 更新所有任務狀態
 */
function updateAllTaskStatus() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEETS.TASK_LIST);
  const data = sheet.getDataRange().getValues();

  let updateCount = 0;

  for (let i = 1; i < data.length; i++) {
    const status = data[i][8];
    const jobId = data[i][0]; // 假設序號就是 job ID

    if (status === '生成中') {
      try {
        const result = checkTaskStatus(jobId);

        if (result && result.status === 'completed') {
          updateTaskStatus(i + 1, '已完成', '', result.video_url);
          updateCount++;
        } else if (result && result.status === 'failed') {
          updateTaskStatus(i + 1, '失敗', '', '', '', result.error);
          updateCount++;
        }
      } catch (error) {
        Logger.log(`更新任務 ${jobId} 失敗：${error}`);
      }
    }
  }

  SpreadsheetApp.getUi().alert(`✅ 已更新 ${updateCount} 個任務狀態`);
}

/**
 * 清理失敗任務
 */
function cleanFailedTasks() {
  const ui = SpreadsheetApp.getUi();
  const response = ui.alert(
    '確認清理',
    '是否要將所有失敗任務重置為「待處理」狀態？',
    ui.ButtonSet.YES_NO
  );

  if (response !== ui.Button.YES) {
    return;
  }

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEETS.TASK_LIST);
  const data = sheet.getDataRange().getValues();

  let cleanCount = 0;

  for (let i = 1; i < data.length; i++) {
    if (data[i][8] === '失敗') {
      sheet.getRange(i + 1, 9).setValue('待處理'); // I欄：狀態
      sheet.getRange(i + 1, 15).setValue(''); // O欄：清空錯誤訊息
      cleanCount++;
    }
  }

  ui.alert(`✅ 已重置 ${cleanCount} 個失敗任務`);
}

/**
 * 顯示使用統計
 */
function showUsageStats() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEETS.TASK_LIST);
  const data = sheet.getDataRange().getValues();

  let total = data.length - 1;
  let completed = 0;
  let failed = 0;
  let processing = 0;
  let pending = 0;

  for (let i = 1; i < data.length; i++) {
    const status = data[i][8];
    if (status === '已完成') completed++;
    else if (status === '失敗') failed++;
    else if (status === '生成中' || status === 'AI分析中') processing++;
    else pending++;
  }

  const successRate = total > 0 ? ((completed / total) * 100).toFixed(1) : 0;

  const message = `📊 使用統計報告\n\n` +
    `總任務數：${total}\n` +
    `✅ 已完成：${completed}\n` +
    `⏳ 進行中：${processing}\n` +
    `📝 待處理：${pending}\n` +
    `❌ 失敗：${failed}\n\n` +
    `成功率：${successRate}%`;

  SpreadsheetApp.getUi().alert(message);
}

// ====================================
// 執行日誌
// ====================================

/**
 * 記錄執行日誌
 */
function logExecution(actionType, aiModel, status, responseTime, details) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEETS.EXECUTION_LOG);

    sheet.appendRow([
      new Date(),
      '',  // 任務序號（如有）
      actionType,
      aiModel,
      status,
      responseTime,
      '',  // Token 用量（如有）
      JSON.stringify(details).substring(0, 500)  // 限制長度
    ]);
  } catch (error) {
    Logger.log('日誌記錄失敗：' + error);
  }
}

// ====================================
// 測試函數
// ====================================

/**
 * 測試 Gemini API 連接
 */
function testGeminiConnection() {
  try {
    const result = callGeminiAPI('請說「連接成功」', 'flash');
    Logger.log('Gemini 測試成功：' + result);
    SpreadsheetApp.getUi().alert('✅ Gemini API 連接成功！\n\n回應：' + result);
  } catch (error) {
    SpreadsheetApp.getUi().alert('❌ Gemini API 連接失敗：\n\n' + error);
  }
}

/**
 * 測試 OpenAI API 連接
 */
function testOpenAIConnection() {
  try {
    const result = callGPTAPI('請說「連接成功」', 'gpt-5.6-terra');
    Logger.log('OpenAI 測試成功：' + result);
    SpreadsheetApp.getUi().alert('✅ OpenAI API 連接成功！\n\n回應：' + result);
  } catch (error) {
    SpreadsheetApp.getUi().alert('❌ OpenAI API 連接失敗：\n\n' + error);
  }
}

/**
 * 測試 Flask API 連接
 */
function testFlaskConnection() {
  try {
    const flaskUrl = getApiKeys().flaskUrl;
    const response = UrlFetchApp.fetch(flaskUrl + '/api/health');
    const result = JSON.parse(response.getContentText());

    SpreadsheetApp.getUi().alert('✅ Flask API 連接成功！\n\n狀態：' + JSON.stringify(result));
  } catch (error) {
    SpreadsheetApp.getUi().alert('❌ Flask API 連接失敗：\n\n' + error);
  }
}
