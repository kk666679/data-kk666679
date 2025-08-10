import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

class HRMSLoadTest:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.results = []

    async def test_endpoint(self, session, endpoint, method="GET", data=None):
        start_time = time.time()
        try:
            if method == "GET":
                async with session.get(f"{self.base_url}{endpoint}") as response:
                    status = response.status
                    await response.text()
            else:
                async with session.post(f"{self.base_url}{endpoint}", json=data) as response:
                    status = response.status
                    await response.text()
            
            end_time = time.time()
            return {
                "endpoint": endpoint,
                "status": status,
                "response_time": end_time - start_time,
                "success": status < 400
            }
        except Exception as e:
            return {
                "endpoint": endpoint,
                "status": 0,
                "response_time": time.time() - start_time,
                "success": False,
                "error": str(e)
            }

    async def run_concurrent_tests(self, concurrent_users=100):
        """Run load test with concurrent users"""
        test_scenarios = [
            ("/health", "GET"),
            ("/api/epf-calculator", "POST", {"basic_salary": 5000}),
            ("/api/er/sentiment-analysis", "POST", {
                "department": "IT",
                "engagement_score": 7.5,
                "comments": ["Good work environment"]
            })
        ]

        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in range(concurrent_users):
                for endpoint, method, *data in test_scenarios:
                    task = self.test_endpoint(
                        session, endpoint, method, 
                        data[0] if data else None
                    )
                    tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            return results

    def analyze_results(self, results):
        """Analyze load test results"""
        total_requests = len(results)
        successful_requests = sum(1 for r in results if r["success"])
        failed_requests = total_requests - successful_requests
        
        response_times = [r["response_time"] for r in results if r["success"]]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        return {
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": (successful_requests / total_requests) * 100,
            "avg_response_time": avg_response_time,
            "max_response_time": max(response_times) if response_times else 0
        }

async def main():
    load_test = HRMSLoadTest()
    print("🚀 Starting HRMS Load Test...")
    
    results = await load_test.run_concurrent_tests(concurrent_users=50)
    analysis = load_test.analyze_results(results)
    
    print(f"📊 Load Test Results:")
    print(f"   Success Rate: {analysis['success_rate']:.2f}%")
    print(f"   Avg Response Time: {analysis['avg_response_time']:.3f}s")
    print(f"   Max Response Time: {analysis['max_response_time']:.3f}s")

if __name__ == "__main__":
    asyncio.run(main())