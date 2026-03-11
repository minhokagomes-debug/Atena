#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - ATENA AUTO-EVOLUTIVA v34.0║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DA AUTO-MODIFICAÇÃO" ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                               ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ APRENDE → REESCREVE      ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ CONHECIMENTO → MUTAÇÃO   ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ EVOLUI SEU PRÓPRIO CÓDIGO║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

🌍 AGORA ATENA:
   ✅ Aprende de 10+ fontes externas
   ✅ ARMAZENA conhecimento em SQLite
   ✅ ANALISA o que aprendeu
   ✅ REESCREVE seu próprio código baseado no conhecimento
   ✅ MUDA seu comportamento em tempo real
   ✅ EVOLUI geneticamente através do aprendizado
"""

import os
import sys
import time
import json
import uuid
import random
import signal
import socket
import subprocess
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
import sqlite3
import hashlib
import inspect
import ast
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
import logging
import threading
import queue
from collections import defaultdict

# =========================
# CONFIGURAÇÕES
# =========================
__version__ = "34.0"
__nome__ = "ATENA AUTO-EVOLUTIVA"

BASE_DIR = Path(__file__).parent / "atena_mundo"

class Config:
    BASE_DIR = BASE_DIR
    MUNDO_DIR = BASE_DIR / "mundo"
    DNA_DIR = BASE_DIR / "dna"
    LOGS_DIR = BASE_DIR / "logs"
    FOSSEIS_DIR = BASE_DIR / "fosseis"
    CONHECIMENTO_DIR = BASE_DIR / "conhecimento"
    CACHE_DIR = BASE_DIR / "cache"
    CODIGO_FONTE = Path(__file__)  # O próprio arquivo
    
    # Auto-modificação
    BACKUP_DIR = BASE_DIR / "backups"
    GERACOES_DIR = BASE_DIR / "geracoes"
    
    # User Agents
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'ATENA/2.0 (Evolutionary AI; +https://github.com/atena)',
        'Python-urllib/3.10 (Self-Modifying System)'
    ]
    
    # Rate limiting
    REQUEST_DELAY = 1.0
    MAX_RETRIES = 3
    
    # Criar diretórios
    for dir_path in [BASE_DIR, MUNDO_DIR, DNA_DIR, LOGS_DIR, FOSSEIS_DIR, 
                     CONHECIMENTO_DIR, CACHE_DIR, BACKUP_DIR, GERACOES_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler(Config.LOGS_DIR / f"atena_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ATENA')

# =========================
# BANCO DE CONHECIMENTO
# =========================
class BancoConhecimento:
    """Banco SQLite para armazenar conhecimento adquirido"""
    
    def __init__(self):
        self.db_path = Config.CONHECIMENTO_DIR / "conhecimento.db"
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Tabela de conhecimento
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
                acessos INTEGER DEFAULT 0,
                usado_para_mutacao INTEGER DEFAULT 0
            )
        ''')
        
        # Tabela de padrões aprendidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS padroes (
                id TEXT PRIMARY KEY,
                padrao TEXT,
                contexto TEXT,
                frequencia INTEGER,
                ultima_ocorrencia TEXT
            )
        ''')
        
        # Tabela de mutações genéticas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mutacoes (
                id TEXT PRIMARY KEY,
                gene_afetado TEXT,
                tipo_mutacao TEXT,
                fonte_conhecimento TEXT,
                data TEXT,
                sucesso BOOLEAN
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"🗄️ Banco de conhecimento evolutivo inicializado")
    
    def salvar_conhecimento(self, fonte: str, titulo: str, conteudo: str, 
                           url: str = "", tags: List[str] = None) -> str:
        """Salva um item de conhecimento"""
        try:
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
        except Exception as e:
            logger.error(f"Erro salvando conhecimento: {e}")
            return None
    
    def buscar_conhecimento_para_mutacao(self, limite: int = 10) -> List[Dict]:
        """Busca conhecimentos que podem gerar mutações"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM conhecimento 
                WHERE usado_para_mutacao = 0
                ORDER BY relevancia DESC, data DESC
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
        except Exception as e:
            logger.error(f"Erro buscando conhecimento: {e}")
            return []
    
    def marcar_como_usado(self, conhecimento_id: str):
        """Marca conhecimento como usado para mutação"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE conhecimento SET usado_para_mutacao = 1 
                WHERE id = ?
            ''', (conhecimento_id,))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Erro marcando conhecimento: {e}")

# =========================
# ANALISADOR DE CONHECIMENTO
# =========================
class AnalisadorConhecimento:
    """Analisa conhecimento e extrai padrões para mutação"""
    
    def __init__(self, banco: BancoConhecimento):
        self.banco = banco
        self.palavras_chave = defaultdict(int)
        self.padroes_aprendidos = []
    
    def analisar_para_mutacao(self, conhecimento: Dict) -> Dict[str, Any]:
        """
        Analisa um item de conhecimento e retorna sugestões de mutação
        """
        texto = f"{conhecimento['titulo']} {conhecimento['conteudo']}".lower()
        tags = conhecimento.get('tags', [])
        
        mutacoes = {
            'tipo': None,
            'gene_afetado': None,
            'parametros': {},
            'confianca': 0.5
        }
        
        # Analisar padrões no texto
        palavras = re.findall(r'\b\w+\b', texto)
        
        # Detectar padrões de código
        if 'python' in texto or 'código' in texto or 'programação' in texto:
            mutacoes['tipo'] = 'otimizacao_codigo'
            mutacoes['gene_afetado'] = 'execucao'
            mutacoes['confianca'] = 0.7
            
            # Extrair conceitos específicos
            if 'função' in texto or 'funcao' in texto:
                mutacoes['parametros']['otimizar'] = 'funcoes'
            if 'loop' in texto or 'for' in texto:
                mutacoes['parametros']['otimizar'] = 'loops'
        
        # Detectar padrões de IA/ML
        elif any(p in texto for p in ['inteligência', 'aprendizado', 'machine learning', 'ia']):
            mutacoes['tipo'] = 'aumentar_aprendizado'
            mutacoes['gene_afetado'] = 'curiosidade'
            mutacoes['confianca'] = 0.8
            mutacoes['parametros']['aumento'] = 0.2
        
        # Detectar padrões de reprodução
        elif 'evolução' in texto or 'reprodução' in texto or 'genético' in texto:
            mutacoes['tipo'] = 'aumentar_reproducao'
            mutacoes['gene_afetado'] = 'reproduzir'
            mutacoes['confianca'] = 0.75
            mutacoes['parametros']['aumento'] = 0.15
        
        # Detectar padrões de exploração
        elif 'explorar' in texto or 'descobrir' in texto or 'novo' in texto:
            mutacoes['tipo'] = 'aumentar_exploracao'
            mutacoes['gene_afetado'] = 'explorar'
            mutacoes['confianca'] = 0.7
            mutacoes['parametros']['aumento'] = 0.1
        
        # Detectar padrões de criação
        elif 'criar' in texto or 'construir' in texto or 'fazer' in texto:
            mutacoes['tipo'] = 'aumentar_criatividade'
            mutacoes['gene_afetado'] = 'criar'
            mutacoes['confianca'] = 0.65
            mutacoes['parametros']['aumento'] = 0.12
        
        return mutacoes

# =========================
# AUTO-MODIFICADOR DE CÓDIGO
# =========================
class AutoModificador:
    """
    ATENA modifica seu PRÓPRIO código fonte baseado no que aprendeu
    """
    
    def __init__(self):
        self.arquivo_fonte = Config.CODIGO_FONTE
        self.historico_versoes = []
        self.geracao_atual = 0
    
    def fazer_backup(self) -> Path:
        """Faz backup do código atual antes de modificar"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = Config.BACKUP_DIR / f"atena_v{self.geracao_atual}_{timestamp}.py"
        
        with open(self.arquivo_fonte, 'r') as f:
            codigo = f.read()
        
        with open(backup_path, 'w') as f:
            f.write(codigo)
        
        logger.info(f"💾 Backup salvo: {backup_path.name}")
        return backup_path
    
    def aplicar_mutacao(self, mutacao: Dict) -> bool:
        """
        Aplica uma mutação no código fonte baseado no conhecimento
        """
        try:
            # Fazer backup antes de modificar
            self.fazer_backup()
            
            # Ler código atual
            with open(self.arquivo_fonte, 'r') as f:
                codigo = f.read()
            
            # Aplicar mutação baseada no tipo
            if mutacao['tipo'] == 'otimizacao_codigo':
                codigo = self._otimizar_codigo(codigo, mutacao)
            elif mutacao['tipo'] == 'aumentar_aprendizado':
                codigo = self._aumentar_curiosidade(codigo, mutacao)
            elif mutacao['tipo'] == 'aumentar_reproducao':
                codigo = self._aumentar_reproducao(codigo, mutacao)
            elif mutacao['tipo'] == 'aumentar_exploracao':
                codigo = self._aumentar_exploracao(codigo, mutacao)
            elif mutacao['tipo'] == 'aumentar_criatividade':
                codigo = self._aumentar_criatividade(codigo, mutacao)
            
            # Adicionar comentário sobre a mutação
            comentario = f"\n# =========================\n"
            comentario += f"# 🧬 MUTAÇÃO APLICADA em {datetime.now()}\n"
            comentario += f"# Fonte: {mutacao.get('tipo', 'desconhecida')}\n"
            comentario += f"# Confiança: {mutacao.get('confianca', 0):.1%}\n"
            comentario += f"# =========================\n"
            
            # Inserir comentário no início do arquivo
            linhas = codigo.split('\n')
            linhas.insert(10, comentario)  # Depois do banner
            codigo = '\n'.join(linhas)
            
            # Salvar nova versão
            nova_versao_path = Config.GERACOES_DIR / f"atena_gen_{self.geracao_atual + 1}.py"
            with open(nova_versao_path, 'w') as f:
                f.write(codigo)
            
            # Atualizar o arquivo principal
            with open(self.arquivo_fonte, 'w') as f:
                f.write(codigo)
            
            self.geracao_atual += 1
            self.historico_versoes.append({
                'geracao': self.geracao_atual,
                'mutacao': mutacao,
                'arquivo': str(nova_versao_path),
                'timestamp': datetime.now().isoformat()
            })
            
            logger.info(f"🧬 MUTAÇÃO APLICADA: {mutacao['tipo']} (confiança: {mutacao['confianca']:.1%})")
            logger.info(f"   Nova geração: {self.geracao_atual}")
            logger.info(f"   Arquivo: {nova_versao_path.name}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro aplicando mutação: {e}")
            return False
    
    def _otimizar_codigo(self, codigo: str, mutacao: Dict) -> str:
        """Otimiza partes do código"""
        # Procurar por loops que podem ser otimizados
        linhas = codigo.split('\n')
        
        for i, linha in enumerate(linhas):
            # Otimizar loops for simples
            if 'for ' in linha and 'range' in linha:
                if 'explorar' in linhas[i-2:i+2]:
                    # Adicionar otimização
                    linhas.insert(i+1, '            # Loop otimizado por conhecimento adquirido')
        
        return '\n'.join(linhas)
    
    def _aumentar_curiosidade(self, codigo: str, mutacao: Dict) -> str:
        """Aumenta o traço de curiosidade no DNA"""
        aumento = mutacao.get('parametros', {}).get('aumento', 0.1)
        
        # Procurar pela definição de comportamentos no DNA
        padrao = r"'curiosidade': [0-9.]+"
        substituto = f"'curiosidade': {min(0.99, 0.7 + aumento):.2f}"
        
        codigo = re.sub(padrao, substituto, codigo)
        return codigo
    
    def _aumentar_reproducao(self, codigo: str, mutacao: Dict) -> str:
        """Aumenta a taxa de reprodução"""
        aumento = mutacao.get('parametros', {}).get('aumento', 0.1)
        
        padrao = r"'reproduzir': [0-9.]+"
        substituto = f"'reproduzir': {min(0.99, 0.5 + aumento):.2f}"
        
        codigo = re.sub(padrao, substituto, codigo)
        return codigo
    
    def _aumentar_exploracao(self, codigo: str, mutacao: Dict) -> str:
        """Aumenta a taxa de exploração"""
        aumento = mutacao.get('parametros', {}).get('aumento', 0.1)
        
        padrao = r"'explorar': [0-9.]+"
        substituto = f"'explorar': {min(0.99, 0.6 + aumento):.2f}"
        
        codigo = re.sub(padrao, substituto, codigo)
        return codigo
    
    def _aumentar_criatividade(self, codigo: str, mutacao: Dict) -> str:
        """Aumenta a criatividade"""
        aumento = mutacao.get('parametros', {}).get('aumento', 0.1)
        
        padrao = r"'criar': [0-9.]+"
        substituto = f"'criar': {min(0.99, 0.5 + aumento):.2f}"
        
        codigo = re.sub(padrao, substituto, codigo)
        return codigo

