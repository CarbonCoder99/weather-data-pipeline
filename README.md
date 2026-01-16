# 🌍 Automated Weather ETL & Analytics Pipeline

An end-to-end data engineering project that extracts global weather data, processes it via a containerized Python environment, and automates the flow into a cloud-hosted PostgreSQL database for real-time visualization.

## 🚀 Project Architecture
The pipeline follows a modern "Cloud-Native" ETL pattern:
1. **Extraction:** Fetches live weather data (Lagos, London, Tokyo, etc.) via Open-Meteo API.
2. **Transformation:** Uses **Pandas** to clean, validate, and convert data into optimized **Parquet** files.
3. **Orchestration:** **GitHub Actions** triggers the pipeline daily (Cron job).
4. **Loading:** Data is pushed to a **Supabase (PostgreSQL)** database using **SQLAlchemy**.
5. **Visualization:** A live **Google Looker Studio** dashboard connects directly to the DB for real-time insights.



## 🛠️ Tech Stack
* **Language:** Python 3.13.5
* **Data Processing:** Pandas, PyArrow
* **Database:** PostgreSQL (Supabase)
* **Infrastructure:** Docker, Docker-Compose
* **CI/CD:** GitHub Actions
* **Visualization:** Google Looker Studio

## 📁 File Structure
* `weather_extractor.py`: Main ETL script logic.
* `.github/workflows/`: Automation YAML for daily runs.
* `Dockerfile` / `docker-compose.yml`: Containerization settings.
* `data/`: Local storage for processed Parquet files.

## 📊 Live Dashboard
You can view the live weather trends here: https://lookerstudio.google.com/reporting/bad49e74-8b03-420f-a933-629b76a05b7d

## 🔧 How to Run Locally
1. Clone the repo: `git clone https://github.com/CarbonCoder99/weather-data-pipeline`
2. Set up your environment variables in a `.env` file.
3. Run via Docker: `docker-compose up`
