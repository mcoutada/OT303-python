from datetime import timedelta


# Arguments for DAGs
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['lg@example.com'],  # Receive alert on email if fail or success
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(seconds=30) } # If fail, wait 30 secs to retry.