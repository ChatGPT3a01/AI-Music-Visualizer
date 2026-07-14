"""
音樂視覺化核心引擎
Music Visualizer Core Engine
"""
import numpy as np
import librosa
import moviepy.editor as mp
from PIL import Image, ImageDraw, ImageFont
import scipy.signal as signal
from pathlib import Path
import json
from typing import Dict, Callable, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MusicVisualizer:
    """音樂視覺化處理器"""

    def __init__(self, config: Dict):
        """
        初始化視覺化器

        Args:
            config: 配置字典，包含所有視覺化參數
        """
        self.config = config
        self.audio_path = config.get('audio_path')
        self.output_path = config.get('output_path')
        self.visualization_type = config.get('visualization_type', 'spectrum_bars')

        # 視訊參數
        self.fps = config.get('fps', 30)
        self.resolution = config.get('resolution', (1920, 1080))
        self.duration = config.get('duration', None)

        # 視覺化參數
        self.spectrum_height_multiplier = config.get('spectrum_height_multiplier', 1.0)
        self.spectrum_opacity = config.get('spectrum_opacity', 0.8)
        self.color_scheme = config.get('color_scheme', 'rainbow')
        self.background_color = config.get('background_color', (0, 0, 0))
        self.blur_effect = config.get('blur_effect', False)

        # 音頻分析參數
        self.n_fft = config.get('n_fft', 2048)
        self.hop_length = config.get('hop_length', 512)
        self.n_mels = config.get('n_mels', 128)

        # 進度回調
        self.progress_callback = config.get('progress_callback', None)

        # 載入音頻
        self.y = None
        self.sr = None
        self.load_audio()

    def load_audio(self):
        """載入音頻檔案"""
        try:
            logger.info(f"載入音頻: {self.audio_path}")
            self.y, self.sr = librosa.load(self.audio_path, sr=None)
            if self.duration is None:
                self.duration = librosa.get_duration(y=self.y, sr=self.sr)
            logger.info(f"音頻載入成功 - 採樣率: {self.sr}, 時長: {self.duration:.2f}秒")
        except Exception as e:
            logger.error(f"音頻載入失敗: {e}")
            raise

    def extract_features(self):
        """提取音頻特徵"""
        logger.info("提取音頻特徵...")

        # 計算頻譜圖
        self.stft = np.abs(librosa.stft(self.y, n_fft=self.n_fft, hop_length=self.hop_length))

        # 計算梅爾頻譜
        self.mel_spec = librosa.feature.melspectrogram(
            y=self.y, sr=self.sr, n_fft=self.n_fft,
            hop_length=self.hop_length, n_mels=self.n_mels
        )
        self.mel_spec_db = librosa.power_to_db(self.mel_spec, ref=np.max)

        # 計算色度特徵
        self.chroma = librosa.feature.chroma_stft(
            y=self.y, sr=self.sr, n_fft=self.n_fft, hop_length=self.hop_length
        )

        # 計算節奏特徵
        self.tempo, self.beats = librosa.beat.beat_track(y=self.y, sr=self.sr)

        logger.info(f"特徵提取完成 - Tempo: {self.tempo:.2f} BPM")

    def get_color_gradient(self, value: float, scheme: str = 'rainbow'):
        """
        根據值生成漸變色

        Args:
            value: 0-1 之間的值
            scheme: 色彩方案

        Returns:
            RGB 元組
        """
        value = np.clip(value, 0, 1)

        if scheme == 'rainbow':
            # 彩虹色
            if value < 0.2:
                r = 255
                g = int(value * 5 * 255)
                b = 0
            elif value < 0.4:
                r = int((0.4 - value) * 5 * 255)
                g = 255
                b = 0
            elif value < 0.6:
                r = 0
                g = 255
                b = int((value - 0.4) * 5 * 255)
            elif value < 0.8:
                r = 0
                g = int((0.8 - value) * 5 * 255)
                b = 255
            else:
                r = int((value - 0.8) * 5 * 255)
                g = 0
                b = 255
        elif scheme == 'fire':
            # 火焰色
            r = 255
            g = int(value * 255)
            b = int(value * 128)
        elif scheme == 'ocean':
            # 海洋色
            r = int(value * 100)
            g = int(value * 200)
            b = 255
        elif scheme == 'purple':
            # 紫色系
            r = int(128 + value * 127)
            g = int(value * 100)
            b = int(200 + value * 55)
        else:
            # 預設灰階
            r = g = b = int(value * 255)

        return (r, g, b)

    def generate_spectrum_bars(self, frame_idx: int) -> Image.Image:
        """生成頻譜能量條視覺化"""
        width, height = self.resolution
        img = Image.new('RGB', (width, height), self.background_color)
        draw = ImageDraw.Draw(img, 'RGBA')

        # 計算當前時間的頻譜
        time_idx = int(frame_idx * self.hop_length / self.sr * self.fps)
        if time_idx >= self.stft.shape[1]:
            time_idx = self.stft.shape[1] - 1

        spectrum = self.stft[:, time_idx]

        # 取對數並正規化
        spectrum_db = librosa.amplitude_to_db(spectrum, ref=np.max)
        spectrum_normalized = (spectrum_db - spectrum_db.min()) / (spectrum_db.max() - spectrum_db.min() + 1e-8)

        # 繪製能量條
        n_bars = min(100, len(spectrum_normalized))
        bar_width = width / n_bars

        for i in range(n_bars):
            bar_height = spectrum_normalized[i * len(spectrum_normalized) // n_bars] * height * self.spectrum_height_multiplier
            x1 = i * bar_width
            y1 = height - bar_height
            x2 = (i + 1) * bar_width - 2
            y2 = height

            color = self.get_color_gradient(spectrum_normalized[i * len(spectrum_normalized) // n_bars], self.color_scheme)
            color_with_alpha = color + (int(255 * self.spectrum_opacity),)

            draw.rectangle([x1, y1, x2, y2], fill=color_with_alpha)

        return img

    def generate_circular_spectrum(self, frame_idx: int) -> Image.Image:
        """生成圓形頻譜視覺化"""
        width, height = self.resolution
        img = Image.new('RGB', (width, height), self.background_color)
        draw = ImageDraw.Draw(img, 'RGBA')

        center_x, center_y = width // 2, height // 2
        base_radius = min(width, height) // 4

        # 計算當前時間的頻譜
        time_idx = int(frame_idx * self.hop_length / self.sr * self.fps)
        if time_idx >= self.stft.shape[1]:
            time_idx = self.stft.shape[1] - 1

        spectrum = self.stft[:, time_idx]
        spectrum_db = librosa.amplitude_to_db(spectrum, ref=np.max)
        spectrum_normalized = (spectrum_db - spectrum_db.min()) / (spectrum_db.max() - spectrum_db.min() + 1e-8)

        # 繪製圓形頻譜
        n_bars = min(120, len(spectrum_normalized))
        angle_step = 360 / n_bars

        for i in range(n_bars):
            angle = i * angle_step
            value = spectrum_normalized[i * len(spectrum_normalized) // n_bars]
            radius = base_radius + value * base_radius * self.spectrum_height_multiplier

            # 計算起點和終點
            angle_rad = np.radians(angle)
            x1 = center_x + base_radius * np.cos(angle_rad)
            y1 = center_y + base_radius * np.sin(angle_rad)
            x2 = center_x + radius * np.cos(angle_rad)
            y2 = center_y + radius * np.sin(angle_rad)

            color = self.get_color_gradient(value, self.color_scheme)
            color_with_alpha = color + (int(255 * self.spectrum_opacity),)

            draw.line([x1, y1, x2, y2], fill=color_with_alpha, width=3)

        return img

    def generate_piano_roll(self, frame_idx: int) -> Image.Image:
        """生成鋼琴瀑布流視覺化"""
        width, height = self.resolution
        img = Image.new('RGB', (width, height), self.background_color)
        draw = ImageDraw.Draw(img, 'RGBA')

        # 計算時間範圍
        time_idx = int(frame_idx * self.hop_length / self.sr * self.fps)
        time_window = 100  # 顯示的時間窗口

        # 繪製色度圖
        for t in range(max(0, time_idx - time_window), time_idx):
            if t >= self.chroma.shape[1]:
                break

            x = width * (t - (time_idx - time_window)) / time_window

            for note in range(12):
                value = self.chroma[note, t]
                y = height * note / 12
                note_height = height / 12

                if value > 0.1:  # 只顯示有音符的地方
                    color = self.get_color_gradient(value, self.color_scheme)
                    color_with_alpha = color + (int(255 * value * self.spectrum_opacity),)

                    draw.rectangle([x, y, x + width / time_window, y + note_height],
                                   fill=color_with_alpha)

        return img

    def generate_frame(self, frame_idx: int) -> np.ndarray:
        """
        生成單一幀

        Args:
            frame_idx: 幀索引

        Returns:
            numpy 陣列 (RGB)
        """
        if self.visualization_type == 'spectrum_bars':
            img = self.generate_spectrum_bars(frame_idx)
        elif self.visualization_type == 'circular_spectrum':
            img = self.generate_circular_spectrum(frame_idx)
        elif self.visualization_type == 'piano_roll':
            img = self.generate_piano_roll(frame_idx)
        else:
            # 預設使用頻譜條
            img = self.generate_spectrum_bars(frame_idx)

        return np.array(img)

    def generate_video(self):
        """生成完整視覺化影片"""
        logger.info("開始生成視覺化影片...")

        # 提取特徵
        self.extract_features()

        # 計算總幀數
        total_frames = int(self.duration * self.fps)

        # 生成影片幀
        def make_frame(t):
            frame_idx = int(t * self.fps)
            if self.progress_callback:
                progress = min(100, int((frame_idx / total_frames) * 100))
                self.progress_callback(progress, f"正在渲染第 {frame_idx}/{total_frames} 幀")
            return self.generate_frame(frame_idx)

        # 建立影片
        video = mp.VideoClip(make_frame, duration=self.duration)

        # 載入音頻
        audio = mp.AudioFileClip(self.audio_path)
        video = video.set_audio(audio)

        # 輸出影片
        logger.info(f"輸出影片到: {self.output_path}")
        video.write_videofile(
            self.output_path,
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            logger=None
        )

        if self.progress_callback:
            self.progress_callback(100, "影片生成完成！")

        logger.info("視覺化影片生成完成！")

        return self.output_path


def create_visualizer(config: Dict) -> MusicVisualizer:
    """
    工廠函數：創建視覺化器實例

    Args:
        config: 配置字典

    Returns:
        MusicVisualizer 實例
    """
    return MusicVisualizer(config)
