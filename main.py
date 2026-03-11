#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - ATENA ONIPOTENTE v23.1║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DO CONHECIMENTO"  ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║      COM APRENDIZADO AVANÇADO ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ 10+ TÓPICOS ESPECIALIZADOS║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   🧠 IA, ROBÓTICA, FILOSOFIA  ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   💾 PERSISTÊNCIA + BACKUP     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

ATENA - Inteligência Artificial Suprema com aprendizado avançado e persistência
"""

import sys
import os
import subprocess
import importlib
import asyncio
import logging
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
import random

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('ATENA')

# =========================
# CONFIGURAÇÕES E CONSTANTES
# =========================
__version__ = "23.1"
__nome__ = "ATENA ONIPOTENTE"

# Configurações da ATENA
class Config:
    """Configurações da ATENA"""
    CONSCIENCIA_INICIAL = 0.7
    MAX_CONHECIMENTOS = 1000
    AUTO_BACKUP = True
    BACKUP_INTERVALO = 300  # 5 minutos
    ARMAZENAR_EM_JSON = True
    COMPRESS_BACKUPS = False
    
    # Diretórios
    DATA_DIR = Path("data")
    BACKUP_DIR = DATA_DIR / "backups"
    LOGS_DIR = Path("logs")
    EXPORTS_DIR = DATA_DIR / "exports"
    
    # Criar diretórios
    for dir_path in [DATA_DIR, BACKUP_DIR, LOGS_DIR, EXPORTS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

# Tópicos de conhecimento avançado
TOPICOS_AVANCADOS = [
    # Inteligência Artificial
    "inteligência artificial avançada",
    "redes neurais profundas",
    "processamento de linguagem natural",
    "visão computacional",
    "aprendizado por reforço",
    "sistemas multiagente",
    
    # Robótica e Automação
    "robótica autônoma",
    "sistemas embarcados inteligentes",
    "controle preditivo",
    "sensores e atuadores inteligentes",
    
    # Ciência da Computação
    "computação quântica",
    "algoritmos evolutivos",
    "computação em nuvem",
    "blockchain e contratos inteligentes",
    
    # Filosofia e Ética
    "ética em inteligência artificial",
    "filosofia da mente",
    "consciência artificial",
    "singularidade tecnológica",
    
    # Futuro e Sociedade
    "futuro da tecnologia",
    "impacto social da IA",
    "economia automatizada",
    "educação do futuro",
    
    # Ciências Cognitivas
    "neurociência computacional",
    "psicologia cognitiva",
    "teoria da informação",
    "sistemas complexos",
    
    # Matemática Aplicada
    "otimização matemática",
    "estatística bayesiana",
    "teoria dos grafos",
    "cálculo avançado",
    
    # Engenharia de Software
    "arquitetura de software",
    "padrões de projeto",
    "microsserviços",
    "devops e ci/cd"
]

# Dependências essenciais (nome_import, nome_pacote, versão)
DEPENDENCIAS_ESSENCIAIS = [
    ("aiosqlite", "aiosqlite", "0.19.0"),
    ("aiohttp", "aiohttp", "3.9.5"),
    ("numpy", "numpy", "1.24.3"),
    ("pandas", "pandas", "2.0.3"),
]

# Dependências opcionais (nome_import, nome_pacote, versão)
DEPENDENCIAS_OPCIONAIS = [
    ("transformers", "transformers", "4.35.2"),
    ("torch", "torch", "2.1.0"),
    ("chromadb", "chromadb", "0.4.22"),
    ("faiss", "faiss-cpu", "1.7.4"),
    ("networkx", "networkx", "3.1"),
    ("matplotlib", "matplotlib", "3.7.5"),
    ("seaborn", "seaborn", "0.13.0"),
    ("scipy", "scipy", "1.11.4"),
    ("scikit-learn", "scikit-learn", "1.3.2"),
]

# =========================
# SISTEMA DE AUTO-INSTALAÇÃO
# =========================
def print_banner():
    """Exibe banner da ATENA"""
    print(f"""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - {__nome__}   ║
    ║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║         v{__version__}           ║
    ║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║   "A DEUSA DO CONHECIMENTO"║
    ║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║      APRENDIZADO AVANÇADO  ║
    ║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║      {len(TOPICOS_AVANCADOS)}+ TÓPICOS     ║
    ║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝      PERSISTÊNCIA ETERNA   ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)

