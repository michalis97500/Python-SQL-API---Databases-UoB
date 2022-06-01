#Import the necessary classes, DBHandler
import DBHandler as DB
import os

DBCommand = DB.DBOperations()


#Clear console 
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

clearConsole()

#Wait for user input
def wait():
  input("Press Enter to continue...")
  clearConsole()
  
while True:
  print ("\n Menu:")
  print ("**********")
  print (" 1. Create Employee Table")
  print (" 2. Insert data into Employee Table")
  print (" 3. Select all data from Employee Table")
  print (" 4. Search data from Employee Table")
  print (" 5. Update data records")
  print (" 6. Delete data records")
  print (" 7. Exit\n")

  __choose_menu = int(input("Enter your choice: "))
  clearConsole()
  if __choose_menu == 1:
    DBCommand.create_table()
    wait()
  elif __choose_menu == 2:
    DBCommand.insert_data()
    wait()
  elif __choose_menu == 3:
    DBCommand.print_all_data()
    wait()
  elif __choose_menu == 4:
    DBCommand.search_database(True)
    wait()
  elif __choose_menu == 5:
    DBCommand.update_data()
    wait()
  elif __choose_menu == 6:
    DBCommand.delete_data()
    wait()
  elif __choose_menu == 7:
    exit(0)
  else:
    print ("Invalid Choice")
    wait()
 