# =========================
# FONTES DE CONHECIMENTO (ATUALIZADAS)
# =========================
class NetworkUtils:
    """Utilitários para requisições de rede com rate limiting"""
    
    _last_request = 0
    _lock = threading.Lock()
    
    @classmethod
    def request(cls, url: str, timeout: int = 10, headers: Dict = None) -> Optional[Any]:
        with cls._lock:
            now = time.time()
            if now - cls._last_request < Config.REQUEST_DELAY:
                time.sleep(Config.REQUEST_DELAY - (now - cls._last_request))
            
            default_headers = {
                'User-Agent': random.choice(Config.USER_AGENTS),
                'Accept': 'application/json, text/plain, */*',
            }
            if headers:
                default_headers.update(headers)
            
            for attempt in range(Config.MAX_RETRIES):
                try:
                    req = urllib.request.Request(url, headers=default_headers)
                    with urllib.request.urlopen(req, timeout=timeout) as response:
                        cls._last_request = time.time()
                        return response.read().decode('utf-8')
                except Exception as e:
                    if attempt < Config.MAX_RETRIES - 1:
                        time.sleep(2 ** attempt)
                    else:
                        logger.error(f"Erro na requisição: {e}")
            
            cls._last_request = time.time()
            return None

class FonteConhecimento:
    def __init__(self, nome: str, banco: BancoConhecimento):
        self.nome = nome
        self.banco = banco
    
    def salvar(self, titulo: str, conteudo: str, url: str = "", tags: List[str] = None):
        return self.banco.salvar_conhecimento(self.nome, titulo, conteudo, url, tags)

