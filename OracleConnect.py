import cx_Oracle
from datetime import date
from dateutil.parser import parser
from faker import Faker
from mimesis.builtins import USASpecProvider
from mimesis import Person, Address, Datetime, Generic
from mimesis.enums import Gender

# Connect as user "QA" with password "root" to the "QA" service running on this computer.
connection = cx_Oracle.connect("QA", "root", "localhost/orcl")

cursor = connection.cursor()


fake_data = Faker()

generic = Generic('en')
generic.add_provider(USASpecProvider)
person = Person('en')
address = Address('en')
date1 = Datetime('en')


# cursor.execute('''CREATE TABLE IF NOT EXISTS users (first_name text, last_name text, middle_name text,
#                 address text, email text, ssn number, phn number, company text)''')
#
# for i in range(10):
#     cursor.execute('INSERT INTO users VALUES (:first_name, :last_name, :middle_name, :address, :email, :ssn, :phn, '
#                    ':company)',
#             {'first_name': fake_data.prefix() + fake_data.first_name(), 'middle_name': fake_data.first_name_male(),
#              'last_name': fake_data.last_name(), 'address': fake_data.address(), 'email': fake_data.email(),
#              'ssn': fake_data.ssn(), 'phn': fake_data.phone_number(), 'company': fake_data.company()})

# how_many_users_to_generate = [(100), (20, 'M', 25-30), (20, 'M', 31-65), ]
cursor.execute('''CREATE TABLE benefit_plan
             (
                  benefit_id INTEGER,
                  benefit_plan_name varchar(20) NOT NULL,
                  assigned_plan_id integer NOT NULL,
                  health_Plan_Deductible integer,
                  Max_OOP_Yearly integer,
                  Co_Pay_Per_Visit integer,
                  Additional_Benefit varchar(20),
                  Lab_Service_Covered varchar(20),
                  Mental_Health_Covered varchar(20),
                  Skilled_Nursing_Facility_Covered varchar(20),
                  constraint benefit_id_pk PRIMARY KEY(benefit_id))''')

data_benefit_plan = [(101, 'HP_101', 10, 0, 1000, 20, 'Not covered', 'No', 'Yes', 'Yes'),
                     (102, 'HP_102', 20, 200, 1000, 0, 'X-Ray', 'Yes', 'Yes', 'Yes'),
                     (103, 'HP_103', 30, 500, 2400, 35, 'X-Ray', 'Yes', 'No', 'Yes'),
                     (104, 'HP_104', 40, 500, 300, 35, 'Lab MRI', 'Yes', 'Yes', 'No')]

for row in data_benefit_plan:
    cursor.execute("""INSERT INTO benefit_plan (benefit_id,
                    benefit_plan_name, assigned_plan_id, health_Plan_Deductible,
                    Max_OOP_Yearly, Co_Pay_Per_Visit, Additional_Benefit,
                    Lab_Service_Covered, Mental_Health_Covered, Skilled_Nursing_Facility_Covered) 
                     Values (:0, :1, :2, :3, :4, :5, :6, :7, :8, :9)""", row)
    

cursor.execute('''CREATE TABLE plan_details
             (
                  Health_Plan_Id INTEGER,
                  Plan_Name varchar(20) NOT NULL,
                  Health_Plan_Type varchar(10) NOT NULL,
                  Start_Date datetime,
                  End_Date datetime,
                  Organization varchar(20),
                  Plan_Active_Status varchar(10),
                  benefit_id INTEGER,
                  Premium INTEGER,
                  Deductible_Amt_Required varchar(20),
                  constraint Health_Plan_Id_pk PRIMARY KEY(Health_Plan_Id),
                  Constraint fk_benefit FOREIGN KEY (benefit_id) 
                  REFERENCES benefit_plan(benefit_id))''')

# Create a object for plan detail page
data_plan_details = [
                        (10, 'Plan_1', 'C1', '1917-09-15', '2018-09-14', 'Newscape', 'Inactive', 101, 450, 'Yes'),
                        (20, 'Plan_2', 'G1', '2018-07-29', '2019-07-28', 'Medicare', 'Active', 102, 550, 'Yes'),
                        (30, 'Plan_3', 'C1', '2018-12-24', '2019-12-23', 'Newscape', 'Active', 103, 145, 'Yes'),
                        (40, 'Plan_4', 'I1', '2018-08-01', '2019-07-31', 'Newscape', 'Active', 104, 250, 'No')]

for row in data_plan_details:
    cursor.execute("""INSERT INTO plan_details (Health_Plan_Id,
                    Plan_Name, Health_Plan_Type, Start_Date,
                    End_Date, Organization, Plan_Active_Status, benefit_id, Premium, Deductible_Amt_Required)
                     Values (:0, :1, :2, :3, :4, :5, :6, :7, :8, :9)""", row)

connection.commit()

connection.close()

