# 6-Month Data Filter Implementation

## Overview
Implemented 6-month data filtering across all dashboard components to ensure data freshness and relevance.

## Changes Made

### 1. Main Dashboard App (`dashboard/app.py`)
- **Default filter**: Changed from 30 days to 180 days (6 months)
- **Maximum filter**: Limited from 365 days to 180 days (6 months)
- **Summary method**: Added 6-month pre-filtering in `get_dashboard_summary()`

**Key Changes:**
```python
# Before: days_back = max(1, min(365, int(request.args.get('days', 30))))
# After: days_back = max(1, min(180, int(request.args.get('days', 180))))

# Added 6-month filter in get_dashboard_summary:
six_months_ago = today - timedelta(days=180)
commitments = [c for c in commitments if datetime.strptime(c['announcement_date'], '%Y-%m-%d').date() >= six_months_ago]
funding = [f for f in funding if datetime.strptime(f['announcement_date'], '%Y-%m-%d').date() >= six_months_ago]
```

### 2. Public Dashboard App (`dashboard/public_app.py`)
- Applied identical 6-month filtering to public version
- Updated both API endpoints (`/api/commitments`, `/api/funding`)
- Updated summary calculations

### 3. Secure Dashboard App (`dashboard/secure_app.py`)
- Updated `validate_query_params()` function
- Changed default and maximum from 1 year to 6 months
- Added 6-month pre-filtering in `get_dashboard_summary()`

**Key Changes:**
```python
# Before: days_back = max(1, min(365, days_back))
# After: days_back = max(1, min(180, days_back))
```

## Impact

### API Endpoints
All API endpoints now:
- **Default to 6 months** of data when no `days` parameter is provided
- **Maximum 6 months** even if a larger `days` parameter is requested
- Return only data from the last 180 days

### Dashboard Summary
The main dashboard summary now:
- Shows metrics based only on the last 6 months of data
- Calculates totals, averages, and trends using 6-month window
- Maintains "recent" (7-day) calculations within the 6-month dataset

### User Experience
- Users see only relevant, recent data
- Dashboard loads faster with smaller datasets
- API responses are more focused and actionable

## Data Sources Unaffected
- **Scrapers continue to collect all available data**
- **Data files contain complete historical records**
- **Filtering happens at the dashboard/API layer**

This ensures we can always expand the time window in the future if needed.

## Verification

To verify the 6-month filtering is working:

1. **Check API responses:**
   ```bash
   curl "http://localhost:5000/api/commitments" | jq '.filters_applied.days_back'
   # Should return: 180
   ```

2. **Check data dates:**
   ```bash
   curl "http://localhost:5000/api/commitments" | jq '.commitments[].announcement_date' | sort
   # Should show only dates from last 6 months
   ```

3. **Test maximum limit:**
   ```bash
   curl "http://localhost:5000/api/commitments?days=365" | jq '.filters_applied.days_back'
   # Should return: 180 (capped at 6 months)
   ```

## Files Modified
- `dashboard/app.py`
- `dashboard/public_app.py` 
- `dashboard/secure_app.py`

## Files NOT Modified
- `scrapers/` - Continue collecting all available data
- `run_dashboard.py` - Orchestration remains the same
- Data files - Historical data preserved