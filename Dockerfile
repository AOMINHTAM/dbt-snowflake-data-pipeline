FROM quay.io/astronomer/astro-runtime:12.1.0

# 1. Xóa sạch thư mục cũ đề phòng rác copy từ ngoài vào, sau đó mới tạo venv mới
RUN rm -rf /usr/local/airflow/dbt_venv && \
    python3 -m venv /usr/local/airflow/dbt_venv && \
    /usr/local/airflow/dbt_venv/bin/pip install --no-cache-dir dbt-snowflake

# 2. Khai báo biến môi trường cho Airflow gõ đầu dbt
ENV ASTRO_PYENV_dbt=/usr/local/airflow/dbt_venv/bin/dbt