#!/usr/bin/env python3
"""
Health check test script

This script tests the health check endpoints to ensure they respond successfully.
"""

import requests
import json
import sys
import time

def test_health_endpoints(base_url, timeout=5):
    """
    Test both health check endpoints
    """
    endpoints = ["/health", "/api/health"]
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
    # Default to localhost if no argument is provided
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    print(f"Testing health endpoints on {base_url} with {timeout}s timeout")
    results = test_health_endpoints(base_url, timeout)
    
    # Print summary
    all_succeeded = all(result.get("success", False) for result in results.values())
    print("\nSummary:")
    print(f"{'✅ All tests passed!' if all_succeeded else '❌ Some tests failed!'}")
    
    # Detailed results
    print("\nDetailed results:")
    print(json.dumps(results, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if all_succeeded else 1)

"""
Simple FastAPI application to test the health check endpoint
Run this with: python3 -m uvicorn test_health_check:app --port 8000
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
import uvicorn
import json
import time
import os

app = FastAPI()

@app.get("/health")
async def root_health_check():
    """
    Minimal health check endpoint
    """
    print("Health check endpoint accessed")
    return Response(content=json.dumps({"status": "ok"}), media_type="application/json")

@app.get("/")
async def root():
    """Root endpoint for testing"""
    return {"message": "Test server is running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 