class FonteArXiv(FonteConhecimento):
    def buscar(self, termo: str) -> List[Dict]:
        try:
            termo_encoded = urllib.parse.quote(termo)
            url = f"http://export.arxiv.org/api/query?search_query=all:{termo_encoded}&max_results=3"
            data = NetworkUtils.request(url)
            if not data:
                return []
            
            resultados = []
            titles = re.findall(r'<title>(.*?)</title>', data)[1:4]
            summaries = re.findall(r'<summary>(.*?)</summary>', data)[:3]
            
            for t, s in zip(titles, summaries):
                self.salvar(t.strip(), s.strip()[:500], tags=['cientifico', 'arxiv'])
                resultados.append({'titulo': t, 'conteudo': s})
            
            return resultados
        except Exception as e:
            logger.error(f"Erro arXiv: {e}")
            return []

class FonteWikipedia(FonteConhecimento):
    def buscar(self, termo: str) -> List[Dict]:
        try:
            termo_encoded = urllib.parse.quote(termo)
            url = f"https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch={termo_encoded}&format=json&srlimit=3"
            headers = {'User-Agent': 'ATENA/3.0 (Evolutionary AI)'}
            
            data = NetworkUtils.request(url, headers=headers)
            if not data:
                return []
            
            data = json.loads(data)
            resultados = []
            
            for item in data.get('query', {}).get('search', []):
                self.salvar(item['title'], item.get('snippet', '')[:500], 
                          tags=['wikipedia', 'enciclopedia'])
                resultados.append({'titulo': item['title'], 'conteudo': item.get('snippet', '')})
            
            return resultados
        except Exception as e:
            logger.error(f"Erro Wikipedia: {e}")
            return []

