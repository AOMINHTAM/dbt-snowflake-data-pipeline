<div align="center">
  <h1>Airflow dbt Snowflake Pipeline 🚀❄️</h1>
  <p><em>A production-ready ELT Data Pipeline orchestrating dbt transformations inside Snowflake via Apache Airflow</em></p>

  [![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)]()
  [![dbt](https://img.shields.io/badge/dbt-Snowflake-FF694B?logo=dbt&logoColor=white)]()
  [![Snowflake](https://img.shields.io/badge/Snowflake-Data_Warehouse-29B5E8?logo=snowflake&logoColor=white)]()
  [![Airflow](https://img.shields.io/badge/Airflow-Orchestration-017CEE?logo=apache-airflow&logoColor=white)]()
  [![Docker](https://img.shields.io/badge/Docker-Infrastructure-2496ED?logo=docker&logoColor=white)]()
</div>

---

## 📖 Project Overview

Dự án này triển khai một hệ thống **Modern Data Stack (MDS)** theo mô hình **ELT Pipeline** tự động hoàn toàn. Hệ thống trích xuất dữ liệu mẫu ngành bán lẻ (TPC-H), nạp vào Cloud Data Warehouse **Snowflake**, sau đó sử dụng **dbt-core** để tổ chức mô hình hóa dữ liệu (Data Modeling) theo cấu trúc Medallion, toàn bộ luồng được điều phối trực quan bởi **Apache Airflow** (Astronomer Cosmos).

### Key Features
- **Modern ELT Workflow**: Chia tách rõ ràng giữa tầng lưu trữ/tính toán (Snowflake) và tầng điều phối (Airflow).
- **Medallion Data Architecture**: Tổ chức dữ liệu qua các lớp Staging (`stg_`) và Marts (`fct_`) giúp chuẩn hóa và sẵn sàng cho Business Intelligence.
- **Dynamic Task Generation**: Sử dụng *Astronomer Cosmos* để tự động phân rã toàn bộ project dbt thành các Task con dạng đồ thị DAG trực quan trên Airflow mà không cần viết lại code Python thủ công.
- **Advanced Transformations**: Tích hợp gói thư viện mở rộng `dbt_utils` để tối ưu hóa việc xử lý chuỗi và tính toán logic.
- **Isolated Environment**: Chạy dbt trong môi trường ảo Python cách ly (`dbt_venv`) nằm ngay bên trong Docker container của Airflow để tránh xung đột thư viện.

---

## 🛠️ Tech Stack & Architecture

<div align="center">
  <img src="images/architecture.png" alt="Data Pipeline Architecture" width="800">
</div>

| Layer | Component | Technology | Description |
| :--- | :--- | :---: | :--- |
| **Storage & Compute** | Data Warehouse | ❄️ Snowflake | Lưu trữ dữ liệu thô (TPC-H) và thực thi tính toán các câu lệnh SQL từ dbt. |
| **Transform** | Data Modeling | 🔨 dbt-core + dbt-snowflake | Đọc dữ liệu thô, biến đổi qua các layer và vật chất hóa (Materialize) thành View/Table trên Snowflake. |
| **Orchestration** | Scheduler | 🌬️ Apache Airflow | Tự động lập lịch, quét cấu trúc dbt và kích hoạt pipeline chạy hàng ngày. |
| **Infrastructure** | Container | 🐳 Docker & Astro CLI | Đóng gói toàn bộ môi trường Airflow Webserver, Scheduler, Triggerer giúp chạy nhất quán trên mọi máy tính. |

---

## 📂 Project Structure

```text
dbt-snowflake-data-pipeline/
├── dags/
│   ├── dbt_dags.py               # File cấu hình Airflow DAG điều phối dbt
│   └── dbt/
│       └── data_pipeline/        # Thư mục gốc chứa toàn bộ dự án dbt
│           ├── dbt_project.yml   # File cấu hình chính của dbt
│           ├── packages.yml      # Khai báo các thư viện mở rộng (dbt_utils)
│           ├── models/           # Nơi chứa các file SQL biến đổi dữ liệu
│           │   ├── staging/      # Lớp Staging (stg_tpch_orders.sql,...)
│           │   └── marts/        # Lớp Marts chứa bảng dữ liệu tinh lọc (fct_orders.sql)
│           └── seeds/            # Dữ liệu tĩnh dạng csv nạp thủ công
├── dbt_venv/                     # Môi trường ảo Python cách ly chứa dbt-core & dbt-snowflake
├── Dockerfile                    # Cấu hình container cài đặt môi trường cho Airflow
└── .gitignore                    # Chặn file rác và bảo mật tệp credentials (profiles.yml)

🚀 Getting Started
1. Chuẩn bị môi trường local 
Tại thư mục gốc của dự án, khởi động môi trường ảo Python và tải các gói phụ thuộc (packages) cục bộ của dbt:Bash./dbt_venv/bin/dbt deps --project-dir dags/dbt/data_pipeline
2. Thiết lập hạ tầng và phân quyền trên Snowflake
Mở giao diện Snowflake Worksheet, chạy bộ lệnh SQL tối cao này bằng role ACCOUNTADMIN để khởi tạo hạ tầng và gỡ bẫy quyền truy cập (future privileges), đảm bảo dbt tạo View xé gió không bị chặn:SQLUSE ROLE ACCOUNTADMIN;

CREATE WAREHOUSE IF NOT EXISTS dbt_wh WITH WAREHOUSE_SIZE='x-small';
CREATE DATABASE IF NOT EXISTS dbt_db;
CREATE ROLE IF NOT EXISTS dbt_role;

GRANT ROLE dbt_role TO USER AOMINHTAM;
GRANT USAGE ON WAREHOUSE dbt_wh TO ROLE dbt_role;
GRANT ALL ON DATABASE dbt_db TO ROLE dbt_role;

-- Cấp đặc quyền tương lai trên Schema cho ACCOUNTADMIN thực thi điều phối
GRANT ALL PRIVILEGES ON SCHEMA DBT_DB.DBT_SCHEMA TO ROLE ACCOUNTADMIN;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA DBT_DB.DBT_SCHEMA TO ROLE ACCOUNTADMIN;
GRANT ALL PRIVILEGES ON FUTURE VIEWS IN SCHEMA DBT_DB.DBT_SCHEMA TO ROLE ACCOUNTADMIN;
3. Khởi chạy hệ thống trên AirflowKhởi động cụm container Airflow bằng Astronomer CLI:Bashastro dev start
---

## 🔗 Monitoring & Access

| Service | Access Link / Endpoint | Credentials / Role |
| :--- | :--- | :--- |
| **Airflow Webserver** | `http://localhost:8080` *(Cổng mặc định khi chạy Astro CLI)* | Administrator (Internal Account) |
| **Snowflake Console** | `https://bs54698.ap-southeast-7.aws.snowflakecomputing.com` | Sử dụng tài khoản cá nhân `AOMINHTAM` / Role `dbt_role` |

---

## 📝 Nhật ký sửa lỗi (Troubleshooting Highlights)

* **Broken DAG (Mù đường dẫn Docker):** Khắc phục lỗi lệch cấu hình đường dẫn tuyệt đối của thư viện Cosmos khi đi vào container Docker bằng cách trỏ chuẩn xác về `/usr/local/airflow/dags/dbt/data_pipeline`.
* **Compilation Error (Thiếu gói dbt_utils):** Di chuyển file `packages.yml` vào đúng thư mục con dự án dbt, chạy `dbt deps` bọc lót cục bộ để nạp thư viện xử lý macro thành công.
* **SQL access control error (Snowflake Lỗi 003001):** Sửa triệt để lỗi xung đột quyền sở hữu schema giữa `dbt_role` và `ACCOUNTADMIN` bằng cách cấp bổ sung đặc quyền `FUTURE TABLES/VIEWS` trực tiếp trên database Snowflake.

---