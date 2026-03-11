#!/bin/bash
# Script de instalação rápida para CI/CD

echo "🚀 ATENA - Instalação Rápida para CI/CD"
echo "========================================"

# Criar diretórios necessários
mkdir -p data backups exports logs chromadb_data faiss_index

# Instalar dependências do sistema (Ubuntu/Debian)
if [ -f /etc/debian_version ]; then
    echo "📦 Instalando dependências do sistema..."
    sudo apt-get update
    sudo apt-get install -y \
        build-essential \
        cmake \
        libopenblas-dev \
        libsqlite3-dev \
        sqlite3 \
        python3-dev
fi

# Atualizar pip
echo "📦 Atualizando pip..."
python3 -m pip install --upgrade pip

# Instalar dependências em grupos (para melhor gerenciamento)
echo "📦 Instalando dependências principais..."
pip install --no-cache-dir \
    aiosqlite==0.19.0 \
    aiohttp==3.9.5 \
    numpy==1.24.3 \
    pandas==2.0.3

echo "📦 Instalando ML/NLP..."
pip install --no-cache-dir \
    transformers==4.35.2 \
    torch==2.1.2 \
    sentence-transformers==2.2.2 \
    scikit-learn==1.3.2

echo "📦 Instalando Vector DB..."
pip install --no-cache-dir \
    chromadb==0.4.24 \
    faiss-cpu==1.7.4

echo "📦 Instalando visualização..."
pip install --no-cache-dir \
    networkx==3.1 \
    matplotlib==3.7.5 \
    seaborn==0.13.0

echo "📦 Instalando utilitários..."
pip install --no-cache-dir \
    python-dotenv==1.0.0 \
    tqdm==4.66.1 \
    colorama==0.4.6 \
    requests==2.31.0 \
    pyyaml==6.0.1

echo "📦 Instalando serialização..."
pip install --no-cache-dir \
    orjson==3.9.15 \
    msgpack==1.0.7 \
    cloudpickle==3.0.0

echo "✅ Instalação concluída!"
echo ""
echo "📊 Verificando instalação..."

# Verificar instalação
python3 -c "
import sys
modules = ['aiosqlite', 'numpy', 'pandas', 'transformers', 'torch', 'chromadb', 'faiss']
missing = []
for m in modules:
    try:
        __import__(m)
        print(f'✅ {m}')
    except ImportError:
        print(f'❌ {m}')
        missing.append(m)

if missing:
    print(f'\n⚠️ Módulos faltando: {missing}')
    sys.exit(1)
else:
    print('\n✨ Todos os módulos instalados!')
"

echo ""
echo "🚀 Execute a ATENA com: python main.py"
