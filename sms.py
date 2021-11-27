from gpiozero import MotionSensor
import os
import smtplib
import io
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from twilio.rest import Client
from google.cloud import vision
from google.cloud.vision import types
    
def SendMail():
    fromaddr = "smitesh22@gmail.com"
    toaddr = "smitesh4250@gmail.com"
    msg = MIMEMultipart() 
      
    
    msg['From'] = fromaddr 
    msg['To'] = toaddr 
    msg['Subject'] = "Intrusion!!!" 
    body = "Alert Intrusion Detected!!"
    msg.attach(MIMEText(body, 'plain')) 
    filename = "abc.jpg"
    attachment = open("/home/pi/abc.jpg", "rb") 

    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p) 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
      
    s.login(fromaddr, "Howudoin?@123") 
    text = msg.as_string() 
    s.sendmail(fromaddr, toaddr, text) 
      
    
    s.quit()
    

pir = MotionSensor(23)

while True:
    pir.wait_for_motion()
    os.system("raspistill -o abc.jpg")
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        'abc.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    for label in labels:
        if str(label.description)=="Face":
            SendMail()
            os.system(“python3 sms.py”)
