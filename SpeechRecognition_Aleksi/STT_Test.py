from vosk import Model, KaldiRecognizer
import pyaudio
import json

model = Model("Python_Packages/VoskModelSmall_en-us_0.15")
recognizer = KaldiRecognizer(model, 16000)
isRunning = True

mic = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, 
                             input=True, frames_per_buffer=4096)
mic.start_stream()

print("Listening... (Speak!)")

while isRunning:
    data = mic.read(4096)
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        print("You said:", result["text"])
        if result["text"] == "":
            result["text"] = "[no_speech]"
        elif result["text"] == "exit":
            isRunning = False
            exit()