#!/usr/bin/env python3
"""
Comprehensive test script for the LAQ RAG branch.
Tests all components without requiring Ollama or full dependencies.
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def test_imports():
    """Test that all modules can be imported."""
    print("=" * 60)
    print("TEST 1: Module Imports")
    print("=" * 60)

    tests = []

    # Test core modules
    try:
        from app.services.config import Config
        tests.append(("✅", "Config"))
    except Exception as e:
        tests.append(("❌", f"Config: {e}"))

    try:
        from app.services.database import LAQDatabase
        tests.append(("✅", "LAQDatabase"))
    except Exception as e:
        tests.append(("❌", f"LAQDatabase: {e}"))

    try:
        from app.services.embeddings import EmbeddingService
        tests.append(("✅", "EmbeddingService"))
    except Exception as e:
        tests.append(("❌", f"EmbeddingService: {e}"))

    try:
        from app.services.rag import RAGService
        tests.append(("✅", "RAGService"))
    except Exception as e:
        tests.append(("❌", f"RAGService: {e}"))

    try:
        from app.core.dependencies import get_config, get_rag_service
        tests.append(("✅", "Dependencies"))
    except Exception as e:
        tests.append(("❌", f"Dependencies: {e}"))

    try:
        from app.api.endpoints import search, chat, upload, database
        tests.append(("✅", "API Endpoints"))
    except Exception as e:
        tests.append(("❌", f"API Endpoints: {e}"))

    try:
        from app.main import app
        tests.append(("✅", "FastAPI App"))
    except Exception as e:
        tests.append(("❌", f"FastAPI App: {e}"))

    for status, msg in tests:
        print(f"{status} {msg}")

    failures = [t for t in tests if t[0] == "❌"]
    return len(failures) == 0


def test_file_structure():
    """Test that all required files exist."""
    print("\n" + "=" * 60)
    print("TEST 2: File Structure")
    print("=" * 60)

    backend = Path(__file__).parent / "backend"
    required_files = [
        "app/main.py",
        "app/__init__.py",
        "app/core/dependencies.py",
        "app/core/__init__.py",
        "app/services/config.py",
        "app/services/database.py",
        "app/services/embeddings.py",
        "app/services/rag.py",
        "app/services/pdf_processor.py",
        "app/services/__init__.py",
        "app/api/endpoints/search.py",
        "app/api/endpoints/chat.py",
        "app/api/endpoints/upload.py",
        "app/api/endpoints/database.py",
        "app/models/schemas.py",
        "requirements.txt",
    ]

    all_exist = True
    for file_path in required_files:
        full_path = backend / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False

    return all_exist


def test_rag_service_structure():
    """Test RAG service has required methods."""
    print("\n" + "=" * 60)
    print("TEST 3: RAG Service Structure")
    print("=" * 60)

    try:
        from app.services.rag import RAGService

        required_methods = [
            'search',
            'chat',
            '_rerank_results',
            '_build_context',
            '_build_chat_prompt',
            'get_match_quality_stats'
        ]

        all_methods = True
        for method in required_methods:
            if hasattr(RAGService, method):
                print(f"✅ RAGService.{method}")
            else:
                print(f"❌ RAGService.{method} - MISSING")
                all_methods = False

        # Check method signatures
        import inspect
        search_sig = inspect.signature(RAGService.search)
        params = list(search_sig.parameters.keys())

        print(f"\n📋 search() parameters: {params}")

        # Check for V3 features
        if 'use_reranking' in params:
            print("✅ Has use_reranking parameter (V3 feature)")
        else:
            print("❌ Missing use_reranking parameter")
            all_methods = False

        if 'use_query_formatting' in params:
            print("✅ Has use_query_formatting parameter (V3 feature)")
        else:
            print("❌ Missing use_query_formatting parameter")
            all_methods = False

        return all_methods

    except Exception as e:
        print(f"❌ Error testing RAG service: {e}")
        return False


def test_dependency_injection():
    """Test dependency injection setup."""
    print("\n" + "=" * 60)
    print("TEST 4: Dependency Injection")
    print("=" * 60)

    try:
        from app.core.dependencies import get_config, get_database, get_embedding_service, get_rag_service

        print("✅ get_config defined")
        print("✅ get_database defined")
        print("✅ get_embedding_service defined")
        print("✅ get_rag_service defined")

        # Check if get_config is cached
        import inspect
        if hasattr(get_config, '__wrapped__'):
            print("✅ get_config uses @lru_cache")
        else:
            print("🟡 get_config might not be cached")

        return True

    except Exception as e:
        print(f"❌ Error testing dependency injection: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_endpoints():
    """Test API endpoint structure."""
    print("\n" + "=" * 60)
    print("TEST 5: API Endpoints")
    print("=" * 60)

    try:
        from app.api.endpoints import search, chat

        # Check search endpoint
        if hasattr(search, 'router'):
            print("✅ search.router exists")
        else:
            print("❌ search.router missing")
            return False

        # Check chat endpoint
        if hasattr(chat, 'router'):
            print("✅ chat.router exists")
        else:
            print("❌ chat.router missing")
            return False

        # Check if endpoints use dependency injection
        import inspect
        search_func = None
        for name, obj in inspect.getmembers(search):
            if name == 'search_laqs':
                search_func = obj
                break

        if search_func:
            sig = inspect.signature(search_func)
            params = list(sig.parameters.keys())
            print(f"📋 search_laqs parameters: {params}")

            if 'rag_service' in params:
                print("✅ search endpoint uses dependency injection")
            else:
                print("❌ search endpoint doesn't use dependency injection")
                return False

        return True

    except Exception as e:
        print(f"❌ Error testing API endpoints: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_main_app():
    """Test main FastAPI app."""
    print("\n" + "=" * 60)
    print("TEST 6: FastAPI Application")
    print("=" * 60)

    try:
        from app.main import app

        print(f"✅ App created: {app.title}")
        print(f"✅ Version: {app.version}")

        # Check routes
        routes = [route.path for route in app.routes]
        print(f"\n📋 Registered routes ({len(routes)}):")

        required_routes = [
            '/',
            '/health',
            '/api/search/',
            '/api/chat/',
            '/api/upload/',
            '/api/database/info'
        ]

        all_routes_exist = True
        for route in required_routes:
            if route in routes:
                print(f"  ✅ {route}")
            else:
                print(f"  ❌ {route} - MISSING")
                all_routes_exist = False

        return all_routes_exist

    except Exception as e:
        print(f"❌ Error testing FastAPI app: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "🧪 " * 30)
    print(" " * 20 + "BRANCH TEST SUITE")
    print("🧪 " * 30 + "\n")

    results = {
        "File Structure": test_file_structure(),
        "Module Imports": test_imports(),
        "RAG Service": test_rag_service_structure(),
        "Dependency Injection": test_dependency_injection(),
        "API Endpoints": test_api_endpoints(),
        "FastAPI App": test_main_app(),
    }

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    print("\n" + "=" * 60)

    passed = sum(results.values())
    total = len(results)

    print(f"\nTests Passed: {passed}/{total}")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Branch is ready.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. See details above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
