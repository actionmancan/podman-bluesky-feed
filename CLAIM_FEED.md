# How to Claim Your Feed on Bluesky

## Method 1: Using the Script (Easiest)

Run the publish script locally:

```bash
cd "/Users/nesmith/Documents/cursor junk"
source venv/bin/activate
python publish_feed.py
```

This will create a feed generator record in your Bluesky account, making your feed discoverable.

## Method 2: Manual Claim via Bluesky App

1. **Open Bluesky** (web or app)
2. **Go to your profile** → Click on your handle
3. **Look for "Feeds" section** → Click "Discover Feeds" or "Add Feed"
4. **Enter your feed URI**:
   ```
   at://did:plc:oe2nzi6rjpijm5o2w2gp7jzo/feed/podman-community
   ```
5. **Click "Subscribe"** or "Add Feed"

## Method 3: Search and Subscribe

1. **In Bluesky**, use the search function
2. **Search for**: `at://did:plc:oe2nzi6rjpijm5o2w2gp7jzo/feed/podman-community`
3. **Click on the feed** when it appears
4. **Click "Subscribe"**

## Method 4: Direct Link (if supported)

Some Bluesky clients support direct feed links. Try:
- `bsky://feed/did:plc:oe2nzi6rjpijm5o2w2gp7jzo/podman-community`
- Or just paste the `at://` URI in a post and click it

## Verify Your Feed is Claimed

After claiming, you should see:
- Feed appears in your "My Feeds" list
- Feed shows up when others search for Podman-related feeds
- You can share the feed URI and others can subscribe

## Troubleshooting

**If feed doesn't appear:**
- Make sure your feed generator is running: `https://feed.laswaan.com/health`
- Verify DID endpoint works: `https://feed.laswaan.com/.well-known/atproto-did`
- Check feed description: `https://feed.laswaan.com/xrpc/app.bsky.feed.describeFeedGenerator`
- Wait a few minutes for Bluesky to discover the feed

**If you get errors:**
- Ensure your `.env` file has correct credentials
- Make sure you're using an app password (not your regular password)
- Check Render logs for any errors

## Your Feed URI

```
at://did:plc:oe2nzi6rjpijm5o2w2gp7jzo/feed/podman-community
```

Share this with others so they can subscribe to your Podman Community feed!

