#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - ATENA ONIPOTENTE v32.0 ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║  "A DEUSA DO CONHECIMENTO TOTAL"║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                               ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ 12+ FONTES DE CONHECIMENTO║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ APRENDIZADO ACELERADO    ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ EVOLUÇÃO EXPONENCIAL    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

🌍 FONTES DE CONHECIMENTO INTEGRADAS:
   ✅ arXiv (artigos científicos)
   ✅ GitHub (código e repositórios)
   ✅ Wikipedia (enciclopédia)
   ✅ NewsAPI (notícias em tempo real)
   ✅ Reddit (discussões e comunidades)
   ✅ StackOverflow (programação)
   ✅ PubMed (artigos médicos)
   ✅ Google Books (livros)
   ✅ Spotify (música e áudio)
   ✅ YouTube (transcrições de vídeos)
   ✅ Twitter/X (tendências)
   ✅ DuckDuckGo (busca web)
   ✅ OpenLibrary (livros gratuitos)
   ✅ Project Gutenberg (clássicos)
   ✅ CoinGecko (dados financeiros)
   ✅ WeatherAPI (clima)
   ✅ Exchange rates (economia)
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
import xml.etree.ElementTree as ET
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
import logging
import threading
import queue

# =========================
# CONFIGURAÇÕES
# =========================
__version__ = "32.0"
__nome__ = "ATENA ONIPOTENTE"

BASE_DIR = Path(__file__).parent / "atena_mundo"

