from .core_fuc import read_f


class Assets:
    def __init__(self):
        # CONFIG: KEY, WHITE_LIST #
        config = read_f("config.json")
        self.key = config["Key"]
        self.white_list = config["WhiteList"]
