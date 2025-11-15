# Deployment Guide for Podman Community Bluesky Feed

## Prerequisites

1. **Bluesky Account**: You need a Bluesky account to authenticate the feed generator
2. **App Password**: Create an app password in Bluesky settings (Settings → App Passwords)
3. **DID (Decentralized Identifier)**: You'll need to create a DID for your feed generator

## Step 1: Create a DID

You need a DID (Decentralized Identifier) for your feed generator. You can:

1. Use a DID service like `did:plc:` (Bluesky's DID method)
2. Or use another DID method supported by Bluesky

For Bluesky, you typically need to:
- Create a DID using a DID service
- Configure it to point to your feed generator's domain

## Step 2: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
BLUESKY_HANDLE=your-handle.bsky.social
BLUESKY_PASSWORD=your-app-password-here
FEED_GENERATOR_DID=did:plc:your-actual-did
PORT=8000
```

## Step 3: Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 4: Test Locally

Run the feed generator locally:

```bash
python feed_generator.py
```

The server will start on `http://localhost:8000`

Test the endpoints:
- `http://localhost:8000/.well-known/atproto-did` - Should return your DID
- `http://localhost:8000/xrpc/app.bsky.feed.describeFeedGenerator` - Should describe your feed

## Step 5: Deploy to a Hosting Service

### Option A: Railway

1. Create a Railway account
2. Create a new project
3. Connect your Git repository
4. Set environment variables in Railway dashboard
5. Deploy

### Option B: Fly.io

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Login: `fly auth login`
3. Create app: `fly launch`
4. Set secrets: `fly secrets set BLUESKY_HANDLE=... BLUESKY_PASSWORD=...`
5. Deploy: `fly deploy`

### Option C: Heroku

1. Install Heroku CLI
2. Create app: `heroku create your-feed-name`
3. Set config vars: `heroku config:set BLUESKY_HANDLE=... BLUESKY_PASSWORD=...`
4. Deploy: `git push heroku main`

### Option D: Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "feed_generator.py"]
```

Build and run:
```bash
docker build -t podman-feed .
docker run -p 8000:8000 --env-file .env podman-feed
```

## Step 6: Configure DNS and DID

1. Point your domain to your hosting service
2. Ensure `/.well-known/atproto-did` is accessible at your domain
3. Update your DID document to point to your domain

## Step 7: Publish Your Feed

Once deployed, your feed will be available at:
```
at://did:plc:your-did/feed/podman-community
```

Users can subscribe to your feed by:
1. Going to Bluesky
2. Searching for your feed URI
3. Clicking "Subscribe"

## Troubleshooting

### Rate Limits
Bluesky has rate limits. If you hit them:
- Reduce the number of searches in `search_podman_posts()`
- Add delays between requests
- Consider caching results

### Authentication Issues
- Ensure your app password is correct
- Check that your Bluesky handle is correct (include `.bsky.social`)

### Feed Not Appearing
- Verify your DID is correctly configured
- Check that `/.well-known/atproto-did` returns the correct DID
- Ensure your feed URI matches what's in `config.py`

## Monitoring

Consider adding:
- Health check endpoint: `GET /health`
- Logging to a service like Logtail or Datadog
- Error tracking with Sentry

