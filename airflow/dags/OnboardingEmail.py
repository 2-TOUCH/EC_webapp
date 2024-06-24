# Modules for Airflow job
from airflow import DAG
from datetime import datetime, timedelta

# Mdoules for PostgreSQL connection and operation
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator

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

# function that updates "isOnboardingSent" column to be true after onboarding email has been sent
def update_isOnboardingSent(emailaddress):
    """
    function that updates "isOnboardingSent" column to be true after onboarding email has been sent

    Args:
        emailaddress (string): email address of the person who has been sent the welcome onboarding email
    """    
    update_request = """
        UPDATE "EcocarAccessRequests"
        SET "isOnboardingSent" = true
        WHERE emailaddress = %s
        """
    
    # Database connection
    pg_hook = PostgresHook(
        postgres_conn_id="postgres_ecocar", 
        schema="ecocar"
    )
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(update_request, (emailaddress))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

    print(f"SUCCESS: Updated \"isOnboardingSent\" to be TRUE for {emailaddress}.")

# function that sends email to new member
def send_onboarding_email(receiver):
    """
    This function operates the ultimate email sending
    procedure using SMTP (Simple Mail Transfer Protocol).
    It takes string input "receiver" which is a email 
    address, this input would then be used by SMTP sending 
    email to.

    Args:
        receiver (string): one single email address of new member
        who are approved by IT Dept. to access VPN.
    """
    # loading .env file
    # remember to create a .env file under "dags" folder to initialize the following two variables.
    # load the .env file in the same current directory (which is "dags")
    load_dotenv()
    sender_email = os.getenv(
        "EMAIL_USERNAME" # Email address to send welcome onboarding emails out
    )
    sender_password = os.getenv(
        "EMAIL_PASSWORD" # Email account password to log in
    )
    
    try:
        # define python email.message basic info
        msg = EmailMessage()
        msg['Subject'] = "[EcoCAR] Welcome Aboard EcoCAR!!!"
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
                                    <h1> Welcome to EcoCAR!</h1>
                                </td>
                        </table>
                        <table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 30px 30px 30px 60px;">
                            <tr>
                                <td>
                                    <h2>Welcome to your new team!</h2>
                                    <p>Thank you for taking the initiative to join the EcoCAR team at UC Davis. You are almost a member, here is a few steps that you must do to join us officially:</p>
                                    
                                    <hr>
                                    
                                    <p><b>VPN Instructions:</b></p>
                                    <p>Here is a step-by-step guide on how to connect to the College of Engineering FortiClient VPN - <a href="https://kb.ucdavis.edu/?id=9438">Click here to download</a></p>
                                    <hr>
                                    <p><b>Another Interest Form?</b></p>
                                    <p>Yes! Last form, trust me. Fill out all the necessary information then make sure everything is correct since you can only submit it once, and then press submit. Confirm that you have successfully submitted the form as well. Here is the link to the form - <a href="LINK_TO_INTEREST_FORM">EcoCAR UC Davis Onboarding form</a></p>
                                    <hr>
                                    <p><b>UPA Signature (Docusign):</b></p>
                                    <p>You will eventually receive an email from Docusign (do NOT ignore this):</p>
                                    <ul>
                                    <li>Once you receive it, <b>press</b> the <b>“Review Document”</b> button, which should take you to a Docusign document where you must sign in certain places.</li>
                                    <li><b>Create</b> your own signature then have your initial ready</li>
                                    <li><b>Press</b> the <b>“Sign”</b> and <b>“Next”</b> buttons to sign in the documents.</li>
                                    <li>Eventually the <b>“Finish”</b> button will appear, once you press that, the document will be submitted.</li>
                                    <li><b>Confirm</b> that you have signed it by <b>checking your email</b>, where you should see a confirmation email for signing the document.</li>
                                    </ul>
                                    
                                    <hr>
                                        
                                    <p><b>Photo Waiver (Docusign):</b></p>
                                    <p>You will also receive a second email for Docusign so keep an eye out for this one as well! Follow the same instructions, which is:</p>
                                    <ul>
                                    <li><b>Press</b> the <b>“Review Document”</b> button</li>
                                    <li>(If you already have your signature created then skip this step) <b>Create</b> your own signature then have your initial ready to use</li>
                                    <li><b>Press</b> the <b>“Sign”</b> and <b>“Next”</b> buttons to sign in the documents.</li>
                                    <li>Once that is done, <b>press</b> the <b>“Finish”</b> button to submit the document</li>
                                    <li>Make sure to <b>confirm</b> your submission by <b>checking your email</b> for a confirmation email!</li>
                                    </ul>
                                    
                                    <hr>
                                        
                                    <p><b>Jira/Confluence:</b></p>
                                    <p>Once we have approved you, you will receive two separate emails about <b>Jira and Confluence invitation</b>. 
                                    <ul>
                                    <li>Turn on the <b>EcoCAR's VPN</b></li>
                                    <li>Click the <b>invitation link</b> in your mailbox</li>
                                    <li>follow the instruction such as <b>resetting the password</b> to finish Jira/Confluence account setup</li>
                                    <li>Try to <b>log into</b> your Jira and Confluence website to see if you have the access to EcoCAR</li>
                                    </ul>
                                        
                                    <hr>
                                        
                                    <h2>
                                        <b>Stay Connected!</b>
                                    </h2>
                                    <p>Once these steps are done, you are now ready to be part of the EcoCAR family! Here is how you can stay connected with your new family:</p>
                                    <p><b>Join Slack!!!!</b></p>
                                    <p>Talk with your team and make new friends (or enemies). Here is the link to join: <a href="https://join.slack.com/t/ecocarucdavis/shared_invite/zt-24sefedb4-1CiWRrGAJ6QnBY~oeVBVCA">Link to Slack</a></p>
                                    <p><b>Google Calendar</b></p>
                                    <p>Keep track of your meetings or attend one you are interested in! Click the link to view: <a href="https://calendar.google.com/calendar/u/1/embed?src=c_4ffm51g5dgr88jqbk8f0csmgek@group.calendar.google.com&ctz=America/Los_Angeles&csspa=1">Google Calendar Link</a></p>
                                    
                                    <hr>
                                    
                                    <h2>Thank you!</h2>
                                    <p>Once again thank you for joining EcoCAR UC Davis!</p>
                        
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

        print(f"Success - Welcome onboarding email sent to {receiver}!!!") # this print can be found in the log of task in 8080 webserver
        update_isOnboardingSent(receiver)
    
    except Exception as exception:
        print("Failure :( !!!") # this print can be found in the log of task in 8080 webserver
        print(exception) # this print can be found in the log of task in 8080 webserver

