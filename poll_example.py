import json

from ewvkqq import *

executed = set()


@poll.poll_event(poll.Event.order, "000000", 1)
def poll_event(order: dict):
    if order["code"] != 1:
        return
    data = order["data"]["list"]
    if len(data) != 0 and (trade_no := data[0]["trade_no"]) not in executed:
        executed.add(trade_no)
        print(
            json.dumps(
                pull.pull_event(pull.Event.order_info, trade_no),
                ensure_ascii=False,
                indent=4,
            )
        )


run_main()
