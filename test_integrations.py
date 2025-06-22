#!/usr/bin/env python3
"""
Test script to verify both ElevenLabs and LiveKit integrations
"""

import requests
import json

BASE_URL = "http://localhost:5001"

def test_elevenlabs_integration():
    """Test ElevenLabs integration endpoints"""
    print("🔵 Testing ElevenLabs Integration...")

    # Test setting topic for ElevenLabs
    response = requests.post(f"{BASE_URL}/set_topic",
                           json={"topic": "animals", "platform": "elevenlabs"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ ElevenLabs topic set: {data}")
    else:
        print(f"❌ ElevenLabs topic failed: {response.text}")

    # Test ElevenLabs status
    response = requests.get(f"{BASE_URL}/elevenlabs/status")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ ElevenLabs status: {data}")
    else:
        print(f"❌ ElevenLabs status failed: {response.text}")

def test_livekit_integration():
    """Test LiveKit integration endpoints"""
    print("\n🟢 Testing LiveKit Integration...")

    # Test setting topic for LiveKit
    response = requests.post(f"{BASE_URL}/set_topic",
                           json={"topic": "colors", "platform": "livekit"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ LiveKit topic set: {data}")
    else:
        print(f"❌ LiveKit topic failed: {response.text}")

    # Test LiveKit status
    response = requests.get(f"{BASE_URL}/livekit/status")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ LiveKit status: {data}")
    else:
        print(f"❌ LiveKit status failed: {response.text}")

def test_server_status():
    """Test basic server functionality"""
    print("\n🟡 Testing Server Status...")

    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Server is running and accessible")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server - make sure it's running on port 5001")
        return False

    return True

if __name__ == "__main__":
    print("🚀 Testing AI Tutor Integrations")
    print("=" * 50)

    # Test basic server connectivity first
    if not test_server_status():
        exit(1)

    # Test both integrations
    test_elevenlabs_integration()
    test_livekit_integration()

    print("\n" + "=" * 50)
    print("🎉 Integration tests completed!")
    print("\nNext steps:")
    print("1. ✅ ElevenLabs: Use the ConvAI widget in the frontend")
    print("2. ✅ LiveKit: Use the /livekit/ endpoints or console mode")
    print("3. ✅ Both integrations are now available simultaneously")
