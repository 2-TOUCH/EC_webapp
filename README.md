# EcoCAR Access Web Application

This application serves as a basis to fill out the interest form to joining ECOCAR and successfully onboard new team members

## Download the code from BitBucket

Clone the project

```bash
  git clone -b "branch name" https://ecocar-bitbucket.engineering.ucdavis.edu/scm/pm/ecocar_webapp.git
```

## Stuff needs to be done before running

### 1. Installing softwares - for using Docker and Database software
1. **Docker**  
2. **dBeaver** (or any other Database software that can use PostgreSQL)  


### 2. Create App Password - for sending email to IT Dept. and back to Requestors after IT Dept. has approved
1. Refer to this website: https://support.google.com/accounts/answer/185833?hl=en  
2. Log in with your desired gmail account to **send email out**  
3. Create a App Password  
4. This part may be confusing, don't hesitate to contact me, Lishen Liu, on slack!


### 3. Using Google Form's API - for retrieving Google Form responses

#### a) Create authentication (service account)
Please refer to this web tutorial to create a service account: https://medium.com/frudens-engineering/how-to-use-google-forms-and-other-apis-easily-from-filemaker-using-google-service-account-261a4b27c5b8

#### b) After you have created a service account (for example: test-google-form-api@pristine-valve-397622.iam.gserviceaccount.com):
1. Download the credential key json file -> rename it **Google-ServiceAccounts-Credentials.json** -> Place it in the **credentials** folder (**ecocar_webapp/airflow/credentials/**)
2. Go to your Google Drive -> right click the Google Form -> Share -> Share the **editor** access to your service account.


### 4. Using Jira Admin account to create Jira user for approved users
***NOTE! If we decide to contine using the "ecocar-atlassian" account, then we can simply skip this part because everything was developed and tested using that admin account***
Please refer to this web tutorial to create needed credentials: https://developer.atlassian.com/cloud/jira/platform/jira-rest-api-oauth-authentication/
Most importantly, we need a file called something like **jira_privatekey.pcks8** and the **access token** created
***NOTE! If we decide to contine using the "ecocar-atlassian" account, then we can simply skip this part because everything was developed and tested using that admin account***

## Trouble Shooting App Password
1. If you do not want to use gmail or if you are having trouble with using app password on google, try creating outlook (microsoft) email address and use that instead. Outlook email does not require you to create an app password. (Problem with outlook email is that when the receiver receives the email, the email is going to be in the spam email.)
2. In airflow/dags/afterApproved.py, go to "def send" function and change x=smtplib.SMTP('smtp.gmail.com', 587) to x=smtplib.SMTP('smtp-mail.outlook.com', 587)
3. In server/routes/accessRequestRouter.js, within the "sendAccessRequestMail" function, find "transporter" variable. Change the service from gmail to hotmail.
4. Try every steps after this and if the server crashes, contact "Jin Lee" on slack

## Create .env files  
You need to create three .env file  
1. Under **ecocar_webapp** directory  
create a .env file, just name it **.env**  
write  
```bash
AIRFLOW_UID=1000
```  
2. Under **ecocar_webapp/airflow/dags** directory  
create a .env file, just name it **.env**  
write  
```bash  
EMAIL_USERNAME=your_email_address_that_you_want_to_send_email_out
EMAIL_PASSWORD=the_App_Password_you_created_before
CONSUMER_KEY=OauthKey
ACCESS_TOKEN=3BHf5cScWtBpErBNA8MI4K6v3TE2ZiUI
refer_to_this_link_https://developer.atlassian.com/cloud/jira/platform/jira-rest-api-oauth-authentication/.
GOOGLE_INTEREST_FORM_ID=google_form_id_you_can_find_this_in_the_url_of_google_form
GOOGLE_TEAM_ROSTER_FORM_ID=google_form_id_you_can_find_this_in_the_url_of_google_form
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
3. Under **ecocar_webapp/server**directory  
create a .env file, just name it **.env**  
Write  
```bash  
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecocar
DB_USER=postgres
DB_PASSWORD=docker
EMAIL_USERNAME=your_email_address_that_you_want_to_send_email_out
EMAIL_PASSWORD=the_App_Password_you_created_before
IT_DEPT_EMAIL=email_address_that_you_want_to_send_email_to_as_if_it_is_the_IT_Dept
```  
  
## Connect to PostgreSQL Database  

1. Make sure you have install **Docker**  
2. Open up **Docker**    
3. cd to **ecocar_webapp** directory  
4. Run    
```bash  
  docker-compose up  
```  
  
5. Install **dBeaver** or any other database connector application  
6. In the menu bar on top, click **New Database Connection** (in dBeaver)  
7. Then select **PostgreSQL** (The elephant logo)  
8. Input the essential keys to connect the database:  
```bash  
Host: localhost
Database: ecocar
Username: postgres
Password: docker
```  
4. Then click **Finish**  
  
## Airflow   
  
### After everything is up, go to the webserver of Airflow  
```bash  
  http://localhost:8080/  
```  
The user and password are currently default as  
```bash  
User: airflow 
Password: airflow
``` 
  
### After you have logged into the webserver, you will need configure the connection with the database  
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
  
  
### Go back to home page  
Unpause the all the tasks by switching the button on the left.  
Then the Airflow is running.    
  
## A complete run  
  
### Front-end   
```bash  
  http://localhost:3000/  
```
1. Fill in corresponding info  
2. Click Submit  
3. This member will then be inserted into the **EcocarAccessRequests** database table awaiting approve from team lead first
4. After team lead has approved it, then a link for final vpn access approval will be sent to the email you put in **IT_DEPT_EMAIL**
5. Clicking that link will change the **request status** in database to be **APPROVED**

### Airflow   
```bash    
  http://localhost:8080/    
```    
1. Unpause the task
2. Trigger the task on the right end of the task interface.
3. You should be getting an email saying "Welcome aboard" soon.

# For Deployment

REMEMBER to replace all "localhost:5000" in the backend request link with our ultimate **deployed backend url** !!!
REMEMBER to edit the **email content** to include the ultimate online url to our frontend app such as the member detial form (Team Roster Form) and teamlead request form (Access Request Form)
REMEMBER to include all subteam's email addresses in .env file under **airflow/dags** !!!