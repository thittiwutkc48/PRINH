from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import psycopg2
import pandas as pd

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 6, 19),
}

# Define the DAG with its configurations
dag = DAG(
    'data_insert_to_postgres',
    default_args=default_args,
    description='A DAG to insert data into PostgreSQL',
    schedule_interval=None,  # Define your schedule interval here
)

# Function to insert data into PostgreSQL
def insert_data_to_postgres():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname='your_database',
            user='your_username',
            password='your_password',
            host='localhost',
            port='5432'
        )
        
        cursor = conn.cursor()

        # Example: Inserting data from a pandas DataFrame into PostgreSQL
        data = {'col1': [1, 2, 3], 'col2': ['A', 'B', 'C']}
        df = pd.DataFrame(data)
        
        # Convert DataFrame to list of tuples
        records = df.to_records(index=False)
        records_list = list(records)

        # Execute SQL command to insert data into PostgreSQL table
        for rec in records_list:
            cursor.execute("INSERT INTO your_table (col1, col2) VALUES (%s, %s)", rec)
        
        # Commit changes and close connection
        conn.commit()
        cursor.close()
        conn.close()

        print("Data inserted successfully into PostgreSQL")

    except Exception as e:
        print(f"Error inserting data into PostgreSQL: {str(e)}")
        raise

# Define the task that calls the function to insert data
task_insert_data = PythonOperator(
    task_id='insert_data_to_postgres',
    python_callable=insert_data_to_postgres,
    dag=dag,
)
