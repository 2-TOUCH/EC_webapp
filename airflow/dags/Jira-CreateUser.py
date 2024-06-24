# Modules for Airflow job
from airflow import DAG
from datetime import datetime, timedelta

# Mdoules for PostgreSQL connection and operation
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator

# Modules for Jira API Auth and request
from requests_oauthlib import OAuth1
from oauthlib.oauth1 import SIGNATURE_RSA
import requests
import json

# Modules for loading .env
from dotenv import load_dotenv
import os

# Modules for sending emails
import smtplib

# Modules for reading a PKCS #8 encoded private key
from cryptography.hazmat.primitives import serialization

"""
**Note**: 
In Jira, OAuth consumers are represented by application links. 
Application links use OAuth with RSA-SHA1 signing for authentication. 
This means that a private key is used to sign requests rather than 
the OAuth token secret/consumer secret.
"""
# loading .env file
# remember to create a .env file under "dags" folder to initialize the following variables.
# load the .env file in the same current directory (which is "dags")
load_dotenv()
consumer_key = os.getenv("CONSUMER_KEY")
access_token = os.getenv("ACCESS_TOKEN")

# Reading private key file
# Specify the path to your PKCS #8 private key file
private_key_path = "/opt/airflow/credentials/jira_privatekey.pcks8"
# Open and read the private key file
with open(private_key_path, "rb") as key_file:
    private_key_bytes = key_file.read()
# Deserialize and load the private key
private_key = serialization.load_pem_private_key(
    private_key_bytes,
    password=None  # If the key is not encrypted
)

