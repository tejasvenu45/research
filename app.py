from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from gtts import gTTS
from one import process_image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        # Save the uploaded file to a temporary location
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        # Call your image processing function with the file path
        processed_text = process_image(file_path)
        # Render the result template with the processed text
        return render_template('result.html', text=processed_text)
    return "Processing failed."

@app.route('/speak', methods=['POST'])
def speak_text():
    text = request.form['text']
    audio_path = os.path.join('audio', 'speech.mp3')
    tts = gTTS(text=text, lang='en')
    tts.save(audio_path)
    return send_file(audio_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
