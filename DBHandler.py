# This class is used to handle the database. It is used to create, read, update and delete data from the database.
import sqlite3
import Employee
import re
import os
from tabulate import tabulate

# Regex to check if string is valid email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Titles array
titles = ["Mr", "Mrs", "Miss", "Dr", "Prof", "N/A"]

# String for cancellation
cancel = "#EXIT_USER_CANCEL#"

# Function to get user confirmation


def get_user_confirmation(notification):
    print(notification)
    print("1. Yes")
    print("2. No")
    try:
        user = int(input())
        if user == 1:
            return True
        else:
            return False
    except ValueError:
        return False


# Function that displays list for user selection and returns selection as String
def make_selection(array):
    while True:
        try:
            y = 1
            for i in array:
                print(str(y), ".", i)
                y = y+1
            print("To cancel, enter exit")
            print("Enter selection")
        except Exception as e:
            print(e)
            return False
        userinput = input()
        try:
            userinput = int(userinput) - 1
            if userinput < 0 or userinput > len(array) - 1:
                clearConsole()
                print("Invalid selection. Please choose from the following :")
            else:
                return array[userinput]
        except ValueError:
            if userinput.lower() == "exit":
                return cancel
            clearConsole()
            print("Invalid selection. Please choose from the following :")

# Function to check if the email is valid


def check(email):
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

# Clear console
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def clearWithMessage(message):
    clearConsole()
    print(message)
    
    
