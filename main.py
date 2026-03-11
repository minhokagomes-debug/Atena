#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████╗     Ω - VERSÃO AUTO-EVOLUTIVA  ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██╗                               ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║   "Aprendendo e evoluindo     ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║    em tempo real"             ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║                               ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝                               ║
║                                                                               ║
║                    🧠 Auto-Evolução por Aprendizado Contínuo                 ║
║                          (ACAE - Autonomous Continuous Auto-Evolution)       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

ATENA Ω - Sistema de IA Auto-Evolutiva
Criado em: Março 2026
Versão: 2.0.0 (Auto-Evolutiva)

Este sistema é capaz de:
    📚 Aprender continuamente da internet
    📊 Analisar sua própria performance
    💡 Propor melhorias no seu código
    🧪 Testar modificações em sandbox
    🚀 Aplicar evoluções bem-sucedidas
    📝 Manter histórico completo de evoluções
"""

import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import json
import hashlib
from dataclasses import dataclass, field, asdict
from collections import defaultdict, deque
import logging
import redis.asyncio as redis
from tenacity import retry, stop_after_attempt, wait_exponential
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
import statistics
import psutil
import os
import sys
import ast
import black
import traceback
from enum import Enum
import pickle
import gc

# =========================
# Configuração de Logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('ATENA-Ω')

# Suprime logs muito verbosos
logging.getLogger('asyncio').setLevel(logging.WARNING)
logging.getLogger('aiohttp').setLevel(logging.WARNING)

# =========================
# Configurações Avançadas
# =========================
@dataclass
class Config:
    """Configurações centralizadas com suporte a variáveis de ambiente"""
    REDIS_URL: str = os.getenv('REDIS_URL', "redis://localhost:6379")
    MAX_RETRIES: int = int(os.getenv('MAX_RETRIES', '3'))
    TIMEOUT: int = int(os.getenv('TIMEOUT', '30'))
    USER_AGENT: str = "ATENA-Ω/2.0 (Auto-Evolutiva; +https://github.com/atena-omega)"
    CACHE_TTL: int = int(os.getenv('CACHE_TTL', '3600'))
    MAX_CONCURRENT_REQUESTS: int = int(os.getenv('MAX_CONCURRENT', '10'))
    EVOLUTION_THRESHOLD: float = float(os.getenv('EVOLUTION_THRESHOLD', '0.7'))
    MAX_EVOLUTIONS_PER_DAY: int = int(os.getenv('MAX_EVOLUTIONS', '5'))
    SANDBOX_MEMORY_LIMIT: int = int(os.getenv('SANDBOX_MEMORY', '500'))  # MB
    AUTO_COMMIT: bool = os.getenv('AUTO_COMMIT', 'True').lower() == 'true'
    
    def __post_init__(self):
        logger.info(f"⚙️ Configurações carregadas: Redis={self.REDIS_URL}, "
                   f"Timeout={self.TIMEOUT}s, Evoluções/dia={self.MAX_EVOLUTIONS_PER_DAY}")

# =========================
# Enums e Constantes
# =========================
class OrigemConhecimento(Enum):
    """Fontes de conhecimento da ATENA"""
    NOTICIA = "noticia"
    WIKIPEDIA = "wikipedia"
    GITHUB = "github"
    GITHUB_ISSUE = "github_issue"
    BLOG = "blog"
    PAPER = "paper"
    FORUM = "forum"
    API = "api"
    
class TipoEvolucao(Enum):
    """Tipos de evolução possíveis"""
    CACHE = "cache"
    HEURISTICA = "heuristica"
    FONTE = "fonte"
    PARSER = "parser"
    ARQUITETURA = "arquitetura"
    OTIMIZACAO = "otimizacao"

# =========================
# Fontes de Dados Dinâmicas
# =========================
NEWS_FEEDS = [
    {
        "nome": "Currents API",
        "url": "https://api.currentsapi.services/v1/latest-news",
        "params": {"apiKey": "SEU_API_KEY", "language": "pt", "category": "technology"},
        "parser": lambda x: x.get("news", []),
        "peso": 1.0,
        "ativa": True
    },
    {
        "nome": "NewsAPI",
        "url": "https://newsapi.org/v2/everything",
        "params": {"apiKey": "SEU_API_KEY", "q": "inteligência artificial OR machine learning OR IA", 
                  "language": "pt", "sortBy": "publishedAt"},
        "parser": lambda x: x.get("articles", []),
        "peso": 1.0,
        "ativa": True
    },
    {
        "nome": "Hacker News (Tech)",
        "url": "https://hacker-news.firebaseio.com/v0/topstories.json",
        "parser": lambda x: [{"id": item_id} for item_id in x[:30]],
        "peso": 0.8,
        "ativa": True
    }
]

WIKI_TOPICS = [
    {"title": "Inteligência Artificial", "depth": 3, "lang": "pt"},
    {"title": "Computação Quântica", "depth": 2, "lang": "pt"},
    {"title": "Redes Neurais Artificiais", "depth": 2, "lang": "pt"},
    {"title": "Aprendizado Profundo", "depth": 2, "lang": "pt"},
    {"title": "Processamento de Linguagem Natural", "depth": 2, "lang": "pt"},
]

GITHUB_REPOS = [
    {"owner": "karpathy", "repo": "char-rnn", "track_issues": True, "track_prs": True},
    {"owner": "openai", "repo": "gpt-2", "track_issues": True, "track_prs": True},
    {"owner": "huggingface", "repo": "transformers", "track_issues": True, "track_prs": True},
    {"owner": "tensorflow", "repo": "tensorflow", "track_issues": False, "track_prs": False},  # Repo muito grande
]

# =========================
# Modelo de Dados Avançado
# =========================
@dataclass
class RegistroAprendizado:
    """Representa um registro de aprendizado com metadados enriquecidos"""
    id: str
    origem: OrigemConhecimento
    titulo: str
    conteudo: str
    link: str
    data_coleta: datetime = field(default_factory=datetime.now)
    data_publicacao: Optional[datetime] = None
    peso: float = 0.0
    embeddings: Optional[np.ndarray] = None
    tags: List[str] = field(default_factory=list)
    metadados: Dict[str, Any] = field(default_factory=dict)
    processado: bool = False
    versao_coleta: str = "2.0.0"
    
    def __post_init__(self):
        if not self.id:
            conteudo_hash = hashlib.md5(
                f"{self.origem.value}{self.titulo}{self.conteudo[:100]}".encode()
            ).hexdigest()[:12]
            self.id = f"{self.origem.value[:3]}_{conteudo_hash}_{int(self.data_coleta.timestamp())}"
        
        if not self.data_publicacao:
            self.data_publicacao = self.data_coleta
    
    def to_dict(self) -> Dict:
        """Converte para dicionário serializável"""
        return {
            "id": self.id,
            "origem": self.origem.value,
            "titulo": self.titulo,
            "conteudo": self.conteudo[:500] + "..." if len(self.conteudo) > 500 else self.conteudo,
            "link": self.link,
            "data_coleta": self.data_coleta.isoformat(),
            "data_publicacao": self.data_publicacao.isoformat() if self.data_publicacao else None,
            "peso": self.peso,
            "tags": self.tags,
            "metadados": self.metadados,
            "processado": self.processado
        }
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, RegistroAprendizado) and self.id == other.id

# =========================
# Analisador de Performance
# =========================
class AnalisadorPerformance:
    """Analisa métricas detalhadas do sistema em tempo real"""
    
    def __init__(self):
        self.tempos_busca = deque(maxlen=100)
        self.relevancias = deque(maxlen=100)
        self.erros = deque(maxlen=50)
        self.memoria_usada = deque(maxlen=50)
        self.cache_hits = 0
        self.cache_misses = 0
        self.inicio_operacao: Optional[datetime] = None
        self.operacao_atual: Optional[str] = None
        
    def iniciar_operacao(self, nome: str):
        """Inicia medição de uma operação"""
        self.inicio_operacao = datetime.now()
        self.operacao_atual = nome
        
    def finalizar_operacao(self, sucesso: bool = True) -> float:
        """Finaliza medição e retorna tempo decorrido"""
        if not self.inicio_operacao:
            return 0.0
            
        tempo = (datetime.now() - self.inicio_operacao).total_seconds()
        self.tempos_busca.append(tempo)
        
        if not sucesso:
            self.erros.append({
                'operacao': self.operacao_atual,
                'tempo': tempo,
                'timestamp': datetime.now().isoformat()
            })
        
        self.inicio_operacao = None
        self.operacao_atual = None
        return tempo
    
    def registrar_relevancia(self, relevancia: float):
        """Registra relevância de um conteúdo"""
        self.relevancias.append(relevancia)
    
    def registrar_cache(self, hit: bool):
        """Registra acesso ao cache"""
        if hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
    
    def registrar_memoria(self):
        """Registra uso atual de memória"""
        self.memoria_usada.append(psutil.Process().memory_percent())
    
    def get_metricas_completas(self) -> Dict:
        """Retorna análise detalhada do sistema"""
        # Coleta dados do sistema
        process = psutil.Process()
        cpu_percent = process.cpu_percent()
        memory_percent = process.memory_percent()
        memory_rss = process.memory_info().rss / 1024 / 1024  # MB
        
        metricas = {
            'velocidade': {
                'media': statistics.mean(self.tempos_busca) if self.tempos_busca else 0,
                'mediana': statistics.median(self.tempos_busca) if self.tempos_busca else 0,
                'p95': self._percentil(95, self.tempos_busca),
                'p99': self._percentil(99, self.tempos_busca),
                'max': max(self.tempos_busca) if self.tempos_busca else 0,
                'min': min(self.tempos_busca) if self.tempos_busca else 0,
                'tendencia': self._calcular_tendencia(self.tempos_busca)
            },
            'relevancia': {
                'media': statistics.mean(self.relevancias) if self.relevancias else 0,
                'mediana': statistics.median(self.relevancias) if self.relevancias else 0,
                'minima': min(self.relevancias) if self.relevancias else 0,
                'maxima': max(self.relevancias) if self.relevancias else 0,
                'distribuicao': self._distribuicao_relevancia()
            },
            'cache': {
                'hit_rate': self.cache_hits / (self.cache_hits + self.cache_misses + 1),
                'hits': self.cache_hits,
                'misses': self.cache_misses,
                'eficiencia': self._calcular_eficiencia_cache()
            },
            'sistema': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'memory_mb': memory_rss,
                'memory_tendencia': self._calcular_tendencia_memoria(),
                'threads': process.num_threads(),
                'conexoes_abertas': len(process.connections())
            },
            'erros': {
                'taxa': len(self.erros) / (len(self.tempos_busca) + 1),
                'total': len(self.erros),
                'ultimos': list(self.erros)[-5:]
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return metricas
    
    def _percentil(self, p: int, dados: deque) -> float:
        """Calcula percentil dos dados"""
        if not dados:
            return 0.0
        dados_ordenados = sorted(dados)
        idx = int(len(dados_ordenados) * p / 100)
        return dados_ordenados[min(idx, len(dados_ordenados) - 1)]
    
    def _calcular_tendencia(self, dados: deque) -> str:
        """Calcula tendência de melhora/piora"""
        if len(dados) < 10:
            return "estavel"
        
        lista_dados = list(dados)
        metade = len(lista_dados) // 2
        primeira_metade = statistics.mean(lista_dados[:metade])
        segunda_metade = statistics.mean(lista_dados[metade:])
        
        if segunda_metade < primeira_metade * 0.9:
            return "melhorando"
        elif segunda_metade > primeira_metade * 1.1:
            return "piorando"
        else:
            return "estavel"
    
    def _calcular_tendencia_memoria(self) -> str:
        """Calcula tendência de uso de memória"""
        if len(self.memoria_usada) < 5:
            return "estavel"
        
        lista_mem = list(self.memoria_usada)
        if lista_mem[-1] > lista_mem[0] * 1.2:
            return "crescendo"
        elif lista_mem[-1] < lista_mem[0] * 0.8:
            return "diminuindo"
        else:
            return "estavel"
    
    def _distribuicao_relevancia(self) -> Dict:
        """Distribuição das relevâncias em categorias"""
        if not self.relevancias:
            return {}
        
        dist = {
            'baixa': 0,    # < 0.3
            'media': 0,    # 0.3 - 0.7
            'alta': 0      # > 0.7
        }
        
        for r in self.relevancias:
            if r < 0.3:
                dist['baixa'] += 1
            elif r < 0.7:
                dist['media'] += 1
            else:
                dist['alta'] += 1
        
        total = len(self.relevancias)
        return {k: v/total for k, v in dist.items()}
    
    def _calcular_eficiencia_cache(self) -> float:
        """Calcula eficiência do cache (hit_rate * economia_tempo)"""
        hit_rate = self.cache_hits / (self.cache_hits + self.cache_misses + 1)
        
        if len(self.tempos_busca) < 10:
            return hit_rate
        
        # Estima tempo economizado pelo cache
        tempo_medio_com_cache = statistics.mean(list(self.tempos_busca)[-10:])
        tempo_sem_cache_estimado = tempo_medio_com_cache * 2  # Estimativa
        
        economia = (tempo_sem_cache_estimado - tempo_medio_com_cache) / tempo_sem_cache_estimado
        return hit_rate * economia

# =========================
# Gerenciador de Cache Avançado
# =========================
class CacheManager:
    """Gerencia cache com Redis e fallback local, com estatísticas"""
    
    def __init__(self, config: Config):
        self.config = config
        self.redis_client = None
        self.local_cache: Dict[str, Tuple[Any, datetime]] = {}
        self.stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0
        }
        
    async def initialize(self):
        """Inicializa conexão com Redis"""
        try:
            self.redis_client = redis.from_url(
                self.config.REDIS_URL, 
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            await self.redis_client.ping()
            logger.info("✅ Redis conectado com sucesso")
        except Exception as e:
            logger.warning(f"⚠️ Redis não disponível, usando cache local: {e}")
    
    async def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        # Tenta Redis primeiro
        if self.redis_client:
            try:
                data = await self.redis_client.get(key)
                if data:
                    self.stats['hits'] += 1
                    return pickle.loads(data.encode('latin1')) if data else None
            except Exception as e:
                logger.debug(f"Erro ao ler Redis: {e}")
        
        # Fallback para cache local
        if key in self.local_cache:
            value, expiry = self.local_cache[key]
            if expiry > datetime.now():
                self.stats['hits'] += 1
                return value
            else:
                del self.local_cache[key]
        
        self.stats['misses'] += 1
        return None
    
    async def set(self, key: str, value: Any, ttl: int = None):
        """Armazena valor no cache"""
        ttl = ttl or self.config.CACHE_TTL
        self.stats['sets'] += 1
        
        # Serializa para pickle (suporta objetos complexos)
        try:
            serialized = pickle.dumps(value).decode('latin1')
        except Exception as e:
            logger.error(f"Erro ao serializar para cache: {e}")
            return
        
        if self.redis_client:
            try:
                await self.redis_client.setex(key, ttl, serialized)
            except Exception as e:
                logger.debug(f"Erro ao escrever Redis: {e}")
        
        # Cache local como backup
        self.local_cache[key] = (value, datetime.now() + timedelta(seconds=ttl))
        
        # Limpeza periódica do cache local
        if len(self.local_cache) > 1000:
            self._limpar_cache_local()
    
    async def delete(self, key: str):
        """Remove item do cache"""
        self.stats['deletes'] += 1
        
        if self.redis_client:
            try:
                await self.redis_client.delete(key)
            except Exception:
                pass
        
        self.local_cache.pop(key, None)
    
    async def clear(self):
        """Limpa todo o cache"""
        if self.redis_client:
            try:
                await self.redis_client.flushdb()
            except Exception:
                pass
        
        self.local_cache.clear()
        logger.info("🧹 Cache limpo")
    
    def _limpar_cache_local(self):
        """Remove itens expirados do cache local"""
        agora = datetime.now()
        expirados = [k for k, (_, exp) in self.local_cache.items() if exp <= agora]
        for k in expirados:
            del self.local_cache[k]
        logger.debug(f"🧹 Cache local: {len(expirados)} itens expirados removidos")
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do cache"""
        total = self.stats['hits'] + self.stats['misses']
        return {
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'hit_rate': self.stats['hits'] / total if total > 0 else 0,
            'sets': self.stats['sets'],
            'deletes': self.stats['deletes'],
            'local_cache_size': len(self.local_cache)
        }

