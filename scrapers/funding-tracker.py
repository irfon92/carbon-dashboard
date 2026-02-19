#!/usr/bin/env python3
"""
Climate Tech Funding Tracker
Monitors VC funding, acquisitions, and partnerships in carbon/climate space
"""

import requests
import json
import re
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import time

@dataclass
class FundingEvent:
    company: str
    funding_type: str  # Series A/B/C, acquisition, partnership
    amount: Optional[str]
    valuation: Optional[str]
    investors: List[str]
    announcement_date: str
    sector: str  # carbon-management, renewable-energy, climate-tech
    business_model: str
    stage: str  # seed, growth, mature
    source_url: str
    dovu_relevance: float
    competitive_threat: float
    partnership_opportunity: float

class ClimateVCTracker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        # Keywords for carbon/climate relevance
        self.carbon_keywords = [
            'carbon credit', 'carbon offset', 'carbon market', 'carbon trading',
            'carbon management', 'carbon accounting', 'carbon footprint',
            'voluntary carbon market', 'compliance carbon', 'nature-based solutions',
            'reforestation', 'afforestation', 'renewable energy credits',
            'sustainability software', 'ESG platform', 'climate tech'
        ]
    
    def track_funding_sources(self) -> List[FundingEvent]:
        """Track funding from multiple sources"""
        sources = [
            self.track_techcrunch_climate(),
            self.track_climatetech_vc(),
            self.track_pitchbook_climate(),
            self.track_crunchbase_carbon(),
        ]
        
        events = []
        for source_results in sources:
            events.extend(source_results)
            time.sleep(3)  # Rate limiting
        
        return events
    
    def track_techcrunch_climate(self) -> List[FundingEvent]:
        """TechCrunch climate tech funding news"""
        try:
            # TechCrunch doesn't have a direct API, would need RSS or web scraping
            url = "https://techcrunch.com/category/climate/"
            response = self.session.get(url, timeout=10)
            
            events = []
            # Parse for funding announcements
            # This would need proper HTML parsing
            
            return events
        except Exception as e:
            print(f"Error tracking TechCrunch: {e}")
            return []
    
    def track_climatetech_vc(self) -> List[FundingEvent]:
        """Climate Tech VC database tracking"""
        try:
            # ClimateVCAPI or similar service
            url = "https://www.climatetechlist.com/api/companies"
            
            events = []
            # This would integrate with actual climate tech APIs
            
            return events
        except Exception as e:
            print(f"Error tracking Climate VC: {e}")
            return []
    
    def track_pitchbook_climate(self) -> List[FundingEvent]:
        """PitchBook climate sector tracking"""
        # Note: PitchBook requires subscription/API access
        # This is a placeholder for the integration
        return []
    
    def track_crunchbase_carbon(self) -> List[FundingEvent]:
        """Crunchbase carbon management companies"""
        try:
            # Crunchbase API requires key - placeholder for now
            # Would search for companies with carbon-related keywords
            
            # Mock data for demonstration
            mock_events = [
                {
                    "company": "CarbonChain",
                    "funding_type": "Series A",
                    "amount": "$5M",
                    "investors": ["Bessemer", "Connect Ventures"],
                    "announcement_date": "2026-02-15",
                    "sector": "carbon-management",
                    "description": "Supply chain carbon accounting platform"
                },
                {
                    "company": "Pachama",
                    "funding_type": "Series B", 
                    "amount": "$55M",
                    "investors": ["Lowercarbon Capital", "Future Positive"],
                    "announcement_date": "2026-02-10",
                    "sector": "nature-based-solutions",
                    "description": "Forest carbon monitoring and verification"
                }
            ]
            
            events = []
            for event_data in mock_events:
                event = self.process_funding_event(event_data)
                if event:
                    events.append(event)
            
            return events
            
        except Exception as e:
            print(f"Error tracking Crunchbase: {e}")
            return []
    
    def process_funding_event(self, raw_data: Dict) -> Optional[FundingEvent]:
        """Process raw funding data into structured event"""
        
        # Calculate relevance scores
        dovu_relevance = self.calculate_dovu_relevance(raw_data)
        competitive_threat = self.calculate_competitive_threat(raw_data)
        partnership_opportunity = self.calculate_partnership_opportunity(raw_data)
        
        # Classify business model
        business_model = self.classify_business_model(raw_data.get('description', ''))
        
        # Determine stage
        stage = self.determine_stage(raw_data.get('funding_type', ''), raw_data.get('amount', ''))
        
        return FundingEvent(
            company=raw_data.get('company', ''),
            funding_type=raw_data.get('funding_type', ''),
            amount=raw_data.get('amount'),
            valuation=raw_data.get('valuation'),
            investors=raw_data.get('investors', []),
            announcement_date=raw_data.get('announcement_date', ''),
            sector=raw_data.get('sector', ''),
            business_model=business_model,
            stage=stage,
            source_url=raw_data.get('source_url', ''),
            dovu_relevance=dovu_relevance,
            competitive_threat=competitive_threat,
            partnership_opportunity=partnership_opportunity
        )
    
    def calculate_dovu_relevance(self, data: Dict) -> float:
        """Calculate how relevant this funding is to DOVU (0-1)"""
        score = 0.0
        
        description = data.get('description', '').lower()
        sector = data.get('sector', '').lower()
        
        # Direct carbon management relevance
        if any(keyword in description for keyword in ['carbon credit', 'carbon trading', 'carbon platform']):
            score += 0.4
        
        # Supply chain carbon
        if any(keyword in description for keyword in ['supply chain', 'scope 3', 'value chain']):
            score += 0.3
        
        # Tokenization/blockchain
        if any(keyword in description for keyword in ['tokenization', 'blockchain', 'digital asset']):
            score += 0.2
        
        # Enterprise software
        if any(keyword in description for keyword in ['enterprise', 'b2b', 'platform', 'saas']):
            score += 0.1
        
        # Sector relevance
        if sector in ['carbon-management', 'climate-tech', 'sustainability-software']:
            score += 0.2
        
        return min(score, 1.0)
    
    def calculate_competitive_threat(self, data: Dict) -> float:
        """Calculate competitive threat level (0-1)"""
        score = 0.0
        
        description = data.get('description', '').lower()
        funding_amount = data.get('amount', '0')
        
        # Direct competition indicators
        if 'carbon credit' in description and 'platform' in description:
            score += 0.6
        
        if 'tokenization' in description and 'carbon' in description:
            score += 0.7
        
        # Funding size threat multiplier
        amount_value = self.parse_funding_amount(funding_amount)
        if amount_value:
            if amount_value > 50:  # >$50M
                score *= 1.5
            elif amount_value > 20:  # >$20M  
                score *= 1.2
        
        return min(score, 1.0)
    
    def calculate_partnership_opportunity(self, data: Dict) -> float:
        """Calculate partnership opportunity score (0-1)"""
        score = 0.0
        
        description = data.get('description', '').lower()
        
        # Complementary technologies
        if any(keyword in description for keyword in ['monitoring', 'verification', 'measurement']):
            score += 0.3
        
        if any(keyword in description for keyword in ['api', 'data', 'registry']):
            score += 0.3
        
        # Geographic expansion
        if any(keyword in description for keyword in ['global', 'international', 'expansion']):
            score += 0.2
        
        # Enterprise focus
        if any(keyword in description for keyword in ['enterprise', 'corporate', 'b2b']):
            score += 0.2
        
        return min(score, 1.0)
    
    def classify_business_model(self, description: str) -> str:
        """Classify company business model"""
        desc_lower = description.lower()
        
        if 'marketplace' in desc_lower or 'trading' in desc_lower:
            return "marketplace"
        elif 'saas' in desc_lower or 'platform' in desc_lower or 'software' in desc_lower:
            return "software-platform"
        elif 'consulting' in desc_lower or 'advisory' in desc_lower:
            return "services"
        elif 'hardware' in desc_lower or 'device' in desc_lower:
            return "hardware"
        else:
            return "other"
    
    def determine_stage(self, funding_type: str, amount: str) -> str:
        """Determine company stage from funding info"""
        if funding_type.lower() in ['seed', 'pre-seed']:
            return "seed"
        elif funding_type.lower() in ['series a', 'series b']:
            return "growth"
        elif funding_type.lower() in ['series c', 'series d', 'series e']:
            return "mature"
        elif 'acquisition' in funding_type.lower():
            return "exit"
        else:
            # Determine by amount
            amount_value = self.parse_funding_amount(amount)
            if amount_value and amount_value < 5:
                return "seed"
            elif amount_value and amount_value < 25:
                return "growth"
            else:
                return "mature"
    
    def parse_funding_amount(self, amount_str: str) -> Optional[float]:
        """Parse funding amount string to numeric value in millions"""
        if not amount_str:
            return None
        
        # Extract numeric value
        match = re.search(r'(\d+(?:\.\d+)?)', amount_str.replace(',', ''))
        if not match:
            return None
        
        value = float(match.group(1))
        
        # Convert to millions
        if 'B' in amount_str.upper() or 'billion' in amount_str.lower():
            return value * 1000
        elif 'M' in amount_str.upper() or 'million' in amount_str.lower():
            return value
        elif 'K' in amount_str.upper() or 'thousand' in amount_str.lower():
            return value / 1000
        else:
            # Assume millions if no unit specified
            return value
    
    def save_funding_events(self, events: List[FundingEvent], filename: str = None):
        """Save funding events to JSON file"""
        if not filename:
            filename = f"data/funding_{datetime.now().strftime('%Y%m%d')}.json"
        
        data = [asdict(event) for event in events]
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved {len(events)} funding events to {filename}")

