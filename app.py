from flask import Flask, request, jsonify
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import pyttsx3
import os
from datetime import datetime

app = Flask(__name__)
os.makedirs("output", exist_ok=True)

@app.route("/api/video", methods=["POST"])
def generate_video():
    data = request.get_json()
    title = data.get("title", "Titre par défaut")
    excerpt = data.get("excerpt", "Aucun extrait fourni.")

    # Créer une image avec texte
    img = Image.new("RGB", (1280, 720), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    font_excerpt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    draw.text((50, 100), title, font=font_title, fill="white")
    draw.text((50, 200), excerpt, font=font_excerpt, fill="lightgray")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_path = f"output/image_{timestamp}.jpg"
    img.save(image_path)

    # Générer voix
    audio_path = f"output/audio_{timestamp}.mp3"
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.save_to_file(f"{title}. {excerpt}", audio_path)
    engine.runAndWait()

    # Créer la vidéo
    image_clip = ImageClip(image_path).set_duration(10)
    audio_clip = AudioFileClip(audio_path)
    video = image_clip.set_audio(audio_clip)
    video_path = f"output/video_{timestamp}.mp4"
    video.write_videofile(video_path, fps=24)

    return jsonify({"success": True, "video": video_path})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)