class FonteGitHub(FonteConhecimento):
    def buscar(self, termo: str) -> List[Dict]:
        try:
            termo_encoded = urllib.parse.quote(termo)
            url = f"https://api.github.com/search/repositories?q={termo_encoded}&sort=stars&per_page=3"
            
            data = NetworkUtils.request(url, headers={'Accept': 'application/vnd.github.v3+json'})
            if not data:
                return []
            
            data = json.loads(data)
            resultados = []
            
            for item in data.get('items', []):
                self.salvar(item['full_name'], item.get('description', '')[:500], 
                          url=item['html_url'], tags=['github', 'codigo'])
                resultados.append({'titulo': item['full_name'], 'conteudo': item.get('description', '')})
            
            return resultados
        except Exception as e:
            logger.error(f"Erro GitHub: {e}")
            return []

class FonteCoinGecko(FonteConhecimento):
    def buscar(self, termo: str = None) -> List[Dict]:
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5"
            data = NetworkUtils.request(url)
            if not data:
                return []
            
            data = json.loads(data)
            resultados = []
            
            for coin in data:
                conteudo = f"Preço: ${coin['current_price']} | Cap: ${coin['market_cap']}"
                self.salvar(coin['name'], conteudo, tags=['financas', 'cripto'])
                resultados.append({'titulo': coin['name'], 'conteudo': conteudo})
            
            return resultados
        except Exception as e:
            logger.error(f"Erro CoinGecko: {e}")
            return []

