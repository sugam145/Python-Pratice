# class Complex():
#     def __init__(self):
       
#         self.integerA=input("Enter first integer")
#         self.integerB=input("Enter second integer")
    
#     def display(self):
#         print(f"{self.integerA},......{self.integerB}")
        
# comp=Complex()
# comp.display()

#Method overloading
# def jod(*a): 
   
#     sum=0
#     for i in a:
#         sum=sum+i
#     print(sum)
    
          
# jod(1,2)
# jod(1,2,3)
# jod(1,2,3,4,5,6,7,8)

#Method overriding
# class College():
#     def task(self):
#         print("i work in ACEM")

# class Teacher(College):
#     ...
    
# class Students(College):
#     ...
    
# sugam=Teacher()
# sugam.task()

# class Student():
#     ...
        
# sugam=Student()
# cigar=Student()
# print(sugam+cigar)

#operator overloading
# class ComplexNum():
#     def __init__(self,real,imaginary):
#         self.real=real
#         self.imaginary=imaginary
    
#     def __add__(self,other):
#         self.real=self.real+other.real
#         self.imaginary=self.imaginary+other.imaginary
#         return f'{self.real}+{self.imaginary}'
    
# complex1=ComplexNum(1,4)
# complex2=ComplexNum(2,3)
# print(complex1+complex2)

class Student():
    def __init__(self,name,marks):
        self.name=name
        self.marks=marks
        
    def __gt__(self,other):
        if self.marks>other.marks:
            return True
        else:
            return False
    
    def __str__(self):
        return self.name
       
        
s1=Student('sugam',90)
s2=Student('cigar',88)
if s1>s2:
    
    print(s1)
else:
     print(s2)


    
        
        
