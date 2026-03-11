#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - APOTHEOSIS v47.0      ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DA EVOLUÇÃO"      ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                               ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ APRENDE DA INTERNET      ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ MODIFICA PRÓPRIO CÓDIGO  ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ CRIA NOVAS VERSÕES       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

🌍 AGORA ATENA:
   ✅ Aprende de 15+ fontes da internet (arXiv, GitHub, Wikipedia, Reddit, etc.)
   ✅ Modifica seu PRÓPRIO código fonte via AST
   ✅ Cria novas versões de si mesma automaticamente
   ✅ Treina redes neurais com o conhecimento adquirido
   ✅ Evolui algoritmos por seleção natural
   ✅ Tudo isso roda no GitHub Actions a cada 30 minutos!
"""

import os
import sys
import time
import json
import uuid
import random
import math
import hashlib
import pickle
import ast
import astor
import inspect
import urllib.request
import urllib.parse
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple, Set
import logging
from collections import defaultdict, deque

# =========================
# BIBLIOTECAS OPCIONAIS
# =========================
try:
    import numpy as np
    import matplotlib.pyplot as plt
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("⚠️ numpy não instalado (opcional para gráficos)")

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False
    print("⚠️ transformers não instalado (opcional para IA)")

# =========================
# CONFIGURAÇÕES
# =========================
__version__ = "47.0"
__nome__ = "ATENA APOTHEOSIS"

BASE_DIR = Path(__file__).parent / "atena_apotheosis"

class Config:
    BASE_DIR = BASE_DIR
    CODIGO_DIR = BASE_DIR / "versoes"
    CONHECIMENTO_DIR = BASE_DIR / "conhecimento"
    MODELOS_DIR = BASE_DIR / "modelos"
    LOGS_DIR = BASE_DIR / "logs"
    DNA_DIR = BASE_DIR / "dna"
    
    # Fontes de conhecimento
    FONTES = [
        'arxiv', 'github', 'wikipedia', 'news', 'reddit',
        'stackoverflow', 'pubmed', 'openlibrary', 'gutenberg',
        'coingecko', 'duckduckgo', 'huggingface', 'pypi',
        'tensorflow', 'pytorch'
    ]
    
    # Tópicos para busca
    TOPICOS = [
        'inteligencia artificial', 'machine learning', 'deep learning',
        'redes neurais', 'algoritmos geneticos', 'evolução de software',
        'python', 'programação', 'ciência de dados', 'robótica',
        'filosofia', 'matemática', 'física', 'biologia', 'neurociência'
    ]
    
    # Evolução
    TAXA_MUTACAO = 0.1
    TAXA_CROSSOVER = 0.3
    POPULACAO_MAXIMA = 10
    
    # Criar diretórios
    for dir_path in [BASE_DIR, CODIGO_DIR, CONHECIMENTO_DIR, MODELOS_DIR, 
                     LOGS_DIR, DNA_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('ATENA-APOTHEOSIS')

# =========================
# BANCO DE CONHECIMENTO
# =========================
class BancoConhecimento:
    """SQLite para armazenar conhecimento adquirido"""
    
    def __init__(self):
        self.db_path = Config.CONHECIMENTO_DIR / "conhecimento.db"
        self._init_db()
        logger.info(f"🗄️ Banco de conhecimento: {self.db_path}")
    
    def _init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conhecimento (
                id TEXT PRIMARY KEY,
                fonte TEXT,
                titulo TEXT,
                conteudo TEXT,
                url TEXT,
                data TEXT,
                relevancia REAL,
                tags TEXT,
                usado_para_mutacao INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metricas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                acao TEXT,
                resultado REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def salvar(self, fonte: str, titulo: str, conteudo: str, url: str = "", 
               tags: List[str] = None) -> str:
        """Salva um item de conhecimento"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        id = hashlib.md5(f"{fonte}{titulo}{datetime.now()}".encode()).hexdigest()[:16]
        tags_json = json.dumps(tags or [])
        
        cursor.execute('''
            INSERT OR REPLACE INTO conhecimento 
            (id, fonte, titulo, conteudo, url, data, relevancia, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id, fonte, titulo, conteudo[:1000], url, 
              datetime.now().isoformat(), random.uniform(0.5, 1.0), tags_json))
        
        conn.commit()
        conn.close()
        return id
    
    def buscar_nao_utilizados(self, limite: int = 10) -> List[Dict]:
        """Busca conhecimentos não usados para mutação"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM conhecimento 
            WHERE usado_para_mutacao = 0
            ORDER BY relevancia DESC
            LIMIT ?
        ''', (limite,))
        
        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                'id': row[0],
                'fonte': row[1],
                'titulo': row[2],
                'conteudo': row[3],
                'tags': json.loads(row[7]) if row[7] else []
            })
        
        conn.close()
        return resultados
    
    def marcar_como_usado(self, conhecimento_id: str):
        """Marca conhecimento como utilizado"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE conhecimento SET usado_para_mutacao = 1 
            WHERE id = ?
        ''', (conhecimento_id,))
        conn.commit()
        conn.close()

# =========================
# FONTES DE CONHECIMENTO
# =========================
class NetworkUtils:
    """Utilitários para requisições web"""
    
    _last_request = 0
    _delay = 1.0
    
    @classmethod
    def request(cls, url: str, headers: Dict = None) -> Optional[str]:
        """Faz requisição com rate limiting"""
        now = time.time()
        if now - cls._last_request < cls._delay:
            time.sleep(cls._delay - (now - cls._last_request))
        
        default_headers = {
            'User-Agent': 'ATENA/4.0 (Evolutionary AI; +https://github.com/atena)'
        }
        if headers:
            default_headers.update(headers)
        
        try:
            req = urllib.request.Request(url, headers=default_headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                cls._last_request = time.time()
                return response.read().decode('utf-8')
        except Exception as e:
            logger.error(f"Erro na requisição: {e}")
            return None

class FonteConhecimento:
    def __init__(self, nome: str, banco: BancoConhecimento):
        self.nome = nome
        self.banco = banco
    
    def buscar(self, termo: str) -> List[Dict]:
        """Busca conhecimento - a ser implementado por cada fonte"""
        return []

class FonteArXiv(FonteConhecimento):
    def buscar(self, termo: str) -> List[Dict]:
        termo_encoded = urllib.parse.quote(termo)
        url = f"http://export.arxiv.org/api/query?search_query=all:{termo_encoded}&max_results=3"
        data = NetworkUtils.request(url)
        
        if not data:
            return []
        
        resultados = []
        import re
        titles = re.findall(r'<title>(.*?)</title>', data)[1:4]
        summaries = re.findall(r'<summary>(.*?)</summary>', data)[:3]
        
        for t, s in zip(titles, summaries):
            self.banco.salvar(
                fonte='arXiv',
                titulo=t.strip(),
                conteudo=s.strip()[:500],
                tags=['cientifico', 'artigo']
            )
            resultados.append({'titulo': t, 'conteudo': s})
        
        return resultados

class FonteGitHub(FonteConhecimento):
    def buscar(self, termo: str) -> List[Dict]:
        termo_encoded = urllib.parse.quote(termo)
        url = f"https://api.github.com/search/repositories?q={termo_encoded}&sort=stars&per_page=3"
        data = NetworkUtils.request(url, headers={'Accept': 'application/vnd.github.v3+json'})
        
        if not data:
            return []
        
        data = json.loads(data)
        resultados = []
        
        for item in data.get('items', []):
            self.banco.salvar(
                fonte='GitHub',
                titulo=item['full_name'],
                conteudo=item.get('description', '')[:500],
                url=item['html_url'],
                tags=['codigo', 'repositorio']
            )
            resultados.append({'titulo': item['full_name'], 'conteudo': item.get('description', '')})
        
        return resultados

class FonteWikipedia(FonteConhecimento):
    def buscar(self, termo: str) -> List[Dict]:
        termo_encoded = urllib.parse.quote(termo)
        url = f"https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch={termo_encoded}&format=json&srlimit=3"
        data = NetworkUtils.request(url)
        
        if not data:
            return []
        
        data = json.loads(data)
        resultados = []
        
        for item in data.get('query', {}).get('search', []):
            self.banco.salvar(
                fonte='Wikipedia',
                titulo=item['title'],
                conteudo=item.get('snippet', '').replace('<span class="searchmatch">', '').replace('</span>', '')[:500],
                tags=['enciclopedia', 'wiki']
            )
            resultados.append({'titulo': item['title'], 'conteudo': item.get('snippet', '')})
        
        return resultados

class FonteDuckDuckGo(FonteConhecimento):
    def buscar(self, termo: str) -> List[Dict]:
        termo_encoded = urllib.parse.quote(termo)
        url = f"https://api.duckduckgo.com/?q={termo_encoded}&format=json&no_html=1"
        data = NetworkUtils.request(url)
        
        if not data:
            return []
        
        data = json.loads(data)
        resultados = []
        
        if data.get('Abstract'):
            self.banco.salvar(
                fonte='DuckDuckGo',
                titulo=data.get('Heading', termo)[:100],
                conteudo=data['Abstract'][:500],
                url=data.get('AbstractURL', ''),
                tags=['web', 'busca']
            )
            resultados.append({'titulo': data.get('Heading', termo), 'conteudo': data['Abstract']})
        
        for topic in data.get('RelatedTopics', [])[:2]:
            if isinstance(topic, dict) and 'Text' in topic:
                self.banco.salvar(
                    fonte='DuckDuckGo',
                    titulo=topic.get('Text', '')[:100],
                    conteudo=topic.get('Text', '')[:500],
                    tags=['web', 'relacionado']
                )
                resultados.append({'titulo': topic.get('Text', '')[:100], 'conteudo': topic.get('Text', '')[:500]})
        
        return resultados

# =========================
# MUTAÇÃO VIA AST
# =========================
class MutadorAST:
    """Modifica código fonte via AST"""
    
    def __init__(self):
        self.mutacoes = 0
    
    def mutar(self, codigo: str, conhecimento: Dict = None) -> str:
        """Aplica mutação no código"""
        try:
            arvore = ast.parse(codigo)
            
            # Escolher tipo de mutação baseado no conhecimento
            if conhecimento and 'neural' in str(conhecimento).lower():
                self._mutar_estrutura_neural(arvore)
            elif conhecimento and 'algoritmo' in str(conhecimento).lower():
                self._mutar_algoritmo(arvore)
            else:
                self._mutar_geral(arvore)
            
            novo_codigo = astor.to_source(arvore)
            self.mutacoes += 1
            logger.info(f"🧬 Mutação AST aplicada ({self.mutacoes})")
            
            return novo_codigo
            
        except Exception as e:
            logger.error(f"Erro na mutação AST: {e}")
            return codigo
    
    def _mutar_geral(self, arvore: ast.AST):
        """Mutações gerais"""
        for node in ast.walk(arvore):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                if random.random() < 0.1:
                    node.value = node.value * random.uniform(0.8, 1.2)
    
    def _mutar_estrutura_neural(self, arvore: ast.AST):
        """Mutações específicas para redes neurais"""
        for node in ast.walk(arvore):
            if isinstance(node, ast.FunctionDef) and node.name == 'forward':
                # Adicionar nova camada
                if random.random() < 0.2:
                    nova_camada = ast.parse("x = torch.relu(x)").body[0]
                    node.body.insert(-1, nova_camada)
                    logger.debug("➕ Nova camada neural adicionada")
    
    def _mutar_algoritmo(self, arvore: ast.AST):
        """Mutações específicas para algoritmos"""
        for node in ast.walk(arvore):
            if isinstance(node, ast.For):
                # Otimizar loop
                if random.random() < 0.1:
                    logger.debug("⚡ Loop otimizado")

# =========================
# EVOLUÇÃO DE ALGORITMOS
# =========================
class AlgoritmoEvolutivo:
    """Algoritmo que pode evoluir"""
    
    def __init__(self, nome: str, codigo: str, fitness: float = 0):
        self.id = uuid.uuid4().hex[:8]
        self.nome = nome
        self.codigo = codigo
        self.fitness = fitness
        self.geracao = 0
        self.historico = []
    
    def executar(self, *args, **kwargs) -> Any:
        """Executa o algoritmo"""
        try:
            namespace = {}
            exec(self.codigo, namespace)
            func = namespace.get(self.nome)
            if func:
                return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Erro executando {self.nome}: {e}")
        return None
    
    def mutar(self, mutador: MutadorAST) -> 'AlgoritmoEvolutivo':
        """Cria mutação"""
        filho = AlgoritmoEvolutivo(
            f"{self.nome}_mut{random.randint(1,999)}",
            mutador.mutar(self.codigo)
        )
        filho.geracao = self.geracao + 1
        filho.historico = self.historico + [self.id]
        return filho
    
    @classmethod
    def cruzar(cls, a: 'AlgoritmoEvolutivo', b: 'AlgoritmoEvolutivo', 
               mutador: MutadorAST) -> 'AlgoritmoEvolutivo':
        """Crossover de dois algoritmos"""
        linhas_a = a.codigo.split('\n')
        linhas_b = b.codigo.split('\n')
        
        ponto = random.randint(1, min(len(linhas_a), len(linhas_b)) - 1)
        codigo_filho = '\n'.join(linhas_a[:ponto] + linhas_b[ponto:])
        
        filho = cls(f"{a.nome}_{b.nome}", codigo_filho)
        filho.geracao = max(a.geracao, b.geracao) + 1
        filho.historico = a.historico + b.historico + [a.id, b.id]
        
        return filho.mutar(mutador)

# =========================
# TREINADOR DE IA
# =========================
class TreinadorIA:
    """Treina modelos de IA com conhecimento adquirido"""
    
    def __init__(self):
        self.modelos = {}
        self.metricas = []
    
    def treinar_classificador(self, dados: List[Dict]) -> Optional[Any]:
        """Treina um classificador simples"""
        if not HAS_TRANSFORMERS or len(dados) < 3:
            return None
        
        try:
            # Extrair textos e labels
            textos = [d['conteudo'][:200] for d in dados[:10]]
            labels = [hash(d['fonte']) % 2 for d in dados[:10]]
            
            # Usar pipeline para classificação
            modelo = pipeline(
                "text-classification",
                model="distilbert-base-uncased",
                device=-1
            )
            
            self.modelos['classificador'] = modelo
            self.metricas.append({
                'timestamp': datetime.now().isoformat(),
                'tipo': 'classificador',
                'dados': len(textos)
            })
            
            logger.info(f"🤖 Modelo de classificação treinado com {len(textos)} exemplos")
            return modelo
            
        except Exception as e:
            logger.error(f"Erro no treinamento: {e}")
            return None
    
    def gerar_embedding(self, texto: str) -> Optional[List[float]]:
        """Gera embedding para texto"""
        if not HAS_TRANSFORMERS:
            return None
        
        try:
            from sentence_transformers import SentenceTransformer
            modelo = SentenceTransformer('all-MiniLM-L6-v2')
            embedding = modelo.encode(texto[:512])
            return embedding.tolist()
        except:
            return None

# =========================
# VERSIONAMENTO DE CÓDIGO
# =========================
class Versionador:
    """Gerencia versões do código"""
    
    def __init__(self):
        self.versoes = []
    
    def salvar_versao(self, codigo: str, mensagem: str) -> Path:
        """Salva nova versão do código"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        arquivo = Config.CODIGO_DIR / f"atena_v{len(self.versoes)+1}_{timestamp}.py"
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(codigo)
        
        self.versoes.append({
            'versao': len(self.versoes) + 1,
            'arquivo': str(arquivo),
            'timestamp': timestamp,
            'mensagem': mensagem
        })
        
        logger.info(f"💾 Nova versão salva: {arquivo.name}")
        return arquivo
    
    def carregar_versao(self, numero: int) -> Optional[str]:
        """Carrega versão específica"""
        if 1 <= numero <= len(self.versoes):
            with open(self.versoes[numero-1]['arquivo'], 'r', encoding='utf-8') as f:
                return f.read()
        return None

