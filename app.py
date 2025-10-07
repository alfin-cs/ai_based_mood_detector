import cv2
from deepface import DeepFace
import os

# Global variables
UPLOADS_FOLDER = "uploads"
EMOTION_EMOJIS = {
    'happy': '😊',
    'sad': '😢',
    'angry': '😠',
    'fear': '😨',
    'surprise': '😲',
    'neutral': '😐',
    'disgust': '🤢'
}

def create_uploads_folder():
    """Create uploads folder if it doesn't exist"""
    if not os.path.exists(UPLOADS_FOLDER):
        os.makedirs(UPLOADS_FOLDER)
        print(f"✅ Created '{UPLOADS_FOLDER}' folder")

def list_images_in_uploads():
    """List all images in the uploads folder"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    images = [f for f in os.listdir(UPLOADS_FOLDER) 
             if os.path.splitext(f)[1].lower() in image_extensions]
    return images

def detect_mood_from_image(image_path):
    """Detect mood from an image file"""
    try:
        # Check if it's just a filename (look in uploads folder)
        if not os.path.isabs(image_path) and not os.path.exists(image_path):
            image_path = os.path.join(UPLOADS_FOLDER, image_path)
        
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"Error: File '{image_path}' not found.")
            print(f"Make sure the image is in the '{UPLOADS_FOLDER}' folder.")
            return None
        
        # Read the image
        img = cv2.imread(image_path)
        
        if img is None:
            print("Error: Could not read image. Make sure it's a valid image file.")
            return None
        
        print("🔍 Analyzing image...")
        
        # Analyze the image using DeepFace
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        
        # Handle both single face and multiple faces
        if isinstance(result, list):
            result = result[0]
        
        return result
        
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return None

def display_results(result):
    """Display the mood detection results"""
    if result is None:
        return
    
    emotions = result['emotion']
    dominant_emotion = result['dominant_emotion']
    
    # Get emoji
    emoji = EMOTION_EMOJIS.get(dominant_emotion, '😐')
    
    print("\n" + "=" * 50)
    print(f"  MOOD DETECTION RESULTS {emoji}")
    print("=" * 50)
    print(f"\n🎯 Dominant Emotion: {dominant_emotion.upper()} {emoji}")
    print(f"\n📊 All Emotion Scores:")
    print("-" * 50)
    
    # Sort emotions by score
    sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
    
    for emotion, score in sorted_emotions:
        bar = '█' * int(score / 5)
        emoji_icon = EMOTION_EMOJIS.get(emotion, '•')
        print(f"{emoji_icon} {emotion.capitalize():12} {score:5.2f}% {bar}")
    
    print("=" * 50 + "\n")

def detect_and_display(image_path):
    """Detect mood and display results"""
    result = detect_mood_from_image(image_path)
    display_results(result)
    return result

def show_available_images():
    """Show all images in uploads folder"""
    images = list_images_in_uploads()
    if images:
        print(f"\n📷 Images in '{UPLOADS_FOLDER}' folder:")
        for img in images:
            print(f"   - {img}")
        print()
    else:
        print(f"\n⚠️  No images found in '{UPLOADS_FOLDER}' folder.\n")

def main():
    """Main program"""
    create_uploads_folder()
    
    print("=" * 50)
    print("     AI IMAGE MOOD DETECTOR")
    print("=" * 50)
    print(f"\n📁 Upload folder: '{UPLOADS_FOLDER}'")
    print("\nHow to use:")
    print(f"1. Place your images in the '{UPLOADS_FOLDER}' folder")
    print("2. Just type the filename (e.g., 'photo.jpg')")
    print("3. Or type 'list' to see all images in uploads folder")
    print("4. Type 'quit' to exit\n")
    
    # Show available images at startup
    images = list_images_in_uploads()
    if images:
        print(f"📷 Found {len(images)} image(s) in uploads folder:")
        for img in images:
            print(f"   - {img}")
        print()
    else:
        print(f"⚠️  No images found in '{UPLOADS_FOLDER}' folder yet.\n")
    
    # Main loop
    while True:
        image_path = input("Enter image filename: ").strip()
        
        if image_path.lower() in ['quit', 'exit', 'q']:
            print("\nThank you for using Mood Detector! Goodbye! 👋")
            break
        
        if image_path.lower() == 'list':
            show_available_images()
            continue
        
        if not image_path:
            print("Please enter a valid image filename.\n")
            continue
        
        detect_and_display(image_path)

if __name__ == "__main__":
    main()