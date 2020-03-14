#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

from requests import session, Response, Session

from notifier import Notifier

import time


class Job:
    _login_header: dict = {"Authorization": "Basic dnVlOnZ1ZQ=="}

    _login_service_url: str = "http://stuinfo.neu.edu.cn/cloud-xxbl/studenLogin"

    _visit_service_url: str = "http://stuinfo.neu.edu.cn/cloud-xxbl/studentinfo?tag={}"

    _get_info_url: str = "http://stuinfo.neu.edu.cn/cloud-xxbl/getStudentInfo"

    _update_info_url: str = "http://stuinfo.neu.edu.cn/cloud-xxbl/updateStudentInfo"

    _full_request_data: dict = {
        "xm": "",
        "xh": "",
        "xy": "",
        "njjzy": "",
        "bj": "",
        "xq": "",
        "ss": "",
        "qy": "",
        "fjh": "",
        "brsjhm": "",
        "sylx": "",
        "jtxxdz_sf": "",
        "jtxxdz_cs": "",
        "jtxxdz_qx": "",
        "jtxxdz": "",
        "mqxxdz_sf": "",
        "mqxxdz_cs": "",
        "mqxxdz_qx": "",
        "mqxxdz": "",
        "mqjzdzsm": "居家学习",
        "jzsjhm": "",

        "mqzk": "A",
        "zjtw": "",
        "zzkssj": "",
        "sfjy": "",
        "sfyqjc": "",
        "mqsfzj": "",
        "jtms": "",
        "glyyms": "",
        "gldxxdz_sf": "",
        "gldxxdz": "",
        "mqstzk": "",
        "sfgcyiqz": "否",
        "cjlqk": "曾经医学观察，后隔离解除",
        "dsjtqkms": "",
        "hjnznl": "家",
        "qgnl": "无",
        "sfqtdqlxs": "否",
        "sfqtdqlxsmsxj": "",
        "sfjcgbr": "否",
        "sfjcgbrmsxj": "",
        "sfjcglxsry": "否",
        "sfjcglxsrymsxj": "",
        "sfjcgysqzbr": "否",
        "sfjcgysqzbrmsxj": "",
        "sfjtcyjjfbqk": "否",
        "sfjtcyjjfbqkmsxj": "",
        "sfqgfrmz": "否",
        "yljgmc": "",
        "zzzd": "",
        "sfygfr": "无",
        "zgtw": "",
        "zgtwcxsj": "",
        "sfyghxdbsy": "无",
        "sfyghxdbsycxsj": "",
        "sfygxhdbsy": "无",
        "sfygxhdbsycxsj": "",
        "sfbrtb": "是",
        "fdysfty": "否",
        "tbrxm": "",
        "tbrxh": "",
        "tbrxy": "",
        "dtyy": "",
        "id": ""
    }
    _unexpected_exception: str = "网络错误或其他错误"

    def __init__(self, username: str, password: str):
        self._username: str = username
        self._password: str = password
        self._token: str = ""
        self._info: dict = {}
        self._tag: str = ""
        self._client: Session = session()

    @property
    def _login_url(self) -> str:
        return f'http://stuinfo.neu.edu.cn/api/auth/oauth/token?username={self._username}&grant_type=password&password={self._password}&imageCodeResult=&imageKey= '

    @property
    def _login_service_header(self) -> dict:
        return {"Authorization": f"Bearer {self._token}"}

    @property
    def _request_data(self) -> dict:
        return {**self._full_request_data, **{k: v for k, v in self._info.items() if k in self._full_request_data}}

    def _login(self) -> (bool, str):
        resp: Response = self._client.post(self._login_url, headers=self._login_header)
        try:
            result: dict = json.loads(resp.text)
            if "access_token" in result:
                self._token = result['access_token']
                return True, ""
            return False, resp.text
        except Exception:
            return False, self._unexpected_exception

    def _login_service(self) -> (bool, str):
        resp: Response = self._client.post(self._login_service_url, headers=self._login_service_header)
        try:
            result: dict = json.loads(resp.text)
            if "success" in result and result["success"]:
                self._client.get(self._visit_service_url.format(result["data"]))
                return True, ""
            return False, resp.text
        except Exception:
            return False, self._unexpected_exception

    def _get_info(self) -> (bool, str):
        resp: Response = self._client.get(self._get_info_url)
        try:
            result: dict = json.loads(resp.text)
            if "success" in result and result["success"]:
                self._info = result["data"]
                return True, ""
            return False, resp.text
        except Exception:
            return False, self._unexpected_exception

    def _update_info(self) -> (bool, str):
        resp: Response = self._client.post(self._update_info_url, json=self._request_data)
        try:
            result: dict = json.loads(resp.text)
            if "success" in result and result["success"]:
                return True, ""
            return False, resp.text
        except Exception:
            return False, self._unexpected_exception

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
        # 打卡
        success, msg = self._update_info()
        if not success:
            notifier.send(f"{today} 打卡失败", msg)
            return
        notifier.send(f"{today} 打卡成功", "I'm fine, thank you.")
