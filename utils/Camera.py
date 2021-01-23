import cv2 

class Camera():
    def __init__(self):
        self.__camera = cv2.VideoCapture(0)



    def capture(self):
        ret, frame = self.__camera.read()

        if not ret:
            print("Echec de capture")
            return None

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imwrite("images/photo.jpg",image)

        return image
        

    def openCamera(self):
        self.__camera = cv2.VideoCapture(0)

    def closeCamera(self):
        self.__camera.release()
