from dotenv import load_dotenv
import streamlit as st
import os
import mysql.connector as sqlpyn
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini model
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt, question])
    return response.text.strip()

# Function to read SQL query
def read_sql_query(sql):
    con = sqlpyn.connect(host="localhost", user="root", password="aryan2323", database="hospital")
    cur = con.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        con.commit()
    except sqlpyn.Error as e:
        rows = [("Error", str(e))]
    finally:
        con.close()
    return rows

# Function to execute SQL command (insert, modify, delete)
def execute_sql_command(sql):
    con = sqlpyn.connect(host="localhost", user="root", password="aryan2323", database="hospital")
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
        result = "Command executed successfully."
    except sqlpyn.Error as e:
        result = f"Error: {str(e)}"
    finally:
        con.close()
    return result
# Define the prompt for the language model
prompt = """
You are a language model capable of converting natural language questions into SQL queries. The SQL database you will work with is named 'hospital', and it has a table named 'patient_records' with the following columns:
- p_no: Patient Number
- p_name: Patient Name
- p_id: Patient ID
- age: Patient Age
- department: Patient Department
- diagnostic: Patient Diagnostic

Your task is to generate SQL queries based on natural language questions about this table. Ensure the SQL queries are valid, correctly formatted, and retrieve only the necessary information from the database.

Examples:
1. For the question "How many patient records are there?", the SQL query should be:
   SELECT COUNT(*) FROM patient_records;

2. For the question "Which patients have leukemia?", the SQL query should be:
   SELECT * FROM patient_records WHERE diagnostic = 'leukemia';

3. For the question "What is the age of the patient with p_no 5?", the SQL query should be:
   SELECT age FROM patient_records WHERE p_no = 5;

4. For the question "Which patient has the ID 1001?", the SQL query should be:
   SELECT p_name FROM patient_records WHERE p_id = 1001;

5. For the question "What are the diagnostic details for the patient named 'John Doe'?", the SQL query should be:
   SELECT diagnostic FROM patient_records WHERE p_name = 'John Doe';

Please provide only the SQL query in response. Do not include any additional text or explanations.

If the question is not clear or does not fit the schema, provide a suitable response indicating the issue.

Example questions:
1. How many patients are in the hospital?
2. What is the age of the patient with p_no 5?
3. Which patient has the ID 1001?
4. What are the diagnostic details for the patient named 'John Doe'?
"""

# Streamlit app
st.set_page_config(page_title="SQL Query Generator and Executor")
st.header("Hospital Management")
st.header("Ask a Question to Generate SQL Query")

# Tab layout for different functionalities
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Query", "Insert", "Modify", "Delete", "Search"])

# Query tab
with tab1:
    question = st.text_input("Enter your question:")
    if st.button("Get SQL Query"):
        response = get_gemini_response(question, prompt)
        st.subheader("Generated SQL Query:")
        st.code(response, language='sql')

        # Execute SQL query and show results
        data = read_sql_query(response)
        st.subheader("Query Results:")
        if data:
            for row in data:
                st.write(row)
        else:
            st.write("No data found or there was an error in the query.")

# Insert tab
with tab2:
    st.subheader("Insert New Record")
    p_no = st.number_input("Patient Number", min_value=1)
    p_name = st.text_input("Patient Name")
    p_id = st.number_input("Patient ID", min_value=1)
    age = st.number_input("Age", min_value=0)
    department = st.text_input("Department")
    diagnostic = st.text_input("Diagnostic")
    if st.button("Insert Record"):
        insert_sql = f"INSERT INTO patient_records (p_no, p_name, p_id, age, department, diagnostic) VALUES ({p_no}, '{p_name}', {p_id}, {age}, '{department}', '{diagnostic}');"
        result = execute_sql_command(insert_sql)
        st.write(result)

# Modify tab
with tab3:
    st.subheader("Modify Existing Record")
    p_no = st.number_input("Enter Patient Number to Modify", min_value=1)
    column = st.selectbox("Column to Modify", ["p_name", "p_id", "age", "department", "diagnostic"])
    new_value = st.text_input("New Value")
    if st.button("Modify Record"):
        modify_sql = f"UPDATE patient_records SET {column} = '{new_value}' WHERE p_no = {p_no};"
        result = execute_sql_command(modify_sql)
        st.write(result)

# Delete tab
with tab4:
    st.subheader("Delete Record")
    p_no = st.number_input("Enter Patient Number to Delete", min_value=1)
    if st.button("Delete Record"):
        delete_sql = f"DELETE FROM patient_records WHERE p_no = {p_no};"
        result = execute_sql_command(delete_sql)
        st.write(result)

# Search tab
with tab5:
    st.subheader("Search Record")
    p_no = st.number_input("Enter Patient Number to Search", min_value=1)
    if st.button("Search Record"):
        search_sql = f"SELECT * FROM patient_records WHERE p_no = {p_no};"
        data = read_sql_query(search_sql)
        if data:
            for row in data:
                st.write(row)
        else:
            st.write("No data found for the given Patient Number.")