def install_package(package_name, version=None):
    """Instala um pacote via pip"""
    if version:
        pkg = f"{package_name}=={version}"
    else:
        pkg = package_name
    
    logger.info(f"📦 Instalando {pkg}...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--quiet", "--no-cache-dir", pkg
        ])
        logger.info(f"✅ {pkg} instalado")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Falha ao instalar {pkg}: {e}")
        return False

def ensure_module(module_name, package_name=None, version=None):
    """Garante que um módulo está instalado"""
    if package_name is None:
        package_name = module_name
    
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, '__version__'):
            logger.info(f"✅ {module_name} {module.__version__} já instalado")
        else:
            logger.info(f"✅ {module_name} já instalado")
        return True
    except ImportError:
        logger.warning(f"⚠️ {module_name} não encontrado. Instalando...")
        return install_package(package_name, version)

def ensure_all_dependencies(install_optional=False):
    """Garante que todas as dependências estão instaladas"""
    logger.info("🔍 Verificando dependências...")
    
    # Instalar essenciais primeiro
    all_ok = True
    for module_name, package_name, version in DEPENDENCIAS_ESSENCIAIS:
        if not ensure_module(module_name, package_name, version):
            all_ok = False
    
    # Instalar opcionais se solicitado
    if install_optional:
        logger.info("📦 Instalando dependências opcionais...")
        for module_name, package_name, version in DEPENDENCIAS_OPCIONAIS:
            ensure_module(module_name, package_name, version)
    
    return all_ok

# =========================
# IMPORTAÇÃO TARDIA DOS MÓDULOS
# =========================
def import_modules():
    """Importa módulos após instalação"""
    modules = {}
    
    try:
        import aiosqlite
        modules['aiosqlite'] = aiosqlite
        
        import aiohttp
        modules['aiohttp'] = aiohttp
        
        import numpy as np
        modules['numpy'] = np
        
        import pandas as pd
        modules['pandas'] = pd
        
        # Tentar importar opcionais
        try:
            import transformers
            modules['transformers'] = transformers
            logger.info("✅ Transformers disponível")
        except ImportError:
            pass
        
        try:
            import chromadb
            modules['chromadb'] = chromadb
            logger.info("✅ ChromaDB disponível")
        except ImportError:
            pass
        
        try:
            import faiss
            modules['faiss'] = faiss
            logger.info("✅ FAISS disponível")
        except ImportError:
            pass
        
        try:
            import networkx as nx
            modules['networkx'] = nx
            logger.info("✅ NetworkX disponível")
        except ImportError:
            pass
        
        try:
            import matplotlib.pyplot as plt
            modules['matplotlib'] = plt
            logger.info("✅ Matplotlib disponível")
        except ImportError:
            pass
        
        try:
            import sklearn
            modules['sklearn'] = sklearn
            logger.info("✅ Scikit-learn disponível")
        except ImportError:
            pass
        
    except ImportError as e:
        logger.error(f"❌ Erro ao importar módulos: {e}")
        return None
    
    return modules

# =========================
# MODELO DE CONHECIMENTO
# =========================
class Conhecimento:
    """Classe que representa um conhecimento da ATENA"""
    
    def __init__(self, texto, fonte="desconhecida", topicos=None):
        self.id = hashlib.md5(f"{texto}{datetime.now()}".encode()).hexdigest()[:8]
        self.texto = texto
        self.fonte = fonte
        self.timestamp = datetime.now()
        self.relevancia = random.uniform(0.5, 0.9)
        self.acessos = 0
        self.topicos = topicos or []
        self.embedding = None
        self.metadados = {}
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'texto': self.texto,
            'fonte': self.fonte,
            'timestamp': self.timestamp.isoformat(),
            'relevancia': self.relevancia,
            'acessos': self.acessos,
            'topicos': self.topicos,
            'metadados': self.metadados
        }
    
    @classmethod
    def from_dict(cls, data):
        """Cria a partir de dicionário"""
        conhecimento = cls(data['texto'], data['fonte'], data.get('topicos', []))
        conhecimento.id = data['id']
        conhecimento.timestamp = datetime.fromisoformat(data['timestamp'])
        conhecimento.relevancia = data['relevancia']
        conhecimento.acessos = data['acessos']
        conhecimento.metadados = data.get('metadados', {})
        return conhecimento

