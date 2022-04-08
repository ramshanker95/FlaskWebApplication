# Module for handling OTP email and Mobile/Phone

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint

print("Import Ho gya hai")
# Define Credentials
class OtpHandler:
    def __init__(self) -> None:
        self.username = "kumtable378@gmail.com"
        self.password = "22111976bjk"
        # Note: Use Less Secure Gamil Account For Email Server.

    # OTS: Online Tutoreial Services
    def send_OTP(self, to, subject="OTS", text="Welcome TO OTS"):
        self.msg = MIMEMultipart()
        self.msg["From"] = self.username
        self.msg["To"]  = to
        self.msg["Subject"] = subject
        self.msg.attach(MIMEText(text, 'plain')) #  for Send Plain Text Message.
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        try:
            self.server.starttls()
            self.server.login(self.username, self.password)
            text = self.msg.as_string()
            self.server.sendmail(self.username, to, text)
            self.server.quit()
            print("MAzza Aa gya OTP Bhej Kar, apna Email Check Karo.")
            return True
        except Exception as E:
            print("Error in Send OTP: ", E)
            print("Bhai Sahi Se codding Kiya karo, Error Aa rahi hai.")
            return False


# Time For Testing
if __name__ == "__main__":
    print("Bhai Main Me Hai")
    Email = OtpHandler()
    # Generate Random OTP
    OTP = randint(1000, 9999)
    reciever = "vramshanker23@gmail.com"
    Subject = "OTS | Reset Passsword OTP"
    Message = "Mis Richa Mishra \n Your one Time OTP For Online Tutorial Service Is: {}  ,\n Please Do not Share With Anyone., Or Ek or bat apana password yad rakha karo Because OTP bhejne me Server ko thoda load Padta HAI. so Next Time Se Yad Rakha karo. Nahi to block Kar denge. Thank you to bolna hi padhta hai formalities jo hai. hahahhahaahh......".format(OTP)
    Email.send_OTP(reciever, Subject, Message)
    print("Kam Ho gya.")
