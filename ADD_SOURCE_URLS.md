# 🔗 Adding Source URLs to Dashboard

## Overview

Your dashboard now displays clickable source links next to company names, allowing team members to read the original articles and press releases.

## ✅ What's Already Done

### Dashboard UI Updated
- **Corporate Commitments**: Show "🔗 Source" links next to company names
- **Funding Events**: Show "🔗 Source" links with investor information
- **External Links**: Open in new tabs for seamless browsing
- **Smart Display**: Only shows links for real URLs (not placeholder example.com links)

### Demo Data Enhanced
- ✅ **Microsoft**: Links to official carbon-negative announcement
- ✅ **Amazon**: Links to Climate Pledge page  
- ✅ **Walmart**: Links to corporate sustainability announcement
- ✅ **Unilever**: Links to net-zero commitment press release
- ✅ **IKEA**: Links to climate positive announcement
- ✅ **CarbonChain**: Links to TechCrunch funding article
- ✅ **Pachama**: Links to Crunchbase funding info
- ✅ **Sylvera**: Links to TechCrunch Series A coverage
- ✅ **Running Tide**: Links to GreenTech Media article
- ✅ **Persefoni**: Links to Reuters $101M Series B coverage

## 🚀 Deploy Updated Dashboard

```bash
cd carbon-dashboard

# Regenerate demo data with real source URLs
python3 create_demo_data.py

# Commit and deploy
git add .
git commit -m "Add clickable source URLs to dashboard"
git push
```

## 🌐 Result

**Team members can now:**
- **Click source links** to read full articles
- **Verify intelligence** with original sources  
- **Share articles** with prospects and investors
- **Deep-dive research** on specific companies and deals

## 📊 Adding URLs to Future Data

### For Corporate Commitments Scraper

```python
# In scrapers/corporate_commitments.py
def extract_commitment_details(self, content: str, url: str) -> Optional[CarbonCommitment]:
    # ... existing extraction logic ...
    
    return CarbonCommitment(
        company=company,
        # ... other fields ...
        source_url=url,  # Use the actual article URL
        # ... remaining fields ...
    )
```

### For Funding Tracker

```python  
# In scrapers/funding_tracker.py
def process_funding_event(self, raw_data: Dict) -> Optional[FundingEvent]:
    # ... existing processing ...
    
    return FundingEvent(
        company=raw_data.get('company', ''),
        # ... other fields ...
        source_url=raw_data.get('source_url', ''),  # Include source URL
        # ... remaining fields ...
    )
```

## 🎯 Key Sources to Target

### Corporate Commitments
- **Company press releases** (official announcements)
- **SEC filings** (regulatory disclosures)
- **Sustainability reports** (annual commitments)
- **News coverage** (TechCrunch, Reuters, Bloomberg)

### Funding Events  
- **TechCrunch funding articles**
- **Crunchbase company pages**
- **PitchBook deal announcements**
- **Company blog posts** (funding announcements)
- **VC firm portfolio updates**

## 🔍 Manual URL Addition

To add URLs to existing data files:

```python
# Edit data/commitments_YYYYMMDD.json
{
  "company": "Example Corp",
  // ... other fields ...
  "source_url": "https://techcrunch.com/2024/example-corp-carbon-commitment"
}

# Edit data/funding_YYYYMMDD.json  
{
  "company": "Example Startup",
  // ... other fields ...
  "source_url": "https://techcrunch.com/2024/example-startup-series-a"
}
```

## 📈 Dashboard Impact

**Enhanced User Experience:**
- **Credible intelligence** with verifiable sources
- **Research efficiency** - no manual Google searching  
- **Professional presentations** with source citations
- **Competitive analysis** with full context

**Business Value:**
- **Investor confidence** in data quality
- **Sales team efficiency** with ready research
- **Strategic planning** with complete context
- **Market credibility** through source transparency

## 🚀 Next Steps

1. **Deploy current updates** (real URLs for demo data)
2. **Train team** on using source links for research
3. **Update scrapers** to capture real URLs from news sources
4. **Monitor usage** - see which sources team clicks most
5. **Expand sources** - add more news outlets and data providers

**Your carbon intelligence now has full source transparency!** 🎉