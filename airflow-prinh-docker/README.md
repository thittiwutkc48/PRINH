# PRINH
PRINH TEST DE


/airflow_project
├── dags
│   └── example_dag.py
├──key
|    └──data-project-test-001-7c40b00754e9.json
├── scripts
│   ├── data_processing.py
│   └── config.yaml
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── airflow.cfg




CREATE DATABASE prinh_db;
cd airflow_project
docker-compose up --build



-- Create user
CREATE USER newuser WITH PASSWORD 'secure_password';

-- Grant all privileges on a database
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO newuser;


GRANT ALL ON SCHEMA public TO "admin";

CREATE TABLE IF NOT EXISTS suppliershipduration (
    supplierid INT,
    shipcountry VARCHAR(100),
    durationday INT,
    was_calculated_to TIMESTAMP,
    last_updated_at TIMESTAMP
);
