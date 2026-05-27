#!/usr/bin/env python3
"""Development server runner for both backend and frontend."""
import subprocess
import sys
import os
import time
from pathlib import Path


def run_backend():
    """Start backend server."""
    print("\n🚀 Starting backend server...")
    backend_dir = Path(__file__).parent.parent / "backend"
    
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    
    proc = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=backend_dir,
        env=env,
    )
    return proc


def run_frontend():
    """Start frontend development server."""
    print("\n⚛️  Starting frontend server...")
    frontend_dir = Path(__file__).parent.parent / "frontend"
    
    # Wait for backend to start
    time.sleep(3)
    
    proc = subprocess.Popen(
        ["npm", "start"],
        cwd=frontend_dir,
    )
    return proc


def main():
    """Start both servers."""
    print("="*50)
    print("WiFi Indoor Positioning - Development Server")
    print("="*50)
    
    try:
        backend_proc = run_backend()
        frontend_proc = run_frontend()
        
        print("\n✅ Both servers started!")
        print("\n🌐 Dashboard: http://localhost:3000")
        print("📡 API: http://localhost:8000/api")
        print("\nPress Ctrl+C to stop\n")
        
        # Wait for processes
        backend_proc.wait()
        frontend_proc.wait()
    
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        backend_proc.terminate()
        frontend_proc.terminate()
        backend_proc.wait()
        frontend_proc.wait()
        print("✅ Servers stopped")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
