else:  # Q&A Mode
    st.markdown("### 💬 Crypto Q&A")
    st.markdown("""
    Ask questions about:
    - Specific cryptocurrencies (e.g., "What do you think about Bitcoin?")
    - Market analysis (e.g., "How is the crypto market performing?")
    - Trading terms and concepts (e.g., "What is HODL?")
    - Technical concepts (e.g., "Explain blockchain")
    - Trading strategies (e.g., "What is DCA?")
    """)

    # Knowledge Base Expander
    with st.expander("📚 Crypto Knowledge Base", expanded=False):
        kb_type = st.selectbox(
            "Select Category",
            ["Trading Terms", "Technical Concepts", "Market Analysis", "Trading Strategies"]
        )
        
        kb_mapping = {
            "Trading Terms": "trading",
            "Technical Concepts": "technical",
            "Market Analysis": "market_analysis",
            "Trading Strategies": "trading_strategies"
        }
        
        selected_category = kb_mapping[kb_type]
        for term, explanation in CRYPTO_KNOWLEDGE[selected_category].items():
            st.markdown(f"""
            <div style='background-color: #1e1e1e; padding: 15px; border-radius: 5px; margin-bottom: 10px;'>
                <strong>{term}</strong>: {explanation}
            </div>
            """, unsafe_allow_html=True)

    question = st.text_input("Ask your question:")
    if question:
        question_lower = question.lower()
        
        # Check for terminology questions first
        term_found = False
        for category in CRYPTO_KNOWLEDGE.values():
            for term, explanation in category.items():
                if term.lower() in question_lower:
                    st.markdown(f"""
                    <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                        <h3>{term}</h3>
                        <p>{explanation}</p>
                        <div class='disclaimer'>{DISCLAIMER}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    term_found = True
                    break
            if term_found:
                break
        
        # If no term is found, look for cryptocurrency analysis
        if not term_found:
            crypto_mentioned = None
            for coin in market_data:
                if coin['symbol'].lower() in question_lower or coin['name'].lower() in question_lower:
                    crypto_mentioned = coin
                    break

            if crypto_mentioned:
                # Get news and sentiment for the mentioned crypto
                news_data = get_news_data(crypto_mentioned['symbol'])
                news_items = []
                for item in news_data.get('Data', []):
                    sentiment = analyze_sentiment(f"{item['title']} {item['body']}", crypto_mentioned['symbol'])
                    news_items.append({
                        'title': item['title'],
                        'sentiment': sentiment,
                        'time': datetime.fromtimestamp(item['published_on'])
                    })
                
                if news_items:
                    news_df = pd.DataFrame(news_items)
                    total_sentiment = news_df['sentiment'].mean()
                    price_change = crypto_mentioned.get('price_change_percentage_24h', 0) or 0
                    
                    # Get investment sentiment
                    sentiment_status, sentiment_message = get_investment_sentiment(
                        price_change,
                        total_sentiment
                    )
                    
                    # Generate analysis
                    analysis = f"Based on recent data for {crypto_mentioned['name']} ({crypto_mentioned['symbol'].upper()}):\n\n"
                    
                    # Market metrics
                    analysis += f"📊 Market Metrics:\n"
                    analysis += f"- Current price: ${format_number(crypto_mentioned.get('current_price'))}\n"
                    analysis += f"- 24h change: {price_change:+.2f}%\n"
                    analysis += f"- Market cap: ${format_number(crypto_mentioned.get('market_cap'))}\n\n"
                    
                    # Sentiment analysis
                    analysis += f"🔍 Market Analysis:\n"
                    analysis += f"- Overall sentiment: {sentiment_status}\n"
                    analysis += f"- Sentiment score: {total_sentiment:.2f}\n"
                    analysis += f"- {sentiment_message}\n\n"
                    
                    # Recent developments
                    analysis += "📰 Recent Developments:\n"
                    for _, news in news_df.head(3).iterrows():
                        analysis += f"- {news['title']}\n"
                    
                    st.markdown(f"""
                    <div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                        <pre style='white-space: pre-wrap; font-family: inherit;'>{analysis}</pre>
                        <div class='disclaimer'>{DISCLAIMER}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info(f"No recent news found for {crypto_mentioned['symbol'].upper()}")
            else:
                st.warning("Please mention a specific cryptocurrency or trading term in your question.")