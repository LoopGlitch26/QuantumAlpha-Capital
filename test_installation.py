#!/usr/bin/env python3
"""
Test script to verify all dependencies are installed correctly
"""

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        # Core trading dependencies
        import hyperliquid
        print("✅ hyperliquid-python-sdk")
        
        import web3
        print("✅ web3")
        
        import aiohttp
        print("✅ aiohttp")
        
        import openai
        print("✅ openai")
        
        import requests
        print("✅ requests")
        
        # GUI dependencies
        import nicegui
        print("✅ nicegui")
        
        import plotly
        print("✅ plotly")
        
        import pandas
        print("✅ pandas")
        
        try:
            import pywebview
            print("✅ pywebview")
        except ImportError:
            print("⚠️  pywebview (optional - for native desktop mode)")
        
        # Database
        import sqlalchemy
        print("✅ sqlalchemy")
        
        # Utilities
        from dotenv import load_dotenv
        print("✅ python-dotenv")
        
        print("\n🎉 All dependencies imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from src.backend.config_loader import CONFIG
        print("✅ Configuration loaded")
        
        # Check if .env file exists
        import os
        if os.path.exists('.env'):
            print("✅ .env file found")
        else:
            print("⚠️  .env file not found - you'll need to configure API keys")
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_database():
    """Test database initialization"""
    print("\nTesting database...")
    
    try:
        from src.database.db_manager import DatabaseManager
        
        # Test database creation
        db = DatabaseManager()
        print("✅ Database manager initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == "__main__":
    print("⚡ Testing QuantumAlpha Capital Platform Installation\n")
    
    success = True
    success &= test_imports()
    success &= test_config()
    success &= test_database()
    
    if success:
        print("\n🎉 Installation test completed successfully!")
        print("\nNext steps:")
        print("1. Edit the .env file with your API keys")
        print("2. Run: python3 main.py")
        print("3. Open http://127.0.0.1:8080 in your browser")
    else:
        print("\n❌ Installation test failed. Please check the errors above.")