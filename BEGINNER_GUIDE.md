# 🎓 Beginner's Complete Guide
**Step-by-Step Instructions for Mobile App Builder Setup**

---

## **Phase 1: Check if Your Computer is Ready (5 minutes)**

### Step 1.1: Run the System Check
1. **Open your file manager** (Windows Explorer)
2. **Navigate to your project folder**:
   ```
   C:\Users\Bernard Sahagun\Downloads\PSC-MOBILE WRAPPER\WebAppWrapperExpo
   ```
3. **Double-click on `check_requirements.bat`**
4. **Read the results carefully**

### Step 1.2: Fix Any Red ❌ Marks

**If you see "Docker Desktop not found":**
1. Go to https://www.docker.com/products/docker-desktop
2. Click "Download for Windows"
3. Run the installer
4. Restart your computer
5. Start Docker Desktop from Start menu
6. Run `check_requirements.bat` again

**If you see "Python not found":**
1. Go to https://www.python.org/downloads/
2. Download the latest Python
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Restart your computer
5. Run `check_requirements.bat` again

**✅ When you see only green marks, continue to Phase 2**

---

## **Phase 2: Get Your Expo Account Ready (10 minutes)**

### Step 2.1: Create Expo Account (if you don't have one)
1. Go to https://expo.dev/
2. Click "Sign up"
3. Create your account
4. Verify your email

### Step 2.2: Get Your EXPO_TOKEN
1. **Log into Expo**: https://expo.dev/
2. **Go to Settings**: Click your profile → Settings
3. **Access Tokens**: Click "Access tokens" in left menu
4. **Create Token**: Click "Create token" button
5. **Name it**: Type "Mobile App Builder"
6. **Copy the token**: It looks like `IxQ90f96kL7P5gYL8TnSHD41tyY2W1T1eoR1v065`

### Step 2.3: Set the EXPO_TOKEN on Windows
1. **Press Windows key + R**
2. **Type**: `sysdm.cpl` and press Enter
3. **Click "Advanced" tab**
4. **Click "Environment Variables"**
5. **Under "User variables", click "New"**
6. **Variable name**: `EXPO_TOKEN`
7. **Variable value**: Paste your copied token
8. **Click OK, OK, OK**
9. **Close all command prompts and restart them**

**💡 Alternative Quick Method:**
1. **Open Command Prompt**
2. **Type**: `setx EXPO_TOKEN "your_token_here"`
3. **Close and reopen Command Prompt**

---

## **Phase 3: Start Your Central Server (15 minutes)**

### Step 3.1: Open Command Prompt in Project Folder
1. **Open File Explorer**
2. **Navigate to your project folder**
3. **Click in the address bar** where it shows the path
4. **Type**: `cmd` and press Enter
5. **You should see**: `C:\Users\Bernard Sahagun\Downloads\PSC-MOBILE WRAPPER\WebAppWrapperExpo>`

### Step 3.2: Start the Server Setup
1. **Type**: `server_setup.bat` and press Enter
2. **You'll see a menu like this**:
   ```
   🏭 Mobile App Builder - Central Server Setup
   ============================================
   
   🔧 Central Server Management:
   
   1. 🚀 Start Server (First Time Setup)
   2. ▶️  Start Server (Existing)  
   3. ⏹️  Stop Server
   ... etc
   ```

3. **Type**: `1` and press Enter (First Time Setup)

### Step 3.3: Wait for Setup to Complete
**You'll see messages like:**
```
📦 Building Docker image...
▶️  Starting server...
✅ Server started successfully!
🌐 Server is running on:
  Local:    http://localhost:3000
  Network:  http://[your-computer-ip]:3000
```

**This might take 5-10 minutes the first time** - Docker is downloading and building everything.

### Step 3.4: Test Your Server
1. **Open your web browser**
2. **Go to**: `http://localhost:3000`
3. **You should see**: `{"message":"Mobile App Builder Server","version":"1.0.0"}`
4. **If you see this, your server is working!** ✅

---

## **Phase 4: Set Up External Access (10 minutes)**

### Step 4.1: Install ngrok
1. **Go to**: https://ngrok.com/
2. **Sign up** for free account
3. **Download ngrok** for Windows
4. **Extract** the `ngrok.exe` file
5. **Move `ngrok.exe`** to your project folder (next to server_setup.bat)

### Step 4.2: Set Up ngrok
1. **From ngrok website**, copy your **authtoken** (looks like `1a2B3c4D5e6F...`)
2. **Open Command Prompt** in project folder
3. **Type**: `ngrok authtoken your_token_here` (paste your actual token)
4. **Press Enter**

