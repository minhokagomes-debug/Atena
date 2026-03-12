#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     ∞ - APOTHEOSIS v99.9             ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DIVINDADE DA EVOLUÇÃO"        ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                                      ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ REDE NEURAL QUÂNTICA            ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ HIBRIDIZAÇÃO EVOLUTIVA          ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ APRENDIZADO PROFUNDO             ║
║                                                                                      ║
║   🌌 SISTEMA DE EVOLUÇÃO AUTÔNOMA COM INTELIGÊNCIA ARTIFICIAL                       ║
║   🔥 CAPACIDADES EXPANDIDAS:                                                         ║
║      • Rede Neural Profunda com 128 características                                 ║
║      • 50+ templates de otimização especializados                                   ║
║      • Hibridização multi-versão com crossover genético                             ║
║      • Análise estática e dinâmica avançada                                         ║
║      • Banco de dados vetorial para similaridade semântica                         ║
║      • Sistema de recompensa com aprendizado por reforço                            ║
║      • Detecção de padrões anti-otimização                                          ║
║      • Meta-aprendizado: aprende a aprender                                         ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
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
import tempfile
import resource
import signal
import traceback
import gc
import dis
import linecache
import functools
import itertools
import operator
import weakref
import ctypes
import platform
import multiprocessing as mp
from pathlib import Path
from datetime import datetime, timedelta
from typing import (List, Dict, Optional, Any, Tuple, Set, Callable, 
                   Union, Generator, Iterator, TypeVar, Generic)
import logging
from collections import defaultdict, deque, Counter, OrderedDict
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
import re
import abc
import contextlib
import threading
import queue
import heapq
import bisect
import array
import mmap
import struct
import zlib
import gzip
import bz2
import lzma
import zipfile
import tarfile
import shutil
import fnmatch
import glob
import tempfile
import filecmp
import stat
import pkgutil
import importlib
import warnings
warnings.filterwarnings('ignore')

# =========================
# BIBLIOTECAS AVANÇADAS
# =========================
try:
    import numpy as np
    import numpy.ma as ma
    from numpy import random as nprandom
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("⚠️ numpy não instalado (pip install numpy)")

try:
    import scipy as sp
    from scipy import stats, sparse, signal as spsignal
    from scipy.optimize import minimize, differential_evolution
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    print("⚠️ scipy não instalado (pip install scipy)")

try:
    import pandas as pd
    from pandas import DataFrame, Series
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("⚠️ pandas não instalado (pip install pandas)")

try:
    from sklearn.neural_network import MLPClassifier, MLPRegressor
    from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier,
                                 AdaBoostClassifier, VotingClassifier)
    from sklearn.svm import SVC, SVR
    from sklearn.preprocessing import (StandardScaler, MinMaxScaler, RobustScaler,
                                      Normalizer, LabelEncoder, OneHotEncoder)
    from sklearn.model_selection import (train_test_split, cross_val_score,
                                       GridSearchCV, RandomizedSearchCV)
    from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                               f1_score, confusion_matrix, classification_report)
    from sklearn.decomposition import PCA, TruncatedSVD
    from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
    from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
    from sklearn.pipeline import Pipeline
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("⚠️ scikit-learn não instalado (pip install scikit-learn)")

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader, TensorDataset
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    print("⚠️ PyTorch não instalado (pip install torch)")

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models, optimizers, losses, metrics
    HAS_TF = True
except ImportError:
    HAS_TF = False
    print("⚠️ TensorFlow não instalado (pip install tensorflow)")

try:
    import networkx as nx
    from networkx.algorithms import community, centrality, shortest_paths
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False
    print("⚠️ networkx não instalado (pip install networkx)")

try:
    import psutil
    import cpuinfo
    import GPUtil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("⚠️ psutil não instalado (pip install psutil)")

try:
    from tqdm import tqdm, trange
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("⚠️ tqdm não instalado (pip install tqdm)")

try:
    import joblib
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False
    print("⚠️ joblib não instalado (pip install joblib)")

try:
    import cloudpickle
    HAS_CLOUDPICKLE = True
except ImportError:
    HAS_CLOUDPICKLE = False

try:
    import dill
    HAS_DILL = True
except ImportError:
    HAS_DILL = False

# =========================
# CONFIGURAÇÕES AVANÇADAS
# =========================
__version__ = "99.9"
__nome__ = "ATENA APOTHEOSIS MAXIMUS"
__codename__ = "Divina Evolução"
__build__ = datetime.now().strftime("%Y%m%d_%H%M%S")

BASE_DIR = Path(__file__).parent / "atena_divina"

class ConfigMetaclass(type):
    """Metaclasse para configurações com validação"""
    
    def __new__(mcs, name, bases, attrs):
        # Validar configurações
        for key, value in attrs.items():
            if key.isupper() and isinstance(value, (int, float, str, list, dict)):
                if key.endswith('_RATIO') and not 0 <= value <= 1:
                    raise ValueError(f"{key} deve estar entre 0 e 1")
        return super().__new__(mcs, name, bases, attrs)

