#!/usr/bin/env python3
"""
Complete GIF Test Script
Tests all available GIF files to ensure they work properly
"""
import os
import sys
from pathlib import Path

def test_gif_files():
    """Test all GIF files in the directory"""
    print("🧪 Testing all GIF files in the Speech to Sign Language project")
    print("=" * 60)
    
    # Get current directory
    current_dir = Path(__file__).parent
    
    # List of expected GIF files
    expected_gifs = [
        "hello.gif",
        "Thank you.gif", 
        "I like you.gif",
        "happy.gif",
        "nice_to_meet_you.gif",
        "no.gif"
    ]
    
    print("🔍 Checking for GIF files...")
    
    missing_files = []
    found_files = []
    
    for gif_file in expected_gifs:
        gif_path = current_dir / gif_file
        if gif_path.exists():
            file_size = gif_path.stat().st_size
            print(f"✅ {gif_file} - Found ({file_size} bytes)")
            found_files.append(gif_file)
        else:
            print(f"❌ {gif_file} - Missing")
            missing_files.append(gif_file)
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results:")
    print(f"   ✅ Found: {len(found_files)}/{len(expected_gifs)} files")
    print(f"   ❌ Missing: {len(missing_files)} files")
    
    if missing_files:
        print(f"\n❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n💡 Make sure all GIF files are in the SpeechToSign directory")
    else:
        print("\n🎉 All GIF files are present!")
    
    # Test if we can import required modules
    print("\n🔧 Testing Python dependencies...")
    try:
        import cv2
        print("✅ OpenCV (cv2) - Available")
    except ImportError:
        print("❌ OpenCV (cv2) - Missing (pip install opencv-python)")
    
    try:
        from PIL import Image, ImageSequence
        print("✅ PIL (Pillow) - Available")
    except ImportError:
        print("❌ PIL (Pillow) - Missing (pip install Pillow)")
    
    try:
        import numpy as np
        print("✅ NumPy - Available")
    except ImportError:
        print("❌ NumPy - Missing (pip install numpy)")
    
    return len(missing_files) == 0

def test_individual_gif(gif_file):
    """Test loading and basic properties of a single GIF"""
    try:
        from PIL import Image, ImageSequence
        import cv2
        import numpy as np
        
        current_dir = Path(__file__).parent
        gif_path = current_dir / gif_file
        
        if not gif_path.exists():
            print(f"❌ {gif_file} not found")
            return False
        
        # Test with PIL
        try:
            im = Image.open(gif_path)
            frames = list(ImageSequence.Iterator(im))
            frame_count = len(frames)
            width, height = im.size
            
            print(f"📁 {gif_file}:")
            print(f"   📐 Size: {width}x{height}")
            print(f"   🎬 Frames: {frame_count}")
            
            # Test first frame conversion
            first_frame = frames[0].convert('RGB')
            opencv_image = cv2.cvtColor(np.array(first_frame), cv2.COLOR_RGB2BGR)
            print(f"   ✅ Successfully converted to OpenCV format")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing {gif_file}: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Missing required modules: {e}")
        return False

def main():
    """Main test function"""
    print("🤟 Speech to Sign Language - GIF Testing Tool 🤟")
    print("=" * 60)
    
    # Test all GIF files
    all_files_present = test_gif_files()
    
    if all_files_present:
        print("\n🧪 Testing individual GIF properties...")
        print("-" * 40)
        
        expected_gifs = [
            "hello.gif",
            "Thank you.gif", 
            "I like you.gif",
            "happy.gif",
            "nice_to_meet_you.gif",
            "no.gif"
        ]
        
        successful_tests = 0
        for gif_file in expected_gifs:
            if test_individual_gif(gif_file):
                successful_tests += 1
            print()
        
        print("=" * 60)
        print(f"🏆 Final Results: {successful_tests}/{len(expected_gifs)} GIFs tested successfully")
        
        if successful_tests == len(expected_gifs):
            print("🎉 All GIF files are working properly!")
            print("✅ You can now run the main application:")
            print("   python signlanguage_fixed.py")
        else:
            print("⚠️ Some GIF files have issues. Check the output above.")
    else:
        print("\n❌ Cannot proceed with detailed testing due to missing files.")
        print("💡 Please ensure all GIF files are in the SpeechToSign directory.")

if __name__ == "__main__":
    main()
