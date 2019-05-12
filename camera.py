import cv2
from detection import Detection

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

        # Opencvのカメラをセットします。(0)はノートパソコンならば組み込まれているカメラ

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, image = self.video.read()
        converted_frame = Detection(image)
        facedetected_frame = converted_frame.face_detection()
        _, jpeg = cv2.imencode('.jpg', facedetected_frame)
        return jpeg.tobytes()

        # read()は、二つの値を返すので、success, imageの2つ変数で受けています。
        # OpencVはデフォルトでは raw imagesなので JPEGに変換
        # ファイルに保存する場合はimwriteを使用、メモリ上に格納したい時はimencodeを使用
        # cv2.imencode() は numpy.ndarray() を返すので .tobytes() で bytes 型に変換

    def get_motion_detection(self, frame):
        _, image = self.video.read()
        converted_frame = Detection(image)
        frame, facedetected_frame = converted_frame.motion_detection(frame)
        _, jpeg = cv2.imencode('.jpg', facedetected_frame)
        return frame, jpeg.tobytes()
