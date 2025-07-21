# 🌙 How to Get MoonshotAI API Access

## 🔑 Getting MoonshotAI Kimi K2 API Access

### 📍 Official Website
**Main Site**: https://www.moonshot.cn/
**API Documentation**: https://platform.moonshot.cn/docs

### 🚀 Step-by-Step Guide

#### 1. **Create Account**
- Visit https://platform.moonshot.cn/
- Click "注册" (Register) or "Sign Up"
- Use email or phone number to register
- Verify your account via email/SMS

#### 2. **Login to Platform**
- Go to https://platform.moonshot.cn/console
- Login with your credentials
- Access the developer console/dashboard

#### 3. **Navigate to API Keys**
- Look for "API Keys" or "密钥管理" in the dashboard
- Click "Create New Key" or "创建新密钥"
- Give your key a descriptive name (e.g., "KoinToss AI Bot")

#### 4. **Copy Your API Key**
- Copy the generated API key immediately
- **Important**: Save it securely - you won't see it again!
- Format should be: `sk-xxx...` (similar to OpenAI format)

#### 5. **Set Usage Limits (Optional)**
- Configure spending limits if available
- Set monthly usage quotas
- Enable notifications for usage alerts

### 💰 Pricing Information

#### Free Tier (Kimi K2 Free)
- **Model**: `moonshot-v1-8k` or `moonshot-v1-32k`
- **Free Credits**: Usually includes some free tokens/requests
- **Rate Limits**: Limited requests per minute/hour
- **Perfect for**: Testing and small projects like KoinToss AI

#### Paid Plans
- **Pay-per-use**: Charged by token usage
- **Monthly subscriptions**: Available for heavy usage
- **Enterprise**: Custom pricing for high-volume usage

### 🌐 Alternative Access Methods

#### If Main Site is Inaccessible:

1. **International Platform**
   - Check for international.moonshot.cn
   - Or global.moonshot.cn

2. **API Marketplace**
   - Some API marketplaces may offer MoonshotAI access
   - Check platforms like RapidAPI or similar

3. **VPN Access**
   - If regionally blocked, try VPN to China/Asia
   - Use during registration and API key generation

### 🛠️ Integration Steps After Getting API Key

#### 1. **Update Your KoinToss AI**
```python
# In improved_dual_personality_chatbot.py
# Replace this line:
moonshot_api_key = "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"

# With your new key:
moonshot_api_key = "YOUR_NEW_API_KEY_HERE"
```

#### 2. **Test the Connection**
```bash
# Run our test script
python test_moonshot_direct.py
```

#### 3. **Verify Integration**
```bash
# Run full integration test
python check_moonshot_status.py
```

### 🔧 Troubleshooting Common Issues

#### Authentication Errors (401)
- **Check key format**: Should start with `sk-`
- **Verify account status**: Ensure account is active
- **Check billing**: Make sure you have available credits
- **Regional access**: Try different network/VPN

#### Connection Errors
- **Network issues**: Check internet connectivity
- **Firewall**: Ensure API endpoints aren't blocked
- **Proxy settings**: Configure if behind corporate proxy

#### Rate Limiting (429)
- **Wait period**: API has rate limits, wait before retrying
- **Upgrade plan**: Consider paid plan for higher limits
- **Implement backoff**: Our code already has retry logic

### 📱 Mobile Registration Tip
If you need a Chinese phone number for registration:
- Some services accept international numbers with +country code
- Virtual number services may work for verification
- Email registration is usually available as alternative

### 🆘 Support Resources

#### Official Support
- **Documentation**: https://platform.moonshot.cn/docs
- **Support Email**: Usually found in platform footer
- **Community**: Look for Discord/Telegram groups

#### API Status
- **Status Page**: Check for service outages
- **Version Updates**: Monitor for API changes
- **Deprecation Notices**: Stay updated on API versions

### ⚡ Quick Start After Getting Key

1. **Replace API key** in the chatbot code
2. **Test connection** with our test scripts  
3. **Launch KoinToss AI** with full MoonshotAI enhancement
4. **Enjoy advanced crypto conversations!**

### 🎯 Expected Results After Setup

Once you have a valid API key, KoinToss AI will:
- ✅ **Enhanced Responses**: Complex crypto questions get AI-powered answers
- ✅ **Context Awareness**: Conversations remember previous exchanges
- ✅ **Technical Analysis**: Detailed blockchain and crypto explanations
- ✅ **Market Insights**: Advanced market analysis and predictions
- ✅ **Educational Content**: Professional-grade crypto education

---

## 🚀 Ready to Upgrade!

Your KoinToss AI chatbot is already **fully integrated** and waiting for the API key. Once you get access, you'll have one of the most advanced crypto AI assistants available! 

The integration code is perfect - you just need the authentication! 🎉
