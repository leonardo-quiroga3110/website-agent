import httpx
import json

def test_raw_sse():
    url = "https://mcp.tavily.com/mcp/?tavilyApiKey=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"
    headers = {"Accept": "text/event-stream"}
    
    print(f"Requesting SSE from {url}...")
    try:
        with httpx.stream("GET", url, headers=headers, timeout=10.0) as response:
            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        print(f"Received: {line}")
                        # Stop after first message to verify it works
                        break
            else:
                print(f"Failed: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_raw_sse()
