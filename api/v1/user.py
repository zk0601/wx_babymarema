import datetime
from models.user import User
from tornado.concurrent import run_on_executor
from .base import BaseHandler
from utils import wx_api


class LoginHandler(BaseHandler):
    @run_on_executor
    def post(self):
        try:
            code = self.get_argument('code', None)
            nick_name = self.get_argument('nick_name', None)
            image = self.get_argument('image', None)
            gender = self.get_argument('gender', '')
            province = self.get_argument('province', '')
            city = self.get_argument('city', '')

            if not code:
                return self.response(code=10002, msg="缺失Code")
            if not nick_name or not image:
                return self.response(code=10002, msg='参数错误')

            json_data = wx_api.wx_get_session(code)
            errcode = json_data['errcode']

            if not errcode == 0:
                errMsg = json_data['errmsg']
                return self.response(code=10002, msg=errMsg)
            else:
                openid = json_data['openid']
                session_key = json_data['session_key']
                unionid = json_data['unionid']
                user = User(openid=openid, nick_name=nick_name, image_url=image, gender=gender,
                            province=province, city=city, create_time=datetime.datetime.now())
                self.session.add(user)
                self.session.flush()
                userid = user.user_id
                self.session.commit()

                token = self.encode(userid, openid)
                data = {'openid': openid, 'session_key': session_key, 'token':token}

                return self.response(data=data, code=10001, msg='success')

        except Exception as e:
            self.logger.error(str(e))
            self.session.rollback()
            return self.response(code=10000, msg='服务端异常')


class UserAuthHandler(BaseHandler):
    @run_on_executor
    def get(self):
        return self.response(code=10010, msg='非登录用户无权限')