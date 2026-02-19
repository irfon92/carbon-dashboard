# Deploy Carbon Deal Intelligence Dashboard

## Railway Deployment (Recommended)

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub account

### Step 2: Deploy from GitHub
1. Push this folder to a GitHub repo
2. In Railway: "New Project" → "Deploy from GitHub repo"
3. Select your carbon-dashboard repo
4. Railway auto-detects and deploys

### Step 3: Access Your Dashboard
- Railway provides a custom URL (e.g. `https://carbon-dashboard-production.up.railway.app`)
- Share this URL with your team - no VPN needed!

## Alternative: Heroku Deployment

### Step 1: Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Login
heroku login
```

### Step 2: Create and Deploy
```bash
cd carbon-dashboard
git init
git add .
git commit -m "Initial dashboard deployment"

heroku create your-carbon-dashboard
git push heroku main
```

### Step 3: Access
- Heroku provides URL: `https://your-carbon-dashboard.herokuapp.com`

## What Your Team Gets

🌐 **Public URL** - accessible from anywhere
📊 **Live Dashboard** - real-time carbon market intelligence  
🔄 **Auto-updates** - dashboard refreshes with latest data
🔒 **Secure** - HTTPS by default

## Demo Data Included
- 4 high-relevance corporate commitments
- 3 competitive threats (CarbonChain, Sylvera, Persefoni)
- 2 partnership opportunities
- Real-time filtering and alerts

## Next Steps
1. Share public URL with team
2. Train team on DOVU relevance scoring
3. Use intelligence for fundraise conversations
4. Connect real data sources for production use