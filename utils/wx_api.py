import requests
from tornado.options import options


def wx_get_session(code):
    req_params = {
        "appid": options.AppID,
        "secret": options.APPSecret,
        "js_code": code,
        "grant_type": 'authorization_code'
    }
    req_result = requests.get('https://api.weixin.qq.com/sns/jscode2session',
                              params=req_params, timeout=3, verify=False)
    return req_result.json()
