# Test script to verify GIF functionality without microphone
import cv2
from PIL import Image, ImageSequence
import os
import numpy as np

available_signs = ["hello", "thank you", "i like you", "happy", "nice to meet you", "no"]

def play_gif(gif_path):
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_gif_path = os.path.join(script_dir, gif_path)
    
    if not os.path.exists(full_gif_path):
        print(f"Error: GIF file {gif_path} not found!")
        print(f"Looking for: {full_gif_path}")
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

# Test with hello
print("Testing GIF functionality...")
play_gif("hello.gif")
