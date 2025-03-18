import pyaudio
from vosk import Model, KaldiRecognizer
from difflib import SequenceMatcher
import json  # JSONを扱うために追加

# Voskモデルのパス (必要に応じて変更)
MODEL_PATH = "vosk/vosk-model-small-en-us-0.15"  # 軽量な英語モデルの例
# MODEL_PATH = "vosk-model-ja-0.22" # より高精度なモデル (サイズが大きい)

# Keyword
KEYWORD = "drone test"

# Similarity threshold
THRESHOLD = 0.4

try:
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 44100)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=8000)
    stream.start_stream()

    print("Keyword detection started...")

    while True:
        data = stream.read(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result_str = recognizer.Result()
            result = json.loads(result_str)

            if "text" in result:
                recognized_text = result["text"].strip().lower()
                print(f"Recognized text: {recognized_text}")

                matcher = SequenceMatcher(None, recognized_text, KEYWORD.lower())
                similarity = matcher.ratio()
                print(f"Similarity with keyword: {similarity}")

                if similarity >= THRESHOLD:
                    print("Keyword 'drone test' or something similar detected!")
                    # Add your action when the keyword is detected here
            elif "partial" in result:
                partial_text = result["partial"].strip().lower()
                print(f"Partial text: {partial_text}")
        else:
            pass # Not a complete utterance yet

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if 'stream' in locals() and stream.is_active():
        stream.stop_stream()
        stream.close()
    if 'p' in locals():
        p.terminate()