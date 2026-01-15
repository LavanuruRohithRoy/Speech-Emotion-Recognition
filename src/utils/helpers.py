"""
Utility functions for SER application
Handles confidence visualization, emotion representation, and other helper functions
"""

def get_confidence_color(confidence):
    """Get color based on confidence level for visualization"""
    if confidence >= 80:
        return "#4CAF50"  # Green for high confidence
    elif confidence >= 60:
        return "#FF9800"  # Orange for medium confidence
    else:
        return "#F44336"  # Red for low confidence

def get_emotion_emoji(emotion):
    """Get emoji representation for emotions"""
    emotion_emojis = {
        "neutral": "😐",
        "calm": "😌", 
        "happy": "😊",
        "sad": "😢",
        "angry": "😠",
        "fearful": "😨",
        "disgust": "🤢",
        "surprised": "😲",
        "uncertain": "❓"
    }
    return emotion_emojis.get(emotion.lower(), "❓")

def get_emotion_description(emotion):
    """Get human-readable description of emotions"""
    descriptions = {
        "neutral": "Neutral - Balanced and calm speech",
        "calm": "Calm - Peaceful and relaxed tone",
        "happy": "Happy - Joyful and positive expression",
        "sad": "Sad - Melancholic or sorrowful tone",
        "angry": "Angry - Frustrated or irritated speech",
        "fearful": "Fearful - Anxious or scared expression",
        "disgust": "Disgust - Repulsed or averse tone",
        "surprised": "Surprised - Astonished or shocked expression",
        "uncertain": "Uncertain - Emotion unclear, try again"
    }
    return descriptions.get(emotion.lower(), "Unknown emotion")

def format_confidence_message(confidence):
    """Get appropriate message based on confidence level"""
    if confidence >= 80:
        return "High confidence - Very reliable prediction"
    elif confidence >= 60:
        return "Medium confidence - Moderately reliable"
    elif confidence >= 30:
        return "Low confidence - Consider retrying with clearer audio"
    else:
        return "Very low confidence - Audio may be unclear or too short"

def validate_audio_file(file_path):
    """Basic validation of audio file"""
    import os
    
    if not os.path.exists(file_path):
        return False, "File does not exist"
    
    # Check file size (minimum 1KB)
    if os.path.getsize(file_path) < 1024:
        return False, "File too small (minimum 1KB required)"
    
    # Check file extension
    valid_extensions = ['.wav', '.mp3', '.m4a', '.flac', '.ogg']
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext not in valid_extensions:
        return False, f"Unsupported file format: {file_ext}"
    
    return True, "File is valid"
