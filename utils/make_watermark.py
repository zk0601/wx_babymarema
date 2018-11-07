from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os
import datetime
import shutil

Current_Path = os.path.dirname(__file__)


class MakeWatermark(object):
    def __init__(self, birthday=None, weight=None, height=None, color_font="#F5F5F5", transparency=0.63, ttf='2.ttf'):
        self.birthday = birthday
        self.weight = weight
        self.height = height
        self.color_font = color_font
        self.transparency = transparency
        self.ttf_font = os.path.join(Current_Path, ttf)

    def total_days(self):
        date_fromat = "%Y-%m-%d"
        today = datetime.datetime.now()
        birthday = datetime.datetime.strptime(self.birthday, date_fromat)
        delta = today - birthday
        return delta.days

    def txt_draw(self, text, size, x_position, y_position, input_picture, output_picture):
        img = Image.open(input_picture)
        watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
        n_font = ImageFont.truetype(self.ttf_font, size)
        draw = ImageDraw.Draw(watermark, 'RGBA')
        draw.text((x_position, y_position), text, font=n_font, fill=self.color_font)
        watermark = watermark.rotate(0)
        alpha = watermark.split()[1]
        alpha = ImageEnhance.Brightness(alpha).enhance(self.transparency)
        watermark.putalpha(alpha)
        Image.composite(watermark, img, watermark).save(output_picture, 'JPEG')

    def get_str_len(self, string):
        count = 0
        for char in string:
            if char in "0123456789.":
                count += 1
            else:
                count += 3
        return count / 3

    def make(self, input, output):
        Month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        img = Image.open(input)
        temp_file = os.path.join(Current_Path, "temp.jpg")
        img_width = img.size[0]
        img_height = img.size[1]
        size = int(img_width / 20)
        date_str = "%s.%s" % (Month[datetime.datetime.now().month-1], datetime.datetime.now().day)
        self.txt_draw(date_str, size, size, img_height - size * 3 - int(img_height / 20), input, temp_file)
        if self.birthday and self.height and self.weight:
            text = "宝宝的第%s天" % self.total_days()
            self.txt_draw(text, size, size, img_height-size*2-int(img_height / 20), temp_file, temp_file)
            text = "%skg,  %scm" % (self.weight, self.height)
            self.txt_draw(text, size, size, img_height-size-int(img_height / 20), temp_file, output)
        elif self.birthday and ( not self.height and not self.weight):
            text = "宝宝的第%s天" % self.total_days()
            self.txt_draw(text, size, size, img_height-size-int(img_height / 20), temp_file, output)
        elif self.birthday and self.weight:
            text = "宝宝的第%s天" % self.total_days()
            self.txt_draw(text, size, size, img_height-size*2-int(img_height / 20), temp_file, temp_file)
            text = "%skg" % self.weight
            self.txt_draw(text, size, size, img_height-size-int(img_height / 20), temp_file, output)
        elif self.birthday and self.height:
            text = "宝宝的第%s天" % self.total_days()
            self.txt_draw(text, size, size, img_height-size*2-int(img_height / 20), temp_file, temp_file)
            text = "%scm" % self.height
            self.txt_draw(text, size, size, img_height-size-int(img_height / 20), temp_file, output)
        else:
            shutil.copy(input, output)
