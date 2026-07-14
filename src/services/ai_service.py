"""
Eye Music - AI 服務整合模組
統一管理 OpenAI (GPT-5.6 Terra/GPT-5.6 Terra) 和 Google AI (Gemini 3.5 Flash/Pro) 的 API 呼叫
"""
import os
import logging
from typing import Dict, Any, Optional
import json

logger = logging.getLogger(__name__)


class AIService:
    """
    AI 服務統一介面
    支援多個 AI 模型的切換使用
    """

    def __init__(self):
        """初始化 AI 服務"""
        self.openai_client = None
        self.gemini_models = {}
        self._initialize_clients()

    def _initialize_clients(self):
        """初始化各 AI 服務的客戶端"""
        # 初始化 OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            try:
                import openai
                self.openai_client = openai.OpenAI(api_key=openai_key)
                logger.info("✅ OpenAI 客戶端初始化成功")
            except Exception as e:
                logger.warning(f"⚠️ OpenAI 初始化失敗: {e}")

        # 初始化 Google Generative AI (Gemini)
        gemini_key = os.getenv('GOOGLE_AI_API_KEY')
        if gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)

                # 初始化不同的 Gemini 模型
                self.gemini_models = {
                    'flash': genai.GenerativeModel('gemini-3.5-flash'),
                    'pro': genai.GenerativeModel('gemini-3.1-pro-preview')
                }
                logger.info("✅ Gemini 客戶端初始化成功")
            except Exception as e:
                logger.warning(f"⚠️ Gemini 初始化失敗: {e}")

    # ========================================
    # Gemini API 整合
    # ========================================

    def call_gemini(
        self,
        prompt: str,
        model_type: str = 'flash',
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Optional[str]:
        """
        呼叫 Gemini API

        Args:
            prompt: 提示詞
            model_type: 'flash' 或 'pro'
            temperature: 溫度參數 (0-1)
            max_tokens: 最大輸出 token 數

        Returns:
            AI 回應文字，失敗時返回 None
        """
        if model_type not in self.gemini_models:
            logger.error(f"❌ 不支援的 Gemini 模型: {model_type}")
            return None

        try:
            model = self.gemini_models[model_type]

            # 設定生成參數
            generation_config = {
                'temperature': temperature,
                'max_output_tokens': max_tokens,
                'top_p': 0.95,
                'top_k': 40
            }

            # 生成回應
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )

            return response.text

        except Exception as e:
            logger.error(f"❌ Gemini API 呼叫失敗: {e}")
            return None

    def analyze_music_style_gemini(self, song_name: str) -> Dict[str, Any]:
        """
        使用 Gemini 3.5 Flash 快速分析音樂風格

        Args:
            song_name: 歌曲名稱

        Returns:
            分析結果 dict
        """
        prompt = f"""分析歌曲「{song_name}」的音樂風格，並以 JSON 格式回傳最適合的視覺化參數。

回傳格式（請直接回傳 JSON，不要有其他文字）：
{{
  "visualization_type": "bars/circular/piano 三選一",
  "color_scheme": "rainbow/fire/ocean/purple 四選一",
  "fps": 24/30/60 三選一（數字）,
  "reason": "選擇理由（繁體中文，50字內）",
  "style_tags": ["標籤1", "標籤2", "標籤3"],
  "mood": "情緒描述",
  "tempo_category": "slow/medium/fast"
}}"""

        response = self.call_gemini(prompt, model_type='flash')

        if response:
            try:
                # 清理回應（移除可能的 markdown 標記）
                clean_response = response.strip()
                clean_response = clean_response.replace('```json\n', '').replace('```\n', '').replace('```', '')
                result = json.loads(clean_response)
                return result
            except json.JSONDecodeError as e:
                logger.error(f"❌ JSON 解析失敗: {e}\n回應內容: {response}")

        # 返回預設值
        return {
            'visualization_type': 'circular',
            'color_scheme': 'rainbow',
            'fps': 30,
            'reason': 'AI 分析失敗，使用預設參數',
            'style_tags': ['預設'],
            'mood': 'neutral',
            'tempo_category': 'medium'
        }

    def get_creative_suggestion_gemini(
        self,
        song_name: str,
        current_params: Dict[str, Any]
    ) -> str:
        """
        使用 Gemini 3.1 Pro 提供深度創意建議

        Args:
            song_name: 歌曲名稱
            current_params: 當前參數設定

        Returns:
            創意建議文字
        """
        prompt = f"""針對歌曲「{song_name}」提供深度創意視覺化建議。

目前參數：
- 視覺化類型：{current_params.get('visualization_type', 'N/A')}
- 色彩方案：{current_params.get('color_scheme', 'N/A')}
- FPS：{current_params.get('fps', 'N/A')}

請提供（繁體中文）：
1. 視覺化優化建議（考慮音樂心理學）
2. 色彩心理學分析
3. 目標觀眾群分析
4. 特殊效果建議
5. 社群媒體傳播建議

請結構化且具體地回答。"""

        response = self.call_gemini(prompt, model_type='pro', max_tokens=3000)
        return response or "深度分析功能暫時無法使用"

    # ========================================
    # OpenAI GPT API 整合
    # ========================================

    def call_gpt(
        self,
        prompt: str,
        model: str = 'gpt-5.6-terra',
        system_message: str = '你是一位音樂視覺化專家，精通音樂分析與視覺設計。',
        temperature: float = 0.8,
        max_tokens: int = 2000
    ) -> Optional[str]:
        """
        呼叫 OpenAI GPT API

        Args:
            prompt: 提示詞
            model: 模型名稱 ('gpt-5.6-terra' 或 'gpt-5.6-terra')
            system_message: 系統訊息
            temperature: 溫度參數
            max_tokens: 最大輸出 token 數

        Returns:
            AI 回應文字，失敗時返回 None
        """
        if not self.openai_client:
            logger.error("❌ OpenAI 客戶端未初始化")
            return None

        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"❌ OpenAI API 呼叫失敗: {e}")
            return None

    def generate_video_description_gpt(
        self,
        song_name: str,
        visualization_type: str,
        color_scheme: str
    ) -> str:
        """
        使用 GPT-5.6 Terra 生成影片描述文字

        Args:
            song_name: 歌曲名稱
            visualization_type: 視覺化類型
            color_scheme: 色彩方案

        Returns:
            影片描述文字
        """
        prompt = f"""為音樂視覺化影片生成吸引人的描述文字（100-150字，繁體中文）：

- 歌曲：{song_name}
- 視覺化類型：{visualization_type}
- 色彩方案：{color_scheme}

要求：
- 使用生動、有感染力的語言
- 突出視覺效果特色
- 引發觀眾興趣
- 適合 YouTube 影片描述
- 包含適當的情感詞彙"""

        response = self.call_gpt(prompt, model='gpt-5.6-terra')

        return response or f"體驗{song_name}的視覺饗宴！採用{visualization_type}視覺化效果與{color_scheme}色彩方案，讓音樂與視覺完美結合。"

    def generate_social_media_content_gpt(
        self,
        song_name: str,
        description: str,
        style_tags: list = None
    ) -> Dict[str, Any]:
        """
        使用 GPT-5.6 Terra 生成社群媒體文案

        Args:
            song_name: 歌曲名稱
            description: 影片描述
            style_tags: 風格標籤列表

        Returns:
            包含多種文案的 dict
        """
        tags_str = ', '.join(style_tags) if style_tags else '未提供'

        prompt = f"""為音樂視覺化影片生成完整的社群媒體發布內容包：

歌曲：{song_name}
影片描述：{description}
風格標籤：{tags_str}

請以 JSON 格式回傳（直接回傳 JSON，不要有其他文字）：
{{
  "youtube_title": "YouTube 標題（吸睛、SEO友善、繁體中文、50字內）",
  "youtube_description": "YouTube 完整描述（包含換行、繁體中文、200-300字）",
  "hashtags": ["標籤1", "標籤2", ...（10-15個繁體中文和英文混合標籤）],
  "instagram_caption": "Instagram 文案（含適當 emoji、繁體中文、150字內）",
  "facebook_post": "Facebook 貼文（吸引人、繁體中文、100-150字）",
  "twitter_tweet": "Twitter/X 推文（簡潔有力、繁體中文、100字內）",
  "tiktok_caption": "TikTok 文案（年輕化、含 emoji、50字內）"
}}"""

        response = self.call_gpt(prompt, model='gpt-5.6-terra', temperature=0.9, max_tokens=3000)

        if response:
            try:
                clean_response = response.strip()
                clean_response = clean_response.replace('```json\n', '').replace('```\n', '').replace('```', '')
                result = json.loads(clean_response)
                return result
            except json.JSONDecodeError as e:
                logger.error(f"❌ JSON 解析失敗: {e}\n回應內容: {response}")

        # 返回預設值
        return {
            'youtube_title': f'{song_name} - 音樂視覺化',
            'youtube_description': description,
            'hashtags': ['音樂視覺化', '視覺藝術', song_name, 'MusicVisualization', 'AudioVisual'],
            'instagram_caption': f'🎵 {song_name} 視覺化作品 ✨\n\n{description[:100]}...',
            'facebook_post': f'🎶 全新音樂視覺化作品發布！\n\n{song_name}\n\n{description[:80]}...',
            'twitter_tweet': f'🎵 {song_name} 音樂視覺化\n\n{description[:80]}...',
            'tiktok_caption': f'🎵 {song_name} ✨ #音樂視覺化 #MusicVisualization'
        }

    # ========================================
    # 智能路由功能
    # ========================================

    def smart_analyze(self, song_name: str, use_pro: bool = False) -> Dict[str, Any]:
        """
        智能分析：自動選擇最佳 AI 模型

        Args:
            song_name: 歌曲名稱
            use_pro: 是否強制使用 Pro 模型

        Returns:
            分析結果
        """
        # 優先使用 Gemini（速度快、成本低）
        if self.gemini_models:
            model_type = 'pro' if use_pro else 'flash'
            return self.analyze_music_style_gemini(song_name)

        # 備選：使用 GPT-5.6 Terra
        if self.openai_client:
            logger.info("⚠️ Gemini 不可用，使用 GPT-5.6 Terra")
            # 可以實作 GPT 版本的音樂分析
            return {
                'visualization_type': 'circular',
                'color_scheme': 'rainbow',
                'fps': 30,
                'reason': '使用 GPT 分析',
                'style_tags': ['AI分析']
            }

        # 都不可用時返回預設值
        logger.warning("⚠️ 所有 AI 服務都不可用，使用預設參數")
        return {
            'visualization_type': 'bars',
            'color_scheme': 'rainbow',
            'fps': 30,
            'reason': 'AI 服務不可用',
            'style_tags': ['預設']
        }

    def get_service_status(self) -> Dict[str, bool]:
        """
        檢查各 AI 服務的可用狀態

        Returns:
            服務狀態 dict
        """
        return {
            'openai': self.openai_client is not None,
            'gemini_flash': 'flash' in self.gemini_models,
            'gemini_pro': 'pro' in self.gemini_models
        }


