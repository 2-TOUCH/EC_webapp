# Modules for Airflow job
from airflow import DAG
from datetime import datetime, timedelta

# Mdoules for PostgreSQL connection and operation
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator

# Modules for loading .env
from dotenv import load_dotenv
import os

# Modules for sending emails
import smtplib
from email.message import EmailMessage

# Modules for using Google Api
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Module for generating a token
import uuid

# Modules for viewing json data (Google API's response)
import json

# define owner
# initializing basic setting for Airflow
default_args = {
    "owner": "PM Software Team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# function that sends notification email to teamlead to ask them to check out the access request form to approve or reject
def send_teamlead_notification_email(receiver):
    """
    This function operates the email sending
    procedure using SMTP (Simple Mail Transfer Protocol).
    It takes string input "receiver" which is a email 
    address, this input would then be used by SMTP sending 
    email to.

    Args:
        receiver (string): one single email address of the specific subteam leader
    """
    # loading .env file
    # remember to create a .env file under "dags" folder to initialize the following two variables.
    # load the .env file in the same current directory (which is "dags")
    load_dotenv()
    sender_email = os.getenv(
        "EMAIL_USERNAME" # Email address to send welcome onboarding emails
    )
    sender_password = os.getenv(
        "EMAIL_PASSWORD" # Email account password to log in
    )
    
    try:
        # define python email.message basic info
        msg = EmailMessage()
        msg['Subject'] = "[EcoCAR] NEW INTERESTED MEMBER :) !!!"
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
                                    <h1> EcoCAR Notification!</h1>
                                </td>
                        </table>
                        <table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 30px 30px 30px 60px;">
                            <tr>
                                <td>
                                    <h2>NEW INTERESTED MEMBER :) !!!</h2>
                                    <p>What a lovely day! </p>
                                    <p>A new member who are interested in joining your team just fill out the Google Interest Form today.</p>
                                    <p>Please log into EcoCAR's onboarding web application: <a href="https://join-ecocar.ucdavis.edu/access-form">https://join-ecocar.ucdavis.edu/access-form</a></p>
                                    <p>Please review and approve this new member to aboard if everything is fine :)</p>
                                    
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
        
        print(f"Success - Notification email sent to teamlead: {receiver}!!!") # this print can be found in the log of task in 8080 webserver
    
    except Exception as exception:
        print("Failure :( !!!") # this print can be found in the log of task in 8080 webserver
        print(exception) # this print can be found in the log of task in 8080 webserver

# function selecting which subteam to send notification email to
def select_subteam_email(subteam):
    """
    This function operates the email sending
    procedure using SMTP (Simple Mail Transfer Protocol).
    It takes string input "receiver" which is a email 
    address, this input would then be used by SMTP sending 
    email to.

    Args:
        receiver (string): one single email address of the specific subteam leader
    """
    # loading .env file
    # remember to create a .env file under "dags" folder to initialize the following two variables.
    # load the .env file in the same current directory (which is "dags")
    load_dotenv()
    com_team_email = os.getenv(
        "COM" 
    )
    dei_team_email = os.getenv(
        "DEI" 
    )
    pm_team_email = os.getenv(
        "PM" 
    )
    cav_team_email = os.getenv(
        "CAV" 
    )
    sdi_team_email = os.getenv(
        "SDI" 
    )
    pcm_team_email = os.getenv(
        "PCM" 
    )

    if subteam == "Communications":
        send_teamlead_notification_email(com_team_email)
    elif subteam == "DEI":
        send_teamlead_notification_email(dei_team_email)
    elif subteam == "PM":
        send_teamlead_notification_email(pm_team_email)
    elif subteam == "CAV":
        send_teamlead_notification_email(cav_team_email)
    elif subteam == "SDI":
        send_teamlead_notification_email(sdi_team_email)
    elif subteam == "PCM":
        send_teamlead_notification_email(pcm_team_email)
    else:
        print("ERRPR: cannot find the corresponding subteam!")

