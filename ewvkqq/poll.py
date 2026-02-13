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
    def order(callback: Callable[[dict], None], contact: str, status: int = 999):
        assert len(contact) >= 6
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
            callback(
                session.post(
                    "https://910.ewvkqq.cn/shopApi/Order/list",
                    json={
                        "status": status,
                        "keywords": contact,
                        "ticket": ticket["data"]["ticket"],
                    },
                ).json()
            )
        else:
            callback(ticket)


def main(event: Callable[..., None], callback: Callable[[dict], None], *args, **kwargs):
    while True:
        try:
            event(callback, *args, **kwargs)
        except JSONDecodeError:
            callback(
                {
                    "code": -1,
                    "msg": "CAPTCHA detected",
                    "time": time.time(),
                    "data": None,
                }
            )
            auth()
        except requests.RequestException as e:
            print(e)
        finally:
            time.sleep(config["delay"])


def poll_event(event: Callable[..., None], *args, **kwargs):
    def decorator(callback: Callable[[dict], None]):
        config["threads"].append(
            threading.Thread(
                target=main,
                args=(event, callback, *args),
                kwargs=kwargs,
                daemon=True,
            )
        )
        return callback

    return decorator
