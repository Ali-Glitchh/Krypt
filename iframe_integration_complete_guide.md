# 📱 KoinToss iframe Integration Guide
## Embed Your AI Assistant Anywhere for FREE

## 🎯 Quick Start (3 Steps)

### Step 1: Deploy to Streamlit Cloud (FREE)
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Connect GitHub and upload the `kointoss-iframe-deploy` folder
3. Set main file: `app.py`
4. Click "Deploy" ✅

### Step 2: Get Your iframe URL
After deployment: `https://your-username-kointoss-iframe-app-xyz.streamlit.app`

### Step 3: Embed Anywhere
```html
<iframe src="YOUR_URL" width="100%" height="600px" frameborder="0"></iframe>
```

## 🌐 Platform-Specific Integration

### HTML/CSS Websites
```html
<!DOCTYPE html>
<html>
<head>
    <title>My App with KoinToss</title>
    <style>
        .kointoss-container {
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .kointoss-iframe {
            width: 100%;
            height: 600px;
            border: none;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .kointoss-iframe {
                height: 500px;
            }
        }
    </style>
</head>
<body>
    <div class="kointoss-container">
        <h1>My Crypto App</h1>
        <iframe 
            class="kointoss-iframe"
            src="YOUR_STREAMLIT_URL"
            title="KoinToss AI Assistant">
        </iframe>
    </div>
</body>
</html>
```

### React Applications
```jsx
// KoinTossWidget.jsx
import React, { useState } from 'react';

const KoinTossWidget = ({ 
  width = "100%", 
  height = "600px",
  streamlitUrl = "YOUR_STREAMLIT_URL" 
}) => {
  const [isLoading, setIsLoading] = useState(true);

  return (
    <div style={{ width, height, position: 'relative' }}>
      {isLoading && (
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          color: '#667eea'
        }}>
          🪙 Loading KoinToss AI...
        </div>
      )}
      
      <iframe
        src={streamlitUrl}
        style={{
          width: '100%',
          height: '100%',
          border: 'none',
          borderRadius: '10px',
          opacity: isLoading ? 0 : 1,
          transition: 'opacity 0.3s ease'
        }}
        title="KoinToss AI Assistant"
        onLoad={() => setIsLoading(false)}
      />
    </div>
  );
};

// Usage in your app
const App = () => {
  return (
    <div>
      <h1>My Crypto Dashboard</h1>
      <KoinTossWidget 
        streamlitUrl="YOUR_STREAMLIT_URL"
        height="700px"
      />
    </div>
  );
};

export default App;
```

### Vue.js Applications
```vue
<!-- KoinTossWidget.vue -->
<template>
  <div class="kointoss-container">
    <div v-if="isLoading" class="loading">
      🪙 Loading KoinToss AI...
    </div>
    
    <iframe
      :src="streamlitUrl"
      class="kointoss-iframe"
      :class="{ hidden: isLoading }"
      title="KoinToss AI Assistant"
      @load="onLoad"
    />
  </div>
</template>

<script>
export default {
  name: 'KoinTossWidget',
  props: {
    streamlitUrl: {
      type: String,
      default: 'YOUR_STREAMLIT_URL'
    },
    height: {
      type: String,
      default: '600px'
    }
  },
  data() {
    return {
      isLoading: true
    };
  },
  methods: {
    onLoad() {
      this.isLoading = false;
    }
  }
};
</script>

<style scoped>
.kointoss-container {
  position: relative;
  width: 100%;
  height: v-bind(height);
}

.kointoss-iframe {
  width: 100%;
  height: 100%;
  border: none;
  border-radius: 10px;
  transition: opacity 0.3s ease;
}

.kointoss-iframe.hidden {
  opacity: 0;
}

.loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #667eea;
  font-weight: bold;
}
</style>
```

### React Native (Mobile Apps)
```javascript
// KoinTossScreen.js
import React from 'react';
import { View, StyleSheet, Text } from 'react-native';
import { WebView } from 'react-native-webview';

const KoinTossScreen = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.header}>🪙 KoinToss AI Assistant</Text>
      
      <WebView 
        source={{ uri: 'YOUR_STREAMLIT_URL' }}
        style={styles.webview}
        javaScriptEnabled={true}
        domStorageEnabled={true}
        startInLoadingState={true}
        renderLoading={() => (
          <View style={styles.loading}>
            <Text>Loading KoinToss AI...</Text>
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    padding: 15,
    backgroundColor: '#667eea',
    color: 'white',
  },
  webview: {
    flex: 1,
  },
  loading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default KoinTossScreen;
```

