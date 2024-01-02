import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import glob
import json
from pathlib import Path
import getpass
from tqdm import tqdm

def send_email(sender_email, sender_password, recipient_email, subject, body, attachment_file_path):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body+'\n', 'plain'))

    attachment = open(attachment_file_path, "rb")
    filename = Path(attachment_file_path).name

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{filename}"')

    message.attach(part)

    # Connect to the SMTP server using SSL
    with smtplib.SMTP_SSL('mail.tecnico.ulisboa.pt', 465) as server:
        # Log in to the email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())


def sender():
    sender_email = input('Please introduce your email: ')
    sender_password = getpass.getpass(prompt='Please introduce your password: ')

    #getting email list
    files = glob.glob('output/evaluation_reports/*.json')
    with open(files[0], 'r') as f:
        email_adresses = json.load(f)
    
    with open('config/email_text.txt', 'r') as f:
        lines = f.readlines()
        subject = lines[0]
        body = '\n'.join(lines[1:])

    print('Sending emails:')
    evaluation_reports = glob.glob('output/evaluation_reports/*.pdf')
    for path in tqdm(evaluation_reports):
        filename = Path(path).stem
        receiver = email_adresses[filename]
        send_email(sender_email, sender_password, receiver, subject, body, path)
    print('Done!')


if __name__ == '__main__':
    sender()
