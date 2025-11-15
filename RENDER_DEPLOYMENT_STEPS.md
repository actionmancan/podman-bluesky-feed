# Exact Steps: Deploy Feed Generator to Render

## Step 1: Deploy to Render

1. **Go to Render**: https://render.com
2. **Sign up/Login** (use GitHub to connect easily)
3. **Click "New +"** → **"Web Service"**
4. **Connect Repository**:
   - If not connected: Click "Connect account" → Authorize GitHub
   - Select repository: `actionmancan/podman-bluesky-feed`
5. **Configure Service**:
   - **Name**: `podman-feed` (or any name)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python feed_generator.py`
6. **Scroll down to Environment Variables** - Click "Add Environment Variable" for each:
   - `BLUESKY_HANDLE` = `actionmancan.bsky.social`
   - `BLUESKY_PASSWORD` = `[your-app-password]` (get from Bluesky Settings → App Passwords)
   - `FEED_GENERATOR_DID` = `did:plc:oe2nzi6rjpijm5o2w2gp7jzo`
   - `PORT` = `8000`
7. **Click "Create Web Service"**
8. **Wait 3-5 minutes** for deployment to complete
9. **Copy your Render URL** (e.g., `podman-feed.onrender.com`)

## Step 2: Connect to Your Domain (GoDaddy)

1. **In Render Dashboard**:
   - Click on your service (`podman-feed`)
   - Go to **"Settings"** tab
   - Scroll to **"Custom Domains"**
   - Click **"Add Custom Domain"**
   - Enter: `feed.laswaan.com`
   - Click **"Save"**
   - Render will show you DNS instructions (you'll add a CNAME)

2. **In GoDaddy DNS**:
   - Log into GoDaddy
   - Go to **"My Products"** → **"DNS"** (or find laswaan.com → Manage DNS)
   - Click **"Add"** or **"+"** to add new record
   - Select **"CNAME"** type
   - Fill in:
     - **Name**: `feed` (just "feed", no @ or www)
     - **Value**: `podman-feed.onrender.com` (your Render URL)
     - **TTL**: `600` (or leave default)
   - Click **"Save"**

3. **Wait for DNS Propagation**:
   - Usually 5-60 minutes
   - You can check with: `nslookup feed.laswaan.com` or `dig feed.laswaan.com`

## Step 3: Test Your Feed

Once DNS propagates, test these URLs:

1. **Health Check**:
   ```bash
   curl https://feed.laswaan.com/health
   ```
   Should return: `{"status":"healthy","service":"podman-community-feed"}`

2. **DID Endpoint**:
   ```bash
   curl https://feed.laswaan.com/.well-known/atproto-did
   ```
   Should return: `{"did":"did:plc:oe2nzi6rjpijm5o2w2gp7jzo"}`

3. **Feed Description**:
   ```bash
   curl https://feed.laswaan.com/xrpc/app.bsky.feed.describeFeedGenerator
   ```
   Should return feed info with your feed URI

4. **Feed Content** (test in browser):
   ```
   https://feed.laswaan.com/xrpc/app.bsky.feed.getFeedSkeleton?feed=at://did:plc:oe2nzi6rjpijm5o2w2gp7jzo/feed/podman-community
   ```

## Step 4: Make Feed Available in Bluesky

Your feed URI is:
```
at://did:plc:oe2nzi6rjpijm5o2w2gp7jzo/feed/podman-community
```

### Option A: Share Feed Link
1. Go to Bluesky
2. Post about your new feed
3. Include the feed URI: `at://did:plc:oe2nzi6rjpijm5o2w2gp7jzo/feed/podman-community`
4. People can click it to subscribe

### Option B: Direct Subscribe (if you have the feed URL)
1. In Bluesky, go to your profile
2. Look for "Feeds" section
3. Click "Discover Feeds" or "Add Feed"
4. Enter: `at://did:plc:oe2nzi6rjpijm5o2w2gp7jzo/feed/podman-community`

### Option C: Test Feed Discovery
Bluesky should be able to discover your feed through:
- Your DID: `did:plc:oe2nzi6rjpijm5o2w2gp7jzo`
- Feed generator endpoint: `https://feed.laswaan.com`

## Step 5: Verify Feed is Working

1. **Check Render Logs**:
   - Go to Render dashboard → Your service → "Logs" tab
   - Look for any errors
   - Should see: "Application startup complete"

2. **Test Feed Endpoints**:
   - All endpoints should return 200 OK
   - Feed skeleton should return posts (may be empty if no Podman posts found yet)

3. **Monitor Feed**:
   - Feed will search for Podman-related posts
   - It may take a few minutes to populate
   - Check logs to see if it's finding posts

## Troubleshooting

### If feed doesn't appear in Bluesky:
- Verify DID endpoint returns correct DID
- Check feed description endpoint works
- Ensure HTTPS is working (Bluesky requires HTTPS)
- Wait a few minutes for Bluesky to discover the feed

### If Render service won't start:
- Check environment variables are set correctly
- Verify `BLUESKY_PASSWORD` is correct (app password, not regular password)
- Check logs for Python errors

### If DNS not working:
- Wait longer (can take up to 24 hours, usually 5-60 min)
- Verify CNAME record is correct in GoDaddy
- Check with: `nslookup feed.laswaan.com`

## Your Feed is Live When:

✅ `https://feed.laswaan.com/health` returns healthy  
✅ `https://feed.laswaan.com/.well-known/atproto-did` returns your DID  
✅ `https://feed.laswaan.com/xrpc/app.bsky.feed.describeFeedGenerator` works  
✅ You can subscribe to `at://did:plc:oe2nzi6rjpijm5o2w2gp7jzo/feed/podman-community` in Bluesky

## Next Steps After Deployment

1. **Share your feed** with the Podman community
2. **Monitor logs** in Render to see what posts are being found
3. **Customize keywords** in `config.py` if needed (then push to GitHub, Render auto-deploys)
4. **Add more Podman accounts** to `config.py` to include in feed

