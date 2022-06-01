#This class is used to handle the database. It is used to create, read, update and delete data from the database.
import sqlite3
import Employee
import re
import os

#Regex to check if string is valid email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

titles = ["Mr" , "Mrs", "Miss", "Dr", "Prof", "N/A"]

def get_user_confirmation(notification):
  print(notification)
  print("1. Yes")
  print("2. No")
  try:
    user = int(input())
    if user==1:
      return True
    else:
      return False
  except ValueError:
    return False


#Function that displays list for user selection and returns selection as String
def make_selection(array):
  while True :
    try:
      y=1
      for i in array:
        print(str(y),".",i)
        y = y+1
      print("Enter selection")
    except Exception as e:
      print(e)
      return False
    try:
      userinput = int(input()) - 1
      if userinput < 0 or userinput > len(array) -1 :
        clearConsole()
        print("Invalid selection. Please choose from the following :")
      else: 
        return array[userinput]
    except ValueError:
      clearConsole()
      print("Invalid selection. Please choose from the following :")
    
#Function to check if the email is valid
def check(email):
  # pass the regular expression
  # and the string into the fullmatch() method
  if(re.fullmatch(regex, email)):
    return True
  else:
    return False
  
#Clear console 
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

class DBOperations():
  #SQL statements
    
  #Statement to create table if it doesnt exists. Table name is EmployeeTable and should hold the following information
  #EmployeeID, EmployeeTitle, EmployeeName, EmployeeSurname, EmployeeEmail, EmployeeSalary
  sql_create_table = "CREATE TABLE IF NOT EXISTS EmployeeTable (EmployeeID INTEGER PRIMARY KEY, EmployeeTitle TEXT, EmployeeName TEXT, EmployeeSurname TEXT, EmployeeEmail TEXT, EmployeeSalary REAL)"
  
  #Statment to insert data to the table
  sql_insert = "INSERT INTO EmployeeTable (EmployeeID, EmployeeTitle, EmployeeName, EmployeeSurname, EmployeeEmail, EmployeeSalary) VALUES (?,?,?,?,?,?)"
  
  #Statement to select all data from table
  sql_select_all = "SELECT * FROM EmployeeTable"
  
  #Statement to search data from table
  sql_search_database = "SELECT * FROM EmployeeTable WHERE "
  
  #Statement to update data in table using employeeID
  sql_update_data = "UPDATE EmployeeTable SET EmployeeTitle = ?, EmployeeName = ?, EmployeeSurname = ?, EmployeeEmail = ?, EmployeeSalary = ? WHERE EmployeeID = ? "
  
  #Statement to delete data from table using employeeID
  sql_delete_data = "DELETE FROM EmployeeTable WHERE EmployeeID = ?"
  
  #Statement to drop/delete table
  sql_drop_table = "DROP TABLE IF EXISTS EmployeeTable"
  
  #End of SQL Statements


  #Database connection
  def get_connection(self):
    try:
      self.conn = sqlite3.connect("DBName.db")
      self.cur = self.conn.cursor()
    except Exception as e:
      print(e)


  #Function to create table if a connection exists
  def create_table(self):
    try:
      self.get_connection()
      #Check if table exists
      self.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='EmployeeTable' ''')
      #If the count is 1, then table exists
      if self.cur.fetchone()[0]==1 :
        #If table exists then print message
        print('Table already exists.')
      else:
        #Create table
        self.cur.execute(self.sql_create_table)
        self.conn.commit()
        print("Table created successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  #Function to insert data to the table
  def insert_data(self):
    try:
      self.get_connection()
      emp = Employee.Employee()
      #Check if employee ID exists in the table. If it does warn the user and ask for a new employee ID
      while True:
        try:
          emp.set_employee_id(int(input("Enter Employee ID: ")))
          #Search for the employeeID in the table
          if self.search_database(False, "EmployeeID", emp.get_employee_id()) == False:
            break
          else:
            print("Employee ID already exists. Please enter a new Employee ID")
        except ValueError:
          print("Please enter digits only")

      clearConsole()
      title = make_selection(titles)
      if type(title) == str:
        emp.set_employee_title(title)
      else : 
        print("Error in parsing title")
        return False
  
      clearConsole()
      
      emp.set_employee_forename(input("Enter Employee Name: "))
      emp.set_employee_surname(input("Enter Employee Surname: "))
      
      clearConsole()
      while True:
        email = input("Enter Employee Email: ")
        if(check(email)):
          emp.set_employee_email(email)
          break
        else:
          print("Invalid Email. Please try again")
          
      clearConsole()
      while True:    
        try:
          emp.set_employee_salary(float(input("Enter Employee Salary: ")))
          break;
        except ValueError:
          print("Wrong format, please use digits and \".\" only")
      clearConsole()
      
      #Get user confirmation before executing query. Display all data to be inserted
      print("Employee ID: ", emp.get_employee_id())
      print("Employee Title: ", emp.get_employee_title())
      print("Employee Name: ", emp.get_employee_forename())
      print("Employee Surname: ", emp.get_employee_surname())
      print("Employee Email: ", emp.get_employee_email())
      print("Employee Salary: $", emp.get_employee_salary())
      
      print("\n")
      if get_user_confirmation("Do you want to insert this data?") == True:
          self.get_connection()
          self.cur.execute(self.sql_insert,tuple(str(emp).split("\n")))

          self.conn.commit()
          print("Inserted data successfully")
      else:
        print("Data not inserted")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  #TODO
  #Function to delete an entry from the table using employee ID
  def delete_data(self):
    try:
      self.get_connection()
      #Get employee ID
      employeeID = int(input("Enter Employee ID: "))
      #Check if the employee ID exists in the table. If it does then print the Name and surname of the employee
      if self.search_database(False, "EmployeeID", employeeID) == True:
        employee = self.get_employee_data(employeeID)
        print("Employee to be deleted: ", employee[0][1] , employee[0][2] ,  employee[0][3], " with ID: ", employee[0][0])
        if get_user_confirmation("Do you want to delete this data?") == True:
          self.get_connection()
          self.cur.execute(self.sql_delete_data, (employeeID,))
          self.conn.commit()
          print("Deleted data successfully")
        else:
          print("Data not deleted")
      else:
        print("Employee does not exists in the database. Please check the Employee ID")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
      
  #Function to drop the table
  def drop_table(self):
    try:
      self.get_connection()
      
      self.cur.execute(sql_drop_table)
      print("Table deleted successfully")
    except Exception() as e:
      print(e)
    finally:
      self.conn.close()
      
  #Function to print all data from the table
  def print_all_data(self):
    try:
      self.get_connection()
      
      self.cur.execute(self.sql_select_all)
      result = self.cur.fetchall()
      
      for row in result:
        print(row[0],row[1],row[2],row[3],row[4],row[5])
    except sqlite3.Error() as error:
      print(error)
    except Exception as e:
      print(e)   
    finally:
      self.conn.close()

  #Function to get Employee data from the table using employee ID
  def get_employee_data(self, employeeID):
    try:
      self.get_connection()
      
      if type(employeeID) == int:
        self.cur.execute(self.sql_search_database + "EmployeeID = ?", (employeeID,))
        result = self.cur.fetchall()
        return result
      return "No data found"
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  #Function to search for an entry in the table
  def search_database(self, display, *args):
    #First we must determine what to search for i.e. EmployeeID or EmployeeEmail
    #Provide a list of possible options for the user to choose from i.e. 1. Employee ID 2. Employee Email
    #If the user enters an invalid option then the function will return False
    try:
      self.get_connection()
      #Check if there are any arguments. If not ask user to input
      if args == ():
        while True:
          print("Choose paramter to search for:")
          print("1. Employee ID")
          print("2. Employee Name")
          print("3. Employee Surname")
          print("4. Employee Email")
          print("5. Cancel")
          option = int(input("Enter your choice: "))
          if option == 1:
            search_parameter = "EmployeeID"
          elif option == 2:
            search_parameter = "EmployeeName"
          elif option == 3:
            search_parameter = "EmployeeSurname"
          elif option == 4:
            search_parameter = "EmployeeEmail"
          elif option == 5:
            return False
          elif option > 5:
            print("Invalid option")
            continue
          if search_parameter != "":
            break
        #Get the search value
        search_value = input("Enter search value: ")
      #If there are two arguments, i.e EmployeeID , 1 then use them to search the database. 
      #If more than 2 arguments are provided then return False. If less than 2 arguments are provided then return False
      #The first argument is the search parameter and the second argument is the search value
      if len(args) == 2:
        search_parameter = args[0]
        search_value = args[1]
      elif args != () and len(args) != 2:
        if display == True:
          print("Invalid number of arguments")
        return False
      #We now have the parameter to search for and the value to search for. We can now search the database
      #We need to build a string using sql_search_database and the search_parameter and search_value
      search_string = self.sql_search_database + search_parameter + " = '" + str(search_value) + "'"
      self.cur.execute(search_string)
      result = self.cur.fetchall()
      if len(result) == 0:
        if display:
          print("No data found")
        return False
      else:
        if display:
          for row in result:
            print(row[0],row[1],row[2],row[3],row[4],row[5])
        return True
    except sqlite3.Error as error:
      print(error)
    except Exception as e:
      print(e)   
    finally:
      self.conn.close()
        
  #Function to update an entry in the table
  def update_data(self):
    try:
      self.get_connection()
      #Ask user for the EmployeeID of the entry to update
      empID = int(input("Enter Employee ID: "))
      
      #Check if the employee ID exists in the table. If not then warn the user and ask for a new employee ID
      while True:
        if self.search_database(False, "EmployeeID", str(empID) ) == False:
          print("Employee ID does not exist. Please enter a valid Employee ID")
          empID = int(input("Enter Employee ID: "))
        else:
          break
        
      #EmployeeID exists. Ask the user for the new details
      clearConsole()
      title = make_selection(titles)
      if type(title) == str:
        empTitle = title
      else : 
        print("Error in parsing title")
        return False
      
      empName = (input("Enter Employee Name: "))
      empSurname = (input("Enter Employee Surname: "))
      clearConsole()
      empEmail = (input("Enter Employee Email: "))
      clearConsole()
      while True:    
        try:
          empSalary = (float(input("Enter Employee Salary: ")))
          break;
        except ValueError:
          print("Wrong format, please use digits and \".\" only")
      #Get user confirmation
      clearConsole()
      print("Are you sure you want to update the following details?")
      print("Employee ID: " + str(empID) + "\nEmployee Title: " + empTitle + "\nEmployee Name: " + empName + "\nEmployee Surname: " + empSurname + "\nEmployee Email: " + empEmail + "\nEmployee Salary: " + str(empSalary))
      if get_user_confirmation("\n") == True :
        self.get_connection()
        self.cur.execute(self.sql_update_data,(empTitle, empName, empSurname, empEmail, empSalary, empID))
        self.conn.commit()
        print("Updated data successfully")
      else:
        print("Update cancelled")    
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
  
 
