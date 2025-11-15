#!/usr/bin/env python3
"""
Publish/Claim your feed generator on Bluesky

This script creates a feed declaration record in your Bluesky account,
making your feed discoverable and claimable.
"""

import os
from atproto import Client
from dotenv import load_dotenv
import config

# Load environment variables
load_dotenv()

def publish_feed():
    """Publish feed declaration to Bluesky."""
    
    # Get credentials
    handle = os.getenv("BLUESKY_HANDLE")
    password = os.getenv("BLUESKY_PASSWORD")
    
    if not handle or not password:
        print("Error: BLUESKY_HANDLE and BLUESKY_PASSWORD must be set in .env")
        return
    
    # Login to Bluesky
    print(f"Logging in as {handle}...")
    client = Client()
    client.login(login=handle, password=password)
    print("✓ Logged in successfully")
    
    # Feed generator service DID (use did:web)
    service_did = "did:web:feed.laswaan.com"
    
    # Feed URI
    feed_uri = config.FEED_URI
    
    print(f"\nPublishing feed declaration...")
    print(f"Feed URI: {feed_uri}")
    print(f"Service DID: {service_did}")
    
    # Create feed generator record
    # This creates a declaration that associates the feed with your account
    try:
        from datetime import datetime, timezone
        
        # Create the feed generator record
        # Format datetime in RFC-3339 format (required by ATProto)
        now = datetime.now(timezone.utc)
        created_at = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        record = client.com.atproto.repo.create_record(
            data={
                "repo": client.me.did,
                "collection": "app.bsky.feed.generator",
                "record": {
                    "did": service_did,
                    "displayName": config.FEED_NAME,
                    "description": config.FEED_DESCRIPTION,
                    "createdAt": created_at,
                },
            }
        )
        
        print(f"\n✓ Feed declaration published successfully!")
        print(f"\nYour feed is now claimable:")
        print(f"Feed URI: {feed_uri}")
        print(f"\nTo subscribe:")
        print(f"1. Go to Bluesky")
        print(f"2. Search for: {feed_uri}")
        print(f"3. Or go to your profile → Feeds → Discover Feeds")
        print(f"4. Enter the feed URI to subscribe")
        
        return record
        
    except Exception as e:
        print(f"\n✗ Error publishing feed: {e}")
        print("\nNote: The feed generator might already be declared.")
        print("If you see an error about duplicate, that's okay - your feed is already claimed!")
        return None

if __name__ == "__main__":
    publish_feed()

