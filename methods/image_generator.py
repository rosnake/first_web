#!/usr/bin/env python
#coding:utf-8
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


class VerifyImage:
    def __init__(self, width=240, height=60):
        self.width = width
        self.height = height
        self.image = None
        self.image_string = ""
        self.__create_image()

    def get_image(self):
        return self.image

    def get_code(self):
        return self.image_string

    # 随机字母:
    def __rndChar(self):
        return chr(random.randint(65, 90))

    # 随机颜色1:
    def __rndColor(self):
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 随机颜色2:
    def __rndColor2(self):
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    def __create_image(self):
        image = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        # 创建Font对象:
        font = ImageFont.truetype('arial.ttf', 36)
        # 创建Draw对象:
        draw = ImageDraw.Draw(image)
        # 填充每个像素:
        for x in range(self.width):
            for y in range(self.height):
                draw.point((x, y), fill=self.__rndColor())
        # 输出文字:
        for t in range(4):
            char = self.__rndChar()
            self.image_string = self.image_string+str(char)
            draw.text((self.height * t + 10, 10), char, font=font, fill=self.__rndColor2())
        # 模糊:
        self.image = image.filter(ImageFilter.BLUR)
        print(self.image_string)

