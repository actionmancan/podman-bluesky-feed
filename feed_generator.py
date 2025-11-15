#!/usr/bin/env python3
"""
Bluesky Feed Generator for Podman Community

This feed generator filters and curates Bluesky posts related to Podman
and the containerization community.
"""

import os
import re
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from atproto import Client, models
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

import config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Podman Community Feed")

# Global client instance (initialized lazily)
_client: Optional[Client] = None


def get_client() -> Client:
    """Get or create Bluesky client instance."""
    global _client
    if _client is None:
        handle = os.getenv("BLUESKY_HANDLE")
        password = os.getenv("BLUESKY_PASSWORD")
        if not handle or not password:
            raise ValueError("BLUESKY_HANDLE and BLUESKY_PASSWORD must be set")
        _client = Client()
        _client.login(login=handle, password=password)
        logger.info(f"Logged in to Bluesky as {handle}")
    return _client


def normalize_text(text: str) -> str:
    """Normalize text for keyword matching."""
    return text.lower()


def contains_podman_keywords(text: str) -> bool:
    """Check if text contains Podman-related keywords."""
    normalized = normalize_text(text)
    return any(keyword.lower() in normalized for keyword in config.PODMAN_KEYWORDS)


def contains_podman_hashtags(text: str) -> bool:
    """Check if text contains Podman-related hashtags."""
    normalized = normalize_text(text)
    hashtags = re.findall(r"#(\w+)", normalized)
    return any(
        hashtag.lower() in [tag.lower().replace("#", "") for tag in config.PODMAN_HASHTAGS]
        for hashtag in hashtags
    )


def is_from_podman_account(author_did: str, author_handle: str) -> bool:
    """Check if post is from a Podman community account."""
    # Check by handle
    if author_handle and author_handle.lower() in [
        acc.lower() for acc in config.PODMAN_ACCOUNTS
    ]:
        return True
    # Could also check by DID if we have DIDs in config
    return False


def should_include_post(post: dict) -> bool:
    """Determine if a post should be included in the feed."""
    record = post.get("record", {})
    text = record.get("text", "")
    
    # Check keywords
    if contains_podman_keywords(text):
        return True
    
    # Check hashtags
    if contains_podman_hashtags(text):
        return True
    
    # Check if from Podman account
    author = post.get("author", {})
    if is_from_podman_account(author.get("did", ""), author.get("handle", "")):
        return True
    
    return False


@app.get("/.well-known/atproto-did")
async def get_did():
    """Return the DID for this feed generator."""
    # Return did:web based on the domain
    return JSONResponse({
        "did": "did:web:feed.laswaan.com"
    })


@app.get("/.well-known/did.json")
async def get_did_document():
    """Return the DID document for did:web."""
    return JSONResponse({
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/multikey/v1"
        ],
        "id": "did:web:feed.laswaan.com",
        "service": [
            {
                "id": "#atproto_feed",
                "type": "AtprotoFeedGenerator",
                "serviceEndpoint": "https://feed.laswaan.com"
            }
        ]
    })


def search_podman_posts(limit: int = 100) -> List[Dict[str, Any]]:
    """Search for Podman-related posts using multiple strategies."""
    client = get_client()
    all_posts = []
    seen_uris = set()
    
    # Strategy 1: Search by hashtags
    for hashtag in config.PODMAN_HASHTAGS[:3]:  # Limit to avoid rate limits
        try:
            results = client.search_posts(q=f"#{hashtag}", limit=30)
            for post in results.posts:
                uri = post.uri
                if uri not in seen_uris:
                    seen_uris.add(uri)
                    all_posts.append(post.model_dump())
        except Exception as e:
            logger.warning(f"Error searching hashtag #{hashtag}: {e}")
    
    # Strategy 2: Search by keywords
    for keyword in config.PODMAN_KEYWORDS[:3]:  # Limit to avoid rate limits
        try:
            results = client.search_posts(q=keyword, limit=30)
            for post in results.posts:
                uri = post.uri
                if uri not in seen_uris:
                    seen_uris.add(uri)
                    all_posts.append(post.model_dump())
        except Exception as e:
            logger.warning(f"Error searching keyword {keyword}: {e}")
    
    # Strategy 3: Get posts from Podman accounts
    for account in config.PODMAN_ACCOUNTS:
        try:
            profile = client.get_profile(actor=account)
            if profile:
                # Get author feed
                author_feed = client.get_author_feed(
                    actor=account,
                    limit=20
                )
                for feed_item in author_feed.feed:
                    post = feed_item.post
                    uri = post.uri
                    if uri not in seen_uris:
                        seen_uris.add(uri)
                        all_posts.append(post.model_dump())
        except Exception as e:
            logger.warning(f"Error getting posts from {account}: {e}")
    
    # Sort by creation time (newest first)
    all_posts.sort(
        key=lambda x: x.get("record", {}).get("createdAt", ""),
        reverse=True
    )
    
    return all_posts[:limit]


@app.get("/xrpc/app.bsky.feed.getFeedSkeleton")
async def get_feed_skeleton(
    feed: str,
    limit: int = 50,
    cursor: Optional[str] = None,
):
    """
    Generate the feed skeleton for Bluesky.
    This is the main endpoint that Bluesky calls to get feed items.
    """
    try:
        # Search for Podman-related posts
        posts = search_podman_posts(limit=limit * 2)
        
        # Filter and format posts
        filtered_posts = []
        for post in posts:
            if should_include_post(post):
                filtered_posts.append({
                    "post": post.get("uri", ""),
                })
                if len(filtered_posts) >= limit:
                    break
        
        # Build response
        response: Dict[str, Any] = {
            "feed": filtered_posts,
        }
        
        # Add cursor for pagination if we have more posts
        if len(filtered_posts) == limit and len(posts) > limit:
            # Use timestamp as cursor (simplified)
            response["cursor"] = str(datetime.now().timestamp())
        
        return JSONResponse(response)
    
    except Exception as e:
        logger.error(f"Error generating feed: {e}", exc_info=True)
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )


@app.get("/xrpc/app.bsky.feed.describeFeedGenerator")
async def describe_feed_generator():
    """Describe the feed generator."""
    return JSONResponse({
        "did": "did:web:feed.laswaan.com",
        "feeds": [
            {
                "uri": config.FEED_URI,
                "displayName": config.FEED_NAME,
            }
        ],
    })


@app.get("/")
async def root():
    """Root endpoint - provides feed information."""
    return JSONResponse({
        "service": "Podman Community Bluesky Feed Generator",
        "status": "running",
        "feed_uri": config.FEED_URI,
        "feed_name": config.FEED_NAME,
        "endpoints": {
            "health": "/health",
            "did": "/.well-known/atproto-did",
            "did_document": "/.well-known/did.json",
            "feed_description": "/xrpc/app.bsky.feed.describeFeedGenerator",
            "feed_skeleton": "/xrpc/app.bsky.feed.getFeedSkeleton?feed=" + config.FEED_URI,
        }
    })


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Try to get client (will raise if not configured)
        client = get_client()
        return JSONResponse({
            "status": "healthy",
            "service": "podman-community-feed",
        })
    except Exception as e:
        return JSONResponse(
            {
                "status": "unhealthy",
                "error": str(e),
            },
            status_code=503
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

