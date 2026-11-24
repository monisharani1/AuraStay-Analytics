# 🏨 AuraStay Analytics — Cloud Data Pipeline & BI Dashboard

An end-to-end cloud data pipeline and business intelligence dashboard for hospitality operations. Raw hotel booking data flows through AWS S3 into MySQL, gets transformed with Python, and surfaces as an interactive Streamlit dashboard for revenue and occupancy decisions.

---

## 🚀 Overview

Hotel operations teams often sit on booking data they can't act on quickly — cancellations, seasonality, room-type demand, and lead-time patterns are buried in CSVs. AuraStay Analytics builds a repeatable pipeline: ingest raw bookings to the cloud, model them in a relational database, and expose the metrics that actually drive pricing and staffing decisions through a live dashboard.

---

## 🧠 Architecture

```
hotel_bookings.csv
      │
      ▼
 [ Python ingestion ]  ──►  AWS S3 (raw storage)
      │
      ▼
 [ Transformation ]   ──►  MySQL (structured tables)
      │
      ▼
 [ Streamlit app ]    ──►  KPI dashboard (revenue, occupancy, cancellations)
```

**Pipeline stages:**
1. **Ingest** — `pipeline.py` reads the raw booking CSV and uploads it to an S3 bucket.
2. **Store** — Data is loaded into MySQL in a structured schema for querying.
3. **Transform** — Python computes derived metrics (revenue, cancellation rate, lead time, seasonal aggregates).
4. **Visualize** — `app.py` (Streamlit) renders the dashboard with filters for month, hotel type, and market segment.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Ingestion & transformation | Python (Pandas) |
| Cloud storage | AWS S3 |
| Database | MySQL |
| Dashboard | Streamlit |
| Data source | Hotel bookings dataset (CSV) |

---

## 📊 Dashboard Metrics

- **Revenue trends** by month and hotel type
- **Cancellation rate** overall and by segment
- **Occupancy / booking volume** by season
- **Lead-time distribution** (how far in advance guests book)
- **Market segment & customer type** breakdown

---

## 📂 Repository Structure

```
AuraStay-Analytics/
├── app.py                 # Streamlit dashboard
├── pipeline.py            # S3 ingestion + MySQL load + transforms
├── hotel_bookings.csv     # Raw dataset
├── requirements.txt       # Dependencies
└── README.md
```

---

## ⚙️ Setup & Run

1. **Clone the repo**
   ```bash
   git clone https://github.com/monisharani1/AuraStay-Analytics.git
   cd AuraStay-Analytics
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure credentials**
   Create a `.env` file with:
   ```
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_BUCKET_NAME=your_bucket
   MYSQL_HOST=your_host
   MYSQL_USER=your_user
   MYSQL_PASSWORD=your_password
   MYSQL_DB=your_database
   ```

4. **Run the pipeline** (upload + load to MySQL)
   ```bash
   python pipeline.py
   ```

5. **Launch the dashboard**
   ```bash
   streamlit run app.py
   ```

---