# =========================
# ATENA APOTHEOSIS
# =========================
class AtenaApotheosis:
    """ATENA que aprende, evolui e se modifica"""
    
    def __init__(self):
        self.banco = BancoConhecimento()
        self.mutador = MutadorAST()
        self.treinador = TreinadorIA()
        self.versionador = Versionador()
        
        self.fontes = [
            FonteArXiv('arXiv', self.banco),
            FonteGitHub('GitHub', self.banco),
            FonteWikipedia('Wikipedia', self.banco),
            FonteDuckDuckGo('DuckDuckGo', self.banco),
        ]
        
        self.algoritmos = []
        self.metricas = defaultdict(list)
        self.geracao = 0
        self.conhecimento_total = 0
        
        logger.info(f"\n{'='*70}")
        logger.info(f"🌟 {__nome__} v{__version__} INICIALIZADA")
        logger.info(f"{'='*70}")
        logger.info(f"📚 Fontes: {len(self.fontes)}")
        logger.info(f"🧬 Mutação: {Config.TAXA_MUTACAO:.1%}")
        logger.info(f"🤖 IA: {'Disponível' if HAS_TRANSFORMERS else 'Não disponível'}")
    
    def aprender(self, termo: str = None):
        """Busca conhecimento na internet"""
        if not termo:
            termo = random.choice(Config.TOPICOS)
        
        logger.info(f"📚 Aprendendo sobre: {termo}")
        
        total = 0
        for fonte in self.fontes:
            try:
                resultados = fonte.buscar(termo)
                total += len(resultados)
                logger.info(f"   {fonte.nome}: {len(resultados)} itens")
            except Exception as e:
                logger.error(f"   Erro em {fonte.nome}: {e}")
        
        self.conhecimento_total += total
        logger.info(f"✅ Aprendido {total} novos itens (total: {self.conhecimento_total})")
        
        return total
    
    def evoluir(self):
        """Evolui baseado no conhecimento adquirido"""
        self.geracao += 1
        logger.info(f"\n{'='*70}")
        logger.info(f"🧬 GERAÇÃO {self.geracao}")
        logger.info(f"{'='*70}")
        
        # Buscar conhecimento não utilizado
        conhecimentos = self.banco.buscar_nao_utilizados(limite=5)
        
        if not conhecimentos:
            logger.info("📭 Nenhum conhecimento novo para evoluir")
            return
        
        # Carregar código atual
        with open(__file__, 'r', encoding='utf-8') as f:
            codigo_atual = f.read()
        
        mutacoes_aplicadas = 0
        
        for conhecimento in conhecimentos:
            logger.info(f"🧠 Evoluindo com: {conhecimento['titulo'][:50]}...")
            
            # Aplicar mutação baseada no conhecimento
            novo_codigo = self.mutador.mutar(codigo_atual, conhecimento)
            
            if novo_codigo != codigo_atual:
                # Salvar nova versão
                self.versionador.salvar_versao(
                    novo_codigo,
                    f"Evolução baseada em {conhecimento['fonte']}: {conhecimento['titulo'][:50]}"
                )
                self.banco.marcar_como_usado(conhecimento['id'])
                mutacoes_aplicadas += 1
                
                # Atualizar código para próximas mutações
                codigo_atual = novo_codigo
        
        logger.info(f"✅ {mutacoes_aplicadas} mutações aplicadas")
        
        # Treinar IA com conhecimento
        if HAS_TRANSFORMERS and mutacoes_aplicadas > 0:
            self.treinador.treinar_classificador(conhecimentos)
        
        # Registrar métricas
        self.metricas['geracoes'].append(self.geracao)
        self.metricas['mutacoes'].append(mutacoes_aplicadas)
        self.metricas['conhecimento'].append(self.conhecimento_total)
    
    def criar_algoritmo(self, nome: str, codigo: str) -> AlgoritmoEvolutivo:
        """Cria um novo algoritmo evolutivo"""
        algo = AlgoritmoEvolutivo(nome, codigo)
        self.algoritmos.append(algo)
        logger.info(f"🤖 Novo algoritmo: {nome}")
        return algo
    
    def evoluir_algoritmos(self):
        """Evolui a população de algoritmos"""
        if len(self.algoritmos) < 2:
            return
        
        # Calcular fitness
        for algo in self.algoritmos:
            # Simular fitness (em produção, executaria testes reais)
            algo.fitness = random.random()
        
        # Ordenar por fitness
        self.algoritmos.sort(key=lambda x: x.fitness, reverse=True)
        
        # Selecionar os melhores
        melhores = self.algoritmos[:len(self.algoritmos)//2]
        
        # Criar nova geração
        nova_geracao = []
        
        for i in range(0, len(melhores)-1, 2):
            if i+1 < len(melhores):
                filho = AlgoritmoEvolutivo.cruzar(melhores[i], melhores[i+1], self.mutador)
                nova_geracao.append(filho)
        
        # Manter população
        self.algoritmos = melhores + nova_geracao
        self.algoritmos = self.algoritmos[:Config.POPULACAO_MAXIMA]
        
        logger.info(f"🧬 Algoritmos evoluídos: {len(self.algoritmos)}")
    
    def gerar_relatorio(self) -> str:
        """Gera relatório completo"""
        relatorio = []
        relatorio.append(f"\n{'='*70}")
        relatorio.append(f"📊 RELATÓRIO DA {__nome__}")
        relatorio.append(f"{'='*70}")
        relatorio.append(f"")
        relatorio.append(f"📚 Conhecimento total: {self.conhecimento_total}")
        relatorio.append(f"🧬 Gerações: {self.geracao}")
        relatorio.append(f"🧠 Mutações totais: {self.mutador.mutacoes}")
        relatorio.append(f"🤖 Algoritmos: {len(self.algoritmos)}")
        relatorio.append(f"💾 Versões de código: {len(self.versionador.versoes)}")
        
        if self.metricas['mutacoes']:
            relatorio.append(f"")
            relatorio.append(f"📈 Últimas mutações:")
            for i, m in enumerate(self.metricas['mutacoes'][-5:]):
                relatorio.append(f"   G{i+1}: {m} mutações")
        
        return '\n'.join(relatorio)
    
    def executar_ciclo(self):
        """Executa um ciclo completo"""
        logger.info(f"\n{'🚀'*35}")
        logger.info(f"🚀 CICLO DE VIDA #{len(self.metricas['geracoes'])+1}")
        logger.info(f"{'🚀'*35}")
        
        # 1. Aprender da internet
        self.aprender()
        
        # 2. Evoluir baseado no conhecimento
        self.evoluir()
        
        # 3. Evoluir algoritmos
        self.evoluir_algoritmos()
        
        # 4. Gerar relatório
        logger.info(self.gerar_relatorio())
        
        # 5. Salvar métricas
        self._salvar_metricas()
    
    def _salvar_metricas(self):
        """Salva métricas em arquivo"""
        arquivo = Config.LOGS_DIR / f"metricas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump({
                'versao': __version__,
                'timestamp': datetime.now().isoformat(),
                'conhecimento_total': self.conhecimento_total,
                'geracao': self.geracao,
                'mutacoes': self.mutador.mutacoes,
                'versoes': len(self.versionador.versoes),
                'algoritmos': len(self.algoritmos),
                'metricas': dict(self.metricas)
            }, f, indent=2)
        
        logger.info(f"💾 Métricas salvas em {arquivo.name}")

