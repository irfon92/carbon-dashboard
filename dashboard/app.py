#!/usr/bin/env python3
"""
Carbon Deal Intelligence Dashboard
Real-time web interface for carbon market intelligence
"""

from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import glob

app = Flask(__name__)

class DashboardData:
    def __init__(self, data_dir: str = "../data"):
        # Handle both local and cloud deployment paths
        if not os.path.exists(data_dir):
            data_dir = "data"  # Fallback for cloud deployment
        self.data_dir = data_dir
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_latest_commitments(self) -> List[Dict]:
        """Load latest corporate commitment data"""
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
        """Load latest funding event data"""
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
        """Get summary statistics for dashboard"""
        commitments = self.load_latest_commitments()
        funding = self.load_latest_funding()
        
        # Calculate key metrics
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        
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
        """Parse funding amount to numeric value in millions"""
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
    """API endpoint for commitment data"""
    commitments = dashboard_data.load_latest_commitments()
    
    # Apply filters
    min_relevance = float(request.args.get('min_relevance', 0))
    commitment_type = request.args.get('type')
    days_back = int(request.args.get('days', 30))
    
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
    """API endpoint for funding data"""
    funding = dashboard_data.load_latest_funding()
    
    # Apply filters
    min_relevance = float(request.args.get('min_relevance', 0))
    sector = request.args.get('sector')
    min_threat = float(request.args.get('min_threat', 0))
    min_partnership = float(request.args.get('min_partnership', 0))
    days_back = int(request.args.get('days', 30))
    
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
    """API endpoint for high-priority alerts"""
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
            'date': commitment['announcement_date']
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
            'date': threat['announcement_date']
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
            'date': opp['announcement_date']
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
    # Create data directory if it doesn't exist
    os.makedirs('../data', exist_ok=True)
    
    # Get port from environment (for cloud deployment) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"🚀 Starting Carbon Deal Intelligence Dashboard...")
    print(f"🌐 Port: {port}")
    print(f"🔧 Debug: {debug}")
    
    # Run with environment-appropriate settings
    app.run(debug=debug, host='0.0.0.0', port=port)