# Modules for Airflow job
from airflow import DAG
from datetime import datetime, timedelta

# Mdoules for PostgreSQL connection and operation
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator

# Modules for loading .env files
from dotenv import load_dotenv
import os

# Modules for sending emails
import smtplib
from email.message import EmailMessage

# define owner
# initializing basic setting for Airflow
default_args = {
    "owner": "PM Software Team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# function that sends reminder email to new member to ask them to fill in team roster page
def send_reminder_email(receiver):
    """
    This function operates the email sending
    procedure using SMTP (Simple Mail Transfer Protocol).
    It takes string input "receiver" which is a email 
    address, this input would then be used by SMTP sending 
    email to.

    Args:
        receiver (string): one single email address of new member
        who needs to be sent a reminder email to sign DocuSign.
    """
    # loading .env file
    # remember to create a .env file under "dags" folder to initialize the following two variables.
    # load the .env file in the same current directory (which is "dags")
    load_dotenv()
    sender_email = os.getenv(
        "EMAIL_USERNAME" # Email address to send emails out
    )
    sender_password = os.getenv(
        "EMAIL_PASSWORD" # Email account password to log in
    )
    
    try:
        # define python email.message basic info
        msg = EmailMessage()
        msg['Subject'] = "[EcoCAR] Reminder: Please Remember to Sign Photo Waiver!!!"
        msg['From'] = sender_email
        msg['To'] = receiver
        msg.set_content('''
            <!DOCTYPE html>
            <html>
                <head>
                    <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Lato|Lato:i,b,bi">
                    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style type="text/css">
                        h1{font-size:56px}
                        h2{font-size:28px;font-weight:900}
                        p{font-weight:100}
                        td{vertical-align:top}
                        #email{margin:auto;width:600px;background-color:#fff}
                    </style>
                </head>
                <body style="background-color: #DBE1F1; width: 100%; font-family:Lato, sans-serif; font-size:18px;">
                    <div id="email">
                        <table role="presentation" width="100%">
                            <tr>
                                <td bgcolor="#022851" align="center" style="color: #FFBF00;">
                                    <h1> EcoCAR Reminder</h1>
                                </td>
                        </table>
                        <table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 30px 30px 30px 60px;">
                            <tr>
                                <td>
                                    <h2>Please sign the Photo Waiver DocuSign ASAP!!!</h2>
                                    <p>Our record shows that you haven't signed the Photo Waiver DocuSign.</p>
                                    <p>Please sign it ASAP to process your EcoCAR onboarding application.</p>
                                    <p>If you can't find the Photo Waiver DocuSign request email, please immediately contact Project Management Team (ecocar-pm@ucdavis.edu).</p>
                                    
                                    <h2>Thank you!!!</h2>
                        
                                    <hr style="border: 1px solid #ccc; margin: 10px 0;">
                        
                                    <div id="emailSignature" style="font-family: Lato, sans-serif; font-size: 14px; color: #333;"> 
                                        <p>EcoCAR UC Davis</p>
                                        <p>https://ecocar.ucdavis.edu </p>
                                        <p>1 Shields Ave, Davis, CA 95616</p>
                                        <p>EcoCAR@ucdavis.edu</p>
                                    </div>
                        
                                    <hr style="border: 1px solid #ccc; margin: 10px 0;">
                    
                                </td>
                            </tr>
                        </table>
                    </div>
                </body>
            </html>
        ''', subtype='html')

        # email SMTP config, email sender login, send message!
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        print(f"Success - Reminder email sent to {receiver}!!!") # this print can be found in the log of task in 8080 webserver
    
    except Exception as exception:
        print("Failure :( !!!") # this print can be found in the log of task in 8080 webserver
        print(exception) # this print can be found in the log of task in 8080 webserver
        

# function check if "isPhotoWaiverSigned" is true after the PhotoWaiverSentID has been filled out
def check_if_photo_waiver_is_signed():
    """
    This function checks the stage where the DocuSign has been sent but it's not signed yet.
    If that's the case, it will call the function to send a reminder email.
    """    

    # Database connection
    pg_hook = PostgresHook(
        postgres_conn_id="postgres_ecocar", 
        schema="ecocar"
    )
    connection = pg_hook.get_conn()
    cursor = connection.cursor()

    sent_but_not_signed_request = """
        SELECT emailaddress
        FROM "EcocarAccessRequests"
        WHERE teamleadapprove = 'APPROVED'
        AND itapprove = 'APPROVED'
        AND "isOnboardingSent" = true
        AND "PhotoWaiverSentID" <> 'NOT YET SENT'
        AND "isPhotoWaiverSigned" = FALSE
    """
    cursor.execute(sent_but_not_signed_request)
    email_list = [row[0] for row in cursor.fetchall()]
    for email in email_list:
        send_reminder_email(email)
    
    # Commit the changes and close the connection
    connection.commit()
    connection.close()

with DAG(
    dag_id="DocuSign-Check_if_Photo_Waiver_is_Signed",
    default_args=default_args,
    start_date=datetime(2023, 4, 10),
    schedule_interval="0 21 * * *",  # daily, see https://crontab.guru/ for more detailed formats.
    catchup=False,
) as dag:
    check_if_photo_waiver_signed_task = PythonOperator(
        task_id="check_if_photo_waiver_is_signed_task", 
        python_callable=check_if_photo_waiver_is_signed,
        provide_context=True,  # Add this line to pass context to the function
    )

check_if_photo_waiver_signed_task