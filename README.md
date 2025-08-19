# Voting-System-in-Python

# 🗳️ Election Management System (Python + MySQL)

This is a basic **Election Management System** project built using **Python** and **MySQL**.  
It is mainly created to demonstrate how to connect Python with a MySQL database.  

---

## ✨ Features
- Add voters (only if age is 18 or above)  
- Map voters to constituencies using their pincode  
- View voters in a specific constituency  
- Manage political parties and candidates  
- Cast votes and calculate winners  
- Store and manage data in MySQL database  

---

## 📂 Project Structure
- `voter_project.py` → Main Python program  
- `DDL.sql` → SQL script to create tables (Database Design Language)  
- `DML.sql` → SQL script with sample data (Database Manipulation Language)  
- `DCL.sql` → SQL script with privileges (Database Control Language)  
- `ER schema.png` → Schema of the database  
- `ER Diagram.png` → Database Entity-Relationship diagram  

---

## 🚀 How to Run
1. Install requirements:
   ```bash
   pip install mysql-connector-python

2.	Create the database and run SQL files:
	•	First run DDL.sql to create tables.
	•	Then run DML.sql to insert sample data.
	•	(Optional) Run DCL.sql to manage permissions.

3.	Update MySQL credentials in voter_project.py if needed:
   ```bash
   conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="yourdbname"
)

4.	Run the project:
    ```bash
    python voter_project.py


🎯 Purpose

This project is a mini DBMS project to practice:
	•	Python + MySQL connectivity
	•	SQL commands (DDL, DML, DCL)
	•	Database design with ER diagrams

👨‍💻 Author
Aradhya Bhagwat
