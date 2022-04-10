# import email
# import sqlite3
# from random import randint

# mydb = sqlite3.connect("./database/user_details.sqlite", check_same_thread=False)


import psycopg2
from config import config

mydb = None
try:
    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    mydb = psycopg2.connect(**params)
    
    # create a cursor
    mycursor = mydb.cursor()
except Exception as e:
    print("In db_134: Error: ", e)
# Create table For User Information
def Create_table():
    sql_command = '''CREATE TABLE user_details (id SERIAL PRIMARY KEY,
                    fname TEXT,
                    lname TEXT,
                    email TEXT,
                    mobile TEXT UNIQUE,
                    location TEXT,
                    password TEXT
                    )'''

    mycursor.execute(sql_command)
    mydb.commit()


'''
CREATE TABLE fruits(
   id SERIAL PRIMARY KEY,
   name VARCHAR NOT NULL
);
'''
# Creating Table For Forgot Passsword. [New Code]
def Create_forgot():
    sql_command = '''CREATE TABLE reset_password_v2 (id SERIAL PRIMARY KEY,
                    email TEXT UNIQUE, mobile TEXT UNIQUE, E_OTP TEXT, M_OTP TEXT, E_status TEXT, 
                    M_status TEXT,time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )'''
    mycursor.execute(sql_command)
    mydb.commit()

# check Email In Forgot Table [New Code]
def check_user(email_id):
    try:
        sql_commad = f"SELECT mobile FROM reset_password_v2 WHERE email='{email_id}'"
        mycursor.execute(sql_commad)
        temp_flag = mycursor.fetchone()
        if temp_flag is not None:
            return True
        else:
            return False
    except Exception as E:
        print("Galat hai kuch: ", E)
        return False

# verify otp
def verify_otp(email_iid, rx_otp):
    sql_command = f"SELECT E_OTP FROM reset_password_v2 WHERE email='{email_iid}' AND E_status='0'"
    mycursor.execute(sql_command)
    tres = mycursor.fetchone()
    print(tres)
    if tres is not None:
        return Update_otp_status(email_iid) if str(rx_otp) in tres[0] else False
    else:
        return False

# Uupdate OTP's and Status [New Code]
def Update_Otp(email_id, email_otp, mobile_otp, email_status, mobile_satus):
    try:
        sql_command = f"UPDATE reset_password_v2 SET E_OTP='{email_otp}', M_OTP='{mobile_otp}', E_status='{email_status}', M_status='{mobile_satus}' WHERE email='{email_id}'"
        mycursor.execute(sql_command)
        mydb.commit()
        print("Update Ho gya IN Line 51.")
        return True
    except Exception as E:
        print("error Hai 54: ", E)
        return False

# Function to Insert reset credentials. [New Code]
def InserOTP(email_id, mobile, email_otp, mobile_otp, email_status, mobile_status):
    try:
        if not check_user(email_id):
            sql_commad = f"INSERT INTO reset_password_v2 (email, mobile, E_OTP, M_OTP, E_status, M_status) VALUES('{email_id}', '{mobile}', '{email_otp}', '{mobile_otp}', '{email_status}', '{mobile_status}');"
            mycursor.execute(sql_commad)
            mydb.commit()
            print("Data INsert kar Diya hu.")
            return True
        else:
            return Update_Otp(email_id, email_otp, mobile_otp, email_status, mobile_status)

    except Exception as E:
        print("Bhai Kuch Galat hua hia, Esko Dekho: ", E)
        return False

# Abhi Status UPDATE Karna hai, OTP KA, Abhi hum only email ka karenge. [New Code]
def Update_otp_status(email_id, status='1'):
    try:
        if check_user(email_id):
            sql_command = f"UPDATE reset_password_v2 SET E_status='{status}' WHERE email='{email_id}'"
            mycursor.execute(sql_command)
            mydb.commit()
            print("Status Change Ho gya hai.")
            return True
        else:
            print("User Nahi Hai DatabasE ke forgot_password_v2 me")
            return False
    except Exception as E:
        print("Bhai Kuch Galat hai, mujhe ye lagta hi: ", E)
        return False

# Insert Data In Database
def InsertData(fname, lname, email, mobile, location, password):
    try:
        sql_command = f"INSERT INTO user_details (fname, lname, email, mobile, location, password) VALUES ('{fname}', '{lname}', '{email}', '{mobile}', '{location}', '{password}');"
        mycursor.execute(sql_command)
        mydb.commit() # Use to Save Change In Database
        return True
    except Exception as E:
        print("Error in database line 27: ", E)
        return False

# get all table data
def get_all():
    sql_command = "SELECT * FROM user_details"
    mycursor.execute(sql_command)
    temp = mycursor.fetchall()
    print(temp)

# Get Eamil and Pasword From Database
def getCredentials(email_id):
    try:
        sql_command = f"SELECT email, password FROM user_details WHERE email='{email_id}'"
        print(sql_command)
        mycursor.execute(sql_command)
        temp = mycursor.fetchone()
        if temp is not None:
            return temp
        else:
            return None

    except Exception as E:
        print("Error in Line 37: ", E)
        return False

# update password
def Update_password(emailID, password):
    mycursor.execute(f"UPDATE user_details SET password='{password}' WHERE email='{emailID}'")
    mydb.commit()
    return True

# check User Registration 
def identify_user(email_id, mobile):
    try:
        sql_command = f"SELECT fname FROM user_details WHERE email='{email_id}' AND mobile='{mobile}'"
        mycursor.execute(sql_command)
        an = mycursor.fetchone()
        if an is not None:
            return [True, an]
        else:
            return [False, "NA"]
    except Exception as E:
        print("Kuchh erro rhai identify me. :", E)
        return [False, E]

if __name__ == "__main__":
    print(mydb)
    # InsertData("Nitish Kumar", "Sahrma", "nitish.ns377@gmail.com",  "7631256855", "Motihari Bihar", "admin123")
    # print(getCredentials("nitish.ns378@gmail.com"))
    print(get_all())
    # [New Code]
    # InserOTP("vramshanker23@gmail.com", "7631256855", f"{randint(1000, 9999)}", f"{randint(1000, 9999)}", "0", "0")
    # Update_otp_status("vramshanker23@gmail.com", "1")
    # print(check_user("vramshanker23@gmail.com"))
    # print(verify_otp("vramshanker23@gmail.com", 2683))
    # Update_password("vramshanker23@gmail.com", "2683")
    
    # delt = "DELETE FROM user_details WHERE id=4"
    # mycursor.execute(delt)
    # mydb.commit()
    
    mydb.close()
    
    

