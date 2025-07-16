# Contributing to KoinToss

⚔️ **Thank you for your interest in contributing to KoinToss!** We welcome contributions from the community to help make this crypto chatbot even better.

## 🎯 Ways to Contribute

### 🐛 Bug Reports
Found a bug? Please help us fix it:
1. Check if the issue already exists in [GitHub Issues](https://github.com/yourusername/kointoss-crypto-chatbot/issues)
2. If not, create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - System information (OS, Python version, etc.)

### ✨ Feature Requests
Have an idea for a new feature?
1. Check our [roadmap](README.md#-roadmap) to see if it's already planned
2. Open a new issue with the `enhancement` label
3. Describe the feature and its benefits
4. Include mockups or examples if helpful

### 🔧 Code Contributions
Ready to write some code? Follow these steps:

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of FastAPI, REST APIs, and Python
- Understanding of embeddable widgets and JavaScript (for frontend integration)

### Development Setup
```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork locally
git clone https://github.com/YOUR_USERNAME/kointoss-crypto-chatbot.git
cd kointoss-crypto-chatbot

# 3. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install development dependencies (if available)
pip install -r requirements-dev.txt

# 6. Run the production verification test
python production_verification_test.py

# 7. Start the autonomous training system
python start_autonomous_training.py

# 8. In another terminal, start the API server
python enhanced_kointoss_api_server.py

# 9. Test the embeddable widget at http://localhost:8000/widget
```

## 📋 Development Workflow

### 1. Create a Branch
```bash
# Create a new branch for your feature/fix
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/your-bugfix-name
```

### 2. Make Your Changes
- Write clean, readable code
- Follow Python PEP 8 style guidelines
- Add comments for complex logic
- Update docstrings for new functions

### 3. Test Your Changes
```bash
# Run production verification test
python production_verification_test.py

# Run core tests
python test_core_components.py

# Test enhanced features
python test_enhanced_features.py

# Run complete verification
python final_verification_complete.py

# Test the API server
python enhanced_kointoss_api_server.py --reload

# Test autonomous training
python start_autonomous_training.py
```

### 4. Commit Your Changes
```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add real-time price alerts for portfolio tracking"

# Use conventional commit format:
# feat: new feature
# fix: bug fix
# docs: documentation
# style: formatting
# refactor: code restructuring
# test: adding tests
# chore: maintenance
```

### 5. Push and Create PR
```bash
# Push to your fork
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
# Include a clear description of your changes
```

## 🎨 Code Style Guidelines

### Python Code Style
- Follow PEP 8
- Use type hints where possible
- Maximum line length: 88 characters (Black formatter standard)
- Use meaningful variable and function names

### Example Code Structure
```python
from typing import Dict, List, Optional

def process_crypto_data(
    coin_id: str, 
    include_market_data: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Process cryptocurrency data for the chatbot.
    
    Args:
        coin_id: The cryptocurrency identifier
        include_market_data: Whether to include market statistics
        
    Returns:
        Processed crypto data or None if error
    """
    try:
        # Implementation here
        return processed_data
    except Exception as e:
        logger.error(f"Error processing {coin_id}: {e}")
        return None
```

### FastAPI Components
- Use consistent naming for API endpoints
- Add comprehensive error handling for all routes
- Implement proper request/response validation with Pydantic
- Include rate limiting and security considerations
- Add comprehensive documentation with examples

### Embeddable Widget Guidelines
- Ensure cross-browser compatibility
- Use vanilla JavaScript (no external dependencies)
- Implement responsive design for mobile devices
- Follow accessibility guidelines (ARIA labels, keyboard navigation)
- Use consistent CSS naming conventions with kointoss- prefix

## 🧪 Testing Guidelines

### Adding Tests
When adding new features, please include tests:

```python
def test_new_feature():
    """Test description"""
    # Arrange
    input_data = "test input"
    
    # Act
    result = your_function(input_data)
    
    # Assert
    assert result is not None
    assert "expected" in result
```

### Test Categories
- **Unit Tests**: Test individual functions
- **Integration Tests**: Test component interactions
- **API Tests**: Test REST API endpoints and WebSocket connections
- **Widget Tests**: Test embeddable widget functionality
- **Training Tests**: Test autonomous learning system
- **Production Tests**: Comprehensive production readiness verification

## 📝 Documentation

### Code Documentation
- Add docstrings to all public functions
- Use Google-style docstrings
- Include examples in docstrings when helpful

### README Updates
If your changes affect usage:
- Update the README.md
- Add new features to the feature list
- Update installation instructions if needed
- Add new dependencies to requirements

## 🔍 Code Review Process

### What We Look For
- **Functionality**: Does the code work as expected?
- **Testing**: Are there adequate tests?
- **Documentation**: Is the code well-documented?
- **Style**: Does it follow our coding standards?
- **Performance**: Is the code efficient?
- **Security**: Are there any security concerns?

### Review Timeline
- We aim to review PRs within 3-5 business days
- Larger PRs may take longer
- Feel free to ping maintainers if no response after a week

## 🏷️ Issue Labels

We use these labels to categorize issues:
- `bug`: Something isn't working
- `enhancement`: New feature or improvement
- `documentation`: Documentation updates
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `priority-high`: Critical issues
- `priority-medium`: Important issues
- `priority-low`: Nice to have

## 🤝 Community Guidelines

### Be Respectful
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Be Collaborative
- Help others learn and grow
- Share knowledge and best practices
- Provide constructive feedback
- Celebrate others' contributions

## 💡 Tips for Success

### First-Time Contributors
- Start with issues labeled `good first issue`
- Don't hesitate to ask questions
- Read through existing code to understand patterns
- Test your changes thoroughly

### Experienced Contributors
- Consider mentoring newcomers
- Help with code reviews
- Suggest architectural improvements
- Share knowledge through documentation

## 📞 Getting Help

Need help with your contribution?
- **Discord**: Join our community chat (coming soon)
- **GitHub Discussions**: Ask questions and share ideas
- **Issues**: Tag maintainers for technical help
- **Email**: Contact maintainers directly for sensitive issues

## 🎉 Recognition

We appreciate all contributions! Contributors will be:
- Added to our [Contributors](README.md#contributors) section
- Mentioned in release notes for significant contributions
- Invited to join our core team for outstanding contributions

---

**Thank you for contributing to KoinToss! Together, we're making cryptocurrency more accessible to everyone.** ⚔️

---

*This document is adapted from the [Contributor Covenant](https://www.contributor-covenant.org/) and follows open source best practices.*
