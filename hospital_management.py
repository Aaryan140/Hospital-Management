from prettytable import PrettyTable
import mysql.connector as sqlpyn

# Establish connection to MySQL database
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

# Display records of all patients
def display_records(cursor):
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

# Insert new records
def insert_record(cursor, con):
    try:
        cursor.execute("SELECT MAX(p_no) FROM patient_records")
        last_p_no = cursor.fetchone()[0]
        if last_p_no is not None:
            p_no = last_p_no + 1
        else:
            p_no = 1

        cursor.execute("SELECT MAX(p_id) FROM patient_records")
        last_p_id = cursor.fetchone()[0]
        if last_p_id is not None:
            p_id = last_p_id + 1
        else:
            p_id = 1

        p_name = input("Patient's name:")
        age = int(input("Age:"))
        department = input("Department:")
        diagnostic = input("Diagnostic:")
        insert_query = "INSERT INTO patient_records(p_no, p_name, p_id, age, department, diagnostic) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (p_no, p_name, p_id, age, department, diagnostic))
        con.commit()  # Commit the transaction
        print("Record inserted successfully.")
    except Exception as e:
        print("Error inserting record:", e)



# Modify existing records
# Modify existing records
def modify_record(cursor, con):
    try:
        patient_name = input("Enter patient name whose records you want to modify: ")
        cursor.execute("SELECT * FROM patient_records WHERE p_name = %s", (patient_name,))
        data = cursor.fetchall()
        if data:
            if len(data) > 1:
                print("Multiple records found for the given patient name:")
                table = PrettyTable(["P_No", "P_Name", "P_ID", "Age", "Department", "Diagnostic"])
                table._max_width = {"P_No": 10, "P_Name": 10, "P_ID": 15, "Age": 10, "Department": 50, "Diagnostic": 20}
                for row in data:
                    table.add_row(row)
                print(table)
                p_no = int(input("Enter the patient number of the record you want to modify: "))
            else:
                p_no = data[0][0]
            column = input("Enter column you want to update (Name/ID/Age/Department/Diagnostics): ")
            value = input(f"Enter new {column}:")
            update_query = f"UPDATE patient_records SET {column.lower()} = %s WHERE p_no = %s"
            cursor.execute(update_query, (value, p_no))
            con.commit()  # Commit the transaction
            print("Record updated successfully.")
        else:
            print("No records found for the given name.")
    except Exception as e:
        print("Error updating record:", e)


# Delete records
def delete_record(cursor, con):
    try:
        patient_name = input("Enter patient name whose records you want to delete: ")
        cursor.execute("SELECT * FROM patient_records WHERE p_name = %s", (patient_name,))
        data = cursor.fetchall()
        if data:
            if len(data) > 1:
                print("Multiple records found for the given patient name:")
                table = PrettyTable(["P_No", "P_Name", "P_ID", "Age", "Department", "Diagnostic"])
                table._max_width = {"P_No": 10, "P_Name": 10, "P_ID": 15, "Age": 10, "Department": 50, "Diagnostic": 20}
                for row in data:
                    table.add_row(row)
                print(table)
                p_no = int(input("Enter the patient number of the record you want to delete: "))
                delete_query = "DELETE FROM patient_records WHERE p_no = %s"
                cursor.execute(delete_query, (p_no,))
                con.commit()  # Commit the transaction
                print("Record deleted successfully.")
            else:
                delete_query = "DELETE FROM patient_records WHERE p_name = %s"
                cursor.execute(delete_query, (patient_name,))
                con.commit()  # Commit the transaction
                print("Record(s) deleted successfully.")
        else:
            print("No records found for the given name.")
    except Exception as e:
        print("Error deleting record:", e)


# Search records
def search_records(cursor, con):
    try:
        while True:
            patient_name = input("Enter patient name to search: ")
            cursor.execute("SELECT * FROM patient_records WHERE p_name LIKE %s", (f"%{patient_name}%",))
            data = cursor.fetchall()
            if data:
                table = PrettyTable(["P_No", "P_Name", "P_ID", "Age", "Department", "Diagnostic"])
                table._max_width = {"P_No": 10, "P_Name": 10, "P_ID": 15, "Age": 10, "Department": 50, "Diagnostic": 20}
                for row in data:
                    table.add_row(row)
                print(table)
            else:
                print("No records found for the given name.")
            con.commit()  # Commit the transaction
            more_records = input("Do you want to search more records? (yes/no)").lower()
            if more_records != "yes":
                break
    except Exception as e:
        print("Error searching records:", e)

def main():
    con = connect_to_database()
    if con:
        try:
            cursor = con.cursor()
            while True:
                print("\nMAIN MENU")
                print("1. Show records of all patients.")
                print("2. Insert new records.")
                print("3. Modify existing records.")
                print("4. Delete records.")
                print("5. Search records.")
                print("6. EXIT")

                choice = int(input("Enter your choice from the above: "))

                if choice == 1:
                    display_records(cursor)
                elif choice == 2:
                    insert_record(cursor, con)
                elif choice == 3:
                    modify_record(cursor, con)
                elif choice == 4:
                    delete_record(cursor, con)
                elif choice == 5:
                    search_records(cursor,con)
                elif choice == 6:
                    print("Thanks for visiting!")
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")
        finally:
            cursor.close()
            con.close()
            print("Connection to the database closed.")

if __name__ == "__main__":
    main()
