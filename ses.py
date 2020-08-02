import sys
import boto3
from botocore.exceptions import ClientError

MYEMAIL = open('email.txt').readlines()[0].strip()

def send_email(subject, text, recipient=MYEMAIL):

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "AWSEC2 <{0}>".format(MYEMAIL)

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = recipient

    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = subject

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = text
            
    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
        # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


if __name__=="__main__":
    subject = ""
    if len(sys.argv)>1:
        subject = sys.argv[1]
    send_email(subject, sys.stdin.read())
