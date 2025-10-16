"""
Quick setup script for E-Commerce Product Recommender
Run this script to set up everything automatically
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - SUCCESS")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(e.stderr)
        return False

def main():
    print("\n" + "="*60)
    print("🚀 E-Commerce Product Recommender - Quick Setup")
    print("="*60)
    
    # Check Python version
    print(f"\n✓ Python version: {sys.version}")
    
    # Install dependencies
    if not run_command(
        "pip install -r requirements.txt",
        "Installing dependencies"
    ):
        print("\n⚠️  Failed to install dependencies. Please check the error above.")
        return
    
    # Create .env if it doesn't exist
    if not os.path.exists(".env"):
        print("\n📝 Creating .env file...")
        with open(".env", "w") as f:
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("DATABASE_URL=sqlite:///./ecommerce.db\n")
        print("✅ .env file created!")
        print("⚠️  Please add your OpenAI API key to the .env file")
    else:
        print("\n✓ .env file already exists")
    
    # Initialize database
    if run_command(
        "python database.py",
        "Initializing database and seeding mock data"
    ):
        print("\n✅ Database setup complete!")
    
    print("\n" + "="*60)
    print("🎉 Setup Complete!")
    print("="*60)
    print("\n📖 Next Steps:")
    print("   1. Add your OpenAI API key to .env (optional but recommended)")
    print("   2. Run: uvicorn main:app --reload")
    print("   3. Visit: http://localhost:8000/docs")
    print("   4. Try: http://localhost:8000/recommend/1")
    print("\n💡 Tip: The system works without OpenAI API, but explanations will be basic")
    print("\n🚀 Happy coding!\n")

if __name__ == "__main__":
    main()
