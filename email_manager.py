import smtplib
import os


# Credencials -------------------------------
email_send = "marco.a.ponce.p@gmail.com"  # "bretrayal_nights@yahoo.com"
password_not = "jfkgsrpzyozggrml"  # "coyotas515"
email_to = "maarco.app98@gmail.com"

class New_Client:


    def send_email(self, message):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            try:
                connection.login(user=email_send, password=password_not)
                connection.sendmail(
                    from_addr=email_send,
                    to_addrs=email_to,
                    msg=message
                )
            except Exception as e:
                # Print any error messages to stdout
                print(e)
