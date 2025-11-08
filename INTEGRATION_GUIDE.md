# APKTrust Frontend-Backend Integration Guide

## Overview
This guide explains how to integrate the React frontend with the Flask backend API.

## Architecture

```
Frontend (React + Vite)     Backend (Flask)
├── Home.tsx              ├── app.py (REST API)
├── Upload.tsx            ├── pages/Report.py (original Streamlit - kept for reference)
├── Result.tsx            ├── extract_permissions.py
└── Detail.tsx           └── ML Models & Analysis Scripts
```

## Setup Instructions

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Ensure all ML models are trained
python train_and_save_models.py

# Start Flask API server
python app.py
```

The backend will run on `http://localhost:5000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd "FRONTEND PMLD REVISED"

# Install dependencies (if not already installed)
npm install

# Start development server
npm run dev
```

The frontend will run on `http://localhost:5173` (default Vite port)

### 3. Environment Configuration

Create/update `.env` file in backend root:
```
API_KEY=your_mobsf_api_key
MOBSF_URL=http://localhost:8000
GROQ_API_KEY=your_groq_api_key
```

## API Endpoints

### POST `/api/upload`
Upload APK file and start analysis
- **Request**: `FormData` with `file` field
- **Response**: `{ analysis_id, status, message }`

### GET `/api/analysis/<analysis_id>`
Get analysis status and results
- **Response**: `{ status, ml_results, mobsf_report, llm_summaries, error }`

### GET `/api/report/latest`
Get the latest analysis report
- **Response**: Same as above

### GET `/api/health`
Health check endpoint
- **Response**: `{ status, models_loaded, feature_columns }`

## Frontend Flow

1. **Upload Page** (`Upload.tsx`)
   - User selects APK file
   - File uploaded to `/api/upload`
   - Analysis ID stored in sessionStorage
   - Navigate to Result page

2. **Result Page** (`Result.tsx`)
   - Fetches analysis using stored analysis_id
   - Polls API if status is "processing"
   - Displays ML predictions, status, and security score
   - Shows detailed analysis in expandable section

3. **Detail Page** (`Detail.tsx`)
   - (To be updated) Show full detailed analysis

## Data Flow

```
1. User uploads APK → POST /api/upload
2. Backend processes:
   - Extract permissions (androguard)
   - Run ML predictions (4 models)
   - MobSF analysis (optional)
   - LLM analysis (optional)
3. Store results in memory (use Redis/DB in production)
4. Frontend polls /api/analysis/<id> until complete
5. Display results on Result page
```

## Key Features

✅ **File Upload**: Real file upload to backend
✅ **Real-time Analysis**: ML predictions work immediately
✅ **Status Polling**: Frontend polls for analysis completion
✅ **Error Handling**: Proper error messages displayed
✅ **Responsive Design**: Works on mobile and desktop

## Troubleshooting

### Backend Issues
- **Port 5000 already in use**: Change port in `app.py`
- **Models not loading**: Ensure models are trained (`train_and_save_models.py`)
- **MobSF errors**: Check API_KEY in `.env`

### Frontend Issues
- **CORS errors**: Ensure Flask-CORS is installed and configured
- **API connection failed**: Check backend is running on port 5000
- **No data displayed**: Check browser console for errors

## Production Deployment

For production:
1. Use environment variables for API URLs
2. Replace in-memory storage with Redis/Database
3. Use Celery for async task processing
4. Add authentication/authorization
5. Configure proper CORS settings
6. Set up proper error logging

## Notes

- Streamlit backend (`pages/Report.py`) is kept for reference but not used in production
- The Flask API replicates all Streamlit functionality
- Frontend uses React hooks for state management
- All analysis functions are reused from Streamlit version

