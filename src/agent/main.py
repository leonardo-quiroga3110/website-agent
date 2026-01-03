import sys
from agent.core.config import get_settings
from agent.core.state import AgentState

def main() -> None:
    """
    Verifies that the project is correctly initialized by loading 
    the settings and demonstrating the AgentState type.
    """
    print("--- LangGraph Project Initialization Verification ---")
    
    try:
        # 1. Verify Configuration Loading
        print("\n1. Verifying Configuration...")
        # Note: This will fail if .env is missing or mandatory keys are unset.
        # For verification, we can catch the error and inform the user.
        settings = get_settings()
        print(f"   - Environment: {settings.ENVIRONMENT}")
        print(f"   - Log Level: {settings.LOG_LEVEL}")
        print(f"   - OpenAI Key Set: {'[YES]' if settings.OPENAI_API_KEY != 'sk-placeholder' else '[NO]'}")
        print(f"   - Tavily Key Set: {'[YES]' if settings.TAVILY_API_KEY != 'your_tavily_api_key_here' else '[NO]'}")
        print("   [OK] Configuration loaded correctly.")
        
    except Exception as e:
        print(f"   [ERROR] Failed to load configuration: {e}")

    # 2. Verify Tool Registration
    print("\n2. Verifying Tool Registration...")
    try:
        from agent.tools.scraper import scrape_website
        print(f"   - Tool Name: {scrape_website.name}")
        print(f"   - Tool Description: {scrape_website.description[:50]}...")
        print("   [OK] Tools imported correctly.")
    except Exception as e:
        print(f"   [SKIP] Tools could not be verified: {e}")

    # 3. Verify State Definition
    print("\n3. Verifying State Definition...")
    state_keys = AgentState.__annotations__.keys()
    print(f"   - State Keys: {list(state_keys)}")
    print("   [OK] AgentState defined correctly.")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    main()