# function using hooks to retrieve data from PostgreSQL
def get_approved_email_list():
    """
    This function runs PostgreSQL command to retrieve
    email address of new member who is approved VPN 
    access by IT Dept. from "EcocarAccessRequests" table.
    This function runs Postgres hook to retrieve a list
    of email addresses.
    For each email address, "send(...)" function is called
    to operate the sending process.
    """  

    # Postgres command to search all data that has been approved by IT Dept.
    request = """
        SELECT emailaddress
        FROM "EcocarAccessRequests"
        WHERE "isOnboardingSent" = false
        AND teamleadapprove = 'APPROVED'
        AND itapprove = 'APPROVED'
        AND "EcocarAccessRequests"."createdAt"
        BETWEEN NOW() - interval '7 day' 
        AND NOW()
    """
    
    # Database connection
    pg_hook = PostgresHook(
        postgres_conn_id="postgres_ecocar", 
        schema="ecocar"
    )
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(request)
    email_list = cursor.fetchall()

    # for each email retrieved from all approved emails
    for email in email_list:
        # call the function to send email one by one
        send_onboarding_email(email)

with DAG(
    dag_id="Send_Onboarding_Email",
    default_args=default_args,
    start_date=datetime(2023, 4, 10),
    schedule_interval="0 19 * * *",  # daily, see https://crontab.guru/ for more detailed formats.
    catchup=False,
) as dag:
    send_onboarding_email_task = PythonOperator(
        task_id="send_email_task", 
        python_callable=get_approved_email_list
    )

send_onboarding_email_task