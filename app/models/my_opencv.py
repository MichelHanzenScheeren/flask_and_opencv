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


    @staticmethod
    def draw_rectangle(frame, initial_xy, final_xy):
        red_color = (0, 0, 255) # formato bgr (no lugar de rgb)
        cv2.rectangle(frame, initial_xy, final_xy, red_color, thickness = 1)


    @staticmethod
    def convert_to_bytes(image):
        return MyOpencv.encode_to_jpg(image).tobytes()


    @staticmethod
    def encode_to_jpg(image):
        return cv2.imencode(".jpg", image)[1]
