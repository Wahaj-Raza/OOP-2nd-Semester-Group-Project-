from abc import ABCMeta,abstractmethod
class User(metaclass=ABCMeta):
    def __init__(self,name='',password='',email_address=''):
        self.name = name
        self.password = password
        self.email_address = email_address
    @abstractmethod
    def log_in(self):
        pass



