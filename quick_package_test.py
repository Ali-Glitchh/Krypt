#!/usr/bin/env python3
"""
Quick package test
"""

packages = ['streamlit', 'requests', 'pandas', 'plotly', 'vaderSentiment', 'numpy']

for pkg in packages:
    try:
        __import__(pkg)
        print(f"✅ {pkg}")
    except ImportError as e:
        print(f"❌ {pkg}: {e}")
    except Exception as e:
        print(f"⚠️ {pkg}: {e}")

print("Package test complete")
