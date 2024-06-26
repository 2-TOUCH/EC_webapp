### Important 
This repository was a group effort, with this version posted on GitHub for the sake of portfolio, with the repository owner being 1 of 4 contributors.

# EcoCAR Access Web Application

This application serves as a basis to fill out the interest form to join ECOCAR and successfully onboard new team members.

## Download the Code from BitBucket

Clone the project:

\```bash
git clone -b "branch name" https://ecocar-bitbucket.engineering.ucdavis.edu/scm/pm/ecocar_webapp.git
\```

## Pre-requisites

### 1. Installing Software

1. **Docker**
2. **dBeaver** (or any other Database software that can use PostgreSQL)

### 2. Create App Password

1. Refer to [this website](https://support.google.com/accounts/answer/185833?hl=en).
2. Log in with your desired Gmail account to **send emails out**.
3. Create an App Password.

### 3. Using Google Form's API

#### a) Create Authentication (Service Account)

Follow [this tutorial](https://medium.com/frudens-engineering/how-to-use-google-forms-and-other-apis-easily-from-filemaker-using-google-service-account-261a4b27c5b8) to create a service account.

#### b) After Creating a Service Account:

1. Download the credential key JSON file, rename it to **Google-ServiceAccounts-Credentials.json**, and place it in the **credentials** folder (**ecocar_webapp/airflow/credentials/**).
2. Go to your Google Drive, right-click the Google Form, select "Share", and share the **editor** access to your service account.

### 4. Using Jira Admin Account to Create Jira User for Approved Users

**NOTE!** If you decide to continue using the "ecocar-atlassian" account, then you can skip this part because everything was developed and tested using that admin account. Follow [this tutorial](https://developer.atlassian.com/cloud/jira/platform/jira-rest-api-oauth-authentication/) to create the needed credentials. Most importantly, you need a file called something like **jira_privatekey.pcks8** and the **access token** created.

**NOTE!** If you decide to continue using the "ecocar-atlassian" account, then you can skip this part because everything was developed and tested using that admin account.

## Troubleshooting App Password

1. If you do not want to use Gmail or if you are having trouble using the app password on Google, try creating an Outlook (Microsoft) email address and use that instead. Outlook email does not require you to create an app password. (Problem with Outlook email is that when the receiver receives the email, the email is going to be in the spam email.)
2. In `airflow/dags/afterApproved.py`, go to the `def send` function and change `x=smtplib.SMTP('smtp.gmail.com', 587)` to `x=smtplib.SMTP('smtp-mail.outlook.com', 587)`.
3. In `server/routes/accessRequestRouter.js`, within the `sendAccessRequestMail` function, find the `transporter` variable. Change the service from Gmail to Hotmail.
4. Try every step after this, and if the server crashes, contact "Jin Lee" on Slack.

## Create .env Files

You need to create three `.env` files:

1. Under the **ecocar_webapp** directory:
   Create a `.env` file named `.env` and write:
   \```bash
   AIRFLOW_UID=1000
   \```

2. Under the **ecocar_webapp/airflow/dags** directory:
   Create a `.env` file named `.env` and write:
   \```bash
   EMAIL_USERNAME=your_email_address_that_you_want_to_send_email_out
   EMAIL_PASSWORD=the_App_Password_you_created_before
   CONSUMER_KEY=OauthKey
   ACCESS_TOKEN=3BHf5cScWtBpErBNA8MI4K6v3TE2ZiUI
   GOOGLE_INTEREST_FORM_ID=google_form_id_you_can_find_this_in_the_url_of_google_form
   GOOGLE_TEAM_ROSTER_FORM_ID=google_form_id_you_can_find_this_in_the_url_of_google_form
   USER_MANAGER_EMAIL=person_who_is_in_charge_of_creating_Confluence_and_Bitbucket_accounts_after_Jira_account_has_been_created.
   DOCUSIGN_INTEGRATION_KEY=fd21a8fe-ba3f-4f95-a973-1ebcbd004c17
   DOCUSIGN_BASE_PATH=https://demo.docusign.net/restapi
   DOCUSIGN_USER_ID=a83cb6c9-bb32-4bc2-825a-37b7a30fba15
   DOCUSIGN_API_ACCOUNT_ID=a9ab76b0-4fe9-4f65-aa20-f091bad8969c
   DOCUSIGN_PHOTO_WAIVER_TEMPLATE_ID=7600bb70-d0ce-4b64-85e1-af6c908b77cb
   DOCUSIGN_UPA_TEMPLATE_ID=
   \```

3. Under the **ecocar_webapp/server** directory:
   Create a `.env` file named `.env` and write:
   \```bash
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=ecocar
   DB_USER=postgres
   DB_PASSWORD=docker
   EMAIL_USERNAME=your_email_address_that_you_want_to_send_email_out
   EMAIL_PASSWORD=the_App_Password_you_created_before
   IT_DEPT_EMAIL=email_address_that_you_want_to_send_email_to_as_if_it_is_the_IT_Dept
   \```

## Connect to PostgreSQL Database

1. Make sure you have installed **Docker**.
2. Open **Docker**.
3. Navigate to the **ecocar_webapp** directory.
4. Run:
   \```bash
   docker-compose up
   \```

5. Install **dBeaver** or any other database connector application.
6. In the menu bar on top, click **New Database Connection** (in dBeaver).
7. Then select **PostgreSQL** (The elephant logo).
8. Input the essential keys to connect to the database:
   \```bash

   \```
9. Then click **Finish**.

## Airflow

### After Everything is Up, Go to the Webserver of Airflow

\```bash
http://localhost:8080/
\```
The user and password are currently default as:
\```bash

\```

### Configure the Connection with the Database

1. At the top bar, hover on **Admin**.
2. Click on **Connections** in the drop-down menu.
3. Click the button **next to Action** to add a new record.
   \```bash
   Connection Id: postgres_ecocar
   Connection Type: Postgres
   Host: host.docker.internal
   Schema: ecocar
   Login: postgres
   Password: docker
   Port: 5432
   \```
4. Then click "Save".

### Go Back to Home Page

Unpause all the tasks by switching the button on the left. Then Airflow is running.

## A Complete Run

### Front-end

\```bash
http://localhost:3000/
\```
1. Fill in corresponding info.
2. Click Submit.
3. This member will then be inserted into the **EcocarAccessRequests** database table, awaiting approval from the team lead first.
4. After the team lead has approved it, a link for final VPN access approval will be sent to the email you put in **IT_DEPT_EMAIL**.
5. Clicking that link will change the **request status** in the database to **APPROVED**.

### Airflow

\```bash
http://localhost:8080/
\```
1. Unpause the task.
2. Trigger the task on the right end of the task interface.
3. You should be getting an email saying "Welcome aboard" soon.

# For Deployment

1. **REMEMBER** to replace all "localhost:5000" in the backend request link with our ultimate **deployed backend URL**!
2. **REMEMBER** to edit the **email content** to include the ultimate online URL to our frontend app, such as the member detail form (Team Roster Form) and team lead request form (Access Request Form).
3. **REMEMBER** to include all subteam's email addresses in the `.env` file under **airflow/dags**!



