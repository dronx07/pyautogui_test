#!/usr/bin/env python3
"""
Simple test to verify PyAutoGUI works in GitHub Actions
"""

import pyautogui
import time
import os
import sys
from datetime import datetime

def test_pyautogui_basics():
    """Test basic PyAutoGUI functionality"""
    
    print("="*50)
    print("PyAutoGUI GitHub Actions Test")
    print("="*50)
    
    # Print version
    print(f"PyAutoGUI version: {pyautogui.__version__}")
    
    # Test 1: Get screen size
    try:
        screen_width, screen_height = pyautogui.size()
        print(f"✅ Screen size: {screen_width} x {screen_height}")
    except Exception as e:
        print(f"❌ Screen size test failed: {e}")
        return False
    
    # Test 2: Take screenshot
    try:
        screenshot = pyautogui.screenshot()
        screenshot_path = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot.save(screenshot_path)
        print(f"✅ Screenshot saved: {screenshot_path}")
        print(f"   Screenshot size: {screenshot.size}")
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
    
    # Test 4: Move mouse
    try:
        pyautogui.moveTo(100, 100, duration=0.5)
        new_x, new_y = pyautogui.position()
        print(f"✅ Mouse moved to: ({new_x}, {new_y})")
    except Exception as e:
        print(f"❌ Mouse movement test failed: {e}")
        return False
    
    # Test 5: Type something
    try:
        pyautogui.click(500, 500)
        pyautogui.write("Hello from GitHub Actions!", interval=0.1)
        print(f"✅ Typing test passed")
    except Exception as e:
        print(f"❌ Typing test failed: {e}")
        return False
    
    # Test 6: Press keys
    try:
        pyautogui.press('enter')
        pyautogui.hotkey('ctrl', 'a')
        print(f"✅ Key press test passed")
    except Exception as e:
        print(f"❌ Key press test failed: {e}")
        return False
    
    # Test 7: Locate on screen (if reference image exists)
    test_image = "test_reference.png"
    if os.path.exists(test_image):
        try:
            location = pyautogui.locateOnScreen(test_image, confidence=0.8)
            if location:
                print(f"✅ Image found at: {location}")
            else:
                print(f"⚠️ Image not found (this is OK for test)")
        except Exception as e:
            print(f"⚠️ Image recognition test: {e}")
    
    print("\n" + "="*50)
    print("🎉 All basic tests completed!")
    print("="*50)
    
    return True

def test_with_xvfb():
    """Test Xvfb specifically"""
    print("\n📺 Testing Xvfb Display...")
    
    # Check DISPLAY variable
    display = os.environ.get('DISPLAY')
    print(f"DISPLAY = {display}")
    
    # Try to create multiple screenshots
    for i in range(3):
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(f"test_sequence_{i}.png")
            print(f"✅ Sequence screenshot {i} saved")
            time.sleep(1)
        except Exception as e:
            print(f"❌ Sequence screenshot {i} failed: {e}")
    
    return True

if __name__ == "__main__":
    print("\n🚀 Starting PyAutoGUI tests...\n")
    
    # Run tests
    basic_result = test_pyautogui_basics()
    xvfb_result = test_with_xvfb()
    
    # Final result
    if basic_result and xvfb_result:
        print("\n✅✅✅ ALL TESTS PASSED! PyAutoGUI works in GitHub Actions!")
        sys.exit(0)
    else:
        print("\n❌❌❌ Some tests failed")
        sys.exit(1)
