from abc import *

class DataCollector(metaclass=ABCMeta):
    @abstractmethod
    def load_data(self, keyword=None):
        pass
