Python 3.13.2 (v3.13.2:4f8bb3947cf, Feb  4 2025, 11:51:10) [Clang 15.0.0 (clang-1500.3.9.4)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> from flask import Flask, request, jsonify
... import openai
... import whisper
... import os
... from flask_cors import CORS
... 
... app = Flask(__name__)
... CORS(app)  # Allow cross-origin requests
... 
... # Load Whisper model
... model = whisper.load_model("base")
... 
... # OpenAI API Key (for GPT)
... openai.api_key = "your_openai_api_key"
... 
... @app.route("/transcribe", methods=["POST"])
... def transcribe_audio():
...     if "audio" not in request.files:
...         return jsonify({"error": "No audio file provided"}), 400
... 
...     audio_file = request.files["audio"]
...     audio_path = "temp_audio.mp3"
...     audio_file.save(audio_path)
... 
...     # Transcribe audio
...     result = model.transcribe(audio_path)
...     os.remove(audio_path)  # Delete file after processing
...     return jsonify({"transcription": result["text"]})
... 
... @app.route("/ask", methods=["POST"])
... def ask_gpt():
...     data = request.get_json()
...     question = data.get("question")
... 
...     if not question:
...         return jsonify({"error": "No question provided"}), 400
... 
...     response = openai.ChatCompletion.create(
...         model="gpt-4",
...         messages=[{"role": "user", "content": question}]
...     )
... 
...     answer = response["choices"][0]["message"]["content"]
...     return jsonify({"answer": answer})
... 
... if __name__ == "__main__":
