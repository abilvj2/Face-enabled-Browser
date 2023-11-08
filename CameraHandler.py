import cv2


class CameraHandler:
    __instance = None

    @staticmethod
    def get_instance():
        if not CameraHandler.__instance:
            CameraHandler.__instance = CameraHandler()

        return CameraHandler.__instance

    def capture(self, file_name):
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            cv2.imshow("input", img)

            key = cv2.waitKey(10)
            if key == 27:
                cv2.imwrite(file_name, img)
                break

        cv2.destroyAllWindows()
        cv2.VideoCapture(0).release()