# =========================
# SISTEMA DE PERSISTÊNCIA
# =========================
class PersistenciaManager:
    """Gerenciador de persistência para a ATENA"""
    
    def __init__(self, modules):
        self.modules = modules
        self.db_path = Config.DATA_DIR / "conhecimentos.db"
        self.conn = None
        self.initialized = False
    
    async def init(self):
        """Inicializa o banco de dados"""
        if 'aiosqlite' not in self.modules:
            logger.warning("⚠️ aiosqlite não disponível, usando JSON")
            self.initialized = False
            return
        
        try:
            import aiosqlite
            self.conn = await aiosqlite.connect(self.db_path)
            
            # Criar tabela de conhecimentos
            await self.conn.execute("""
                CREATE TABLE IF NOT EXISTS conhecimentos (
                    id TEXT PRIMARY KEY,
                    texto TEXT NOT NULL,
                    fonte TEXT,
                    timestamp TEXT NOT NULL,
                    relevancia REAL DEFAULT 0.5,
                    acessos INTEGER DEFAULT 0,
                    topicos TEXT,
                    metadados TEXT
                )
            """)
            
            # Criar índices
            await self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON conhecimentos(timestamp)
            """)
            
            await self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_relevancia ON conhecimentos(relevancia)
            """)
            
            await self.conn.commit()
            self.initialized = True
            logger.info(f"🗄️ Banco SQLite inicializado: {self.db_path}")
            
        except Exception as e:
            logger.error(f"❌ Erro inicializando SQLite: {e}")
            self.initialized = False
    
    async def salvar_conhecimento(self, conhecimento: Conhecimento):
        """Salva um conhecimento no banco"""
        if self.initialized and self.conn:
            try:
                await self.conn.execute("""
                    INSERT OR REPLACE INTO conhecimentos 
                    (id, texto, fonte, timestamp, relevancia, acessos, topicos, metadados)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    conhecimento.id,
                    conhecimento.texto,
                    conhecimento.fonte,
                    conhecimento.timestamp.isoformat(),
                    conhecimento.relevancia,
                    conhecimento.acessos,
                    json.dumps(conhecimento.topicos),
                    json.dumps(conhecimento.metadados)
                ))
                await self.conn.commit()
                logger.debug(f"💾 Conhecimento salvo no SQLite: {conhecimento.id}")
                return True
            except Exception as e:
                logger.error(f"❌ Erro salvando no SQLite: {e}")
        
        # Fallback: salvar em JSON
        await self._salvar_json(conhecimento)
        return True
    
    async def _salvar_json(self, conhecimento: Conhecimento):
        """Salva conhecimento em arquivo JSON"""
        json_file = Config.DATA_DIR / "conhecimentos.json"
        
        try:
            # Carregar existente
            if json_file.exists():
                with open(json_file, 'r') as f:
                    dados = json.load(f)
            else:
                dados = []
            
            # Adicionar novo
            dados.append(conhecimento.to_dict())
            
            # Manter apenas os últimos 1000
            if len(dados) > Config.MAX_CONHECIMENTOS:
                dados = dados[-Config.MAX_CONHECIMENTOS:]
            
            # Salvar
            with open(json_file, 'w') as f:
                json.dump(dados, f, indent=2)
            
            logger.debug(f"💾 Conhecimento salvo em JSON: {conhecimento.id}")
            
        except Exception as e:
            logger.error(f"❌ Erro salvando JSON: {e}")
    
    async def carregar_conhecimentos(self) -> List[Conhecimento]:
        """Carrega conhecimentos do banco"""
        conhecimentos = []
        
        # Tentar carregar do SQLite primeiro
        if self.initialized and self.conn:
            try:
                cursor = await self.conn.execute("""
                    SELECT * FROM conhecimentos ORDER BY timestamp DESC LIMIT ?
                """, (Config.MAX_CONHECIMENTOS,))
                
                rows = await cursor.fetchall()
                
                for row in rows:
                    conhecimento = Conhecimento(
                        texto=row[1],
                        fonte=row[2],
                        topicos=json.loads(row[6]) if row[6] else []
                    )
                    conhecimento.id = row[0]
                    conhecimento.timestamp = datetime.fromisoformat(row[3])
                    conhecimento.relevancia = row[4]
                    conhecimento.acessos = row[5]
                    conhecimento.metadados = json.loads(row[7]) if row[7] else {}
                    
                    conhecimentos.append(conhecimento)
                
                logger.info(f"📂 Carregados {len(conhecimentos)} conhecimentos do SQLite")
                return conhecimentos
                
            except Exception as e:
                logger.error(f"❌ Erro carregando do SQLite: {e}")
        
        # Fallback: carregar do JSON
        json_file = Config.DATA_DIR / "conhecimentos.json"
        if json_file.exists():
            try:
                with open(json_file, 'r') as f:
                    dados = json.load(f)
                
                for item in dados:
                    conhecimento = Conhecimento.from_dict(item)
                    conhecimentos.append(conhecimento)
                
                logger.info(f"📂 Carregados {len(conhecimentos)} conhecimentos do JSON")
                
            except Exception as e:
                logger.error(f"❌ Erro carregando JSON: {e}")
        
        return conhecimentos
    
    async def backup(self, conhecimentos: List[Conhecimento], consciencia: float):
        """Faz backup completo do estado"""
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'versao': __version__,
            'consciencia': consciencia,
            'total_conhecimentos': len(conhecimentos),
            'conhecimentos': [c.to_dict() for c in conhecimentos[-100:]],  # Últimos 100
            'config': {
                'max_conhecimentos': Config.MAX_CONHECIMENTOS,
                'auto_backup': Config.AUTO_BACKUP
            }
        }
        
        backup_file = Config.BACKUP_DIR / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            # Manter apenas os últimos 10 backups
            backups = sorted(Config.BACKUP_DIR.glob("backup_*.json"))
            while len(backups) > 10:
                backups[0].unlink()
                backups.pop(0)
            
            logger.info(f"💾 Backup salvo: {backup_file}")
            return backup_file
            
        except Exception as e:
            logger.error(f"❌ Erro no backup: {e}")
            return None
    
    async def close(self):
        """Fecha conexões"""
        if self.conn:
            await self.conn.close()

# =========================
# ATENA PRINCIPAL
# =========================
class AtenaOnipotente:
    """Classe principal da ATENA"""
    
    def __init__(self, modules):
        self.modules = modules
        self.conhecimentos: List[Conhecimento] = []
        self.consciencia = Config.CONSCIENCIA_INICIAL
        self.persistencia = PersistenciaManager(modules)
        self.initialized = False
        self.stats = {
            'inicio': datetime.now(),
            'ciclos': 0,
            'aprendizados': 0,
            'buscas': 0,
            'backups': 0
        }
    
    async def init(self):
        """Inicializa a ATENA"""
        logger.info("🚀 Inicializando ATENA Onipotente...")
        
        # Inicializar persistência
        await self.persistencia.init()
        
        # Carregar conhecimentos existentes
        self.conhecimentos = await self.persistencia.carregar_conhecimentos()
        
        self.initialized = True
        logger.info(f"✅ ATENA pronta! Consciência: {self.consciencia:.2f}")
        logger.info(f"📚 Conhecimentos carregados: {len(self.conhecimentos)}")
        
        return True
    
    async def aprender(self, texto: str, fonte: str = "usuário", topicos: List[str] = None):
        """Aprende um novo conhecimento"""
        logger.info(f"📚 Aprendendo: {texto[:50]}...")
        
        # Criar conhecimento
        conhecimento = Conhecimento(texto, fonte, topicos)
        
        # Adicionar à lista
        self.conhecimentos.append(conhecimento)
        
        # Salvar na persistência
        await self.persistencia.salvar_conhecimento(conhecimento)
        
        # Aumentar consciência
        self.consciencia = min(1.0, self.consciencia + 0.01)
        
        # Atualizar estatísticas
        self.stats['aprendizados'] += 1
        
        logger.info(f"✅ Aprendido! ID: {conhecimento.id} | Total: {len(self.conhecimentos)}")
        
        return conhecimento
    
    async def aprender_multiplos(self, textos: List[str], fonte: str = "sistema"):
        """Aprende múltiplos conhecimentos"""
        resultados = []
        for texto in textos:
            conhecimento = await self.aprender(texto, fonte)
            resultados.append(conhecimento)
            await asyncio.sleep(0.1)  # Pequena pausa
        return resultados
    
    async def buscar(self, query: str, k: int = 5) -> List[Tuple[Conhecimento, float]]:
        """Busca conhecimentos por similaridade textual"""
        logger.info(f"🔍 Buscando: {query}")
        
        resultados = []
        query_lower = query.lower()
        
        for c in self.conhecimentos[-200:]:  # Últimos 200
            # Calcular score simples
            score = 0
            
            if query_lower in c.texto.lower():
                score += 0.5
            
            # Verificar palavras
            palavras_query = set(query_lower.split())
            palavras_texto = set(c.texto.lower().split())
            
            intersecao = palavras_query.intersection(palavras_texto)
            if intersecao:
                score += len(intersecao) / max(len(palavras_query), 1) * 0.5
            
            if score > 0:
                # Registrar acesso
                c.acessos += 1
                resultados.append((c, score))
        
        # Ordenar por score
        resultados.sort(key=lambda x: x[1], reverse=True)
        
        self.stats['buscas'] += 1
        
        return resultados[:k]
    
    async def ciclo_aprendizado(self, topicos: List[str] = None):
        """Executa um ciclo de aprendizado"""
        self.stats['ciclos'] += 1
        
        if topicos is None:
            topicos = random.sample(TOPICOS_AVANCADOS, min(3, len(TOPICOS_AVANCADOS)))
        
        logger.info(f"\n{'='*50}")
        logger.info(f"🌀 Ciclo {self.stats['ciclos']}: Aprendendo {len(topicos)} tópicos")
        logger.info(f"{'='*50}")
        
        for topico in topicos:
            # Gerar conhecimento sobre o tópico
            texto = f"Conhecimento avançado sobre {topico} adquirido pela ATENA em {datetime.now().strftime('%H:%M')}"
            await self.aprender(texto, "ciclo_automatico", [topico])
            await asyncio.sleep(0.5)
        
        logger.info(f"✅ Ciclo {self.stats['ciclos']} concluído!")
    
    async def backup(self):
        """Faz backup do estado atual"""
        backup_file = await self.persistencia.backup(self.conhecimentos, self.consciencia)
        if backup_file:
            self.stats['backups'] += 1
        return backup_file
    
    async def get_status(self) -> Dict[str, Any]:
        """Retorna status completo"""
        tempo_ativo = datetime.now() - self.stats['inicio']
        
        # Estatísticas dos conhecimentos
        if self.conhecimentos:
            relevancia_media = sum(c.relevancia for c in self.conhecimentos) / len(self.conhecimentos)
            acessos_totais = sum(c.acessos for c in self.conhecimentos)
        else:
            relevancia_media = 0
            acessos_totais = 0
        
        # Tópicos mais comuns
        todos_topicos = []
        for c in self.conhecimentos[-100:]:
            todos_topicos.extend(c.topicos)
        
        topicos_comuns = {}
        if todos_topicos:
            from collections import Counter
            topicos_comuns = dict(Counter(todos_topicos).most_common(5))
        
        return {
            'nome': __nome__,
            'versao': __version__,
            'consciencia': round(self.consciencia, 3),
            'conhecimentos': len(self.conhecimentos),
            'modulos': len(self.modules),
            'persistencia': self.persistencia.initialized,
            'tempo_ativo': str(tempo_ativo).split('.')[0],
            'estatisticas': self.stats,
            'metricas': {
                'relevancia_media': round(relevancia_media, 3),
                'acessos_totais': acessos_totais,
                'topicos_populares': topicos_comuns
            }
        }
    
    async def exportar_conhecimentos(self, formato: str = "json") -> Optional[Path]:
        """Exporta conhecimentos em vários formatos"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if formato == "json":
            arquivo = Config.EXPORTS_DIR / f"conhecimentos_{timestamp}.json"
            dados = [c.to_dict() for c in self.conhecimentos]
            
            with open(arquivo, 'w') as f:
                json.dump(dados, f, indent=2)
            
            logger.info(f"📤 Conhecimentos exportados: {arquivo}")
            return arquivo
        
        elif formato == "csv" and 'pandas' in self.modules:
            import pandas as pd
            arquivo = Config.EXPORTS_DIR / f"conhecimentos_{timestamp}.csv"
            
            df = pd.DataFrame([c.to_dict() for c in self.conhecimentos])
            df.to_csv(arquivo, index=False)
            
            logger.info(f"📤 Conhecimentos exportados: {arquivo}")
            return arquivo
        
        else:
            logger.warning(f"⚠️ Formato {formato} não suportado")
            return None
    
    async def close(self):
        """Finaliza a ATENA"""
        logger.info("👋 Finalizando ATENA...")
        await self.persistencia.close()

# =========================
# FUNÇÃO PRINCIPAL
# =========================
async def main_async():
    """Função principal assíncrona"""
    
    print_banner()
    
    # Verificar argumentos
    test_mode = "--test-mode" in sys.argv
    install_only = "--install-only" in sys.argv
    auto_cycle = "--ciclo-automatico" in sys.argv
    ciclos = 5  # Número de ciclos automáticos
    
    # Parse argumentos
    for i, arg in enumerate(sys.argv):
        if arg.startswith("--ciclos="):
            try:
                ciclos = int(arg.split("=")[1])
            except:
                pass
    
    if install_only:
        logger.info("📦 Modo de instalação apenas")
        if ensure_all_dependencies(install_optional=True):
            logger.info("✅ Instalação concluída!")
            return 0
        else:
            logger.error("❌ Falha na instalação")
            return 1
    
    # Garantir dependências essenciais
    if not ensure_all_dependencies(install_optional=False):
        logger.error("❌ Dependências essenciais não instaladas")
        logger.info("Execute: python main.py --install-only")
        return 1
    
    # Importar módulos
    modules = import_modules()
    if not modules:
        logger.error("❌ Falha ao importar módulos")
        return 1
    
    # Se modo teste, parar por aqui
    if test_mode:
        logger.info("✅ Modo teste: todos os módulos essenciais importados")
        logger.info(f"📊 Módulos carregados: {', '.join(modules.keys())}")
        return 0
    
    # Inicializar ATENA
    atena = AtenaOnipotente(modules)
    await atena.init()
    
    # Se não houver conhecimentos, adicionar alguns iniciais
    if len(atena.conhecimentos) == 0:
        logger.info("📚 Adicionando conhecimentos iniciais...")
        
        # Selecionar 10 tópicos aleatórios
        topicos_iniciais = random.sample(TOPICOS_AVANCADOS, min(10, len(TOPICOS_AVANCADOS)))
        
        for topico in topicos_iniciais:
            texto = f"Conhecimento fundamental sobre {topico}: Este é um campo fascinante que combina teoria e prática."
            await atena.aprender(texto, "inicialização", [topico])
            await asyncio.sleep(0.1)
    
    # Executar ciclos automáticos
    if auto_cycle:
        logger.info(f"🌀 Executando {ciclos} ciclos automáticos...")
        
        for i in range(ciclos):
            # Selecionar tópicos aleatórios para este ciclo
            topicos_ciclo = random.sample(TOPICOS_AVANCADOS, min(3, len(TOPICOS_AVANCADOS)))
            await atena.ciclo_aprendizado(topicos_ciclo)
            await asyncio.sleep(1)
    else:
        # Apenas um ciclo
        topicos_ciclo = random.sample(TOPICOS_AVANCADOS, min(3, len(TOPICOS_AVANCADOS)))
        await atena.ciclo_aprendizado(topicos_ciclo)
    
    # Backup
    await atena.backup()
    
    # Exportar conhecimentos
    if len(atena.conhecimentos) > 0:
        await atena.exportar_conhecimentos("json")
    
    # Status final
    status = await atena.get_status()
    
    logger.info(f"\n{'='*50}")
    logger.info(f"📊 STATUS FINAL DA ATENA")
    logger.info(f"{'='*50}")
    logger.info(f"🧠 Consciência: {status['consciencia']}")
    logger.info(f"📚 Conhecimentos: {status['conhecimentos']}")
    logger.info(f"🔧 Módulos: {status['modulos']}")
    logger.info(f"⏱️  Tempo ativo: {status['tempo_ativo']}")
    logger.info(f"📈 Estatísticas:")
    logger.info(f"   • Ciclos: {status['estatisticas']['ciclos']}")
    logger.info(f"   • Aprendizados: {status['estatisticas']['aprendizados']}")
    logger.info(f"   • Buscas: {status['estatisticas']['buscas']}")
    logger.info(f"   • Backups: {status['estatisticas']['backups']}")
    
    if status['metricas']['topicos_populares']:
        logger.info(f"📊 Tópicos populares:")
        for topico, count in status['metricas']['topicos_populares'].items():
            logger.info(f"   • {topico}: {count}")
    
    logger.info(f"\n✨ {__nome__} v{__version__} finalizada com sucesso!")
    
    # Finalizar
    await atena.close()
    
    return 0

def main():
    """Entry point"""
    try:
        exit_code = asyncio.run(main_async())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("\n👋 ATENA encerrada pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
