#!/usr/bin/env python3
"""
Test script for LiveKit integration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        'LIVEKIT_API_KEY',
        'LIVEKIT_API_SECRET',
        'LIVEKIT_URL',
        'OPENAI_API_KEY'
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var) or os.getenv(var) == f'your_{var.lower()}_here':
            missing_vars.append(var)

    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Please update your .env file with proper values")
        return False

    print("✅ All required environment variables are set")
    return True

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import livekit_elevenlabs_integration
        print("✅ LiveKit ElevenLabs integration imported successfully")

        import elevenlabs_integration
        print("✅ ElevenLabs integration imported successfully")

        from livekit import agents
        print("✅ LiveKit agents imported successfully")

        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_livekit_functions():
    """Test LiveKit integration functions"""
    try:
        import livekit_elevenlabs_integration

        # Test topic setting
        livekit_elevenlabs_integration.set_livekit_topic("animals")
        print("✅ LiveKit topic setting works")

        # Check current topic
        current_topic = livekit_elevenlabs_integration.current_topic
        if current_topic == "animals":
            print("✅ LiveKit topic retrieval works")
        else:
            print(f"❌ LiveKit topic mismatch: expected 'animals', got '{current_topic}'")
            return False

        return True
    except Exception as e:
        print(f"❌ LiveKit function test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing LiveKit Integration\n")

    # Test 1: Environment variables
    if not check_environment():
        print("\n❌ Environment check failed")
        return False

    print()

    # Test 2: Imports
    if not test_imports():
        print("\n❌ Import test failed")
        return False

    print()

    # Test 3: Basic functionality
    if not test_livekit_functions():
        print("\n❌ Function test failed")
        return False

    print("\n🎉 All tests passed! LiveKit integration is ready.")
    print("\n📋 Next steps:")
    print("1. Make sure you have valid LiveKit credentials in your .env file")
    print("2. Run the LiveKit agent: python livekit_elevenlabs_integration.py dev")
    print("3. Or use it through the main Flask app: python main.py")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