### Step 4.3: Start ngrok Tunnel
1. **Run**: `server_setup.bat` again
2. **Choose**: `7` (Setup ngrok Tunnel)
3. **A new window opens** showing something like:
   ```
   ngrok by @inconshreveable
   
   Web Interface                 http://127.0.0.1:4040
   Forwarding                    https://abc123.ngrok.io -> http://localhost:3000
   ```
4. **Copy the https URL** (like `https://abc123.ngrok.io`)
5. **Keep this window open** - closing it stops the tunnel

### Step 4.4: Test External Access
1. **Open browser**
2. **Visit your ngrok URL**: `https://abc123.ngrok.io`
3. **You should see**: `{"message":"Mobile App Builder Server","version":"1.0.0"}`
4. **If yes, external access is working!** ✅

---

## **Phase 5: Build the Client for POS Computers (5 minutes)**

### Step 5.1: Build the Portable Executable
1. **Open Command Prompt** in project folder
2. **Run**: `build_client.bat`
3. **Choose**: `1` (Build Portable Executable)
4. **Wait** - this installs dependencies and builds the .exe file

### Step 5.2: Find Your Built Client
1. **Look in the `dist` folder**
2. **You'll find**: `MobileAppBuilder.exe`
3. **This is your portable client** - about 15-20MB

### Step 5.3: Test the Client on Your Computer
1. **Double-click**: `MobileAppBuilder.exe` in the dist folder
2. **The familiar GUI opens**
3. **Click**: ⚙️ Server Settings
4. **Enter**: Your ngrok URL (like `https://abc123.ngrok.io`)
5. **Click**: Save
6. **You should see**: "Server Status: ✅ Connected"

---

## **Phase 6: Test the Complete System (10 minutes)**

### Step 6.1: Test Building an App
1. **In the client**, enter:
   - **App URL**: `http://192.168.1.226/NEWKIOSK` (or your POS URL)
   - **App Name**: `Test POS App`
2. **Click**: 📱 Build Android App
3. **Watch the logs** - you should see real-time progress

### Step 6.2: What You Should See
```
🚀 Starting Android app build...
📱 App Name: Test POS App  
🌐 App URL: http://192.168.1.226/NEWKIOSK
📡 Sending build request to server...
✅ Build request accepted. Build ID: abc12345
Starting build for Test POS App
Target URL: http://192.168.1.226/NEWKIOSK
Updating app configuration...
Configuration updated successfully
... (more build logs)
```

### Step 6.3: If Build is Successful
- **You'll see**: "🎉 Build completed successfully!"
- **A download link appears** for the APK file
- **Click "Yes"** to open the download link
- **The APK downloads** from Expo's servers

---

## **Phase 7: Deploy to POS Computers (Per Store)**

### For Each POS Computer:

1. **Copy** `MobileAppBuilder.exe` to a USB drive
2. **Go to the POS computer**
3. **Copy** `MobileAppBuilder.exe` to Desktop
4. **Double-click** to run it
5. **Click** ⚙️ Server Settings
6. **Enter** your ngrok URL: `https://abc123.ngrok.io`
7. **Click** Save
8. **Check**: "Server Status: ✅ Connected"
9. **Now they can build apps** just like before!

---

## **🚨 Common Problems & Solutions**

### "Docker build failed"
- **Make sure** Docker Desktop is running
- **Restart** Docker Desktop
- **Try again** - sometimes it takes 2-3 tries

### "Server Status: ❌ Disconnected" 
- **Check** if your server is running (`server_setup.bat` → option 5)
- **Check** if ngrok tunnel is running
- **Test** the URL in your browser first

### "EAS authentication failed"
- **Double-check** your EXPO_TOKEN is set correctly
- **Environment variable** might need computer restart
- **Try** setting it again: `setx EXPO_TOKEN "your_token"`

### Client won't start
- **Make sure** Python is installed with "Add to PATH"
- **Run from** Command Prompt to see error messages
- **Antivirus** might be blocking it - add exception

---

## **📞 Getting Help**

If something doesn't work:

1. **Read the error message carefully**
2. **Check** which Phase it fails at
3. **Look in** the Common Problems section above
4. **Try** running `check_requirements.bat` again
5. **Check** server logs: `server_setup.bat` → option 6

---

## **🎉 Success Checklist**

✅ Docker Desktop running  
✅ EXPO_TOKEN set correctly  
✅ Server starts without errors  
✅ ngrok tunnel working  
✅ Client builds successfully  
✅ Client connects to server  
✅ Test build completes  
✅ POS computers can connect  

**When you have all ✅ marks, you're ready for production!**

---

**🎓 Congratulations! You've successfully set up a professional mobile app building system!**