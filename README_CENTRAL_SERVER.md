# Mobile App Builder - Central Server & Lightweight Client

## 🏭 Architecture Overview

This system solves the POS computer resource limitations by using a **Central Server + Lightweight Client** architecture:

```
┌─────────────────────┐    ┌──────────────────────┐    ┌─────────────────┐
│   POS Computer      │───▶│   Central Server     │───▶│   EAS Cloud     │
│                     │    │   (Your Laptop)      │    │                 │
│ Lightweight Client  │    │ ┌──────────────────┐ │    │ - Builds APK    │
│ - 15MB executable   │    │ │ Docker Container │ │    │ - Returns file  │
│ - Same familiar UI  │    │ │ - Node.js        │ │    │                 │
│ - Zero installation │    │ │ - Expo CLI       │ │    │                 │
│ - Zero maintenance  │    │ │ - EAS CLI        │ │    │                 │
└─────────────────────┘    │ │ - Python API     │ │    │                 │
                           │ └──────────────────┘ │    │                 │
                           └──────────────────────┘    └─────────────────┘
```

## 🚀 Quick Start Guide

### Step 1: Set Up Central Server (Your Side)

1. **Install Docker Desktop** on your laptop/server computer:
   - Download from: https://www.docker.com/products/docker-desktop
   - Install and start Docker Desktop

2. **Set up EAS Token** (required for building):
   ```bash
   # Windows
   set EXPO_TOKEN=your_expo_token_here
   
   # Or add to Windows Environment Variables permanently
   ```
   Get your token from: https://expo.dev/accounts/[your-account]/settings/access-tokens

3. **Start the Central Server**:
   ```bash
   # Run the setup script
   server_setup.bat
   
   # Choose option 1: "Start Server (First Time Setup)"
   ```

4. **Set up External Access with ngrok**:
   - Install ngrok from: https://ngrok.com/
   - Run setup script and choose option 7: "Setup ngrok Tunnel"
   - Note your public URL (e.g., `https://abc123.ngrok.io`)

### Step 2: Build Lightweight Client

1. **Build the portable executable**:
   ```bash
   build_client.bat
   
   # Choose option 1: "Build Portable Executable"
   ```

2. **Distribute to POS computers**:
   - Copy `dist\MobileAppBuilder.exe` to each POS computer
   - No installation required!

### Step 3: Configure POS Computers

1. **On each POS computer**:
   - Double-click `MobileAppBuilder.exe`
   - Click "⚙️ Server Settings"
   - Enter your ngrok URL (e.g., `https://abc123.ngrok.io`)
   - Click "Save"

2. **Build apps as usual**:
   - Same familiar interface
   - Enter POS URL and app name
   - Click "📱 Build Android App"
   - Watch real-time progress
   - Download APK when complete

## 📁 File Structure

```
📁 Mobile App Builder/
├── 🏭 Central Server Files
│   ├── server_api.py           # Main API server
│   ├── Dockerfile              # Enhanced container
│   ├── docker-compose.yml      # Server orchestration  
│   ├── server_setup.bat        # Server management
│   └── configure_app.py        # App configuration
│
├── 📱 Client Files
│   ├── client_lightweight.py   # Lightweight client source
│   ├── build_client.bat        # Client builder
│   └── dist/
│       └── MobileAppBuilder.exe # Portable executable
│
├── 📄 App Files
│   ├── App.tsx                 # React Native app
│   ├── app.json               # Expo configuration
│   ├── package.json           # Dependencies
│   └── android/               # Android project
│
└── 📚 Documentation
    ├── README.md              # This file
    └── DOCKER_README.md       # Docker specifics
```

## 🔧 Management Commands

### Central Server Management

```bash
# Start server management
server_setup.bat

Options:
1. 🚀 Start Server (First Time Setup)  # Initial setup
2. ▶️  Start Server (Existing)         # Regular start  
3. ⏹️  Stop Server                     # Stop service
4. 🔄 Restart Server                   # Restart service
5. 📊 View Server Status               # Health check
6. 📜 View Server Logs                 # Debug logs
7. 🌐 Setup ngrok Tunnel               # External access
8. 🧹 Clean Up                         # Remove all
```

