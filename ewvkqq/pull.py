from json import JSONDecodeError
from typing import Callable
import cv2
import re
import time

from .utils import *
import numpy
import ollama


class Event:
    # status: 999-全部, 0-待付款, 1-已支付, 3-已退款
    @staticmethod
    def order(
        contact: str, status: int = 999, current: int = 1, page_size: int = 999
    ) -> dict:
        assert len(contact) >= 6
        assert page_size >= 10
        data = session.post("https://910.ewvkqq.cn/shopApi/Common/captchaStart").json()[
            "data"
        ]
        code = re.sub(
            r"[^A-Za-z0-9]",
            "",
            ollama.generate(
                model="glm-ocr",
                prompt="Text Recognition: ",
                images=[
                    cv2.imencode(
                        ".png",
                        cv2.threshold(
                            cv2.imdecode(
                                numpy.frombuffer(
                                    session.get(data["img_url"]).content,
                                    numpy.uint8,
                                ),
                                cv2.IMREAD_GRAYSCALE,
                            ),
                            128,
                            255,
                            cv2.THRESH_BINARY,
                        )[1],
                    )[1].tobytes()
                ],
            )["response"],
        )
        ticket = session.post(
            data["check_url"],
            json={"code": code, "sign": md5(md5(code + data["ip"]) + "JING")},
        ).json()
        if ticket["code"]:
            return session.post(
                "https://910.ewvkqq.cn/shopApi/Order/list",
                json={
                    "status": status,
                    "current": current,
                    "pageSize": page_size,
                    "keywords": contact,
                    "ticket": ticket["data"]["ticket"],
                },
            ).json()
        else:
            raise requests.RequestException(ticket["msg"])

    @staticmethod
    def order_info(trade_no: str) -> dict:
        return session.post(
            "https://910.ewvkqq.cn/shopApi/Order/info", json={"trade_no": trade_no}
        ).json()

    @staticmethod
    def shop_info(token: str) -> dict:
        return session.post(
            "https://910.ewvkqq.cn/shopApi/Shop/info", json={"token": token}
        ).json()


def pull_event(event: Callable[..., dict], *args, **kwargs) -> dict:
    while True:
        try:
            return event(*args, **kwargs)
        except JSONDecodeError:
            auth()
        except requests.RequestException as e:
            print(e)
        finally:
            time.sleep(config["delay"])
