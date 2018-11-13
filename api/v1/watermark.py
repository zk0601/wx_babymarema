import base64
import os
import datetime
from tornado.concurrent import run_on_executor
from .base import BaseHandler
from utils.make_watermark import MakeWatermark
from models.baby import Baby


class MakeWatermarkHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            photo = self.get_argument('photo', None)
            birthday = self.get_argument("birthday", None)
            if not photo or not birthday:
                return self.response(code=10002, msg="参数错误")

            weight = self.get_argument('weight', None)
            height = self.get_argument('height', None)

            # ttf_font = self.get_argument('ttf_font', None)
            # color_font = self.get_argument('color_font', None)
            # transparency = self.get_argument('transparency', None)
            # if not ttf_font or not color_font or not transparency:
            #     return self.response(code=10002, msg='参数错误')

            if weight:
                weight = float(weight)
            if height:
                height = float(height)
            photo_dir = os.path.join(self.basedir, "photo_directory")
            watermark = MakeWatermark(birthday, weight, height)
            token = self.get_argument("token", None)
            json_data = self.decode(token)
            openid = json_data["openid"]
            outphoto_filename = "%s.jpg" % openid
            outphoto = os.path.join(photo_dir, outphoto_filename)
            if os.path.exists(outphoto):
                os.remove(outphoto)
            with open(outphoto, 'wb') as infile:
                infile.write(base64.b64decode(photo.encode()))
            watermark.make(outphoto, outphoto, str(openid))
            if not weight:
                weight = float(0)
            if not height:
                height = float(0)

            baby = Baby(birthday=birthday, weight=weight, height=height, create_time=datetime.datetime.now())
            self.session.add(baby)
            self.session.commit()

            return self.response(data={'photo': outphoto_filename}, code=10001, msg='success')

        except Exception as e:
            self.logger.error(str(e))
            self.session.rollback()
            return self.response(code=10000, msg='服务端异常')
