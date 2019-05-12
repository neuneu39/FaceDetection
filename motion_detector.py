import os
from flask import Flask, render_template, Response, request

from camera import VideoCamera
from detection import Detection

app = Flask(__name__)

@app.route('/', methods=["POST"])
def index():
    if request.method == "POST":
        return render_template('index.html', video_detect = request.form["video_value"])
    else:
        return render_template('index.html')

    # "/" を呼び出したときには、indexが表示される。

def gen(camera):
    while True:
        frame = camera.get_frame()
        # converted_frame = Detection(frame)
        # facedetected_frame = converted_frame.face_detection()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# returnではなくジェネレーターのyieldで逐次出力。
# Generatorとして働くためにgenとの関数名にしている
# Content-Type（送り返すファイルの種類として）multipart/x-mixed-replace を利用。
# HTTP応答によりサーバーが任意のタイミングで複数の文書を返し、紙芝居的にレンダリングを切り替えさせるもの。

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/face_detect')
def face_detect():
    return Response(generate(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def generate(camera):
    first_frame = None
    while True:
        first_frame, frame = camera.get_motion_detection(first_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# 0.0.0.0はすべてのアクセスを受け付けます。
# webブラウザーには、「localhost:5000」と入力
