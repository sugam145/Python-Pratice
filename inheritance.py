# class Human():
#     def __init__(self,name):
#         self.name=name
        
#     def show(self):
#         return f' Hi !{self.name}'
    
# class Male(Human):
#     ...

# male=Male('Sugam')
# print(male.show())

# class College():
#      def work(self):
#          print("I do assignment")
    
# class Office():
#     def work(self):
#         print("I do code")

# class Student(College,Office):
#     ...
    
# student=Student()
# student.work()
# print(Student.mro())

# class Human():
#     def __init__(self,name):
#         self.name=name

# class Male(Human):
#     def show(self):
#         print(f"{self.name}. yoyo")
# class Boy(Male):
#     ...
# boy=Boy('sugam')
# boy.show()
# print(boy.name)

# class Human():
#     def __init__(self,name):
#         self.name=name
    
# class Male(Human):
#     def work(self):
#         print(f"{self.name}.. i m male")

# class Female(Human):
#      def work(self):
#         print(f"{self.name}.. i m female")
        
# male=Male("sugam")
# male.work()

# female=Female('maya')
# female.work()      

    
# class Human():
#     def __init__(self,name):
#         self.name=name

# class Male(Human):
#     def work(self):
#         print(f"{self.name}.. i m male")
    
# class Female(Human):
#     def work(self):
#         print(f"{self.name}.. i m female")
    
# class Boy(Male):
#      def work(self):
#         print(f"{self.name}.. i m boy")
    
# class Girl(Female):
#     #  def work(self):
#     #     print(f"{self.name}.. i m girl")
#     ...
# class Student(Girl,Boy):
#     ...
    
# student=Student('sugam')
# student.work()
# print(student.name)
# print(Student.mro())

class College():
    def __init__(self,name,email):
        self.name=name
        self.email=email
        
class Student(College):
    ...

class Teacher(College):
    def __init__(self, name, email, department, subject, salary):
        super().__init__(name, email)
        self.department = department
        self.subject = subject
        self.salary = float(salary)

    def calculate_vat(self):
        if self.salary > 600000:
            return self.salary * 0.15
        return 0
        

class Fulltime(Teacher):
    def __init__(self, name, email, department, subject, salary):
        super().__init__(name, email, department, subject, salary)
    
    def calculate_tax(self):
        return self.salary * 0.15
    
    def detail(self):
        tax = self.calculate_tax()
        vat = self.calculate_vat()
        total_deductions = tax + vat
        salary_after_deductions = self.salary - total_deductions
        print(f"Name: {self.name}, Email: {self.email}")
        print(f"Department: {self.department}, Subject: {self.subject}")
        print(f"Salary: {self.salary}")
        print(f"Income Tax: {tax}")
        if vat > 0:
            print(f"VAT (for salaries > 600000): {vat}")
        print(f"Salary After Tax and VAT: {salary_after_deductions}")

            
      
    
class Parttime(Teacher):
    def __init__(self, name, email, department, subject, salary):
        super().__init__(name, email, department, subject, salary)
    
    def calculate_tax(self):
        return self.salary * 0.10
    
    def detail(self):
        tax = self.calculate_tax()
        vat = self.calculate_vat()
        total_deductions = tax + vat
        salary_after_deductions = self.salary - total_deductions
        print(f"Name: {self.name}, Email: {self.email}")
        print(f"Department: {self.department}, Subject: {self.subject}")
        print(f"Salary: {self.salary}")
        print(f"Income Tax: {tax}")
        if vat > 0:
            print(f"VAT (for salaries > 600000): {vat}")
        print(f"Salary After Tax and VAT: {salary_after_deductions}")
        
    
    

parttime=Parttime("sugam","yoyoy","bca","cloud","6000")
parttime.detail()


fulltime=Fulltime("sugam","yoyoy","bca","cloud","6000")
fulltime.detail()


