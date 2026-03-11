#!/usr/bin/env python3
"""
Teste rápido para verificar se a ATENA pode executar
"""

import sys
import importlib

def test_module(module_name):
    """Testa se um módulo pode ser importado"""
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, "__version__", "desconhecida")
        print(f"  ✅ {module_name:<12} {version}")
        return True
    except ImportError as e:
        print(f"  ❌ {module_name:<12} {e}")
        return False

def main():
    print("🧪 ATENA - TESTE RÁPIDO DE MÓDULOS")
    print("=" * 50)
    
    # Módulos essenciais
    essential = [
        "aiosqlite",
        "aiohttp",
        "numpy",
        "pandas",
        "transformers",
        "torch",
        "chromadb",
        "faiss",
        "networkx"
    ]
    
    print("\n📦 Módulos essenciais:")
    results = []
    for mod in essential:
        results.append(test_module(mod))
    
    # Módulos opcionais
    optional = [
        "matplotlib",
        "seaborn",
        "sklearn",
        "dotenv",
        "tqdm",
        "colorama",
        "requests",
        "yaml"
    ]
    
    print("\n📦 Módulos opcionais:")
    for mod in optional:
        test_module(mod)
    
    # Resultado final
    if all(results):
        print("\n✨ TODOS OS MÓDULOS ESSENCIAIS ESTÃO OK!")
        return 0
    else:
        print("\n❌ Alguns módulos essenciais estão faltando")
        return 1

if __name__ == "__main__":
    sys.exit(main())