### Client Building

```bash
# Build client executable
build_client.bat

Options:
1. 🏗️  Build Portable Executable      # Standard build
2. 📦 Build with Icon and Metadata     # Advanced build
3. 🧪 Test Client Locally              # Local testing
4. 📋 Install Client Dependencies      # Setup deps
5. 🧹 Clean Build Files               # Cleanup
```

## 🌐 API Endpoints

The central server provides a REST API:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/status` | Server health check |
| `POST` | `/api/build` | Start new build |
| `GET` | `/api/build/{id}/status` | Build status |
| `GET` | `/api/build/{id}/logs` | Build logs |
| `WS` | `/api/build/{id}/logs/ws` | Real-time logs |
| `GET` | `/api/builds` | List all builds |

## 💡 Benefits of This System

### For POS Computers (Store Staff)
✅ **Zero Installation**: Just download and run .exe file  
✅ **Familiar Interface**: Same GUI they already know  
✅ **No Maintenance**: Nothing to configure or update  
✅ **Low Resources**: Only 15-20MB memory usage  
✅ **Works Offline**: Queues builds when disconnected  

### For You (Technical Management)
✅ **Centralized Control**: One server handles all locations  
✅ **Easy Updates**: Update server, all clients benefit  
✅ **Monitoring**: See all store activity in one place  
✅ **Cost Effective**: One server serves unlimited stores  
✅ **Scalable**: Add new stores instantly  

## 🔐 Security Considerations

- **Network Security**: Uses HTTPS via ngrok
- **Authentication**: Server-level access control
- **Token Management**: EAS tokens stored securely on server
- **Data Privacy**: No sensitive data stored on POS computers

## 🐛 Troubleshooting

### Common Issues

**"Server Status: ❌ Disconnected"**
- Check if central server is running
- Verify ngrok tunnel is active
- Test server URL in browser

**"Build failed: EAS authentication failed"**
- Check EXPO_TOKEN environment variable
- Verify token is valid and not expired
- Run `eas whoami` on server to test

**"Docker build failed"**
- Ensure Docker Desktop is running
- Check if ports 3000, 8081 are available
- Review Docker logs for specific errors

**Client won't start**
- Check if client_config.json exists
- Verify server URL format (include http/https)
- Run client from command line to see error messages

### Getting Help

1. **Check Server Logs**:
   ```bash
   server_setup.bat
   # Choose option 6: "View Server Logs"
   ```

2. **Test API Directly**:
   ```bash
   curl http://localhost:3000/api/status
   # or visit in browser
   ```

3. **Client Debug Mode**:
   ```bash
   python client_lightweight.py
   # Run client from source to see detailed errors
   ```

## 🚀 Deployment Scenarios

### Scenario 1: Local Network Only
- Server on office computer
- POS computers connect via local IP
- No internet required for building
- Perfect for single-location businesses

### Scenario 2: Multi-Location with ngrok
- Server on main office computer
- ngrok tunnel for external access
- All store locations connect remotely
- Ideal for multi-store businesses

### Scenario 3: Cloud Deployment
- Server on AWS/Azure/GCP
- Custom domain with SSL
- Enterprise-grade reliability
- Best for large-scale operations

## 📞 Support

If you need help with setup or encounter issues:

1. Run the troubleshooting commands above
2. Check the logs for specific error messages
3. Verify network connectivity between components
4. Test each component individually

## 🎯 Next Steps

After successful deployment:

1. **Monitor Usage**: Track build frequency and success rates
2. **Optimize Performance**: Adjust server resources as needed
3. **User Training**: Provide simple instructions to store staff
4. **Backup Strategy**: Regular backups of build configurations
5. **Update Process**: Plan for updating clients and server

---

**🎉 You now have a professional, scalable mobile app building system that works efficiently on resource-constrained POS computers!**