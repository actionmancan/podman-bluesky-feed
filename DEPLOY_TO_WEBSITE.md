# Deploying Feed Generator to Your Own Website

Yes! You can absolutely deploy the feed generator to your existing website. Here are the main approaches:

## Option 1: Deploy as a Subdomain (Recommended)

Deploy to a subdomain like `feed.yourdomain.com` or `bluesky.yourdomain.com`:

### Steps:

1. **Set up a subdomain** pointing to your server/hosting
2. **Deploy the Python app** to your server
3. **Configure reverse proxy** (nginx/Apache) to forward requests to the Python app
4. **Set up SSL certificate** (Let's Encrypt) for HTTPS

### Example nginx configuration:

```nginx
server {
    listen 80;
    server_name feed.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Option 2: Deploy to a Path on Your Domain

Deploy to `yourdomain.com/bluesky-feed` or similar:

### Steps:

1. Configure your web server to route `/bluesky-feed/*` to the Python app
2. Update the feed generator endpoints accordingly

## Option 3: Use Your Existing Domain with did:web

If you want to use `did:web` instead of `did:plc`:

1. **Create a DID document** at `https://yourdomain.com/.well-known/did.json`
2. **Host the feed generator** at your domain
3. **Update your DID** to point to your domain

### Example did.json structure:

```json
{
  "@context": ["https://www.w3.org/ns/did/v1"],
  "id": "did:web:yourdomain.com",
  "service": [
    {
      "id": "#atproto_feed",
      "type": "AtprotoFeedGenerator",
      "serviceEndpoint": "https://yourdomain.com"
    }
  ]
}
```

## Hosting Options for Your Website

### If you have a VPS/Server:

1. **Install Python 3.11+** and dependencies
2. **Set up a process manager** (systemd, supervisor, or PM2)
3. **Configure reverse proxy** (nginx/Apache)
4. **Set up SSL** with Let's Encrypt

### If you use shared hosting:

Most shared hosting doesn't support long-running Python processes. Consider:
- **Upgrading to VPS** or cloud hosting
- **Using a service** like Railway, Fly.io, or Render (they can use your domain)

### If you use a Platform-as-a-Service:

Services like **Railway**, **Fly.io**, **Render**, or **Heroku** can use your custom domain:

1. Deploy your app to the platform
2. Add your domain in the platform's settings
3. Update DNS records to point to the platform
4. SSL is usually handled automatically

## Required Endpoints

Make sure these are accessible at your domain:

- `https://yourdomain.com/.well-known/atproto-did` - Returns your DID
- `https://yourdomain.com/xrpc/app.bsky.feed.describeFeedGenerator` - Feed description
- `https://yourdomain.com/xrpc/app.bsky.feed.getFeedSkeleton` - Feed content
- `https://yourdomain.com/health` - Health check (optional)

## DNS Configuration

You'll need to add DNS records:

- **A record** or **CNAME** pointing to your server's IP or hostname
- **TXT record** (if using did:web) for DID verification

## Process Management

Use a process manager to keep the app running:

### systemd service example (`/etc/systemd/system/podman-feed.service`):

```ini
[Unit]
Description=Podman Community Bluesky Feed
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/feed-generator
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python feed_generator.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then enable and start:
```bash
sudo systemctl enable podman-feed
sudo systemctl start podman-feed
```

## Environment Variables

Make sure your `.env` file is on the server with:
- `BLUESKY_HANDLE`
- `BLUESKY_PASSWORD`
- `FEED_GENERATOR_DID`
- `PORT=8000` (or whatever port you choose)

## Testing After Deployment

1. Test health endpoint: `curl https://yourdomain.com/health`
2. Test DID endpoint: `curl https://yourdomain.com/.well-known/atproto-did`
3. Test feed description: `curl https://yourdomain.com/xrpc/app.bsky.feed.describeFeedGenerator`

## Important Notes

- **HTTPS is required** - Bluesky requires secure connections
- **Port 80/443** should be accessible (or use reverse proxy)
- **Keep the process running** - Use a process manager or container orchestration
- **Monitor logs** - Set up logging to track issues

## Quick Deploy Script Example

```bash
#!/bin/bash
# deploy.sh

# Pull latest code
git pull

# Activate venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Restart service
sudo systemctl restart podman-feed

echo "Deployment complete!"
```

