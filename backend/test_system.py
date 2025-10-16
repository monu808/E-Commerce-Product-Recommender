"""
Test script to verify the E-Commerce Recommender API
"""
import sys
import time
import subprocess

def test_imports():
    """Test if all required packages are installed"""
    print("\n🧪 Testing Package Imports...")
    print("-" * 50)
    
    required_packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("sqlalchemy", "SQLAlchemy"),
        ("openai", "OpenAI"),
        ("dotenv", "python-dotenv"),
        ("pydantic", "Pydantic")
    ]
    
    all_passed = True
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - NOT INSTALLED")
            all_passed = False
    
    return all_passed


def test_database():
    """Test if database is set up correctly"""
    print("\n🗄️  Testing Database Setup...")
    print("-" * 50)
    
    try:
        from database import engine, User, Product, Interaction
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = ['users', 'products', 'interactions']
        all_present = True
        
        for table in required_tables:
            if table in tables:
                print(f"✅ Table '{table}' exists")
            else:
                print(f"❌ Table '{table}' missing")
                all_present = False
        
        # Check data count
        from database import SessionLocal
        db = SessionLocal()
        
        user_count = db.query(User).count()
        product_count = db.query(Product).count()
        interaction_count = db.query(Interaction).count()
        
        print(f"\n📊 Database Statistics:")
        print(f"   Users: {user_count}")
        print(f"   Products: {product_count}")
        print(f"   Interactions: {interaction_count}")
        
        db.close()
        
        if user_count > 0 and product_count > 0:
            print("\n✅ Database is properly seeded!")
            return True
        else:
            print("\n⚠️  Database tables exist but no data found")
            return False
            
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        return False


def test_recommendation_logic():
    """Test the recommendation engine"""
    print("\n🧠 Testing Recommendation Logic...")
    print("-" * 50)
    
    try:
        from database import SessionLocal
        from recommendation import get_recommendations, get_user_profile
        
        db = SessionLocal()
        
        # Test for user 1
        recommended_products, user_profile = get_recommendations(db, user_id=1, top_n=3)
        
        print(f"✅ Recommendations generated for User 1")
        print(f"   Found {len(recommended_products)} recommendations")
        
        if recommended_products:
            print(f"   Top recommendation: {recommended_products[0].name}")
        
        db.close()
        return len(recommended_products) > 0
        
    except Exception as e:
        print(f"❌ Recommendation error: {str(e)}")
        return False


def test_api_endpoints():
    """Test if the API endpoints work (requires server to be running)"""
    print("\n🌐 Testing API Endpoints (Server must be running)...")
    print("-" * 50)
    
    try:
        import requests
        
        base_url = "http://localhost:8000"
        
        # Test root endpoint
        try:
            response = requests.get(base_url, timeout=2)
            if response.status_code == 200:
                print("✅ Root endpoint (/) working")
            else:
                print(f"⚠️  Root endpoint returned status {response.status_code}")
        except requests.exceptions.RequestException:
            print("⚠️  Server not running. Start with: uvicorn main:app --reload")
            return False
        
        # Test recommendation endpoint
        try:
            response = requests.get(f"{base_url}/recommend/1", timeout=2)
            if response.status_code == 200:
                data = response.json()
                print("✅ Recommendation endpoint working")
                print(f"   User: {data.get('user_name')}")
                print(f"   Products: {len(data.get('recommended_products', []))}")
            else:
                print(f"⚠️  Recommendation endpoint returned status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error testing recommendation endpoint: {str(e)}")
            return False
        
        return True
        
    except ImportError:
        print("⚠️  'requests' package not installed. Skipping API tests.")
        print("   Install with: pip install requests")
        return None


def main():
    print("\n" + "="*60)
    print("🧪 E-Commerce Recommender - System Test")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Package Imports", test_imports()))
    results.append(("Database Setup", test_database()))
    results.append(("Recommendation Logic", test_recommendation_logic()))
    
    api_result = test_api_endpoints()
    if api_result is not None:
        results.append(("API Endpoints", api_result))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! Your system is ready to use.")
        print("\n📖 Quick Start:")
        print("   1. Run: uvicorn main:app --reload")
        print("   2. Visit: http://localhost:8000/docs")
        print("   3. Try: http://localhost:8000/recommend/1")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print()


if __name__ == "__main__":
    main()
