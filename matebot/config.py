import staticconfig


class Config(staticconfig.Config):
    def __init__(self):
        super().__init__()
        self.application_id = ""
        self.uri = ""
        self.secret = ""
        self.verify = True