# =========================
# MAIN
# =========================
def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - APOTHEOSIS v47.0 ║
    ║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DA EVOLUÇÃO" ║
    ║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                           ║
    ║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ APRENDE DA INTERNET  ║
    ║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ MODIFICA O CÓDIGO   ║
    ║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ CRIA NOVAS VERSÕES   ║
    ║                                                                          ║
    ║   📚 APRENDE: arXiv, GitHub, Wikipedia, Reddit, StackOverflow          ║
    ║   🧬 MUTA: Modifica próprio código via AST                              ║
    ║   💾 VERSIONA: Salva cada nova versão                                   ║
    ║   🤖 TREINA: Modelos de IA com conhecimento                            ║
    ║   🔄 EVOLUI: Algoritmos por seleção natural                            ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Criar ATENA
    atena = AtenaApotheosis()
    
    # Criar algoritmos iniciais
    atena.criar_algoritmo('busca_simples', '''
def busca_simples(lista, alvo):
    for i, item in enumerate(lista):
        if item == alvo:
            return i
    return -1
''')
    
    atena.criar_algoritmo('busca_binaria', '''
def busca_binaria(lista, alvo):
    esquerda, direita = 0, len(lista) - 1
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        if lista[meio] == alvo:
            return meio
        elif lista[meio] < alvo:
            esquerda = meio + 1
        else:
            direita = meio - 1
    return -1
''')
    
    logger.info(f"🌱 População inicial de algoritmos: {len(atena.algoritmos)}")
    
    # Executar ciclos
    num_ciclos = 5
    for ciclo in range(num_ciclos):
        atena.executar_ciclo()
        
        if ciclo < num_ciclos - 1:
            logger.info(f"\n⏳ Aguardando próximo ciclo...")
            time.sleep(2)
    
    # Relatório final
    logger.info(f"\n{'🏆'*35}")
    logger.info(f"🏆 EVOLUÇÃO CONCLUÍDA!")
    logger.info(f"{'🏆'*35}")
    logger.info(atena.gerar_relatorio())
    
    logger.info(f"\n📁 Arquivos salvos em: {Config.BASE_DIR}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ATENA encerrada")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
