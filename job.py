#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import time
from datetime import timedelta, timezone, datetime
from random import randint
from re import Pattern

from requests import session, Response, Session

from notifier import Notifier

shanghai_tz = timezone(timedelta(hours=8), name='Asia/Shanghai')


def get_current_hour() -> int:
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    return now.astimezone(shanghai_tz).hour


class Job:
    _login_header: dict = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'pass.neu.edu.cn',
        'Origin': 'https://pass.neu.edu.cn',
    }

    _init_url: str = 'https://e-report.neu.edu.cn/login'

    _service_url: str = 'https://e-report.neu.edu.cn/notes/create'

    _update_info_url: str = 'https://e-report.neu.edu.cn/api/notes'

    _feedback_url: str = "https://e-report.neu.edu.cn/notes"

    _lt_matcher: Pattern = re.compile(r'name="lt" value="(.+?)"')

    _login_path_matcher: Pattern = re.compile(r'id="loginForm" action="(.+?)"')

    _token_matcher: Pattern = re.compile(r'name="_token" value="(.+?)"')

    _name_matcher: Pattern = re.compile(r'当前用户：(.+?) <span')

    _class_matcher: Pattern = re.compile(r'"suoshubanji":"(.+?)"')

    _date_matcher: Pattern = re.compile(r'"created_on":"(.+?)"')

    _wrong_auth: str = '账号或密码错误'
    _bad_info: str = '信息获取失败'
    _bad_init_login: str = '获取登陆信息失败'

    def __init__(self, username: str, password: str, ip: str = ''):
        self._username: str = username
        self._password: str = password
        self._ip: str = ip
        self._client: Session = session()

        # 获取到的跨步骤共用中间信息
        self._token: str = ""
        self._name: str = ""
        self._lt = ""
        self._login_path: str = ""
        self._class: str = ""
        self._date: str = ""

    @property
    def _login_body(self) -> str:
        return f'rsa={self._username}{self._password}{self._lt}&ul={len(self._username)}&pl={len(self._password)}&lt={self._lt}&execution=e1s1&_eventId=submit'

    @property
    def _login_url(self) -> str:
        return f'https://pass.neu.edu.cn{self._login_path}'

    @property
    def _update_info_body(self) -> str:
        return f'_token={self._token}&jibenxinxi_shifoubenrenshangbao=1&profile%5Bxuegonghao%5D={self._username}&profile%5Bsuoshubanji%5D={self._class}&jiankangxinxi_muqianshentizhuangkuang=%E6%AD%A3%E5%B8%B8&xingchengxinxi_weizhishifouyoubianhua=0&qitashixiang_qitaxuyaoshuomingdeshixiang='

    @property
    def _update_info_header(self) -> dict:
        h = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'e-report.neu.edu.cn',
            'Origin': 'https://e-report.neu.edu.cn',
        }
        if len(self._ip) > 0:
            h['X-Forwarded-For'] = self._ip
        return h

    @property
    def _info_url(self) -> str:
        return f'https://e-report.neu.edu.cn/api/profiles/{self._username}?xingming={self._name}'

    @property
    def _body_temperature(self) -> float:
        return 36 + randint(4, 7) / 10

    @property
    def _report_body_temperature_url(self) -> str:
        hour = get_current_hour()
        item_id = 1 if 7 <= hour <= 9 else 2 if 12 <= hour <= 14 else 3
        return f'https://e-report.neu.edu.cn/inspection/items/{item_id}/records'

    @property
    def _report_body_temperature_body(self) -> str:
        return f'_token={self._token}&temperature={self._body_temperature}&suspicious_respiratory_symptoms=0&symptom_descriptions='

    @staticmethod
    def _is_login_success(resp: Response) -> bool:
        return resp.url.startswith("https://e-report.neu.edu.cn")

    # property 不好看
    def _is_reported(self) -> bool:
        return self._date == time.strftime(r'%Y-%m-%d', time.localtime())

    @staticmethod
    def _unexpected_exception(error: Exception = None) -> str:
        return f'网络错误或其他错误\n{error}'

    def _login(self) -> (bool, str):
        try:
            resp: Response = self._client.get(self._init_url)
            lt: list = self._lt_matcher.findall(resp.text)
            lp: list = self._login_path_matcher.findall(resp.text)
            if len(lt) < 1 or len(lp) < 1:
                return False, self._bad_init_login
            self._lt = lt[0]
            self._login_path = lp[0]

            resp: Response = self._client.post(self._login_url, data=self._login_body, headers=self._login_header)
            if self._is_login_success(resp):
                return True, ''
            return False, self._wrong_auth
        except Exception as e:
            return False, self._unexpected_exception(e)

    def _login_service(self) -> (bool, str):
        try:
            resp: Response = self._client.get(self._service_url)
            self._token = self._token_matcher.findall(resp.text)[0]
            self._name = self._name_matcher.findall(resp.text)[0]
            return True, ''
        except Exception as e:
            return False, self._unexpected_exception(e)

    def _get_info(self) -> (bool, str):
        try:
            resp: Response = self._client.get(self._info_url)

            if resp.text.find(self._username) == -1:
                return False, self._bad_info

            date = self._date_matcher.findall(resp.text)
            klass = self._class_matcher.findall(resp.text)

            if len(date) < 1 or len(klass) < 1:
                return False, self._bad_info

            self._date = date[0]
            self._class = klass[0]

            return True, ''
        except Exception as e:
            return False, self._unexpected_exception(e)

    def _update_info(self) -> (bool, str):
        try:
            resp: Response = self._client.post(self._update_info_url, data=self._update_info_body,
                                               headers=self._update_info_header)
            if resp.status_code == 201:
                return True, ""
            return False, resp.text
        except Exception as e:
            return False, self._unexpected_exception(e)

    def _report_body_temperature(self):
        try:
            resp: Response = self._client.post(self._report_body_temperature_url,
                                               data=self._report_body_temperature_body,
                                               headers=self._update_info_header)
            print(resp.status_code)
            if resp.status_code == 200:
                return True, ""
            return False, resp.text
        except Exception as e:
            return False, self._unexpected_exception(e)

    def do(self, notifier: Notifier):
        today = time.strftime('%m/%d/%Y')

        # 登陆
        success, msg = self._login()
        if not success:
            notifier.send(f"{today} 登陆失败", msg)
            return
        # 进入平台
        success, msg = self._login_service()
        if not success:
            notifier.send(f"{today} 鉴权失败", msg)
            return
        # 获取信息
        success, msg = self._get_info()
        if not success:
            notifier.send(f"{today} 获取已有信息失败", msg)
            return
        # 是否今日有签到过
        if not self._is_reported():
            # 打卡
            success, msg = self._update_info()
            if not success:
                notifier.send(f"{today} 打卡失败", msg)
                return
            notifier.send(f"{today} 打卡成功", "I'm fine, thank you.")

        # 上报体温
        success, msg = self._report_body_temperature()
        if not success:
            notifier.send(f"{today} 上报体温失败", msg)
            return
        notifier.send(f"{today} 上报体温成功", "I'm fine, really thank you.")
