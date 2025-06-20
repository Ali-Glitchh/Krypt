# 🚀 Krypt AI Assistant - Iframe & Mobile/Web Integration Guide

## 📋 Overview

The Krypt AI Assistant is now fully embeddable and ready for integration into your mobile apps and websites. This guide covers all integration methods and features.

## ✨ Features

### 🤖 **Core AI Capabilities**
- **Real-time Crypto Prices** - Live data from CoinGecko and KuCoin APIs
- **Market News & Insights** - Latest crypto news and market analysis
- **Custom Article Insights** - AI analysis of your own article content
- **Natural Conversation** - Human-like chat trained on 730+ conversation pairs
- **Dual Personality Mode** - Switch between Normal and Sub-Zero personalities

### 🌐 **Integration Options**
1. **Iframe Embedding** - Easy web integration
2. **REST API** - Full programmatic access
3. **Streamlit App** - Ready-to-use web interface
4. **Mobile-Friendly** - Responsive design for all devices

## 🔧 Setup Instructions

### 1. Install Dependencies
```bash
cd "c:\Users\Dell\Desktop\Krypt"
pip install -r requirements.txt
```

### 2. Start the Services

#### Option A: Iframe-Ready Streamlit App
```bash
python -m streamlit run iframe_app.py --server.port 8501
```

#### Option B: REST API Server
```bash
python api_server.py
```

#### Option C: Full Streamlit App
```bash
python -m streamlit run streamlit_app.py --server.port 8501
```

## 📱 Iframe Integration

### Basic Iframe Embed
```html
<!-- Simple iframe embedding -->
<iframe 
    src="http://your-domain.com:8501" 
    width="100%" 
    height="600" 
    frameborder="0"
    style="border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
</iframe>
```

### Mobile App Integration
```html
<!-- For mobile apps with full-height container -->
<div style="width: 100%; height: 80vh;">
    <iframe 
        src="http://your-domain.com:8501" 
        width="100%" 
        height="100%" 
        frameborder="0"
        style="border-radius: 10px;">
    </iframe>
</div>
```

### Responsive Design
```html
<!-- Responsive iframe that adapts to screen size -->
<div class="krypt-container">
    <iframe 
        src="http://your-domain.com:8501" 
        width="100%" 
        height="100%" 
        frameborder="0">
    </iframe>
</div>

<style>
.krypt-container {
    width: 100%;
    height: 600px;
    max-width: 500px;
    margin: 0 auto;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
    .krypt-container {
        height: 80vh;
        max-width: 100%;
        margin: 10px;
        border-radius: 10px;
    }
}
</style>
```

## 🔌 REST API Integration

### Base URL
```
http://localhost:5000/api
```

### Key Endpoints

#### 1. Chat with AI
```javascript
// Send message to chatbot
const response = await fetch('http://localhost:5000/api/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: "What's the price of Bitcoin?",
        personality: "normal" // or "subzero"
    })
});

const data = await response.json();
console.log(data.message); // AI response
```

#### 2. Get Article Insights
```javascript
// Search your custom articles
const insights = await fetch('http://localhost:5000/api/insights?q=bitcoin')
    .then(response => response.json());

console.log(insights.insights); // Article analysis
```

#### 3. Manage Personality
```javascript
// Switch to Sub-Zero mode
const personality = await fetch('http://localhost:5000/api/personality', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mode: 'subzero' })
}).then(response => response.json());

console.log(personality.message); // "🧊 Sub-Zero mode activated!"
```

#### 4. Add Custom Articles
```javascript
// Add your own articles for AI insights
const article = await fetch('http://localhost:5000/api/articles', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        title: "My Crypto Analysis",
        content: "Detailed analysis content...",
        category: "analysis",
        tags: ["bitcoin", "technical-analysis"]
    })
}).then(response => response.json());

console.log(article.article_id); // New article ID
```

## 📚 Custom Article Management

### Adding Your Articles

The AI can provide insights based on your own articles. Add them programmatically:

```python
from article_manager import ArticleManager

manager = ArticleManager()

# Add your article
article_id = manager.add_article(
    title="Bitcoin Analysis 2025",
    content="Your detailed analysis content...",
    category="market-analysis",
    tags=["bitcoin", "2025", "prediction"]
)
```

### Article Categories
- `analysis` - Market analysis and insights
- `education` - Educational content
- `news` - News and updates
- `defi` - DeFi-related content
- `nft` - NFT market content
- `regulation` - Regulatory updates
- `technical` - Technical analysis

