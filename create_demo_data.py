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
            "commitment_details": "Microsoft reaffirms carbon negative commitment with new supply chain initiatives and tokenization pilots",
            "carbon_volume_mentioned": "16 million tons CO2e annually",
            "relevance_score": 0.85,
            "dovu_opportunity": "Supply Chain Carbon Management - Full tokenization and tracking solution",
            "source_url": "https://blogs.microsoft.com/blog/2020/01/16/microsoft-will-be-carbon-negative-by-2030/"
        },
        {
            "company": "Amazon.com Inc",
            "commitment_type": "net-zero",
            "target_year": 2040,
            "commitment_details": "Amazon expands Climate Pledge with new carbon accounting requirements for suppliers",
            "carbon_volume_mentioned": "44 million tons CO2e baseline",
            "relevance_score": 0.92,
            "dovu_opportunity": "Comprehensive Decarbonization Platform - End-to-end carbon management",
            "source_url": "https://sustainability.aboutamazon.com/climate-pledge"
        },
        {
            "company": "Walmart Inc",
            "commitment_type": "scope-reductions",
            "target_year": 2030,
            "commitment_details": "Walmart launches Project Gigaton expansion with blockchain-based carbon tracking for suppliers",
            "carbon_volume_mentioned": "1 gigaton CO2e scope 3 reductions",
            "relevance_score": 0.78,
            "dovu_opportunity": "Supply Chain Carbon Management - Full tokenization and tracking solution",
            "source_url": "https://corporate.walmart.com/newsroom/2020/09/21/walmart-sets-goal-to-become-a-regenerative-company"
        },
        {
            "company": "Unilever PLC",
            "commitment_type": "net-zero",
            "target_year": 2039,
            "commitment_details": "Unilever pilots digital carbon tokens for sustainable sourcing across value chain",
            "carbon_volume_mentioned": "5.2 million tons CO2e scope 3",
            "relevance_score": 0.65,
            "dovu_opportunity": "Carbon Credit Procurement - Registry integration and verification",
            "source_url": "https://www.unilever.com/news/news-search/2020/unilever-commits-to-net-zero-emissions-from-all-its-products-by-2039/"
        },
        {
            "company": "IKEA Group",
            "commitment_type": "carbon-negative",
            "target_year": 2030,
            "commitment_details": "IKEA announces partnership with carbon registry platforms for forestry offset tokenization",
            "carbon_volume_mentioned": "2.8 million tons CO2e removals",
            "relevance_score": 0.71,
            "dovu_opportunity": "Comprehensive Decarbonization Platform - End-to-end carbon management",
            "source_url": "https://www.ikea.com/us/en/this-is-ikea/newsroom/ikea-commits-to-become-climate-positive-by-2030-pub44f93660"
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
            "source_url": company_data["source_url"],
            "relevance_score": company_data["relevance_score"],
            "dovu_opportunity": company_data["dovu_opportunity"]
        }
        commitments.append(commitment)
    
    return commitments

def create_demo_funding():
    """Create sample funding event data"""
    
    demo_funding = [
        {
            "company": "CarbonScope",
            "funding_type": "Series B",
            "amount": "$12M",
            "valuation": "$45M",
            "investors": ["Breakthrough Energy Ventures", "Climate Investment Coalition"],
            "sector": "carbon-management",
            "business_model": "software-platform",
            "stage": "growth",
            "dovu_relevance": 0.95,
            "competitive_threat": 0.85,
            "partnership_opportunity": 0.3,
            "source_url": "https://techcrunch.com/2026/01/24/carbonscope-raises-12m-series-b-for-enterprise-carbon-tracking/"
        },
        {
            "company": "ForestLink",
            "funding_type": "Series A",
            "amount": "$25M",
            "valuation": None,
            "investors": ["Lowercarbon Capital", "Future Positive Capital", "Microsoft Climate Fund"],
            "sector": "nature-based-solutions",
            "business_model": "software-platform",
            "stage": "growth",
            "dovu_relevance": 0.72,
            "competitive_threat": 0.65,
            "partnership_opportunity": 0.80,
            "source_url": "https://www.reuters.com/business/sustainable-business/forestlink-secures-25m-series-a-nature-based-carbon-solutions-2026-02-18/"
        },
        {
            "company": "CarbonTracker Pro",
            "funding_type": "Series A",
            "amount": "$18M",
            "valuation": None,
            "investors": ["Index Ventures", "Insight Partners", "Energy Impact Partners"],
            "sector": "carbon-management",
            "business_model": "software-platform",
            "stage": "growth",
            "dovu_relevance": 0.88,
            "competitive_threat": 0.75,
            "partnership_opportunity": 0.65,
            "source_url": "https://www.crunchbase.com/organization/carbontracker-pro/funding_rounds/funding_round"
        },
        {
            "company": "OceanCarbon",
            "funding_type": "Series A",
            "amount": "$15M",
            "valuation": None,
            "investors": ["Union Square Ventures", "Lowercarbon Capital", "Ocean14 Capital"],
            "sector": "carbon-removal",
            "business_model": "hardware",
            "stage": "growth",
            "dovu_relevance": 0.45,
            "competitive_threat": 0.20,
            "partnership_opportunity": 0.75,
            "source_url": "https://www.greentechmedia.com/articles/read/oceancarbon-raises-15m-series-a-marine-carbon-removal"
        },
        {
            "company": "EmissionIQ",
            "funding_type": "Series C",
            "amount": "$85M",
            "valuation": "$750M",
            "investors": ["Lightspeed Venture Partners", "TPG Rise", "Blackstone Growth"],
            "sector": "carbon-management",
            "business_model": "software-platform",
            "stage": "mature",
            "dovu_relevance": 0.82,
            "competitive_threat": 0.90,
            "partnership_opportunity": 0.40,
            "source_url": "https://www.bloomberg.com/news/articles/2026-02-11/emissioniq-raises-85m-series-c-at-750m-valuation-carbon-accounting"
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
            "source_url": event_data["source_url"],
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