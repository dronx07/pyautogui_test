#!/usr/bin/env python3
"""
Simple test to verify PyAutoGUI works in GitHub Actions
"""

import pyautogui
import time
import os
import sys
from datetime import datetime


# CI safety settings
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.2


def test_pyautogui_basics():
    """Test basic PyAutoGUI functionality"""

    print("=" * 50)
    print("PyAutoGUI GitHub Actions Test")
    print("=" * 50)

    print(f"PyAutoGUI version: {pyautogui.__version__}")

    # Test 1: Screen size
    try:
        screen_width, screen_height = pyautogui.size()
        print(f"✅ Screen size: {screen_width} x {screen_height}")
    except Exception as e:
        print(f"❌ Screen size test failed: {e}")
        return False

    # Test 2: Screenshot
    try:
        screenshot = pyautogui.screenshot()
        path = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot.save(path)

        print(f"✅ Screenshot saved: {path}")
        print(f"Screenshot size: {screenshot.size}")
    except Exception as e:
        print(f"❌ Screenshot test failed: {e}")
        return False

    # Test 3: Mouse position
    try:
        x, y = pyautogui.position()
        print(f"✅ Mouse position: ({x}, {y})")
    except Exception as e:
        print(f"❌ Mouse position test failed: {e}")
        return False

    # Test 4: Move mouse safely within screen
    try:
        target_x = min(100, screen_width - 1)
        target_y = min(100, screen_height - 1)

        pyautogui.moveTo(target_x, target_y, duration=0.5)
        new_x, new_y = pyautogui.position()

        print(f"✅ Mouse moved to: ({new_x}, {new_y})")
    except Exception as e:
        print(f"❌ Mouse movement test failed: {e}")
        return False

    # Test 5: Mouse click
    try:
        pyautogui.click(target_x, target_y)
        print("✅ Mouse click test passed")
    except Exception as e:
        print(f"❌ Mouse click test failed: {e}")
        return False

    # Test 6: Keyboard test (safe)
    try:
        pyautogui.press("enter")
        pyautogui.press("tab")
        print("✅ Keyboard test passed")
    except Exception as e:
        print(f"❌ Keyboard test failed: {e}")
        return False

    print("\n" + "=" * 50)
    print("🎉 Basic tests completed")
    print("=" * 50)

    return True


def test_with_xvfb():
    """Test Xvfb display behavior"""

    print("\n📺 Testing Xvfb display")

    display = os.environ.get("DISPLAY")
    print(f"DISPLAY = {display}")

    for i in range(3):
        try:
            screenshot = pyautogui.screenshot()
            filename = f"test_sequence_{i}.png"
            screenshot.save(filename)

            print(f"✅ Screenshot {i} saved")
            time.sleep(1)

        except Exception as e:
            print(f"❌ Screenshot {i} failed: {e}")
            return False

    return True


if __name__ == "__main__":

    print("\n🚀 Starting PyAutoGUI tests\n")

    basic_result = test_pyautogui_basics()
    xvfb_result = test_with_xvfb()

    if basic_result and xvfb_result:
        print("\n✅ ALL TESTS PASSED — PyAutoGUI works in GitHub Actions!")
        sys.exit(0)

    print("\n❌ Some tests failed")
    sys.exit(1)
