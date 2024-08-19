import mysql.connector as sqlpyn
from prettytable import PrettyTable

def connect_to_database():
    try:
        con = sqlpyn.connect(host="localhost", user="root", password="aryan2323", database="hospital")
        if con.is_connected():
            print("Successfully connected to the database.")
            return con
        else:
            print("Error connecting to the database.")
            return None
    except Exception as e:
        print("Error:", e)
        return None

def display_records(con):
    cursor = con.cursor()
    try:
        cursor.execute("SELECT * FROM patient_records;")
        data = cursor.fetchall()
        table = PrettyTable(["P_No", "P_Name", "P_ID", "Age", "Department", "Diagnostic"])
        table._max_width = {"P_No": 10, "P_Name": 10, "P_ID": 15, "Age": 10, "Department": 50, "Diagnostic": 20}
        for row in data:
            table.add_row(row)
        print(table)
    except Exception as e:
        print("Error displaying records:", e)
    finally:
        cursor.close()

def insert_record(con, p_no, p_name, p_id, age, department, diagnostic):
    cursor = con.cursor()
    try:
        insert_query = "INSERT INTO patient_records(p_no, p_name, p_id, age, department, diagnostic) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (p_no, p_name, p_id, age, department, diagnostic))
        con.commit()  # Commit the transaction
        print("Record inserted successfully.")
    except Exception as e:
        print("Error inserting record:", e)
    finally:
        cursor.close()

def modify_record(con, p_no, column, new_value):
    cursor = con.cursor()
    try:
        update_query = f"UPDATE patient_records SET {column} = %s WHERE p_no = %s"
        cursor.execute(update_query, (new_value, p_no))
        con.commit()  # Commit the transaction
        print("Record updated successfully.")
    except Exception as e:
        print("Error updating record:", e)
    finally:
        cursor.close()

def delete_record(con, p_no):
    cursor = con.cursor()
    try:
        delete_query = "DELETE FROM patient_records WHERE p_no = %s"
        cursor.execute(delete_query, (p_no,))
        con.commit()  # Commit the transaction
        print("Record deleted successfully.")
    except Exception as e:
        print("Error deleting record:", e)
    finally:
        cursor.close()

def search_records(con, p_no):
    cursor = con.cursor()
    try:
        cursor.execute("SELECT * FROM patient_records WHERE p_no = %s", (p_no,))
        data = cursor.fetchall()
        if data:
            table = PrettyTable(["P_No", "P_Name", "P_ID", "Age", "Department", "Diagnostic"])
            table._max_width = {"P_No": 10, "P_Name": 10, "P_ID": 15, "Age": 10, "Department": 50, "Diagnostic": 20}
            for row in data:
                table.add_row(row)
            print(table)
        else:
            print("No records found for the given Patient Number.")
    except Exception as e:
        print("Error searching records:", e)
    finally:
        cursor.close()

def menu(con):
    while True:
        print("\n")
        print("MAIN MENU")
        print("1. Display all records")
        print("2. Insert a new record")
        print("3. Modify an existing record")
        print("4. Delete a record")
        print("5. Search for a record")
        print("6. Exit")
        choice = input("Enter your choice :) ")
        
        if choice == "1":
            display_records(con)
        elif choice == "2":
            p_no = input("Enter Patient Number: ")
            p_name = input("Enter Patient Name: ")
            p_id = input("Enter Patient ID: ")
            age = input("Enter Age: ")
            department = input("Enter Department: ")
            diagnostic = input("Enter Diagnostic Information: ")
            insert_record(con, p_no, p_name, p_id, age, department, diagnostic)
        elif choice == "3":
            p_no = input("Enter Patient Number to modify: ")
            column = input("Enter the column to modify (p_name, p_id, age, department, diagnostic): ")
            new_value = input(f"Enter the new value for {column}: ")
            modify_record(con, p_no, column, new_value)
        elif choice == "4":
            p_no = input("Enter Patient Number to delete: ")
            delete_record(con, p_no)
        elif choice == "5":
            p_no = input("Enter Patient Number to search: ")
            search_records(con, p_no)
        elif choice == "6":
            print("Thank you :)")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    con = connect_to_database()
    if con:
        menu(con)
        con.close()
