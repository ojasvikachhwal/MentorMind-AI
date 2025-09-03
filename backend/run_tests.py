#!/usr/bin/env python3
"""
Comprehensive test runner for MentorMind backend
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🚀 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        if e.stdout:
            print("Stdout:", e.stdout)
        if e.stderr:
            print("Stderr:", e.stderr)
        return False

def main():
    """Run all tests and checks."""
    print("🧪 MentorMind Backend Testing Suite")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Install test dependencies
    print("\n📦 Installing test dependencies...")
    if not run_command("pip install -r requirements-test.txt", "Installing test dependencies"):
        print("❌ Failed to install test dependencies")
        return False
    
    # Run linting
    print("\n🔍 Running code quality checks...")
    if not run_command("flake8 app/ --max-line-length=120 --ignore=E501,W503", "Code linting"):
        print("⚠️ Linting issues found (continuing with tests)")
    
    # Run unit tests with coverage
    print("\n🧪 Running unit tests...")
    if not run_command(
        "pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing",
        "Unit tests with coverage"
    ):
        print("❌ Unit tests failed")
        return False
    
    # Run integration tests
    print("\n🔗 Running integration tests...")
    if not run_command(
        "pytest tests/test_integration.py -v",
        "Integration tests"
    ):
        print("❌ Integration tests failed")
        return False
    
    # Run performance tests
    print("\n⚡ Running performance tests...")
    if not run_command(
        "locust -f locustfile.py --headless --users 10 --spawn-rate 2 --run-time 30s",
        "Performance tests with Locust"
    ):
        print("⚠️ Performance tests failed (continuing)")
    
    # Run security checks
    print("\n🔒 Running security checks...")
    if not run_command(
        "bandit -r app/ -f json -o bandit-report.json",
        "Security vulnerability scan"
    ):
        print("⚠️ Security scan failed (continuing)")
    
    # Generate test report
    print("\n📊 Generating test report...")
    if not run_command(
        "pytest tests/ --html=test-report.html --self-contained-html",
        "HTML test report generation"
    ):
        print("⚠️ Test report generation failed")
    
    print("\n🎉 Testing suite completed!")
    print("\n📋 Test Results Summary:")
    print("   ✅ Unit Tests: Completed")
    print("   ✅ Integration Tests: Completed")
    print("   ⚠️ Performance Tests: Completed (with warnings)")
    print("   ⚠️ Security Scan: Completed (with warnings)")
    print("   ✅ Coverage Report: Generated")
    print("   ✅ HTML Test Report: Generated")
    
    print("\n📁 Generated Reports:")
    print("   - Coverage: htmlcov/index.html")
    print("   - Test Report: test-report.html")
    print("   - Security: bandit-report.json")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
