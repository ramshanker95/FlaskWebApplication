from flask import Flask, render_template, render_template_string, url_for, request, session, redirect, g
from numpy import require
from db import *
from forgot_pass import *
from random import randint
from flask_session import Session

global Subject, Message

# Create A Flask App
app = Flask(__name__)
otp_sender = OtpHandler()
Subject = "OTS | Reset Passsword OTP"
E_OTP = randint(1000, 9999)

# Session Configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# set Secret Key 
app.config['SECRET_KEY'] = 'nitish378' 

def get_msg(Name, E_OTP):
    return "Hello  {} \n Your one Time OTP For Online Tutorial Service Is: {}  ,\n Please Do not Share With Anyone.".format(Name, E_OTP)

# Create Route for Login page
@app.route("/", methods=["POST", "GET"])
def index():
    print(">>>>>", session.get("user_id"))
    if session.get("user_id"):
        return render_template("home.html")
    Loging_error = "Please Enter Credential to login Home page."
    print(session.get("_flashes"))
    print(request.method)
    print(request.form.get("userId"))
    if request.method == "POST":
        email = request.form["userId"]
        password = request.form["password"]
        user_data =  getCredentials(email)
        print("user Data: ", user_data)
        
        if user_data is not None:
            if user_data[1] == password:
                Loging_error = "Login Success Full"
                session["user_id"] = request.form.get("userId")
                return render_template("home.html")
            else:
                Loging_error = "Incorect Pasword!"
                render_template("index.html", Loging_error=Loging_error)
        else:
            Loging_error = "You are Not Registerd With Us"
            render_template("index.html", Loging_error=Loging_error)

    return render_template("index.html", Loging_error=Loging_error)


# URL For New Registration
@app.route("/register", methods=['POST', 'GET'])
def resister():
    register_error = ""
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        location = request.form["city"]
        password = request.form["password"]
        cpassword = request.form["confirm_pass"]
        
        temp = getCredentials(email)
        if temp is not None:
            register_error = "User All Ready Registerd, Please go to login"
            render_template("register.html", register_error=register_error)
            
        else:
            if password == cpassword:
                if InsertData(fname, lname, email, mobile, location, password):
                    register_error = "Succesfully Registered"
                    return redirect("/")
                else:
                    register_error = "Error Ocures! please try Again"
                    return render_template("register.html", register_error=register_error)
            else:
                register_error = "Password Is Not Matched!"
                return render_template("register.html", register_error=register_error)

    return render_template("register.html", register_error=register_error)


# Adding URL/Path For /learn_more
@app.route("/learn_more", methods=["GET", "POST"])
def learn_more():
    if not session.get("user_id"):
        return redirect("/")
    return render_template("/learn_more.html")


# URL for Forgot_password
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    forgot_error = ""
    if request.method == "POST":
        Email = request.form["userId"]
        mobile = request.form["mobile"]
        session["Email"] = Email
        session["mobile"] = mobile
        print(Email, mobile)
        check_user_ = identify_user(Email, mobile)
        print(check_user_)
        print(">>>>>>>>104>>>>>>>>: ",session)
        if check_user_[0]:
            Eotp = randint(1000, 9999)
            InserOTP(Email, mobile, f"{Eotp}", f"{Eotp}", "0", "0")
            otp_sender.send_OTP(Email, Subject, get_msg(check_user_[1], Eotp))
            print("Send")
            return render_template("otp.html")
        else:
            forgot_error = "Please Enter Vailed Credential"
            render_template("forgotpassword.html", forgot_error=forgot_error)

    return render_template("forgotpassword.html", forgot_error=forgot_error)


# Set Password
@app.route("/reset_password", methods=["GET", "POST"])
def Reset_password():
    reset_error = ""
    if request.method == "POST":
        RX_OTP = request.form["otp"]
        npass = request.form["npassword"]
        cpass = request.form["cpassword"]
        print(session.get("Eamil"), RX_OTP)
        print(">>>>>>>>>>127>>>>>>: ",session.get("Email"))
        if npass == cpass:
            if verify_otp(session.get("Email"), RX_OTP):
                Update_password(session.get("Email"), npass)
                return redirect("/")
            else:
                reset_error = "Invaild OTP"
                return render_template("otp.html", reset_error=reset_error)
        else:
            reset_error = "Password Do not Match"
            return render_template("otp.html", reset_error=reset_error)

    return render_template("otp.html")



# Set to run as Main Application
if __name__ =="__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

