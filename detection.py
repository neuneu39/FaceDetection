import cv2

FIRST_FLAME = None
class Detection(object):
    def __init__(self, frame):
        self.frame = frame
        self.face_cascade = cv2.CascadeClassifier("./utility/haarcascade_frontalface_default.xml")
        # Opencvのカメラをセットします。(0)はノートパソコンならば組み込まれているカメラ

    def face_detection(self):
        faces = self.face_cascade.detectMultiScale(self.frame,
                                        scaleFactor=1.1,
                                        minNeighbors=5)

        for x, y, w, h in faces:
            cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        return self.frame

    def motion_detection(self, first_frame):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if first_frame is None:
            first_frame = gray
            return first_frame, self.frame

        delta_frame = cv2.absdiff(first_frame, gray)
        threshold_frame = cv2.threshold(delta_frame, 30,255, cv2.THRESH_BINARY)[1]
        thresh_frame_dilate = cv2.dilate(threshold_frame, None, iterations=2)
        # 輪郭を見つけて描写する
        (cnts, _) = cv2.findContours(thresh_frame_dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in cnts:
            if cv2.contourArea(contour) < 10000:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        # return self.frame
        # return first_frame, thresh_frame_dilate.copy()
        return first_frame, self.frame

