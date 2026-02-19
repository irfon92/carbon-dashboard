#!/usr/bin/env python3
"""
Create demo data for Carbon Deal Intelligence Dashboard
"""

import json
import os
from datetime import datetime, timedelta
import random

def create_demo_commitments():
    """Create sample corporate commitment data"""
    
    demo_companies = [
        {
            "company": "Microsoft Corporation",
            "commitment_type": "carbon-negative",
            "target_year": 2030,
            "commitment_details": "Microsoft commits to be carbon negative by 2030 and remove all historical emissions by 2050",
            "carbon_volume_mentioned": "16 million tons CO2e annually",
            "relevance_score": 0.85,
            "dovu_opportunity": "Supply Chain Carbon Management - Full tokenization and tracking solution"
        },
        {
            "company": "Amazon.com Inc",
            "commitment_type": "net-zero",
            "target_year": 2040,
            "commitment_details": "The Climate Pledge: net-zero carbon emissions by 2040, 10 years ahead of Paris Agreement",
            "carbon_volume_mentioned": "44 million tons CO2e baseline",
            "relevance_score": 0.92,
            "dovu_opportunity": "Comprehensive Decarbonization Platform - End-to-end carbon management"
        },
        {
            "company": "Walmart Inc",
            "commitment_type": "scope-reductions",
            "target_year": 2030,
            "commitment_details": "Reduce Scope 1 and 2 emissions by 35% and Scope 3 emissions by 1 gigaton by 2030",
            "carbon_volume_mentioned": "1 gigaton CO2e scope 3 reductions",
            "relevance_score": 0.78,
            "dovu_opportunity": "Supply Chain Carbon Management - Full tokenization and tracking solution"
        },
        {
            "company": "Unilever PLC",
            "commitment_type": "net-zero",
            "target_year": 2039,
            "commitment_details": "Achieve net-zero emissions across value chain by 2039",
            "carbon_volume_mentioned": None,
            "relevance_score": 0.65,
            "dovu_opportunity": "Carbon Credit Procurement - Registry integration and verification"
        },
        {
            "company": "IKEA Group",
            "commitment_type": "carbon-negative",
            "target_year": 2030,
            "commitment_details": "Become climate positive by 2030 by reducing more greenhouse gases than entire value chain emits",
            "carbon_volume_mentioned": None,
            "relevance_score": 0.71,
            "dovu_opportunity": "Comprehensive Decarbonization Platform - End-to-end carbon management"
        }
    ]
    
    commitments = []
    for i, company_data in enumerate(demo_companies):
        commitment_date = datetime.now() - timedelta(days=random.randint(1, 30))
        
        commitment = {
            "company": company_data["company"],
            "announcement_date": commitment_date.strftime('%Y-%m-%d'),
            "commitment_type": company_data["commitment_type"],
            "target_year": company_data["target_year"],
            "baseline_year": None,
            "commitment_details": company_data["commitment_details"],
            "carbon_volume_mentioned": company_data["carbon_volume_mentioned"],
            "source_url": f"https://example.com/news/{i+1}",
            "relevance_score": company_data["relevance_score"],
            "dovu_opportunity": company_data["dovu_opportunity"]
        }
        commitments.append(commitment)
    
    return commitments

def create_demo_funding():
    """Create sample funding event data"""
    
    demo_funding = [
        {
            "company": "CarbonChain",
            "funding_type": "Series A",
            "amount": "$5M",
            "valuation": None,
            "investors": ["Bessemer Venture Partners", "Connect Ventures"],
            "sector": "carbon-management",
            "business_model": "software-platform",
            "stage": "growth",
            "dovu_relevance": 0.95,
            "competitive_threat": 0.85,
            "partnership_opportunity": 0.3
        },
        {
            "company": "Pachama",
            "funding_type": "Series B",
            "amount": "$55M",
            "valuation": None,
            "investors": ["Lowercarbon Capital", "Future Positive Capital", "Breakthrough Energy Ventures"],
            "sector": "nature-based-solutions",
            "business_model": "software-platform",
            "stage": "growth",
            "dovu_relevance": 0.72,
            "competitive_threat": 0.65,
            "partnership_opportunity": 0.80
        },
        {
            "company": "Sylvera",
            "funding_type": "Series A",
            "amount": "$32M",
            "valuation": None,
            "investors": ["Index Ventures", "Insight Partners"],
            "sector": "carbon-management",
            "business_model": "software-platform",
            "stage": "growth",
            "dovu_relevance": 0.88,
            "competitive_threat": 0.75,
            "partnership_opportunity": 0.65
        },
        {
            "company": "Running Tide",
            "funding_type": "Series A",
            "amount": "$8M",
            "valuation": None,
            "investors": ["Union Square Ventures", "Lowercarbon Capital"],
            "sector": "carbon-removal",
            "business_model": "hardware",
            "stage": "growth",
            "dovu_relevance": 0.45,
            "competitive_threat": 0.20,
            "partnership_opportunity": 0.75
        },
        {
            "company": "Persefoni",
            "funding_type": "Series B",
            "amount": "$101M",
            "valuation": "$1B",
            "investors": ["Lightspeed Venture Partners", "TPG Rise"],
            "sector": "carbon-management",
            "business_model": "software-platform",
            "stage": "mature",
            "dovu_relevance": 0.82,
            "competitive_threat": 0.90,
            "partnership_opportunity": 0.40
        }
    ]
    
    events = []
    for i, event_data in enumerate(demo_funding):
        event_date = datetime.now() - timedelta(days=random.randint(1, 30))
        
        event = {
            "company": event_data["company"],
            "funding_type": event_data["funding_type"],
            "amount": event_data["amount"],
            "valuation": event_data.get("valuation"),
            "investors": event_data["investors"],
            "announcement_date": event_date.strftime('%Y-%m-%d'),
            "sector": event_data["sector"],
            "business_model": event_data["business_model"],
            "stage": event_data["stage"],
            "source_url": f"https://example.com/funding/{i+1}",
            "dovu_relevance": event_data["dovu_relevance"],
            "competitive_threat": event_data["competitive_threat"],
            "partnership_opportunity": event_data["partnership_opportunity"]
        }
        events.append(event)
    
    return events

def main():
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Generate demo data
    commitments = create_demo_commitments()
    funding_events = create_demo_funding()
    
    # Save to files
    today = datetime.now().strftime('%Y%m%d')
    
    with open(f'data/commitments_{today}.json', 'w') as f:
        json.dump(commitments, f, indent=2)
    
    with open(f'data/funding_{today}.json', 'w') as f:
        json.dump(funding_events, f, indent=2)
    
    print(f"✅ Demo data created:")
    print(f"   • {len(commitments)} corporate commitments")
    print(f"   • {len(funding_events)} funding events")
    print(f"   • Saved to data/commitments_{today}.json and data/funding_{today}.json")
    print()
    print("📊 Key highlights:")
    
    high_relevance_commitments = [c for c in commitments if c['relevance_score'] > 0.7]
    competitive_threats = [f for f in funding_events if f['competitive_threat'] > 0.7]
    partnership_opps = [f for f in funding_events if f['partnership_opportunity'] > 0.7]
    
    print(f"   • {len(high_relevance_commitments)} high-relevance commitments")
    print(f"   • {len(competitive_threats)} competitive threats")
    print(f"   • {len(partnership_opps)} partnership opportunities")

if __name__ == "__main__":
    main()