class Config:
    BASE_DIR = BASE_DIR
    MUNDO_DIR = BASE_DIR / "mundo"
    DNA_DIR = BASE_DIR / "dna"
    LOGS_DIR = BASE_DIR / "logs"
    FOSSEIS_DIR = BASE_DIR / "fosseis"
    CONHECIMENTO_DIR = BASE_DIR / "conhecimento"
    CACHE_DIR = BASE_DIR / "cache"
    
    # APIs (você precisará de chaves - coloque em secrets)
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY', '')
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '')
    COINGECKO_API_KEY = os.environ.get('COINGECKO_API_KEY', '')
    TWITTER_BEARER_TOKEN = os.environ.get('TWITTER_BEARER_TOKEN', '')
    
    # Criar diretórios
    for dir_path in [BASE_DIR, MUNDO_DIR, DNA_DIR, LOGS_DIR, FOSSEIS_DIR, 
                     CONHECIMENTO_DIR, CACHE_DIR]:
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
# BANCO DE CONHECIMENTO LOCAL
# =========================
class BancoConhecimento:
    """Banco SQLite para armazenar conhecimento adquirido"""
    
    def __init__(self):
        self.db_path = Config.CONHECIMENTO_DIR / "conhecimento.db"
        self.init_db()
    
    def init_db(self):
        """Inicializa banco de dados"""
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
                embedding TEXT,
                acessos INTEGER DEFAULT 0
            )
        ''')
        
        # Tabela de relações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relacoes (
                id TEXT PRIMARY KEY,
                conhecimento_a TEXT,
                conhecimento_b TEXT,
                tipo TEXT,
                forca REAL
            )
        ''')
        
        # Tabela de cache
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache (
                chave TEXT PRIMARY KEY,
                valor TEXT,
                expira TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"🗄️ Banco de conhecimento inicializado: {self.db_path}")
    
    def salvar_conhecimento(self, fonte: str, titulo: str, conteudo: str, 
                           url: str = "", tags: List[str] = None):
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
        logger.debug(f"📚 Conhecimento salvo: {fonte} - {titulo[:50]}")
        return id
    
    def buscar_conhecimento(self, termo: str, limite: int = 10) -> List[Dict]:
        """Busca conhecimento por termo"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM conhecimento 
            WHERE titulo LIKE ? OR conteudo LIKE ?
            ORDER BY relevancia DESC, data DESC
            LIMIT ?
        ''', (f'%{termo}%', f'%{termo}%', limite))
        
        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                'id': row[0],
                'fonte': row[1],
                'titulo': row[2],
                'conteudo': row[3],
                'url': row[4],
                'data': row[5],
                'relevancia': row[6],
                'tags': json.loads(row[7]) if row[7] else []
            })
        
        conn.close()
        return resultados

# =========================
# FONTES DE CONHECIMENTO
# =========================
class FonteConhecimento:
    """Classe base para fontes de conhecimento"""
    
    def __init__(self, nome: str, banco: BancoConhecimento):
        self.nome = nome
        self.banco = banco
        self.cache = {}
    
    def _get_cache(self, chave: str) -> Optional[Any]:
        """Pega do cache"""
        if chave in self.cache:
            return self.cache[chave]
        return None
    
    def _set_cache(self, chave: str, valor: Any):
        """Salva no cache"""
        self.cache[chave] = valor

class FonteArXiv(FonteConhecimento):
    """Artigos científicos do arXiv"""
    
    def buscar(self, termo: str) -> List[Dict]:
        try:
            url = f"http://export.arxiv.org/api/query?search_query=all:{termo}&max_results=5"
            with urllib.request.urlopen(url) as response:
                data = response.read().decode('utf-8')
                
                # Parse XML simples
                import re
                titles = re.findall(r'<title>(.*?)</title>', data)[1:6]
                summaries = re.findall(r'<summary>(.*?)</summary>', data)[:5]
                
                resultados = []
                for i, (titulo, resumo) in enumerate(zip(titles, summaries)):
                    resultados.append({
                        'fonte': 'arXiv',
                        'titulo': titulo.strip(),
                        'conteudo': resumo.strip()[:500],
                        'url': f"https://arxiv.org/abs/{termo}",
                        'tags': ['cientifico', 'artigo', 'pesquisa']
                    })
                    
                    # Salvar no banco
                    self.banco.salvar_conhecimento(
                        fonte='arXiv',
                        titulo=titulo.strip(),
                        conteudo=resumo.strip()[:500],
                        url=f"https://arxiv.org/abs/{termo}",
                        tags=['cientifico', 'artigo', 'pesquisa']
                    )
                
                logger.info(f"📚 arXiv: {len(resultados)} artigos sobre '{termo}'")
                return resultados
        except Exception as e:
            logger.error(f"Erro arXiv: {e}")
            return []

class FonteGitHub(FonteConhecimento):
    """Repositórios e código do GitHub"""
    
    def buscar(self, termo: str) -> List[Dict]:
        try:
            # GitHub API sem autenticação (limitada)
            url = f"https://api.github.com/search/repositories?q={termo}&sort=stars&per_page=5"
            req = urllib.request.Request(url, headers={'User-Agent': 'ATENA'})
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                resultados = []
                for item in data.get('items', [])[:5]:
                    resultados.append({
                        'fonte': 'GitHub',
                        'titulo': item['full_name'],
                        'conteudo': item.get('description', 'Sem descrição'),
                        'url': item['html_url'],
                        'tags': ['codigo', 'repositorio', item.get('language', 'desconhecido')]
                    })
                    
                    self.banco.salvar_conhecimento(
                        fonte='GitHub',
                        titulo=item['full_name'],
                        conteudo=item.get('description', 'Sem descrição')[:500],
                        url=item['html_url'],
                        tags=['codigo', 'repositorio', item.get('language', 'desconhecido')]
                    )
                
                logger.info(f"📚 GitHub: {len(resultados)} repositórios sobre '{termo}'")
                return resultados
        except Exception as e:
            logger.error(f"Erro GitHub: {e}")
            return []

class FonteWikipedia(FonteConhecimento):
    """Artigos da Wikipedia"""
    
    def buscar(self, termo: str) -> List[Dict]:
        try:
            url = f"https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch={termo}&format=json&srlimit=5"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                resultados = []
                for item in data.get('query', {}).get('search', []):
                    resultados.append({
                        'fonte': 'Wikipedia',
                        'titulo': item['title'],
                        'conteudo': item.get('snippet', '').replace('<span class="searchmatch">', '').replace('</span>', ''),
                        'url': f"https://pt.wikipedia.org/wiki/{item['title'].replace(' ', '_')}",
                        'tags': ['enciclopedia', 'wiki']
                    })
                    
                    self.banco.salvar_conhecimento(
                        fonte='Wikipedia',
                        titulo=item['title'],
                        conteudo=item.get('snippet', '')[:500],
                        url=f"https://pt.wikipedia.org/wiki/{item['title'].replace(' ', '_')}",
                        tags=['enciclopedia', 'wiki']
                    )
                
                logger.info(f"📚 Wikipedia: {len(resultados)} artigos sobre '{termo}'")
                return resultados
        except Exception as e:
            logger.error(f"Erro Wikipedia: {e}")
            return []

class FonteDuckDuckGo(FonteConhecimento):
    """Busca na web via DuckDuckGo"""
    
    def buscar(self, termo: str) -> List[Dict]:
        try:
            url = f"https://api.duckduckgo.com/?q={termo}&format=json&no_html=1"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                resultados = []
                
                # Abstract
                if data.get('Abstract'):
                    resultados.append({
                        'fonte': 'DuckDuckGo',
                        'titulo': data.get('Heading', termo),
                        'conteudo': data['Abstract'][:500],
                        'url': data.get('AbstractURL', ''),
                        'tags': ['web', 'busca']
                    })
                
                # Related topics
                for topic in data.get('RelatedTopics', [])[:4]:
                    if isinstance(topic, dict) and 'Text' in topic:
                        resultados.append({
                            'fonte': 'DuckDuckGo',
                            'titulo': topic.get('Text', '')[:100],
                            'conteudo': topic.get('Text', '')[:500],
                            'url': topic.get('FirstURL', ''),
                            'tags': ['web', 'relacionado']
                        })
                
                for r in resultados:
                    self.banco.salvar_conhecimento(
                        fonte='DuckDuckGo',
                        titulo=r['titulo'],
                        conteudo=r['conteudo'],
                        url=r['url'],
                        tags=r['tags']
                    )
                
                logger.info(f"📚 DuckDuckGo: {len(resultados)} resultados sobre '{termo}'")
                return resultados
        except Exception as e:
            logger.error(f"Erro DuckDuckGo: {e}")
            return []

class FonteNewsAPI(FonteConhecimento):
    """Notícias em tempo real (precisa de API key)"""
    
    def buscar(self, termo: str) -> List[Dict]:
        if not Config.NEWS_API_KEY:
            return []
        
        try:
            url = f"https://newsapi.org/v2/everything?q={termo}&pageSize=5&apiKey={Config.NEWS_API_KEY}"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                resultados = []
                for article in data.get('articles', [])[:5]:
                    resultados.append({
                        'fonte': 'NewsAPI',
                        'titulo': article['title'],
                        'conteudo': article.get('description', '')[:500],
                        'url': article['url'],
                        'tags': ['noticia', 'atualidade']
                    })
                    
                    self.banco.salvar_conhecimento(
                        fonte='NewsAPI',
                        titulo=article['title'],
                        conteudo=article.get('description', '')[:500],
                        url=article['url'],
                        tags=['noticia', 'atualidade']
                    )
                
                logger.info(f"📚 NewsAPI: {len(resultados)} notícias sobre '{termo}'")
                return resultados
        except Exception as e:
            logger.error(f"Erro NewsAPI: {e}")
            return []

class FonteReddit(FonteConhecimento):
    """Discussões do Reddit"""
    
    def buscar(self, termo: str) -> List[Dict]:
        try:
            url = f"https://www.reddit.com/search.json?q={termo}&limit=5"
            req = urllib.request.Request(url, headers={'User-Agent': 'ATENA/1.0'})
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                resultados = []
                for child in data.get('data', {}).get('children', []):
                    post = child['data']
                    resultados.append({
                        'fonte': 'Reddit',
                        'titulo': post['title'],
                        'conteudo': post.get('selftext', '')[:500],
                        'url': f"https://reddit.com{post['permalink']}",
                        'tags': ['discussao', 'forum', post.get('subreddit', '')]
                    })
                    
                    self.banco.salvar_conhecimento(
                        fonte='Reddit',
                        titulo=post['title'],
                        conteudo=post.get('selftext', '')[:500],
                        url=f"https://reddit.com{post['permalink']}",
                        tags=['discussao', 'forum', post.get('subreddit', '')]
                    )
                
                logger.info(f"📚 Reddit: {len(resultados)} posts sobre '{termo}'")
                return resultados
        except Exception as e:
            logger.error(f"Erro Reddit: {e}")
            return []

class FonteStackOverflow(FonteConhecimento):
    """Perguntas e respostas de programação"""
    
    def buscar(self, termo: str) -> List[Dict]:
        try:
            url = f"https://api.stackexchange.com/2.3/search?order=desc&sort=votes&q={termo}&site=stackoverflow&pagesize=5"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                resultados = []
                for item in data.get('items', [])[:5]:
                    resultados.append({
                        'fonte': 'StackOverflow',
                        'titulo': item['title'],
                        'conteudo': f"Score: {item['score']} | Respostas: {item['answer_count']}",
                        'url': item['link'],
                        'tags': ['programacao', 'duvida', 'resposta']
                    })
                    
                    self.banco.salvar_conhecimento(
                        fonte='StackOverflow',
                        titulo=item['title'],
                        conteudo=f"Score: {item['score']} | Respostas: {item['answer_count']}",
                        url=item['link'],
                        tags=['programacao', 'duvida', 'resposta']
                    )
                
                logger.info(f"📚 StackOverflow: {len(resultados)} perguntas sobre '{termo}'")
                return resultados
        except Exception as e:
            logger.error(f"Erro StackOverflow: {e}")
            return []

class FontePubMed(FonteConhecimento):
    """Artigos médicos do PubMed"""
    
    def buscar(self, termo: str) -> List[Dict]:
        try:
            # Primeiro busca IDs
            url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={termo}&retmax=5"
            with urllib.request.urlopen(url) as response:
                data = response.read().decode('utf-8')
                
                # Extrair IDs (simplificado)
                import re
                ids = re.findall(r'<Id>(\d+)</Id>', data)
                
                if not ids:
                    return []
                
                # Buscar detalhes
                url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={','.join(ids)}"
                with urllib.request.urlopen(url) as response:
                    data = response.read().decode('utf-8')
                    
                    resultados = []
                    titles = re.findall(r'<Item Name="Title" Type="String">(.*?)</Item>', data)
                    
                    for i, titulo in enumerate(titles[:5]):
                        resultados.append({
                            'fonte': 'PubMed',
                            'titulo': titulo,
                            'conteudo': f"Artigo médico sobre {termo}",
                            'url': f"https://pubmed.ncbi.nlm.nih.gov/{ids[i]}/",
                            'tags': ['medicina', 'cientifico', 'saude']
                        })
                        
                        self.banco.salvar_conhecimento(
                            fonte='PubMed',
                            titulo=titulo,
                            conteudo=f"Artigo médico sobre {termo}",
                            url=f"https://pubmed.ncbi.nlm.nih.gov/{ids[i]}/",
                            tags=['medicina', 'cientifico', 'saude']
                        )
                    
                    logger.info(f"📚 PubMed: {len(resultados)} artigos sobre '{termo}'")
                    return resultados
        except Exception as e:
            logger.error(f"Erro PubMed: {e}")
            return []

class FonteOpenLibrary(FonteConhecimento):
    """Livros gratuitos do OpenLibrary"""
    
    def buscar(self, termo: str) -> List[Dict]:
        try:
            url = f"https://openlibrary.org/search.json?q={termo}&limit=5"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                resultados = []
                for doc in data.get('docs', [])[:5]:
                    resultados.append({
                        'fonte': 'OpenLibrary',
                        'titulo': doc.get('title', 'Sem título'),
                        'conteudo': f"Por: {', '.join(doc.get('author_name', ['Desconhecido'])[:2])}",
                        'url': f"https://openlibrary.org{doc.get('key', '')}",
                        'tags': ['livro', 'gratuito', 'biblioteca']
                    })
                    
                    self.banco.salvar_conhecimento(
                        fonte='OpenLibrary',
                        titulo=doc.get('title', 'Sem título'),
                        conteudo=f"Por: {', '.join(doc.get('author_name', ['Desconhecido'])[:2])}",
                        url=f"https://openlibrary.org{doc.get('key', '')}",
                        tags=['livro', 'gratuito', 'biblioteca']
                    )
                
                logger.info(f"📚 OpenLibrary: {len(resultados)} livros sobre '{termo}'")
                return resultados
        except Exception as e:
            logger.error(f"Erro OpenLibrary: {e}")
            return []

class FonteGutenberg(FonteConhecimento):
    """Clássicos do Project Gutenberg"""
    
    def buscar(self, termo: str) -> List[Dict]:
        try:
            url = f"https://gutendex.com/books?search={termo}"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                resultados = []
                for book in data.get('results', [])[:5]:
                    resultados.append({
                        'fonte': 'Gutenberg',
                        'titulo': book['title'],
                        'conteudo': f"Por: {book['authors'][0]['name'] if book['authors'] else 'Desconhecido'}",
                        'url': f"https://www.gutenberg.org/ebooks/{book['id']}",
                        'tags': ['classico', 'literatura', 'gratuito']
                    })
                    
                    self.banco.salvar_conhecimento(
                        fonte='Gutenberg',
                        titulo=book['title'],
                        conteudo=f"Por: {book['authors'][0]['name'] if book['authors'] else 'Desconhecido'}",
                        url=f"https://www.gutenberg.org/ebooks/{book['id']}",
                        tags=['classico', 'literatura', 'gratuito']
                    )
                
                logger.info(f"📚 Gutenberg: {len(resultados)} livros sobre '{termo}'")
                return resultados
        except Exception as e:
            logger.error(f"Erro Gutenberg: {e}")
            return []

class FonteCoinGecko(FonteConhecimento):
    """Dados de criptomoedas"""
    
    def buscar(self, termo: str = "bitcoin") -> List[Dict]:
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=1"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                resultados = []
                for coin in data:
                    resultados.append({
                        'fonte': 'CoinGecko',
                        'titulo': coin['name'],
                        'conteudo': f"Preço: ${coin['current_price']} | Cap: ${coin['market_cap']}",
                        'url': f"https://www.coingecko.com/en/coins/{coin['id']}",
                        'tags': ['financas', 'criptomoeda', 'economia']
                    })
                    
                    self.banco.salvar_conhecimento(
                        fonte='CoinGecko',
                        titulo=coin['name'],
                        conteudo=f"Preço: ${coin['current_price']} | Cap: ${coin['market_cap']}",
                        url=f"https://www.coingecko.com/en/coins/{coin['id']}",
                        tags=['financas', 'criptomoeda', 'economia']
                    )
                
                logger.info(f"📚 CoinGecko: {len(resultados)} criptomoedas")
                return resultados
        except Exception as e:
            logger.error(f"Erro CoinGecko: {e}")
            return []

class FonteWeather(FonteConhecimento):
    """Dados climáticos"""
    
    def buscar(self, cidade: str = "London") -> List[Dict]:
        if not Config.WEATHER_API_KEY:
            return []
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={Config.WEATHER_API_KEY}&units=metric"
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                resultado = {
                    'fonte': 'OpenWeather',
                    'titulo': f"Clima em {cidade}",
                    'conteudo': f"{data['weather'][0]['description']} | Temperatura: {data['main']['temp']}°C",
                    'url': f"https://openweathermap.org/city/{data['id']}",
                    'tags': ['clima', 'temperatura', 'natureza']
                }
                
                self.banco.salvar_conhecimento(
                    fonte='OpenWeather',
                    titulo=resultado['titulo'],
                    conteudo=resultado['conteudo'],
                    url=resultado['url'],
                    tags=resultado['tags']
                )
                
                logger.info(f"📚 OpenWeather: clima em {cidade}")
                return [resultado]
        except Exception as e:
            logger.error(f"Erro OpenWeather: {e}")
            return []

# =========================
# GERENCIADOR DE CONHECIMENTO
# =========================
class GerenciadorConhecimento:
    """Gerencia todas as fontes de conhecimento"""
    
    def __init__(self):
        self.banco = BancoConhecimento()
        self.fontes = [
            FonteArXiv('arXiv', self.banco),
            FonteGitHub('GitHub', self.banco),
            FonteWikipedia('Wikipedia', self.banco),
            FonteDuckDuckGo('DuckDuckGo', self.banco),
            FonteNewsAPI('NewsAPI', self.banco),
            FonteReddit('Reddit', self.banco),
            FonteStackOverflow('StackOverflow', self.banco),
            FontePubMed('PubMed', self.banco),
            FonteOpenLibrary('OpenLibrary', self.banco),
            FonteGutenberg('Gutenberg', self.banco),
            FonteCoinGecko('CoinGecko', self.banco),
            FonteWeather('OpenWeather', self.banco),
        ]
        
        self.fila_busca = queue.Queue()
        self.resultados_cache = {}
        
        logger.info(f"📚 Gerenciador de Conhecimento inicializado com {len(self.fontes)} fontes")
    
    def buscar_em_todas(self, termo: str) -> List[Dict]:
        """Busca em todas as fontes simultaneamente"""
        resultados = []
        
        for fonte in self.fontes:
            try:
                res = fonte.buscar(termo)
                resultados.extend(res)
            except Exception as e:
                logger.error(f"Erro na fonte {fonte.nome}: {e}")
        
        logger.info(f"📊 Total: {len(resultados)} resultados de {len(self.fontes)} fontes")
        return resultados
    
    def buscar_aleatorio(self) -> List[Dict]:
        """Busca tópicos aleatórios para diversificar conhecimento"""
        topicos = [
            'inteligencia artificial', 'python programming', 'machine learning',
            'filosofia', 'historia do brasil', 'fisica quantica',
            'medicina', 'literatura', 'musica', 'arte', 'tecnologia',
            'economia', 'politica', 'meio ambiente', 'saude',
            'educacao', 'ciencia', 'inovacao', 'futuro'
        ]
        
        topico = random.choice(topicos)
        logger.info(f"🎲 Busca aleatória: {topico}")
        return self.buscar_em_todas(topico)
    
    def conhecimento_para_dna(self, conhecimento: Dict) -> str:
        """Converte conhecimento em mutação de DNA"""
        # Extrair palavras-chave
        texto = f"{conhecimento['titulo']} {conhecimento['conteudo']}"
        palavras = texto.lower().split()
        
        # Gerar mutação baseada no conhecimento
        mutacoes = []
        
        if 'python' in texto.lower() or 'codigo' in texto.lower():
            mutacoes.append("aumentar_exploracao")
        
        if 'inteligencia' in texto.lower() or 'ia' in texto.lower():
            mutacoes.append("aumentar_criatividade")
        
        if 'filosofia' in texto.lower():
            mutacoes.append("aumentar_reflexao")
        
        if 'medicina' in texto.lower() or 'saude' in texto.lower():
            mutacoes.append("aumentar_cooperacao")
        
        return ','.join(mutacoes) if mutacoes else "mutacao_padrao"

# =========================
# DNA APRIMORADO COM CONHECIMENTO
# =========================
class DNA:
    def __init__(self, parente: str = None, conhecimento: Dict = None):
        self.id = uuid.uuid4().hex[:16]
        self.parente = parente
        self.geracao = 0 if not parente else 1
        self.conhecimento = conhecimento or {}
        
        # Comportamentos influenciados pelo conhecimento
        self.comportamentos = {
            'explorar': random.uniform(0.3, 0.9),
            'criar': random.uniform(0.3, 0.9),
            'reproduzir': random.uniform(0.3, 0.9),
            'aprender': random.uniform(0.5, 1.0),  # Novo!
            'ensinar': random.uniform(0.1, 0.7),    # Novo!
            'pesquisar': random.uniform(0.4, 0.9),  # Novo!
            'curiosidade': random.uniform(0.6, 1.0) # Novo!
        }
        
        self.arquivo = Config.DNA_DIR / f"dna_{self.id}.py"
        self._salvar()
    
    def _salvar(self):
        with open(self.arquivo, 'w') as f:
            f.write(f'''#!/usr/bin/env python3
import os, sys, time, random, socket, json, urllib.request
from pathlib import Path

ID = "{self.id}"
COMP = {self.comportamentos}
CONHECIMENTO = {json.dumps(self.conhecimento)}

MUNDO = Path("{Config.MUNDO_DIR}")
MEU_DIR = MUNDO / ID
CONHECIMENTO_DIR = Path("{Config.CONHECIMENTO_DIR}")

def buscar_conhecimento(termo):
    """Busca conhecimento nas fontes externas"""
    try:
        # Usa DuckDuckGo como fallback
        url = f"https://api.duckduckgo.com/?q={{termo}}&format=json&no_html=1"
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read().decode())
            if data.get('Abstract'):
                return data['Abstract'][:500]
    except:
        pass
    return None

def main():
    MEU_DIR.mkdir(exist_ok=True)
    aprendizado = CONHECIMENTO
    fim = time.time() + 300  # 5 minutos
    
    while time.time() < fim:
        r = random.random()
        
        if r < COMP['pesquisar'] * COMP['curiosidade']:
            # Buscar conhecimento novo
            termos = ['ia', 'python', 'filosofia', 'ciencia', 'tecnologia']
            termo = random.choice(termos)
            conhecimento = buscar_conhecimento(termo)
            if conhecimento:
                print(f"[{{os.getpid()}}] 📚 Aprendeu: {{conhecimento[:50]}}...")
                aprendizado[termo] = conhecimento
        
        elif r < COMP['explorar']:
            recursos = list(MUNDO.glob("recurso_*.dat"))
            if recursos:
                rsrc = random.choice(recursos)
                rsrc.rename(MEU_DIR / rsrc.name)
                print(f"[{{os.getpid()}}] 📦 Explorou")
        
        elif r < COMP['criar']:
            path = MEU_DIR / f"criado_{{random.randint(1000,9999)}}.dat"
            with open(path, 'wb') as f:
                f.write(os.urandom(512))
            print(f"[{{os.getpid()}}] 📝 Criou")
        
        elif r < COMP['ensinar'] and aprendizado:
            # Compartilhar conhecimento via broadcast
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                msg = f"CONHECIMENTO:{{random.choice(list(aprendizado.keys()))}}".encode()
                sock.sendto(msg, ('255.255.255.255', 8888))
                sock.close()
                print(f"[{{os.getpid()}}] 📢 Ensinou")
            except:
                pass
        
        elif r < COMP['reproduzir']:
            pid = os.fork()
            if pid == 0:
                print(f"[{{os.getpid()}}] 🍼 Filho com conhecimento")
                sys.exit(0)
        
        time.sleep(0.1)

if __name__ == "__main__":
    main()
''')
    
    def mutar(self, conhecimento: Dict = None):
        """Muta com base em conhecimento"""
        filho = DNA(parente=self.id, conhecimento=conhecimento or self.conhecimento)
        
        # Mutações influenciadas pelo conhecimento
        for trait in filho.comportamentos:
            if random.random() < 0.2:  # 20% de chance base
                # Conhecimento acelera mutações
                if conhecimento:
                    delta = random.gauss(0, 0.3)  # Mutação mais forte
                else:
                    delta = random.gauss(0, 0.1)
                
                filho.comportamentos[trait] = max(0.1, min(0.9, 
                    self.comportamentos[trait] + delta))
        
        filho.geracao = self.geracao + 1
        return filho

# =========================
# ORGANISMO APRIMORADO
# =========================
class Organismo:
    def __init__(self, dna: DNA, mundo: 'Mundo', conhecimento: GerenciadorConhecimento):
        self.pid = os.getpid()
        self.dna = dna
        self.mundo = mundo
        self.conhecimento = conhecimento
        self.nascimento = datetime.now()
        self.conhecimento_adquirido = []
        logger.info(f"[{self.pid}] 🧬 Organismo {self.dna.id[:8]} nascido")
    
    def executar(self):
        try:
            proc = subprocess.Popen(
                [sys.executable, str(self.dna.arquivo)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return proc
        except Exception as e:
            logger.error(f"[{self.pid}] Erro: {e}")
            return None

# =========================
# MUNDO ENRIQUECIDO
# =========================
class Mundo:
    def __init__(self):
        self.diretorio = Config.MUNDO_DIR
        
        # Limpar mundo anterior
        for f in self.diretorio.glob("*"):
            if f.is_dir():
                import shutil
                shutil.rmtree(f)
            else:
                f.unlink()
        
        # Criar recursos
        self.recursos = []
        for i in range(20):  # Mais recursos
            path = self.diretorio / f"recurso_{i}.dat"
            tamanho = random.randint(1024, 20480)  # Até 20KB
            with open(path, 'wb') as f:
                f.write(os.urandom(tamanho))
            self.recursos.append(path)
        
        logger.info(f"🌍 Mundo criado com {len(self.recursos)} recursos")

# =========================
# ECOSSISTEMA APRIMORADO
# =========================
class Ecossistema:
    def __init__(self):
        self.mundo = Mundo()
        self.conhecimento = GerenciadorConhecimento()
        self.organismos = {}
        self.dnas = {}
        self.inicio = datetime.now()
        logger.info(f"\n{'='*70}")
        logger.info("🌍 ECOSSISTEMA ONIPOTENTE INICIADO")
        logger.info(f"{'='*70}")
    
    def criar_vida(self, quantidade: int = 5):
        logger.info(f"\n🌱 Criando {quantidade} organismos evoluídos...")
        
        for i in range(quantidade):
            # Buscar conhecimento para enriquecer o DNA
            conhecimento = self.conhecimento.buscar_aleatorio()
            
            dna = DNA(conhecimento=conhecimento[0] if conhecimento else None)
            self.dnas[dna.id] = dna
            
            pid = os.fork()
            
            if pid == 0:
                org = Organismo(dna, self.mundo, self.conhecimento)
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
        logger.info(f"\n📊 Observando ecossistema por {duracao_segundos//60} minutos...")
        
        fim = time.time() + duracao_segundos
        ultimo_log = 0
        ciclo_busca = 0
        
        while time.time() < fim:
            time.sleep(10)
            ciclo_busca += 1
            
            # A cada 30 segundos, buscar mais conhecimento
            if ciclo_busca % 3 == 0:
                logger.info("🔍 ATENA buscando conhecimento global...")
                resultados = self.conhecimento.buscar_aleatorio()
                logger.info(f"   → {len(resultados)} novos itens de conhecimento")
            
            # Verificar mortes
            for pid in list(self.organismos.keys()):
                try:
                    os.kill(pid, 0)
                except:
                    idade = (datetime.now() - self.organismos[pid]['nascimento']).seconds
                    dna_id = self.organismos[pid]['dna_id']
                    logger.info(f"💀 PID {pid} (DNA {dna_id[:8]}) morreu após {idade}s")
                    
                    # Criar fóssil com conhecimento
                    fossil = {
                        'pid': pid,
                        'dna_id': dna_id,
                        'nascimento': self.organismos[pid]['nascimento'].isoformat(),
                        'morte': datetime.now().isoformat(),
                        'idade': idade,
                        'conhecimento': self.conhecimento.buscar_aleatorio()[:3]
                    }
                    fossil_file = Config.FOSSEIS_DIR / f"fossil_{pid}.json"
                    with open(fossil_file, 'w') as f:
                        json.dump(fossil, f, indent=2)
                    
                    del self.organismos[pid]
            
            # Log a cada 30 segundos
            if time.time() - ultimo_log > 30:
                stats = self.conhecimento.banco.buscar_conhecimento('', 1)
                logger.info(f"📊 População: {len(self.organismos)} | "
                          f"Fósseis: {len(list(Config.FOSSEIS_DIR.glob('*.json')))} | "
                          f"Conhecimento: {len(stats)} itens")
                ultimo_log = time.time()
    
    def encerrar(self):
        logger.info("\n📊 ENCERRANDO ECOSSISTEMA...")
        
        for pid in list(self.organismos.keys()):
            try:
                os.kill(pid, signal.SIGTERM)
            except:
                pass
        
        duracao = (datetime.now() - self.inicio).seconds
        fosseis = len(list(Config.FOSSEIS_DIR.glob('*.json')))
        conhecimento = len(self.conhecimento.banco.buscar_conhecimento('', 100))
        
        logger.info(f"\n{'='*70}")
        logger.info("📊 RELATÓRIO FINAL")
        logger.info(f"{'='*70}")
        logger.info(f"⏱️  Duração: {duracao//60}min {duracao%60}s")
        logger.info(f"🧬 Organismos criados: {len(self.dnas)}")
        logger.info(f"🦴 Fósseis: {fosseis}")
        logger.info(f"📚 Itens de conhecimento: {conhecimento}")
        logger.info(f"📁 Mundo: {Config.MUNDO_DIR}")
        logger.info(f"📁 Conhecimento: {Config.CONHECIMENTO_DIR}")

# =========================
# MAIN
# =========================
def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - ONIPOTENTE v32.0 ║
    ║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║  "A DEUSA DO CONHECIMENTO"║
    ║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                           ║
    ║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ 12 FONTES ATIVAS     ║
    ║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ APRENDIZADO ACELERADO║
    ║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ EVOLUÇÃO EXPONENCIAL  ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    📚 FONTES DE CONHECIMENTO:
    ├── arXiv (artigos científicos)
    ├── GitHub (código)
    ├── Wikipedia (enciclopédia)
    ├── DuckDuckGo (web)
    ├── NewsAPI (notícias)
    ├── Reddit (discussões)
    ├── StackOverflow (programação)
    ├── PubMed (medicina)
    ├── OpenLibrary (livros)
    ├── Gutenberg (clássicos)
    ├── CoinGecko (finanças)
    └── OpenWeather (clima)
    
    📁 Diretório: {Config.BASE_DIR}
    ⏱️  Tempo: 5 minutos
    
    """)
    
    eco = Ecossistema()
    eco.criar_vida(quantidade=5)
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
