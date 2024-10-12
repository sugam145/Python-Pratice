# m=[1,2]
# m[1]=5
# print(m)

# m=(1,2)
# print(m)

# m={1,1.5,1}

# print(m)
# m={"name":"Sugam","roll":31}
# m["name"]
# print(m["name"])
# print("Sakriya Maharjan, from BCA Department teaches Python Programming")

# def main():

#     teacher=get_details()
#     print(f"{teacher[0]},from {teacher[1]} Department teaches {teacher[2]} Programming")

    
    
# def get_details():
    
#     name=input("Enter Name")
#     department=input("Enter department") 
#     Program= input("Enter Language")
#     return name,department,Program

# if __name__=="__main__":
#     main()

# def main():
#     teacher = get_details()
#     print(f"{teacher['name']}, from {teacher['department']} Department teaches {teacher['program']} Programming")

# def get_details():
#     details = {}
#     details['name'] = input("Enter Name: ")
#     details['department'] = input("Enter Department: ")
#     details['program'] = input("Enter Language: ")
#     return details

# if __name__ == "__main__":
#     main()


# class Teacher():
#     ...
    
# def main():
#     teacher = get_details()
#     print(f"{teacher.name}, from {teacher.department} Department teaches {teacher.program} Programming")


# def get_details():
#     teacher=Teacher()
#     teacher.name=input("Enter Name: ")
#     teacher.department= input("Enter Department: ")
#     teacher.program= input("Enter Language: ")
#     return teacher
        
# if __name__ == "__main__":
#       main()

# import random
# class Teacher():
    
#     def get_details(self):
#         self.name=input("Enter Name: ")
#         self.department= input("Enter Department: ")
#         self.program= input("Enter Language: ")
#         list=['a','b','c']
#         self.project=random.choice(list)
   
#         if not self.name:
#             raise ValueError("Name missing !Please enter a valid name")
#         if self.department not in ['BCA','BCE','BSC']:
#             raise ValueError("Department not availabe in ACEM")
#         if self.program not in ['Python','CLoud','Multimedia']:
#             raise ValueError("Subject not in this acem")
#         return self
        
#     def __str__(self):
#         return f"{self.name}, from {self.department} Department teaches {self.program} Programming project is{self.project}" 
    
    
    
# def main():
#     teacher = Teacher().get_details()
#     print(teacher)
#     # print(f"{teacher.name}, from {teacher.department} Department teaches {teacher.program} Programming")



        
# if __name__ == "__main__":
#       main()
      
# x=5 
# print(type(x))

class Teacher():
    def __init__(self,name,department,program):
        self.name=name
        self.department=department
        self.program=program
        
    college='ACEM'
    
    def __str__(self):
        return f"{self.name}, from {self.department} Department teaches {self.program} Programming " 



    @classmethod
    def get_details(cls):
        name=input("Enter Name: ")
        department= input("Enter Department: ")
        program= input("Enter Language: ")
      
   
        if not name:
            raise ValueError("Name missing !Please enter a valid name")
       
        if program not in ['Python','CLoud','Multimedia']:
            raise ValueError("Subject not in this acem")
        
        return cls(name,department,program)
    @property
    def department(self):
        return self._department

    @department.setter
    def department(self,department):
         if department not in ['BCA','BCE','BSC']:
            raise ValueError("Department not availabe in ACEM")
         self._department=department
        


     
def main():
    teacher = Teacher.get_details()
    teacher.department="BSW"
    print(teacher)
    # print(f"{teacher.name}, from {teacher.department} Department teaches {teacher.program} Programming")



if __name__ == "__main__":
    main()