import requests

api = "https://app.splatoon2.nintendo.net/api/onlineshop"


class Merchandises():
    """线上商店操作"""

    def __init__(self, cookie: dict) -> None:
        self.cookie = cookie

    def get_list(self) -> dict:
        """查询线上商店正在出售的物品"""
        raw_response = requests.get(url=f"{api}/merchandises",
                                    cookies=self.cookie)
        data = raw_response.json()
        return data

    def order(self, item_id: str, unique_id: str) -> dict:
        """购买线上商店正在出售的物品"""
        headers = {
            "X-Requested-With":
            "XMLHttpRequest",
            "X-Unique-Id":
            unique_id,
            'Content-Type':
            "multipart/form-data;boundary=----WebKitFormBoundaryRubAzu8lBx1RHBLz",
        }
        body = ("------WebKitFormBoundaryRubAzu8lBx1RHBLz"
                "Content-Disposition: form-data; name='override'"
                "0"
                "------WebKitFormBoundaryRubAzu8lBx1RHBLz--")

        raw_response = requests.post(url=f"{api}/order/{item_id}",
                                     cookies=self.cookie,
                                     body=body,
                                     headers=headers)
        data = raw_response.json()
        return data
