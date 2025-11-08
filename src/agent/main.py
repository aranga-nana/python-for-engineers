"""
Main entry point for the Navigation Agent

This script demonstrates the agent navigating between different locations.
"""

import os
import time
from agent import NavigationAgent


def main():
    """Run the navigation agent demo."""
    # Get map server URL from environment variable or use default
    map_server_url = os.getenv('MAP_SERVER_URL', 'http://localhost:5000')
    agent_id = os.getenv('AGENT_ID', 'agent-001')
    
    print("Navigation Agent Demo")
    print("=" * 60)
    
    # Wait for map server to be ready (when running in Docker)
    print(f"Connecting to map server at {map_server_url}...")
    for attempt in range(10):
        try:
            import requests
            response = requests.get(f"{map_server_url}/", timeout=2)
            if response.status_code == 200:
                print("✓ Map server is ready\n")
                break
        except:
            print(f"  Waiting for map server... (attempt {attempt + 1}/10)")
            time.sleep(2)
    else:
        print("⚠️  Warning: Could not connect to map server")
        print("   Make sure the map server is running")
        print("   The agent will attempt to continue anyway...\n")
    
    # Create agent
    agent = NavigationAgent(map_server_url, agent_id)
    
    # Example locations (San Francisco Bay Area)
    locations = {
        'San Francisco': (37.7749, -122.4194),
        'Oakland': (37.8044, -122.2712),
        'San Jose': (37.3382, -121.8863),
        'Berkeley': (37.8715, -122.2730)
    }
    
    # Navigation 1: San Francisco to Oakland
    print("\n" + "=" * 60)
    print("Navigation 1: San Francisco → Oakland")
    print("=" * 60)
    agent.start_navigation(
        start=locations['San Francisco'],
        destination=locations['Oakland'],
        step_delay=0.5
    )
    
    time.sleep(2)
    
    # Navigation 2: Oakland to San Jose
    print("\n" + "=" * 60)
    print("Navigation 2: Oakland → San Jose")
    print("=" * 60)
    agent.start_navigation(
        start=locations['Oakland'],
        destination=locations['San Jose'],
        step_delay=0.5
    )
    
    # Final status
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    status = agent.get_status()
    print(f"\nFinal Agent Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    print()


if __name__ == "__main__":
    main()
