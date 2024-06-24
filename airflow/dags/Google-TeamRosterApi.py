# Modules for Airflow job
from airflow import DAG
from datetime import datetime, timedelta

# Mdoules for PostgreSQL connection and operation
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator

# Modules for loading .env
from dotenv import load_dotenv
import os

# Modules for using Google Api
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Modules for viewing json data (Google API's response)
import json

# define owner
# initializing basic setting for Airflow
default_args = {
    "owner": "PM Software Team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# function using Postgres Hook to update "isTeamRosterFilled" column to true
def update_isTeamRosterFilled(emailAddress):
    """
    This function would run Postgres Hook to update "isTeamRosterFilled"
    column in the "EcocarAccessRequests" table to be true since this Google
    Form has been filled by this member (emailAddress).

    Args:
        emailAddress (string): this is used to locate the user with the same
        email address in the "EcocarAccessRequests" table.
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
        SELECT COUNT(*) FROM "EcocarAccessRequests" WHERE "emailaddress" = %s
    """
    update_sql = """
        UPDATE "EcocarAccessRequests"
        SET "isTeamRosterFilled" = true
        WHERE emailaddress = %s
    """
    # Check if the email even exists in the database
    cursor.execute(check_sql, (emailAddress,))
    email_exists = cursor.fetchone()[0] > 0

    if email_exists:
        # Execute the INSERT statement
        cursor.execute(update_sql, (emailAddress,))
        print(f"Updated isTeamRosterFilled to be TRUE for {emailAddress} in EcocarAccessRequests.")
        
    else:
        print(f"ERROR:Email {emailAddress} does NOT exists in the EcocarAccessRequests!")
        
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# function using Postgres Hook to connect and execute inserting operation
def insert_answers(
        firstName, 
        lastName, 
        phoneNumber, 
        subTeam, 
        leadershipRole, 
        degree, 
        major, 
        classType, 
        graduationTerm, 
        lookEmployment, 
        employmentBegins, 
        gender, 
        raceEthnicity, 
        countryCitizenship, 
        tShirtSize, 
        linkedInURL, 
        emailAddress
    ):
    """
    This function runs PostgreSQL command to insert the selected values into the database "ecocar" table "EcocarTeamRosters".

    This function also checks the duplicate case according to the given email address. It checks if the email address is
    already stored in this database table. If it's already contained, it would skip inserting the data.

    Args:
        firstName (string): first name of the person filling out the Google Form

        lastName (string): last name of the person filling out the Google Form

        phoneNumber (string): phone number of the person filling out the Google Form

        subTeam (string): the chosen sub team that the person interested in joining

        leadershipRole (string): leadership role of the person e.x. team member

        degree (string): degree of the person e.x. bachelor

        major (string): major of the person e.x. computer science

        classType (string): class of the person e.x. senior

        graduationTerm (string): the term of the person expect to graduate e.x. spring2024

        lookEmployment (string): if the person is looking for employment e.x. yes: full-time

        employmentBegins (string): when does the person expect to get employed e.x. Summer 2024

        gender (string): gender of the person e.x. female

        raceEthnicity (string): race of the person e.x. Hispanic

        countryCitizenship (string): nationality of the person e.x. China

        tShirtSize (string): perferred t shirt size e.x. Male L

        linkedInURL (string): the link to the person's LinkedIn

        emailAddress (string): the email address collected by Google Form
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
        SELECT COUNT(*) FROM "EcocarTeamRosters" WHERE "emailAddress" = %s
    """
    insert_sql = """
        INSERT INTO "EcocarTeamRosters" (
            "firstName", 
            "lastName", 
            "emailAddress", 
            "phoneNumber", 
            "subTeam", 
            "leadershipRole", 
            degree,
            major,
            "classType",
            "graduationTerm",
            "lookEmployment",
            "employmentBegins",
            gender,
            "raceEthnicity",
            "countryCitizenship",
            "tShirtSize",
            "linkedInURL",
            "createdAt", 
            "updatedAt"
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW());
    """

    # Check if the email already exists in the database
    cursor.execute(check_sql, (emailAddress,))
    email_exists = cursor.fetchone()[0] > 0

    if email_exists:
        print(f"Email {emailAddress} already exists in the database. Skipping insertion.")
    else:
        # Execute the INSERT statement
        cursor.execute(
            insert_sql, (
                firstName,
                lastName,
                emailAddress,
                phoneNumber,
                subTeam,
                leadershipRole,
                degree,
                major,
                classType,
                graduationTerm,
                lookEmployment,
                employmentBegins,
                gender,
                raceEthnicity,
                countryCitizenship,
                tShirtSize,
                linkedInURL
            )
        )

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        
        print(f"Inserted data for respondent {emailAddress} into the EcocarTeamRosters.")
    
        update_isTeamRosterFilled(emailAddress)

# function extracting essential values from a dump of json data
def extract_answers(result):
    """
    This function extracts all answers from the complete json data retrieved from the Google Api request.

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

            # # Initialize an array to store answers for each question ID
            # question_answers_arr = []

            # # Iterate through the question IDs
            # for question_id in answers:
            #     answer_value = answers[question_id]['textAnswers']['answers'][0]['value']
            #     question_answers_arr.append(answer_value)
            
            # print(question_answers_arr)
            # # extract answer to each question
            # tShirtSize = question_answers_arr[0]
            # degree = question_answers_arr[1]
            # employmentBegins = question_answers_arr[2]
            # lastName = question_answers_arr[3]
            # raceEthnicity = question_answers_arr[4]
            # leadershipRole = question_answers_arr[5]
            # lookEmployment = question_answers_arr[6]
            # isSubscribedCalendar = question_answers_arr[7]
            # emergencyPhone = question_answers_arr[8]
            # subTeam = question_answers_arr[9]
            # countryCitizenship = question_answers_arr[10]
            # graduationTerm = question_answers_arr[11]
            # emergencyName = question_answers_arr[12]
            # isJoinedSlack = question_answers_arr[13]
            # linkedInURL = question_answers_arr[14]
            # emergencyEmail = question_answers_arr[15]
            # phoneNumber = question_answers_arr[16]
            # firstName = question_answers_arr[17]
            # classType = question_answers_arr[18]
            # major = question_answers_arr[19]
            # gender = question_answers_arr[20]
            # hobby = question_answers_arr[21]
            # emailAddress = question_answers_arr[22]

            # Access answers through question ID:
            tShirtSize = answers["553390bc"]['textAnswers']['answers'][0]['value']
            degree = answers["4e2eb0c6"]['textAnswers']['answers'][0]['value']
            employmentBegins = answers["1b3caa76"]['textAnswers']['answers'][0]['value']
            lastName = answers["6973f2e7"]['textAnswers']['answers'][0]['value']
            raceEthnicity = answers["5bd2b616"]['textAnswers']['answers'][0]['value']
            leadershipRole = answers["00eeb762"]['textAnswers']['answers'][0]['value']
            lookEmployment = answers["62cc2a5d"]['textAnswers']['answers'][0]['value']
            isSubscribedCalendar = answers["5ab0b964"]['textAnswers']['answers'][0]['value']
            emergencyPhone = answers["1ed4db1e"]['textAnswers']['answers'][0]['value']
            subTeam = answers["598bfb27"]['textAnswers']['answers'][0]['value']
            countryCitizenship = answers["2055c7e8"]['textAnswers']['answers'][0]['value']
            graduationTerm = answers["7a99424c"]['textAnswers']['answers'][0]['value']
            emergencyName = answers["5cbe10b8"]['textAnswers']['answers'][0]['value']
            isJoinedSlack = answers["28bc0649"]['textAnswers']['answers'][0]['value']
            linkedInURL = answers["21b1200d"]['textAnswers']['answers'][0]['value']
            emergencyEmail = answers["02365c39"]['textAnswers']['answers'][0]['value']
            phoneNumber = answers["2093e25b"]['textAnswers']['answers'][0]['value']
            firstName = answers["3b6a417d"]['textAnswers']['answers'][0]['value']
            classType = answers["75924da9"]['textAnswers']['answers'][0]['value']
            major = answers["4984a77a"]['textAnswers']['answers'][0]['value']
            gender = answers["2ca4781e"]['textAnswers']['answers'][0]['value']
            hobby = answers["66625e28"]['textAnswers']['answers'][0]['value']
            emailAddress = answers["69b86b6d"]['textAnswers']['answers'][0]['value']
            
            print(tShirtSize)
            print(degree)
            print(employmentBegins)
            print(lastName)
            print(raceEthnicity)
            print(leadershipRole)
            print(lookEmployment)
            print(isSubscribedCalendar)
            print(emergencyPhone)
            print(subTeam)
            print(countryCitizenship)
            print(graduationTerm)
            print(emergencyName)
            print(isJoinedSlack)
            print(linkedInURL)
            print(emergencyEmail)
            print(phoneNumber)
            print(firstName)
            print(classType)
            print(major)
            print(gender)
            print(hobby)
            print(emailAddress)

            insert_answers(firstName, lastName, phoneNumber, subTeam, leadershipRole, degree, major, classType, graduationTerm, lookEmployment, employmentBegins, gender, raceEthnicity, countryCitizenship, tShirtSize, linkedInURL, respondent_email)
        
        else:
            print(f"Skipping inserting {respondent_email} because it was submitted at least two days ago.")

# function running Google Form Api to retrieve all responses from the specific Google Form
def run_google_team_roster_api():
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
        'GOOGLE_TEAM_ROSTER_FORM_ID'
    )

    # List responses
    response = service.forms().responses().list(formId=form_id).execute()
    # print(json.dumps(response, indent=4))
    extract_answers(response)

with DAG(
    dag_id="Google-Pull_Team_Roster_to_PostgreSQL",
    default_args=default_args,
    start_date=datetime(2023, 4, 10),
    schedule_interval="0 18 * * *",  # daily at 18:00 (6 p.m.), see https://crontab.guru/ for more detailed formats.
    catchup=False,
) as dag:
    pull_google_team_roster_task = PythonOperator(
        task_id="google_team_roster_to_postgresqk_task", 
        python_callable=run_google_team_roster_api
    )

pull_google_team_roster_task
