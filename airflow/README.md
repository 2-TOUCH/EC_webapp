# Getting Started with Apache Airflow

Apache Airflow is an open-source platform used for orchestrating, scheduling, and monitoring workflows, allowing you to automate complex data pipelines and tasks. 

EcoCAR is currently using Airflow job to monitor the certain request status of new members, then Airflow job would trigger the task at certain to send email or do other things.

## Using Google Form's API - for retrieving Google Form responses

### a) Create authentication (service account)
Please refer to this web tutorial to create a service account: https://medium.com/frudens-engineering/how-to-use-google-forms-and-other-apis-easily-from-filemaker-using-google-service-account-261a4b27c5b8

### b) After you have created a service account (for example: test-google-form-api@pristine-valve-397622.iam.gserviceaccount.com):
1. Download the credential key json file -> rename it **Google-ServiceAccounts-Credentials.json** -> Place it in the **credentials** folder (**ecocar_webapp/airflow/credentials/**)
2. Go to your Google Drive -> right click the Google Form -> Share -> Share the **editor** access to your service account.

## Using Jira Admin account to create Jira user for approved users
***NOTE! If we decide to contine using the "ecocar-atlassian" account, then we can simply skip this part because everything was developed and tested using that admin account***
Please refer to this web tutorial to create needed credentials: https://developer.atlassian.com/cloud/jira/platform/jira-rest-api-oauth-authentication/
Most importantly, we need a file called something like **jira_privatekey.pcks8** and the **access token** created
***NOTE! If we decide to contine using the "ecocar-atlassian" account, then we can simply skip this part because everything was developed and tested using that admin account***

## .env file
Since we are sending email out, we require an email account.
If you are using gmail, you can create APP Password to test/debug

After you have created an temporary password, you can create a .env file.
Under **ecocar_webapp/airflow/dags** directory  
create a .env file, just name it **.env**  
write  
```bash  
EMAIL_USERNAME=your_email_address_that_you_want_to_send_email_out
EMAIL_PASSWORD=the_App_Password_you_created_before
CONSUMER_KEY=OauthKey
ACCESS_TOKEN=3BHf5cScWtBpErBNA8MI4K6v3TE2ZiUI
refer_to_this_link_https://developer.atlassian.com/cloud/jira/platform/jira-rest-api-oauth-authentication/.
GOOGLE_INTEREST_FORM_ID=the_form_id_that_you_can_obtain_from_the_url_address
GOOGLE_TEAM_ROSTER_FORM_ID=the_form_id_that_you_can_obtain_from_the_url_address
COM=use_your_own_email_address_for_testing - (ecocar-comm@ucdavis.edu)
DEI=use_your_own_email_address_for_testing - (ecocar-dei@ucdavis.edu)
PM=use_your_own_email_address_for_testing - (ecocar-pm@ucdavis.edu)
CAV=use_your_own_email_address_for_testing - (ecocar-cav@ucdavis.edu)
SDI=use_your_own_email_address_for_testing - (ecocar-sdi@ucdavis.edu)
PCM=use_your_own_email_address_for_testing - (ecocar-pcm@ucdavis.edu)
USER_MANAGER_EMAIL=person_who_is_in_charge_of_creating_Confluence_and_Bitbucket_accounts_after_Jira_account_has_been_created.
DOCUSIGN_INTEGRATION_KEY=fd21a8fe-ba3f-4f95-a973-1ebcbd004c17
DOCUSIGN_BASE_PATH=https://demo.docusign.net/restapi
DOCUSIGN_USER_ID=a83cb6c9-bb32-4bc2-825a-37b7a30fba15
DOCUSIGN_API_ACCOUNT_ID=a9ab76b0-4fe9-4f65-aa20-f091bad8969c
DOCUSIGN_PHOTO_WAIVER_TEMPLATE_ID=7600bb70-d0ce-4b64-85e1-af6c908b77cb
DOCUSIGN_UPA_TEMPLATE_ID=
``` 

## After everything is up, go to the webserver of Airflow  
```bash  
  http://localhost:8080/  
```  
The user and password are currently default as  
```bash  
User: airflow 
Password: airflow
``` 
  
## After you have logged into the webserver, you will need configure the connection with the Postgres database  
1. At the top bar, hover on **Admin**.  
2. Click on **Connections** in the drop-down menu.  
3. Click the button **next to Action** to add a new record.
```bash    
  Connection Id: postgres_ecocar
  Connection Type: Postgres
  Host: host.docker.internal
  Schema: ecocar
  Login: postgres
  Password: docker
  Port: 5432
```  
4. Then click "Save".  
  
  
## Go back to home page  
Unpause the dags tasks.  
Then the Airflow will be running. 

## Manually trigger the task
Airflow job usually set to trigger the task at certain time.
However, you can manual trigger the task to see if everything works as expected.

# For Deployment

REMEMBER to replace all "localhost:5000" in the backend request link with our ultimate **deployed backend url** !!!
REMEMBER to edit the **email content** to include the ultimate online url to our frontend app
REMEMBER to include all subteam's email addresses in .env file under **airflow/dags** !!!