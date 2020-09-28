import cv2.cv2 as cv2


class MyOpencv():

    @staticmethod
    def new_stream(port):
        return cv2.VideoCapture(port)
    

    @staticmethod
    def webcans_list(current_port):
        list_webcans = []
        index = 0
        while True:
            if index == current_port:
                list_webcans.append(index)
            else:
                video = MyOpencv.new_stream(index)
                if video is None or not video.isOpened():
                    break
                list_webcans.append(index)
            index += 1
        return list_webcans


