class Employee:
  def __init__(self):
    self.employeeID = 0
    self.empTitle = ''
    self.forename = ''
    self.surname = ''
    self.email = ''
    self.salary = 0.0

  def set_employee_id(self, employeeID):
    self.employeeID = employeeID

  def set_employee_title(self, empTitle):
    self.empTitle = empTitle

  def set_employee_forename(self,forename):
   self.forename = forename
  
  def set_employee_surname(self,surname):
    self.surname = surname

  def set_employee_email(self,email):
    self.email = email
  
  def set_employee_salary(self,salary):
    self.salary = salary
  
  def get_employee_id(self):
    return self.employeeID

  def get_employee_title(self):
    return self.empTitle
  
  def get_employee_forename(self):
    return self.forename
  
  def get_employee_surname(self):
    return self.surname
  
  def get_employee_email(self):
    return self.email
  
  def get_employee_salary(self):
    return self.salary

  def __str__(self):
    return [[str(self.employeeID) , self.empTitle , self.forename , self.surname , self.email , "$"+str(self.salary)]]

