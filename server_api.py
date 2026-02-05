#!/usr/bin/env python3
"""
Central Server API for Mobile App Builder
Handles build requests from lightweight clients
"""

import os
import json
import uuid
import asyncio
import threading
import subprocess
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="Mobile App Builder Server", version="1.0.0")

# Enable CORS for client connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
PROJECT_DIR = "/app"
BUILDS_DIR = "/app/builds"
LOGS_DIR = "/app/logs"
UPLOADS_DIR = "/app/uploads"

# Ensure directories exist
os.makedirs(BUILDS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

# In-memory storage for build status and logs
builds = {}
active_websockets = {}

class BuildRequest(BaseModel):
    app_url: str
    app_name: str
    client_id: str = None

class BuildStatus(BaseModel):
    id: str
    status: str  # pending, building, success, error
    progress: int
    message: str
    created_at: str
    completed_at: str = None
    apk_url: str = None

class LogMessage(BaseModel):
    timestamp: str
    level: str
    message: str

# Helper functions
def generate_build_id():
    return str(uuid.uuid4())[:8]

def get_timestamp():
    return datetime.now().isoformat()

def log_message(build_id: str, level: str, message: str):
    """Add a log message and broadcast to websockets"""
    log_entry = LogMessage(
        timestamp=get_timestamp(),
        level=level,
        message=message
    )
    
    if build_id not in builds:
        builds[build_id] = {
            "logs": [],
            "status": "pending",
            "progress": 0
        }
    
    builds[build_id]["logs"].append(log_entry.dict())
    
    # Broadcast to connected websockets
    if build_id in active_websockets:
        for websocket in active_websockets[build_id]:
            try:
                asyncio.create_task(websocket.send_json(log_entry.dict()))
            except:
                pass

def update_app_config(app_url: str, app_name: str):
    """Update App.tsx and app.json with new configuration"""
    try:
        # Update App.tsx
        app_tsx_path = os.path.join(PROJECT_DIR, "App.tsx")
        with open(app_tsx_path, 'r') as f:
            content = f.read()
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'APP_URL' in line and '=' in line:
                lines[i] = f"const APP_URL = '{app_url}';"
                break
        
        with open(app_tsx_path, 'w') as f:
            f.write('\n'.join(lines))
        
        # Update app.json
        app_json_path = os.path.join(PROJECT_DIR, "app.json")
        with open(app_json_path, 'r') as f:
            config = json.load(f)
        
        config['expo']['name'] = app_name
        if 'android' in config['expo']:
            config['expo']['android']['label'] = app_name
        
        with open(app_json_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error updating config: {e}")
        return False

async def run_build_process(build_id: str, app_url: str, app_name: str):
    """Run the EAS build process asynchronously"""
    try:
        builds[build_id]["status"] = "building"
        builds[build_id]["progress"] = 10
        
        log_message(build_id, "info", f"Starting build for {app_name}")
        log_message(build_id, "info", f"Target URL: {app_url}")
        
        # Update configuration
        log_message(build_id, "info", "Updating app configuration...")
        if not update_app_config(app_url, app_name):
            raise Exception("Failed to update app configuration")
        
        builds[build_id]["progress"] = 30
        log_message(build_id, "info", "Configuration updated successfully")
        
        # Check EAS authentication
        log_message(build_id, "info", "Checking EAS authentication...")
        result = subprocess.run(["eas", "whoami"], cwd=PROJECT_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception("EAS authentication failed")
        
        builds[build_id]["progress"] = 50
        log_message(build_id, "info", "EAS authentication verified")
        
        # Start the build
        log_message(build_id, "info", "Starting EAS build...")
        build_process = subprocess.Popen(
            ["eas", "build", "--platform", "android", "--profile", "production", "--non-interactive"],
            cwd=PROJECT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            universal_newlines=True
        )
        
        builds[build_id]["progress"] = 70
        
        # Stream build output
        for line in iter(build_process.stdout.readline, ''):
            if line:
                log_message(build_id, "info", line.strip())
                
                # Update progress based on build output
                if "Build completed" in line:
                    builds[build_id]["progress"] = 90
                elif "Download URL" in line or "APK" in line:
                    # Extract APK URL if available
                    if "https://" in line:
                        apk_url = line.split("https://")[1].split()[0]
                        builds[build_id]["apk_url"] = "https://" + apk_url
        
        build_process.wait()
        
        if build_process.returncode == 0:
            builds[build_id]["status"] = "success"
            builds[build_id]["progress"] = 100
            builds[build_id]["completed_at"] = get_timestamp()
            log_message(build_id, "success", "Build completed successfully!")
        else:
            raise Exception(f"Build failed with exit code {build_process.returncode}")
            
    except Exception as e:
        builds[build_id]["status"] = "error"
        builds[build_id]["completed_at"] = get_timestamp()
        builds[build_id]["message"] = str(e)
        log_message(build_id, "error", f"Build failed: {str(e)}")

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Mobile App Builder Server", "version": "1.0.0"}

@app.get("/api/status")
async def server_status():
    return {
        "status": "running",
        "timestamp": get_timestamp(),
        "active_builds": len([b for b in builds.values() if b.get("status") == "building"]),
        "total_builds": len(builds)
    }

@app.post("/api/build")
async def start_build(request: BuildRequest):
    build_id = generate_build_id()
    
    builds[build_id] = {
        "id": build_id,
        "status": "pending",
        "progress": 0,
        "message": "Build queued",
        "created_at": get_timestamp(),
        "app_url": request.app_url,
        "app_name": request.app_name,
        "logs": []
    }
    
    # Start build process in background
    threading.Thread(
        target=asyncio.run,
        args=(run_build_process(build_id, request.app_url, request.app_name),)
    ).start()
    
    return {"build_id": build_id, "status": "queued"}

@app.get("/api/build/{build_id}/status")
async def get_build_status(build_id: str):
    if build_id not in builds:
        raise HTTPException(status_code=404, detail="Build not found")
    
    return builds[build_id]

@app.get("/api/build/{build_id}/logs")
async def get_build_logs(build_id: str):
    if build_id not in builds:
        raise HTTPException(status_code=404, detail="Build not found")
    
    return builds[build_id].get("logs", [])

@app.get("/api/build/{build_id}/download")
async def download_apk(build_id: str):
    if build_id not in builds:
        raise HTTPException(status_code=404, detail="Build not found")
    
    build_info = builds[build_id]
    if build_info["status"] != "success":
        raise HTTPException(status_code=400, detail="Build not completed or failed")
    
    apk_url = build_info.get("apk_url")
    if not apk_url:
        raise HTTPException(status_code=404, detail="APK download URL not available")
    
    return {"download_url": apk_url}

@app.websocket("/api/build/{build_id}/logs/ws")
async def websocket_logs(websocket: WebSocket, build_id: str):
    await websocket.accept()
    
    # Add websocket to active connections
    if build_id not in active_websockets:
        active_websockets[build_id] = []
    active_websockets[build_id].append(websocket)
    
    try:
        # Send existing logs
        if build_id in builds:
            for log_entry in builds[build_id].get("logs", []):
                await websocket.send_json(log_entry)
        
        # Keep connection alive
        while True:
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        # Remove websocket from active connections
        if build_id in active_websockets:
            active_websockets[build_id].remove(websocket)
            if not active_websockets[build_id]:
                del active_websockets[build_id]

@app.get("/api/builds")
async def list_builds():
    return {"builds": list(builds.values())}

if __name__ == "__main__":
    print("🚀 Starting Mobile App Builder Server...")
    print(f"📁 Project Directory: {PROJECT_DIR}")
    print(f"📦 Builds Directory: {BUILDS_DIR}")
    print(f"📜 Logs Directory: {LOGS_DIR}")
    
    uvicorn.run(app, host="0.0.0.0", port=3000, log_level="info")