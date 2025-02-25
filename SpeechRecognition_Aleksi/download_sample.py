import requests
import os
import shutil

def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        script_path = __file__  # スクリプト自身のファイルパス
        script_directory = os.path.dirname(script_path)  # スクリプトのディレクトリパス
        filepath = script_directory+"/"+filename
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"{filename} をダウンロードしました。")
    else:
        print(f"{url} からのダウンロードに失敗しました。ステータスコード: {response.status_code}")

# 例
url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"  # ダウンロードしたいファイルのURL
filename = "file.zip"  # 保存するファイル名
download_file(url, filename)

script_path = __file__  # スクリプト自身のファイルパス
script_directory = os.path.dirname(script_path)  # スクリプトのディレクトリパス
shutil.unpack_archive(script_directory+'/file.zip', 'vosk')
os.remove(script_directory+'/file.zip')