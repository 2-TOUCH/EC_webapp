# Modules for Airflow job
from airflow import DAG
from datetime import datetime, timedelta

# Mdoules for PostgreSQL connection and operation
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator

# Modules for loading .env files
from dotenv import load_dotenv
import os

# Modules to use DocuSign API
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, TemplateRole

# define owner
# initializing basic setting for Airflow
default_args = {
    "owner": "PM Software Team",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# function updating "isUPASigned" to be true after the UPA DocuSign status has changed to be signed
def updateIsUPASigned(emailAddress):
    """
    This function updates the column "isUPASigned" according to the email address
    in the "EcocarAccessRequests" table after getting the status of DocuSign has been completed.

    Args:
        emailAddress (string): email address of the new member who has completed signing DocuSign
    """    

    # Fetch the PostgreSQL connection
    hook = PostgresHook(
        postgres_conn_id="postgres_ecocar", 
        schema="ecocar"
    )
    conn = hook.get_conn()
    cursor = conn.cursor()
    # Define your SQL statements
    update_sql = """
        UPDATE "EcocarAccessRequests"
        SET "isUPASigned" = true
        WHERE emailaddress = %s
    """
    # Check if the email even exists in the database
    cursor.execute(update_sql, (emailAddress))
    
    print(f"Updated \"isUPASigned\" to be TRUE for \"{emailAddress}\" in EcocarAccessRequests.")
        
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# function inserting DocuSign ID into the "UPASentID" column in "EcocarAccessRequests"
def insertDocuSignSentID(envelopeID, emailAddress):
    """
    Function insert the unique sent envelope ID into "EcocarAccessRequests" according to the email address
    after a DocuSign request has been sent to that email address.

    Args:
        envelopeID (string): envelop ID of UPA doc
        emailAddress (string): email address of the new member who signed the DocuSign
    """
    
    # Fetch the PostgreSQL connection
    hook = PostgresHook(
        postgres_conn_id="postgres_ecocar", 
        schema="ecocar"
    )
    conn = hook.get_conn()
    cursor = conn.cursor()
    # Define your SQL statements
    insert_sql = """
        UPDATE "EcocarAccessRequests"
        SET "UPASentID" = %s
        WHERE "emailaddress" = %s
    """
    # Check if the email even exists in the database
    cursor.execute(insert_sql, (envelopeID, emailAddress))
    
    print(f"Inserted UPASentID: \"{envelopeID}\" for \"{emailAddress}\" in EcocarAccessRequests.")
        
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# function that pass through the DocuSign auth
def getEnvelopesApi(access_token, base_path):
    """
    Function that get passed through the DocuSign API to configure auth

    Args:
        access_token (string): access token
        base_path (string): url to DocuSign API

    Returns:
        string: DocuSign's envelope API string
    """

    api_client = ApiClient()
    api_client.host = base_path

    api_client.set_default_header(header_name="Authorization", header_value=f"Bearer {access_token}")
    envelopes_api = EnvelopesApi(api_client)

    return envelopes_api

# function that obtains the token to run DocuSign API
def getToken(integration_key, base_path, user_id, private_key_file_location):
    """
    This function obtains the access token given integration key, base path,
    user id, and the privatekey file

    Args:
        integration_key (string): key of the integration
        base_path (string): url to DocuSign API
        user_id (string): id of the DocuSign account
        private_key_file_location (string): path to private key file

    Returns:
        string: access token to use DocuSign API
    """    

    api_client = ApiClient()
    api_client.host = base_path

    with open(private_key_file_location, 'r') as private_key_file:
        private_key_data = private_key_file.read()

    # consent_url = "https://account-d.docusign.com/oauth/auth?response_type=code&scope=signature%20impersonation&client_id=fd21a8fe-ba3f-4f95-a973-1ebcbd004c17&redirect_uri=http://localhost:5000/"

    jwt_token = api_client.request_jwt_user_token(
            client_id=integration_key,
            user_id=user_id,
            # oauth_host_name: needs change for production/deployment
            oauth_host_name="account-d.docusign.com",
            private_key_bytes=private_key_data,
            expires_in=3600,
            scopes=["signature"]
        )

    access_token = jwt_token.access_token

    return access_token

# function that makes the envelop with filling information such as email and name
def make_envelope(template_id, signer_email, signer_firstname, signer_lastname):
    """
    Creates envelope
    returns an envelope definition

    Args:
        template_id (string): id of the document template that needs to be filled in with basic info
        signer_email (string): the email address of the new onboarding member who needs to sign this doc
        signer_firstname (string): the first name of the new onboarding member who needs to sign this doc
        signer_lastname (string): the last name of the new onboarding member who needs to sign this doc

    Returns:
        string: the definition of envelope after the basic info has been filled in
    """

    # Create the envelope definition
    envelope_definition = EnvelopeDefinition(
        status = "sent", # requests that the envelope be created and sent.
        template_id = template_id
    )
    # Create template role elements to connect the signer and cc recipients
    # to the template
    signer = TemplateRole(
        email = signer_email,
        name = signer_firstname + " " + signer_lastname,
        role_name = 'signer')

    # Create a cc template role.
    # cc = TemplateRole(
    #     email = args['cc_email'],
    #     name = args['cc_name'],
    #     role_name = 'cc')

    # Add the TemplateRole objects to the envelope object
    # If cc needed, just add cc variable to the list
    # cc variable can be found above with comments
    # e.g.
    # envelope_definition.template_roles = [signer, cc]
    envelope_definition.template_roles = [signer]

    return envelope_definition

# function that execute the sending part, also retrieve the so-called envelope ID
def sendEnvelope(envelopes_api, envelope_definition, account_id):
    """
    Create the envelope request object
    Send the envelope

    Args:
        envelopes_api (string): api string of the envelopes
        envelope_definition (string): the definition of envelope after the basic info has been filled in
        account_id (string): account id generated from auth configuration

    Returns:
        string: id string of the envelopes being sent out
    """   

    results = envelopes_api.create_envelope(account_id, envelope_definition=envelope_definition)
    envelope_id = results.envelope_id
    return {'envelope_id': envelope_id}

# function that gets the status of the DocuSign, if it's been sent, or completed, or others
def getEnvelopeStatus(envelopes_api, account_id, envelope_id):
    """
    This function that gets the status of the DocuSign, if it's been sent, or completed, or others

    Args:
        envelopes_api (string): api string of the envelopes
        account_id (string): account id generated from auth configuration
        envelope_id (string): id string of the envelopes being sent out

    Returns:
        string: status of DocuSign completion such as 'sent', 'complete', and so on
    """

    results = envelopes_api.get_envelope(account_id, envelope_id)
    return results.status

# function gets DocuSign auths
def get_DocuSign_auth():
    load_dotenv()
    integration_key = os.getenv(
        "DOCUSIGN_INTEGRATION_KEY"
    )
    base_path = os.getenv(
        "DOCUSIGN_BASE_PATH"
    )
    user_id = os.getenv(
        "DOCUSIGN_USER_ID"
    )

    # Get Token
    # './private.key is the location of the 'private.key' file
    access_token = getToken(integration_key, base_path, user_id, '/opt/airflow/credentials/docusign_private.key')

    # Envelope API
    envelopes_api = getEnvelopesApi(access_token, base_path)
    
    return envelopes_api

# function that check the status of DocuSign, if completed, update "is...Signed" to be true
def check_DocuSign_status(email, envelopeID):
    """
    This function is designed to check specifically for
    those who have been sent DocuSign,
    if the status of the DocuSign has been "completed"
    then update the column "is...Signed" in "EcocarAccessRequests"
    to be true

    Args:
        email (string): email address of the member who is being checked
        envelopeID (_type_): the envelope ID of the DocuSign being sent out
        and needed to check the status
    """

    # environment    
    load_dotenv()
    api_account_id = os.getenv(
        "DOCUSIGN_API_ACCOUNT_ID"
    )

    # Envelope API auth
    envelopes_api = get_DocuSign_auth()

    # Get status
    status = getEnvelopeStatus(envelopes_api, api_account_id, envelopeID)
    print("Checked status:", status)
    if status == 'completed':
        updateIsUPASigned(emailAddress=email)
    
# function that run all other functions to execute DocuSign API
def send_DocuSign_doc(emailAddress, firstName, lastName):
    """
    This function is the main entry function to run DocuSign API, it calls the following functions to complete the whole process
    1. getToken & getEnvelopesApi function can be ran before the while loop. We only need to initialize it one time
    2. make_envelope & sendEnvelope function should be within the while loop since we want to send to multiple ppl.
    3. getEnvelopeStatus: use this to get the status of the docuSign document. Should run in while loop to get multiple documents
    4. getEnvelopeStatus: make sure to call getToken and getEnvelopesApi before using it. If you already initialized those before, than it is fine.

    Args:
        emailAddress (string): email address of the new onboarding member who need to sign the doc
        firstName (string): first name of the new onboarding member
        lastName (string): last name of the new onboarding member
    """
    
    load_dotenv()
    api_account_id = os.getenv(
        "DOCUSIGN_API_ACCOUNT_ID"
    )
    template_id = os.getenv(
        "DOCUSIGN_UPA_TEMPLATE_ID"
    )

    # Envelope API auth
    envelopes_api = get_DocuSign_auth()

    # Make Envelope
    # Inputs in order:
    # template_id -> docuSign document template id; get from .env file
    # email -> new members email address
    # name -> new members name
    envelope_definition = make_envelope(template_id, emailAddress, firstName, lastName)

    # Create and Send Envelope
    # res -> {'envelope_id': envelope_id} # returns a dictionary with value of envelope_id (the id of the document).
    res = sendEnvelope(envelopes_api, envelope_definition, api_account_id)

    # Get Envelopement Status
    # inputs in order: 
    # envelopes_api -> use getEnvelopesApi to get it
    # api_account_id -> get it from .env file
    # res['envelope_id'] -> the id of document (envelope_id)
    # status value: 'sent', 'complete', ... # there are more than these I think but docuSign API document does not have details on their website
    # 'sent': when the document is just sent
    # 'complete': when the signer signed the document
    # => use complete to check whether the user signed or not
    status = getEnvelopeStatus(envelopes_api, api_account_id, res['envelope_id'])
    print("status:", status)
    if status == 'sent':
        insertDocuSignSentID(res['envelope_id'], emailAddress)
    else:
        print("ERROR: DocuSign status is NOT \"sent\".")

# function using hooks to retrieve data from PostgreSQL
def get_approved_and_not_yet_sent_member_list():
    """
    This function runs PostgreSQL command to retrieve
    email address, firstname, and lastname of new member
    who is approved VPN access by IT Dept. from 
    "EcocarAccessRequests" table. So the next step is to send
    them DocuSign document. This would also select members who
    haven't been sent the DocuSign. This function runs 
    Postgres hook to retrieve a list of email addresses, 
    firstnames, and lastnames in tuple object. Such as,
    [(user1@email.com, firstname1, lastname1), (user2@email.com, firstname2, lastname2), ...].
    For each approved user, "create(...)" function is called
    to create new user to Jira softwares.
    """

    # Postgres command to search all data that has been approved by IT Dept.
    not_yet_sent_request = """
        SELECT emailaddress, firstname, lastname
        FROM "EcocarAccessRequests"
        WHERE teamleadapprove = 'APPROVED'
        AND itapprove = 'APPROVED'
        AND "isOnboardingSent" = true
        AND "UPASentID" = 'NOT YET SENT'
        AND "isUPASigned" = false
        AND "EcocarAccessRequests"."createdAt"
        BETWEEN NOW() - interval '7 day' 
        AND NOW()
    """

    get_status_request = """
        SELECT emailaddress, "UPASentID"
        FROM "EcocarAccessRequests"
        WHERE teamleadapprove = 'APPROVED'
        AND itapprove = 'APPROVED'
        AND "isOnboardingSent" = true
        AND "UPASentID" <> 'NOT YET SENT'
        AND "isUPASigned" = false
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
    
    # Step 1: send DocuSign to those who has not been sent
    cursor.execute(not_yet_sent_request)
    email_first_last_list = cursor.fetchall()
    # for each email retrieved from all approved emails
    for email_first_last_tuple in email_first_last_list:
        # call the function to send email one by one
        email_address1_tuple = email_first_last_tuple[0]
        firstname_tuple = email_first_last_tuple[1]
        lastname_tuple = email_first_last_tuple[2]
        send_DocuSign_doc(email_address1_tuple, firstname_tuple, lastname_tuple)
    
    # Step 2: check the status of those sent DocuSign, see if they are completed (signed)
    cursor.execute(get_status_request)
    email_envelopeID_list = cursor.fetchall()
    # for each email retrieved from all approved emails
    for email_envelopeID_tuple in email_envelopeID_list:
        # call the function to send email one by one
        email_address2_tuple = email_envelopeID_tuple[0]
        envelopID_tuple = email_envelopeID_tuple[1]
        check_DocuSign_status(email_address2_tuple, envelopID_tuple)

with DAG(
    dag_id="DocuSign-Send_UPA_Document",
    default_args=default_args,
    start_date=datetime(2023, 4, 10),
    schedule_interval="0 20 * * *",  # daily, see https://crontab.guru/ for more detailed formats.
    catchup=False,
) as dag:
    UPA_docusign_task = PythonOperator(
        task_id="docusign_send_UPA_task", 
        python_callable=get_approved_and_not_yet_sent_member_list
    )

UPA_docusign_task