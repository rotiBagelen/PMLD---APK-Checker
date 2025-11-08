# External Network Access Setup Guide

This guide explains how to make APKTrust accessible from external networks.

## Quick Setup

### 1. Backend (Flask API)

The backend is already configured to accept external connections:
- Host: `0.0.0.0` (accepts connections from any network interface)
- Port: `5000`
- CORS: Enabled for all origins

**Start the backend:**
```bash
python app.py
```

The server will display:
```
🌐 Server accessible at:
   Local:   http://localhost:5000
   Network: http://YOUR_IP:5000
```

### 2. Frontend (React/Vite)

The frontend is configured to:
- Accept external connections on `0.0.0.0`
- Auto-detect API URL based on access method

**Start the frontend:**
```bash
cd "FRONTEND PMLD REVISED"
npm run dev
```

Vite will display:
```
➜  Local:   http://localhost:5173/
➜  Network: http://YOUR_IP:5173/
```

## Configuration Options

### Option 1: Automatic Detection (Recommended)

The frontend automatically detects the API URL:
- If accessed via `localhost` → API: `http://localhost:5000`
- If accessed via IP address → API: `http://YOUR_IP:5000`
- Works automatically for most cases

### Option 2: Environment Variables

Create `.env` file in frontend directory:
```
VITE_API_URL=http://YOUR_SERVER_IP:5000/api
```

Then rebuild:
```bash
npm run build
npm run preview
```

### Option 3: Hardcode IP Address

Edit `src/config.ts and set specific IP:
```typescript
export const API_BASE_URL = 'http://192.168.1.100:5000/api';
```

## Network Requirements

### Firewall Configuration

**Windows Firewall:**
1. Open Windows Defender Firewall
2. Allow apps through firewall
3. Allow Python and Node.js (or allow ports 5000 and 5173)

**Or manually allow ports:**
```powershell
# Allow backend port
netsh advfirewall firewall add rule name="APKTrust Backend" dir=in action=allow protocol=TCP localport=5000

# Allow frontend port
netsh advfirewall firewall add rule name="APKTrust Frontend" dir=in action=allow protocol=TCP localport=5173
```

**Linux (UFW):**
```bash
sudo ufw allow 5000/tcp
sudo ufw allow 5173/tcp
```

**Router/Network:**
- Ensure router doesn't block incoming connections
- For internet access, configure port forwarding (ports 5000 and 5173)

## Accessing from External Devices

### On Same Network (LAN)

1. Find your computer's IP address:
   - **Windows:** `ipconfig` → IPv4 Address
   - **Linux/Mac:** `ifconfig` or `ip addr`

2. Access from other devices:
   - Frontend: `http://YOUR_IP:5173`
   - Backend API: `http://YOUR_IP:5000/api/health`

### From Internet (WAN)

1. **Get your public IP:**
   ```bash
   curl ifconfig.me
   ```

2. **Configure router port forwarding:**
   - External Port 5173 → Internal IP:5173 (Frontend)
   - External Port 5000 → Internal IP:5000 (Backend)

3. **Access:**
   - Frontend: `http://YOUR_PUBLIC_IP:5173`
   - **Note:** Update frontend API URL to use public IP or domain

## Production Deployment

For production, consider:

1. **Reverse Proxy (Nginx/Apache):**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:5173;
       }
       
       location /api {
           proxy_pass http://localhost:5000;
       }
   }
   ```

2. **HTTPS/SSL:**
   - Use Let's Encrypt for free SSL certificates
   - Configure HTTPS in reverse proxy

3. **Process Manager:**
   - Use PM2 for Node.js frontend
   - Use systemd/gunicorn for Flask backend

## Testing External Access

1. **Test backend:**
   ```bash
   curl http://YOUR_IP:5000/api/health
   ```

2. **Test frontend:**
   - Open browser on external device
   - Navigate to `http://YOUR_IP:5173`

3. **Check API connection:**
   - Open browser console (F12)
   - Check for CORS or connection errors

## Troubleshooting

### Cannot Access from External Network

1. **Check firewall rules** - Ensure ports are open
2. **Verify IP address** - Use correct network interface IP
3. **Check router settings** - Some routers block inter-device communication
4. **Test localhost first** - Ensure services work locally

### CORS Errors

The backend is configured to accept all origins. If you see CORS errors:
- Check backend is running on `0.0.0.0`
- Verify CORS configuration in `app.py`
- Check browser console for specific error messages

### API Connection Failed

1. **Check API URL in frontend:**
   - Open browser DevTools → Network tab
   - Check what URL is being called
   
2. **Test API directly:**
   ```bash
   curl http://YOUR_IP:5000/api/health
   ```

3. **Update frontend config:**
   - Edit `src/config.ts` if auto-detection fails
   - Or set `VITE_API_URL` environment variable

## Security Considerations

⚠️ **For Production:**

1. **Don't use `debug=True`** in Flask
2. **Restrict CORS origins** instead of `*`
3. **Use HTTPS** for encrypted connections
4. **Add authentication** for API endpoints
5. **Rate limiting** to prevent abuse
6. **Input validation** on upload endpoints

## Quick Reference

| Component | Port | Access URL |
|-----------|------|------------|
| Frontend  | 5173 | `http://YOUR_IP:5173` |
| Backend   | 5000 | `http://YOUR_IP:5000` |

**To find your IP:**
- Windows: `ipconfig` → IPv4 Address
- Linux/Mac: `hostname -I` or `ifconfig`

