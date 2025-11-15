#!/usr/bin/env python3
"""
Update feed record to use did:web
"""

import os
from atproto import Client
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

client = Client()
client.login(login=os.getenv('BLUESKY_HANDLE'), password=os.getenv('BLUESKY_PASSWORD'))

# Get existing record
records = client.com.atproto.repo.list_records(
    params={'repo': client.me.did, 'collection': 'app.bsky.feed.generator'}
)

if records.records:
    rkey = records.records[0].uri.split('/')[-1]
    
    now = datetime.now(timezone.utc)
    created_at = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    # Update to use did:web
    client.com.atproto.repo.put_record(
        data={
            'repo': client.me.did,
            'collection': 'app.bsky.feed.generator',
            'rkey': rkey,
            'record': {
                'did': 'did:web:feed.laswaan.com',  # Use did:web!
                'displayName': 'Podman Community',
                'description': 'A curated feed for the Podman containerization community',
                'createdAt': created_at,
            }
        }
    )
    
    print(f"✓ Updated feed record to use did:web:feed.laswaan.com")
    print(f"Feed URI: at://{client.me.did}/app.bsky.feed.generator/{rkey}")
else:
    print("No feed records found")

