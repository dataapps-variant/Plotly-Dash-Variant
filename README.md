# Variant Analytics Dashboard - Plotly Dash Version

This is a Plotly Dash conversion of the original Streamlit-based Variant Analytics Dashboard.

## Features

- **Authentication**: Simple username/password login with session management
- **Dark/Light Theme**: Toggle between dark and light modes
- **Dashboard Hub**: Landing page with list of available dashboards
- **ICARUS Historical Dashboard**: 
  - Active/Inactive tabs
  - Comprehensive filters (Date Range, BC, Cohort, Plan Groups, Metrics)
  - Pivot tables with CSV export
  - Interactive line charts with zoom/pan
- **Admin Panel**: User management for admin users

## Project Structure

```
dash_app/
├── app/
│   ├── __init__.py
│   ├── main.py              # Main entry point
│   ├── auth.py              # Authentication system
│   ├── bigquery_client.py   # BigQuery data loading
│   ├── charts.py            # Chart components
│   ├── colors.py            # Color system
│   ├── config.py            # Configuration and constants
│   ├── filters.py           # Filter components
│   ├── pivots.py            # Pivot table components
│   ├── theme.py             # Theme system (CSS)
│   ├── assets/              # Static assets (CSS, images)
│   └── pages/
│       ├── __init__.py
│       ├── login.py         # Login page
│       ├── landing.py       # Dashboard hub
│       ├── icarus_historical.py  # ICARUS dashboard
│       └── admin_panel.py   # Admin panel
├── requirements.txt
├── Dockerfile
└── README.md
```

## Installation

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
export GCS_CACHE_BUCKET=your-bucket-name  # Optional
export SECRET_KEY=your-secret-key
```

4. Run the application:
```bash
python app/main.py
```

The dashboard will be available at `http://localhost:8050`

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t variant-dashboard .
```

2. Run the container:
```bash
docker run -p 8080:8080 \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  -e GCS_CACHE_BUCKET=your-bucket-name \
  -e SECRET_KEY=your-secret-key \
  -v /path/to/credentials.json:/app/credentials.json \
  variant-dashboard
```

### Cloud Run Deployment

1. Build and push to Container Registry:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/variant-dashboard
```

2. Deploy to Cloud Run:
```bash
gcloud run deploy variant-dashboard \
  --image gcr.io/PROJECT_ID/variant-dashboard \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GCS_CACHE_BUCKET=your-bucket-name,SECRET_KEY=your-secret-key
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to GCP service account JSON | Yes |
| `GCS_CACHE_BUCKET` | GCS bucket for caching | No |
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `PORT` | Server port (default: 8050) | No |
| `DEBUG` | Debug mode (default: True) | No |

### Default Users

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| viewer | viewer123 | Read Only |

## Key Differences from Streamlit Version

### Architecture Changes

1. **State Management**: Uses Flask sessions instead of Streamlit session_state
2. **Routing**: URL-based routing with dcc.Location instead of page navigation
3. **Callbacks**: Event-driven callbacks instead of top-to-bottom execution
4. **Styling**: CSS-based theming instead of Streamlit's markdown styling

### Component Mapping

| Streamlit | Dash |
|-----------|------|
| `st.session_state` | Flask `session` |
| `st.columns()` | `html.Div` with flexbox |
| `st.expander()` | `html.Details` |
| `st.tabs()` | `dcc.Tabs` |
| `st.selectbox()` | `dcc.Dropdown` |
| `st.checkbox()` | `dcc.Checklist` |
| `st.date_input()` | `dcc.DatePickerSingle` |
| `st.dataframe()` | `dash_table.DataTable` |
| `st.plotly_chart()` | `dcc.Graph` |
| `@st.cache_data` | `@lru_cache` or custom caching |

### Features Not Directly Ported

1. **AG Grid**: Replaced with Dash DataTable (similar functionality)
2. **st.rerun()**: Handled via callback outputs
3. **Automatic reruns**: Need explicit callback triggers

## Usage

1. **Login**: Use demo credentials (admin/admin123 or viewer/viewer123)
2. **Landing Page**: View available dashboards and their status
3. **ICARUS Dashboard**:
   - Select Active or Inactive tab
   - Configure filters (date range, BC, cohort, plans, metrics)
   - Click "Apply Filter" to load data
   - View pivot tables and charts
4. **Admin Panel** (admin only): Manage users and access

## Development Notes

### Adding New Pages

1. Create a new file in `app/pages/`
2. Define a `create_layout(theme)` function
3. Add route in `main.py`'s `display_page` callback
4. Add any necessary callbacks

### Modifying Themes

1. Edit `theme.py`'s `THEME_COLORS` in `config.py`
2. Update `get_base_stylesheet()` in `theme.py` for CSS changes

### Adding New Charts

1. Add chart configuration to `CHART_METRICS` in `config.py`
2. Charts will automatically appear in the dashboard

## Troubleshooting

### Common Issues

1. **"No data available"**: Ensure BigQuery credentials are properly configured
2. **Theme not persisting**: Clear browser localStorage and refresh
3. **Callbacks not firing**: Check component IDs match in callbacks

### Debug Mode

Set `DEBUG=True` environment variable for detailed error messages.

## License

Internal use only - Variant Group
