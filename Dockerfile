FROM astrocrpublic.azurecr.io/runtime:3.0-1

# Install the GCP provider package
RUN pip install apache-airflow-providers-google

# Copy the key file into the container at a consistent internal path
COPY include/gcp-key.json /usr/local/airflow/include/gcp-key.json

# Set the environment variable so ADC (Application Default Credentials) can use it
ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/local/airflow/include/gcp-key.json


