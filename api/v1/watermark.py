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

            watermark = MakeWatermark(birthday, weight, height)
            token = self.request.headers.get("Authentication", None)
            json_data = self.decode(token)
            openid = json_data["openid"]
            tmp_dir = os.path.join(self.basedir, 'temp_photos')
            tmp_photo = os.path.join(tmp_dir, "%s.jpg" % openid)
            with open(tmp_photo, 'wb') as infile:
                infile.write(photo)
            watermark.make(tmp_photo, tmp_photo)
            with open(tmp_photo, 'rb') as outfile:
                output_photo = base64.b64encode(outfile.read())
            baby = Baby(birthday=birthday, weight=weight, height=height, create_time=datetime.datetime.now())
            self.session.add(baby)
            self.session.commit()

            return self.response(data={'photo': output_photo}, code=10001, msg='success')

        except Exception as e:
            self.logger.error(str(e))
            self.session.rollback()
            return self.response(code=10000, msg='服务端异常')
