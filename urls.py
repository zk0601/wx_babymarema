from api.v1.user import LoginHandler
from api.v1.watermark import MakeWatermarkHandler


handlers = [
    (r'/v1/user/login', LoginHandler),
    (r'/v1/watermark/make', MakeWatermarkHandler)
]

Need_Token_URLs = {
    '/v1/watermark/make': 1
}