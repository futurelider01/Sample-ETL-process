from exchangelib import Credentials, Account, Message, DELEGATE
from exchangelib.errors import UnauthorizedError
from core import config
import datetime


# Set your Outlook email credentials
outlook_email = config.SENDER
outlook_password = config.E_PASSWORD

# Set the recipient email address
recipient_email = config.RECIEVER

def log(text,table, error_text):
    with open(f'monitoring/monitoring_{datetime.datetime.now().date()}','a') as f:
        t=f"\n-----------------------------------------------\
                \nCould not send email. Check credentials, please.\nError: {text}\
                \n-----------------------------------------------\
                \nTable {table} failed.\nError text: {error_text}\n\n"
        f.write(t)
       
def create_message(table,error_text):
    # Create the email message
    subject = "Reporting failure"
    body = f"Table {table} failed.\nError text: {error_text}"
    to_recipient = recipient_email
    return (subject,body,to_recipient)


def send_mail(table, error_text, account):
    # Send the email
    subject,body,to_recipient=create_message(table, error_text)
    message = Message(account=account, subject=subject, body=body, to_recipients=[to_recipient])
    message.send()

def send(table, error_text):
    try:
        credentials = Credentials(outlook_email, outlook_password)
        acc = Account(outlook_email, credentials=credentials, autodiscover=True, access_type=DELEGATE)
        send_mail(table, error_text, acc=acc)
    except UnauthorizedError as e:
        log(e, table, error_text)
        


# Connect to the Outlook account

if __name__=='__main__':
    send('Table','error')

