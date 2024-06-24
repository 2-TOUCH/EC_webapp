# Use the official Airflow image as the base image
FROM apache/airflow:2.5.2

# Install additional Python packages
RUN pip install google-auth google-auth-oauthlib google-auth-httplib2
RUN pip install google-api-python-client
RUN pip install docusign_esign