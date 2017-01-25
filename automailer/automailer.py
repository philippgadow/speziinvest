import urllib
import xhtml2pdf.pisa as pisa
import time
import smtplib

# create pdf file

timestr = time.strftime("%Y%m%d")
path = "/var/www/html/reports/"
f = "report_" + timestr + ".pdf"
name = path + f

def convertURL(
            url="http://134.107.40.24/print.php",
            dest=name):
    
    pdf = pisa.CreatePDF(
                         urllib.urlopen(url),
                         file(dest, "wb")
                         )

convertURL()

# send mail to admin

sender = 'speziinvest@mail.de'
receivers = ['koehler@mpp.mpg.de','pgadow@mpp.mpg.de']

message = """From: Spezi Invest Report <speziinvest@mail.de>
To: Nicholas Koehler <koehler@mpp.mpg.de>
Subject: Spezi-Invest Report

Report abrufen unter 
"""

message += "http://134.107.40.24/reports/" + f

smtpObj = smtplib.SMTP('smtp.mail.de', 587)
smtpObj.starttls()
smtpObj.login("speziinvest@mail.de", "speziinvest_pwd")
smtpObj.sendmail(sender, receivers, message)
smtpObj.quit()
print "Successfully sent email"

