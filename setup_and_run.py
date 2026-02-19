#!/usr/bin/env python3
"""
Quick Setup and Run Script for Carbon Deal Intelligence Dashboard
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def setup_virtual_environment():
    """Set up virtual environment if it doesn't exist"""
    venv_dir = "venv"
    
    if not os.path.exists(venv_dir):
        print("🔄 Creating virtual environment...")
        if not run_command(f"{sys.executable} -m venv {venv_dir}", "Virtual environment creation"):
            return False
    else:
        print("✅ Virtual environment already exists")
    
    # Determine activation script path
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
        pip_path = os.path.join(venv_dir, "Scripts", "pip")
        python_path = os.path.join(venv_dir, "Scripts", "python")
    else:  # Unix/macOS
        activate_script = os.path.join(venv_dir, "bin", "activate")
        pip_path = os.path.join(venv_dir, "bin", "pip")
        python_path = os.path.join(venv_dir, "bin", "python")
    
    return activate_script, pip_path, python_path

def install_dependencies(pip_path):
    """Install Python dependencies"""
    if not run_command(f"{pip_path} install -r requirements.txt", "Installing dependencies"):
        return False
    return True

def create_demo_data():
    """Create demo data for testing"""
    print("🔄 Creating demo data...")
    try:
        subprocess.run([sys.executable, "create_demo_data.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Demo data creation failed: {e}")
        return False

def main():
    print("🚀 Carbon Deal Intelligence Dashboard Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python():
        sys.exit(1)
    
    # Set up virtual environment
    try:
        activate_script, pip_path, python_path = setup_virtual_environment()
    except Exception as e:
        print(f"❌ Failed to set up virtual environment: {e}")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies(pip_path):
        sys.exit(1)
    
    # Create demo data
    if not create_demo_data():
        print("⚠️  Demo data creation failed, but continuing...")
    
    print("\n✅ Setup completed!")
    print("\n🌐 Starting dashboard...")
    print("   Dashboard will be available at: http://localhost:5000")
    print("   Press Ctrl+C to stop")
    print("-" * 50)
    
    # Start the dashboard using the virtual environment Python
    try:
        os.system(f"{python_path} run_dashboard.py")
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        
        # Fallback instructions
        print("\n📝 Manual start instructions:")
        print("1. Activate virtual environment:")
        if os.name == 'nt':
            print(f"   {activate_script}")
        else:
            print(f"   source {activate_script}")
        print("2. Run dashboard:")
        print("   python run_dashboard.py")

if __name__ == "__main__":
    main()