### Flutter (Mobile Apps)
```dart
// kointoss_widget.dart
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class KoinTossWidget extends StatefulWidget {
  final String streamlitUrl;
  
  const KoinTossWidget({
    Key? key, 
    this.streamlitUrl = 'YOUR_STREAMLIT_URL'
  }) : super(key: key);

  @override
  _KoinTossWidgetState createState() => _KoinTossWidgetState();
}

class _KoinTossWidgetState extends State<KoinTossWidget> {
  late final WebViewController controller;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageFinished: (String url) {
            setState(() {
              isLoading = false;
            });
          },
        ),
      )
      ..loadRequest(Uri.parse(widget.streamlitUrl));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('🪙 KoinToss AI Assistant'),
        backgroundColor: Color(0xFF667eea),
      ),
      body: Stack(
        children: [
          WebViewWidget(controller: controller),
          if (isLoading)
            Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(
                    color: Color(0xFF667eea),
                  ),
                  SizedBox(height: 16),
                  Text('Loading KoinToss AI...'),
                ],
              ),
            ),
        ],
      ),
    );
  }
}
```

### WordPress Integration
```html
<!-- Add to WordPress post/page or widget -->
<div style="width: 100%; max-width: 800px; margin: 0 auto;">
    <h3>🪙 Chat with KoinToss AI</h3>
    <iframe 
        src="YOUR_STREAMLIT_URL"
        style="width: 100%; height: 600px; border: none; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);"
        title="KoinToss AI Assistant">
    </iframe>
</div>

<!-- Or use WordPress shortcode -->
[iframe src="YOUR_STREAMLIT_URL" width="100%" height="600"]
```

## 🎨 Styling & Customization

### Custom CSS for iframe
```css
.kointoss-widget {
    width: 100%;
    max-width: 800px;
    height: 600px;
    border: none;
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3px;
}

.kointoss-widget iframe {
    width: 100%;
    height: 100%;
    border: none;
    border-radius: 12px;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .kointoss-widget {
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
    }
}

/* Mobile responsive */
@media (max-width: 768px) {
    .kointoss-widget {
        height: 500px;
        margin: 10px;
        max-width: calc(100% - 20px);
    }
}
```

### Full-screen Modal Integration
```html
<!-- Trigger button -->
<button onclick="openKoinToss()" class="kointoss-trigger">
    🪙 Open KoinToss AI
</button>

<!-- Modal -->
<div id="kointoss-modal" class="modal">
    <div class="modal-content">
        <span class="close" onclick="closeKoinToss()">&times;</span>
        <iframe 
            src="YOUR_STREAMLIT_URL"
            style="width: 100%; height: 80vh; border: none;">
        </iframe>
    </div>
</div>

<style>
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
}

.modal-content {
    background-color: #fefefe;
    margin: 5% auto;
    padding: 20px;
    border-radius: 10px;
    width: 90%;
    max-width: 1000px;
    position: relative;
}

.close {
    position: absolute;
    right: 20px;
    top: 10px;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}
</style>

<script>
function openKoinToss() {
    document.getElementById('kointoss-modal').style.display = 'block';
}

function closeKoinToss() {
    document.getElementById('kointoss-modal').style.display = 'none';
}
</script>
```

## 🚀 Deployment Platforms (All FREE)

### 1. Streamlit Cloud ⭐ (Recommended)
- **Cost:** 100% FREE
- **Setup:** 1-click deployment
- **URL:** `https://username-repo-app.streamlit.app`
- **Perfect for:** iframe embedding

### 2. Railway.app
- **Cost:** FREE tier (500 hours/month)
- **Custom Domain:** ✅ Yes
- **Setup:** Connect GitHub repo

### 3. Render.com
- **Cost:** FREE tier
- **Limitation:** Sleeps after 15min
- **Good for:** Testing

### 4. Vercel (with modifications)
- **Cost:** FREE
- **Requirement:** Convert to Next.js
- **Advanced option**

## 📊 Performance Tips

### Optimize Loading Speed
```html
<!-- Preload the iframe -->
<link rel="preload" as="document" href="YOUR_STREAMLIT_URL">

<!-- Progressive loading -->
<iframe 
    src="YOUR_STREAMLIT_URL"
    loading="lazy"
    style="width: 100%; height: 600px; border: none;">
</iframe>
```

### Mobile Optimization
```css
/* Responsive iframe */
.responsive-iframe {
    position: relative;
    overflow: hidden;
    width: 100%;
    padding-top: 75%; /* 4:3 aspect ratio */
}

.responsive-iframe iframe {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    width: 100%;
    height: 100%;
}
```

## 🎯 Use Cases

### E-commerce Integration
Add crypto price checking to your online store

### Educational Platforms
Embed crypto learning assistant in courses

### Portfolio Websites
Show off your AI project interactively

### Mobile Apps
Native crypto chat experience

### Client Demos
Quick deployment for presentations

## 🔧 Troubleshooting

### Common Issues & Solutions

1. **iframe not loading**
   - Check URL is correct
   - Ensure HTTPS is used
   - Verify Streamlit app is running

2. **Mobile display issues**
   - Add viewport meta tag
   - Use responsive CSS
   - Test on actual devices

3. **Performance slow**
   - Use Streamlit Cloud (fastest)
   - Implement loading states
   - Optimize iframe size

## 🎉 You're Ready!

Your KoinToss AI Assistant can now be embedded anywhere:
- ✅ **Free hosting** via Streamlit Cloud
- ✅ **Mobile responsive** design
- ✅ **Easy integration** in any platform
- ✅ **Professional appearance**

Deploy once, embed everywhere! 🚀📱💻
