import json

from ewvkqq import *

account = {}
order = [
    v
    for v in pull.pull_event(pull.Event.order, "000000", 1)["data"]["list"]
    if "忙盒" in v["goods_name"]
]
order_len = len(order)

print("All data has been read into the buffer.")

for i, v in enumerate(order):
    print(f"\rwriting: {i + 1}/{order_len}", end="")
    order_info = pull.pull_event(pull.Event.order_info, v["trade_no"])
    if not order_info["code"]:
        continue
    order_info = order_info["data"]
    if order_info["trade_no"] not in account:
        account[order_info["trade_no"]] = order_info["response"]["cards"]

with open("account.json", "w+", encoding="utf-8") as f:
    json.dump(account, f, ensure_ascii=False, indent=4)
