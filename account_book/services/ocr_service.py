"""
OCR 服务 - 图片文字识别

支持远程 API 和 mock 实现
"""

import os
import requests


class OCRService:
    """OCR 服务类"""

    def __init__(self):
        self.provider = 'remote'
        self.api_url = "https://mai8z4cdp3o8c3p0.aistudio-app.com/ocr"
        self.token = "59dceb11cf50ded642e40f14c3a0b31999684562"
        self._init_providers()

    def _init_providers(self):
        """初始化提供商"""
        self.providers = {
            'mock': self._recognize_mock,
            'remote': self._recognize_remote,
            # 'paddleocr': self._recognize_paddle,
        }

    def set_provider(self, provider):
        """设置 OCR 提供商"""
        if provider in self.providers:
            self.provider = provider
            print(f"[OCRService] Provider set to: {provider}")
        else:
            print(f"[OCRService] Unknown provider: {provider}, keeping {self.provider}")

    def recognize_image(self, image_path):
        """
        识别图片中的文字

        Args:
            image_path: 图片文件路径

        Returns:
            str: 识别出的文字内容
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        try:
            return self._recognize_remote(image_path)
        except Exception as e:
            print(f"[OCRService] Remote OCR failed: {e}, falling back to mock")
            return self._recognize_mock(image_path)

    def _recognize_remote(self, image_path):
        """调用远程 OCR API"""
        with open(image_path, 'rb') as f:
            files = {'file': f}
            headers = {'Authorization': f'Bearer {self.token}'}
            response = requests.post(self.api_url, files=files, headers=headers, timeout=30)

        response.raise_for_status()
        result = response.json()
        return result.get('text', '')

    def _recognize_mock(self, image_path):
        """Mock OCR 实现"""
        filename = os.path.basename(image_path)
        if 'test' in filename.lower():
            return "测试图片，无实际内容"
        return "请替换为真实 OCR 识别结果"


# 全局单例
ocr_service = OCRService()
