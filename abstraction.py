
from abc import ABC, abstractmethod
class Teacher(ABC):
    def __init__(self,name,subject):
        self._name=name
        self.__subject=subject
        
    def display(self):
         print(f"this is {self._name} from {self.__subject}")
         
    @abstractmethod
    def teach():
        ...
    
    
class Parttime(Teacher):
    def display(self):
        ...
    def teach(self):
        ...
        
        

partime=Parttime("sugam","cloud")
partime.teach()

# print(f'''
# Name:{partime.name}
# Subject:{partime.subject}''')
    
