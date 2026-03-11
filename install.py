#!/usr/bin/env python3
"""
Script de instalação automática para a ATENA
Versão robusta com tratamento de erros e verificação de compatibilidade
"""

import subprocess
import sys
import platform
import os
from pathlib import Path
import json
from datetime import datetime

def print_header(text):
    print("\n" + "="*60)
    print(f"🔧 {text}")
    print("="*60)

def print_step(text):
    print(f"  ➡️  {text}")

def check_python_version():
    """Verifica versão do Python"""
    version = sys.version_info
    print_step(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("  ✅ Versão compatível")
        return True
    else:
        print("  ❌ Versão incompatível (necessário Python 3.8+)")
        return False

def install_dependencies_batch(dependencies, pip_args=None):
    """Instala dependências em lote"""
    if pip_args is None:
        pip_args = []
    
    cmd = [sys.executable, "-m", "pip", "install"] + pip_args + dependencies
    
    try:
        subprocess.run(cmd, check=True, capture_output=False)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Erro instalando lote: {e}")
        return False

def install_dependencies_individual(dependencies):
    """Instala dependências individualmente (fallback)"""
    sucessos = 0
    falhas = 0
    
    for dep in dependencies:
        print(f"    Instalando {dep}...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", dep],
                check=True,
                capture_output=True
            )
            print(f"    ✅ {dep}")
            sucessos += 1
        except subprocess.CalledProcessError:
            print(f"    ❌ {dep} (falhou)")
            falhas += 1
    
    return sucessos, falhas

def install_dependencies():
    """Instala todas as dependências necessárias"""
    
    print_header("ATENA - INSTALAÇÃO AUTOMÁTICA")
    
    # Detectar ambiente
    sistema = platform.system()
    print_step(f"Sistema: {sistema}")
    
    if not check_python_version():
        sys.exit(1)
    
    # Atualizar pip e ferramentas básicas
    print_step("Atualizando ferramentas básicas...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"],
        check=False
    )
    
    # Dependências por categoria
    categorias = {
        "Core": [
            "aiosqlite==0.19.0",
            "aiohttp==3.9.5",
            "numpy==1.24.3",
            "pandas==2.0.3",
            "python-dateutil==2.8.2"
        ],
        "Machine Learning": [
            "transformers==4.35.2",
            "torch==2.1.2",
            "sentence-transformers==2.2.2",
            "scikit-learn==1.3.2"
        ],
        "Vector DB": [
            "chromadb==0.4.24",
            "faiss-cpu==1.7.4"
        ],
        "Visualização": [
            "networkx==3.1",
            "matplotlib==3.7.5",
            "seaborn==0.13.0"
        ],
        "Utilitários": [
            "python-dotenv==1.0.0",
            "tqdm==4.66.1",
            "colorama==0.4.6",
            "requests==2.31.0",
            "pyyaml==6.0.1"
        ],
        "Qualidade de Código (opcional)": [
            "black==23.12.1",
            "autopep8==2.0.4",
            "pylint==3.0.3"
        ],
        "Testes (opcional)": [
            "pytest==7.4.4",
            "pytest-asyncio==0.21.1",
            "pytest-cov==4.1.0"
        ],
        "Serialização": [
            "orjson==3.9.15",
            "msgpack==1.0.7",
            "cloudpickle==3.0.0"
        ],
        "Monitoramento": [
            "prometheus-client==0.19.0",
            "structlog==23.3.0"
        ],
        "Type Hints": [
            "typing-extensions==4.9.0",
            "pydantic==2.5.3"
        ]
    }
    
    total_sucesso = 0
    total_falhas = 0
    
    for categoria, deps in categorias.items():
        print(f"\n📦 Instalando: {categoria}")
        
        # Tentar instalar em lote
        if not install_dependencies_batch(deps, ["--no-cache-dir"]):
            print(f"  ⚠️ Falha no lote, tentando individualmente...")
            sucessos, falhas = install_dependencies_individual(deps)
            total_sucesso += sucessos
            total_falhas += falhas
    
    # Criar diretórios necessários
    print("\n📁 Criando diretórios...")
    dirs = [
        "data",
        "backups",
        "exports",
        "logs",
        "chromadb_data",
        "faiss_index",
        "models",
        "cache"
    ]
    
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"  ✅ {dir_name}")
    
    # Criar arquivo de configuração
    print("\n⚙️  Criando configuração inicial...")
    config = {
        "versao": "22.0",
        "instalacao": datetime.now().isoformat(),
        "sistema": sistema,
        "python": f"{sys.version_info.major}.{sys.version_info.minor}",
        "diretorios": dirs
    }
    
    with open("data/config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"\n📊 Resumo da instalação:")
    print(f"  ✅ Sucessos: {total_sucesso}")
    print(f"  ❌ Falhas: {total_falhas}")
    
    if total_falhas == 0:
        print("\n✨ INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        print("\n🚀 Execute a ATENA com: python main.py")
    else:
        print("\n⚠️ Instalação concluída com algumas falhas.")
        print("   Algumas funcionalidades podem não estar disponíveis.")

def verificar_instalacao():
    """Verifica se todas as dependências estão instaladas"""
    
    print_header("VERIFICANDO INSTALAÇÃO")
    
    modulos_essenciais = [
        ("aiosqlite", "aiosqlite"),
        ("aiohttp", "aiohttp"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("transformers", "transformers"),
        ("torch", "torch"),
        ("sentence_transformers", "sentence_transformers"),
        ("sklearn", "scikit-learn"),
        ("chromadb", "chromadb"),
        ("faiss", "faiss"),
        ("networkx", "networkx"),
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn")
    ]
    
    modulos_opcionais = [
        ("black", "black"),
        ("pylint", "pylint"),
        ("pytest", "pytest"),
        ("orjson", "orjson"),
        ("msgpack", "msgpack"),
        ("prometheus_client", "prometheus-client"),
        ("structlog", "structlog"),
        ("pydantic", "pydantic")
    ]
    
    print("\n📦 Módulos Essenciais:")
    todos_ok = True
    
    for modulo_nome, import_nome in modulos_essenciais:
        try:
            __import__(import_nome)
            print(f"  ✅ {modulo_nome}: OK")
        except ImportError as e:
            print(f"  ❌ {modulo_nome}: Não instalado")
            todos_ok = False
    
    print("\n📦 Módulos Opcionais:")
    for modulo_nome, import_nome in modulos_opcionais:
        try:
            __import__(import_nome)
            print(f"  ✅ {modulo_nome}: OK")
        except ImportError:
            print(f"  ⚠️  {modulo_nome}: Não instalado (opcional)")
    
    # Verificar diretórios
    print("\n📁 Diretórios:")
    dirs_necessarios = ["data", "backups", "logs", "exports"]
    for dir_name in dirs_necessarios:
        if Path(dir_name).exists():
            print(f"  ✅ {dir_name}")
        else:
            print(f"  ⚠️  {dir_name} (criando...)")
            Path(dir_name).mkdir(exist_ok=True)
    
    if todos_ok:
        print("\n✨ SISTEMA PRONTO PARA EXECUÇÃO!")
        return True
    else:
        print("\n⚠️ Alguns módulos essenciais estão faltando.")
        print("   Execute: python install.py")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--check":
            verificar_instalacao()
        elif sys.argv[1] == "--quick":
            # Instalação rápida (só essenciais)
            install_dependencies_quick()
        else:
            print(f"Argumento desconhecido: {sys.argv[1]}")
    else:
        install_dependencies()
