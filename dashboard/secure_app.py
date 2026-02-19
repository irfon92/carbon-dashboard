#!/usr/bin/env python3
"""
SECURE Carbon Deal Intelligence Dashboard
Security-hardened version with authentication and input validation
"""

from flask import Flask, render_template, jsonify, request, abort
from functools import wraps
import json
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any
import glob
import logging

# Configure secure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Security configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-in-production')
app.config['JSON_SORT_KEYS'] = False

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# API Key authentication
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        expected_key = os.environ.get('CARBON_DASHBOARD_API_KEY')
        
        if not expected_key:
            logger.error("API key not configured")
            return jsonify({'error': 'Service temporarily unavailable'}), 503
            
        if not api_key or api_key != expected_key:
            logger.warning(f"Unauthorized access attempt from {request.remote_addr}")
            return jsonify({'error': 'Unauthorized'}), 401
            
        return f(*args, **kwargs)
    return decorated_function

# Input validation
def validate_query_params():
    """Validate and sanitize query parameters"""
    try:
        min_relevance = float(request.args.get('min_relevance', 0))
        min_relevance = max(0.0, min(1.0, min_relevance))
        
        days_back = int(request.args.get('days', 30))
        days_back = max(1, min(365, days_back))  # Limit to 1 year max
        
        commitment_type = request.args.get('type', '')
        # Sanitize commitment type
        if commitment_type and not re.match(r'^[a-zA-Z0-9_-]+$', commitment_type):
            commitment_type = ''
            
        sector = request.args.get('sector', '')
        # Sanitize sector
        if sector and not re.match(r'^[a-zA-Z0-9_-]+$', sector):
            sector = ''
            
        min_threat = float(request.args.get('min_threat', 0))
        min_threat = max(0.0, min(1.0, min_threat))
        
        min_partnership = float(request.args.get('min_partnership', 0))
        min_partnership = max(0.0, min(1.0, min_partnership))
        
        return {
            'min_relevance': min_relevance,
            'days_back': days_back,
            'commitment_type': commitment_type,
            'sector': sector,
            'min_threat': min_threat,
            'min_partnership': min_partnership
        }
    except (ValueError, TypeError) as e:
        logger.warning(f"Invalid query parameters: {e}")
        abort(400, description="Invalid parameters")

