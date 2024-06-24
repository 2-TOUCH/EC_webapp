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
        who are approved by IT Dept. to access VPN.
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
        msg['Subject'] = "[EcoCAR] Reminder: Please Fill out EcoCAR's Team Roster Form"
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
                                    <h1> EcoCAR Reminder!</h1>
                                </td>
                        </table>
                        <table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 30px 30px 30px 60px;">
                            <tr>
                                <td>
                                    <h2>Please fill out the EcoCAR's Team Roster Form ASAP!!!</h2>
                                    <p>Our record shows that you haven't filled out the EcoCAR's Team Roster Form. </p>
                                    <p>Before we give you access to Jira, Confluence, and Bitbucket software, we need you to fill out the form for us.</p>
                                    <p>Please refer to the link below to finish the Team Roster Form: <a href="https://forms.gle/oTvAAGtzSP928Cet5">https://forms.gle/oTvAAGtzSP928Cet5</a></p>
                                    
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
        
        print(f"Success - Reminder email sent to {receiver}!!!") # this print can be found in the log of task in 8080 webserver
    
    except Exception as exception:
        print("Failure :( !!!") # this print can be found in the log of task in 8080 webserver
        print(exception) # this print can be found in the log of task in 8080 webserver
        

# function check if "EcocarTeamRosters" contains a email address that is same as the email address in "EcocarAccessRequests"
def check_if_team_roster_filled():
    """
    This function retrieves email addresses from "EcocarAccessRequests",
    checks if they exist in "EcocarTeamRosters", and updates the
    "isTeamRosterFilled" column accordingly.
    However, if the "isTeamRosterFilled" remains false by the end of the day,
    then send a reminder email to the member.
    """ 
    # Database connection
    pg_hook = PostgresHook(
        postgres_conn_id="postgres_ecocar", 
        schema="ecocar"
    )
    # Step 1: Retrieve email addresses from "EcocarAccessRequests"
    select_all_email_request = """
        SELECT emailaddress FROM "EcocarAccessRequests"
    """
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(select_all_email_request)
    email_list = [row[0] for row in cursor.fetchall()]

    # Step 2: Check if each email exists in "EcocarTeamRosters" and update "isTeamRosterFilled"
    update_isTeamRosterFilled_request = """
        UPDATE "EcocarAccessRequests"
        SET "isTeamRosterFilled" = true
        WHERE emailaddress = %s and exists (
	        SELECT 1
	        FROM "EcocarTeamRosters" 
	        WHERE "emailAddress" = %s
        )
    """
    for email in email_list:
        cursor.execute(update_isTeamRosterFilled_request, (email, email))

    # Step 3: If the isTeamRosterFilled remain false, send reminder email for new team member
    select_isTeamRosterFilled_request = """
        SELECT "isTeamRosterFilled" 
        FROM "EcocarAccessRequests" 
        WHERE emailaddress = %s
        AND teamleadapprove = 'APPROVED'
        AND itapprove = 'APPROVED'
        AND "isOnboardingSent" = true
    """
    for email in email_list:
        cursor.execute(select_isTeamRosterFilled_request, (email,))
        is_team_roster_filled = cursor.fetchone()[0]
        if not is_team_roster_filled: # if isTeamRosterFilled == FALSE (not fill out the form yet)
            send_reminder_email(email)
    
    # Commit the changes and close the connection
    connection.commit()
    connection.close()

with DAG(
    dag_id="Google-Check_if_Team_Roster_is_Filled",
    default_args=default_args,
    start_date=datetime(2023, 4, 10),
    schedule_interval="0 21 * * *",  # daily, see https://crontab.guru/ for more detailed formats.
    catchup=False,
) as dag:
    check_if_team_roster_filled_task = PythonOperator(
        task_id="check_if_team_roster_filled_task", 
        python_callable=check_if_team_roster_filled,
        provide_context=True,  # Add this line to pass context to the function
    )

check_if_team_roster_filled_task