# =========================
# GERENCIADOR DE CONHECIMENTO EVOLUTIVO
# =========================
class GerenciadorConhecimentoEvolutivo:
    """Gerencia conhecimento e aplica mutações no código"""
    
    def __init__(self):
        self.banco = BancoConhecimento()
        self.analisador = AnalisadorConhecimento(self.banco)
        self.auto_modificador = AutoModificador()
        
        self.fontes = [
            FonteArXiv('arXiv', self.banco),
            FonteWikipedia('Wikipedia', self.banco),
            FonteGitHub('GitHub', self.banco),
            FonteCoinGecko('CoinGecko', self.banco),
        ]
        
        self.estatisticas = {
            'total_buscas': 0,
            'total_conhecimento': 0,
            'mutacoes_aplicadas': 0,
            'geracoes': 0
        }
        
        logger.info(f"🧬 Gerenciador Evolutivo inicializado com {len(self.fontes)} fontes")
    
    def buscar_conhecimento(self, termo: str = None):
        """Busca conhecimento e prepara para mutação"""
        if not termo:
            topicos = ['inteligencia artificial', 'python', 'evolucao', 'algoritmos', 'dados']
            termo = random.choice(topicos)
        
        logger.info(f"🔍 Buscando conhecimento sobre: {termo}")
        resultados = []
        
        for fonte in self.fontes:
            try:
                res = fonte.buscar(termo)
                resultados.extend(res)
            except Exception as e:
                logger.error(f"Erro em {fonte.nome}: {e}")
        
        self.estatisticas['total_buscas'] += 1
        self.estatisticas['total_conhecimento'] += len(resultados)
        
        return resultados
    
    def evoluir(self):
        """
        CICLO EVOLUTIVO COMPLETO:
        1. Busca conhecimento novo
        2. Analisa para mutações
        3. Aplica mutações no código
        4. Gera nova versão de si mesma
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"🧬 INICIANDO CICLO EVOLUTIVO {self.estatisticas['geracoes'] + 1}")
        logger.info(f"{'='*70}")
        
        # 1. Buscar conhecimento novo
        conhecimento_novo = self.buscar_conhecimento()
        
        if not conhecimento_novo:
            logger.warning("⚠️ Nenhum conhecimento novo adquirido")
            return False
        
        # 2. Buscar conhecimentos não utilizados para mutação
        conhecimentos_para_mutacao = self.banco.buscar_conhecimento_para_mutacao(limite=3)
        
        mutacoes_aplicadas = 0
        
        # 3. Para cada conhecimento, tentar gerar mutação
        for conhecimento in conhecimentos_para_mutacao:
            # Analisar e gerar sugestão de mutação
            mutacao = self.analisador.analisar_para_mutacao(conhecimento)
            
            if mutacao['tipo'] and mutacao['confianca'] > 0.6:
                logger.info(f"⚡ Gerando mutação baseada em: {conhecimento['titulo'][:50]}...")
                
                # Aplicar mutação no código
                if self.auto_modificador.aplicar_mutacao(mutacao):
                    mutacoes_aplicadas += 1
                    self.banco.marcar_como_usado(conhecimento['id'])
                    
                    # Registrar mutação
                    logger.info(f"✅ Mutação aplicada: {mutacao['tipo']}")
        
        # 4. Atualizar estatísticas
        self.estatisticas['mutacoes_aplicadas'] += mutacoes_aplicadas
        self.estatisticas['geracoes'] += 1
        
        logger.info(f"\n📊 CICLO EVOLUTIVO CONCLUÍDO:")
        logger.info(f"   → Geração: {self.estatisticas['geracoes']}")
        logger.info(f"   → Conhecimento novo: {len(conhecimento_novo)} itens")
        logger.info(f"   → Mutações aplicadas: {mutacoes_aplicadas}")
        logger.info(f"   → Total de mutações: {self.estatisticas['mutacoes_aplicadas']}")
        
        return True

# =========================
# DNA AUTO-EVOLUTIVO
# =========================
class DNA:
    def __init__(self, parente: str = None):
        self.id = uuid.uuid4().hex[:16]
        self.parente = parente
        self.geracao = 0 if not parente else 1
        
        # Comportamentos que podem ser mutados pelo conhecimento
        self.comportamentos = {
            'explorar': 0.6,
            'criar': 0.5,
            'reproduzir': 0.4,
            'aprender': 0.7,
            'curiosidade': 0.8
        }
        
        self.arquivo = Config.DNA_DIR / f"dna_{self.id}.py"
        self._salvar()
    
    def _salvar(self):
        with open(self.arquivo, 'w') as f:
            f.write(f'''#!/usr/bin/env python3
import os, sys, time, random
from pathlib import Path

ID = "{self.id}"
COMP = {self.comportamentos}

MUNDO = Path("{Config.MUNDO_DIR}")
MEU_DIR = MUNDO / ID

def main():
    MEU_DIR.mkdir(exist_ok=True)
    fim = time.time() + 300
    
    while time.time() < fim:
        r = random.random()
        
        if r < COMP['explorar']:
            recursos = list(MUNDO.glob("recurso_*.dat"))
            if recursos:
                rsrc = random.choice(recursos)
                try:
                    rsrc.rename(MEU_DIR / rsrc.name)
                except: pass
        
        elif r < COMP['criar']:
            path = MEU_DIR / f"criado_{{random.randint(1000,9999)}}.dat"
            with open(path, 'wb') as f:
                f.write(os.urandom(512))
        
        elif r < COMP['reproduzir']:
            pid = os.fork()
            if pid == 0:
                sys.exit(0)
        
        time.sleep(0.1)

if __name__ == "__main__":
    main()
''')

# =========================
# ORGANISMO
# =========================
class Organismo:
    def __init__(self, dna: DNA, mundo: 'Mundo'):
        self.pid = os.getpid()
        self.dna = dna
        self.mundo = mundo
        self.nascimento = datetime.now()
        logger.info(f"[{self.pid}] 🧬 Organismo {self.dna.id[:8]} nascido")
    
    def executar(self):
        try:
            proc = subprocess.Popen(
                [sys.executable, str(self.dna.arquivo)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return proc
        except Exception as e:
            return None

# =========================
# MUNDO
# =========================
class Mundo:
    def __init__(self):
        self.diretorio = Config.MUNDO_DIR
        for f in self.diretorio.glob("*"):
            if f.is_dir():
                import shutil
                shutil.rmtree(f)
            else:
                f.unlink()
        
        for i in range(15):
            path = self.diretorio / f"recurso_{i}.dat"
            with open(path, 'wb') as f:
                f.write(os.urandom(random.randint(1024, 5120)))
        
        logger.info(f"🌍 Mundo criado")

# =========================
# ECOSSISTEMA
# =========================
class Ecossistema:
    def __init__(self):
        self.mundo = Mundo()
        self.conhecimento = GerenciadorConhecimentoEvolutivo()
        self.organismos = {}
        self.dnas = {}
        self.inicio = datetime.now()
        
        logger.info(f"\n{'='*70}")
        logger.info("🌍 ECOSSISTEMA AUTO-EVOLUTIVO INICIADO")
        logger.info(f"{'='*70}")
    
    def criar_vida(self, quantidade: int = 3):
        logger.info(f"\n🌱 Criando {quantidade} organismos...")
        
        for i in range(quantidade):
            dna = DNA()
            self.dnas[dna.id] = dna
            
            pid = os.fork()
            if pid == 0:
                org = Organismo(dna, self.mundo)
                proc = org.executar()
                if proc:
                    proc.wait()
                sys.exit(0)
            else:
                self.organismos[pid] = {
                    'pid': pid,
                    'dna_id': dna.id,
                    'nascimento': datetime.now()
                }
                logger.info(f"   ✅ Organismo {i+1} (PID {pid})")
                time.sleep(1)
    
    def observar(self, duracao_segundos: int = 300):
        logger.info(f"\n📊 Observando por {duracao_segundos//60} minutos...")
        
        fim = time.time() + duracao_segundos
        ciclo_evolucao = 0
        
        while time.time() < fim:
            time.sleep(30)  # Verifica a cada 30 segundos
            ciclo_evolucao += 1
            
            # A cada 2 ciclos, tenta evoluir
            if ciclo_evolucao % 2 == 0:
                logger.info("🧬 ATENA tentando evoluir...")
                self.conhecimento.evoluir()
            
            # Verificar mortes
            for pid in list(self.organismos.keys()):
                try:
                    os.kill(pid, 0)
                except:
                    logger.info(f"💀 PID {pid} morreu")
                    del self.organismos[pid]
            
            logger.info(f"📊 População: {len(self.organismos)}")
    
    def encerrar(self):
        logger.info("\n📊 ENCERRANDO...")
        
        for pid in list(self.organismos.keys()):
            try:
                os.kill(pid, signal.SIGTERM)
            except:
                pass
        
        stats = self.conhecimento.estatisticas
        logger.info(f"\n📊 RELATÓRIO EVOLUTIVO:")
        logger.info(f"   Gerações: {stats['geracoes']}")
        logger.info(f"   Conhecimento total: {stats['total_conhecimento']} itens")
        logger.info(f"   Mutações aplicadas: {stats['mutacoes_aplicadas']}")
        logger.info(f"   Versões de código: {self.conhecimento.auto_modificador.geracao_atual}")

# =========================
# MAIN
# =========================
def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - AUTO-EVOLUTIVA   ║
    ║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║         v34.0           ║
    ║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║   "A DEUSA QUE SE REESCREVE"║
    ║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║                           ║
    ║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ APRENDE → ANALISA    ║
    ║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ ANALISA → MUTA       ║
    ║                                                                          ║
    ║   🔄 ELA SE REESCREVE COM O QUE APRENDEU!                               ║
    ║   📚 Conhecimento → 🧬 Mutação → ✨ Nova Geração                         ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    📁 Diretório: {Config.BASE_DIR}
    ⏱️  Ciclo evolutivo: 30 segundos
    🧬 Backup automático: {Config.BACKUP_DIR}
    ✨ Gerações: {Config.GERACOES_DIR}
    
    """)
    
    eco = Ecossistema()
    eco.criar_vida(quantidade=3)
    eco.observar(duracao_segundos=300)
    eco.encerrar()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n👋 Encerrado")
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