# define owner
# initializing basic setting for Airflow
default_args = {
    "owner": "PM Software Team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# function that update "isOnboardingComplete" after Jira has created a new account
def update_isOnboardingComplete(emailAddress):
    """
    This function would update "isOnboardingComplete" column corresponding to
    the given email address after the new Jira account has been successfully created

    Args:
        emailAddress (string): email address of the newly created account
    """ 

    update_request = """
        UPDATE "EcocarAccessRequests"
        SET "isOnboardingComplete" = true
        WHERE emailaddress = %s
        """
    
    # Database connection
    pg_hook = PostgresHook(
        postgres_conn_id="postgres_ecocar", 
        schema="ecocar"
    )
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(update_request, (emailAddress))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

    print(f"SUCCESS: Updated \"isOnboardingComplete\" to be TRUE for {emailAddress}.")

# function that send notification email to teamlead to create Confluence and/or Bitbucket account(s)
def send_notification_email(userName, emailAddress, firstName, lastName):
    """
    This function operates the email sending
    procedure using SMTP (Simple Mail Transfer Protocol).
    It takes string input "receiver" which is a email 
    address, this input would then be used by SMTP sending 
    email to.

    Args:
        userName (string): username of the newly created Jira account.

        emailAddress (string): email address of the newly created Jira account.

        firstName (string): first name of the new member of the newly created Jira account.

        lastName (string): first name of the new member of the newly created Jira account.
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
    user_manager_email = os.getenv(
        "USER_MANAGER_EMAIL"
    )

    try:
        # email SMTP config
        smtp = smtplib.SMTP(
            "smtp.gmail.com", 
            587
        )
        smtp.starttls()
        # email account login
        smtp.login(
            sender_email, 
            sender_password
        )
        # define and initialize email contents
        subject = "[EcoCAR] NOTIFICATION: New Jira Account Created!"
        body_text = f"""
            A new Jira account has been created for:\n
            First name: "{firstName}"\n
            Last name: "{lastName}"\n
            Email address: "{emailAddress}"\n
            Username: "{userName}"\n

            Please refer to these information to create Confluence and/or Bitbucket account(s) accordingly. 
        """
        message = "Subject: {}\n\n{}".format(subject, body_text)
        # send!
        smtp.sendmail(
            sender_email, 
            user_manager_email, 
            message
        )
        print(f"Success - Notification email sent to {user_manager_email}!!!") # this print can be found in the log of task in 8080 webserver
    
    except Exception as exception:
        print("Failure :( !!!") # this print can be found in the log of task in 8080 webserver
        print(exception) # this print can be found in the log of task in 8080 webserver

# function that creates new jira account and sends notification email to new member
def create_jira_user(userName, emailAddress, firstName, lastName):
    """
    This function operates Jira REST API to create Jira account
    for new onboarding members. Their email addresses, firstnames,
    and lastnames are retrieved from the "EcocarAccessRequests" 
    database, then this infomation will then be used to create a
    new Jira account to use Jira software.

    Args:
        name (string): substring extracted from emaill address.
        Everything before "@" would be extracted. This substring is
        then used as "username" for creating a new user.

        email_address (string): one single email address of new member
        who are approved by IT Dept. They are to be created using
        Jira softwares.

        first (string): first name of the new member corresponding to
        the email address being accessed to VPN.

        last (string): last name of the new member corresponding to
        the email address being accessed to VPN.
    """

    # url to Jira REST API to create user
    url = "https://ecocar-jira.engineering.ucdavis.edu/rest/api/2/user"

    # authentication info of the admin Jira account to operate the API
    oauth_rsa = OAuth1(
        client_key=consumer_key,
        resource_owner_key=access_token,
        signature_method=SIGNATURE_RSA,
        rsa_key=private_key,
        signature_type="auth_header",
    )

    # request headers
    headers = {
        "Accept": "application/json", 
        "Content-Type": "application/json"
    }

    # request body
    body_json = json.dumps(
        {
            "name": userName,
            "displayName": firstName + " " + lastName,
            "emailAddress": emailAddress,
            "notification": "true"
        }
    )

    response = requests.request(
        "POST", 
        url=url, 
        data=body_json, 
        headers=headers, 
        auth=oauth_rsa
    )

    if response.status_code == 200 or response.status_code == 201:
        # Jira API call was successful, so we can proceed
        # print(
        #     json.dumps(
        #         json.loads(response.text), 
        #         sort_keys=True, 
        #         indent=4, 
        #         separators=(",", ": ")
        #     )
        # )

        # Call the functions only if the Jira API call was successful
        send_notification_email(userName, emailAddress, firstName, lastName)
        update_isOnboardingComplete(emailAddress)
    else:
        # Jira API call was not successful, handle the error
        print(f"Jira API call failed with status code: {response.status_code}")
        print(f"Error message: {response.text}")

# function using hooks to retrieve data from PostgreSQL
def get_approved_member_list():
    """
    This function runs PostgreSQL command to retrieve
    email address, firstname, and lastname of new member
    who is approved VPN access by IT Dept. from 
    "EcocarAccessRequests" table. This function runs 
    Postgres hook to retrieve a list of email addresses, 
    firstnames, and lastnames in tuple object. Such as,
    [(user1@email.com, firstname1, lastname1), (user2@email.com, firstname2, lastname2), ...].
    For each approved user, "create(...)" function is called
    to create new user to Jira softwares.
    """
    # Postgres command to search all data that has been approved by IT Dept.
    request = """
        SELECT emailaddress, firstname, lastname
        FROM "EcocarAccessRequests"
        WHERE teamleadapprove = 'APPROVED'
        AND itapprove = 'APPROVED'
        AND "isOnboardingSent" = true
        AND "isPhotoWaiverSigned" = true
        AND "isUPASigned" = true
        AND "isTeamRosterFilled" = true 
        AND "isOnboardingComplete" = false
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
    email_first_last_list = cursor.fetchall()
    # for each email retrieved from all approved emails
    for email_first_last_tuple in email_first_last_list:
        # call the function to send email one by one
        email_address_tuple = email_first_last_tuple[0]
        firstname_tuple = email_first_last_tuple[1]
        lastname_tuple = email_first_last_tuple[2]
        username = email_address_tuple.split("@")[0]
        create_jira_user(username, email_address_tuple, firstname_tuple, lastname_tuple)

with DAG(
    dag_id="Jira-Create_User_and_Send_Invite_Link",
    default_args=default_args,
    start_date=datetime(2023, 4, 10),
    schedule_interval="0 22 * * *",  # daily, see https://crontab.guru/ for more detailed formats.
    catchup=False,
) as dag:
    create_jira_user_task = PythonOperator(
        task_id="create_jira_user_task", 
        python_callable=get_approved_member_list
    )

create_jira_user_task