#!/usr/bin/env python3
"""
Quick script to verify if a Bluesky handle exists
"""

import sys
from atproto import Client

def verify_handle(handle: str):
    """Check if a Bluesky handle exists."""
    # Remove @ if present
    handle = handle.replace('@', '').strip()
    
    print(f"Checking handle: {handle}")
    
    try:
        # Create a client (no login needed to check profiles)
        client = Client()
        
        # Try to get the profile
        profile = client.get_profile(actor=handle)
        
        if profile:
            print(f"✅ Handle '{handle}' is VALID!")
            print(f"   Display Name: {profile.display_name or 'N/A'}")
            print(f"   DID: {profile.did}")
            print(f"   Description: {profile.description[:100] if profile.description else 'N/A'}...")
            return True
    except Exception as e:
        print(f"❌ Handle '{handle}' is NOT VALID or doesn't exist")
        print(f"   Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        handle = sys.argv[1]
    else:
        handle = "actionmancan.bsky.social"
    
    verify_handle(handle)

