#!/usr/bin/env python3
"""
Script de emergência para instalação em ambientes CI/CD
Instala tudo de forma sequencial e verificada
"""

import subprocess
import sys
import platform

def run_cmd(cmd, desc):
    """Executa comando e verifica resultado"""
    print(f"\n📦 {desc}...")
    try:
        subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {desc} concluído")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {desc} falhou: {e}")
        return False

def main():
    print("""
    🚨 ATENA - INSTALAÇÃO DE EMERGÊNCIA 🚨
    ======================================
    """)
    
    print(f"🐍 Python: {sys.version}")
    print(f"💻 Sistema: {platform.system()}")
    
    # Passo 1: Atualizar pip
    if not run_cmd(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        "Atualizando pip"
    ):
        print("❌ Falha crítica")
        return 1
    
    # Passo 2: Instalar wheel e setuptools
    run_cmd(
        [sys.executable, "-m", "pip", "install", "--upgrade", "wheel", "setuptools"],
        "Instalando wheel e setuptools"
    )
    
    # Passo 3: Instalar aiosqlite (crítico)
    if not run_cmd(
        [sys.executable, "-m", "pip", "install", "aiosqlite==0.19.0"],
        "Instalando aiosqlite"
    ):
        print("❌ Falha ao instalar aiosqlite")
        return 1
    
    # Passo 4: Instalar numpy
    if not run_cmd(
        [sys.executable, "-m", "pip", "install", "numpy==1.24.3"],
        "Instalando numpy"
    ):
        print("❌ Falha ao instalar numpy")
        return 1
    
    # Passo 5: Instalar resto das dependências
    packages = [
        "aiohttp==3.9.5",
        "pandas==2.0.3",
        "python-dateutil==2.8.2",
        "transformers==4.35.2",
        "torch==2.1.0",
        "sentence-transformers==2.2.2",
        "scikit-learn==1.3.2",
        "chromadb==0.4.22",
        "faiss-cpu==1.7.4",
        "networkx==3.1",
        "matplotlib==3.7.5",
        "seaborn==0.13.0",
        "python-dotenv==1.0.0",
        "tqdm==4.66.1",
        "colorama==0.4.6",
        "requests==2.31.0",
        "pyyaml==6.0.1"
    ]
    
    for pkg in packages:
        run_cmd(
            [sys.executable, "-m", "pip", "install", pkg],
            f"Instalando {pkg}"
        )
    
    # Verificação final
    print("\n🔍 Verificando instalação...")
    
    test_code = """
import sys
modules = ['aiosqlite', 'numpy', 'pandas', 'aiohttp']
for m in modules:
    try:
        __import__(m)
        print(f'✅ {m}')
    except ImportError as e:
        print(f'❌ {m}: {e}')
        sys.exit(1)
print('✨ Todos os módulos instalados!')
"""
    
    result = subprocess.run(
        [sys.executable, "-c", test_code],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        return 1
    
    print("\n🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