def main():
    tracker = ClimateVCTracker()
    events = tracker.track_funding_sources()
    
    if events:
        tracker.save_funding_events(events)
        
        # Analyze key insights
        high_relevance = [e for e in events if e.dovu_relevance > 0.5]
        threats = [e for e in events if e.competitive_threat > 0.6]
        partnerships = [e for e in events if e.partnership_opportunity > 0.6]
        
        print(f"\n📊 FUNDING INTELLIGENCE SUMMARY:")
        print(f"• {len(events)} total funding events tracked")
        print(f"• {len(high_relevance)} high-relevance to DOVU")
        print(f"• {len(threats)} potential competitive threats")
        print(f"• {len(partnerships)} partnership opportunities")
        
        if threats:
            print(f"\n🚨 COMPETITIVE THREATS:")
            for threat in threats:
                print(f"• {threat.company} - {threat.funding_type} {threat.amount}")
                print(f"  Threat Score: {threat.competitive_threat:.2f}")
        
        if partnerships:
            print(f"\n🤝 PARTNERSHIP OPPORTUNITIES:")
            for opp in partnerships:
                print(f"• {opp.company} - {opp.business_model}")
                print(f"  Partnership Score: {opp.partnership_opportunity:.2f}")

if __name__ == "__main__":
    main()