# function using Postgres Hook to connect and execute inserting operation
def insert_answers(email, subteam, firstname, lastname):
    """
    This function runs PostgreSQL command to insert the given email address, chosen sub team, first name, and last name of
    the person who are interested in joining the EcoCAR team into the database "ecocar" table "EcocarAccessRequests".

    This function also checks the duplicate case according to the given email address. It checks if the email address is
    already stored in this database table. If it's already contained, it would skip inserting the data.

    Args:
        email (string): email address of the person who submitted the Google Form.

        subteam (string): the subteam of the person interested in joining

        firstname (string): first name of the person filling out the Google Form

        lastname (string): last name of the person filling out the Google Form
    """

    # Fetch the PostgreSQL connection
    hook = PostgresHook(
        postgres_conn_id="postgres_ecocar", 
        schema="ecocar"
    )
    conn = hook.get_conn()
    cursor = conn.cursor()

    # Define your SQL statements
    check_sql = """
        SELECT COUNT(*) FROM "EcocarAccessRequests" WHERE emailaddress = %s
    """
    insert_sql = """
        INSERT INTO "EcocarAccessRequests" (
            emailaddress, 
            subteam, 
            firstname, 
            lastname, 
            token, 
            "createdAt", 
            "updatedAt"
        )
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
    """

    # Check if the email already exists in the database
    cursor.execute(check_sql, (email,))
    email_exists = cursor.fetchone()[0] > 0

    if email_exists:
        print(f"Email {email} already exists in the database. Skipping insertion.")
    else:
        # Generate a token
        token = uuid.uuid4()

        # Execute the INSERT statement
        cursor.execute(
            insert_sql, (
                email, 
                subteam, 
                firstname, 
                lastname, 
                str(token)
            )
        )

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Print operation success feedback
        print(f"Inserted data for respondent {email} into the EcocarAccessRequests with token {token}.")
        select_subteam_email(subteam)

# function extracting essential values from a dump of json data
def extract_answers(result):
    """
    This function extracts email address, sub team, first name, last name from the complete
    json data retrieved from the Google Api request.

    This function also checks if the Google Form response is submitted two days ago. If the
    Google Form response is "old", then it would skip sending that data to insert into databse

    Then this selected data would be sent to insert into database table

    Args:
        result (string/json data): the response of the google api request. It contains
        the complete form of the json data.
    """

    # Define the maximum allowable response age in days
    max_response_age_days = 2

    for response in result['responses']:
        respondent_email = response['respondentEmail']

        # Convert createTime to a datetime object
        submission_time = datetime.strptime(response['createTime'], '%Y-%m-%dT%H:%M:%S.%fZ')

        # Calculate the time difference in days
        time_difference_days = (datetime.now() - submission_time).days

        # Check if the response was submitted within two days
        if time_difference_days <= max_response_age_days:
            # Access the answers for each response
            answers = response['answers']

            # Initialize an array to store answers for each question ID
            question_answers_arr = []

            # Iterate through the question IDs
            for question_id in answers:
                answer_value = answers[question_id]['textAnswers']['answers'][0]['value']
                question_answers_arr.append(answer_value)
            
            
            # extract answer to each question
            subteam = question_answers_arr[0]
            firstname = question_answers_arr[1]
            lastname = question_answers_arr[2]

            # Print or process the specific answers for this respondent
            print(f"Respondent Email: {respondent_email}")
            print(f"Sub Team: {subteam}")
            print(f"Firstname: {firstname}")
            print(f"Lastname: {lastname}")

            insert_answers(respondent_email, subteam, firstname, lastname)
        
        else:
            print(f"Skipping inserting {respondent_email} because it was submitted at least two days ago.")

# function running Google Form Api to retrieve all responses from the specific Google Form
def run_google_interest_form_api():
    """
    This function runs the Google Form Api to retrieve all response of the specific Google Form.

    The data retrieved from the Google Form would be sent to the function "extract_answer()" for
    extracting the desired values.
    """

    # Path to your service account JSON key file
    SERVICE_ACCOUNT_FILE = '/opt/airflow/credentials/Google-ServiceAccounts-Credentials.json'

    # Define the scopes you need
    SCOPES = ['https://www.googleapis.com/auth/forms.responses.readonly']

    # Authenticate using the service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Build the Google Forms API service
    service = build('forms', 'v1', credentials=credentials, cache_discovery=False)

    # Specify the form ID you want to access
    load_dotenv()
    form_id = os.getenv(
        'GOOGLE_INTEREST_FORM_ID'
    )

    # List responses
    response = service.forms().responses().list(formId=form_id).execute()
    # print(json.dumps(response, indent=4))
    extract_answers(response)

with DAG(
    dag_id="Google-Pull_Interest_to_PostgreSQL",
    default_args=default_args,
    start_date=datetime(2023, 4, 10),
    schedule_interval="0 17 * * *",  # daily at 17:00 (5 p.m.), see https://crontab.guru/ for more detailed formats.
    catchup=False,
) as dag:
    pull_google_interest_task = PythonOperator(
        task_id="google_interest_form_to_postgresqk_task", 
        python_callable=run_google_interest_form_api
    )

pull_google_interest_task
