# 🚀 KoinToss iframe Deployment
## Free Hosting for Mobile & Web Integration

This repository contains the iframe-optimized version of KoinToss AI Assistant, designed for seamless embedding in mobile and web applications.

## 🎯 Live Demo
**Deployed App:** `https://kointoss-iframe.streamlit.app` (after deployment)

## 📱 iframe Integration

### For Web Applications
```html
<!-- Full-width iframe -->
<iframe 
  src="https://kointoss-iframe.streamlit.app" 
  width="100%" 
  height="600px"
  frameborder="0"
  allow="fullscreen">
</iframe>

<!-- Mobile-responsive iframe -->
<div style="position: relative; width: 100%; height: 0; padding-bottom: 75%;">
  <iframe 
    src="https://kointoss-iframe.streamlit.app"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
    frameborder="0">
  </iframe>
</div>
```

### For React Applications
```jsx
import React from 'react';

const KoinTossWidget = () => {
  return (
    <iframe 
      src="https://kointoss-iframe.streamlit.app"
      style={{
        width: '100%',
        height: '600px',
        border: 'none',
        borderRadius: '10px'
      }}
      title="KoinToss AI Assistant"
    />
  );
};

export default KoinTossWidget;
```

### For React Native
```javascript
import { WebView } from 'react-native-webview';

const KoinTossScreen = () => {
  return (
    <WebView 
      source={{ uri: 'https://kointoss-iframe.streamlit.app' }}
      style={{ flex: 1 }}
      javaScriptEnabled={true}
      domStorageEnabled={true}
    />
  );
};
```

### For Flutter
```dart
import 'package:webview_flutter/webview_flutter.dart';

class KoinTossWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return WebView(
      initialUrl: 'https://kointoss-iframe.streamlit.app',
      javascriptMode: JavascriptMode.unrestricted,
    );
  }
}
```

## 🛠️ Quick Deployment to Streamlit Cloud

### Step 1: Fork/Clone This Repository
```bash
git clone https://github.com/yourusername/kointoss-iframe
cd kointoss-iframe
```

### Step 2: Deploy to Streamlit Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select this repository
4. Set main file: `kointoss_iframe_app.py`
5. Click "Deploy"

### Step 3: Get Your iframe URL
After deployment, you'll get a URL like:
`https://yourusername-kointoss-iframe-kointoss-iframe-app-xyz123.streamlit.app`

## 🎨 Features Optimized for iframe

- ✅ **Mobile Responsive**: Works perfectly on all screen sizes
- ✅ **No Scrollbars**: Clean interface without Streamlit branding
- ✅ **Fast Loading**: Optimized for iframe embedding
- ✅ **Cross-Origin**: Supports embedding in any domain
- ✅ **Real-time Chat**: Dual personality AI assistant
- ✅ **Crypto Data**: Live market information

## 🔧 Alternative Free Hosting Options

### Railway.app
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### Render.com
1. Connect GitHub repository
2. Select "Web Service"
3. Build Command: `pip install -r requirements_iframe.txt`
4. Start Command: `streamlit run kointoss_iframe_app.py --server.port=$PORT`

### Heroku (with limitations)
```bash
# Create Procfile
echo "web: streamlit run kointoss_iframe_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

## 🎯 Usage Examples

### Simple iframe Embed
```html
<iframe src="YOUR_DEPLOYED_URL" width="400" height="600"></iframe>
```

### Responsive iframe
```css
.iframe-container {
  position: relative;
  overflow: hidden;
  width: 100%;
  padding-top: 75%; /* 4:3 aspect ratio */
}

.iframe-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  width: 100%;
  height: 100%;
}
```

## 📊 Performance & Limits

### Streamlit Cloud (FREE)
- ✅ Unlimited public apps
- ✅ 1GB RAM per app
- ✅ Custom domains
- ✅ Always online

### Railway.app (FREE tier)
- ✅ 500 hours/month
- ✅ 1GB RAM
- ✅ Custom domains
- ⚠️ $5/month after limits

### Render.com (FREE tier)
- ✅ 750 hours/month
- ✅ 512MB RAM
- ⚠️ Sleeps after 15min inactivity

## 🚀 Ready to Deploy?

1. **Recommended**: Use Streamlit Cloud for best iframe experience
2. **Alternative**: Railway.app for custom domain needs
3. **Backup**: Render.com for additional hosting

Your KoinToss AI Assistant will be live and embeddable in minutes! 🎉

## 🔗 Links
- [Streamlit Cloud](https://share.streamlit.io)
- [Railway.app](https://railway.app)
- [Render.com](https://render.com)

---
*Deploy once, embed everywhere! 📱💻*