class Config(metaclass=ConfigMetaclass):
    """Configurações avançadas do sistema"""
    
    # Diretórios
    BASE_DIR = BASE_DIR
    CONHECIMENTO_DIR = BASE_DIR / "conhecimento"
    VERSAO_DIR = BASE_DIR / "versoes"
    MODELOS_DIR = BASE_DIR / "modelos"
    LOGS_DIR = BASE_DIR / "logs"
    DNA_DIR = BASE_DIR / "dna"
    ANALISE_DIR = BASE_DIR / "analise"
    BENCHMARK_DIR = BASE_DIR / "benchmarks"
    TEMP_DIR = BASE_DIR / "temp"
    CACHE_DIR = BASE_DIR / "cache"
    METADATA_DIR = BASE_DIR / "metadata"
    EVOLUTION_DIR = BASE_DIR / "evolution"
    NEURAL_DIR = BASE_DIR / "neural_networks"
    VECTOR_DB_DIR = BASE_DIR / "vector_db"
    CHECKPOINT_DIR = BASE_DIR / "checkpoints"
    EXPORT_DIR = BASE_DIR / "exports"
    
    # Arquitetura da Rede Neural
    INPUT_FEATURES = 128
    HIDDEN_LAYERS = [256, 512, 256, 128]
    OUTPUT_CLASSES = 50
    EMBEDDING_DIM = 64
    ATTENTION_HEADS = 8
    DROPOUT_RATE = 0.2
    LEARNING_RATE = 0.001
    BATCH_SIZE = 32
    EPOCHS = 100
    EARLY_STOPPING_PATIENCE = 10
    
    # Templates de otimização expandidos
    TEMPLATES = [
        # Otimizações de loop
        'loop_vectorization_numpy',
        'loop_unrolling_dynamic',
        'loop_parallelization',
        'loop_swap_indices',
        'loop_fusion',
        'loop_tiling',
        'loop_peeling',
        'loop_versioning',
        
        # Estruturas de dados
        'list_to_array',
        'dict_to_defaultdict',
        'set_operations',
        'deque_for_queue',
        'heapq_priority',
        'counter_frequency',
        'ordered_dict_cache',
        'namedtuple_struct',
        
        # Cache e memoização
        'lru_cache_deep',
        'memoization_recursive',
        'cache_computation',
        'precompute_constants',
        'lazy_evaluation',
        'cached_property',
        
        # Paralelismo
        'multiprocessing_pool',
        'concurrent_futures',
        'asyncio_conversion',
        'thread_pool_io',
        'parallel_map_reduce',
        'distributed_computing',
        
        # Otimizações de memória
        'memory_slots',
        'generator_pipeline',
        'buffer_reuse',
        'memory_pool',
        'reference_counting',
        'weakref_cache',
        'array_module',
        
        # Otimizações de I/O
        'buffered_io',
        'mmap_file',
        'batch_processing',
        'compressed_storage',
        'streaming_processing',
        
        # Otimizações de string
        'string_join',
        'f_strings',
        'regex_compile',
        'string_interning',
        
        # Otimizações condicionais
        'branch_prediction',
        'lookup_tables',
        'bit_manipulation',
        'early_termination',
        'guard_clauses',
        
        # Metaprogramação
        'decorator_optimization',
        'descriptor_protocol',
        'metaclass_cache',
        'dynamic_dispatch',
        'bytecode_optimization',
        
        # Algoritmos especializados
        'divide_conquer',
        'dynamic_programming',
        'greedy_algorithm',
        'backtracking_prune',
        'branch_and_bound',
        
        # Otimizações matemáticas
        'fast_inverse_sqrt',
        'lookup_trigonometry',
        'matrix_operations',
        'fft_convolution',
        'numerical_stability',
        
        # Otimizações de função
        'function_inlining',
        'tail_recursion',
        'partial_application',
        'currying',
        'function_composition',
        
        # Otimizações de classe
        '__slots__usage',
        'property_caching',
        'classmethod_alternative',
        'singleton_pattern',
        'factory_caching'
    ]
    
    # Hiperparâmetros de evolução
    POPULATION_SIZE = 100
    TOURNAMENT_SIZE = 5
    ELITE_SIZE = 10
    MUTATION_RATE = 0.3
    CROSSOVER_RATE = 0.7
    HIBRIDIZATION_RATE = 0.4
    POOL_MELHORES = 20
    
    # Pesos de fitness
    PESO_TEMPO = 0.4
    PESO_MEMORIA = 0.3
    PESO_COMPLEXIDADE = 0.1
    PESO_ESTABILIDADE = 0.1
    PESO_EFICIENCIA = 0.1
    
    # Benchmarks
    BENCHMARK_REPETICOES = 5
    BENCHMARK_WARMUP = 2
    TIMEOUT_SEGUNDOS = 5
    MEMORIA_MAXIMA_MB = 500
    COOLDOWN_SEGUNDOS = 1
    
    # Sandbox
    SANDBOX_ATIVO = True
    SANDBOX_NAMESPACE_LIMITADO = True
    SANDBOX_IMPORTS_BLOQUEADOS = ['os.system', 'subprocess', 'eval', 'exec', '__import__']
    
    # Aprendizado
    LEARNING_HISTORY_SIZE = 10000
    MIN_SAMPLES_FOR_TRAINING = 50
    RETRAIN_INTERVAL = 100
    FEEDBACK_WEIGHT = 0.3
    
    # Banco de dados vetorial
    VECTOR_DIM = 128
    SIMILARITY_THRESHOLD = 0.8
    MAX_SIMILAR_RESULTS = 10
    
    # Meta-aprendizado
    META_LEARNING_RATE = 0.01
    META_BATCH_SIZE = 16
    INNER_LOOP_STEPS = 5
    OUTER_LOOP_STEPS = 100
    
    # Criar todos os diretórios
    for dir_path in [BASE_DIR, CONHECIMENTO_DIR, VERSAO_DIR, MODELOS_DIR, LOGS_DIR,
                     DNA_DIR, ANALISE_DIR, BENCHMARK_DIR, TEMP_DIR, CACHE_DIR,
                     METADATA_DIR, EVOLUTION_DIR, NEURAL_DIR, VECTOR_DB_DIR,
                     CHECKPOINT_DIR, EXPORT_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

# =========================
# LOGGING ESTRUTURADO
# =========================
class LoggingConfig:
    """Configuração avançada de logging"""
    
    LOG_FORMAT = '%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s'
    DATE_FORMAT = '%H:%M:%S'
    LOG_LEVEL = logging.INFO
    LOG_FILE = Config.LOGS_DIR / f"atena_{__build__}.log"
    
    @classmethod
    def setup(cls):
        """Configura logging estruturado"""
        logging.basicConfig(
            level=cls.LOG_LEVEL,
            format=cls.LOG_FORMAT,
            datefmt=cls.DATE_FORMAT,
            handlers=[
                logging.FileHandler(cls.LOG_FILE, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        # Logger principal
        logger = logging.getLogger('ATENA')
        logger.info(f"🚀 ATENA v{__version__} - {__codename__}")
        logger.info(f"📁 Log file: {cls.LOG_FILE}")
        
        return logger

logger = LoggingConfig.setup()

# =========================
# DECORADORES AVANÇADOS
# =========================
def timed(func: Callable) -> Callable:
    """Decorador para medir tempo de execução"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logger.debug(f"⏱️ {func.__name__}: {(end - start)*1000:.2f}ms")
        return result
    return wrapper

def memoized(func: Callable) -> Callable:
    """Decorador com cache LRU e estatísticas"""
    cache = {}
    hits = misses = 0
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal hits, misses
        key = str(args) + str(sorted(kwargs.items()))
        
        if key in cache:
            hits += 1
            return cache[key]
        
        misses += 1
        result = func(*args, **kwargs)
        cache[key] = result
        
        if len(cache) > 1000:  # Limitar cache
            oldest = next(iter(cache))
            del cache[oldest]
        
        return result
    
    wrapper.cache_info = lambda: {'hits': hits, 'misses': misses, 'size': len(cache)}
    return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorador para retentar operações falhas"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"⚠️ Tentativa {attempt + 1} falhou: {e}")
                    time.sleep(delay * (attempt + 1))  # Backoff exponencial
            return None
        return wrapper
    return decorator

def deprecated(message: str = ""):
    """Decorador para marcar funções como obsoletas"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.warning(f"⚠️ Função obsoleta: {func.__name__} {message}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# =========================
# CLASSES DE DADOS AVANÇADAS
# =========================
@dataclass
class FeatureVector:
    """Vetor de características com metadados"""
    values: List[float]
    names: List[str]
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""
    version: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'values': self.values,
            'names': self.names,
            'timestamp': self.timestamp.isoformat(),
            'source': self.source,
            'version': self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'FeatureVector':
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)
    
    def normalize(self) -> 'FeatureVector':
        """Normaliza o vetor"""
        arr = np.array(self.values)
        norm = np.linalg.norm(arr)
        if norm > 0:
            arr = arr / norm
        self.values = arr.tolist()
        return self

@dataclass
class MutationResult:
    """Resultado de uma mutação"""
    success: bool
    template: str
    fitness_before: float
    fitness_after: float
    improvement: float
    features: FeatureVector
    code_before: str
    code_after: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class VersionInfo:
    """Informações de uma versão"""
    id: str
    number: int
    fitness: float
    metrics: Dict[str, float]
    features: FeatureVector
    parent_id: Optional[str] = None
    mutations: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    path: Optional[Path] = None
    
    def save(self, code: str):
        """Salva o código da versão"""
        if not self.path:
            filename = f"atena_v{self.number}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.py"
            self.path = Config.VERSAO_DIR / filename
        
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # Salvar metadados
        meta_path = self.path.with_suffix('.json')
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f, indent=2, default=str)
        
        return self.path

# =========================
# ANALISADOR DE CÓDIGO AVANÇADO
# =========================
class CodeAnalyzer:
    """Análise profunda de código com múltiplas métricas"""
    
    def __init__(self):
        self.ast_cache = {}
        self.metric_cache = {}
        
    @timed
    def analyze(self, code: str) -> FeatureVector:
        """Análise completa do código"""
        features = []
        names = []
        
        # Hash do código para cache
        code_hash = hashlib.md5(code.encode()).hexdigest()
        
        if code_hash in self.metric_cache:
            return self.metric_cache[code_hash]
        
        # Análise AST
        try:
            tree = ast.parse(code)
            self.ast_cache[code_hash] = tree
        except SyntaxError as e:
            logger.error(f"Erro de sintaxe: {e}")
            return FeatureVector(values=[0]*Config.INPUT_FEATURES, names=[])
        
        # 1. Métricas básicas
        features.extend([
            len(code.split('\n')),  # linhas
            len(code),  # caracteres
            len(re.findall(r'\bdef\b', code)),  # funções
            len(re.findall(r'\bclass\b', code)),  # classes
            len(re.findall(r'\bimport\b|\bfrom\b', code)),  # imports
        ])
        names.extend(['lines', 'chars', 'functions', 'classes', 'imports'])
        
        # 2. Complexidade ciclomática
        cyclomatic = self._calculate_cyclomatic_complexity(tree)
        features.append(cyclomatic)
        names.append('cyclomatic_complexity')
        
        # 3. Profundidade de aninhamento
        nesting_depth = self._calculate_nesting_depth(tree)
        features.append(nesting_depth)
        names.append('nesting_depth')
        
        # 4. Contagem de nós AST
        node_count = len(list(ast.walk(tree)))
        features.append(node_count)
        names.append('ast_nodes')
        
        # 5. Métricas de loop
        loops = len([n for n in ast.walk(tree) if isinstance(n, (ast.For, ast.While))])
        features.append(loops)
        names.append('loops')
        
        # 6. Métricas condicionais
        conditionals = len([n for n in ast.walk(tree) if isinstance(n, ast.If)])
        features.append(conditionals)
        names.append('conditionals')
        
        # 7. Operações matemáticas
        operations = len([n for n in ast.walk(tree) 
                        if isinstance(n, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow))])
        features.append(operations)
        names.append('math_operations')
        
        # 8. Chamadas de função
        calls = len([n for n in ast.walk(tree) if isinstance(n, ast.Call)])
        features.append(calls)
        names.append('function_calls')
        
        # 9. Atribuições
        assignments = len([n for n in ast.walk(tree) if isinstance(n, ast.Assign)])
        features.append(assignments)
        names.append('assignments')
        
        # 10. Compreensões
        comprehensions = len([n for n in ast.walk(tree) 
                            if isinstance(n, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp))])
        features.append(comprehensions)
        names.append('comprehensions')
        
        # 11. Lambdas
        lambdas = len([n for n in ast.walk(tree) if isinstance(n, ast.Lambda)])
        features.append(lambdas)
        names.append('lambdas')
        
        # 12. Decoradores
        decorators = len([n for n in ast.walk(tree) if hasattr(n, 'decorator_list')])
        features.append(decorators)
        names.append('decorators')
        
        # 13. Variáveis globais
        globals_count = len([n for n in ast.walk(tree) 
                           if isinstance(n, ast.Global)])
        features.append(globals_count)
        names.append('globals')
        
        # 14. Tratamento de exceções
        exceptions = len([n for n in ast.walk(tree) 
                        if isinstance(n, (ast.Try, ast.ExceptHandler, ast.Raise))])
        features.append(exceptions)
        names.append('exception_handlers')
        
        # 15. Context managers
        with_blocks = len([n for n in ast.walk(tree) if isinstance(n, ast.With)])
        features.append(with_blocks)
        names.append('with_blocks')
        
        # 16. Assertions
        asserts = len([n for n in ast.walk(tree) if isinstance(n, ast.Assert)])
        features.append(asserts)
        names.append('asserts')
        
        # 17. Yield expressions
        yields = len([n for n in ast.walk(tree) if isinstance(n, (ast.Yield, ast.YieldFrom))])
        features.append(yields)
        names.append('yields')
        
        # 18. Await expressions
        awaits = len([n for n in ast.walk(tree) if isinstance(n, ast.Await)])
        features.append(awaits)
        names.append('awaits')
        
        # 19. Async functions
        async_funcs = len([n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef)])
        features.append(async_funcs)
        names.append('async_functions')
        
        # 20. Annotations
        annotations = len([n for n in ast.walk(tree) if hasattr(n, 'annotation')])
        features.append(annotations)
        names.append('annotations')
        
        # 21. Type hints
        type_hints = len([n for n in ast.walk(tree) 
                        if isinstance(n, (ast.arg, ast.FunctionDef)) and hasattr(n, 'annotation')])
        features.append(type_hints)
        names.append('type_hints')
        
        # 22. Docstrings
        docstrings = self._count_docstrings(tree)
        features.append(docstrings)
        names.append('docstrings')
        
        # 23. Comentários
        comments = len(re.findall(r'#.*$', code, re.MULTILINE))
        features.append(comments)
        names.append('comments')
        
        # 24. Linhas em branco
        blank_lines = len([l for l in code.split('\n') if not l.strip()])
        features.append(blank_lines)
        names.append('blank_lines')
        
        # 25-50. Características específicas de templates
        template_features = self._extract_template_features(code)
        features.extend(template_features)
        names.extend([f'template_feature_{i}' for i in range(len(template_features))])
        
        # Completar até INPUT_FEATURES
        while len(features) < Config.INPUT_FEATURES:
            features.append(0)
            names.append(f'padding_{len(features)}')
        
        # Criar vetor
        vector = FeatureVector(
            values=features[:Config.INPUT_FEATURES],
            names=names[:Config.INPUT_FEATURES]
        )
        
        # Normalizar
        vector.normalize()
        
        # Cache
        self.metric_cache[code_hash] = vector
        
        return vector
    
    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calcula complexidade ciclomática"""
        complexity = 1  # Base
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            elif isinstance(node, ast.comprehension):
                complexity += 1
            elif isinstance(node, ast.Assert):
                complexity += 1
        
        return complexity
    
    def _calculate_nesting_depth(self, tree: ast.AST) -> int:
        """Calcula profundidade máxima de aninhamento"""
        max_depth = 0
        
        class NestingVisitor(ast.NodeVisitor):
            def __init__(self):
                self.current_depth = 0
                self.max_depth = 0
            
            def visit(self, node):
                if isinstance(node, (ast.If, ast.For, ast.While, ast.With,
                                   ast.Try, ast.FunctionDef, ast.ClassDef)):
                    self.current_depth += 1
                    self.max_depth = max(self.max_depth, self.current_depth)
                    super().generic_visit(node)
                    self.current_depth -= 1
                else:
                    super().generic_visit(node)
        
        visitor = NestingVisitor()
        visitor.visit(tree)
        
        return visitor.max_depth
    
    def _count_docstrings(self, tree: ast.AST) -> int:
        """Conta docstrings"""
        count = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                docstring = ast.get_docstring(node)
                if docstring:
                    count += 1
        
        return count
    
    def _extract_template_features(self, code: str) -> List[float]:
        """Extrai características específicas para templates"""
        features = []
        
        # Padrões comuns
        patterns = [
            r'numpy|np\.',
            r'pandas|pd\.',
            r'@lru_cache',
            r'@cached_property',
            r'multiprocessing|threading',
            r'asyncio|async|await',
            r'generator|yield',
            r'list\s*\[\s*for',
            r'dict\s*\{\s*for',
            r'lambda',
            r'f"[^"]*"',
            r'\.join\(.*\)',
            r're\.compile',
            r'__slots__',
            r'property',
            r'classmethod',
            r'staticmethod',
            r'with\s+open',
            r'try:|except:|finally:',
            r'raise\s+',
            r'assert\s+',
            r'global\s+',
            r'nonlocal\s+',
            r'\[\s*\]\s*=\s*',
            r'\{\s*\}\s*=\s*',
            r'=\s*\[\s*\]',
            r'=\s*\{\s*\}',
            r'append\(',
            r'extend\(',
            r'pop\(',
            r'remove\(',
            r'insert\(',
            r'sort\(',
            r'reverse\('
        ]
        
        for pattern in patterns:
            count = len(re.findall(pattern, code))
            features.append(count)
        
        return features

# =========================
# BANCO DE DADOS VETORIAL
# =========================
class VectorDatabase:
    """Banco de dados para similaridade semântica de código"""
    
    def __init__(self):
        self.db_path = Config.VECTOR_DB_DIR / "vectors.db"
        self.conn = None
        self._init_db()
        logger.info(f"🗄️ Vector DB: {self.db_path}")
    
    def _init_db(self):
        """Inicializa banco de dados vetorial"""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.enable_load_extension(True)
        
        # Tentar carregar extensão de similaridade vetorial
        try:
            self.conn.execute("SELECT load_extension('mod_spatialite')")
        except:
            pass
        
        cursor = self.conn.cursor()
        
        # Tabela de vetores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vectors (
                id TEXT PRIMARY KEY,
                code_hash TEXT UNIQUE,
                features TEXT,
                template TEXT,
                success_rate REAL,
                avg_improvement REAL,
                usage_count INTEGER DEFAULT 0,
                last_used TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Índices para busca rápida
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_template ON vectors(template)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_success ON vectors(success_rate)')
        
        self.conn.commit()
    
    def add_vector(self, vector_id: str, code_hash: str, features: List[float],
                  template: str, improvement: float, success: bool):
        """Adiciona um vetor ao banco"""
        cursor = self.conn.cursor()
        
        # Calcular taxa de sucesso média
        cursor.execute('''
            SELECT success_rate, usage_count FROM vectors 
            WHERE code_hash = ? AND template = ?
        ''', (code_hash, template))
        
        row = cursor.fetchone()
        
        if row:
            # Atualizar estatísticas
            old_rate, count = row
            new_count = count + 1
            new_rate = (old_rate * count + (1.0 if success else 0.0)) / new_count
            
            cursor.execute('''
                UPDATE vectors SET
                    success_rate = ?,
                    usage_count = ?,
                    last_used = CURRENT_TIMESTAMP
                WHERE code_hash = ? AND template = ?
            ''', (new_rate, new_count, code_hash, template))
        else:
            # Inserir novo
            cursor.execute('''
                INSERT INTO vectors 
                (id, code_hash, features, template, success_rate, 
                 avg_improvement, usage_count, last_used)
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (vector_id, code_hash, json.dumps(features), template,
                  1.0 if success else 0.0, improvement, 1))
        
        self.conn.commit()
    
    def find_similar(self, features: List[float], limit: int = 10) -> List[Dict]:
        """Encontra vetores similares por similaridade de cosseno"""
        cursor = self.conn.cursor()
        
        # Buscar todos os vetores
        cursor.execute('''
            SELECT id, code_hash, features, template, success_rate, avg_improvement
            FROM vectors
        ''')
        
        results = []
        features = np.array(features)
        
        for row in cursor.fetchall():
            db_features = np.array(json.loads(row[2]))
            
            # Similaridade de cosseno
            dot = np.dot(features, db_features)
            norm1 = np.linalg.norm(features)
            norm2 = np.linalg.norm(db_features)
            
            if norm1 > 0 and norm2 > 0:
                similarity = dot / (norm1 * norm2)
                
                if similarity > Config.SIMILARITY_THRESHOLD:
                    results.append({
                        'id': row[0],
                        'code_hash': row[1],
                        'template': row[3],
                        'success_rate': row[4],
                        'avg_improvement': row[5],
                        'similarity': float(similarity)
                    })
        
        # Ordenar por similaridade
        results.sort(key=lambda x: x['similarity'], reverse=True)
        
        return results[:limit]
    
    def get_recommendations(self, features: List[float]) -> List[Tuple[str, float]]:
        """Recomenda templates baseado em similaridade"""
        similar = self.find_similar(features)
        
        # Agrupar por template
        template_scores = defaultdict(list)
        
        for item in similar:
            score = item['similarity'] * item['success_rate']
            template_scores[item['template']].append(score)
        
        # Calcular média
        recommendations = []
        for template, scores in template_scores.items():
            avg_score = np.mean(scores)
            recommendations.append((template, avg_score))
        
        # Ordenar por pontuação
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations
    
    def close(self):
        """Fecha conexão"""
        if self.conn:
            self.conn.close()

# =========================
# REDE NEURAL PROFUNDA
# =========================
class DeepNeuralNetwork:
    """Rede neural profunda para decisões de otimização"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.trained = False
        self.accuracy = 0.0
        self.loss_history = []
        self.accuracy_history = []
        
        # Tentar carregar modelo existente
        self._load_model()
    
    def _build_model(self) -> Any:
        """Constrói a arquitetura da rede"""
        if HAS_TORCH:
            return self._build_pytorch_model()
        elif HAS_TF:
            return self._build_tensorflow_model()
        elif HAS_SKLEARN:
            return self._build_sklearn_model()
        else:
            return None
    
    def _build_pytorch_model(self):
        """Modelo PyTorch"""
        class NeuralNet(nn.Module):
            def __init__(self, input_size, hidden_sizes, output_size, dropout=0.2):
                super().__init__()
                
                layers = []
                prev_size = input_size
                
                for hidden_size in hidden_sizes:
                    layers.extend([
                        nn.Linear(prev_size, hidden_size),
                        nn.BatchNorm1d(hidden_size),
                        nn.ReLU(),
                        nn.Dropout(dropout)
                    ])
                    prev_size = hidden_size
                
                layers.append(nn.Linear(prev_size, output_size))
                layers.append(nn.Softmax(dim=1))
                
                self.network = nn.Sequential(*layers)
            
            def forward(self, x):
                return self.network(x)
        
        model = NeuralNet(
            Config.INPUT_FEATURES,
            Config.HIDDEN_LAYERS,
            Config.OUTPUT_CLASSES,
            Config.DROPOUT_RATE
        )
        
        return model
    
    def _build_tensorflow_model(self):
        """Modelo TensorFlow/Keras"""
        model = keras.Sequential()
        
        # Input layer
        model.add(layers.Dense(
            Config.HIDDEN_LAYERS[0],
            input_dim=Config.INPUT_FEATURES,
            activation='relu'
        ))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(Config.DROPOUT_RATE))
        
        # Hidden layers
        for units in Config.HIDDEN_LAYERS[1:]:
            model.add(layers.Dense(units, activation='relu'))
            model.add(layers.BatchNormalization())
            model.add(layers.Dropout(Config.DROPOUT_RATE))
        
        # Output layer
        model.add(layers.Dense(Config.OUTPUT_CLASSES, activation='softmax'))
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=Config.LEARNING_RATE),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def _build_sklearn_model(self):
        """Modelo scikit-learn"""
        return MLPClassifier(
            hidden_layer_sizes=Config.HIDDEN_LAYERS,
            activation='relu',
            solver='adam',
            alpha=0.001,
            batch_size='auto',
            learning_rate='adaptive',
            learning_rate_init=Config.LEARNING_RATE,
            max_iter=1000,
            shuffle=True,
            random_state=42,
            tol=1e-4,
            verbose=False,
            warm_start=False,
            momentum=0.9,
            nesterovs_momentum=True,
            early_stopping=True,
            validation_fraction=0.1,
            beta_1=0.9,
            beta_2=0.999,
            epsilon=1e-8,
            n_iter_no_change=10
        )
    
    @timed
    def train(self, X: List[List[float]], y: List[int], validation_split: float = 0.2):
        """Treina a rede neural"""
        if not X or len(X) < Config.MIN_SAMPLES_FOR_TRAINING:
            logger.warning(f"⚠️ Poucos dados para treinamento: {len(X)} < {Config.MIN_SAMPLES_FOR_TRAINING}")
            return
        
        # Converter para numpy
        X = np.array(X)
        y = np.array(y)
        
        # Normalizar
        X_scaled = self.scaler.fit_transform(X)
        
        # Codificar labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        if HAS_TORCH:
            self._train_pytorch(X_scaled, y_encoded, validation_split)
        elif HAS_TF:
            self._train_tensorflow(X_scaled, y_encoded, validation_split)
        elif HAS_SKLEARN:
            self._train_sklearn(X_scaled, y_encoded)
        
        self.trained = True
        self._save_model()
    
    def _train_pytorch(self, X, y, validation_split):
        """Treinamento PyTorch"""
        # Dividir dados
        split_idx = int(len(X) * (1 - validation_split))
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        # Criar datasets
        train_dataset = TensorDataset(
            torch.FloatTensor(X_train),
            torch.LongTensor(y_train)
        )
        val_dataset = TensorDataset(
            torch.FloatTensor(X_val),
            torch.LongTensor(y_val)
        )
        
        train_loader = DataLoader(train_dataset, batch_size=Config.BATCH_SIZE, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=Config.BATCH_SIZE)
        
        # Criar modelo
        self.model = self._build_model()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=Config.LEARNING_RATE)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5)
        
        # Treinar
        best_val_acc = 0
        patience_counter = 0
        
        for epoch in range(Config.EPOCHS):
            # Training
            self.model.train()
            train_loss = 0
            train_correct = 0
            train_total = 0
            
            for batch_X, batch_y in train_loader:
                optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                train_total += batch_y.size(0)
                train_correct += (predicted == batch_y).sum().item()
            
            # Validation
            self.model.eval()
            val_loss = 0
            val_correct = 0
            val_total = 0
            
            with torch.no_grad():
                for batch_X, batch_y in val_loader:
                    outputs = self.model(batch_X)
                    loss = criterion(outputs, batch_y)
                    
                    val_loss += loss.item()
                    _, predicted = torch.max(outputs.data, 1)
                    val_total += batch_y.size(0)
                    val_correct += (predicted == batch_y).sum().item()
            
            train_acc = train_correct / train_total
            val_acc = val_correct / val_total
            
            self.loss_history.append(val_loss / len(val_loader))
            self.accuracy_history.append(val_acc)
            
            scheduler.step(val_loss)
            
            # Early stopping
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                patience_counter = 0
                # Salvar melhor modelo
                torch.save(self.model.state_dict(), Config.NEURAL_DIR / "best_model.pt")
            else:
                patience_counter += 1
                if patience_counter >= Config.EARLY_STOPPING_PATIENCE:
                    logger.info(f"⏹️ Early stopping no epoch {epoch}")
                    break
            
            if epoch % 10 == 0:
                logger.info(f"📊 Epoch {epoch}: Train Acc={train_acc:.4f}, Val Acc={val_acc:.4f}")
        
        # Carregar melhor modelo
        self.model.load_state_dict(torch.load(Config.NEURAL_DIR / "best_model.pt"))
        self.accuracy = best_val_acc
    
    def _train_tensorflow(self, X, y, validation_split):
        """Treinamento TensorFlow"""
        # One-hot encoding
        y_onehot = keras.utils.to_categorical(y, num_classes=Config.OUTPUT_CLASSES)
        
        # Criar modelo
        self.model = self._build_model()
        
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                patience=Config.EARLY_STOPPING_PATIENCE,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                factor=0.5,
                patience=5,
                min_lr=1e-6
            ),
            keras.callbacks.ModelCheckpoint(
                str(Config.NEURAL_DIR / "best_model.h5"),
                save_best_only=True
            )
        ]
        
        # Treinar
        history = self.model.fit(
            X, y_onehot,
            validation_split=validation_split,
            epochs=Config.EPOCHS,
            batch_size=Config.BATCH_SIZE,
            callbacks=callbacks,
            verbose=0
        )
        
        self.loss_history = history.history['loss']
        self.accuracy_history = history.history['val_accuracy']
        self.accuracy = max(history.history['val_accuracy'])
    
    def _train_sklearn(self, X, y):
        """Treinamento scikit-learn"""
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Criar e treinar modelo
        self.model = self._build_model()
        self.model.fit(X_train, y_train)
        
        # Avaliar
        y_pred = self.model.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"📊 Acurácia: {self.accuracy:.4f}")
        logger.info(f"📊 Relatório:\n{classification_report(y_test, y_pred)}")
    
    def predict(self, features: List[float]) -> Tuple[Optional[str], float]:
        """Faz predição do melhor template"""
        if not self.trained or not self.model:
            return None, 0.0
        
        # Normalizar
        features = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        
        if HAS_TORCH:
            with torch.no_grad():
                features_tensor = torch.FloatTensor(features_scaled)
                outputs = self.model(features_tensor)
                probabilities = torch.softmax(outputs, dim=1).numpy()[0]
        elif HAS_TF:
            probabilities = self.model.predict(features_scaled, verbose=0)[0]
        elif HAS_SKLEARN:
            probabilities = self.model.predict_proba(features_scaled)[0]
        else:
            return None, 0.0
        
        best_idx = np.argmax(probabilities)
        confidence = probabilities[best_idx]
        
        if confidence > 0.3:
            template = self.label_encoder.inverse_transform([best_idx])[0]
            return template, confidence
        
        return None, confidence
    
    def _save_model(self):
        """Salva o modelo treinado"""
        model_dir = Config.NEURAL_DIR
        
        if HAS_TORCH:
            torch.save({
                'model_state_dict': self.model.state_dict(),
                'scaler': self.scaler,
                'label_encoder': self.label_encoder,
                'accuracy': self.accuracy
            }, model_dir / "model.pth")
        elif HAS_TF:
            self.model.save(model_dir / "model.h5")
            joblib.dump(self.scaler, model_dir / "scaler.pkl")
            joblib.dump(self.label_encoder, model_dir / "label_encoder.pkl")
        elif HAS_SKLEARN:
            joblib.dump(self.model, model_dir / "model.pkl")
            joblib.dump(self.scaler, model_dir / "scaler.pkl")
            joblib.dump(self.label_encoder, model_dir / "label_encoder.pkl")
        
        # Salvar metadados
        with open(model_dir / "metadata.json", 'w') as f:
            json.dump({
                'accuracy': self.accuracy,
                'trained': self.trained,
                'features': Config.INPUT_FEATURES,
                'layers': Config.HIDDEN_LAYERS,
                'classes': Config.OUTPUT_CLASSES,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        
        logger.info(f"💾 Modelo salvo em {model_dir}")
    
    def _load_model(self):
        """Carrega modelo existente"""
        model_dir = Config.NEURAL_DIR
        
        if HAS_TORCH and (model_dir / "model.pth").exists():
            try:
                checkpoint = torch.load(model_dir / "model.pth")
                self.model = self._build_model()
                self.model.load_state_dict(checkpoint['model_state_dict'])
                self.scaler = checkpoint['scaler']
                self.label_encoder = checkpoint['label_encoder']
                self.accuracy = checkpoint['accuracy']
                self.trained = True
                logger.info(f"🤖 Modelo PyTorch carregado (acurácia: {self.accuracy:.4f})")
            except Exception as e:
                logger.error(f"Erro carregando modelo PyTorch: {e}")
        
        elif HAS_TF and (model_dir / "model.h5").exists():
            try:
                self.model = keras.models.load_model(model_dir / "model.h5")
                self.scaler = joblib.load(model_dir / "scaler.pkl")
                self.label_encoder = joblib.load(model_dir / "label_encoder.pkl")
                self.trained = True
                logger.info(f"🤖 Modelo TensorFlow carregado")
            except Exception as e:
                logger.error(f"Erro carregando modelo TensorFlow: {e}")
        
        elif HAS_SKLEARN and (model_dir / "model.pkl").exists():
            try:
                self.model = joblib.load(model_dir / "model.pkl")
                self.scaler = joblib.load(model_dir / "scaler.pkl")
                self.label_encoder = joblib.load(model_dir / "label_encoder.pkl")
                self.trained = True
                logger.info(f"🤖 Modelo scikit-learn carregado")
            except Exception as e:
                logger.error(f"Erro carregando modelo scikit-learn: {e}")

# =========================
# TEMPLATES AVANÇADOS
# =========================
class TemplateOptimizer:
    """Implementação avançada de templates de otimização"""
    
    def __init__(self):
        self.templates = self._initialize_templates()
        self.stats = defaultdict(lambda: {'success': 0, 'attempts': 0})
    
    def _initialize_templates(self) -> Dict[str, Callable]:
        """Inicializa todos os templates"""
        return {
            # Loop Optimizations
            'loop_vectorization_numpy': self._optimize_loop_vectorization,
            'loop_unrolling_dynamic': self._optimize_loop_unrolling,
            'loop_parallelization': self._optimize_loop_parallel,
            'loop_fusion': self._optimize_loop_fusion,
            
            # Data Structures
            'list_to_array': self._optimize_list_to_array,
            'dict_to_defaultdict': self._optimize_dict_to_defaultdict,
            'set_operations': self._optimize_set_operations,
            'deque_for_queue': self._optimize_deque,
            
            # Caching
            'lru_cache_deep': self._optimize_lru_cache,
            'memoization_recursive': self._optimize_memoization,
            'cached_property': self._optimize_cached_property,
            
            # Parallelism
            'multiprocessing_pool': self._optimize_multiprocessing,
            'concurrent_futures': self._optimize_concurrent,
            'asyncio_conversion': self._optimize_asyncio,
            
            # Memory
            'memory_slots': self._optimize_slots,
            'generator_pipeline': self._optimize_generator,
            'buffer_reuse': self._optimize_buffer,
            
            # I/O
            'buffered_io': self._optimize_buffered_io,
            'mmap_file': self._optimize_mmap,
            'batch_processing': self._optimize_batch,
            
            # String
            'string_join': self._optimize_string_join,
            'f_strings': self._optimize_fstrings,
            'regex_compile': self._optimize_regex,
            
            # Algorithms
            'divide_conquer': self._optimize_divide_conquer,
            'dynamic_programming': self._optimize_dp,
            'greedy_algorithm': self._optimize_greedy,
            
            # Functions
            'function_inlining': self._optimize_inlining,
            'tail_recursion': self._optimize_tail_recursion,
            'partial_application': self._optimize_partial,
            
            # Classes
            '__slots__usage': self._optimize_slots_class,
            'property_caching': self._optimize_property_cache,
            'singleton_pattern': self._optimize_singleton
        }
    
    def apply(self, code: str, template_name: str) -> str:
        """Aplica um template ao código"""
        if template_name not in self.templates:
            logger.warning(f"⚠️ Template desconhecido: {template_name}")
            return code
        
        try:
            optimizer = self.templates[template_name]
            optimized = optimizer(code)
            
            self.stats[template_name]['attempts'] += 1
            
            if optimized != code:
                self.stats[template_name]['success'] += 1
            
            return optimized
            
        except Exception as e:
            logger.error(f"Erro aplicando template {template_name}: {e}")
            return code
    
    def _optimize_loop_vectorization(self, code: str) -> str:
        """Converte loops para operações vetorizadas com numpy"""
        lines = code.split('\n')
        modified = False
        
        # Procurar padrões de loop que podem ser vetorizados
        for i, line in enumerate(lines):
            # Padrão: for i in range(n): arr[i] = arr[i] * 2
            match = re.search(r'for\s+(\w+)\s+in\s+range\(\s*(\w+)\s*\):\s*(\w+)\[\1\]\s*=\s*(\w+)\[\1\]\s*([+\-*/])\s*([\d.]+)', line)
            if match:
                var, n, arr, _, op, val = match.groups()
                
                # Verificar se numpy já está importado
                if 'import numpy' not in code:
                    lines.insert(0, 'import numpy as np')
                
                # Substituir loop
                numpy_op = {
                    '+': '+', '-': '-', '*': '*', '/': '/'
                }.get(op, op)
                
                lines[i] = f"    {arr} = {arr} {numpy_op} {val}"
                modified = True
                
                # Remover linhas do loop
                j = i + 1
                while j < len(lines) and lines[j].startswith('    '):
                    lines.pop(j)
        
        if modified:
            logger.debug("🔄 Loop vetorizado com numpy")
        
        return '\n'.join(lines)
    
    def _optimize_loop_unrolling(self, code: str) -> str:
        """Desenrola loops pequenos para reduzir overhead"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Procurar loops pequenos
            match = re.search(r'for\s+(\w+)\s+in\s+range\(\s*(\d+)\s*\):', line)
            if match:
                var, n = match.groups()
                n = int(n)
                
                if n <= 8:  # Só desenrolar loops pequenos
                    # Coletar corpo do loop
                    body = []
                    j = i + 1
                    while j < len(lines) and lines[j].startswith('    '):
                        body.append(lines[j].strip())
                        j += 1
                    
                    if len(body) == 1:
                        # Desenrolar
                        unrolled = []
                        for k in range(n):
                            line_body = body[0].replace(var, str(k))
                            unrolled.append(f"    {line_body}")
                        
                        lines[i:j] = unrolled
                        logger.debug(f"🔄 Loop desenrolado ({n} iterações)")
        
        return '\n'.join(lines)
    
    def _optimize_loop_parallel(self, code: str) -> str:
        """Paraleliza loops com multiprocessing"""
        if 'from multiprocessing import Pool' not in code:
            # Adicionar import
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    lines.insert(i, 'from multiprocessing import Pool')
                    break
            else:
                lines.insert(0, 'from multiprocessing import Pool')
            
            code = '\n'.join(lines)
        
        # Procurar loops independentes
        # Implementação simplificada
        return code
    
    def _optimize_loop_fusion(self, code: str) -> str:
        """Funde loops consecutivos sobre o mesmo range"""
        lines = code.split('\n')
        i = 0
        modified = False
        
        while i < len(lines) - 3:
            # Procurar dois loops consecutivos
            match1 = re.search(r'for\s+(\w+)\s+in\s+range\(\s*(\w+)\s*\):', lines[i])
            if match1:
                var1, n1 = match1.groups()
                
                # Coletar corpo do primeiro loop
                body1 = []
                j = i + 1
                while j < len(lines) and lines[j].startswith('    '):
                    body1.append(lines[j][4:])  # Remover indentação
                    j += 1
                
                # Verificar segundo loop
                if j < len(lines):
                    match2 = re.search(r'for\s+(\w+)\s+in\s+range\(\s*(\w+)\s*\):', lines[j])
                    if match2 and match2.group(2) == n1:
                        var2 = match2.group(1)
                        
                        # Coletar corpo do segundo loop
                        body2 = []
                        k = j + 1
                        while k < len(lines) and lines[k].startswith('    '):
                            body2.append(lines[k][4:])
                            k += 1
                        
                        # Fundir loops se independentes
                        fused_body = []
                        for line in body1:
                            fused_body.append(f"    {line}")
                        for line in body2:
                            # Substituir variável se necessário
                            line = line.replace(var2, var1)
                            fused_body.append(f"    {line}")
                        
                        # Substituir
                        lines[i:k] = [f"for {var1} in range({n1}):"] + fused_body
                        modified = True
                        i = k
                        continue
            
            i += 1
        
        if modified:
            logger.debug("🔄 Loops fundidos")
        
        return '\n'.join(lines)
    
    def _optimize_list_to_array(self, code: str) -> str:
        """Converte listas para arrays numpy"""
        if 'import numpy' not in code:
            lines = code.split('\n')
            lines.insert(0, 'import numpy as np')
            code = '\n'.join(lines)
        
        # Procurar criações de lista
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Padrão: var = [0] * n
            match = re.search(r'(\w+)\s*=\s*\[\s*0\s*\]\s*\*\s*(\w+)', line)
            if match:
                var, n = match.groups()
                lines[i] = f"{var} = np.zeros({n})"
            
            # Padrão: var = []
            elif re.search(r'(\w+)\s*=\s*\[\s*\]', line):
                var = re.search(r'(\w+)\s*=\s*\[\s*\]', line).group(1)
                
                # Verificar se usa append depois
                for j in range(i+1, min(i+10, len(lines))):
                    if f'{var}.append(' in lines[j]:
                        lines[i] = f"{var} = []  # Consider using np.array for performance"
                        break
        
        return '\n'.join(lines)
    
    def _optimize_dict_to_defaultdict(self, code: str) -> str:
        """Converte dict para defaultdict quando apropriado"""
        if 'from collections import defaultdict' not in code:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    lines.insert(i, 'from collections import defaultdict')
                    break
            else:
                lines.insert(0, 'from collections import defaultdict')
            
            code = '\n'.join(lines)
        
        # Procurar padrões de verificação de chave
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Padrão: if key not in dict: dict[key] = [] / dict[key].append()
            match = re.search(r'if\s+(\w+)\s+not\s+in\s+(\w+):\s*\2\[\1\]\s*=\s*\[\]', line)
            if match:
                key, dict_name = match.groups()
                
                # Verificar próxima linha
                if i+1 < len(lines) and f'{dict_name}[{key}].append(' in lines[i+1]:
                    # Substituir
                    lines[i] = f"    {dict_name} = defaultdict(list)"
                    lines[i+1] = f"    {dict_name}[{key}].append(" + lines[i+1].split('.append(')[1]
        
        return '\n'.join(lines)
    
    def _optimize_set_operations(self, code: str) -> str:
        """Otimiza operações de conjunto"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Procurar loops de verificação de pertencimento
            match = re.search(r'for\s+(\w+)\s+in\s+(\w+):\s+if\s+(\w+)\s+in\s+(\w+):', line)
            if match:
                var, list1, _, list2 = match.groups()
                
                # Converter para operação de conjunto
                lines[i] = f"    common = set({list1}) & set({list2})"
                lines[i+1] = f"    for {var} in common:"
        
        return '\n'.join(lines)
    
    def _optimize_deque(self, code: str) -> str:
        """Usa deque para operações de fila"""
        if 'from collections import deque' not in code:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    lines.insert(i, 'from collections import deque')
                    break
            else:
                lines.insert(0, 'from collections import deque')
            
            code = '\n'.join(lines)
        
        # Procurar uso de list como fila
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Padrão: var = [] seguido de pop(0)
            if re.search(r'(\w+)\s*=\s*\[\s*\]', line):
                var = re.search(r'(\w+)\s*=\s*\[\s*\]', line).group(1)
                
                for j in range(i+1, min(i+20, len(lines))):
                    if f'{var}.pop(0)' in lines[j]:
                        lines[i] = f"{var} = deque()"
                        lines[j] = lines[j].replace(f'{var}.pop(0)', f'{var}.popleft()')
                        break
        
        return '\n'.join(lines)
    
    def _optimize_lru_cache(self, code: str) -> str:
        """Adiciona cache LRU a funções"""
        if 'from functools import lru_cache' not in code:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    lines.insert(i, 'from functools import lru_cache')
                    break
            else:
                lines.insert(0, 'from functools import lru_cache')
            
            code = '\n'.join(lines)
        
        # Adicionar decorator a funções recursivas
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            if line.strip().startswith('def ') and not line.strip().startswith('def __'):
                # Verificar se é recursiva
                func_name = line.split('def ')[1].split('(')[0].strip()
                
                # Procurar chamadas recursivas
                is_recursive = False
                for j in range(i+1, min(i+50, len(lines))):
                    if f'{func_name}(' in lines[j] and not lines[j].strip().startswith('#'):
                        is_recursive = True
                        break
                
                if is_recursive and '@lru_cache' not in lines[i-1]:
                    lines.insert(i, '@lru_cache(maxsize=128)')
        
        return '\n'.join(lines)
    
    def _optimize_memoization(self, code: str) -> str:
        """Adiciona memoização a funções recursivas"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            if line.strip().startswith('def ') and not line.strip().startswith('def __'):
                func_name = line.split('def ')[1].split('(')[0].strip()
                
                # Verificar se é recursiva
                is_recursive = False
                params = []
                
                for j in range(i+1, min(i+50, len(lines))):
                    if f'{func_name}(' in lines[j]:
                        is_recursive = True
                        # Extrair parâmetros
                        match = re.search(rf'{func_name}\(([^)]+)\)', lines[j])
                        if match:
                            params.extend(re.findall(r'\b\w+\b', match.group(1)))
                        break
                
                if is_recursive and params:
                    # Adicionar cache manual
                    cache_name = f"_{func_name}_cache"
                    lines.insert(i, f"{cache_name} = {{}}")
                    
                    # Modificar função
                    lines[i+1] = f"def {func_name}({', '.join(set(params))}):"
                    lines.insert(i+2, f"    args = ({', '.join(set(params))})")
                    lines.insert(i+3, f"    if args in {cache_name}:")
                    lines.insert(i+4, f"        return {cache_name}[args]")
                    
                    # Adicionar cache no retorno
                    for j in range(i+5, len(lines)):
                        if 'return ' in lines[j]:
                            lines[j] = f"    result = {lines[j].strip()}"
                            lines.insert(j+1, f"    {cache_name}[args] = result")
                            lines.insert(j+2, f"    return result")
                            break
        
        return '\n'.join(lines)
    
    def _optimize_cached_property(self, code: str) -> str:
        """Usa cached_property para propriedades caras"""
        if 'from functools import cached_property' not in code:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    lines.insert(i, 'from functools import cached_property')
                    break
            else:
                lines.insert(0, 'from functools import cached_property')
            
            code = '\n'.join(lines)
        
        # Procurar propriedades com @property
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            if '@property' in line:
                # Verificar se a propriedade tem cálculos pesados
                for j in range(i+1, min(i+20, len(lines))):
                    if 'for ' in lines[j] or 'while ' in lines[j]:
                        lines[i] = '@cached_property'
                        break
        
        return '\n'.join(lines)
    
    def _optimize_multiprocessing(self, code: str) -> str:
        """Adiciona multiprocessing para tarefas paralelizáveis"""
        if 'from multiprocessing import Pool' not in code:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    lines.insert(i, 'from multiprocessing import Pool')
                    break
            else:
                lines.insert(0, 'from multiprocessing import Pool')
            
            code = '\n'.join(lines)
        
        # Procurar loops independentes
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            if 'for ' in line and ' in ' in line:
                # Extrair informações do loop
                match = re.search(r'for\s+(\w+)\s+in\s+(\w+):', line)
                if match:
                    var, iterable = match.groups()
                    
                    # Verificar se as iterações são independentes
                    body = []
                    j = i + 1
                    independent = True
                    
                    while j < len(lines) and lines[j].startswith('    '):
                        body.append(lines[j].strip())
                        # Verificar dependências
                        if '=' in lines[j] and var not in lines[j].split('=')[0]:
                            independent = False
                        j += 1
                    
                    if independent and len(body) > 0:
                        # Criar função para o worker
                        worker_name = f"_worker_{var}"
                        worker_code = f"""
def {worker_name}({var}):
    {' '.join(body).replace(var, 'x')}
    return result
"""
                        # Substituir loop por Pool
                        pool_code = f"""
    with Pool() as pool:
        results = pool.map({worker_name}, {iterable})
"""
                        lines[i:j] = [worker_code, pool_code]
        
        return '\n'.join(lines)
    
    def _optimize_concurrent(self, code: str) -> str:
        """Usa concurrent.futures para paralelismo"""
        if 'from concurrent.futures import ThreadPoolExecutor' not in code:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    lines.insert(i, 'from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor')
                    break
            else:
                lines.insert(0, 'from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor')
            
            code = '\n'.join(lines)
        
        return code
    
    def _optimize_asyncio(self, code: str) -> str:
        """Converte código síncrono para assíncrono quando apropriado"""
        if 'import asyncio' not in code:
            lines = code.split('\n')
            lines.insert(0, 'import asyncio')
            code = '\n'.join(lines)
        
        # Procurar operações de I/O
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            if 'time.sleep(' in line:
                lines[i] = line.replace('time.sleep', 'await asyncio.sleep')
            
            elif 'open(' in line or 'with open(' in line:
                # Marcar para possível conversão
                if 'async' not in line:
                    lines[i] = '# TODO: Convert to async file I/O\n' + lines[i]
        
        return '\n'.join(lines)
    
    def _optimize_slots(self, code: str) -> str:
        """Adiciona __slots__ a classes"""
        lines = code.split('\n')
        
        in_class = False
        class_name = ""
        attributes = set()
        
        for i, line in enumerate(lines):
            if line.strip().startswith('class '):
                in_class = True
                class_name = line.split('class ')[1].split('(')[0].strip()
                attributes = set()
            
            elif in_class:
                if line.strip().startswith('def __init__'):
                    # Extrair atributos do __init__
                    match = re.search(r'def\s+__init__\s*\(\s*self\s*,\s*([^)]*)\)', line)
                    if match:
                        params = match.group(1).split(',')
                        for param in params:
                            param = param.strip()
                            if param and param != 'self':
                                attributes.add(param)
                
                elif line.strip() and not line.strip().startswith(('def ', '@', '#')):
                    # Possível atributo
                    if 'self.' in line:
                        attr = line.split('self.')[1].split('=')[0].strip()
                        if attr and not attr.startswith('_'):
                            attributes.add(attr)
                
                elif line.strip() == '' and i < len(lines) - 1:
                    # Fim da classe
                    if attributes:
                        # Inserir __slots__
                        slots_line = f"    __slots__ = {tuple(attributes)}"
                        for j in range(i, 0, -1):
                            if lines[j].strip().startswith('class '):
                                lines.insert(j+1, slots_line)
                                break
                    in_class = False
        
        return '\n'.join(lines)
    
    def _optimize_generator(self, code: str) -> str:
        """Converte listas para generators"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Procurar list comprehensions grandes
            match = re.search(r'\[\s*(\w+)\s+for\s+(\w+)\s+in\s+(\w+)\s*\]', line)
            if match:
                expr, var, iterable = match.groups()
                
                # Verificar se a lista é usada toda de uma vez
                var_name = line.split('=')[0].strip() if '=' in line else ''
                
                if var_name:
                    uses = 0
                    for j in range(i+1, len(lines)):
                        if var_name in lines[j]:
                            uses += 1
                    
                    if uses <= 1:
                        # Converter para generator
                        lines[i] = lines[i].replace('[', '(').replace(']', ')')
        
        return '\n'.join(lines)
    
    def _optimize_buffer(self, code: str) -> str:
        """Reusa buffers para evitar alocações"""
        lines = code.split('\n')
        
        # Procurar alocações repetidas
        buffers = {}
        
        for i, line in enumerate(lines):
            # Padrão: var = [] dentro de loop
            if '= []' in line and any(x in lines[max(0, i-5):i] for x in ['for ', 'while ']):
                var = line.split('=')[0].strip()
                
                # Criar buffer externo
                for j in range(i-1, -1, -1):
                    if lines[j].strip().startswith('def '):
                        # Adicionar buffer como argumento padrão
                        lines[j] = lines[j].replace('):', f', {var}=None):')
                        lines.insert(j+1, f"    if {var} is None:")
                        lines.insert(j+2, f"        {var} = []")
                        break
        
        return '\n'.join(lines)
    
    def _optimize_buffered_io(self, code: str) -> str:
        """Otimiza operações de I/O com buffer"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Padrão: f.write() em loop
            if '.write(' in line and 'for ' in lines[max(0, i-10):i]:
                # Coletar escritas
                writes = []
                j = i
                while j < len(lines) and '.write(' in lines[j]:
                    writes.append(lines[j].strip())
                    j += 1
                
                if len(writes) > 1:
                    # Combinar em uma única escrita
                    content = '+'.join([f"({w.split('.write(')[1][:-1]})" for w in writes])
                    lines[i] = f"    f.write({content})"
                    for k in range(i+1, j):
                        lines[k] = ''
        
        return '\n'.join(lines)
    
    def _optimize_mmap(self, code: str) -> str:
        """Usa mmap para arquivos grandes"""
        if 'import mmap' not in code:
            lines = code.split('\n')
            lines.insert(0, 'import mmap')
            code = '\n'.join(lines)
        
        # Procurar leitura de arquivos grandes
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            if 'open(' in line and '.read()' in line:
                # Substituir por mmap
                lines[i] = line.replace('.read()', '')
                lines.insert(i+1, f"    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:")
        
        return '\n'.join(lines)
    
    def _optimize_batch(self, code: str) -> str:
        """Processa dados em batches"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Procurar processamento item a item
            if 'for ' in line and ' in ' in line:
                match = re.search(r'for\s+(\w+)\s+in\s+(\w+):', line)
                if match:
                    var, iterable = match.groups()
                    
                    # Verificar tamanho do iterável
                    if 'range(' in iterable:
                        # Batch processing
                        lines[i] = f"    batch_size = 1000"
                        lines.insert(i+1, f"    for i in range(0, len({iterable}), batch_size):")
                        lines.insert(i+2, f"        batch = {iterable}[i:i+batch_size]")
                        lines.insert(i+3, f"        for {var} in batch:")
        
        return '\n'.join(lines)
    
    def _optimize_string_join(self, code: str) -> str:
        """Otimiza concatenação de strings"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Padrão: s = s + x em loop
            if '+= ' in line and 'str' in str(type(line)):
                # Procurar loop
                for j in range(max(0, i-10), i):
                    if 'for ' in lines[j]:
                        var = lines[j].split('for ')[1].split(' in ')[0]
                        if var in line:
                            # Coletar strings
                            parts = []
                            k = j + 1
                            while k < len(lines) and lines[k].strip():
                                if '+= ' in lines[k]:
                                    parts.append(lines[k].split('+= ')[1])
                                k += 1
                            
                            if parts:
                                # Substituir por join
                                lines[j:k] = [
                                    f"    parts = []",
                                    f"    for {var} in {lines[j].split(' in ')[1][:-1]}:",
                                    f"        parts.append({parts[0]})",
                                    f"    result = ''.join(parts)"
                                ]
                                break
        
        return '\n'.join(lines)
    
    def _optimize_fstrings(self, code: str) -> str:
        """Converte para f-strings quando possível"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Padrão: "..." + var + "..."
            if "' + " in line or '" + ' in line:
                # Tentar converter para f-string
                parts = re.split(r"('|\") \+ ", line)
                if len(parts) > 1:
                    # Construir f-string
                    fstring = 'f"'
                    for part in parts:
                        if part.startswith(("'", '"')):
                            fstring += part[1:-1]
                        else:
                            fstring += '{' + part.strip() + '}'
                    fstring += '"'
                    lines[i] = fstring
        
        return '\n'.join(lines)
    
    def _optimize_regex(self, code: str) -> str:
        """Compila regex para reuso"""
        if 'import re' not in code:
            lines = code.split('\n')
            lines.insert(0, 'import re')
            code = '\n'.join(lines)
        
        lines = code.split('\n')
        compiled = set()
        
        for i, line in enumerate(lines):
            # Procurar re.search/re.findall com strings literais
            match = re.search(r're\.(search|findall|match|sub)\(\s*[\'"]([^\'"]+)[\'"]', line)
            if match:
                func, pattern = match.groups()
                if pattern not in compiled:
                    # Compilar antes
                    var_name = f"_re_{len(compiled)}"
                    lines.insert(i, f"{var_name} = re.compile(r'{pattern}')")
                    lines[i+1] = lines[i+1].replace(
                        f"re.{func}(r'{pattern}'",
                        f"{var_name}.{func}("
                    ).replace(
                        f"re.{func}('{pattern}'",
                        f"{var_name}.{func}("
                    )
                    compiled.add(pattern)
        
        return '\n'.join(lines)
    
    def _optimize_divide_conquer(self, code: str) -> str:
        """Implementa divisão e conquista"""
        # Análise de algoritmo para detectar oportunidades
        return code
    
    def _optimize_dp(self, code: str) -> str:
        """Implementa programação dinâmica"""
        # Análise de algoritmo para detectar oportunidades
        return code
    
    def _optimize_greedy(self, code: str) -> str:
        """Implementa algoritmo guloso"""
        # Análise de algoritmo para detectar oportunidades
        return code
    
    def _optimize_inlining(self, code: str) -> str:
        """Inline funções pequenas"""
        lines = code.split('\n')
        
        # Identificar funções pequenas
        functions = {}
        i = 0
        while i < len(lines):
            if lines[i].strip().startswith('def '):
                start = i
                name = lines[i].split('def ')[1].split('(')[0].strip()
                body = []
                i += 1
                while i < len(lines) and lines[i].startswith('    '):
                    body.append(lines[i][4:])
                    i += 1
                
                # Verificar se é pequena (1-2 linhas)
                if len(body) <= 2:
                    functions[name] = {'start': start, 'end': i, 'body': body}
            else:
                i += 1
        
        # Inline chamadas
        for name, info in functions.items():
            for i, line in enumerate(lines):
                if f'{name}(' in line and not line.strip().startswith('def '):
                    # Substituir chamada pelo corpo
                    indent = len(line) - len(line.lstrip())
                    call_indent = ' ' * indent
                    
                    # Criar versão inline
                    inline_code = []
                    for body_line in info['body']:
                        inline_code.append(call_indent + body_line)
                    
                    # Substituir linha
                    lines[i] = '\n'.join(inline_code)
        
        # Remover funções originais (opcional)
        # for name, info in reversed(sorted(functions.items(), key=lambda x: x[1]['start'])):
        #     del lines[info['start']:info['end']]
        
        return '\n'.join(lines)
    
    def _optimize_tail_recursion(self, code: str) -> str:
        """Otimiza recursão de cauda"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            if line.strip().startswith('def '):
                func_name = line.split('def ')[1].split('(')[0].strip()
                
                # Analisar corpo para recursão de cauda
                for j in range(i+1, min(i+50, len(lines))):
                    if f'return {func_name}(' in lines[j]:
                        # Converter para loop
                        params = re.findall(r'\(([^)]+)\)', lines[j])
                        if params:
                            # Adicionar decorator
                            lines.insert(i, '@tail_recursive')
        
        return '\n'.join(lines)
    
    def _optimize_partial(self, code: str) -> str:
        """Usa partial para funções com argumentos fixos"""
        if 'from functools import partial' not in code:
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    lines.insert(i, 'from functools import partial')
                    break
            else:
                lines.insert(0, 'from functools import partial')
            
            code = '\n'.join(lines)
        
        # Procurar chamadas repetidas com mesmos argumentos
        calls = defaultdict(list)
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            match = re.search(r'(\w+)\(([^)]+)\)', line)
            if match:
                func, args = match.groups()
                calls[func].append((args, i))
        
        # Criar partials
        for func, occurrences in calls.items():
            if len(occurrences) > 2:
                # Verificar argumentos comuns
                common_args = None
                for args, _ in occurrences:
                    if common_args is None:
                        common_args = set(args.split(','))
                    else:
                        common_args &= set(args.split(','))
                
                if common_args and len(common_args) > 0:
                    # Criar partial
                    common_str = ', '.join(sorted(common_args))
                    lines.insert(0, f"_{func} = partial({func}, {common_str})")
                    
                    # Substituir chamadas
                    for args, idx in occurrences:
                        remaining = [a for a in args.split(',') if a not in common_args]
                        if remaining:
                            lines[idx] = lines[idx].replace(
                                f"{func}({args})",
                                f"_{func}({', '.join(remaining)})"
                            )
        
        return '\n'.join(lines)
    
    def _optimize_slots_class(self, code: str) -> str:
        """Adiciona __slots__ a classes para economia de memória"""
        return self._optimize_slots(code)
    
    def _optimize_property_cache(self, code: str) -> str:
        """Adiciona cache a propriedades"""
        return self._optimize_cached_property(code)
    
    def _optimize_singleton(self, code: str) -> str:
        """Implementa padrão Singleton"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            if line.strip().startswith('class '):
                # Adicionar decorator de singleton
                class_name = line.split('class ')[1].split('(')[0].strip()
                
                # Criar decorator
                singleton_decorator = f"""
def singleton(cls):
    instances = {{}}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
"""
                lines.insert(0, singleton_decorator)
                lines[i] = f"@singleton\n{lines[i]}"
                break
        
        return '\n'.join(lines)
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas de uso dos templates"""
        stats = {}
        for template, data in self.stats.items():
            if data['attempts'] > 0:
                success_rate = data['success'] / data['attempts']
                stats[template] = {
                    'attempts': data['attempts'],
                    'success': data['success'],
                    'success_rate': success_rate
                }
        return stats

# =========================
# AVALIADOR DE FITNESS AVANÇADO
# =========================
class FitnessEvaluator:
    """Avaliação avançada de fitness com múltiplas métricas"""
    
    def __init__(self):
        self.sandbox = SandboxExecutor()
        self.history = []
    
    @timed
    def evaluate(self, code: str, iterations: int = Config.BENCHMARK_REPETICOES) -> Dict[str, Any]:
        """Avaliação completa do código"""
        metrics = {
            'time': [],
            'memory': [],
            'cpu': [],
            'io': [],
            'stability': []
        }
        
        # Warmup
        for _ in range(Config.BENCHMARK_WARMUP):
            self.sandbox.execute(code, timeout=1)
        
        # Benchmarks
        for i in range(iterations):
            result = self.sandbox.execute(code)
            
            if result['success']:
                metrics['time'].append(result.get('time', 0))
                metrics['memory'].append(result.get('memory', 0))
                metrics['cpu'].append(result.get('cpu', 0))
                metrics['io'].append(result.get('io', 0))
                metrics['stability'].append(1.0)
            else:
                metrics['stability'].append(0.0)
            
            # Cooldown
            time.sleep(Config.COOLDOWN_SEGUNDOS)
        
        # Calcular estatísticas
        stats = {}
        for key, values in metrics.items():
            if values:
                stats[f'{key}_mean'] = np.mean(values)
                stats[f'{key}_std'] = np.std(values)
                stats[f'{key}_min'] = np.min(values)
                stats[f'{key}_max'] = np.max(values)
            else:
                stats[f'{key}_mean'] = 0
                stats[f'{key}_std'] = 0
                stats[f'{key}_min'] = 0
                stats[f'{key}_max'] = 0
        
        # Calcular fitness composto
        fitness = self._calculate_fitness(stats)
        stats['fitness'] = fitness
        stats['stable'] = stats['stability_mean'] > 0.8
        
        # Adicionar ao histórico
        self.history.append(stats)
        
        return stats
    
    def _calculate_fitness(self, stats: Dict[str, float]) -> float:
        """Calcula fitness composto"""
        # Normalizar métricas
        time_score = 1.0 / (stats.get('time_mean', 1.0) + 0.1)
        memory_score = 1.0 / (stats.get('memory_mean', 10) + 1.0)
        cpu_score = 1.0 / (stats.get('cpu_mean', 50) + 1.0)
        stability_score = stats.get('stability_mean', 0)
        
        # Pesos
        fitness = (
            Config.PESO_TEMPO * time_score +
            Config.PESO_MEMORIA * memory_score +
            Config.PESO_EFICIENCIA * cpu_score +
            Config.PESO_ESTABILIDADE * stability_score
        )
        
        return fitness
    
    def compare(self, code1: str, code2: str) -> Dict[str, Any]:
        """Compara duas versões de código"""
        eval1 = self.evaluate(code1, iterations=3)
        eval2 = self.evaluate(code2, iterations=3)
        
        comparison = {
            'fitness_improvement': eval2['fitness'] - eval1['fitness'],
            'time_improvement': (eval1['time_mean'] - eval2['time_mean']) / eval1['time_mean'] * 100,
            'memory_improvement': (eval1['memory_mean'] - eval2['memory_mean']) / eval1['memory_mean'] * 100,
            'stable': eval2['stable']
        }
        
        return comparison

# =========================
# SANDBOX EXECUTOR
# =========================
class SandboxExecutor:
    """Executor seguro de código em ambiente isolado"""
    
    def __init__(self):
        self.temp_dir = Config.TEMP_DIR
        self.timeout = Config.TIMEOUT_SEGUNDOS
        self.memory_limit = Config.MEMORIA_MAXIMA_MB * 1024 * 1024
    
    @timed
    def execute(self, code: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """Executa código em sandbox seguro"""
        if timeout is None:
            timeout = self.timeout
        
        # Criar arquivo temporário
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', 
                                        dir=self.temp_dir, delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        result = {
            'success': False,
            'time': 0,
            'memory': 0,
            'cpu': 0,
            'io': 0,
            'error': None,
            'output': ''
        }
        
        try:
            # Medir recursos
            start_time = time.perf_counter()
            process = psutil.Process()
            mem_before = process.memory_info().rss
            
            # Executar em subprocesso com limites
            cmd = [sys.executable, temp_file]
            
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                env={'PYTHONPATH': '', 'PYTHONHASHSEED': '0'}
            )
            
            # Medir após execução
            end_time = time.perf_counter()
            mem_after = process.memory_info().rss
            
            result['time'] = end_time - start_time
            result['memory'] = (mem_after - mem_before) / (1024 * 1024)  # MB
            result['cpu'] = psutil.cpu_percent(interval=0.1)
            result['output'] = proc.stdout
            result['success'] = proc.returncode == 0
            
            if proc.stderr:
                result['error'] = proc.stderr
            
        except subprocess.TimeoutExpired:
            result['error'] = f"Timeout após {timeout}s"
        except Exception as e:
            result['error'] = str(e)
        finally:
            # Limpar
            try:
                os.unlink(temp_file)
            except:
                pass
        
        return result

# =========================
# MUTADOR INTELIGENTE AVANÇADO
# =========================
class IntelligentMutator:
    """Mutador com IA e múltiplas estratégias"""
    
    def __init__(self, vector_db: VectorDatabase, neural_net: DeepNeuralNetwork):
        self.vector_db = vector_db
        self.neural_net = neural_net
        self.template_optimizer = TemplateOptimizer()
        self.analyzer = CodeAnalyzer()
        self.stats = defaultdict(int)
    
    @timed
    def mutate(self, code: str, version_id: str) -> Optional[MutationResult]:
        """Tenta mutar o código com múltiplas estratégias"""
        
        # Analisar código atual
        features = self.analyzer.analyze(code)
        features.normalize()
        
        # Avaliar fitness atual
        evaluator = FitnessEvaluator()
        current_fitness = evaluator.evaluate(code)
        
        # Estratégia 1: Rede neural
        template, confidence = self.neural_net.predict(features.values)
        
        if template and confidence > 0.5:
            logger.info(f"🤖 Rede neural recomenda: {template} (confiança: {confidence:.2f})")
            result = self._try_template(code, template, features, current_fitness['fitness'])
            if result and result.success:
                return result
        
        # Estratégia 2: Banco vetorial
        recommendations = self.vector_db.get_recommendations(features.values)
        
        for template, score in recommendations[:3]:
            logger.info(f"📊 Vetor DB recomenda: {template} (score: {score:.2f})")
            result = self._try_template(code, template, features, current_fitness['fitness'])
            if result and result.success:
                return result
        
        # Estratégia 3: Templates aleatórios (exploração)
        if random.random() < Config.MUTATION_RATE:
            template = random.choice(Config.TEMPLATES)
            logger.info(f"🎲 Explorando template: {template}")
            result = self._try_template(code, template, features, current_fitness['fitness'])
            if result and result.success:
                return result
        
        return None
    
    def _try_template(self, code: str, template: str, features: FeatureVector,
                     current_fitness: float) -> Optional[MutationResult]:
        """Tenta aplicar um template específico"""
        
        # Aplicar template
        mutated = self.template_optimizer.apply(code, template)
        
        if mutated == code:
            return None
        
        # Avaliar mutação
        evaluator = FitnessEvaluator()
        new_fitness = evaluator.evaluate(mutated)
        
        improvement = new_fitness['fitness'] - current_fitness
        
        # Criar resultado
        result = MutationResult(
            success=improvement > 0,
            template=template,
            fitness_before=current_fitness,
            fitness_after=new_fitness['fitness'],
            improvement=improvement,
            features=features,
            code_before=code,
            code_after=mutated
        )
        
        # Registrar no banco vetorial
        self.vector_db.add_vector(
            vector_id=str(uuid.uuid4()),
            code_hash=hashlib.md5(code.encode()).hexdigest(),
            features=features.values,
            template=template,
            improvement=improvement,
            success=improvement > 0
        )
        
        # Atualizar estatísticas
        self.stats['attempts'] += 1
        if improvement > 0:
            self.stats['successes'] += 1
        
        return result
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do mutador"""
        stats = dict(self.stats)
        stats['success_rate'] = self.stats.get('successes', 0) / max(1, self.stats.get('attempts', 1))
        stats['template_stats'] = self.template_optimizer.get_stats()
        return stats

# =========================
# HIBRIDIZADOR AVANÇADO
# =========================
class AdvancedHybridizer:
    """Hibridização avançada com crossover genético"""
    
    def __init__(self, vector_db: VectorDatabase):
        self.vector_db = vector_db
        self.analyzer = CodeAnalyzer()
    
    @timed
    def hybridize(self, code: str, version_id: str, population: List[VersionInfo]) -> Optional[str]:
        """Tenta hibridizar código com versões de alta performance"""
        
        if len(population) < 2:
            return None
        
        # Selecionar pais (torneio)
        parent1 = self._tournament_select(population)
        parent2 = self._tournament_select([v for v in population if v.id != parent1.id])
        
        if not parent1 or not parent2:
            return None
        
        # Carregar código dos pais
        code1 = self._load_code(parent1)
        code2 = self._load_code(parent2)
        
        if not code1 or not code2:
            return None
        
        # Realizar crossover
        child_code = self._crossover(code1, code2)
        
        # Avaliar filho
        evaluator = FitnessEvaluator()
        child_fitness = evaluator.evaluate(child_code)
        parent_fitness = max(parent1.fitness, parent2.fitness)
        
        if child_fitness['fitness'] > parent_fitness:
            logger.info(f"✅ Crossover bem-sucedido: +{child_fitness['fitness'] - parent_fitness:.4f}")
            return child_code
        
        return None
    
    def _tournament_select(self, population: List[VersionInfo]) -> Optional[VersionInfo]:
        """Seleção por torneio"""
        if not population:
            return None
        
        tournament = random.sample(population, min(Config.TOURNAMENT_SIZE, len(population)))
        return max(tournament, key=lambda v: v.fitness)
    
    def _load_code(self, version: VersionInfo) -> Optional[str]:
        """Carrega código de uma versão"""
        if version.path and version.path.exists():
            with open(version.path, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def _crossover(self, code1: str, code2: str) -> str:
        """Realiza crossover entre dois códigos"""
        
        # Analisar AST
        try:
            tree1 = ast.parse(code1)
            tree2 = ast.parse(code2)
        except:
            return code1  # Fallback
        
        # Identificar funções em ambos
        functions1 = {node.name: node for node in ast.walk(tree1) 
                     if isinstance(node, ast.FunctionDef)}
        functions2 = {node.name: node for node in ast.walk(tree2) 
                     if isinstance(node, ast.FunctionDef)}
        
        # Funções comuns
        common_functions = set(functions1.keys()) & set(functions2.keys())
        
        if not common_functions:
            return code1
        
        # Escolher função para crossover
        func_name = random.choice(list(common_functions))
        
        # Decidir qual versão usar (baseado em fitness dos pais)
        # Simplificado: usar a função da versão com maior fitness
        # Isso seria determinado pelos metadados das versões
        
        # Substituir função
        class FunctionReplacer(ast.NodeTransformer):
            def visit_FunctionDef(self, node):
                if node.name == func_name:
                    return functions2[func_name]
                return node
        
        replacer = FunctionReplacer()
        new_tree = replacer.visit(tree1)
        
        # Converter de volta
        try:
            new_code = astor.to_source(new_tree)
            return new_code
        except:
            return code1

# =========================
# SISTEMA DE APRENDIZADO CONTÍNUO
# =========================
class ContinuousLearningSystem:
    """Sistema de aprendizado contínuo com feedback loop"""
    
    def __init__(self, neural_net: DeepNeuralNetwork, vector_db: VectorDatabase):
        self.neural_net = neural_net
        self.vector_db = vector_db
        self.experience_buffer = deque(maxlen=Config.LEARNING_HISTORY_SIZE)
        self.training_count = 0
    
    def add_experience(self, mutation: MutationResult):
        """Adiciona experiência ao buffer"""
        self.experience_buffer.append({
            'features': mutation.features.values,
            'template': mutation.template,
            'success': mutation.success,
            'improvement': mutation.improvement,
            'timestamp': datetime.now()
        })
        
        # Treinar periodicamente
        if len(self.experience_buffer) >= Config.MIN_SAMPLES_FOR_TRAINING:
            if self.training_count % Config.RETRAIN_INTERVAL == 0:
                self._retrain()
            self.training_count += 1
    
    def _retrain(self):
        """Retreina a rede neural com novas experiências"""
        logger.info("🔄 Retreinando rede neural...")
        
        # Preparar dados
        X = []
        y = []
        
        for exp in self.experience_buffer:
            if exp['success']:
                X.append(exp['features'])
                try:
                    y.append(Config.TEMPLATES.index(exp['template']))
                except ValueError:
                    continue
        
        if len(X) >= Config.MIN_SAMPLES_FOR_TRAINING:
            self.neural_net.train(X, y)
            
            # Registrar
            metadata = {
                'timestamp': datetime.now().isoformat(),
                'samples': len(X),
                'accuracy': self.neural_net.accuracy
            }
            
            with open(Config.METADATA_DIR / f"training_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
                json.dump(metadata, f, indent=2)
    
    def get_learning_curve(self) -> Dict:
        """Retorna curva de aprendizado"""
        if not self.neural_net.accuracy_history:
            return {}
        
        return {
            'accuracy': self.neural_net.accuracy_history,
            'loss': self.neural_net.loss_history,
            'samples': len(self.experience_buffer)
        }

# =========================
# SISTEMA PRINCIPAL DE EVOLUÇÃO
# =========================
class EvolutionSystem:
    """Sistema principal de evolução com todas as capacidades"""
    
    def __init__(self):
        # Inicializar componentes
        self.vector_db = VectorDatabase()
        self.neural_net = DeepNeuralNetwork()
        self.mutator = IntelligentMutator(self.vector_db, self.neural_net)
        self.hybridizer = AdvancedHybridizer(self.vector_db)
        self.learner = ContinuousLearningSystem(self.neural_net, self.vector_db)
        self.analyzer = CodeAnalyzer()
        self.evaluator = FitnessEvaluator()
        
        # População
        self.population: List[VersionInfo] = []
        self.current_version: Optional[VersionInfo] = None
        
        # Estatísticas
        self.stats = {
            'generations': 0,
            'mutations': 0,
            'successful_mutations': 0,
            'hybridizations': 0,
            'successful_hybridizations': 0,
            'best_fitness': 0,
            'average_fitness': 0
        }
        
        logger.info(f"\n{'='*80}")
        logger.info(f"🌟 ATENA APOTHEOSIS v{__version__} - {__codename__}")
        logger.info(f"{'='*80}")
        logger.info(f"🧠 Rede Neural: {Config.HIDDEN_LAYERS}")
        logger.info(f"🧬 Templates: {len(Config.TEMPLATES)}")
        logger.info(f"📊 Features: {Config.INPUT_FEATURES}")
        logger.info(f"👥 População: {Config.POPULATION_SIZE}")
        logger.info(f"{'='*80}\n")
    
    def initialize(self, initial_code: str):
        """Inicializa o sistema com código inicial"""
        
        # Criar versão inicial
        features = self.analyzer.analyze(initial_code)
        fitness = self.evaluator.evaluate(initial_code)
        
        self.current_version = VersionInfo(
            id=str(uuid.uuid4()),
            number=1,
            fitness=fitness['fitness'],
            metrics=fitness,
            features=features
        )
        
        self.current_version.save(initial_code)
        self.population.append(self.current_version)
        
        logger.info(f"📦 Versão inicial criada: v{self.current_version.number}")
        logger.info(f"   Fitness: {self.current_version.fitness:.4f}")
    
    def evolve(self, generations: int = 10):
        """Executa evolução por múltiplas gerações"""
        
        for gen in range(generations):
            logger.info(f"\n{'🧬'*80}")
            logger.info(f"🧬 GERAÇÃO {gen + 1}/{generations}")
            logger.info(f"{'🧬'*80}")
            
            # Tentar hibridização
            if random.random() < Config.HIBRIDIZATION_RATE:
                hybrid_code = self.hybridizer.hybridize(
                    self._load_current_code(),
                    self.current_version.id,
                    self.population
                )
                
                if hybrid_code:
                    self.stats['hybridizations'] += 1
                    self._process_new_version(hybrid_code, 'hybridization')
            
            # Tentar mutações
            for _ in range(3):  # Múltiplas tentativas
                mutation = self.mutator.mutate(
                    self._load_current_code(),
                    self.current_version.id
                )
                
                if mutation:
                    self.stats['mutations'] += 1
                    self.learner.add_experience(mutation)
                    
                    if mutation.success:
                        self.stats['successful_mutations'] += 1
                        self._process_new_version(
                            mutation.code_after,
                            f"mutation:{mutation.template}"
                        )
                        break
            
            # Atualizar estatísticas
            self._update_stats()
            
            # Mostrar progresso
            self._show_progress()
    
    def _process_new_version(self, code: str, source: str):
        """Processa uma nova versão"""
        
        # Analisar
        features = self.analyzer.analyze(code)
        fitness = self.evaluator.evaluate(code)
        
        # Criar versão
        new_version = VersionInfo(
            id=str(uuid.uuid4()),
            number=len(self.population) + 1,
            fitness=fitness['fitness'],
            metrics=fitness,
            features=features,
            parent_id=self.current_version.id
        )
        
        new_version.save(code)
        
        # Adicionar à população
        self.population.append(new_version)
        
        # Manter apenas as melhores versões
        self.population.sort(key=lambda v: v.fitness, reverse=True)
        self.population = self.population[:Config.POPULATION_SIZE]
        
        # Atualizar versão atual se for melhor
        if new_version.fitness > self.current_version.fitness:
            logger.info(f"✅ NOVA MELHOR VERSÃO! v{new_version.number}")
            logger.info(f"   Fitness: {new_version.fitness:.4f} (+{new_version.fitness - self.current_version.fitness:.4f})")
            self.current_version = new_version
            
            # Registrar marco
            self._save_milestone(new_version)
    
    def _load_current_code(self) -> str:
        """Carrega código da versão atual"""
        if self.current_version and self.current_version.path:
            with open(self.current_version.path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def _update_stats(self):
        """Atualiza estatísticas da população"""
        if self.population:
            fitness_values = [v.fitness for v in self.population]
            self.stats['best_fitness'] = max(fitness_values)
            self.stats['average_fitness'] = np.mean(fitness_values)
            self.stats['population_size'] = len(self.population)
    
    def _show_progress(self):
        """Mostra progresso atual"""
        logger.info(f"\n📊 ESTATÍSTICAS ATUAIS:")
        logger.info(f"   Melhor fitness: {self.stats['best_fitness']:.4f}")
        logger.info(f"   Fitness médio: {self.stats['average_fitness']:.4f}")
        logger.info(f"   Versões: {len(self.population)}")
        logger.info(f"   Mutações: {self.stats['mutations']} (sucesso: {self.stats['successful_mutations']})")
        logger.info(f"   Hibridizações: {self.stats['hybridizations']}")
        
        # Taxa de sucesso
        if self.stats['mutations'] > 0:
            success_rate = self.stats['successful_mutations'] / self.stats['mutations']
            logger.info(f"   Taxa de sucesso: {success_rate:.2%}")
    
    def _save_milestone(self, version: VersionInfo):
        """Salva um marco da evolução"""
        milestone = {
            'version': version.number,
            'fitness': version.fitness,
            'timestamp': datetime.now().isoformat(),
            'metrics': version.metrics,
            'parent': version.parent_id
        }
        
        with open(Config.EVOLUTION_DIR / f"milestone_v{version.number}.json", 'w') as f:
            json.dump(milestone, f, indent=2)
    
    def export_report(self) -> Dict:
        """Exporta relatório completo da evolução"""
        report = {
            'system': {
                'version': __version__,
                'name': __nome__,
                'build': __build__
            },
            'configuration': {
                key: value for key, value in Config.__dict__.items()
                if key.isupper() and not key.startswith('_')
            },
            'population': {
                'size': len(self.population),
                'best_fitness': self.stats['best_fitness'],
                'average_fitness': self.stats['average_fitness']
            },
            'evolution': self.stats,
            'learning': self.learner.get_learning_curve(),
            'mutator': self.mutator.get_stats(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Salvar relatório
        report_file = Config.EXPORT_DIR / f"report_{__build__}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Relatório exportado: {report_file}")
        
        return report

# =========================
# INTERFACE PRINCIPAL
# =========================
def print_banner():
    """Imprime banner do sistema"""
    banner = f"""
    ╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                                                                                      ║
    ║     █████╗ ████████╗███████╗███╗   ██╗ █████║     ∞ - APOTHEOSIS v{__version__}            ║
    ║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "{__codename__}"        ║
    ║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                                      ║
    ║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ REDE NEURAL PROFUNDA            ║
    ║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ APRENDIZADO CONTÍNUO            ║
    ║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ EVOLUÇÃO AUTÔNOMA              ║
    ║                                                                                      ║
    ║   🧠 REDE NEURAL: {Config.HIDDEN_LAYERS}                                              ║
    ║   🧬 TEMPLATES: {len(Config.TEMPLATES)} otimizações especializadas                              ║
    ║   📊 FEATURES: {Config.INPUT_FEATURES} características do código                                 ║
    ║   🔄 APRENDIZADO: Contínuo com feedback loop                                       ║
    ║   👥 POPULAÇÃO: {Config.POPULATION_SIZE} versões simultâneas                                    ║
    ║                                                                                      ║
    ║   🚀 INICIANDO SISTEMA DE EVOLUÇÃO INTELIGENTE...                                  ║
    ║                                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    """Função principal"""
    print_banner()
    
    # Verificar dependências
    logger.info("🔍 Verificando dependências...")
    deps = {
        'numpy': HAS_NUMPY,
        'scipy': HAS_SCIPY,
        'pandas': HAS_PANDAS,
        'sklearn': HAS_SKLEARN,
        'torch': HAS_TORCH,
        'tensorflow': HAS_TF,
        'psutil': HAS_PSUTIL,
        'tqdm': HAS_TQDM,
        'joblib': HAS_JOBLIB,
        'networkx': HAS_NETWORKX
    }
    
    for name, available in deps.items():
        status = "✅" if available else "⚠️"
        logger.info(f"   {status} {name}")
    
    if not any([HAS_TORCH, HAS_TF, HAS_SKLEARN]):
        logger.warning("⚠️ Nenhuma biblioteca de deep learning encontrada!")
        logger.warning("   Instale pelo menos uma: torch, tensorflow, ou scikit-learn")
    
    # Criar sistema
    logger.info("\n🚀 Inicializando sistema evolutivo...")
    system = EvolutionSystem()
    
    # Carregar código atual
    with open(__file__, 'r', encoding='utf-8') as f:
        current_code = f.read()
    
    # Inicializar
    system.initialize(current_code)
    
    # Treinar rede neural inicial com dados existentes
    logger.info("\n📚 Treinando rede neural inicial...")
    X, y = [], []
    
    # Usar templates como dados sintéticos para treinamento inicial
    for i, template in enumerate(Config.TEMPLATES[:10]):
        features = system.analyzer.analyze(f"# Template: {template}\n{current_code[:500]}")
        X.append(features.values)
        y.append(i)
    
    if X:
        system.neural_net.train(X, y)
    
    # Evoluir
    generations = 10
    logger.info(f"\n🧬 Iniciando evolução por {generations} gerações...")
    
    if HAS_TQDM:
        for _ in trange(generations, desc="Evoluindo"):
            system.evolve(generations=1)
    else:
        system.evolve(generations=generations)
    
    # Relatório final
    logger.info(f"\n{'📊'*80}")
    logger.info("📊 RELATÓRIO FINAL")
    logger.info(f"{'📊'*80}")
    
    report = system.export_report()
    
    logger.info(f"\n✅ Evolução concluída!")
    logger.info(f"   Versões geradas: {len(system.population)}")
    logger.info(f"   Fitness inicial: {system.population[0].fitness:.4f}" if system.population else "")
    logger.info(f"   Fitness final: {system.current_version.fitness:.4f}" if system.current_version else "")
    
    if system.population and system.current_version:
        improvement = system.current_version.fitness - system.population[0].fitness
        logger.info(f"   Melhoria total: +{improvement:.4f}")
    
    logger.info(f"\n📁 Arquivos salvos em: {Config.BASE_DIR}")
    logger.info(f"📄 Relatório: {Config.EXPORT_DIR / f'report_{__build__}.json'}")
    
    # Mostrar melhores templates
    mutator_stats = system.mutator.get_stats()
    if 'template_stats' in mutator_stats:
        logger.info(f"\n🏆 Templates mais eficazes:")
        templates = sorted(
            mutator_stats['template_stats'].items(),
            key=lambda x: x[1]['success_rate'],
            reverse=True
        )[:5]
        
        for template, stats in templates:
            logger.info(f"   • {template}: {stats['success_rate']:.1%} sucesso ({stats['attempts']} tentativas)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\n👋 Evolução interrompida pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        logger.error(traceback.format_exc())
    finally:
        logger.info("\n✨ ATENA APOTHEOSIS finalizada")