class DashboardData:
    def __init__(self, data_dir: str = "../data"):
        # Handle both local and cloud deployment paths
        if not os.path.exists(data_dir):
            data_dir = "data"  # Fallback for cloud deployment
        self.data_dir = data_dir
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """Ensure data directory exists"""
        try:
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir, mode=0o750)  # Secure permissions
        except Exception:
            logger.error("Failed to create data directory")
    
    def load_latest_commitments(self) -> List[Dict]:
        """Load latest corporate commitment data"""
        try:
            pattern = os.path.join(self.data_dir, "commitments_*.json")
            files = glob.glob(pattern)
            if not files:
                return []
            
            latest_file = max(files, key=os.path.getmtime)
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Validate data structure
                if isinstance(data, list):
                    return data[:1000]  # Limit to prevent memory issues
                return []
        except Exception:
            logger.warning("Error loading commitments data")
            return []
    
    def load_latest_funding(self) -> List[Dict]:
        """Load latest funding event data"""
        try:
            pattern = os.path.join(self.data_dir, "funding_*.json")
            files = glob.glob(pattern)
            if not files:
                return []
            
            latest_file = max(files, key=os.path.getmtime)
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Validate data structure
                if isinstance(data, list):
                    return data[:1000]  # Limit to prevent memory issues
                return []
        except Exception:
            logger.warning("Error loading funding data")
            return []
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get summary statistics for dashboard"""
        try:
            commitments = self.load_latest_commitments()
            funding = self.load_latest_funding()
            
            # Calculate key metrics safely
            today = datetime.now().date()
            week_ago = today - timedelta(days=7)
            
            recent_commitments = []
            recent_funding = []
            
            for c in commitments:
                try:
                    if datetime.strptime(c['announcement_date'], '%Y-%m-%d').date() >= week_ago:
                        recent_commitments.append(c)
                except (KeyError, ValueError, TypeError):
                    continue
            
            for f in funding:
                try:
                    if datetime.strptime(f['announcement_date'], '%Y-%m-%d').date() >= week_ago:
                        recent_funding.append(f)
                except (KeyError, ValueError, TypeError):
                    continue
            
            high_value_commitments = [c for c in commitments 
                                    if isinstance(c.get('relevance_score'), (int, float)) and c['relevance_score'] > 0.6]
            competitive_threats = [f for f in funding 
                                 if isinstance(f.get('competitive_threat'), (int, float)) and f['competitive_threat'] > 0.6]
            partnership_opps = [f for f in funding 
                              if isinstance(f.get('partnership_opportunity'), (int, float)) and f['partnership_opportunity'] > 0.6]
            
            total_funding_value = 0
            for f in funding:
                try:
                    amount = self.parse_funding_amount(f.get('amount', '0'))
                    if isinstance(amount, (int, float)) and amount > 0:
                        total_funding_value += amount
                except:
                    continue
            
            return {
                'total_commitments': len(commitments),
                'recent_commitments': len(recent_commitments),
                'high_value_commitments': len(high_value_commitments),
                'total_funding_events': len(funding),
                'recent_funding_events': len(recent_funding),
                'total_funding_value': f"${total_funding_value:.1f}M",
                'competitive_threats': len(competitive_threats),
                'partnership_opportunities': len(partnership_opps),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M UTC')
            }
        except Exception:
            logger.error("Error generating dashboard summary")
            return {
                'total_commitments': 0,
                'recent_commitments': 0,
                'high_value_commitments': 0,
                'total_funding_events': 0,
                'recent_funding_events': 0,
                'total_funding_value': "$0.0M",
                'competitive_threats': 0,
                'partnership_opportunities': 0,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M UTC')
            }
    
    def parse_funding_amount(self, amount_str: str) -> float:
        """Parse funding amount to numeric value in millions"""
        try:
            if not amount_str or not isinstance(amount_str, str):
                return 0.0
            
            # Remove common formatting
            clean_amount = re.sub(r'[^\d.MBK]', '', amount_str.upper())
            match = re.search(r'(\d+(?:\.\d+)?)', clean_amount)
            if not match:
                return 0.0
            
            value = float(match.group(1))
            
            if 'B' in clean_amount:
                return value * 1000
            elif 'M' in clean_amount:
                return value
            elif 'K' in clean_amount:
                return value / 1000
            else:
                return value
        except:
            return 0.0

# Initialize data handler
dashboard_data = DashboardData()

@app.route('/')
def dashboard():
    """Main dashboard page - public access"""
    try:
        summary = dashboard_data.get_dashboard_summary()
        return render_template('dashboard.html', summary=summary)
    except Exception:
        logger.error("Error rendering dashboard")
        abort(500)

@app.route('/api/commitments')
@require_api_key
def api_commitments():
    """API endpoint for commitment data - requires API key"""
    params = validate_query_params()
    
    try:
        commitments = dashboard_data.load_latest_commitments()
        
        # Filter by date
        cutoff_date = datetime.now() - timedelta(days=params['days_back'])
        filtered = []
        
        for c in commitments:
            try:
                if datetime.strptime(c['announcement_date'], '%Y-%m-%d') >= cutoff_date:
                    filtered.append(c)
            except (KeyError, ValueError, TypeError):
                continue
        
        # Filter by relevance
        if params['min_relevance'] > 0:
            filtered = [c for c in filtered 
                       if isinstance(c.get('relevance_score'), (int, float)) and 
                          c['relevance_score'] >= params['min_relevance']]
        
        # Filter by type
        if params['commitment_type']:
            filtered = [c for c in filtered 
                       if c.get('commitment_type') == params['commitment_type']]
        
        return jsonify({
            'commitments': filtered[:100],  # Limit response size
            'total': len(filtered),
            'filters_applied': {
                'min_relevance': params['min_relevance'],
                'commitment_type': params['commitment_type'],
                'days_back': params['days_back']
            }
        })
    except Exception:
        logger.error("Error processing commitments API")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/funding')
@require_api_key  
def api_funding():
    """API endpoint for funding data - requires API key"""
    params = validate_query_params()
    
    try:
        funding = dashboard_data.load_latest_funding()
        
        # Filter by date
        cutoff_date = datetime.now() - timedelta(days=params['days_back'])
        filtered = []
        
        for f in funding:
            try:
                if datetime.strptime(f['announcement_date'], '%Y-%m-%d') >= cutoff_date:
                    filtered.append(f)
            except (KeyError, ValueError, TypeError):
                continue
        
        # Apply filters safely
        if params['min_relevance'] > 0:
            filtered = [f for f in filtered 
                       if isinstance(f.get('dovu_relevance'), (int, float)) and 
                          f['dovu_relevance'] >= params['min_relevance']]
        
        if params['sector']:
            filtered = [f for f in filtered if f.get('sector') == params['sector']]
        
        if params['min_threat'] > 0:
            filtered = [f for f in filtered 
                       if isinstance(f.get('competitive_threat'), (int, float)) and 
                          f['competitive_threat'] >= params['min_threat']]
        
        if params['min_partnership'] > 0:
            filtered = [f for f in filtered 
                       if isinstance(f.get('partnership_opportunity'), (int, float)) and 
                          f['partnership_opportunity'] >= params['min_partnership']]
        
        return jsonify({
            'funding_events': filtered[:100],  # Limit response size
            'total': len(filtered),
            'filters_applied': {
                'min_relevance': params['min_relevance'],
                'sector': params['sector'],
                'min_threat': params['min_threat'],
                'min_partnership': params['min_partnership'],
                'days_back': params['days_back']
            }
        })
    except Exception:
        logger.error("Error processing funding API")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/alerts')
@require_api_key
def api_alerts():
    """API endpoint for high-priority alerts - requires API key"""
    try:
        commitments = dashboard_data.load_latest_commitments()
        funding = dashboard_data.load_latest_funding()
        
        alerts = []
        
        # High-relevance commitments from last 7 days
        week_ago = datetime.now() - timedelta(days=7)
        
        for commitment in commitments:
            try:
                if (datetime.strptime(commitment['announcement_date'], '%Y-%m-%d') >= week_ago and
                    isinstance(commitment.get('relevance_score'), (int, float)) and
                    commitment['relevance_score'] > 0.6):
                    
                    alerts.append({
                        'type': 'commitment',
                        'priority': 'high',
                        'title': f"🎯 High-Value Commitment: {commitment.get('company', 'Unknown')}",
                        'description': f"{commitment.get('commitment_type', 'Unknown')} target, relevance score {commitment['relevance_score']:.2f}",
                        'action': commitment.get('dovu_opportunity', 'Evaluate opportunity'),
                        'date': commitment['announcement_date'],
                        'source_url': commitment.get('source_url', '')
                    })
            except (KeyError, ValueError, TypeError):
                continue
        
        # Competitive threats
        for threat in funding:
            try:
                if (isinstance(threat.get('competitive_threat'), (int, float)) and 
                    threat['competitive_threat'] > 0.6):
                    
                    alerts.append({
                        'type': 'threat',
                        'priority': 'urgent',
                        'title': f"⚠️ Competitive Threat: {threat.get('company', 'Unknown')}",
                        'description': f"{threat.get('funding_type', 'Funding')} {threat.get('amount', '')} - threat score {threat['competitive_threat']:.2f}",
                        'action': "Monitor product development and market positioning",
                        'date': threat.get('announcement_date', ''),
                        'source_url': threat.get('source_url', '')
                    })
            except (KeyError, ValueError, TypeError):
                continue
        
        # Partnership opportunities  
        for opp in funding:
            try:
                if (isinstance(opp.get('partnership_opportunity'), (int, float)) and 
                    opp['partnership_opportunity'] > 0.6):
                    
                    alerts.append({
                        'type': 'partnership',
                        'priority': 'medium',
                        'title': f"🤝 Partnership Opportunity: {opp.get('company', 'Unknown')}",
                        'description': f"{opp.get('business_model', 'Unknown model')} - partnership score {opp['partnership_opportunity']:.2f}",
                        'action': "Evaluate integration and partnership potential",
                        'date': opp.get('announcement_date', ''),
                        'source_url': opp.get('source_url', '')
                    })
            except (KeyError, ValueError, TypeError):
                continue
        
        # Sort by date (newest first)
        alerts.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return jsonify({
            'alerts': alerts[:20],  # Limit to top 20
            'total': len(alerts)
        })
    except Exception:
        logger.error("Error processing alerts API")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics - public access"""
    try:
        return jsonify(dashboard_data.get_dashboard_summary())
    except Exception:
        logger.error("Error processing stats API")
        return jsonify({'error': 'Internal server error'}), 500

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized'}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Forbidden'}), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get port from environment (for cloud deployment) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Force production mode for security
    debug = False
    
    if not os.environ.get('CARBON_DASHBOARD_API_KEY'):
        print("⚠️  WARNING: CARBON_DASHBOARD_API_KEY environment variable not set!")
        print("API endpoints will be unavailable until configured.")
    
    print(f"🚀 Starting SECURE Carbon Deal Intelligence Dashboard...")
    print(f"🔒 API Key Protection: {'Enabled' if os.environ.get('CARBON_DASHBOARD_API_KEY') else 'DISABLED'}")
    print(f"🌐 Port: {port}")
    print(f"🔧 Debug: {debug}")
    
    # Run with secure settings
    app.run(debug=debug, host='0.0.0.0', port=port)