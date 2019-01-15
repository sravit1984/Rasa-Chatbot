# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

# me == the sender's email address
# you == the recipient's email address

msg = EmailMessage()
msg.set_content("Sample Email")
msg['Subject'] = 'Foodie Restaurat Search'
msg['From'] = 'Foodie'
msg['To'] = 'sample.gmail.com'

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()