import mss
import os
import time
from datetime import datetime


class ScreenScanner:
    """Screen capture and desktop vision analysis."""

    OUTPUT_DIR = "screenshots"

    def __init__(self):
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)

    @staticmethod
    def capture_screen(output_path: str = "screen_capture.png") -> str:
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_path)
                return output_path
        except Exception as e:
            print(f"Screen capture error: {e}")
            return None

    @staticmethod
    def capture_with_timestamp() -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"screenshots/screen_{timestamp}.png"
        os.makedirs("screenshots", exist_ok=True)
        return ScreenScanner.capture_screen(output_path)
