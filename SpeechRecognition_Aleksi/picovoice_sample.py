"""
Picovoice Porcupineの仕様サンプル
"""

"""
kbB3YPolDdITb1fUGfty6dPhiHdUPrXjOyddzyQguWC2l2jK1RT0Pw==
"""
import os
import pvporcupine
import pyaudio
import shutil
import struct  # structモジュールをインポート


script_path = __file__  # スクリプト自身のファイルパス
script_directory = os.path.dirname(script_path)  # スクリプトのディレクトリパス

access_key = "kbB3YPolDdITb1fUGfty6dPhiHdUPrXjOyddzyQguWC2l2jK1RT0Pw=="  # 取得したAccessKeyを入力
keyword_paths = [script_directory+"/Drone-Test_en_windows_v3_0_0.ppn"]  # キーワードファイルのパスを指定

porcupine = pvporcupine.create(
    access_key=access_key,
    keyword_paths=keyword_paths
)

pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True
)

while True:
    pcm = audio_stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

    keyword_index = porcupine.process(pcm)

    if keyword_index >= 0:
        print("Keyword detected!")
        # キーワードが検出されたときの処理を記述
        #porcupine.delete()

porcupine.delete()