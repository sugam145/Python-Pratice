

class Teacher():
    def __init__(self,name,subject):
        self._name=name
        self.__subject=subject
        
    def display(self):
         print(f"this is {self._name} from {self.__subject}")
    
# class Parttime(Teacher):
#     def display(self):
#         print(f"this is {self._name} from {self.__subject}")
        

partime=Teacher("sugam","cloud")
partime.display()
print(f'''
Name:{partime.name}
Subject:{partime.subject}''')
    
