# Variant Analytics Dashboard (Dash Version)

A comprehensive analytics dashboard built with Plotly Dash, converted from Streamlit.

## Features

- **Authentication**: Username/password authentication with role-based access (admin/readonly)
- **Theme Support**: Dark and Light mode toggle
- **ICARUS Historical Dashboard**: 
  - Active/Inactive tabs
  - Date range, Billing Cycle, Cohort filters
  - Multi-select plan and metrics filters
  - Pivot tables with Regular and Crystal Ball views
  - Line charts for 10 metrics with zoom/pan support
- **Admin Panel**: User management and dashboard access control
- **BigQuery Integration**: Efficient data loading with multi-level caching
- **GCS Caching**: Parquet file caching for performance

## Project Structure

```
variant_dashboard_dash/
├── app/
│   ├── __init__.py
│   ├── main.py              # Main Dash application entry point
│   ├── config.py            # Configuration and constants
│   ├── auth.py              # Authentication system
│   ├── theme.py             # Theme/CSS generation
│   ├── colors.py            # Color utilities for charts
│   ├── charts.py            # Plotly chart builders
│   ├── pivots.py            # Pivot table utilities
│   ├── bigquery_client.py   # BigQuery data loading
│   ├── assets/              # Static assets (CSS, images)
│   └── pages/
│       ├── __init__.py
│       ├── login.py         # Login page
│       ├── landing.py       # Dashboard hub
│       ├── admin_panel.py   # Admin panel
│       └── icarus_historical.py  # ICARUS dashboard
├── requirements.txt
├── Dockerfile
└── README.md
```

## Local Development

### Prerequisites

- Python 3.11+
- Google Cloud credentials (for BigQuery)

### Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
export GCS_CACHE_BUCKET="your-bucket-name"  # Optional
export SECRET_KEY="your-secret-key"  # For session management
```

4. Run the application:
```bash
python app/main.py
```

5. Open browser at http://localhost:8050

## Demo Credentials

- **Admin**: `admin` / `admin123`
- **Viewer**: `viewer` / `viewer123`

## Docker Deployment

### Build
```bash
docker build -t variant-dashboard-dash .
```

### Run
```bash
docker run -p 8050:8050 \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  -e GCS_CACHE_BUCKET=your-bucket \
  -v /path/to/credentials.json:/app/credentials.json \
  variant-dashboard-dash
```

## Cloud Run Deployment

1. Build and push to Container Registry:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/variant-dashboard-dash
```

2. Deploy to Cloud Run:
```bash
gcloud run deploy variant-dashboard-dash \
  --image gcr.io/PROJECT_ID/variant-dashboard-dash \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GCS_CACHE_BUCKET=your-bucket
```

## Key Differences from Streamlit Version

| Feature | Streamlit | Dash |
|---------|-----------|------|
| Session State | `st.session_state` | `dcc.Store` |
| Caching | `@st.cache_data` | `lru_cache` / manual |
| Routing | Multi-page apps | `dcc.Location` + callbacks |
| Components | Streamlit native | Dash HTML/DCC components |
| Tables | AG Grid | Dash DataTable |
| Styling | `st.markdown(CSS)` | External CSS / inline styles |

## Configuration

Edit `app/config.py` to modify:

- BigQuery project/dataset/table
- Dashboard registry
- Filter options (BC, Cohort)
- Metrics configuration
- Theme colors
- Default users

## Caching Architecture

1. **App-level cache**: In-memory PyArrow table
2. **GCS cache**: Parquet files for persistence across instances
3. **BigQuery**: Source of truth

Cache refresh flow:
1. `Refresh BQ` → Query BigQuery → Save to staging
2. `Refresh GCS` → Copy staging to active → Clear caches

## License

Proprietary - Variant Group
