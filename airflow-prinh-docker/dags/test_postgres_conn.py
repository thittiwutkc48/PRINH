from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dag = DAG(
    'postgres_test_dag',
    default_args=default_args,
    description='A simple test DAG to query PostgreSQL',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)


run_test_query = PostgresOperator(
    task_id='run_test_query',
    postgres_conn_id='postgres_conn',
    sql='SELECT customerid, customername, contactname, phone, fax FROM public.customers;', 
    dag=dag,
)

def fetch_data_from_db():
    """Function to fetch data from the PostgreSQL database."""
    pg_hook = PostgresHook(postgres_conn_id='postgres_conn')
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute("SELECT customerid, customername, contactname, phone, fax FROM public.customers;" )
    results = cursor.fetchall()
    for result in results:
        print(result)
    cursor.close()
    connection.close()


fetch_data_task = PythonOperator(
    task_id='fetch_data_task',
    python_callable=fetch_data_from_db,
    dag=dag,
)


run_test_query >> fetch_data_task
