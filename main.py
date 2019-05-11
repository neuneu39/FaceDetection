from flask import Flask, render_template, Response, request

from camera import VideoCamera
from detection import Detection

app = Flask(__name__)

@app.route('/')
def index():
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

# @app.route("/<button_ans>", methods=["GET", "POST"])
# @app.route("/face_detect")
# def detedct_face():
#     return render_template('face_detect.html')

def move_forward():
    #Moving forward code
    print("Moving Forward...")

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

@app.route("/<name>", methods=["GET", "POST"])
def namepage(name):
    return render_template("name.html", name=name)


@app.route("/odd_even", methods=["GET", "POST"])
def odd_even():
    if request.method == "GET":
        return """
        下に整数を入力してください。奇数か偶数か判定します
        <form action="/odd_even" method="POST">
        <input name="num"></input>
        </form>"""
    else:
        return """
        {}は{}です！
        <form action="/odd_even" method="POST">
        <input name="num"></input>
        </form>""".format(str(request.form["num"]), ["偶数", "奇数"][int(request.form["num"]) % 2])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# 0.0.0.0はすべてのアクセスを受け付けます。
# webブラウザーには、「localhost:5000」と入力
