import cv2
import os
import shutil
import subprocess

class Ascinator:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    @staticmethod
    def convert_row_to_ascii(row):
        # 17-long
        ORDER = (' ', '.', "'", ',', ':', ';', 'c', 'l',
                 'x', 'o', 'k', 'X', 'd', 'O', '0', 'K', 'N')
        return tuple(ORDER[int(x / (255 / 16))] for x in row)[::-1]

    def convert_to_ascii(self, input_grays):
        return tuple(self.convert_row_to_ascii(row) for row in input_grays)

    @staticmethod
    def print_array(input_ascii_array):
        os.system("cls" if os.name == "nt" else "clear")
        print('\n'.join((''.join(row) for row in input_ascii_array)), end='')

    @staticmethod
    def rescale_frame(frame, percent=75):
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    def get_terminal_size(self):
        if os.name == 'nt':
            columns, lines = shutil.get_terminal_size()
        else:
            out = subprocess.check_output(['stty', 'size'])
            lines, columns = map(int, out.split())
        return columns, lines

    def main(self):
        while self.cap.isOpened():
            screen_width, screen_height = self.get_terminal_size()
            ret, image = self.cap.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            reduced = cv2.resize(gray, (screen_width, screen_height))

            converted = self.convert_to_ascii(reduced)
            self.print_array(converted)

            cv2.imshow('frame', self.rescale_frame(cv2.flip(image, 1), percent=50))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    Ascinator().main()
