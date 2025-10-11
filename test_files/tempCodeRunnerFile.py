import os
import shutil
from yourdb.yourdb import YourDB
from yourdb.utils import register_class

DB_NAME = "company_db"
DB_DIR = f"{DB_NAME}.yourdb"

# Clean up previous database runs for a fresh start
if os.path.exists(DB_DIR):
    shutil.rmtree(DB_DIR)

# 1. Define the data model
@register_class
class Employee:
    def __init__(self, emp_id, name, department, salary):
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.salary = salary

    def __repr__(self):
        return f"Employee(id={self.emp_id}, name='{self.name}', dept='{self.department}', salary=${self.salary})"

# 2. Initialize the database
db = YourDB(DB_NAME)

# 3. Define the schema
employee_schema = {
    'primary_key': 'emp_id',
    'emp_id': "int",
    'name': "str",
    'department': "str",
    'salary': "int",
    'indexes': ['department'] # Index on department for fast lookups
}

# 4. Create the entity
db.create_entity("employees", employee_schema)

# 5. Insert sample data
print("--> Inserting employees...")
db.insert_into("employees", Employee(emp_id=101, name="Alice", department="Engineering", salary=90000))
db.insert_into("employees", Employee(emp_id=102, name="Bob", department="Sales", salary=75000))
db.insert_into("employees", Employee(emp_id=103, name="Charlie", department="Engineering", salary=110000))
db.insert_into("employees", Employee(emp_id=104, name="Diana", department="Sales", salary=82000))

# 5.5. Verify all data was inserted
print("\n--> Verifying all data in the database...")
all_employees = db.select_from("employees")
print(f"Found {len(all_employees)} employees total.")
for emp in all_employees:
    print(emp)

# 6. Perform an advanced query
print("\n--> Finding all employees with a salary greater than $80,000...")
high_earners = db.select_from(
    "employees",
    filter_dict={'salary': {'$gt': 80000}}
)

print("High earners:")
for emp in high_earners:
    print(emp)

# 7. Perform a combined query (index-assisted)
print("\n--> Finding all 'Engineering' employees with an ID greater than 101...")
senior_engineers = db.select_from(
    "employees",
    filter_dict={'department': 'Engineering', 'emp_id': {'$gt': 101}}
)

print("Senior engineers:")
for emp in senior_engineers:
    print(emp)

