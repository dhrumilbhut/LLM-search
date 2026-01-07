from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from app.pipelines.init_pgvector import init_pgvector
from app.pipelines.init_schema import init_schema
from app.pipelines.ingest_documents import ingest
from scripts.generate_embeddings import backfill_embeddings
from app.pipelines.run_evaluation_task import run_evaluation
from app.pipelines.auto_promote_task import auto_promote


with DAG(
    dag_id="document_ingestion_and_embedding",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["rag", "mlflow", "autopromotion"],
) as dag:

    init_vector = PythonOperator(
        task_id="init_pgvector",
        python_callable=init_pgvector,
    )

    init_db = PythonOperator(
        task_id="init_schema",
        python_callable=init_schema,
    )

    ingest_documents = PythonOperator(
        task_id="ingest_documents",
        python_callable=ingest,
    )

    generate_embeddings = PythonOperator(
        task_id="generate_embeddings",
        python_callable=backfill_embeddings,
    )

    evaluate_and_log = PythonOperator(
        task_id="evaluate_and_log",
        python_callable=run_evaluation,
        retries=3,
        retry_delay=timedelta(seconds=20),
    )

    auto_promotion = PythonOperator(
        task_id="auto_promote",
        python_callable=auto_promote,
    )

    (
        init_vector
        >> init_db
        >> ingest_documents
        >> generate_embeddings
        >> evaluate_and_log
        >> auto_promotion
    )
