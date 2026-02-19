# 🔒 SECURE DEPLOYMENT GUIDE

## ⚠️ CRITICAL: Your dashboard is currently UNSECURED

**Current URL**: https://dovucarboninsights.up.railway.app
**Risk**: Anyone can access your competitive intelligence

## 🚀 QUICK SECURE DEPLOYMENT (5 minutes)

### Step 1: Deploy Secure Version

```bash
# Update Procfile for secure app
echo "web: python create_demo_data.py && cd dashboard && python secure_app.py" > Procfile

# Commit and push
git add .
git commit -m "Deploy secure version with API key protection"
git push
```

### Step 2: Configure Environment Variables in Railway

1. Go to https://railway.app/dashboard
2. Select your **carbon-dashboard** project  
3. Go to **Variables** tab
4. Add these variables:

```
CARBON_DASHBOARD_API_KEY=dovu_carbon_intel_2024_secure_key_change_me
SECRET_KEY=your_very_long_random_secret_key_here_change_this
FLASK_ENV=production
```

### Step 3: Test Secure Access

**Public Dashboard**: https://dovucarboninsights.up.railway.app (basic metrics only)

**API Access** (requires API key):
```bash
curl -H "X-API-Key: dovu_carbon_intel_2024_secure_key_change_me" \
  "https://dovucarboninsights.up.railway.app/api/commitments"
```

## 🛡️ SECURITY IMPROVEMENTS ADDED

### ✅ API Key Authentication
- All sensitive endpoints now require `X-API-Key` header
- Public dashboard shows summary only
- Full data requires authentication

### ✅ Input Validation  
- All parameters bounded and sanitized
- Prevents DoS attacks via large queries
- Type validation prevents crashes

### ✅ Security Headers
- `X-Frame-Options: DENY` (prevents clickjacking)
- `X-Content-Type-Options: nosniff`  
- `Strict-Transport-Security` (HSTS)
- `X-XSS-Protection: 1; mode=block`

### ✅ Error Handling
- No internal paths exposed to users
- Generic error messages prevent information leakage
- Secure logging with no sensitive data

### ✅ Resource Limits
- Response size limited to prevent memory exhaustion
- Query time ranges bounded (max 1 year)
- File access with proper error handling

## 🔑 TEAM ACCESS

Share with your team:

**Dashboard URL**: https://dovucarboninsights.up.railway.app (public metrics)

**API Key**: `dovu_carbon_intel_2024_secure_key_change_me` 
- Store securely (password manager)
- Rotate monthly
- Don't commit to code

**API Usage**:
```javascript
fetch('/api/commitments', {
  headers: {
    'X-API-Key': 'dovu_carbon_intel_2024_secure_key_change_me'
  }
})
```

## 🚨 CHANGE DEFAULT KEYS

**IMMEDIATELY change these in Railway variables:**

1. **CARBON_DASHBOARD_API_KEY**: Generate strong random key
2. **SECRET_KEY**: Use `python -c "import secrets; print(secrets.token_hex(32))"`

## ⚡ QUICK DEPLOY COMMANDS

```bash
# Update to secure version
cd carbon-dashboard
cp dashboard/secure_app.py dashboard/app.py
echo "web: python create_demo_data.py && cd dashboard && python app.py" > Procfile
git add .  
git commit -m "Deploy secure version"
git push

# Then configure environment variables in Railway dashboard
```

## 🎯 RESULT

- ✅ **Public dashboard** with basic metrics (safe for marketing)
- 🔒 **Protected APIs** with full competitive intelligence  
- 🛡️ **Security headers** prevent common attacks
- 📊 **Access logging** for monitoring usage
- ⚡ **Performance limits** prevent resource abuse

Your competitive intelligence is now **enterprise-grade secure**! 🔐