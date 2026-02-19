#!/usr/bin/env python3
"""
Carbon Deal Intelligence Dashboard Runner
Orchestrates data collection and starts the web dashboard
"""

import sys
import os
import time
import subprocess
import threading
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrapers.corporate_commitments import CorporateCommitmentsScraper
from scrapers.funding_tracker import ClimateVCTracker

class DashboardOrchestrator:
    def __init__(self):
        self.running = True
        self.data_collection_interval = 3600  # 1 hour
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
    
    def collect_data(self):
        """Run data collection from all sources"""
        print(f"🔄 Starting data collection at {datetime.now().strftime('%H:%M:%S')}")
        
        # Collect corporate commitments
        try:
            print("📊 Collecting corporate commitments...")
            commitments_scraper = CorporateCommitmentsScraper()
            commitments = commitments_scraper.scrape_news_sources()
            
            if commitments:
                commitments_scraper.save_commitments(commitments)
                print(f"✅ Saved {len(commitments)} commitments")
            else:
                print("ℹ️  No new commitments found")
                
        except Exception as e:
            print(f"❌ Error collecting commitments: {e}")
        
        # Collect funding data
        try:
            print("💰 Collecting funding data...")
            funding_tracker = ClimateVCTracker()
            events = funding_tracker.track_funding_sources()
            
            if events:
                funding_tracker.save_funding_events(events)
                print(f"✅ Saved {len(events)} funding events")
            else:
                print("ℹ️  No new funding events found")
                
        except Exception as e:
            print(f"❌ Error collecting funding data: {e}")
        
        print(f"✅ Data collection completed at {datetime.now().strftime('%H:%M:%S')}")
    
    def data_collection_loop(self):
        """Background data collection loop"""
        while self.running:
            self.collect_data()
            
            # Wait for next collection cycle
            for _ in range(self.data_collection_interval):
                if not self.running:
                    break
                time.sleep(1)
    
    def start_dashboard(self):
        """Start the web dashboard"""
        print("🌐 Starting web dashboard on http://localhost:5000")
        
        # Change to dashboard directory
        dashboard_dir = os.path.join(os.path.dirname(__file__), 'dashboard')
        
        try:
            # Start Flask app
            subprocess.run([
                sys.executable, 'app.py'
            ], cwd=dashboard_dir)
        except KeyboardInterrupt:
            print("\n🛑 Dashboard stopped by user")
        except Exception as e:
            print(f"❌ Error starting dashboard: {e}")
    
    def run(self):
        """Run the complete dashboard system"""
        print("🚀 Starting Carbon Deal Intelligence Dashboard")
        print("=" * 50)
        
        # Run initial data collection
        print("📦 Running initial data collection...")
        self.collect_data()
        
        # Start background data collection
        data_thread = threading.Thread(target=self.data_collection_loop, daemon=True)
        data_thread.start()
        print(f"🔄 Background data collection started (interval: {self.data_collection_interval}s)")
        
        # Start web dashboard (this will block)
        try:
            self.start_dashboard()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down dashboard...")
            self.running = False

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--collect-only':
        # Just run data collection once and exit
        orchestrator = DashboardOrchestrator()
        orchestrator.collect_data()
    else:
        # Run full dashboard system
        orchestrator = DashboardOrchestrator()
        orchestrator.run()

if __name__ == "__main__":
    main()