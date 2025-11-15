# Render Deployment Checklist

## Verify Render is Working

1. **Check Render Dashboard**:
   - Go to https://dashboard.render.com
   - Find your `podman-feed` service
   - Check status: Should be "Live" (green)
   - Check latest deploy: Should show recent deployment

2. **Check Logs**:
   - In Render dashboard → Your service → "Logs" tab
   - Look for:
     - "Application startup complete"
     - No error messages
     - Should see uvicorn/FastAPI startup messages

3. **Verify Environment Variables**:
   - Render dashboard → Your service → "Environment" tab
   - Verify these are set:
     - `BLUESKY_HANDLE=actionmancan.bsky.social`
     - `BLUESKY_PASSWORD=[your-app-password]`
     - `FEED_GENERATOR_DID=did:web:feed.laswaan.com` (or can be removed, we're using did:web now)
     - `PORT=8000`

4. **Test Endpoints**:
   ```bash
   # Health check
   curl https://feed.laswaan.com/health
   
   # DID endpoint
   curl https://feed.laswaan.com/.well-known/atproto-did
   
   # DID document
   curl https://feed.laswaan.com/.well-known/did.json
   
   # Feed description
   curl https://feed.laswaan.com/xrpc/app.bsky.feed.describeFeedGenerator
   ```

## If Render Shows Issues

1. **Service Not Starting**:
   - Check logs for Python errors
   - Verify all dependencies are in `requirements.txt`
   - Check if port is set correctly (8000)

2. **404 Errors**:
   - Verify custom domain is set correctly
   - Check DNS propagation (can take up to 24 hours)
   - Try accessing via Render URL directly (e.g., `podman-feed.onrender.com`)

3. **500 Errors**:
   - Check logs for specific error messages
   - Verify environment variables are set
   - Check if Bluesky credentials are correct

4. **Redeploy**:
   - In Render dashboard → "Manual Deploy" → "Deploy latest commit"
   - Or push a new commit to trigger auto-deploy

## Current Status

✅ Feed declaration fixed (old records deleted, new one created)
✅ DID endpoints working correctly
✅ Using `did:web:feed.laswaan.com` (correct format)

## Next Steps

1. Wait 1-2 minutes for Bluesky to recognize the new feed declaration
2. Try subscribing again: `at://did:web:feed.laswaan.com/feed/podman-community`
3. If still not working, check Render logs for any errors

