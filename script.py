from bs4 import BeautifulSoup
import requests
import re
import smtplib




def send_email():
    EMAIL_ADDRESS = ""
    PASSWORD = ""
    subject = "Test alert"
    msg = "the page content has changed"

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(EMAIL_ADDRESS,EMAIL_ADDRESS, message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")





url="https://www.msg.com/madison-square-garden/faqs"

data=requests.get(url).text
soup=BeautifulSoup(data,features="html.parser")

# find the image
img=soup.find('img',class_='_3JakF')
img=img['src']
img = img[28 : : ]


# find the main content
description=soup.find('div',class_='K5mMP')
description=description.text

# find the FAQS
faqs=soup.find('div',class_='_2YHWX')
faqs=faqs.text

data=img+description+faqs
data = re.sub('\s{2,}', '|', data.strip())

# print(data)


with open('content_trace.txt','r+') as file:
    first = file.read(1)
    if not first:
        file.write(' '+data)

        file.close()
    else:
        print("comparing data...........................")
        file_data=file.read()

        # file.close()
        if list(file_data) == list(data):
            print("content remain same")

        else:
            file.truncate(0)
            file.write(data)
            print("sending email....................")
            send_email()
