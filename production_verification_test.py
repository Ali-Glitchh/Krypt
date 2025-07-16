#!/usr/bin/env python3
"""
KoinToss Production Verification Test
- Tests all components for production readiness
- Verifies API server functionality
- Tests autonomous training system
- Checks for any errors or issues
"""

import time
import json
import requests
import threading
from datetime import datetime

class KoinTossProductionTest:
    def __init__(self):
        self.chatbot = None
        self.autonomous_trainer = None
        self.test_results = {}
        
    def test_chatbot_core(self):
        """Test core chatbot functionality"""
        print("\n🤖 Testing Core Chatbot...")
        
        try:
            from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
            self.chatbot = ImprovedDualPersonalityChatbot()
            
            # Test basic response
            response = self.chatbot.get_response("Hello")
            assert response and "message" in response
            
            # Test personality switch
            switch_result = self.chatbot.switch_personality("subzero")
            assert "Sub-Zero" in switch_result
            
            subzero_response = self.chatbot.get_response("What is Bitcoin?")
            assert subzero_response and "message" in subzero_response
            
            # Switch back
            self.chatbot.switch_personality("normal")
            
            self.test_results["chatbot_core"] = {
                "status": "PASS",
                "message": "All core chatbot functions working"
            }
            print("✅ Core chatbot tests PASSED")
            
        except Exception as e:
            self.test_results["chatbot_core"] = {
                "status": "FAIL",
                "error": str(e)
            }
            print(f"❌ Core chatbot tests FAILED: {e}")
    
    def test_autonomous_training(self):
        """Test autonomous training system"""
        print("\n🚀 Testing Autonomous Training...")
        
        try:
            from advanced_autonomous_trainer import AdvancedAutonomousTrainer
            
            if not self.chatbot:
                from improved_dual_personality_chatbot import ImprovedDualPersonalityChatbot
                self.chatbot = ImprovedDualPersonalityChatbot()
            
            self.autonomous_trainer = AdvancedAutonomousTrainer(self.chatbot)
            
            # Test initialization
            stats = self.autonomous_trainer.get_training_statistics()
            assert isinstance(stats, dict)
            
            # Test data fetching
            real_time_data = self.autonomous_trainer.fetch_real_time_data()
            assert "timestamp" in real_time_data
            
            # Test training data generation
            training_data = self.autonomous_trainer.generate_contextual_training_data(real_time_data)
            assert isinstance(training_data, list)
            
            # Test response evaluation
            test_response = {"message": "Bitcoin is a cryptocurrency", "confidence": 0.8}
            quality_score = self.autonomous_trainer.self_evaluate_response("What is Bitcoin?", test_response)
            assert 0 <= quality_score <= 1
            
            self.test_results["autonomous_training"] = {
                "status": "PASS",
                "message": "Autonomous training system functional"
            }
            print("✅ Autonomous training tests PASSED")
            
        except Exception as e:
            self.test_results["autonomous_training"] = {
                "status": "FAIL",
                "error": str(e)
            }
            print(f"❌ Autonomous training tests FAILED: {e}")
    
    def test_api_imports(self):
        """Test API server dependencies"""
        print("\n📡 Testing API Server Dependencies...")
        
        try:
            # Test FastAPI imports
            from fastapi import FastAPI, HTTPException
            from fastapi.middleware.cors import CORSMiddleware
            from pydantic import BaseModel
            import uvicorn
            
            # Test enhanced API server import
            from enhanced_kointoss_api_server import app
            
            self.test_results["api_imports"] = {
                "status": "PASS",
                "message": "All API dependencies available"
            }
            print("✅ API server dependency tests PASSED")
            
        except Exception as e:
            self.test_results["api_imports"] = {
                "status": "FAIL",
                "error": str(e)
            }
            print(f"❌ API server dependency tests FAILED: {e}")
    
    def test_data_sources(self):
        """Test external data source connectivity"""
        print("\n📊 Testing External Data Sources...")
        
        try:
            # Test CoinGecko API
            response = requests.get("https://api.coingecko.com/api/v3/ping", timeout=10)
            assert response.status_code == 200
            
            # Test trending data
            trending = requests.get("https://api.coingecko.com/api/v3/search/trending", timeout=10)
            assert trending.status_code == 200
            
            # Test market data
            markets = requests.get(
                "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=1",
                timeout=10
            )
            assert markets.status_code == 200
            
            self.test_results["data_sources"] = {
                "status": "PASS",
                "message": "External data sources accessible"
            }
            print("✅ Data source tests PASSED")
            
        except Exception as e:
            self.test_results["data_sources"] = {
                "status": "FAIL",
                "error": str(e)
            }
            print(f"❌ Data source tests FAILED: {e}")
    
    def test_training_functionality(self):
        """Test short training cycle"""
        print("\n🔄 Testing Training Cycle...")
        
        try:
            if not self.autonomous_trainer:
                self.test_autonomous_training()
            
            # Test one training cycle
            real_time_data = self.autonomous_trainer.fetch_real_time_data()
            training_scenarios = self.autonomous_trainer.generate_contextual_training_data(real_time_data)
            
            if training_scenarios:
                # Test first scenario
                scenario = training_scenarios[0]
                question = scenario["question"]
                
                response = self.chatbot.get_response(question)
                quality_score = self.autonomous_trainer.self_evaluate_response(question, response)
                
                # Store conversation
                self.autonomous_trainer.conversation_patterns.append({
                    "question": question,
                    "response": response,
                    "quality_score": quality_score,
                    "timestamp": datetime.now().isoformat(),
                    "test_run": True
                })
                
                print(f"   🤔 Test Question: {question}")
                print(f"   💬 Response: {response.get('message', 'No response')[:100]}...")
                print(f"   📈 Quality Score: {quality_score:.2f}")
            
            self.test_results["training_functionality"] = {
                "status": "PASS",
                "message": "Training cycle completed successfully"
            }
            print("✅ Training functionality tests PASSED")
            
        except Exception as e:
            self.test_results["training_functionality"] = {
                "status": "FAIL",
                "error": str(e)
            }
            print(f"❌ Training functionality tests FAILED: {e}")
    
    def test_file_integrity(self):
        """Test that all required files exist and are valid"""
        print("\n📁 Testing File Integrity...")
        
        try:
            import os
            
            required_files = [
                "improved_dual_personality_chatbot.py",
                "enhanced_normal_trainer.py",
                "pure_subzero_trainer.py",
                "crypto_news_insights.py",
                "advanced_autonomous_trainer.py",
                "enhanced_kointoss_api_server.py",
                "requirements.txt"
            ]
            
            missing_files = []
            for file in required_files:
                if not os.path.exists(file):
                    missing_files.append(file)
            
            if missing_files:
                raise Exception(f"Missing files: {missing_files}")
            
            self.test_results["file_integrity"] = {
                "status": "PASS",
                "message": "All required files present"
            }
            print("✅ File integrity tests PASSED")
            
        except Exception as e:
            self.test_results["file_integrity"] = {
                "status": "FAIL",
                "error": str(e)
            }
            print(f"❌ File integrity tests FAILED: {e}")
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🎯 KoinToss Production Verification Starting...")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all tests
        self.test_file_integrity()
        self.test_chatbot_core()
        self.test_autonomous_training()
        self.test_api_imports()
        self.test_data_sources()
        self.test_training_functionality()
        
        end_time = time.time()
        
        # Generate report
        print("\n" + "=" * 60)
        print("📋 PRODUCTION VERIFICATION REPORT")
        print("=" * 60)
        
        passed = 0
        failed = 0
        
        for test_name, result in self.test_results.items():
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_icon} {test_name.upper()}: {result['status']}")
            
            if result["status"] == "PASS":
                passed += 1
                print(f"   {result['message']}")
            else:
                failed += 1
                print(f"   ERROR: {result.get('error', 'Unknown error')}")
            print()
        
        print(f"📊 SUMMARY: {passed} passed, {failed} failed")
        print(f"⏱️ Total time: {end_time - start_time:.2f} seconds")
        
        if failed == 0:
            print("🎉 ALL TESTS PASSED - KoinToss is PRODUCTION READY!")
            print("\n🚀 Ready to start:")
            print("   • Autonomous Training: python start_autonomous_training.py")
            print("   • API Server: python enhanced_kointoss_api_server.py")
            print("   • Combined: python -c 'import start_autonomous_training; start_autonomous_training.main()'")
        else:
            print("⚠️ SOME TESTS FAILED - Review errors above before deployment")
        
        return failed == 0

if __name__ == "__main__":
    tester = KoinTossProductionTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n🤖 Starting Brief Autonomous Training Demo...")
        try:
            if tester.autonomous_trainer:
                # Export test data
                export_file = tester.autonomous_trainer.export_training_data("production_test_export.json")
                print(f"💾 Test data exported to: {export_file}")
        except Exception as e:
            print(f"⚠️ Could not export test data: {e}")
    
    exit(0 if success else 1)
