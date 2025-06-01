# Krypt - Crypto Sentiment Analysis for Vercel

This is a modified version of your Krypt app that's compatible with Vercel deployment.

## What I Changed

1. **Converted from Streamlit to Web App**: Since Vercel doesn't support Streamlit, I created a full-featured web application with HTML/CSS/JavaScript that replicates all your Streamlit app's functionality.

2. **API Structure**: Created serverless API endpoints in the `/api` folder that Vercel can deploy:
   - `/api/markets` - Returns market data for all cryptocurrencies
   - `/api/analyze` - Analyzes a specific cryptocurrency with sentiment analysis

3. **Frontend**: Created a responsive web interface (`index.html`) that includes:
   - All the features from your Streamlit app
   - Sidebar with coin navigation (Main, Top Coins, All Coins tabs)
   - Real-time search functionality
   - Market data display
   - Sentiment analysis
   - News feed with sentiment scores
   - Similar coins suggestions

## Deployment Instructions

### Option 1: Deploy with Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Navigate to your project folder:
   ```bash
   cd C:\Users\Dell\Desktop\Krypt
   ```

3. Deploy to Vercel:
   ```bash
   vercel
   ```

4. Follow the prompts:
   - Login/create Vercel account
   - Choose project name
   - Select default settings

5. Your app will be deployed to a URL like: `https://your-project-name.vercel.app`

### Option 2: Deploy via GitHub

1. Push your code to a GitHub repository

2. Go to [vercel.com](https://vercel.com) and sign in

3. Click "Import Project"

4. Import your GitHub repository

5. Vercel will automatically detect the configuration and deploy

## Features Preserved

✅ Real-time cryptocurrency data
✅ Sentiment analysis based on news
✅ Market metrics (price, volume, market cap)
✅ News aggregation from multiple sources
✅ Investment sentiment indicators
✅ Similar coins suggestions
✅ Responsive design
✅ All coins alphabetical navigation

## API Limitations

- The free CoinGecko API has rate limits
- CryptoCompare news API is used for sentiment analysis
- Consider adding your own API keys for better performance

## Local Testing

To test locally before deploying:

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Run development server:
   ```bash
   vercel dev
   ```

3. Open http://localhost:3000 in your browser

## Troubleshooting

If you encounter issues:

1. **API Errors**: The app includes fallback to client-side API calls if the serverless functions fail
2. **CORS Issues**: Already configured to allow all origins
3. **Missing Dependencies**: Make sure all packages in requirements.txt are compatible with Vercel's Python runtime

## Next Steps

After deployment, you can:
- Add custom domain in Vercel dashboard
- Monitor usage and logs in Vercel dashboard
- Add environment variables for API keys (optional)
- Customize the design further

The app is now fully compatible with Vercel's serverless architecture!