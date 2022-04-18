import requests

api = "https://app.splatoon2.nintendo.net/api"


class Schedules():
    """时刻表查询函数"""

    def __init__(self, cookie: dict) -> None:
        self.cookie = cookie

    def battle(self) -> dict:
        """查询标准模式时刻表"""
        raw_response = requests.get(url=f"{api}/schedules",
                                    cookies=self.cookie)
        schedules_battle_data = raw_response.json()
        return schedules_battle_data

    def coop(self) -> dict:
        """查询打工模式时刻表"""
        raw_response = requests.get(url=f"{api}/coop_schedules",
                                    cookies=self.cookie)
        schedules_battle_data = raw_response.json()
        return schedules_battle_data
