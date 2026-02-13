import threading
import hashlib

from playwright.sync_api import sync_playwright
import requests

config = {"threads": [], "delay": 0.0}
auth_event = threading.Event()
session = requests.Session()


def md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def auth():
    if auth_event.is_set():
        auth_event.clear()
        with sync_playwright() as p:
            context = p.chromium.launch(headless=True).new_context()
            context.new_page().goto("https://910.ewvkqq.cn", wait_until="networkidle")
            for cookies in context.cookies():
                session.cookies.set(
                    **{
                        k: v
                        for k, v in cookies.items()
                        if k not in ["httpOnly", "sameSite"]
                    }
                )
        auth_event.set()
    else:
        auth_event.wait()
