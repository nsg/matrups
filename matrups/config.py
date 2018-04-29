import yaml

class Config:

    def __init__(self, config_file):
        self.config = yaml.load(open(config_file))

    def matrix(self, k):
        return self.config['matrix'][k]

    def hangouts(self, k):
        return self.config['hangouts'][k]

    def bridge(self, k):
        return self.config['bridge'][k]
