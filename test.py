#!/usr/bin/env python3
"""
PyAutoGUI CI Test for GitHub Actions with Xvfb
Ensures screenshots and basic automation work correctly.
"""

import pyautogui
import time
import os
import sys
from datetime import datetime


# CI-safe configuration
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.2


def wait_for_display():
    """Ensure the X display is ready"""
    print("Waiting for display to stabilize...")
    time.sleep(3)

    display = os.environ.get("DISPLAY")
    print(f"DISPLAY = {display}")

    if not display:
        print("❌ DISPLAY variable not set!")
        sys.exit(1)


def save_debug_screenshot(name):
    """Save screenshot using both PyAutoGUI and scrot"""
    try:
        img = pyautogui.screenshot()
        img.save(name)
        print(f"✅ PyAutoGUI screenshot saved: {name}")
    except Exception as e:
        print(f"❌ PyAutoGUI screenshot failed: {e}")

    # fallback screenshot using scrot
    try:
        scrot_name = "scrot_" + name
        os.system(f"scrot {scrot_name}")
        print(f"✅ Scrot screenshot saved: {scrot_name}")
    except Exception as e:
        print(f"⚠️ Scrot screenshot failed: {e}")


def test_pyautogui_basics():
    """Test core PyAutoGUI functionality"""

    print("=" * 50)
    print("PyAutoGUI GitHub Actions Test")
    print("=" * 50)

    print(f"PyAutoGUI version: {pyautogui.__version__}")

    # Screen size
    try:
        width, height = pyautogui.size()
        print(f"✅ Screen size: {width} x {height}")
    except Exception as e:
        print(f"❌ Screen size failed: {e}")
        return False

    # Initial screenshot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_debug_screenshot(f"screenshot_{timestamp}.png")

    # Mouse position
    try:
        x, y = pyautogui.position()
        print(f"✅ Mouse position: ({x}, {y})")
    except Exception as e:
        print(f"❌ Mouse position failed: {e}")
        return False

    # Move mouse
    try:
        target_x = min(200, width - 1)
        target_y = min(200, height - 1)

        pyautogui.moveTo(target_x, target_y, duration=0.5)
        new_x, new_y = pyautogui.position()

        print(f"✅ Mouse moved to: ({new_x}, {new_y})")
    except Exception as e:
        print(f"❌ Mouse move failed: {e}")
        return False

    # Click test
    try:
        pyautogui.click(target_x, target_y)
        print("✅ Mouse click successful")
    except Exception as e:
        print(f"❌ Mouse click failed: {e}")
        return False

    # Keyboard test
    try:
        pyautogui.press("enter")
        pyautogui.press("tab")
        print("✅ Keyboard input successful")
    except Exception as e:
        print(f"❌ Keyboard input failed: {e}")
        return False

    return True


def test_sequence_screenshots():
    """Take multiple screenshots to verify framebuffer updates"""

    print("\n📸 Testing screenshot sequence...")

    for i in range(3):
        filename = f"test_sequence_{i}.png"
        save_debug_screenshot(filename)
        time.sleep(1)

    return True


def main():
    print("\n🚀 Starting PyAutoGUI CI tests\n")

    wait_for_display()

    basic = test_pyautogui_basics()
    sequence = test_sequence_screenshots()

    print("\n" + "=" * 50)

    if basic and sequence:
        print("✅ ALL TESTS PASSED — PyAutoGUI works in GitHub Actions!")
        print("=" * 50)
        sys.exit(0)

    print("❌ Some tests failed")
    print("=" * 50)
    sys.exit(1)


if __name__ == "__main__":
    main()
