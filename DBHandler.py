#This class is used to handle the database. It is used to create, read, update and delete data from the database.
import sqlite3
import Employee

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
        self.cur.execute(sql_create_table)
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
      emp.set_employee_id(int(input("Enter Employee ID: ")))
      #Check if employee ID exists in the table. If it does warn the user and ask for a new employee ID
      while True:
        #Search for the employeeID in the table
        if self.search_database(False, emp.get_employee_id()) == True:
          print("Employee ID already exists. Please enter a new Employee ID")
          emp.set_employee_id(int(input("Enter Employee ID: ")))
        else:
          break
      emp.set_employee_title(input("Enter Employee Title: "))
      emp.set_employee_forename(input("Enter Employee Name: "))
      emp.set_employee_surname(input("Enter Employee Surname: "))
      emp.set_employee_email(input("Enter Employee Email: "))
      emp.set_employee_salary(float(input("Enter Employee Salary: ")))


      self.get_connection()
      self.cur.execute(self.sql_insert,tuple(str(emp).split("\n")))

      self.conn.commit()
      print("Inserted data successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  #Function to delete an entry from the table using employee ID
  def delete_data(self):
    try:
      self.get_connection()
      #Get employee ID
      employeeID = int(input("Enter Employee ID: "))
      #Check if the employee ID exists in the table. If it does then print the Name and Surname of the employee to delete
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
        print(row)
    except Exception() as e:
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
      search_string = self.sql_search_database + search_parameter + " = '" + search_value + "'"
      self.cur.execute(search_string)
      result = self.cur.fetchall()
      if result is None:
        if display:
          print("No data found")
        return False
      else:
        if display:
          for row in result:
            print(row)
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
      empTitle = (input("Enter Employee Title: "))
      empName = (input("Enter Employee Name: "))
      empSurname = (input("Enter Employee Surname: "))
      empEmail = (input("Enter Employee Email: "))
      empSalary = (float(input("Enter Employee Salary: ")))
      
      #Get user confirmation
      print("Are you sure you want to update the following details?")
      print("Employee ID: " + str(empID) + "\nEmployee Title: " + empTitle + "\nEmployee Name: " + empName + "\nEmployee Surname: " + empSurname + "\nEmployee Email: " + empEmail + "\nEmployee Salary: " + str(empSalary))
      print("1. Yes")
      print("2. No")
      confirmation = int(input("Enter your choice: "))
      if confirmation != 1:
        print("Update cancelled")
        return False
      elif confirmation == 1:
        self.get_connection()
        self.cur.execute(sql_update_data,(empTitle, empName, empSurname, empEmail, empSalary, empID))
        self.conn.commit()
        print("Updated data successfully")
     

    except Exception as e:
      print(e)
    finally:
      self.conn.close()
      