import os
from datetime import datetime
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping

# 1. ĐƯỜNG DẪN TUYỆT ĐỐI CHUẨN XÁC TRÊN CONTAINER DOCKER (Né hoàn toàn vòng lặp)
PATH_TO_DBT_PROJECT = "/usr/local/airflow/dags/dbt/data_pipeline"


# 2. Đường dẫn đến file chạy dbt trong môi trường ảo ngoài Codespaces
PATH_TO_DBT_EXECUTABLE = "/usr/local/airflow/dbt_venv/bin/dbt"

# 3. Cấu hình kết nối sang Snowflake
profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="snowflake_conn", 
        profile_args={"database": "dbt_db", "schema": "dbt_schema"},
    )
)

# 4. Khởi tạo DAG điều phối
dbt_snowflake_dag = DbtDag(
    project_config=ProjectConfig(PATH_TO_DBT_PROJECT),
    profile_config=profile_config,
    execution_config=ExecutionConfig(dbt_executable_path=PATH_TO_DBT_EXECUTABLE),
    operator_args={"install_deps": True},
    schedule="@daily",
    start_date=datetime(2026, 6, 1),
    catchup=False,
    dag_id="dbt_snowflake_data_pipeline",
)