### Querying Article Insights

Users can ask questions like:
- "What do your articles say about Bitcoin?"
- "Tell me about DeFi from your analysis"
- "What insights do you have on NFTs?"
- "Explain Ethereum staking from your content"

## 📱 Mobile App Integration Examples

### React Native
```javascript
import { WebView } from 'react-native-webview';

export default function CryptoAssistant() {
    return (
        <WebView
            source={{ uri: 'http://your-domain.com:8501' }}
            style={{ flex: 1 }}
            javaScriptEnabled={true}
            domStorageEnabled={true}
        />
    );
}
```

### Flutter
```dart
import 'package:webview_flutter/webview_flutter.dart';

class CryptoAssistant extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(title: Text('Krypt AI Assistant')),
            body: WebView(
                initialUrl: 'http://your-domain.com:8501',
                javascriptMode: JavascriptMode.unrestricted,
            ),
        );
    }
}
```

### JavaScript/Web
```javascript
// Dynamic iframe injection
function embedKryptAI(containerId) {
    const container = document.getElementById(containerId);
    const iframe = document.createElement('iframe');
    
    iframe.src = 'http://your-domain.com:8501';
    iframe.width = '100%';
    iframe.height = '600px';
    iframe.frameBorder = '0';
    iframe.style.borderRadius = '15px';
    
    container.appendChild(iframe);
}

// Call function to embed
embedKryptAI('ai-assistant-container');
```

## 🎨 Customization Options

### Theme Integration
```css
/* Match your app's theme */
.krypt-iframe {
    border: 2px solid var(--your-brand-color);
    border-radius: var(--your-border-radius);
    box-shadow: var(--your-shadow);
}
```

### Brand Colors
Modify the iframe app to match your brand:
- Edit `iframe_app.py`
- Update CSS variables
- Customize colors and styling

## 🚀 Production Deployment

### Using Vercel
1. Deploy the Streamlit app to Vercel
2. Update iframe URLs to your domain
3. Configure environment variables

### Using Heroku
1. Create `Procfile`:
```
web: streamlit run iframe_app.py --server.port=$PORT --server.address=0.0.0.0
```
2. Deploy to Heroku
3. Update iframe sources

### Using AWS/Azure
1. Deploy using your preferred cloud service
2. Configure load balancing for scalability
3. Set up SSL certificates for HTTPS

## 📊 Usage Examples

### Query Types Supported

#### Price Queries
- "What's the price of Bitcoin?"
- "Current Ethereum value"
- "How much is Dogecoin worth?"

#### News Queries
- "Latest crypto news"
- "What's happening with Bitcoin?"
- "Recent market updates"

#### Article Insights
- "Tell me about DeFi from your articles"
- "What do you know about NFTs?"
- "Explain staking from your content"

#### Personality Switch
- "Switch to Sub-Zero mode"
- "Change to normal mode"
- "Toggle personality"

## 🔒 Security Considerations

### API Security
- Use API keys for production
- Implement rate limiting
- Add CORS configuration
- Use HTTPS in production

### Iframe Security
- Set appropriate CSP headers
- Use sandbox attributes if needed
- Validate origins for postMessage

## 📈 Performance Optimization

### Caching
- Cache API responses
- Use Redis for session storage
- Implement response compression

### Scaling
- Use load balancers
- Implement database caching
- Optimize API response times

## 🐛 Troubleshooting

### Common Issues

#### API Not Responding
```bash
# Check if API is running
curl http://localhost:5000/api/status
```

#### Iframe Not Loading
- Check CORS settings
- Verify URL accessibility
- Check browser console for errors

#### Chat Not Working
- Verify API connection
- Check network requests
- Validate JSON payloads

## 📞 Support

For integration support or questions:
- Check the API documentation at `http://localhost:5000`
- Review the example files in the repository
- Test using the `mobile_web_demo.html` file

## 🎯 Next Steps

1. **Deploy to Production**: Host on your preferred platform
2. **Custom Branding**: Modify colors and styling to match your app
3. **Add Articles**: Populate with your own content for better insights
4. **Monitor Usage**: Track API calls and user interactions
5. **Scale**: Implement caching and load balancing as needed

---

🚀 **Your Krypt AI Assistant is now ready for embedding into any platform!** 

The combination of real-time crypto data, custom article insights, and dual personality modes makes it a powerful addition to any crypto-related application.
