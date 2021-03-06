'''
フィルタ処理実装部
'''
from django.conf import settings

from .models import Image
import cv2

class Filter_pro(): #実際のフィルタ処理実装部
    input_path = '' #入力画像へのパス
    output_path = '' #出力画像のパス

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def gray(self):
        #self.get_imgpath()
        img = cv2.imread(self.input_path)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(self.output_path, img_gray)
    
    def blur(self, filter_size):
        #self.get_imgpath()
        img = cv2.imread(self.input_path)
        img_gray = cv2.GaussianBlur(img, (filter_size, filter_size), 0)
        cv2.imwrite(self.output_path, img_gray)
