# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')

import logging
import time

LOG_FORMAT = '\n'.join((
    '/' + '-' * 80,
    '[%(levelname)s][%(asctime)s][%(process)d:%(thread)d][%(filename)s:%(lineno)d %(funcName)s]:',
    '%(message)s',
    '-' * 80 + '/',
))

logger = logging.getLogger('maple')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


logger2 = logging.getLogger('maple_timer')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger2.addHandler(handler)
logger2.setLevel(logging.DEBUG)


from maple import Worker
from netkit.box import Box
from maple_timer import MapleTimer

app = Worker(Box)

timer = MapleTimer(app, dict(
    interval=15
))


@app.route(1)
def reg(request):
    time.sleep(0.1)
    request.write_to_client(dict(
        ret=0,
    ))


@app.route(2)
def login(request):
    # logger.error("login: %s", request.gw_box)
    uid = request.box.get_json()["uid"]
    request.login_client(uid)
    time.sleep(1)
    # request.logout_client()
    request.write_to_client(dict(
        ret=0,
        body="login %s" % uid
    ))


# app.run("192.168.1.67", 28000, workers=2, debug=True)
app.run("115.28.224.64", 28000, workers=1)
