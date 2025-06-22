import speech_recognition as sr
import cv2
from PIL import Image, ImageSequence
import os
import numpy as np
import time

# Note: Removed mediapipe dependency as it's not compatible with Python 3.13
# The hand detection functionality was initialized but not used in the main program

print("🤟 Speech to Sign Language Translator 🤟")
print("=" * 50)
print("Available signs:")
available_signs = ["hello", "thank you", "i like you", "happy", "nice to meet you", "no"]
for sign in available_signs:
    print(f"  • {sign}")
print("=" * 50)

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    
    try:
        print("🎤 Initializing microphone...")
        # Check if microphone is available
        try:
            microphone = sr.Microphone()
        except OSError as e:
            print(f"❌ Microphone not available: {e}")
            print("💡 Tip: Check if your microphone is connected and not being used by another application")
            return None
        
        print("🔊 Listening... (speak now)")
        with microphone as source:
            print("🔧 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

        print("🔍 Processing your speech...")
        text = recognizer.recognize_google(audio)
        print(f"✅ You said: '{text}'")
        return text
        
    except sr.UnknownValueError:
        print("❌ Could not understand the audio. Please speak clearly.")
        return None
    except sr.RequestError as e:
        print(f"❌ Internet connection error: {e}")
        print("💡 Make sure you have an active internet connection for speech recognition")
        return None
    except sr.WaitTimeoutError:
        print("❌ No speech detected. Please try speaking.")
        return None    except OSError as e:
        print(f"❌ Audio system error: {e}")
        print("💡 Try restarting the program or check your audio drivers")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💡 Please check your microphone settings and permissions")
        return None

def get_text_input():
    """Fallback function for manual text input when microphone fails"""
    print("\n🔤 Manual text input mode activated")
    print("Available phrases:", ", ".join(available_signs))
    text = input("👆 Type a phrase from the list above: ").strip()
    if text:
        print(f"✅ You typed: '{text}'")
        return text
    return None

def process_sign_language(text):
    # Dictionary mapping recognized text to video/GIF filenames
    sign_language_dict = {
        "hello": "hello.gif",
        "thank you": "Thank you.gif",
        "i like you": "I like you.gif",
        "happy": "happy.gif",
        "nice to meet you": "nice_to_meet_you.gif",
        "no": "no.gif"
        # Add more mappings here
    }
    
    # Convert text to lowercase for matching
    text_lower = text.lower().strip()
    
    # Check for exact phrase matches first
    found_match = False
    if text_lower in sign_language_dict:
        filename = sign_language_dict[text_lower]
        print(f"🎯 Found exact match for: '{text}'")
        if filename.endswith('.mp4'):
            play_video(filename)
        elif filename.endswith('.gif'):
            play_gif(filename)
        found_match = True
    else:
        # Split text into words and check each word individually
        words = text_lower.split()
        for word in words:
            if word in sign_language_dict:
                filename = sign_language_dict[word]
                print(f"🎯 Found match for word: '{word}'")
                if filename.endswith('.mp4'):
                    play_video(filename)
                elif filename.endswith('.gif'):
                    play_gif(filename)
                found_match = True
            else:
                print(f"❌ No sign language video/GIF found for '{word}'")
    
    if not found_match:
        print(f"❌ No sign language content found for: '{text}'")
        print(f"📝 Available phrases: {', '.join(available_signs)}")

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return
    
    print(f"Playing video {video_path}...")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Sign Language Video', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Video ended.")

def play_gif(gif_path):
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_gif_path = os.path.join(script_dir, gif_path)
    
    if not os.path.exists(full_gif_path):
        print(f"Error: GIF file {gif_path} not found!")
        return
    
    try:
        im = Image.open(full_gif_path)
        frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
        phrase_name = gif_path.replace('.gif', '').replace('_', ' ').title()
        print(f"🎬 Playing sign for: {phrase_name}")
        print("Press 'q' or 'ESC' to close the window")
        
        # Create a window for displaying the GIF with better settings
        window_name = 'Sign Language - ' + phrase_name
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 600, 400)
        
        # Loop the GIF 3 times for better understanding
        for loop in range(3):
            for frame in frames:
                # Convert PIL image to OpenCV format
                frame_rgb = frame.convert('RGB')
                opencv_image = cv2.cvtColor(np.array(frame_rgb), cv2.COLOR_RGB2BGR)
                
                # Resize frame for better visibility
                height, width = opencv_image.shape[:2]
                if width > 600:
                    scale = 600 / width
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    opencv_image = cv2.resize(opencv_image, (new_width, new_height))
                
                cv2.imshow(window_name, opencv_image)
                
                # Wait for key press or timeout
                key = cv2.waitKey(100) & 0xFF
                if key == ord('q') or key == 27:  # q or ESC key
                    cv2.destroyAllWindows()
                    print("✅ Sign display closed by user")
                    return
        
        # Keep the last frame displayed for a moment
        print("✅ Sign display completed! Closing in 2 seconds...")
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
        
    except Exception as e:
        print(f"❌ Error: Could not play GIF {gif_path}: {e}")
        cv2.destroyAllWindows()

