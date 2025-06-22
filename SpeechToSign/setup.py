#!/usr/bin/env python3
"""
Setup script for Speech to Sign Language Translator
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("🔧 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_microphone():
    """Check if microphone is available"""
    print("🎤 Checking microphone availability...")
    try:
        import pyaudio
        audio = pyaudio.PyAudio()
        
        # Check for input devices
        input_devices = []
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append(device_info['name'])
        
        audio.terminate()
        
        if input_devices:
            print("✅ Microphone detected!")
            print("Available input devices:")
            for device in input_devices:
                print(f"  • {device}")
            return True
        else:
            print("❌ No microphone detected!")
            return False
            
    except Exception as e:
        print(f"❌ Error checking microphone: {e}")
        return False

def main():
    print("🤟 Speech to Sign Language Translator Setup 🤟")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("signlanguage.py"):
        print("❌ Error: Please run this script from the SpeechToSign directory")
        return
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed! Please check your internet connection and try again.")
        return
    
    # Check microphone
    mic_available = check_microphone()
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed!")
    
    if mic_available:
        print("✅ Your system is ready to use the Speech to Sign Language Translator!")
        print("📝 Run: python signlanguage.py")
    else:
        print("⚠️  Warning: No microphone detected. Please connect a microphone to use the translator.")
    
    print("\n📋 Available commands:")
    print("  • hello")
    print("  • thank you") 
    print("  • i like you")
    print("  • happy")
    print("  • nice to meet you")
    print("  • no")

if __name__ == "__main__":
    main()
