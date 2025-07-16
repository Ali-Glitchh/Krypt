"""
KoinToss - Enhanced Crypto Chatbot
===================================

A dual-personality cryptocurrency chatbot with real-time data integration,
autonomous learning capabilities, and beautiful KoinToss branding.

Features:
- Dual AI personalities (Krypt AI & Sub-Zero)
- Real-time cryptocurrency data
- Autonomous learning system
- Beautiful Streamlit interface
- Production-ready deployment
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="kointoss-crypto-chatbot",
    version="1.5.0",
    author="KoinToss Team",
    author_email="team@kointoss.ai",
    description="Enhanced dual-personality cryptocurrency chatbot with real-time data integration",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kointoss-crypto-chatbot",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/kointoss-crypto-chatbot/issues",
        "Documentation": "https://github.com/yourusername/kointoss-crypto-chatbot/wiki",
        "Source Code": "https://github.com/yourusername/kointoss-crypto-chatbot",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Framework :: Streamlit",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=6.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "safety>=2.3.0",
            "bandit>=1.7.5",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "kointoss=kointoss_streamlit_app:main",
            "kointoss-train=autonomous_training_system:main",
            "kointoss-test=final_verification_complete:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "*.json",
            "*.md",
            "*.txt",
            "*.yml",
            "*.yaml",
        ],
    },
    keywords=[
        "cryptocurrency",
        "chatbot",
        "ai",
        "bitcoin",
        "ethereum",
        "trading",
        "fintech",
        "streamlit",
        "real-time",
        "machine-learning",
    ],
    zip_safe=False,
)
