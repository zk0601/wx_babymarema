from tornado.options import define

#port
define("port", default=8901, help="run on the given port", type=int)

#mysql test
define("mysql_host", default="47.91.252.155:3306", help="database host")
define("mysql_database", default="wx_camera", help="database name")
define("mysql_user", default="root", help="database user")
define("mysql_password", default="123456", help="database password")

define("pool_size", default=20, help="pool size")
define("pool_recycle", default=3600, help="pool recycle")

#tornado execute threads num
define("max_workers", default=25, type=int, help="max threads")

#token
define("secret", default='Camera~348#fgEHz24$9deHPfL', help="token secret")

#wechat config
define("AppID", default='wxecd4405453198abb', help='wechat mini program id')
define('APPSecret', default='66fa8490754d313b29cb9d1b72fbbd57', help='wechat secret')