def main():
    print("\n🎤 Starting Speech to Sign Language Translator...")
    print("Say one of the available phrases to see the sign language GIF!")
    print("Press Ctrl+C to exit anytime\n")
    
    # Test microphone availability
    microphone_available = True
    try:
        import speech_recognition as sr
        mic = sr.Microphone()
        print("✅ Microphone detected successfully!")
    except Exception as e:
        microphone_available = False
        print(f"⚠️  Microphone not available: {e}")
        print("🔤 Switching to manual text input mode...")
    
    consecutive_failures = 0
    
    while True:
        try:
            recognized_text = None
            
            if microphone_available and consecutive_failures < 3:
                print("🔊 Ready to listen... Say something!")
                recognized_text = recognize_speech_from_mic()
                
                if recognized_text is None:
                    consecutive_failures += 1
                    if consecutive_failures >= 3:
                        print("\n⚠️  Multiple microphone failures detected.")
                        choice = input("🔤 Switch to manual text input mode? (y/n): ").lower().strip()
                        if choice in ['y', 'yes']:
                            microphone_available = False
                            consecutive_failures = 0
                        else:
                            consecutive_failures = 0
                else:
                    consecutive_failures = 0
            
            # Use manual input if microphone is not available or failed
            if not microphone_available or (recognized_text is None and consecutive_failures < 3):
                if not microphone_available:
                    recognized_text = get_text_input()
            
            if recognized_text:
                process_sign_language(recognized_text)
                print("\n" + "="*50)
                
                # Ask if user wants to continue
                continue_choice = input("🔄 Want to try another phrase? (y/n): ").lower().strip()
                if continue_choice in ['n', 'no', 'exit', 'quit']:
                    print("👋 Thank you for using Speech to Sign Language Translator!")
                    break
                    
                # Ask if they want to switch input method
                if microphone_available:
                    switch_choice = input("🔄 Switch to manual text input? (y/n): ").lower().strip()
                    if switch_choice in ['y', 'yes']:
                        microphone_available = False
                elif consecutive_failures == 0:  # Only ask if microphone was working
                    switch_choice = input("🔄 Try microphone again? (y/n): ").lower().strip()
                    if switch_choice in ['y', 'yes']:
                        microphone_available = True
                        
            else:
                # If no input was received, ask if they want to try again
                retry_choice = input("🔄 Try again? (y/n): ").lower().strip()
                if retry_choice in ['n', 'no', 'exit', 'quit']:
                    print("👋 Thank you for using Speech to Sign Language Translator!")
                    break
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thank you for using Speech to Sign Language Translator!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            retry_choice = input("🔄 Try again? (y/n): ").lower().strip()
            if retry_choice in ['n', 'no', 'exit', 'quit']:
                print("👋 Thank you for using Speech to Sign Language Translator!")
                break

if __name__ == "__main__":
    main()
