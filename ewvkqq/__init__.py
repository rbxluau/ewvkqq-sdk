from . import poll
from . import pull
from . import utils


def run_main(delay: float = 0):
    utils.config["delay"] = delay
    for v in utils.config["threads"]:
        v.start()
    for v in utils.config["threads"]:
        v.join()
