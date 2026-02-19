#!/usr/bin/env python3
"""
Carbon Deal Intelligence Dashboard - Public Version
Open access for team collaboration
"""

from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import glob

app = Flask(__name__)

# Security headers (keep these for basic protection)
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

class DashboardData:
    def __init__(self, data_dir: str = "../data"):
        if not os.path.exists(data_dir):
            data_dir = "data"
        self.data_dir = data_dir
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_latest_commitments(self) -> List[Dict]:
        try:
            pattern = os.path.join(self.data_dir, "commitments_*.json")
            files = glob.glob(pattern)
            if not files:
                return []
            
            latest_file = max(files, key=os.path.getmtime)
            with open(latest_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading commitments: {e}")
            return []
    
    def load_latest_funding(self) -> List[Dict]:
        try:
            pattern = os.path.join(self.data_dir, "funding_*.json")
            files = glob.glob(pattern)
            if not files:
                return []
            
            latest_file = max(files, key=os.path.getmtime)
            with open(latest_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading funding data: {e}")
            return []
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        commitments = self.load_latest_commitments()
        funding = self.load_latest_funding()
        
        today = datetime.now().date()
        six_months_ago = today - timedelta(days=180)  # 6 months filter
        week_ago = today - timedelta(days=7)
        
        # Filter all data to last 6 months
        commitments = [
            c for c in commitments 
            if datetime.strptime(c['announcement_date'], '%Y-%m-%d').date() >= six_months_ago
        ]
        
        funding = [
            f for f in funding
            if datetime.strptime(f['announcement_date'], '%Y-%m-%d').date() >= six_months_ago
        ]
        
        recent_commitments = [
            c for c in commitments 
            if datetime.strptime(c['announcement_date'], '%Y-%m-%d').date() >= week_ago
        ]
        
        recent_funding = [
            f for f in funding
            if datetime.strptime(f['announcement_date'], '%Y-%m-%d').date() >= week_ago
        ]
        
        high_value_commitments = [c for c in commitments if c['relevance_score'] > 0.6]
        competitive_threats = [f for f in funding if f.get('competitive_threat', 0) > 0.6]
        partnership_opps = [f for f in funding if f.get('partnership_opportunity', 0) > 0.6]
        
        total_funding_value = sum([
            self.parse_funding_amount(f.get('amount', '0')) or 0 
            for f in funding
        ])
        
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
    
    def parse_funding_amount(self, amount_str: str) -> float:
        if not amount_str:
            return 0.0
        
        import re
        match = re.search(r'(\d+(?:\.\d+)?)', amount_str.replace(',', ''))
        if not match:
            return 0.0
        
        value = float(match.group(1))
        
        if 'B' in amount_str.upper() or 'billion' in amount_str.lower():
            return value * 1000
        elif 'M' in amount_str.upper() or 'million' in amount_str.lower():
            return value
        elif 'K' in amount_str.upper() or 'thousand' in amount_str.lower():
            return value / 1000
        else:
            return value

# Initialize data handler
dashboard_data = DashboardData()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    summary = dashboard_data.get_dashboard_summary()
    return render_template('dashboard.html', summary=summary)

@app.route('/api/commitments')
def api_commitments():
    """API endpoint for commitment data - OPEN ACCESS"""
    commitments = dashboard_data.load_latest_commitments()
    
    # Apply filters with safe defaults - 6 months max
    try:
        min_relevance = max(0, min(1, float(request.args.get('min_relevance', 0))))
        days_back = max(1, min(180, int(request.args.get('days', 180))))  # Default and max: 6 months
        commitment_type = request.args.get('type', '')
    except:
        min_relevance = 0
        days_back = 180  # Default to 6 months
        commitment_type = ''
    
    # Filter by date
    cutoff_date = datetime.now() - timedelta(days=days_back)
    filtered = [
        c for c in commitments
        if datetime.strptime(c['announcement_date'], '%Y-%m-%d') >= cutoff_date
    ]
    
    # Filter by relevance
    if min_relevance > 0:
        filtered = [c for c in filtered if c['relevance_score'] >= min_relevance]
    
    # Filter by type
    if commitment_type:
        filtered = [c for c in filtered if c['commitment_type'] == commitment_type]
    
    return jsonify({
        'commitments': filtered,
        'total': len(filtered),
        'filters_applied': {
            'min_relevance': min_relevance,
            'commitment_type': commitment_type,
            'days_back': days_back
        }
    })

@app.route('/api/funding')
def api_funding():
    """API endpoint for funding data - OPEN ACCESS"""
    funding = dashboard_data.load_latest_funding()
    
    # Apply filters with safe defaults - 6 months max
    try:
        min_relevance = max(0, min(1, float(request.args.get('min_relevance', 0))))
        days_back = max(1, min(180, int(request.args.get('days', 180))))  # Default and max: 6 months
        sector = request.args.get('sector', '')
        min_threat = max(0, min(1, float(request.args.get('min_threat', 0))))
        min_partnership = max(0, min(1, float(request.args.get('min_partnership', 0))))
    except:
        min_relevance = 0
        days_back = 180  # Default to 6 months
        sector = ''
        min_threat = 0
        min_partnership = 0
    
    # Filter by date
    cutoff_date = datetime.now() - timedelta(days=days_back)
    filtered = [
        f for f in funding
        if datetime.strptime(f['announcement_date'], '%Y-%m-%d') >= cutoff_date
    ]
    
    # Apply filters
    if min_relevance > 0:
        filtered = [f for f in filtered if f.get('dovu_relevance', 0) >= min_relevance]
    
    if sector:
        filtered = [f for f in filtered if f.get('sector') == sector]
    
    if min_threat > 0:
        filtered = [f for f in filtered if f.get('competitive_threat', 0) >= min_threat]
    
    if min_partnership > 0:
        filtered = [f for f in filtered if f.get('partnership_opportunity', 0) >= min_partnership]
    
    return jsonify({
        'funding_events': filtered,
        'total': len(filtered),
        'filters_applied': {
            'min_relevance': min_relevance,
            'sector': sector,
            'min_threat': min_threat,
            'min_partnership': min_partnership,
            'days_back': days_back
        }
    })

@app.route('/api/alerts')
def api_alerts():
    """API endpoint for high-priority alerts - OPEN ACCESS"""
    commitments = dashboard_data.load_latest_commitments()
    funding = dashboard_data.load_latest_funding()
    
    alerts = []
    
    # High-relevance commitments from last 7 days
    week_ago = datetime.now() - timedelta(days=7)
    recent_high_value = [
        c for c in commitments
        if (datetime.strptime(c['announcement_date'], '%Y-%m-%d') >= week_ago 
            and c['relevance_score'] > 0.6)
    ]
    
    for commitment in recent_high_value:
        alerts.append({
            'type': 'commitment',
            'priority': 'high',
            'title': f"🎯 High-Value Commitment: {commitment['company']}",
            'description': f"{commitment['commitment_type']} target, relevance score {commitment['relevance_score']:.2f}",
            'action': commitment['dovu_opportunity'],
            'date': commitment['announcement_date'],
            'source_url': commitment.get('source_url', '')
        })
    
    # Competitive threats
    threats = [f for f in funding if f.get('competitive_threat', 0) > 0.6]
    for threat in threats:
        alerts.append({
            'type': 'threat',
            'priority': 'urgent',
            'title': f"⚠️ Competitive Threat: {threat['company']}",
            'description': f"{threat['funding_type']} {threat.get('amount', '')} - threat score {threat.get('competitive_threat', 0):.2f}",
            'action': "Monitor product development and market positioning",
            'date': threat['announcement_date'],
            'source_url': threat.get('source_url', '')
        })
    
    # Partnership opportunities
    partnerships = [f for f in funding if f.get('partnership_opportunity', 0) > 0.6]
    for opp in partnerships:
        alerts.append({
            'type': 'partnership',
            'priority': 'medium',
            'title': f"🤝 Partnership Opportunity: {opp['company']}",
            'description': f"{opp['business_model']} - partnership score {opp.get('partnership_opportunity', 0):.2f}",
            'action': "Evaluate integration and partnership potential",
            'date': opp['announcement_date'],
            'source_url': opp.get('source_url', '')
        })
    
    # Sort by date (newest first)
    alerts.sort(key=lambda x: x['date'], reverse=True)
    
    return jsonify({
        'alerts': alerts[:20],  # Limit to top 20
        'total': len(alerts)
    })

@app.route('/api/stats')
def api_stats():
    """API endpoint for dashboard statistics"""
    return jsonify(dashboard_data.get_dashboard_summary())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = False  # Keep debug off for security
    
    print(f"🚀 Starting Carbon Deal Intelligence Dashboard...")
    print(f"🌐 OPEN ACCESS - No API key required")
    print(f"🔓 Team can access all endpoints directly")
    print(f"🌐 Port: {port}")
    
    app.run(debug=debug, host='0.0.0.0', port=port)