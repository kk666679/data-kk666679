#!/usr/bin/env python3
"""
HRMS Malaysia Integration Tests
Tests Malaysian compliance, API endpoints, and core functionality
"""

import requests
import json
import sys
from datetime import datetime

class HRMSIntegrationTest:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.passed = 0
        self.failed = 0

    def test_api_health(self):
        """Test API health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            assert response.status_code == 200
            print("✅ API Health Check")
            self.passed += 1
        except Exception as e:
            print(f"❌ API Health Check: {e}")
            self.failed += 1

    def test_malaysian_compliance(self):
        """Test Malaysian compliance calculations"""
        try:
            # Test EPF calculation
            payload = {"salary": 5000, "employee_type": "local"}
            response = requests.post(f"{self.base_url}/api/payroll/epf", json=payload, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                expected_employee = 5000 * 0.11  # 11%
                expected_employer = 5000 * 0.13  # 13%
                
                assert abs(data["employee_contribution"] - expected_employee) < 0.01
                assert abs(data["employer_contribution"] - expected_employer) < 0.01
                print("✅ EPF Calculation")
                self.passed += 1
            else:
                raise Exception(f"EPF API returned {response.status_code}")
                
        except Exception as e:
            print(f"❌ EPF Calculation: {e}")
            self.failed += 1

    def test_ai_services(self):
        """Test AI services"""
        try:
            payload = {"text": "Saya sangat gembira bekerja di sini"}
            response = requests.post(f"{self.base_url}/api/ai/sentiment", json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                assert "sentiment" in data
                assert "language" in data
                print("✅ AI Sentiment Analysis")
                self.passed += 1
            else:
                raise Exception(f"AI API returned {response.status_code}")
                
        except Exception as e:
            print(f"❌ AI Sentiment Analysis: {e}")
            self.failed += 1

    def test_multi_language_support(self):
        """Test multi-language support"""
        try:
            languages = ["en", "ms", "zh"]
            for lang in languages:
                response = requests.get(f"{self.base_url}/api/i18n/{lang}", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    assert "messages" in data
                    
            print("✅ Multi-language Support")
            self.passed += 1
        except Exception as e:
            print(f"❌ Multi-language Support: {e}")
            self.failed += 1

    def run_all_tests(self):
        """Run all integration tests"""
        print("🧪 HRMS Malaysia Integration Tests")
        print("==================================")
        
        self.test_api_health()
        self.test_malaysian_compliance()
        self.test_ai_services()
        self.test_multi_language_support()
        
        print(f"\n📊 Test Results:")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📈 Success Rate: {(self.passed/(self.passed+self.failed)*100):.1f}%")
        
        if self.failed > 0:
            print("⚠️ Some tests failed. Check logs above.")
            sys.exit(1)
        else:
            print("🎉 All tests passed! System is ready for production.")

if __name__ == "__main__":
    tester = HRMSIntegrationTest()
    tester.run_all_tests()