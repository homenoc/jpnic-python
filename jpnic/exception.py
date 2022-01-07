class InitException(Exception):
    def __init__(self, arg=""):
        self.arg = arg


class InvalidGetDataException(InitException):
    def __str__(self):
        return f"[{self.arg}]データの取得に失敗しました。"


class InvalidLoginException(InitException):
    def __str__(self):
        return f"ログインに失敗しました。原因は、[{self.arg}]"


class InvalidSearchMenuException(InitException):
    def __str__(self):
        return f"指定した操作({self.arg})は見つかりません。"