# ========================================
# 全域實例
# ========================================

# 建立全域 AI 服務實例
ai_service = AIService()


# ========================================
# 便捷函數
# ========================================

def analyze_music_style(song_name: str) -> Dict[str, Any]:
    """快速分析音樂風格（使用 Gemini Flash）"""
    return ai_service.analyze_music_style_gemini(song_name)


def get_creative_suggestion(song_name: str, params: Dict[str, Any]) -> str:
    """獲取創意建議（使用 Gemini Pro）"""
    return ai_service.get_creative_suggestion_gemini(song_name, params)


def generate_video_description(song_name: str, viz_type: str, color: str) -> str:
    """生成影片描述（使用 GPT-5.6 Terra）"""
    return ai_service.generate_video_description_gpt(song_name, viz_type, color)


def generate_social_content(song_name: str, description: str, tags: list = None) -> Dict[str, Any]:
    """生成社群媒體內容（使用 GPT-5.6 Terra）"""
    return ai_service.generate_social_media_content_gpt(song_name, description, tags)


def get_ai_service_status() -> Dict[str, bool]:
    """獲取 AI 服務狀態"""
    return ai_service.get_service_status()


# ========================================
# 測試函數
# ========================================

if __name__ == '__main__':
    # 載入環境變數
    from dotenv import load_dotenv
    load_dotenv()

    # 測試 AI 服務
    print("🔍 測試 AI 服務整合\n")

    # 檢查服務狀態
    status = get_ai_service_status()
    print(f"📊 服務狀態: {status}\n")

    # 測試音樂分析
    if status['gemini_flash']:
        print("🎵 測試音樂風格分析（Gemini Flash）...")
        result = analyze_music_style("夜曲 - 周杰倫")
        print(f"結果: {json.dumps(result, ensure_ascii=False, indent=2)}\n")

    # 測試描述生成
    if status['openai']:
        print("📝 測試影片描述生成（GPT-5.6 Terra）...")
        desc = generate_video_description("夜曲 - 周杰倫", "circular", "purple")
        print(f"描述: {desc}\n")

    print("✅ 測試完成！")
