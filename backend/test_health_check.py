#!/usr/bin/env python3
"""
Health check test script

This script tests the health check endpoints to ensure they respond successfully.
"""

import requests
import json
import sys
import time
import os

def test_health_endpoints(base_url, timeout=5):
    """
    Test all health check endpoints
    """
    # Test both essential and detailed health endpoints
    endpoints = ["/", "/health", "/api/health", "/api/health/detailed"]
    results = {}
    
    for endpoint in endpoints:
        full_url = f"{base_url}{endpoint}"
        print(f"Testing health check endpoint: {full_url}")
        
        try:
            start_time = time.time()
            response = requests.get(full_url, timeout=timeout)
            duration = time.time() - start_time
            
            results[endpoint] = {
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
                "success": response.status_code == 200,
                "content_type": response.headers.get("Content-Type", ""),
                "response_size_bytes": len(response.content),
            }
            
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    results[endpoint]["json_valid"] = True
                    results[endpoint]["response"] = json_data
                except json.JSONDecodeError:
                    results[endpoint]["json_valid"] = False
                    results[endpoint]["response_text"] = response.text[:100] + "..." if len(response.text) > 100 else response.text
                
                print(f"✅ {endpoint} - Status: {response.status_code}, Time: {results[endpoint]['duration_ms']}ms")
            else:
                results[endpoint]["response_text"] = response.text[:100] + "..." if len(response.text) > 100 else response.text
                print(f"❌ {endpoint} - Status: {response.status_code}, Time: {results[endpoint]['duration_ms']}ms")
                
        except requests.RequestException as e:
            results[endpoint] = {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
            print(f"❌ {endpoint} - Error: {str(e)}")
    
    return results

if __name__ == "__main__":
    # Get test URL from environment variable or command line argument or default
    base_url = os.environ.get("TEST_URL") or (sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000")
    timeout = int(os.environ.get("TEST_TIMEOUT") or (sys.argv[2] if len(sys.argv) > 2 else 5))
    
    print(f"Testing health endpoints on {base_url} with {timeout}s timeout")
    results = test_health_endpoints(base_url, timeout)
    
    # Print summary
    all_succeeded = all(result.get("success", False) for result in results.values())
    print("\nSummary:")
    print(f"{'✅ All tests passed!' if all_succeeded else '❌ Some tests failed!'}")
    
    # Check root endpoint specifically - critical for Railway health checks
    if results.get("/", {}).get("success", False):
        print("✅ Root endpoint (/) is working - Railway health checks should pass")
    else:
        print("❌ Root endpoint (/) is NOT working - Railway health checks will FAIL")
    
    # Check health endpoint - also important for Railway
    if results.get("/health", {}).get("success", False):
        print("✅ Health endpoint (/health) is working")
    else:
        print("❌ Health endpoint (/health) is NOT working")
    
    # Detailed results
    print("\nDetailed results:")
    for endpoint, result in results.items():
        success = "✅" if result.get("success", False) else "❌"
        if "status_code" in result:
            print(f"{success} {endpoint} - Status: {result['status_code']}, Time: {result.get('duration_ms', 'N/A')}ms")
        else:
            print(f"{success} {endpoint} - Error: {result.get('error', 'Unknown error')}")
    
    # Exit with appropriate code
    sys.exit(0 if all_succeeded else 1) 