# =========================
# Processador de NLP Avançado
# =========================
class NLPProcessor:
    """Processamento de linguagem natural para análise de conteúdo"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words=self._get_stopwords_portugues(),
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )
        self.documentos: List[str] = []
        self.tfidf_matrix = None
        self.embeddings_cache: Dict[str, np.ndarray] = {}
        
    def _get_stopwords_portugues(self) -> List[str]:
        """Lista de stopwords em português"""
        return [
            'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'com',
            'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos',
            'como', 'mas', 'ao', 'ele', 'das', 'à', 'seu', 'sua', 'ou', 'quando',
            'muito', 'nos', 'já', 'eu', 'também', 'só', 'pelo', 'pela', 'até',
            'isso', 'ela', 'entre', 'depois', 'sem', 'mesmo', 'aos', 'seus',
            'quem', 'nas', 'me', 'esse', 'eles', 'você', 'essa', 'num', 'nem',
            'suas', 'meu', 'às', 'minha', 'numa', 'pelos', 'elas', 'qual', 'nós',
            'lhe', 'deles', 'essas', 'esses', 'pelas', 'este', 'dele', 'tu'
        ]
    
    async def extrair_tags(self, texto: str, limite: int = 5) -> List[str]:
        """Extrai tags relevantes do texto usando TF-IDF"""
        if not texto or len(texto.strip()) < 20:
            return []
        
        try:
            # Adiciona ao corpus se necessário
            if texto not in self.documentos:
                self.documentos.append(texto)
                self._atualizar_tfidf()
            
            # Pega índices das palavras mais importantes
            if self.tfidf_matrix is not None:
                idx = self.documentos.index(texto)
                tfidf_scores = self.tfidf_matrix[idx].toarray()[0]
                
                # Pega top N palavras
                top_indices = tfidf_scores.argsort()[-limite:][::-1]
                feature_names = self.vectorizer.get_feature_names_out()
                
                tags = [feature_names[i] for i in top_indices if tfidf_scores[i] > 0.1]
                return tags[:limite]
        except Exception as e:
            logger.debug(f"Erro na extração de tags: {e}")
        
        # Fallback: extração simples por keywords
        keywords = [
            "ia", "inteligência artificial", "machine learning", "deep learning",
            "redes neurais", "algoritmo", "dados", "computação", "quantum",
            "python", "código", "programação", "tecnologia", "inovação"
        ]
        
        texto_lower = texto.lower()
        encontradas = []
        for kw in keywords:
            if kw in texto_lower and kw not in encontradas:
                encontradas.append(kw)
                if len(encontradas) >= limite:
                    break
        
        return encontradas
    
    def _atualizar_tfidf(self):
        """Atualiza matriz TF-IDF com novos documentos"""
        if len(self.documentos) > 1:
            try:
                self.tfidf_matrix = self.vectorizer.fit_transform(self.documentos)
            except Exception as e:
                logger.debug(f"Erro ao atualizar TF-IDF: {e}")
    
    async def gerar_embeddings(self, texto: str) -> np.ndarray:
        """Gera embeddings para o texto (versão otimizada)"""
        if not texto:
            return np.zeros(384)
        
        # Cache simples
        cache_key = hashlib.md5(texto.encode()[:1000]).hexdigest()
        if cache_key in self.embeddings_cache:
            return self.embeddings_cache[cache_key]
        
        try:
            # Em produção, usaria SentenceTransformers ou similar
            # Aqui usamos uma abordagem simplificada baseada em palavras
            palavras = texto.lower().split()[:200]  # Limita para performance
            
            # Mapeia palavras para vetores aleatórios consistentes
            seed = sum(hash(p) for p in palavras) % 2**32
            rng = np.random.RandomState(seed)
            
            # Gera embedding baseado nas palavras presentes
            embedding = np.zeros(384)
            for i, palavra in enumerate(palavras[:50]):
                word_seed = hash(palavra) % 2**32
                rng_word = np.random.RandomState(word_seed)
                word_vec = rng_word.randn(384)
                word_vec = word_vec / np.linalg.norm(word_vec)
                embedding += word_vec * 0.1  # Contribuição pequena por palavra
            
            # Normaliza
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
        except Exception:
            # Fallback: vetor aleatório mas determinístico
            rng = np.random.RandomState(hash(texto[:100]) % 2**32)
            embedding = rng.randn(384)
            embedding = embedding / np.linalg.norm(embedding)
        
        self.embeddings_cache[cache_key] = embedding
        
        # Limpa cache se muito grande
        if len(self.embeddings_cache) > 1000:
            self.embeddings_cache.clear()
        
        return embedding
    
    async def similaridade(self, texto1: str, texto2: str) -> float:
        """Calcula similaridade entre dois textos"""
        if not texto1 or not texto2:
            return 0.0
        
        # Usa embeddings para similaridade
        emb1 = await self.gerar_embeddings(texto1)
        emb2 = await self.gerar_embeddings(texto2)
        
        return float(cosine_similarity([emb1], [emb2])[0][0])
    
    async def resumir(self, texto: str, max_sentencas: int = 3) -> str:
        """Gera um resumo simples do texto (extrativo)"""
        if not texto:
            return ""
        
        # Divide em sentenças (simplificado)
        sentencas = texto.replace('!', '.').replace('?', '.').split('.')
        sentencas = [s.strip() for s in sentencas if len(s.strip()) > 20]
        
        if len(sentencas) <= max_sentencas:
            return texto
        
        # Pontua sentenças por relevância
        pontuacoes = []
        texto_lower = texto.lower()
        
        for i, sentenca in enumerate(sentencas):
            pontuacao = 0.0
            
            # Posição (primeiras sentenças são mais importantes)
            if i == 0:
                pontuacao += 0.3
            elif i < 3:
                pontuacao += 0.1
            
            # Presença de palavras-chave
            keywords = [
                "importante", "principal", "conclusão", "resultado", "descoberta",
                "inovação", "avanço", "novo", "estudo", "pesquisa"
            ]
            for kw in keywords:
                if kw in sentenca.lower():
                    pontuacao += 0.1
            
            # Tamanho (nem muito curta, nem muito longa)
            palavras = len(sentenca.split())
            if 10 <= palavras <= 30:
                pontuacao += 0.1
            
            pontuacoes.append((pontuacao, sentenca))
        
        # Seleciona as melhores sentenças
        pontuacoes.sort(reverse=True)
        selecionadas = [s for _, s in pontuacoes[:max_sentencas]]
        
        # Ordena por posição original
        selecionadas.sort(key=lambda s: sentencas.index(s) if s in sentencas else 0)
        
        return '. '.join(selecionadas) + '.'

# =========================
# Memória Avançada com Indexação
# =========================
class MemoriaAvancada:
    """Sistema de memória com indexação e busca semântica"""
    
    def __init__(self, nlp_processor: NLPProcessor, cache_manager: CacheManager):
        self.nlp = nlp_processor
        self.cache = cache_manager
        self.registros: List[RegistroAprendizado] = []
        self.registros_por_id: Dict[str, RegistroAprendizado] = {}
        
        # Índices para busca rápida
        self.indice_por_tag: Dict[str, List[RegistroAprendizado]] = defaultdict(list)
        self.indice_por_origem: Dict[OrigemConhecimento, List[RegistroAprendizado]] = defaultdict(list)
        self.indice_por_data: Dict[str, List[RegistroAprendizado]] = defaultdict(list)
        self.indice_por_palavra: Dict[str, List[RegistroAprendizado]] = defaultdict(list)
        
        # Estatísticas
        self.stats = {
            'total_registros': 0,
            'por_origem': defaultdict(int),
            'tags_populares': Counter(),
            'ultima_atualizacao': None
        }
        
    async def armazenar(self, registro: RegistroAprendizado):
        """Armazena registro com processamento avançado e indexação"""
        
        # Evita duplicatas
        if registro.id in self.registros_por_id:
            logger.debug(f"Registro duplicado ignorado: {registro.id}")
            return
        
        # Processa conteúdo
        registro.tags = await self.nlp.extrair_tags(registro.conteudo)
        registro.embeddings = await self.nlp.gerar_embeddings(registro.conteudo)
        registro.peso = self._calcular_peso_base(registro)
        
        # Adiciona aos índices
        self.registros.append(registro)
        self.registros_por_id[registro.id] = registro
        
        # Índice por tag
        for tag in registro.tags:
            self.indice_por_tag[tag].append(registro)
        
        # Índice por origem
        self.indice_por_origem[registro.origem].append(registro)
        
        # Índice por data
        data_key = registro.data_coleta.strftime("%Y-%m-%d")
        self.indice_por_data[data_key].append(registro)
        
        # Índice por palavras-chave (simplificado)
        palavras = set(registro.titulo.lower().split()[:10])
        for palavra in palavras:
            if len(palavra) > 3:
                self.indice_por_palavra[palavra].append(registro)
        
        # Atualiza estatísticas
        self.stats['total_registros'] += 1
        self.stats['por_origem'][registro.origem.value] += 1
        for tag in registro.tags:
            self.stats['tags_populares'][tag] += 1
        self.stats['ultima_atualizacao'] = datetime.now()
        
        # Cache para recuperação rápida
        await self.cache.set(f"registro:{registro.id}", registro.to_dict(), ttl=86400)  # 1 dia
        
        logger.debug(f"📚 Registro armazenado: {registro.titulo[:50]}... (tags: {registro.tags})")
    
    def _calcular_peso_base(self, registro: RegistroAprendizado) -> float:
        """Calcula peso base do registro"""
        peso = 0.5  # Peso base
        
        # Origem influencia
        pesos_origem = {
            OrigemConhecimento.PAPER: 1.0,
            OrigemConhecimento.BLOG: 0.8,
            OrigemConhecimento.NOTICIA: 0.7,
            OrigemConhecimento.WIKIPEDIA: 0.6,
            OrigemConhecimento.GITHUB: 0.5,
        }
        peso += pesos_origem.get(registro.origem, 0.3)
        
        # Tamanho do conteúdo
        tamanho = len(registro.conteudo.split())
        if tamanho > 500:
            peso += 0.3
        elif tamanho > 200:
            peso += 0.2
        elif tamanho > 50:
            peso += 0.1
        
        # Novidade (conteúdo recente é mais relevante)
        idade_dias = (datetime.now() - registro.data_publicacao).days
        if idade_dias < 1:
            peso += 0.5
        elif idade_dias < 7:
            peso += 0.3
        elif idade_dias < 30:
            peso += 0.1
        
        return min(2.0, peso)  # Limita a 2.0
    
    async def buscar_por_tag(self, tag: str, limite: int = 20) -> List[RegistroAprendizado]:
        """Busca registros por tag"""
        registros = self.indice_por_tag.get(tag, [])
        
        # Ordena por peso e data
        registros.sort(key=lambda r: (r.peso, r.data_publicacao), reverse=True)
        
        return registros[:limite]
    
    async def buscar_por_origem(self, origem: OrigemConhecimento, limite: int = 50) -> List[RegistroAprendizado]:
        """Busca registros por origem"""
        registros = self.indice_por_origem.get(origem, [])
        registros.sort(key=lambda r: r.data_publicacao, reverse=True)
        return registros[:limite]
    
    async def buscar_semantica(self, query: str, limite: int = 10) -> List[Tuple[float, RegistroAprendizado]]:
        """Busca semântica por similaridade com a query"""
        if not self.registros:
            return []
        
        # Gera embedding da query
        query_embedding = await self.nlp.gerar_embeddings(query)
        
        # Calcula similaridade com todos os registros
        similaridades = []
        batch_size = 100
        
        for i in range(0, len(self.registros), batch_size):
            batch = self.registros[i:i+batch_size]
            for reg in batch:
                if reg.embeddings is not None:
                    sim = cosine_similarity([query_embedding], [reg.embeddings])[0][0]
                    # Ajusta pelo peso
                    sim_ajustada = sim * (0.5 + reg.peso)
                    similaridades.append((sim_ajustada, reg))
        
        # Ordena e retorna os mais similares
        similaridades.sort(key=lambda x: x[0], reverse=True)
        return similaridades[:limite]
    
    async def encontrar_conexoes(self, registro: RegistroAprendizado, limite: int = 5) -> List[Dict]:
        """Encontra conexões de um registro com outros"""
        conexoes = []
        
        # Busca por tags em comum
        for tag in registro.tags[:3]:  # Limita para performance
            similares = await self.buscar_por_tag(tag, limite=10)
            for similar in similares:
                if similar.id != registro.id:
                    # Calcula similaridade real
                    sim = await self.nlp.similaridade(registro.conteudo, similar.conteudo)
                    if sim > 0.3:
                        conexoes.append({
                            'registro': similar,
                            'similaridade': sim,
                            'tipo': 'tag_comum',
                            'tag': tag
                        })
        
        # Remove duplicatas e ordena
        vistos = set()
        conexoes_unicas = []
        for conn in conexoes:
            if conn['registro'].id not in vistos:
                vistos.add(conn['registro'].id)
                conexoes_unicas.append(conn)
        
        conexoes_unicas.sort(key=lambda x: x['similaridade'], reverse=True)
        return conexoes_unicas[:limite]
    
    async def refletir(self) -> Dict[str, Any]:
        """Gera reflexões profundas sobre o conhecimento adquirido"""
        if not self.registros:
            logger.info("🧠 Memória vazia - ainda sem conhecimento para refletir")
            return {"mensagem": "Memória vazia"}
        
        # Análise temporal
        agora = datetime.now()
        registros_hoje = [r for r in self.registros if r.data_coleta.date() == agora.date()]
        registros_semana = [r for r in self.registros if (agora - r.data_coleta).days <= 7]
        
        # Tags mais populares
        top_tags = self.stats['tags_populares'].most_common(20)
        
        # Tópicos emergentes (tags que cresceram mais recentemente)
        tags_antigas = Counter()
        tags_recentes = Counter()
        
        for r in registros_semana:
            for tag in r.tags:
                tags_recentes[tag] += 1
        
        for r in self.registros:
            if (agora - r.data_coleta).days > 30:
                for tag in r.tags:
                    tags_antigas[tag] += 1
        
        topicos_emergentes = []
        for tag, count_recente in tags_recentes.most_common(30):
            count_antigo = tags_antigas.get(tag, 0)
            if count_antigo > 0:
                crescimento = (count_recente - count_antigo) / count_antigo
                if crescimento > 0.5:
                    topicos_emergentes.append((tag, crescimento))
        
        topicos_emergentes.sort(key=lambda x: x[1], reverse=True)
        
        # Encontra conexões fortes entre áreas
        conexoes_fortes = []
        areas = list(set(r.origem for r in self.registros[:100]))
        
        for i, area1 in enumerate(areas):
            for area2 in areas[i+1:]:
                # Amostra de registros de cada área
                regs_area1 = [r for r in self.registros if r.origem == area1][:20]
                regs_area2 = [r for r in self.registros if r.origem == area2][:20]
                
                if regs_area1 and regs_area2:
                    # Calcula similaridade média
                if regs_area1 and regs_area2:
                    sim_total = 0
                    count = 0
                    for r1 in regs_area1[:5]:  # Limita para performance
                        for r2 in regs_area2[:5]:
                            sim = await self.nlp.similaridade(r1.conteudo, r2.conteudo)
                            sim_total += sim
                            count += 1
                    
                    if count > 0:
                        sim_media = sim_total / count
                        if sim_media > 0.2:
                            conexoes_fortes.append({
                                'area1': area1.value,
                                'area2': area2.value,
                                'similaridade': sim_media
                            })
        
        # Gera insights
        insights = []
        
        # Insight 1: Áreas mais ativas
        areas_ativas = self.stats['por_origem'].most_common(3)
        if areas_ativas:
            insights.append(f"📊 Áreas mais ativas: {', '.join([f'{a}({c})' for a, c in areas_ativas])}")
        
        # Insight 2: Tópicos emergentes
        if topicos_emergentes:
            top_emergentes = topicos_emergentes[:3]
            insights.append(f"🔥 Tópicos emergentes: {', '.join([t for t, _ in top_emergentes])}")
        
        # Insight 3: Conexões surpreendentes
        conexoes_interessantes = [c for c in conexoes_fortes if c['similaridade'] > 0.3][:3]
        if conexoes_interessantes:
            for conn in conexoes_interessantes:
                insights.append(f"🔗 Conexão: {conn['area1']} ↔ {conn['area2']} ({conn['similaridade']:.2f})")
        
        # Insight 4: Lacunas de conhecimento
        areas_conhecidas = set(self.stats['por_origem'].keys())
        areas_importantes = {'paper', 'blog', 'github'}
        areas_faltando = areas_importantes - areas_conhecidas
        if areas_faltando:
            insights.append(f"⚠️ Lacunas: {', '.join(areas_faltando)}")
        
        # Prepara resultado
        resultado = {
            'timestamp': agora.isoformat(),
            'estatisticas': {
                'total': len(self.registros),
                'novos_hoje': len(registros_hoje),
                'novos_semana': len(registros_semana),
                'por_origem': dict(self.stats['por_origem']),
                'media_peso': statistics.mean([r.peso for r in self.registros]) if self.registros else 0
            },
            'tags': {
                'top_10': top_tags[:10],
                'emergentes': topicos_emergentes[:5]
            },
            'conexoes': conexoes_fortes[:5],
            'insights': insights
        }
        
        # Log bonito
        print("\n" + "="*60)
        print("🧠 REFLEXÃO DA ATENA Ω")
        print("="*60)
        print(f"📚 Total de aprendizados: {resultado['estatisticas']['total']}")
        print(f"📈 Novos hoje: {resultado['estatisticas']['novos_hoje']} | Esta semana: {resultado['estatisticas']['novos_semana']}")
        print(f"📊 Distribuição: {dict(resultado['estatisticas']['por_origem'])}")
        print(f"🏷️ Top tags: {[t for t, c in resultado['tags']['top_10'][:5]]}")
        
        if insights:
            print("\n💡 INSIGHTS:")
            for insight in insights:
                print(f"   {insight}")
        
        print("="*60)
        
        return resultado

# =========================
# Sandbox para Testes Seguros
# =========================
class SandboxExecucao:
    """Ambiente isolado para testar modificações antes de aplicar"""
    
    def __init__(self, config: Config):
        self.config = config
        self.temp_dir = f"/tmp/atena_sandbox_{os.getpid()}"
        self.modulos_carregados = set()
        
    async def __aenter__(self):
        """Cria ambiente sandbox"""
        os.makedirs(self.temp_dir, exist_ok=True)
        logger.debug(f"🔬 Sandbox criado em {self.temp_dir}")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Limpa ambiente sandbox"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
            logger.debug("🧹 Sandbox limpo")
        except Exception:
            pass
    
    async def testar_codigo(self, codigo: str, funcao_teste: str, *args, **kwargs) -> Tuple[bool, Any, str]:
        """Testa código em ambiente isolado"""
        resultado = None
        erro = None
        sucesso = False
        
        try:
            # Cria namespace isolado
            namespace = {
                '__name__': '__sandbox__',
                'datetime': datetime,
                'asyncio': asyncio,
                'json': json,
                'logging': logging,
                'numpy': np,
            }
            
            # Executa código
            exec(compile(codigo, '<sandbox>', 'exec'), namespace)
            
            # Chama função de teste se existir
            if funcao_teste in namespace:
                if asyncio.iscoroutinefunction(namespace[funcao_teste]):
                    resultado = await namespace[funcao_teste](*args, **kwargs)
                else:
                    resultado = namespace[funcao_teste](*args, **kwargs)
                sucesso = True
            else:
                erro = f"Função {funcao_teste} não encontrada"
                
        except Exception as e:
            erro = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
            logger.debug(f"❌ Erro no sandbox: {erro[:200]}...")
        
        return sucesso, resultado, erro
    
    async def testar_performance(self, codigo: str, funcao_teste: str, iteracoes: int = 5) -> Dict:
        """Testa performance do código"""
        tempos = []
        uso_memoria = []
        
        for i in range(iteracoes):
            # Força garbage collection
            gc.collect()
            
            # Mede memória antes
            mem_antes = psutil.Process().memory_info().rss / 1024 / 1024
            
            # Executa código
            inicio = time.perf_counter()
            sucesso, _, erro = await self.testar_codigo(codigo, funcao_teste)
            tempo = time.perf_counter() - inicio
            
            # Mede memória depois
            mem_depois = psutil.Process().memory_info().rss / 1024 / 1024
            
            if sucesso:
                tempos.append(tempo)
                uso_memoria.append(mem_depois - mem_antes)
        
        if not tempos:
            return {'sucesso': False, 'erro': erro}
        
        return {
            'sucesso': True,
            'tempo_medio': statistics.mean(tempos),
            'tempo_std': statistics.stdev(tempos) if len(tempos) > 1 else 0,
            'tempo_min': min(tempos),
            'tempo_max': max(tempos),
            'memoria_media': statistics.mean(uso_memoria) if uso_memoria else 0,
            'iteracoes_sucesso': len(tempos)
        }

# =========================
# Sistema de Evolução
# =========================
class SistemaEvolucao:
    """Gerencia o processo de auto-evolução da ATENA"""
    
    def __init__(self, config: Config, memoria: MemoriaAvancada, analisador: AnalisadorPerformance):
        self.config = config
        self.memoria = memoria
        self.analisador = analisador
        self.historico_evolucoes: List[Dict] = []
        self.evolucoes_hoje = 0
        self.ultima_evolucao = datetime.now()
        self.versao = "2.0.0"
        
    def _incrementar_versao(self) -> str:
        """Incrementa versão (major.minor.patch)"""
        major, minor, patch = map(int, self.versao.split('.'))
        
        # Lógica de incremento baseada no tipo de mudança
        if self.evolucoes_hoje % 10 == 0:
            major += 1
            minor = 0
            patch = 0
        elif self.evolucoes_hoje % 3 == 0:
            minor += 1
            patch = 0
        else:
            patch += 1
        
        return f"{major}.{minor}.{patch}"
    
    async def analisar_e_sugerir(self) -> Optional[Dict]:
        """Analisa métricas e sugere melhorias"""
        metricas = self.analisador.get_metricas_completas()
        
        # Verifica se pode evoluir hoje
        if self.evolucoes_hoje >= self.config.MAX_EVOLUTIONS_PER_DAY:
            logger.info(f"⚠️ Limite de evoluções diárias atingido ({self.config.MAX_EVOLUTIONS_PER_DAY})")
            return None
        
        # Coleta sugestões em paralelo
        sugestoes = await asyncio.gather(
            self._sugerir_cache_mais_agressivo(metricas),
            self._sugerir_nova_heuristica_pesos(metricas),
            self._sugerir_nova_fonte_dados(metricas),
            return_exceptions=True
        )
        
        # Filtra sugestões válidas
        sugestoes_validas = []
        for s in sugestoes:
            if s and not isinstance(s, Exception) and s.get('confianca', 0) >= self.config.EVOLUTION_THRESHOLD:
                sugestoes_validas.append(s)
        
        if not sugestoes_validas:
            return None
        
        # Escolhe melhor sugestão
        melhor_sugestao = max(sugestoes_validas, key=lambda x: x['confianca'])
        
        # Adiciona metadados
        melhor_sugestao.update({
            'timestamp': datetime.now().isoformat(),
            'versao_atual': self.versao,
            'metricas_motivacao': {
                'hit_rate': metricas['cache']['hit_rate'],
                'tempo_medio': metricas['velocidade']['media'],
                'relevancia_media': metricas['relevancia']['media']
            }
        })
        
        return melhor_sugestao
    
    async def _sugerir_cache_mais_agressivo(self, metricas: Dict) -> Optional[Dict]:
        """Sugere otimizações de cache baseado em métricas"""
        hit_rate = metricas['cache']['hit_rate']
        tempo_medio = metricas['velocidade']['media']
        
        # Cache ineficiente
        if hit_rate < 0.3:
            return {
                'tipo': TipoEvolucao.CACHE.value,
                'descricao': 'Implementar cache preditivo baseado em padrões de acesso',
                'confianca': 0.85,
                'prioridade': 'alta',
                'codigo': '''
class CachePreditivo:
    """Cache que aprende padrões de acesso e pré-carrega conteúdo"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.padroes_acesso = defaultdict(int)
        self.correlacoes = defaultdict(lambda: defaultdict(int))
        
    async def get(self, key: str):
        # Registra acesso
        self.padroes_acesso[key] += 1
        
        # Verifica correlações
        for outro_key in list(self.correlacoes[key].keys())[:5]:
            self.correlacoes[key][outro_key] += 1
        
        # Busca do cache
        return await self.redis.get(key)
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        await self.redis.setex(key, ttl, value)
        
        # Pré-carrega itens correlacionados
        if len(self.padroes_acesso) > 10:
            await self._precarregar_correlacionados(key)
    
    async def _precarregar_correlacionados(self, key: str):
        """Pré-carrega itens frequentemente acessados junto"""
        correlatos = sorted(
            self.correlacoes[key].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        for outro_key, _ in correlatos:
            if not await self.redis.exists(outro_key):
                # Agenda pré-carregamento
                asyncio.create_task(self._carregar_item(outro_key))
'''
            }
        
        # Cache lento
        if tempo_medio > 2.0:
            return {
                'tipo': TipoEvolucao.CACHE.value,
                'descricao': 'Adicionar cache em múltiplos níveis (L1/L2)',
                'confianca': 0.9,
                'prioridade': 'media',
                'codigo': '''
class CacheMultinivel:
    """Cache L1 (memória) + L2 (Redis)"""
    
    def __init__(self, redis_client, l1_size=100):
        self.redis = redis_client
        self.l1_cache = OrderedDict()
        self.l1_size = l1_size
        
    async def get(self, key: str):
        # Tenta L1 primeiro
        if key in self.l1_cache:
            self.l1_cache.move_to_end(key)
            return self.l1_cache[key]
        
        # Tenta L2
        value = await self.redis.get(key)
        if value:
            # Promove para L1
            self._add_to_l1(key, value)
        
        return value
    
    def _add_to_l1(self, key: str, value: Any):
        if len(self.l1_cache) >= self.l1_size:
            self.l1_cache.popitem(last=False)
        self.l1_cache[key] = value
'''
            }
        
        return None
    
    async def _sugerir_nova_heuristica_pesos(self, metricas: Dict) -> Optional[Dict]:
        """Sugere nova heurística de pesos baseada em aprendizado"""
        relevancia_media = metricas['relevancia']['media']
        distribuicao = metricas['relevancia']['distribuicao']
        
        # Muitos conteúdos de baixa relevância
        if distribuicao.get('baixa', 0) > 0.5:
            # Busca padrões nos melhores conteúdos
            melhores = await self.memoria.buscar_semantica("importante relevante inovador", limite=20)
            
            if melhores:
                # Extrai características dos melhores
                caracteristicas = []
                for _, reg in melhores[:10]:
                    palavras = set(reg.titulo.lower().split() + reg.conteudo.lower().split()[:50])
                    caracteristicas.extend(list(palavras))
                
                from collections import Counter
                palavras_importantes = Counter(caracteristicas).most_common(30)
                
                return {
                    'tipo': TipoEvolucao.HEURISTICA.value,
                    'descricao': 'Heurística adaptativa baseada em exemplos reais de sucesso',
                    'confianca': 0.8,
                    'prioridade': 'alta',
                    'codigo': f'''
def calcular_peso_adaptativo(self, registro: RegistroAprendizado) -> float:
    """Heurística gerada por análise de {len(melhores)} exemplos reais"""
    
    peso = 0.5  # Peso base
    
    # Palavras indicadoras de qualidade (aprendidas)
    palavras_positivas = {[p for p, _ in palavras_importantes[:20]]}
    palavras_negativas = ['clique', 'compre', 'promoção', 'desconto']
    
    # Análise de título
    titulo_lower = registro.titulo.lower()
    for palavra in palavras_positivas:
        if palavra in titulo_lower:
            peso += 0.1
    
    for palavra in palavras_negativas:
        if palavra in titulo_lower:
            peso -= 0.2
    
    # Análise de conteúdo
    if len(registro.conteudo.split()) > 300:
        peso += 0.3  # Conteúdo substancial
    
    # Fonte confiável (aprendido)
    fontes_confiaveis = {self._identificar_fontes_confiaveis()}
    if registro.origem.value in fontes_confiaveis:
        peso += 0.4
    
    return max(0, min(2, peso))
'''
                }
        
        return None
    
    async def _sugerir_nova_fonte_dados(self, metricas: Dict) -> Optional[Dict]:
        """Sugere novas fontes de dados baseado em gaps de conhecimento"""
        
        # Identifica gaps
        gaps = []
        conceitos_importantes = [
            'transformer', 'attention', 'neural network', 'deep learning',
            'reinforcement learning', 'computer vision', 'nlp'
        ]
        
        for conceito in conceitos_importantes:
            ocorrencias = sum(
                1 for r in self.memoria.registros[-500:]  # Últimos 500
                if conceito.lower() in r.conteudo.lower()
            )
            if ocorrencias < 5:
                gaps.append(conceito)
        
        if gaps:
            # Sugere fontes específicas para os gaps
            fontes_sugeridas = []
            
            if 'transformer' in gaps or 'attention' in gaps:
                fontes_sugeridas.append({
                    'nome': 'arXiv CS.CL',
                    'url': 'https://export.arxiv.org/api/query',
                    'params': {
                        'search_query': 'cat:cs.CL+AND+transformer',
                        'max_results': 10,
                        'sortBy': 'submittedDate'
                    },
                    'parser': 'parse_arxiv'
                })
            
            if 'reinforcement learning' in gaps:
                fontes_sugeridas.append({
                    'nome': 'OpenAI Spinning Up',
                    'url': 'https://spinningup.openai.com/en/latest/_static/rl_intro.html',
                    'parser': 'parse_html'
                })
            
            if fontes_sugeridas:
                return {
                    'tipo': TipoEvolucao.FONTE.value,
                    'descricao': f'Adicionar fontes para gaps: {", ".join(gaps[:3])}',
                    'confianca': 0.75,
                    'prioridade': 'media',
                    'fontes': fontes_sugeridas,
                    'codigo': self._gerar_codigo_novas_fontes(fontes_sugeridas)
                }
        
        return None
    
    def _gerar_codigo_novas_fontes(self, fontes: List[Dict]) -> str:
        """Gera código para adicionar novas fontes"""
        fontes_json = json.dumps(fontes, indent=4, ensure_ascii=False)
        
        return f'''
# Novas fontes sugeridas pela auto-evolução
NOVAS_FONTES = {fontes_json}

async def buscar_novas_fontes(self):
    """Busca dados das novas fontes sugeridas"""
    for fonte in NOVAS_FONTES:
        try:
            if fonte['parser'] == 'parse_arxiv':
                await self._buscar_arxiv(fonte)
            elif fonte['parser'] == 'parse_html':
                await self._buscar_html(fonte)
        except Exception as e:
            logger.error(f"Erro na nova fonte {{fonte['nome']}}: {{e}}")

async def _buscar_arxiv(self, fonte):
    """Parser específico para arXiv"""
    async with self.sessao_http.get(fonte['url'], params=fonte.get('params', {{}})) as resp:
        data = await resp.text()
        # Implementar parsing de XML do arXiv
        logger.info(f"📚 Buscando arXiv: {{fonte['nome']}}")
'''
    
    async def testar_evolucao(self, sugestao: Dict) -> Tuple[bool, Dict]:
        """Testa evolução em sandbox antes de aplicar"""
        
        logger.info(f"🧪 Testando evolução: {sugestao['descricao']}")
        
        async with SandboxExecucao(self.config) as sandbox:
            # Teste 1: Compilação e execução básica
            sucesso, _, erro = await sandbox.testar_codigo(
                sugestao['codigo'],
                'teste_evolucao' if 'teste_evolucao' in sugestao['codigo'] else 'main'
            )
            
            if not sucesso:
                logger.warning(f"❌ Teste de compilação falhou: {erro[:100]}...")
                return False, {'erro': erro}
            
            # Teste 2: Performance
            perf = await sandbox.testar_performance(sugestao['codigo'], 'main', iteracoes=3)
            
            if not perf.get('sucesso', False):
                logger.warning(f"❌ Teste de performance falhou: {perf.get('erro', 'desconhecido')}")
                return False, perf
            
            # Teste 3: Consumo de memória
            if perf.get('memoria_media', 0) > self.config.SANDBOX_MEMORY_LIMIT:
                logger.warning(f"❌ Consumo de memória muito alto: {perf.get('memoria_media', 0):.1f}MB")
                return False, perf
            
            logger.info(f"✅ Testes OK - Tempo: {perf['tempo_medio']*1000:.1f}ms, "
                       f"Memória: {perf['memoria_media']:.1f}MB")
            
            return True, perf
    
    async def aplicar_evolucao(self, sugestao: Dict, resultados_teste: Dict):
        """Aplica evolução aprovada no código real"""
        
        logger.info(f"🚀 Aplicando evolução: {sugestao['descricao']}")
        
        # Incrementa versão
        self.versao = self._incrementar_versao()
        
        # Registra evolução
        evolucao = {
            'id': hashlib.md5(f"{sugestao['descricao']}{datetime.now()}".encode()).hexdigest()[:8],
            'timestamp': datetime.now().isoformat(),
            'versao': self.versao,
            'sugestao': sugestao,
            'resultados_teste': resultados_teste
        }
        
        self.historico_evolucoes.append(evolucao)
        self.evolucoes_hoje += 1
        self.ultima_evolucao = datetime.now()
        
        # Se AUTO_COMMIT ativo, modifica o código
        if self.config.AUTO_COMMIT:
            await self._modificar_codigo_fonte(sugestao['codigo'])
        
        # Log da evolução
        print("\n" + "✨"*40)
        print(f"✨ EVOLUÇÃO CONCLUÍDA - Versão {self.versao}")
        print("✨"*40)
        print(f"📝 Descrição: {sugestao['descricao']}")
        print(f"🎯 Confiança: {sugestao['confianca']:.1%}")
        print(f"⚡ Performance: {resultados_teste['tempo_medio']*1000:.1f}ms")
        print(f"💾 Memória: {resultados_teste.get('memoria_media', 0):.1f}MB")
        print(f"📊 Total de evoluções: {len(self.historico_evolucoes)}")
        print("✨"*40)
        
        # Salva histórico
        self._salvar_historico()
    
    async def _modificar_codigo_fonte(self, novo_codigo: str):
        """Modifica o próprio código fonte (auto-substituição)"""
        try:
            # Backup
            backup_file = f"backup_v{self.versao}.py"
            with open(__file__, 'r') as f:
                codigo_atual = f.read()
            
            with open(backup_file, 'w') as f:
                f.write(codigo_atual)
            
            # Aplica formatação
            try:
                novo_codigo = black.format_str(novo_codigo, mode=black.Mode())
            except:
                pass
            
            # Escreve novo código
            with open(__file__, 'w') as f:
                f.write(novo_codigo)
            
            logger.info(f"💾 Código modificado (backup: {backup_file})")
            
        except Exception as e:
            logger.error(f"❌ Erro ao modificar código: {e}")
    
    def _salvar_historico(self):
        """Salva histórico de evoluções em arquivo"""
        try:
            historico_file = 'historico_evolucoes.json'
            
            # Carrega histórico existente
            historico_completo = []
            if os.path.exists(historico_file):
                with open(historico_file, 'r') as f:
                    historico_completo = json.load(f)
            
            # Adiciona novas evoluções
            for ev in self.historico_evolucoes:
                if ev not in historico_completo:
                    historico_completo.append(ev)
            
            # Salva
            with open(historico_file, 'w') as f:
                json.dump(historico_completo, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"📝 Histórico salvo ({len(historico_completo)} evoluções)")
            
        except Exception as e:
            logger.error(f"Erro ao salvar histórico: {e}")

# =========================
# ATENA Ω - Versão Auto-Evolutiva
# =========================
class AtenaOmegaEvolutiva:
    """Versão final da ATENA Ω com capacidade de auto-evolução"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.cache = CacheManager(self.config)
        self.nlp = NLPProcessor()
        self.memoria = MemoriaAvancada(self.nlp, self.cache)
        self.analisador = AnalisadorPerformance()
        self.sistema_evolucao = SistemaEvolucao(self.config, self.memoria, self.analisador)
        
        self.fontes_ativas = {
            'news': NEWS_FEEDS.copy(),
            'wiki': WIKI_TOPICS.copy(),
            'github': GITHUB_REPOS.copy()
        }
        
        self.semaforo = asyncio.Semaphore(self.config.MAX_CONCURRENT_REQUESTS)
        self.sessao_http: Optional[aiohttp.ClientSession] = None
        self.rodando = True
        self.ciclo_atual = 0
        
    async def __aenter__(self):
        """Context manager para recursos"""
        headers = {
            "User-Agent": self.config.USER_AGENT,
            "Accept": "application/json"
        }
        self.sessao_http = aiohttp.ClientSession(
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=self.config.TIMEOUT)
        )
        await self.cache.initialize()
        
        # Tenta carregar histórico de evoluções
        await self._carregar_historico()
        
        logger.info("🚀 ATENA Ω Auto-Evolutiva iniciada")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Limpeza de recursos"""
        self.rodando = False
        if self.sessao_http:
            await self.sessao_http.close()
        
        # Salva estado final
        await self._salvar_estado()
        logger.info("👋 ATENA Ω encerrada")
    
    async def _carregar_historico(self):
        """Carrega histórico de evoluções"""
        try:
            if os.path.exists('historico_evolucoes.json'):
                with open('historico_evolucoes.json', 'r') as f:
                    historico = json.load(f)
                self.sistema_evolucao.historico_evolucoes = historico
                logger.info(f"📚 Histórico carregado: {len(historico)} evoluções")
        except Exception as e:
            logger.debug(f"Erro ao carregar histórico: {e}")
    
    async def _salvar_estado(self):
        """Salva estado atual"""
        estado = {
            'versao': self.sistema_evolucao.versao,
            'total_registros': len(self.memoria.registros),
            'total_evolucoes': len(self.sistema_evolucao.historico_evolucoes),
            'ciclos_completados': self.ciclo_atual,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            with open('estado_atena.json', 'w') as f:
                json.dump(estado, f, indent=2)
        except Exception:
            pass
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def _fazer_requisicao(self, url: str, params: Dict = None) -> Dict:
        """Faz requisição HTTP com retry e rate limiting"""
        async with self.semaforo:
            # Verifica cache
            cache_key = f"req:{url}:{hashlib.md5(str(params).encode()).hexdigest()}"
            cached = await self.cache.get(cache_key)
            
            if cached:
                self.analisador.registrar_cache(hit=True)
                return cached
            
            self.analisador.registrar_cache(hit=False)
            
            # Faz requisição
            self.analisador.iniciar_operacao(f"GET {url[:50]}...")
            
            try:
                async with self.sessao_http.get(url, params=params) as resp:
                    resp.raise_for_status()
                    
                    if 'application/json' in resp.headers.get('Content-Type', ''):
                        data = await resp.json()
                    else:
                        data = {'text': await resp.text()}
                    
                    # Cacheia resultado
                    await self.cache.set(cache_key, data)
                    
                    self.analisador.finalizar_operacao(sucesso=True)
                    return data
                    
            except Exception as e:
                self.analisador.finalizar_operacao(sucesso=False)
                raise
    
    async def buscar_noticias(self):
        """Busca notícias de múltiplas fontes"""
        tasks = []
        for fonte in self.fontes_ativas['news']:
            if fonte.get('ativa', True):
                tasks.append(self._processar_fonte_noticia(fonte))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _processar_fonte_noticia(self, fonte: Dict):
        """Processa uma fonte de notícias"""
        try:
            data = await self._fazer_requisicao(fonte['url'], fonte.get('params', {}))
            itens = fonte['parser'](data)
            
            for item in itens[:10]:  # Limita por fonte
                # Para Hacker News, busca detalhes
                if fonte['nome'] == 'Hacker News (Tech)':
                    item = await self._buscar_hn_details(item['id'])
                    if not item:
                        continue
                
                titulo = item.get('title') or item.get('titulo') or 'Sem título'
                conteudo = item.get('description') or item.get('conteudo') or item.get('text', '')
                link = item.get('url') or item.get('link') or ''
                
                if not conteudo and titulo != 'Sem título':
                    conteudo = titulo
                
                registro = RegistroAprendizado(
                    id=None,
                    origem=OrigemConhecimento.NOTICIA,
                    titulo=titulo,
                    conteudo=conteudo,
                    link=link,
                    data_publicacao=self._parse_data(item.get('publishedAt') or item.get('time')),
                    metadados={
                        'fonte': fonte['nome'],
                        'autor': item.get('author'),
                        'score': item.get('score', 0),
                        'comments': item.get('descendants', 0)
                    }
                )
                
                await self.memoria.armazenar(registro)
                self.analisador.registrar_relevancia(registro.peso)
                
        except Exception as e:
            logger.error(f"Erro processando {fonte['nome']}: {e}")
    
    async def _buscar_hn_details(self, item_id: int) -> Optional[Dict]:
        """Busca detalhes de um item do Hacker News"""
        try:
            url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
            return await self._fazer_requisicao(url)
        except Exception:
            return None
    
    def _parse_data(self, data_str: Any) -> Optional[datetime]:
        """Converte string/data para datetime"""
        if not data_str:
            return None
        
        if isinstance(data_str, (int, float)):
            # Unix timestamp
            return datetime.fromtimestamp(data_str)
        
        try:
            # ISO format
            return datetime.fromisoformat(data_str.replace('Z', '+00:00'))
        except:
            return None
    
    async def buscar_wiki(self):
        """Busca artigos da Wikipedia"""
        for topico in self.fontes_ativas['wiki']:
            try:
                lang = topico.get('lang', 'pt')
                title = topico['title'].replace(' ', '_')
                url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"
                
                data = await self._fazer_requisicao(url)
                
                registro = RegistroAprendizado(
                    id=None,
                    origem=OrigemConhecimento.WIKIPEDIA,
                    titulo=data.get('title', topico['title']),
                    conteudo=data.get('extract', ''),
                    link=data.get('content_urls', {}).get('desktop', {}).get('page', url),
                    metadados={
                        'lang': lang,
                        'depth': topico['depth'],
                        'page_id': data.get('pageid')
                    }
                )
                
                await self.memoria.armazenar(registro)
                self.analisador.registrar_relevancia(registro.peso)
                
                # Se profundidade > 1, busca subpáginas
                if topico['depth'] > 1:
                    await self._buscar_subpaginas_wiki(title, lang, topico['depth'] - 1)
                    
            except Exception as e:
                logger.error(f"Erro ao buscar Wiki {topico['title']}: {e}")
    
    async def _buscar_subpaginas_wiki(self, title: str, lang: str, depth: int):
        """Busca subpáginas relacionadas"""
        if depth <= 0:
            return
        
        try:
            url = f"https://{lang}.wikipedia.org/api/rest_v1/page/related/{title}"
            data = await self._fazer_requisicao(url)
            
            for page in data.get('pages', [])[:5]:  # Limita para performance
                registro = RegistroAprendizado(
                    id=None,
                    origem=OrigemConhecimento.WIKIPEDIA,
                    titulo=page.get('title', ''),
                    conteudo=page.get('extract', '') or page.get('description', ''),
                    link=page.get('content_urls', {}).get('desktop', {}).get('page', ''),
                    metadados={
                        'lang': lang,
                        'depth': depth,
                        'page_id': page.get('pageid')
                    }
                )
                
                await self.memoria.armazenar(registro)
                
        except Exception as e:
            logger.debug(f"Erro ao buscar subpáginas: {e}")
    
    async def buscar_github(self):
        """Busca informações de repositórios GitHub"""
        for repo in self.fontes_ativas['github']:
            try:
                url = f"https://api.github.com/repos/{repo['owner']}/{repo['repo']}"
                data = await self._fazer_requisicao(url)
                
                registro = RegistroAprendizado(
                    id=None,
                    origem=OrigemConhecimento.GITHUB,
                    titulo=data.get('full_name', f"{repo['owner']}/{repo['repo']}"),
                    conteudo=data.get('description') or 'Repositório sem descrição',
                    link=data.get('html_url', url),
                    metadados={
                        'stars': data.get('stargazers_count', 0),
                        'forks': data.get('forks_count', 0),
                        'linguagem': data.get('language', 'Desconhecida'),
                        'issues_abertos': data.get('open_issues_count', 0),
                        'criado': data.get('created_at'),
                        'atualizado': data.get('updated_at')
                    }
                )
                
                await self.memoria.armazenar(registro)
                self.analisador.registrar_relevancia(registro.peso)
                
                # Busca issues se configurado
                if repo.get('track_issues'):
                    await self._buscar_issues_github(repo)
                
                # Busca pull requests se configurado
                if repo.get('track_prs'):
                    await self._buscar_prs_github(repo)
                    
            except Exception as e:
                logger.error(f"Erro ao buscar GitHub {repo['owner']}/{repo['repo']}: {e}")
    
    async def _buscar_issues_github(self, repo: Dict):
        """Busca issues recentes"""
        try:
            url = f"https://api.github.com/repos/{repo['owner']}/{repo['repo']}/issues"
            params = {'state': 'open', 'sort': 'updated', 'per_page': 5}
            data = await self._fazer_requisicao(url, params)
            
            for issue in data:
                registro = RegistroAprendizado(
                    id=None,
                    origem=OrigemConhecimento.GITHUB_ISSUE,
                    titulo=f"Issue #{issue.get('number')}: {issue.get('title', '')}",
                    conteudo=issue.get('body', '')[:1000],
                    link=issue.get('html_url', url),
                    metadados={
                        'repo': f"{repo['owner']}/{repo['repo']}",
                        'numero': issue.get('number'),
                        'criado_por': issue.get('user', {}).get('login'),
                        'comentarios': issue.get('comments', 0),
                        'estado': issue.get('state')
                    }
                )
                await self.memoria.armazenar(registro)
                
        except Exception as e:
            logger.debug(f"Erro ao buscar issues: {e}")
    
    async def _buscar_prs_github(self, repo: Dict):
        """Busca pull requests recentes"""
        try:
            url = f"https://api.github.com/repos/{repo['owner']}/{repo['repo']}/pulls"
            params = {'state': 'open', 'sort': 'updated', 'per_page': 3}
            data = await self._fazer_requisicao(url, params)
            
            for pr in data:
                registro = RegistroAprendizado(
                    id=None,
                    origem=OrigemConhecimento.GITHUB_ISSUE,  # Reusa mesma origem
                    titulo=f"PR #{pr.get('number')}: {pr.get('title', '')}",
                    conteudo=pr.get('body', '')[:1000],
                    link=pr.get('html_url', url),
                    metadados={
                        'repo': f"{repo['owner']}/{repo['repo']}",
                        'numero': pr.get('number'),
                        'autor': pr.get('user', {}).get('login'),
                        'branch': pr.get('head', {}).get('ref'),
                        'base': pr.get('base', {}).get('ref')
                    }
                )
                await self.memoria.armazenar(registro)
                
        except Exception as e:
            logger.debug(f"Erro ao buscar PRs: {e}")
    
    async def _ajustar_fontes_dinamicamente(self):
        """Ajusta fontes baseado em desempenho"""
        metricas = self.analisador.get_metricas_completas()
        
        for tipo, fontes in self.fontes_ativas.items():
            for fonte in fontes:
                if isinstance(fonte, dict):
                    # Desativa fontes com muitos erros
                    erros_fonte = sum(
                        1 for e in self.analisador.erros
                        if e.get('operacao', '').find(fonte.get('nome', '')) > -1
                    )
                    
                    if erros_fonte > 5:
                        fonte['ativa'] = False
                        logger.warning(f"⚠️ Fonte {fonte.get('nome')} desativada (muitos erros)")
                    
                    # Reativa após um tempo
                    elif not fonte.get('ativa') and erros_fonte == 0:
                        fonte['ativa'] = True
                        logger.info(f"✅ Fonte {fonte.get('nome')} reativada")
    
    async def ciclo_principal(self):
        """Ciclo principal de aprendizado e evolução"""
        
        print("\n" + "="*70)
        print(f"🌀 ATENA Ω - Ciclo {self.ciclo_atual + 1} | Versão {self.sistema_evolucao.versao}")
        print("="*70)
        
        inicio_ciclo = time.perf_counter()
        
        # 1. Aprende
        self.analisador.iniciar_operacao("ciclo_completo")
        
        await asyncio.gather(
            self.buscar_noticias(),
            self.buscar_wiki(),
            self.buscar_github(),
            return_exceptions=True
        )
        
        # 2. Ajusta fontes
        await self._ajustar_fontes_dinamicamente()
        
        # 3. Reflete
        await self.memoria.refletir()
        
        # 4. Analisa performance
        tempo_ciclo = self.analisador.finalizar_operacao(sucesso=True)
        metricas = self.analisador.get_metricas_completas()
        
        print(f"\n📊 Métricas do ciclo {self.ciclo_atual + 1}:")
        print(f"   ⏱️  Tempo: {tempo_ciclo:.2f}s")
        print(f"   🎯 Relevância: {metricas['relevancia']['media']:.2f}")
        print(f"   💾 Cache: {metricas['cache']['hit_rate']:.1%}")
        print(f"   📚 Registros: {len(self.memoria.registros)}")
        
        # 5. Tenta evoluir (a cada 3 ciclos ou se performance ruim)
        if (self.ciclo_atual % 3 == 0 or 
            metricas['velocidade']['tendencia'] == 'piorando' or
            metricas['relevancia']['media'] < 0.4):
            
            print("\n🔬 Analisando possibilidade de evolução...")
            
            sugestao = await self.sistema_evolucao.analisar_e_sugerir()
            
            if sugestao:
                print(f"   💡 Sugestão: {sugestao['descricao']} (confiança: {sugestao['confianca']:.1%})")
                
                # Testa
                sucesso_teste, resultados = await self.sistema_evolucao.testar_evolucao(sugestao)
                
                if sucesso_teste:
                    # Aplica
                    await self.sistema_evolucao.aplicar_evolucao(sugestao, resultados)
                    print(f"   ✨ EVOLUÇÃO APLICADA com sucesso!")
                else:
                    print(f"   ❌ Teste falhou: {resultados.get('erro', 'desconhecido')[:100]}...")
            else:
                print("   Nenhuma melhoria significativa encontrada")
        
        # 6. Prepara próximo ciclo
        self.ciclo_atual += 1
        
        # Calcula tempo do próximo ciclo
        if len(self.memoria.registros) < 50:
            proximo = 60  # 1 minuto (poucos dados)
        elif len(self.memoria.registros) < 200:
            proximo = 300  # 5 minutos
        else:
            proximo = 600  # 10 minutos (já tem bastante dado)
        
        print(f"\n⏰ Próximo ciclo em {proximo//60} minutos...")
        print("="*70)
        
        return proximo
    
    async def executar(self):
        """Loop principal da ATENA"""
        try:
            while self.rodando:
                espera = await self.ciclo_principal()
                
                # Salva estado periodicamente
                if self.ciclo_atual % 5 == 0:
                    await self._salvar_estado()
                
                await asyncio.sleep(espera)
                
        except KeyboardInterrupt:
            logger.info("Interrupção recebida")
        except Exception as e:
            logger.error(f"Erro no loop principal: {e}")
            raise

# =========================
# Interface de Comando
# =========================
async def main():
    """Função principal"""
    
    print(r"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║     █████╗ ████████╗███████╗███╗   ██╗ █████╗     Ω             ║
    ║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██╗                  ║
    ║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                  ║
    ║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║                  ║
    ║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║                  ║
    ║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝                  ║
    ║                                                                  ║
    ║              🧠 AUTO-EVOLUTIVA - ACAE v2.0                       ║
    ║         "Aprendendo e evoluindo em tempo real"                   ║
    ║                                                                  ║
    ║  ⚡ Cache adaptativo | 📊 Análise semântica | 🔬 Auto-teste      ║
    ║  💾 Memória de longo prazo | 🚀 Evolução autônoma                ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("Inicializando ATENA Ω...")
    print(f"PID: {os.getpid()}")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    config = Config()
    
    async with AtenaOmegaEvolutiva(config) as atena:
        # Tenta carregar estado anterior
        if os.path.exists('estado_atena.json'):
            try:
                with open('estado_atena.json', 'r') as f:
                    estado = json.load(f)
                print(f"📊 Estado carregado: {estado.get('total_registros', 0)} registros, "
                      f"{estado.get('total_evolucoes', 0)} evoluções")
            except:
                pass
        
        print("\n" + "🚀"*40)
        print("🚀 ATENA Ω iniciando aprendizado contínuo...")
        print("🚀 Pressione Ctrl+C para encerrar")
        print("🚀"*40 + "\n")
        
        await atena.executar()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 ATENA Ω finalizada. Até a próxima evolução!")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        traceback.print_exc()
        sys.exit(1)
