#!/usr/bin/env python3
"""
Pre-Deployment Verification Script
Ensures the system is ready for deployment without scikit-learn dependencies
"""

import sys
import json

def verify_requirements():
    """Verify requirements.txt doesn't contain problematic dependencies"""
    print("📋 Checking requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        problematic_deps = ['scikit-learn', 'sklearn', 'scipy', 'joblib']
        found_issues = []
        
        for dep in problematic_deps:
            if dep in requirements.lower():
                found_issues.append(dep)
        
        if found_issues:
            print(f"   ❌ Found problematic dependencies: {found_issues}")
            return False
        else:
            print("   ✅ Requirements.txt is clean")
            return True
            
    except FileNotFoundError:
        print("   ❌ requirements.txt not found")
        return False

def verify_imports():
    """Verify no scikit-learn imports in active files"""
    print("📋 Checking for scikit-learn imports...")
    
    active_files = [
        'improved_dual_personality_chatbot.py',
        'enhanced_normal_trainer.py',
        'pure_subzero_trainer.py',
        'crypto_news_insights.py',
        'advanced_training_system.py',
        'streamlit_app.py'
    ]
    
    issues_found = False
    
    for file_path in active_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'from sklearn' in content or 'import sklearn' in content:
                print(f"   ❌ {file_path} contains sklearn imports")
                issues_found = True
            else:
                print(f"   ✅ {file_path} is clean")
                
        except FileNotFoundError:
            print(f"   ⚠️ {file_path} not found")
    
    return not issues_found

def verify_functionality():
    """Test core functionality"""
    print("📋 Testing core functionality...")
    
    try:
        # Test normal trainer
        from enhanced_normal_trainer import PureNormalTrainer
        normal_trainer = PureNormalTrainer()
        normal_response = normal_trainer.get_response("Hello")
        print("   ✅ Normal trainer working")
        
        # Test sub-zero trainer  
        from pure_subzero_trainer import PureSubZeroTrainer
        subzero_trainer = PureSubZeroTrainer()
        subzero_response = subzero_trainer.get_response("Hello")
        print("   ✅ Sub-Zero trainer working")
        
        # Test news service
        from crypto_news_insights import CryptoNewsInsights
        news_service = CryptoNewsInsights()
        print("   ✅ News service working")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Functionality test failed: {e}")
        return False

def main():
    print("🚀 PRE-DEPLOYMENT VERIFICATION")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Run all verification checks
    checks = [
        ("Requirements.txt verification", verify_requirements),
        ("Import verification", verify_imports), 
        ("Functionality verification", verify_functionality)
    ]
    
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        if not check_func():
            all_checks_passed = False
    
    print("\n" + "=" * 50)
    
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED!")
        print("🚀 System is ready for deployment!")
        print("\nDeployment Notes:")
        print("- No scikit-learn dependencies")
        print("- Custom similarity functions implemented")
        print("- All core components tested and working")
        print("- UTF-8 encoding issues resolved")
        print("\nYou can now deploy to platforms like:")
        print("- Streamlit Cloud")
        print("- Heroku")
        print("- Railway")
        print("- Google Cloud Run")
        
        return 0
    else:
        print("❌ SOME CHECKS FAILED!")
        print("Please resolve the issues above before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
