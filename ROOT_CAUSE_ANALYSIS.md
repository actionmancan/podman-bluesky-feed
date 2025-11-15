# Root Cause Analysis: Feed Generator Configuration Issue

## Problem
Error message: "invalid feed generator service details in did document: did:web:feed.laswaan.com"

## Root Cause Found
The DID document had the **wrong service type**. Bluesky requires the service type to be `BskyFeedGenerator`, but we were using `AtprotoFeedGenerator`.

## What Was Wrong

### Incorrect Configuration:
```json
{
  "service": [
    {
      "id": "#atproto_feed",
      "type": "AtprotoFeedGenerator",  ← WRONG
      "serviceEndpoint": "https://feed.laswaan.com"
    }
  ]
}
```

### Correct Configuration:
```json
{
  "service": [
    {
      "id": "#bsky_fg",
      "type": "BskyFeedGenerator",  ← CORRECT
      "serviceEndpoint": "https://feed.laswaan.com"
    }
  ]
}
```

## Changes Made

1. **Updated `feed_generator.py`**:
   - Changed service `id` from `#atproto_feed` to `#bsky_fg`
   - Changed service `type` from `AtprotoFeedGenerator` to `BskyFeedGenerator`

2. **Updated `.well-known/did.json`**:
   - Same changes as above

3. **Committed and pushed** to GitHub

## Why This Fixes It

Bluesky's feed generator specification requires:
- Service ID: `#bsky_fg` (Bluesky Feed Generator)
- Service Type: `BskyFeedGenerator` (exact spelling)
- Service Endpoint: The URL where the feed generator is hosted

Using the wrong type caused Bluesky to reject the DID document as misconfigured.

## Next Steps

1. **Wait 2-3 minutes** for Render to deploy the fix
2. **Verify the fix**:
   ```bash
   curl https://feed.laswaan.com/.well-known/did.json
   ```
   Should show `"type": "BskyFeedGenerator"`

3. **Try subscribing again** in Bluesky:
   ```
   at://did:web:feed.laswaan.com/feed/podman-community
   ```

## Timeline

- Initial DID used: `did:plc:oe2nzi6rjpijm5o2w2gp7jzo` (user's account DID - wrong approach)
- Switched to: `did:web:feed.laswaan.com` (correct approach)
- Issue: Used wrong service type `AtprotoFeedGenerator`
- Fix: Changed to `BskyFeedGenerator`

## Lessons Learned

1. `did:plc` DIDs are for user accounts, not feed generators
2. `did:web` is the correct approach for feed generators
3. Service type must be exactly `BskyFeedGenerator` (case-sensitive)
4. Service ID should be `#bsky_fg` per Bluesky conventions

