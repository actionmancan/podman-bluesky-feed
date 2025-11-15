# Podman Community Bluesky Feed

A custom Bluesky feed generator that curates content related to the Podman containerization community.

## Features

- Filters posts containing Podman-related keywords and hashtags
- Includes posts from key Podman community accounts
- Real-time feed generation using ATProto
- Configurable filtering criteria

## Quick Start

1. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure your Bluesky credentials:**
   - Copy `env.example` to `.env`
   - Add your Bluesky handle and app password
   - Get an app password from: Bluesky Settings → App Passwords

4. **Run the feed generator:**
```bash
python feed_generator.py
```

5. **Test the endpoints:**
   - Health check: `http://localhost:8000/health`
   - Feed description: `http://localhost:8000/xrpc/app.bsky.feed.describeFeedGenerator`
   - Feed skeleton: `http://localhost:8000/xrpc/app.bsky.feed.getFeedSkeleton?feed=at://did:plc:your-did/feed/podman-community`

## Configuration

Edit `config.py` to customize:
- Keywords to search for
- Hashtags to include
- Accounts to follow
- Feed description and display name

## Deployment

The feed generator runs as a FastAPI server. Deploy it to a hosting service that supports Python applications (e.g., Railway, Fly.io, Heroku).

## Feed URL

Once deployed, your feed will be available at:
`https://your-domain.com/.well-known/atproto-did`

Users can subscribe to your feed using the feed URI in Bluesky.

