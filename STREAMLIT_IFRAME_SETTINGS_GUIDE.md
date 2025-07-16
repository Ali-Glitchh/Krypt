# 🔧 Streamlit Cloud iframe Settings Guide
## Configure Your App for Perfect iframe Embedding

## 🎯 Where to Find iframe Settings in Streamlit Cloud

### 1. App Settings in Streamlit Cloud Dashboard

After deploying to [share.streamlit.io](https://share.streamlit.io):

1. **Go to your app dashboard**
2. **Click on your deployed app**
3. **Click the "⋮" menu (three dots)**
4. **Select "Settings"**

### 2. Key iframe Configuration Settings

#### A. Advanced Settings
```
Repository: your-username/kointoss-iframe
Branch: main
Main file path: app.py
Python version: 3.9 (or latest)
```

#### B. Environment Variables (if needed)
```
STREAMLIT_SERVER_HEADLESS = true
STREAMLIT_SERVER_ENABLE_CORS = true
STREAMLIT_BROWSER_GATHER_USAGE_STATS = false
```

#### C. Secrets (for API keys)
```
[secrets]
COINGECKO_API_KEY = "your_api_key_here"
CRYPTOCOMPARE_API_KEY = "your_api_key_here"
```

## 🛠️ iframe-Specific Configuration Files

### 1. Update your .streamlit/config.toml
Your `kointoss-iframe-deploy/.streamlit/config.toml` should have:

```toml
[server]
headless = true
port = 8501
enableCORS = true
enableXsrfProtection = false

[browser]
gatherUsageStats = false
showErrorDetails = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[client]
caching = true
displayEnabled = true

[runner]
magicEnabled = true
installTracer = false
fixMatplotlib = true
```

### 2. Add iframe Headers in Your App
Add this to your `app.py`:

```python
import streamlit as st

# iframe optimization headers
st.set_page_config(
    page_title="KoinToss AI Assistant",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Add iframe-specific meta tags
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-Frame-Options" content="ALLOWALL">
<meta http-equiv="Content-Security-Policy" content="frame-ancestors *;">
""", unsafe_allow_html=True)
```

## 📱 Streamlit Cloud iframe Settings Checklist

### ✅ Repository Settings
- [ ] Repository is public (required for free tier)
- [ ] Main file path: `app.py`
- [ ] Python version: 3.9+
- [ ] Requirements.txt includes all dependencies

### ✅ iframe Optimization Settings
- [ ] headless = true
- [ ] enableCORS = true
- [ ] gatherUsageStats = false
- [ ] showErrorDetails = false
- [ ] Menu items disabled

### ✅ Security Settings for iframe
- [ ] X-Frame-Options: ALLOWALL
- [ ] Content-Security-Policy: frame-ancestors *
- [ ] enableXsrfProtection = false (for iframe)

## 🚀 Step-by-Step Deployment with iframe Settings

### Step 1: Prepare Your Repository
```bash
cd kointoss-iframe-deploy
git init
git add .
git commit -m "KoinToss iframe app ready"
git remote add origin https://github.com/YOUR_USERNAME/kointoss-iframe
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Visit: https://share.streamlit.io
2. Click "New app"
3. **Repository**: your-username/kointoss-iframe
4. **Branch**: main
5. **Main file path**: app.py
6. **Advanced settings**:
   - Python version: 3.9
   - Enable CORS: ✅
   - Headless mode: ✅

### Step 3: Configure iframe Settings
After deployment, in your app settings:

#### Environment Variables:
```
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
STREAMLIT_CLIENT_DISPLAY_ENABLED=true
```

#### Secrets (if using APIs):
```toml
[secrets]
# Add your API keys here
api_key = "your_secret_key"
```

## 🎯 iframe URL Configuration

Once deployed, your app will have a URL like:
```
https://your-username-kointoss-iframe-app-hash.streamlit.app
```

### Use this URL in your iframe:
```html
<iframe 
    src="https://your-username-kointoss-iframe-app-hash.streamlit.app"
    width="100%" 
    height="600px"
    frameborder="0"
    allow="fullscreen"
    sandbox="allow-same-origin allow-scripts allow-popups allow-forms">
</iframe>
```

## 🔧 Troubleshooting iframe Issues

### Issue: App not loading in iframe
**Solution**: Check these settings in Streamlit Cloud:
```toml
[server]
enableCORS = true
enableXsrfProtection = false
```

### Issue: Streamlit menu visible in iframe
**Solution**: Add to your app.py:
```python
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
.stDecoration {display: none;}
</style>
""", unsafe_allow_html=True)
```

### Issue: App sleeping/not responsive
**Solution**: Use Streamlit Cloud (not free alternatives) for always-on apps

## 📊 Alternative iframe Settings for Different Hosts

### For Railway.app:
```json
{
  "deploy": {
    "startCommand": "streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.enableCORS=true --server.enableXsrfProtection=false"
  }
}
```

### For Render.com:
```yaml
services:
  - type: web
    name: kointoss-iframe
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.enableCORS=true
```

## 🎉 Quick iframe Test

After deployment, test your iframe with this HTML:

```html
<!DOCTYPE html>
<html>
<head>
    <title>KoinToss iframe Test</title>
</head>
<body>
    <h1>Testing KoinToss iframe</h1>
    <iframe 
        src="YOUR_STREAMLIT_CLOUD_URL"
        width="100%" 
        height="600px"
        frameborder="0"
        style="border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
    </iframe>
</body>
</html>
```

## 🎯 Final iframe Settings Summary

**In Streamlit Cloud Dashboard:**
1. ✅ Enable CORS
2. ✅ Disable usage stats
3. ✅ Set headless mode
4. ✅ Configure environment variables

**In Your Code:**
1. ✅ Hide Streamlit UI elements
2. ✅ Set iframe-friendly page config
3. ✅ Add responsive CSS
4. ✅ Configure security headers

Your iframe will be ready for embedding anywhere! 🌍
