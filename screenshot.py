import mss
import base64
from io import BytesIO
from PIL import Image

def getScreenshot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot =  sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        img = img.resize((1344,336))
        # Save the image to a bytes buffer
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img.save("test.png", format="PNG")
        
        
        # Convert bytes to Base64
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