class DBOperations():
    # SQL statements

    # Statement to create table if it doesnt exists. Table name is EmployeeTable and should hold the following information
    #EmployeeID, EmployeeTitle, EmployeeName, EmployeeSurname, EmployeeEmail, EmployeeSalary
    sql_create_table = "CREATE TABLE IF NOT EXISTS EmployeeTable (EmployeeID INTEGER PRIMARY KEY, EmployeeTitle TEXT, EmployeeName TEXT, EmployeeSurname TEXT, EmployeeEmail TEXT, EmployeeSalary REAL)"

    # Statment to insert data to the table
    sql_insert = "INSERT INTO EmployeeTable (EmployeeID, EmployeeTitle, EmployeeName, EmployeeSurname, EmployeeEmail, EmployeeSalary) VALUES (?,?,?,?,?,?)"

    # Statement to select all data from table
    sql_select_all = "SELECT * FROM EmployeeTable"

    # Statement to search data from table
    sql_search_database = "SELECT * FROM EmployeeTable WHERE "

    # Statement to delete data from table using employeeID
    sql_delete_data = "DELETE FROM EmployeeTable WHERE EmployeeID = ?"

    # Statement to drop/delete table
    sql_drop_table = "DROP TABLE IF EXISTS EmployeeTable"

    # End of SQL Statements

    # Database connection
    def get_connection(self):
        try:
            self.conn = sqlite3.connect("DBName.db")
            self.cur = self.conn.cursor()
        except Exception as e:
            print(e)

    # Database operations. Choose between creating a table or deleting the one that exists
    def database_op(self):
        while True:
            clearConsole()
            userinput = make_selection(array=["Create Table", "Delete Table"])
            if userinput == "Create Table":
                self.create_table()
                break
            elif userinput == "Delete Table":
                clearConsole()
                if get_user_confirmation(notification="Are you sure you want to delete the table?") == True:
                    self.drop_table()
                    break
                else:
                    return False
            elif userinput == cancel:
                return False
            

    # Function to create table if a connection exists
    def create_table(self):
        try:
            self.get_connection()
            # Check if table exists
            self.cur.execute(
                ''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='EmployeeTable' ''')
            # If the count is 1, then table exists
            if self.cur.fetchone()[0] == 1:
                # If table exists then print message
                print('Table already exists.')
                return False
            else:
                # Create table
                self.cur.execute(self.sql_create_table)
                self.conn.commit()
                print("Table created successfully")
                return True
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    # Function to insert data to the table
    def insert_data(self):
        try:
            self.get_connection()
            emp = Employee.Employee()
            # Check if employee ID exists in the table. If it does warn the user and ask for a new employee ID
            while True:
                try:
                    print("To cancel, enter \"exit\"")
                    empID = input("Enter Employee ID: ")
                    if empID.lower() == "exit":
                        return False
                    empID = int(empID)
                    # Check if the employee ID exists in the table
                    if self.search_database(False, "EmployeeID", str(empID)) == True:
                        clearWithMessage("Employee ID already exists. Please enter different ID")
                    else:
                        emp.set_employee_id(empID)
                        break
                except ValueError:
                    clearWithMessage("Please enter digits only")

            clearConsole()
            title = make_selection(titles)
            if type(title) == str and title != cancel:
                emp.set_employee_title(title)
            elif title == cancel:
                print("Operation cancelled")
                return False
            else:
                print("Error in parsing title")
                return False

            clearWithMessage("Enter \"exit\" to cancel")
            empName = input("Enter Employee Name: ")
            if empName.lower() == "exit" or empName == "":
                print("Operation cancelled")
                input("Press enter to continue")
                return False
            else:
                emp.set_employee_forename(empName)
                
            clearWithMessage("Enter \"exit\" to cancel")
            empName = input("Enter Employee Surame: ")
            if empName.lower() == "exit" or empName == "":
                print("Operation cancelled")
                input("Press enter to continue")
                return False
            else:
                emp.set_employee_surname(empName)

            clearConsole()
            while True:
                email = input("Enter new email: ")
                if(check(email)):
                    emp.set_employee_email(email)
                    break
                elif email.lower() == "exit":
                    print("Operation cancelled")
                    input("Press enter to continue")
                    break
                else:
                    clearWithMessage("Invalid Email. Please try again")
                    continue
            clearConsole()
            while True:
                print("Enter \"exit\" to cancel")
                salary = input("Enter new salary: ")
                if salary.lower() == "exit" or salary == "":
                    print("Operation cancelled")
                    input("Press enter to continue")
                    break
                else:
                    try:
                        salary = int(float(salary))
                        emp.set_employee_salary(salary)
                        break
                    except ValueError:
                        clearWithMessage("Wrong format, please use digits and \".\" only")
            clearConsole()
            print ("\n",tabulate(emp.__str__(), headers=["Employee ID", "Employee Title", "Emloyee Name", "Employee Surame", "Employee Email", "Employee Salary"]))

            print("\n")
            if get_user_confirmation("Do you want to insert this data?") == True:
                self.get_connection()
                self.cur.execute(self.sql_insert, (emp.get_employee_id(), emp.get_employee_title(), emp.get_employee_forename(), emp.get_employee_surname(), emp.get_employee_email(), emp.get_employee_salary()))
                self.conn.commit()
                print("Inserted data successfully")
            else:
                print("Data not inserted")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    # Function to delete an entry from the table using employee ID
    def delete_data(self):
        try:
            self.get_connection()
            # Get employee ID
            employeeID = int(input("Enter Employee ID: "))
            # Check if the employee ID exists in the table. If it does then print the Name and surname of the employee
            if self.search_database(False, "EmployeeID", employeeID) == True:
                employee = self.get_employee_data(employeeID)
                print ("\n",tabulate(employee, headers=["Employee ID", "Employee Title", "Emloyee Name", "Employee Surame", "Employee Email", "Employee Salary"]))
                if get_user_confirmation("\nDo you want to delete this data?") == True:
                    self.get_connection()
                    self.cur.execute(self.sql_delete_data, (employeeID,))
                    self.conn.commit()
                    print("Deleted data successfully")
                else:
                    print("Data not deleted")
            else:
                print(
                    "Employee does not exists in the database. Please check the Employee ID")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    # Function to drop the table
    def drop_table(self):
        try:
            self.get_connection()

            self.cur.execute(sql_drop_table)
            print("Table deleted successfully")
        except Exception() as e:
            print(e)
        finally:
            self.conn.close()

    # Function to print all data from the table
    def print_all_data(self):
        try:
            self.get_connection()

            self.cur.execute(self.sql_select_all)
            result = self.cur.fetchall()
            print (tabulate(result, headers=["Employee ID", "Employee Title", "Emloyee Name", "Employee Surame", "Employee Email", "Employee Salary"]))
        except sqlite3.Error() as error:
            print(error)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    # Function to get Employee data from the table using employee ID
    def get_employee_data(self, employeeID):
        try:
            self.get_connection()

            if type(employeeID) == int:
                self.cur.execute(self.sql_search_database +
                                 "EmployeeID = ?", (employeeID,))
                result = self.cur.fetchall()
                return result
            return "No data found"
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    # Function to search for an entry in the table
    def search_database(self, display, *args):
        # First we must determine what to search for i.e. EmployeeID or EmployeeEmail
        # Provide a list of possible options for the user to choose from i.e. 1. Employee ID 2. Employee Email
        # If the user enters an invalid option then the function will return False
        try:
            self.get_connection()
            # Check if there are any arguments. If not ask user to input
            if args == ():
                while True:
                    print("Choose paramter to search for:")
                    selection = make_selection(["Employee ID", "Employee Name", "Employee Surname", "Employee Email"])
                    if selection == "Employee ID":
                        search_parameter = "EmployeeID"
                        break
                    elif selection == "Employee Name":
                        search_parameter = "EmployeeName"
                        break
                    elif selection == "Employee Surname":
                        search_parameter = "EmployeeSurname"
                        break
                    elif selection == "Employee Email":
                        search_parameter = "EmployeeEmail"
                        break
                    elif selection == cancel:
                        return False
                    else:
                        print("Invalid selection")
                # Get the search value
                clearConsole()
                print("Searching for : ", search_parameter)
                search_value = input("Enter search value: ")
            # If there are two arguments, i.e EmployeeID , 1 then use them to search the database.
            # If more than 2 arguments are provided then return False. If less than 2 arguments are provided then return False
            # The first argument is the search parameter and the second argument is the search value
            if len(args) == 2:
                search_parameter = args[0]
                search_value = args[1]
            elif args != () and len(args) != 2:
                if display == True:
                    print("Invalid number of arguments")
                return False
            # We now have the parameter to search for and the value to search for. We can now search the database
            # We need to build a string using sql_search_database and the search_parameter and search_value
            search_string = self.sql_search_database + \
                search_parameter + " LIKE '%" + str(search_value) + "%'"
            self.cur.execute(search_string)
            result = self.cur.fetchall()
            if len(result) == 0:
                if display:
                    print("No data found")
                return False
            else:
                if display:
                    print("\n Found ", len(result), " results:\n")
                    print (tabulate(result, headers=["Employee ID", "Employee Title", "Emloyee Name", "Employee Surame", "Employee Email", "Employee Salary"]))
                return True
        except sqlite3.Error as error:
            print(error)
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    # Function to update an entry in the table
    def update_data(self):
        while True:
            try:
                # Ask user for the EmployeeID of the entry to update
                print("To cancel, enter \"exit\"")
                empID = input("Enter Employee ID of the entry to update: ")
                if empID.lower() == "exit":
                    return False
                empID = int(empID)
                # Check if the employee ID exists in the table. If not then warn the user and ask for a new employee ID
                if self.search_database(False, "EmployeeID", str(empID)) == True:
                    break
                else:
                    print("Employee ID does not exist. Please enter a valid Employee ID")
            except ValueError:
                print("Invalid Employee ID")

        # EmployeeID exists. Create 2 employee objects. One for the old data and one for the new data
        clearConsole()
        old = Employee.Employee()
        new = Employee.Employee()
        old_data = self.get_employee_data(empID)
        old.set_employee_id(employeeID=old_data[0][0])
        old.set_employee_title(empTitle=old_data[0][1])
        old.set_employee_forename(forename=old_data[0][2])
        old.set_employee_surname(surname=old_data[0][3])
        old.set_employee_email(email=old_data[0][4])
        old.set_employee_salary(salary=old_data[0][5])
        new.set_employee_id(employeeID=old_data[0][0])
        new.set_employee_title(empTitle=old_data[0][1])
        new.set_employee_forename(forename=old_data[0][2])
        new.set_employee_surname(surname=old_data[0][3])
        new.set_employee_email(email=old_data[0][4])
        new.set_employee_salary(salary=old_data[0][5])
        
        
        #Ask the user what data they want to update.
        while True:
            clearConsole()
            selection = make_selection(array=["Employee ID", "Employee Title", "Employee Forename", "Employee Surname", "Employee Email", "Employee Salary", "Continue"],)
            if selection == cancel:
                print("Operation cancelled")
                return False
            elif selection == "Employee ID":
                clearConsole()
                while True:
                    print("Old Employee ID: ", old.get_employee_id())
                    print("New Employee ID: ", new.get_employee_id())
                    print("Enter new Employee ID or enter \"exit\" to cancel")
                    empID = input("Enter new Employee ID: ")
                    if empID.lower() == "exit":
                        print("Operation cancelled")
                        input("Press any key to continue...")
                        break
                    try:
                        if self.search_database(False, "EmployeeID", empID) == False:
                            new.set_employee_id(empID)
                            break
                        else:
                            clearWithMessage(
                                "Employee ID already exists. Please enter a new Employee ID")
                    except ValueError:
                        clearWithMessage("Please enter digits only")
                
            elif selection == "Employee Title":
                clearConsole()
                while True:
                    print("Previous title : ", old.get_employee_title())
                    print("New title: ", new.get_employee_title())
                    print("To update title make a selection")
                    title = make_selection(titles)
                    if type(title) == str and title != cancel:
                        new.set_employee_title(title)
                        break
                    elif title == cancel:
                        print("Operation cancelled")
                        input("Press enter to continue")
                        break
                    else:
                        clearWithMessage("Error in parsing title")
            elif selection == "Employee Forename":
                clearConsole()
                print("Old name : ", old.get_employee_forename())
                print("New name: ", new.get_employee_forename())
                print("To update the new name please enter the new name below, or enter \"exit\" to cancel")
                empName = input("Enter new name: ")
                if empName.lower() == "exit" or empName == "":
                    print("Operation cancelled")
                    input("Press enter to continue")
                    continue
                else:
                    new.set_employee_forename(empName)
            elif selection == "Employee Surname":
                clearConsole()
                print("Old name : ", old.get_employee_surname())
                print("New name: ", new.get_employee_surname())
                print("To update the new surname please enter the new surname below, or enter \"exit\" to cancel")
                empName = input("Enter new surname: ")
                if empName.lower() == "exit" or empName == "":
                    print("Operation cancelled")
                    input("Press enter to continue")
                    continue
                else:
                    new.set_employee_surname(empName)
            elif selection == "Employee Email":
                clearConsole()
                while True:
                    print("Old email : ", old.get_employee_email())
                    print("New email: ", new.get_employee_email())
                    print("To update the new email please enter the new email below, or enter \"exit\" to cancel")
                    email = input("Enter new email: ")
                    if(check(email)):
                        new.set_employee_email(email)
                        break
                    elif email.lower() == "exit":
                        print("Operation cancelled")
                        input("Press enter to continue")
                        break
                    else:
                        clearWithMessage("Invalid Email. Please try again")
                        continue
            elif selection == "Employee Salary":
                clearConsole()
                while True:
                    print("Old salary : ", old.get_employee_salary())
                    print("New salary: ", new.get_employee_salary())
                    print("To update the new salary please enter the new salary below, or enter \"exit\" to cancel")
                    salary = input("Enter new salary: ")
                    if salary.lower() == "exit" or salary == "":
                        print("Operation cancelled")
                        input("Press enter to continue")
                        break
                    else:
                        try:
                            salary = int(float(salary))
                            new.set_employee_salary(salary)
                            break
                        except ValueError:
                            clearWithMessage("Wrong format, please use digits and \".\" only")
            elif selection == "Continue":
                clearConsole()
                print("Are you sure you want to update the following details?")
                print("\nOld details : ")
                print (tabulate(old.__str__(), headers=["Employee ID", "Employee Title", "Emloyee Name", "Employee Surame", "Employee Email", "Employee Salary"]))
                print("\nNew details : ")
                print (tabulate(new.__str__(), headers=["Employee ID", "Employee Title", "Emloyee Name", "Employee Surame", "Employee Email", "Employee Salary"]))
                if get_user_confirmation("\nEnter selection") == True:
                    try: 
                        self.get_connection()
                        self.cur.execute(self.sql_delete_data, (old.get_employee_id(),))
                        self.conn.commit()
                        self.cur.execute(self.sql_insert, (new.get_employee_id(), new.get_employee_title(), new.get_employee_forename(), new.get_employee_surname(), new.get_employee_email(), new.get_employee_salary()))
                        self.conn.commit()
                        print("Updated data successfully")
                        break
                    except Exception as e:
                        print(e)
                        break
                    except sqlite3.Error():
                        print("Error updating data")
                        break
                    finally :
                        self.conn.close()
                else:
                    print("Update cancelled")
                    break
