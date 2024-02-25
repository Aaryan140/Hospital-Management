# Hospital-Management
Hospital Management project with python and mysql.
# Hospital Management System

This project is a simple hospital management system implemented in Python using MySQL as the database. It allows users to perform basic CRUD (Create, Read, Update, Delete) operations on patient records.

## Features

- Display records of all patients
- Insert new patient records
- Modify existing patient records
- Delete patient records
- Search for patient records by name

## Requirements

To run this project, you'll need:
- Python 3.x
- MySQL Server
- MySQL Connector for Python (`mysql-connector-python`)

## Setup

1. Clone the repository:
git clone https://github.com/Aaryan140/hospital-management.git

2. Create the MySQL database and table by executing the following SQL script in your MySQL command-line client or GUI tool:
   - [create_table.sql](create_table.sql)

3. Install the required Python packages:
pip install -r requirements.txt


4. Update the `config.ini` file with your MySQL database connection details.

5. Run the Python script:
python hospital_management.py


## Configuration

Update the `config.ini` file with your MySQL database connection details:
[mysql]
host = localhost
user = your_username
password = your_password
database = hospital


## Usage

Follow the prompts in the command-line interface to interact with the hospital management system.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


