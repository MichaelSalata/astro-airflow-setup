# Suggested test dag per setup instructions at: https://www.astronomer.io/docs/astro/cli/authenticate-to-gcp

"""
# requires the following environment variables to be set in your Airflow environment:
AIRFLOW__SECRETS__BACKEND=airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend
AIRFLOW__SECRETS__BACKEND_KWARGS={"connections_prefix": "airflow-connections", "variables_prefix": "airflow-variables", "project_id": "gcp-online-test"}

# requires the secret Variables in the GCP Manager to be prefaced by the value set at key "variables_prefix"
# requires the secret Connections in the GCP Manager to be prefaced by the value set at key "connections_prefix"

# This DAG requires the secrets to be created in your GCP Secret Manager:
# Example Secret Connection key: airflow-variables-astro-airflow-setup_secret_variable
# Example Secret Connection value : example_secret_value

# Example Secret Variable key: airflow-connections-astro-airflow-setup_secret_connection
# Example Secret Variable value: postgresql+psycopg2://user:password@host:5432
"""

# from airflow.models import Variable # Depreciated
from airflow.models.connection import Connection # Depreciated but from airflow.sdk import Connection doesn't have get_connection_from_secretshttps://www.astronomer.io/docs/astro-private-cloud/v-0-37/ci-cd#example-cicd-workflow
from airflow.sdk import DAG, task, Variable
from datetime import datetime

with DAG(
    dag_id="example_secrets_dag",
    start_date=datetime(2022, 1, 1),
    schedule=None,
    catchup=False,
):
    @task
    def print_var():
        # Variables
        my_var = Variable.get("astro-airflow-setup_secret_variable")
        print(f"My secret variable is: {my_var}")

        # Preferred modern way to fetch a connection (no BaseHook needed)
        conn = Connection.get_connection_from_secrets("astro-airflow-setup_secret_connection")
        print(f"My secret connection is: {conn.get_uri()}")

    print_var()
