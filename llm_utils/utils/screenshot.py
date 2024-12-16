import pyautogui
from PIL import Image
import os
import shutil
import uuid
from time import sleep


IMAGE_FOLDER = "/Users/oscarjuliusadserballe/cli_scripts/llm_utils/temp/"

def clear_temp_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)

def take_screenshot():
    clear_temp_folder(IMAGE_FOLDER)

    unique_filename = f"screenshot_{uuid.uuid4().hex}.png"
    path = os.path.join(IMAGE_FOLDER, unique_filename)

    screenshot = pyautogui.screenshot()
    screenshot.save(path)
    print(f"Screenshot taken and saved to {path}")

    img = Image.open(path)
    return img
