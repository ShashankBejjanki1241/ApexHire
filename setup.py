#!/usr/bin/env python3
"""
Setup script for ApexHire - AI Resume Screener
"""

import os
import subprocess
import sys

def run_command(command):
    """Run a command and return success status"""
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up ApexHire - AI Resume Screener")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install requirements
    print("\n📦 Installing dependencies...")
    if run_command("pip install -r requirements.txt"):
        print("✅ Dependencies installed successfully")
    else:
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Download spaCy model
    print("\n🧠 Downloading spaCy model...")
    if run_command("python -m spacy download en_core_web_sm"):
        print("✅ spaCy model downloaded successfully")
    else:
        print("⚠️  spaCy model download failed (may already be installed)")
    
    # Create necessary directories
    print("\n📁 Creating directories...")
    directories = [
        "data/resumes",
        "data/job_descriptions",
        "logs",
        "output"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}/")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Add your resume to data/resumes/")
    print("2. Add job descriptions to data/job_descriptions/")
    print("3. Run: python src/main_pipeline.py")
    print("4. Or run web interface: streamlit run app/main.py")

if __name__ == "__main__":
    main()
