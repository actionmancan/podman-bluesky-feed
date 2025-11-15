#!/usr/bin/env python3
"""
Update the existing feed record to point to the correct service endpoint
"""

import os
from atproto import Client
from dotenv import load_dotenv

load_dotenv()

client = Client()
client.login(login=os.getenv('BLUESKY_HANDLE'), password=os.getenv('BLUESKY_PASSWORD'))

# Update the existing feed record to change the DID
print("Updating feed record...")
print(f"Setting DID to: {client.me.did}")
print(f"Service endpoint: https://feed.laswaan.com")

from datetime import datetime, timezone

# Get existing record
records = client.com.atproto.repo.list_records(
    params={'repo': client.me.did, 'collection': 'app.bsky.feed.generator'}
)

if records.records:
    rkey = records.records[0].uri.split('/')[-1]
    
    # Update it with the correct configuration
    now = datetime.now(timezone.utc)
    created_at = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    client.com.atproto.repo.put_record(
        data={
            'repo': client.me.did,
            'collection': 'app.bsky.feed.generator',
            'rkey': rkey,
            'record': {
                'did': client.me.did,  # Use the account DID
                'displayName': 'Podman Community',
                'description': 'A curated feed for the Podman containerization community',
                'createdAt': created_at,
            }
        }
    )
    
    print(f"✓ Updated feed record")
    print(f"Feed URI: at://{client.me.did}/app.bsky.feed.generator/{rkey}")
    print(f"\nThe feed generator service at https://feed.laswaan.com will serve this feed")
else:
    print("No feed records found")

