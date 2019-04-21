# Reading an excel file using Python
import xlrd
import sqlite3
import random
from faker import Faker
from mimesis.builtins import USASpecProvider
from mimesis import Person, Address, Datetime, Generic


fake_data = Faker()

generic = Generic('en')
generic.add_provider(USASpecProvider)
person = Person('en')
address = Address('en')

connection = sqlite3.connect('file:C:/Users/IT117/PycharmProjects/testData/'
                             'syntheticDataGenerator/database_faker.db?mode=rw', uri=True)

cursor = connection.cursor()
from array import array
# Give the location of the file
loc = ("../dataRule.xlsx")

# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

# For row 0 and column 0
sheet.cell_value(0, 0)
# print(sheet.row_values(0))

def get_headers(row_value):

    row = sheet.row_values(row_value)
    #print(row[1])
    return row


def update_qry_without_fk(i, update_value):
    cursor.execute('''UPDATE ''' + set_row_value.table_name + ''' SET ''' + set_row_value.table_fields +
                   ''' = ? where id=?''', (update_value, i))


def update_qry_with_fk(count):
    cursor.execute('''select distinct '''
                   + set_row_value.table_dependent_tbl_fields + ''' from ''' + set_row_value.table_dependent_tbl_name)

    col_values = cursor.fetchall()

    for value in col_values:
        set_value = value[0]
        print(set_value)
        for i in range(count):
            random_id = random.randint(1, 99)
            cursor.execute('''UPDATE ''' + set_row_value.table_dependent_tbl_name + ''' SET '''
                           + set_row_value.table_dependent_tbl_fields + ''' = ? where '''
                           + set_row_value.table_dependent_tbl_fields + '''=?''', (random_id, set_value))
            cursor.execute(
                '''UPDATE ''' + set_row_value.table_name + ''' SET ''' + set_row_value.table_fields +
                ''' = ? where ''' + set_row_value.table_dependent_tbl_fields + '''=?''', (random_id, set_value))


def update_street_address():
    print("update street called here")
    if set_row_value.table_foreign_key == 'N':
        for i in range(set_row_value.record_count):
            # This will create a new street address using mimesis.
            update_street_address.street_address = address.address()
            # print(set_row_value.table_fields)
            update_qry_without_fk(i, update_street_address.street_address)

    return "Update succesfull"


def update_plan_id():
    print("Plan id called")
    if set_row_value.table_foreign_key == 'Y':
        cursor.execute('''select count(*) from ''' + set_row_value.table_dependent_tbl_name)
        rows = cursor.fetchall()
        for row in rows:
            set_row_value.record_count = row[0]

        update_qry_with_fk(set_row_value.record_count)


def perform_masking(masking_code):
    # Function to convert number into string
    # Switcher is dictionary data type here
    if masking_code == 101:
        update_street_address()

    if masking_code == 102:
        update_plan_id()


def set_row_value(noOfRows):
    strt_frm_norow= 0
    for i in range(noOfRows):
        if i > strt_frm_norow:
            row = sheet.row_values(i)
            set_row_value.table_name = row[0]
            set_row_value.table_fields = row[1]
            set_row_value.table_foreign_key = row[2]
            set_row_value.table_dependent_tbl_name = row[3]
            set_row_value.table_dependent_tbl_fields = row[4]
            set_row_value.table_masking_code = row[5]
            print(set_row_value.table_name, set_row_value.table_fields,
                  set_row_value.table_foreign_key, set_row_value.table_dependent_tbl_name,
                  set_row_value.table_dependent_tbl_fields, set_row_value.table_masking_code)
            cursor.execute('''select count(*) from '''+set_row_value.table_name)
            rows = cursor.fetchall()
            for row in rows:
                set_row_value.record_count = row[0]
                print(set_row_value.record_count)

            # for i in range(set_row_value.record_count):
            perform_masking(set_row_value.table_masking_code)


set_row_value(sheet.nrows)

# print(set_row_value.table_name)
# print(get_headers(0))





# for i in range(1):
#
#     row = sheet.row_values(1)
#     print(row[1])
#     for cell in row:
#         print (cell)

# for i in cursor.execute('SELECT first_name, middle_name, last_name, address, email FROM users'):
#     print(i)

connection.commit()
connection.close()
