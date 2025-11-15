#!/usr/bin/env python3
"""
Fix feed declaration - delete old and create new with correct DID
"""

import os
from atproto import Client
from dotenv import load_dotenv
from datetime import datetime, timezone
import config

load_dotenv()

def fix_feed_declaration():
    """Delete old feed declarations and create new one with correct DID."""
    
    handle = os.getenv("BLUESKY_HANDLE")
    password = os.getenv("BLUESKY_PASSWORD")
    
    if not handle or not password:
        print("Error: BLUESKY_HANDLE and BLUESKY_PASSWORD must be set")
        return
    
    print(f"Logging in as {handle}...")
    client = Client()
    client.login(login=handle, password=password)
    print("✓ Logged in")
    
    # List all existing feed generator records
    print("\nChecking existing feed generator records...")
    records = client.com.atproto.repo.list_records(
        params={'repo': client.me.did, 'collection': 'app.bsky.feed.generator'}
    )
    
    # Delete all old records
    for record in records.records:
        print(f"\nDeleting old record: {record.uri}")
        try:
            did = record.value.did if hasattr(record.value, 'did') else 'unknown'
            print(f"  DID: {did}")
        except:
            print(f"  DID: (could not read)")
        
        try:
            rkey = record.uri.split('/')[-1]
            client.com.atproto.repo.delete_record(
                data={
                    'repo': client.me.did,
                    'collection': 'app.bsky.feed.generator',
                    'rkey': rkey
                }
            )
            print(f"  ✓ Deleted")
        except Exception as e:
            print(f"  ✗ Error deleting: {e}")
    
    # Wait a moment
    import time
    time.sleep(1)
    
    # Create new record with correct DID
    print(f"\nCreating new feed declaration...")
    print(f"Feed URI: {config.FEED_URI}")
    print(f"Service DID: did:web:feed.laswaan.com")
    
    try:
        now = datetime.now(timezone.utc)
        created_at = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        record = client.com.atproto.repo.create_record(
            data={
                "repo": client.me.did,
                "collection": "app.bsky.feed.generator",
                "record": {
                    "did": "did:web:feed.laswaan.com",
                    "displayName": config.FEED_NAME,
                    "description": config.FEED_DESCRIPTION,
                    "createdAt": created_at,
                },
            }
        )
        
        print(f"\n✓ Feed declaration created successfully!")
        print(f"\nNew feed URI: {config.FEED_URI}")
        print(f"\nTry subscribing again in Bluesky!")
        
        return record
        
    except Exception as e:
        print(f"\n✗ Error creating feed: {e}")
        return None

if __name__ == "__main__":
    fix_feed_declaration()

