#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ ATENA NEURAL - SISTEMA COM REDES NEURAIS REAIS
Versão 2.0 - Com Deep Learning Funcional
"""

import ast
import time
import json
import uuid
import random
import hashlib
import sqlite3
import subprocess
import tempfile
import traceback
import gc
import re
import logging
import pickle
import warnings
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field, asdict
from collections import defaultdict, deque
import functools
import numpy as np

warnings.filterwarnings('ignore')

# =========================
# BIBLIOTECAS REAIS PARA ML
# =========================
try:
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import RandomForestClassifier
    HAS_SKLEARN = True
    print("✅ Scikit-learn carregado")
except ImportError:
    HAS_SKLEARN = False
    print("⚠️ Instale: pip install scikit-learn")

try:
    import joblib
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False
    print("⚠️ Instale: pip install joblib")

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("⚠️ Instale: pip install psutil")

# =========================
# CONFIGURAÇÕES
# =========================
BASE_DIR = Path.home() / ".atena_neural"
BASE_DIR.mkdir(exist_ok=True)

@dataclass
class Config:
    """Configurações do sistema neural"""
    BASE_DIR = BASE_DIR
    DB_PATH = BASE_DIR / "neural_memory.db"
    MODELS_DIR = BASE_DIR / "models"
    CODE_DIR = BASE_DIR / "code"
    LOGS_DIR = BASE_DIR / "logs"
    VECTOR_DIR = BASE_DIR / "vectors"
    
    # Configurações da Rede Neural
    INPUT_FEATURES = 50
    HIDDEN_LAYERS = (100, 50, 25)
    MAX_ITER = 500
    LEARNING_RATE = 0.001
    
    # Configurações do Sistema
    MAX_ITERATIONS = 10
    TIMEOUT_SECONDS = 3
    POPULATION_SIZE = 20
    MIN_SAMPLES_FOR_TRAINING = 10
    
    for dir_path in [MODELS_DIR, CODE_DIR, LOGS_DIR, VECTOR_DIR]:
        dir_path.mkdir(exist_ok=True)

# =========================
# BANCO DE DADOS VETORIAL
# =========================
class VectorDatabase:
    """Banco de dados para vetores de características"""
    
    def __init__(self):
        self.conn = sqlite3.connect(str(Config.DB_PATH))
        self._init_db()
    
    def _init_db(self):
        cursor = self.conn.cursor()
        
        # Tabela de vetores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feature_vectors (
                id TEXT PRIMARY KEY,
                code_hash TEXT UNIQUE,
                features TEXT,
                template_used TEXT,
                improvement REAL,
                success BOOLEAN,
                created_at TIMESTAMP
            )
        ''')
        
        # Tabela de versões
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS versions (
                id TEXT PRIMARY KEY,
                code_hash TEXT,
                fitness REAL,
                parent_id TEXT,
                generation INTEGER,
                template TEXT,
                features TEXT
            )
        ''')
        
        # Índices
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_code_hash ON feature_vectors(code_hash)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_success ON feature_vectors(success)')
        
        self.conn.commit()
    
    def add_vector(self, code: str, template: str, improvement: float, success: bool):
        """Adiciona um vetor de características"""
        code_hash = hashlib.md5(code.encode()).hexdigest()
        features = FeatureExtractor.extract(code)
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO feature_vectors 
            (id, code_hash, features, template_used, improvement, success, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            str(uuid.uuid4()),
            code_hash,
            json.dumps(features),
            template,
            improvement,
            success,
            datetime.now().isoformat()
        ))
        self.conn.commit()
        
        return features
    
    def get_training_data(self, min_samples: int = 10) -> Tuple[List, List]:
        """Recupera dados para treinamento"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT features, template_used, improvement 
            FROM feature_vectors 
            WHERE success = 1
            ORDER BY created_at DESC
            LIMIT 1000
        ''')
        
        X = []
        y = []
        
        for row in cursor.fetchall():
            features = json.loads(row[0])
            template = row[1]
            improvement = row[2]
            
            # Só usar exemplos com melhoria significativa
            if improvement > 0.01:
                X.append(features)
                y.append(template)
        
        return X, y
    
    def get_similar_successes(self, features: List[float], threshold: float = 0.7) -> List[Dict]:
        """Encontra casos de sucesso similares"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT features, template_used, improvement 
            FROM feature_vectors 
            WHERE success = 1
        ''')
        
        results = []
        features_array = np.array(features)
        
        for row in cursor.fetchall():
            db_features = np.array(json.loads(row[0]))
            
            # Similaridade de cosseno
            norm1 = np.linalg.norm(features_array)
            norm2 = np.linalg.norm(db_features)
            
            if norm1 > 0 and norm2 > 0:
                similarity = np.dot(features_array, db_features) / (norm1 * norm2)
                
                if similarity > threshold:
                    results.append({
                        'template': row[1],
                        'improvement': row[2],
                        'similarity': float(similarity)
                    })
        
        # Ordenar por similaridade
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:5]
    
    def close(self):
        self.conn.close()

# =========================
# EXTRATOR DE CARACTERÍSTICAS
# =========================
class FeatureExtractor:
    """Extrai características do código para a rede neural"""
    
    @staticmethod
    def extract(code: str) -> List[float]:
        """Extrai vetor de características do código"""
        features = []
        
        # 1. Métricas básicas (normalizadas)
        lines = code.split('\n')
        features.append(min(len(lines) / 100, 1.0))  # Linhas
        features.append(min(len(code) / 5000, 1.0))  # Caracteres
        
        # 2. Complexidade
        features.append(len(re.findall(r'if |elif |else:', code)) / 20)  # Condicionais
        features.append(len(re.findall(r'for |while ', code)) / 10)  # Loops
        features.append(len(re.findall(r'try:|except:|finally:', code)) / 5)  # Exceções
        
        # 3. Estruturas
        features.append(len(re.findall(r'def ', code)) / 10)  # Funções
        features.append(len(re.findall(r'class ', code)) / 5)  # Classes
        features.append(len(re.findall(r'lambda', code)) / 5)  # Lambdas
        
        # 4. Operações
        features.append(len(re.findall(r'\[\]|\{\}|\(\)', code)) / 20)  # Estruturas vazias
        features.append(len(re.findall(r'\.append\(|\.extend\(', code)) / 10)  # Operações de lista
        features.append(len(re.findall(r'\.join\(', code)) / 5)  # String operations
        
        # 5. Importações
        imports = len(re.findall(r'^import |^from ', code, re.MULTILINE))
        features.append(min(imports / 10, 1.0))
        
        # 6. Comentários e docstrings
        comments = len(re.findall(r'#.*$', code, re.MULTILINE))
        features.append(min(comments / 20, 1.0))
        docstrings = len(re.findall(r'""".*?"""', code, re.DOTALL))
        features.append(min(docstrings / 5, 1.0))
        
        # 7. Complexidade ciclomática aproximada
        try:
            tree = ast.parse(code)
            complexity = 1
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    complexity += len(node.values) - 1
            features.append(min(complexity / 20, 1.0))
        except:
            features.append(0.0)
        
        # 8. Presença de padrões de otimização
        patterns = [
            r'numpy|np\.',
            r'@lru_cache',
            r'yield',
            r'\[\s*\w+\s+for',
            r'\.join\(.*\)',
            r'__slots__',
            r'with open',
            r'multiprocessing',
            r'asyncio',
            r'f"',
        ]
        
        for pattern in patterns:
            features.append(1.0 if re.search(pattern, code) else 0.0)
        
        # Garantir tamanho fixo
        while len(features) < Config.INPUT_FEATURES:
            features.append(0.0)
        
        return features[:Config.INPUT_FEATURES]

# =========================
# REDE NEURAL REAL
# =========================
class NeuralOptimizer:
    """Rede neural para recomendar otimizações"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.templates = [
            'list_comprehension',
            'string_join',
            'use_set_for_membership',
            'cache_results',
            'use_generators',
            'remove_dead_code',
            'use_local_vars',
            'vectorize_loop'
        ]
        self.accuracy = 0.0
        self.trained = False
        
        # Tentar carregar modelo existente
        self._load_model()
    
    def _build_model(self):
        """Constrói a rede neural"""
        return MLPClassifier(
            hidden_layer_sizes=Config.HIDDEN_LAYERS,
            activation='relu',
            solver='adam',
            alpha=0.001,
            batch_size='auto',
            learning_rate='adaptive',
            learning_rate_init=Config.LEARNING_RATE,
            max_iter=Config.MAX_ITER,
            shuffle=True,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=10,
            verbose=False
        )
    
    def train(self, X: List[List[float]], y: List[str]):
        """Treina a rede neural"""
        if len(X) < Config.MIN_SAMPLES_FOR_TRAINING:
            print(f"⚠️ Poucos dados para treinamento: {len(X)} < {Config.MIN_SAMPLES_FOR_TRAINING}")
            return
        
        print(f"\n🧠 Treinando rede neural com {len(X)} exemplos...")
        
        # Converter para numpy
        X = np.array(X)
        
        # Normalizar
        X_scaled = self.scaler.fit_transform(X)
        
        # Codificar labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Dividir treino/validação
        X_train, X_val, y_train, y_val = train_test_split(
            X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Criar e treinar modelo
        self.model = self._build_model()
        self.model.fit(X_train, y_train)
        
        # Avaliar
        y_pred = self.model.predict(X_val)
        self.accuracy = accuracy_score(y_val, y_pred)
        
        print(f"✅ Acurácia da rede neural: {self.accuracy:.2%}")
        print(f"📊 Relatório por template:")
        print(classification_report(y_val, y_pred, 
                                   target_names=self.label_encoder.classes_, 
                                   zero_division=0))
        
        self.trained = True
        self._save_model()
    
    def predict(self, features: List[float]) -> Tuple[Optional[str], float]:
        """Prediz o melhor template"""
        if not self.trained or self.model is None:
            return None, 0.0
        
        # Normalizar
        features = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        
        # Predizer probabilidades
        probabilities = self.model.predict_proba(features_scaled)[0]
        best_idx = np.argmax(probabilities)
        confidence = probabilities[best_idx]
        
        if confidence > 0.3:  # Threshold mínimo
            template = self.label_encoder.inverse_transform([best_idx])[0]
            return template, confidence
        
        return None, confidence
    
    def get_all_probabilities(self, features: List[float]) -> Dict[str, float]:
        """Retorna probabilidades para todos os templates"""
        if not self.trained or self.model is None:
            return {}
        
        features = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        return {
            template: prob 
            for template, prob in zip(self.label_encoder.classes_, probabilities)
        }
    
    def _save_model(self):
        """Salva o modelo treinado"""
        model_path = Config.MODELS_DIR / "neural_optimizer.pkl"
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'accuracy': self.accuracy,
            'templates': self.templates
        }
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"💾 Modelo salvo em: {model_path}")
    
    def _load_model(self):
        """Carrega modelo existente"""
        model_path = Config.MODELS_DIR / "neural_optimizer.pkl"
        
        if model_path.exists():
            try:
                with open(model_path, 'rb') as f:
                    model_data = pickle.load(f)
                
                self.model = model_data['model']
                self.scaler = model_data['scaler']
                self.label_encoder = model_data['label_encoder']
                self.accuracy = model_data['accuracy']
                self.templates = model_data['templates']
                self.trained = True
                
                print(f"🤖 Modelo carregado (acurácia: {self.accuracy:.2%})")
            except Exception as e:
                print(f"⚠️ Erro carregando modelo: {e}")

# =========================
# TEMPLATES DE OTIMIZAÇÃO
# =========================
class OptimizerTemplates:
    """Templates reais de otimização"""
    
    @staticmethod
    def apply(code: str, template: str) -> str:
        """Aplica um template de otimização"""
        
        if template == 'list_comprehension':
            return OptimizerTemplates._list_comprehension(code)
        elif template == 'string_join':
            return OptimizerTemplates._string_join(code)
        elif template == 'use_set_for_membership':
            return OptimizerTemplates._use_set(code)
        elif template == 'cache_results':
            return OptimizerTemplates._add_cache(code)
        elif template == 'use_generators':
            return OptimizerTemplates._use_generators(code)
        elif template == 'remove_dead_code':
            return OptimizerTemplates._remove_dead(code)
        elif template == 'use_local_vars':
            return OptimizerTemplates._local_vars(code)
        elif template == 'vectorize_loop':
            return OptimizerTemplates._vectorize(code)
        
        return code
    
    @staticmethod
    def _list_comprehension(code: str) -> str:
        """Converte loop com append para list comprehension"""
        pattern = r'(\w+)\s*=\s*\[\]\s*\n\s+for\s+(\w+)\s+in\s+(\w+):\s*\n\s+\1\.append\(([^)]+)\)'
        
        def replace(match):
            var, item, iterable, expr = match.groups()
            return f"{var} = [{expr} for {item} in {iterable}]"
        
        return re.sub(pattern, replace, code, flags=re.MULTILINE)
    
    @staticmethod
    def _string_join(code: str) -> str:
        """Otimiza concatenação de strings"""
        # Procurar padrão de concatenação em loop
        lines = code.split('\n')
        modified = False
        
        for i, line in enumerate(lines):
            if '+= ' in line and ('for ' in ' '.join(lines[max(0, i-5):i])):
                # Extrair variável
                var_match = re.match(r'\s*(\w+)\s*\+=', line)
                if var_match:
                    var = var_match.group(1)
                    
                    # Coletar partes
                    parts = []
                    j = i
                    while j < len(lines) and f'{var} +=' in lines[j]:
                        part = lines[j].split('+=')[1].strip()
                        parts.append(part)
                        lines[j] = ''
                        j += 1
                    
                    if parts:
                        # Inserir join
                        lines[i-1] = f"    {var} = ''.join([{', '.join(parts)}])"
                        modified = True
        
        if modified:
            return '\n'.join(lines)
        return code
    
    @staticmethod
    def _use_set(code: str) -> str:
        """Usa set para operações de pertencimento"""
        # Procurar if item in lista em loop
        pattern = r'if\s+(\w+)\s+in\s+(\w+):'
        
        def check_and_replace(match):
            item, container = match.groups()
            
            # Verificar se container é lista
            if f"{container} = [" in code or f"{container}.append" in code:
                return f"if {item} in set({container}):"
            return match.group(0)
        
        return re.sub(pattern, check_and_replace, code)
    
    @staticmethod
    def _add_cache(code: str) -> str:
        """Adiciona cache LRU para funções recursivas"""
        if 'from functools import lru_cache' not in code:
            code = 'from functools import lru_cache\n' + code
        
        # Procurar funções recursivas
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            if line.strip().startswith('def '):
                func_name = line.split('def ')[1].split('(')[0]
                
                # Verificar se é recursiva
                for j in range(i+1, min(i+20, len(lines))):
                    if f'{func_name}(' in lines[j] and 'return' in lines[j]:
                        # Adicionar decorator
                        if not lines[i-1].strip().startswith('@'):
                            lines.insert(i, '@lru_cache(maxsize=128)')
                        break
        
        return '\n'.join(lines)
    
    @staticmethod
    def _use_generators(code: str) -> str:
        """Converte list comprehensions grandes para generators"""
        # Procurar list comprehensions que podem ser generators
        pattern = r'\[\s*(\w+)\s+for\s+(\w+)\s+in\s+range\(\s*(\d{4,})\s*\)\s*\]'
        
        def replace(match):
            expr, var, size = match.groups()
            return f"({expr} for {var} in range({size}))"
        
        return re.sub(pattern, replace, code)
    
    @staticmethod
    def _remove_dead(code: str) -> str:
        """Remove código morto"""
        lines = code.split('\n')
        result = []
        skip = False
        
        for line in lines:
            if 'if False:' in line or 'if 0:' in line:
                skip = True
                result.append(line)
            elif skip and line.startswith('    '):
                continue
            else:
                skip = False
                result.append(line)
        
        return '\n'.join(result)
    
    @staticmethod
    def _local_vars(code: str) -> str:
        """Otimiza acesso a atributos repetidos"""
        # Análise simplificada - marcar para revisão
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            if 'self.' in line and 'for ' in line:
                # Extrair atributo
                attr_match = re.search(r'self\.(\w+)', line)
                if attr_match:
                    attr = attr_match.group(1)
                    # Sugerir cache
                    lines[i] = f"    {attr} = self.{attr}\n" + lines[i]
        
        return '\n'.join(lines)
    
    @staticmethod
    def _vectorize(code: str) -> str:
        """Sugere vetorização com numpy"""
        if 'import numpy' not in code and 'np.' not in code:
            # Procurar loops que podem ser vetorizados
            if 'for i in range' in code and '[' in code and ']' in code:
                code = 'import numpy as np\n' + code
                code += '\n# TODO: Considere vetorizar loops com numpy\n'
        
        return code

# =========================
# EXECUTOR DE CÓDIGO
# =========================
class CodeExecutor:
    """Executa código com medição"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def execute(self, code: str) -> Dict[str, Any]:
        """Executa e mede performance"""
        result = {
            'success': False,
            'time': float('inf'),
            'memory': 0,
            'output': '',
            'error': ''
        }
        
        # Criar arquivo
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', 
                                        dir=self.temp_dir, delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Medir tempo
            start = time.perf_counter()
            
            # Executar
            proc = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=Config.TIMEOUT_SECONDS,
                env={'PYTHONPATH': ''}
            )
            
            end = time.perf_counter()
            
            result['time'] = end - start
            result['output'] = proc.stdout
            result['success'] = proc.returncode == 0
            
            if proc.stderr:
                result['error'] = proc.stderr
            
            # Medir memória
            if HAS_PSUTIL:
                process = psutil.Process()
                result['memory'] = process.memory_info().rss / 1024 / 1024
            
        except subprocess.TimeoutExpired:
            result['error'] = f"Timeout"
        except Exception as e:
            result['error'] = str(e)
        finally:
            try:
                Path(temp_file).unlink()
            except:
                pass
        
        return result

# =========================
# AVALIADOR NEURAL
# =========================
class NeuralEvaluator:
    """Avalia código com suporte da rede neural"""
    
    def __init__(self, neural_net: NeuralOptimizer, vector_db: VectorDatabase):
        self.executor = CodeExecutor()
        self.neural_net = neural_net
        self.vector_db = vector_db
    
    def evaluate(self, code: str) -> Tuple[float, Dict]:
        """Avalia código e recomenda otimizações"""
        
        # Executar
        result = self.executor.execute(code)
        
        if not result['success']:
            return 0.0, result
        
        # Extrair características
        features = FeatureExtractor.extract(code)
        
        # Calcular fitness base
        time_score = 1.0 / (result['time'] + 0.1)
        memory_score = 1.0 / (result.get('memory', 1) + 1)
        
        fitness = (time_score * 0.6 + memory_score * 0.4)
        
        # Adicionar recomendações da rede neural
        if self.neural_net.trained:
            template, confidence = self.neural_net.predict(features)
            if template:
                result['recommended_template'] = template
                result['confidence'] = confidence
            
            # Todas as probabilidades
            result['template_probs'] = self.neural_net.get_all_probabilities(features)
        
        # Buscar casos similares
        similar = self.vector_db.get_similar_successes(features)
        if similar:
            result['similar_successes'] = similar
        
        result['fitness'] = fitness
        result['features'] = features
        
        return fitness, result

# =========================
# SISTEMA PRINCIPAL NEURAL
# =========================
class NeuralEvolutionSystem:
    """Sistema de evolução com rede neural"""
    
    def __init__(self):
        self.vector_db = VectorDatabase()
        self.neural_net = NeuralOptimizer()
        self.evaluator = NeuralEvaluator(self.neural_net, self.vector_db)
        self.population = []
        self.generation = 0
        self.training_data = []
        
        print("\n" + "="*70)
        print("🧠 ATENA NEURAL - Evolução com Deep Learning")
        print("="*70)
    
    def initialize(self, initial_code: str):
        """Inicializa o sistema"""
        
        # Avaliar código inicial
        fitness, metrics = self.evaluator.evaluate(initial_code)
        
        # Salvar
        version_id = hashlib.md5(initial_code.encode()).hexdigest()[:8]
        
        self.population.append({
            'id': version_id,
            'code': initial_code,
            'fitness': fitness,
            'metrics': metrics,
            'generation': 0
        })
        
        print(f"\n📦 Versão inicial: {version_id}")
        print(f"   Fitness: {fitness:.4f}")
        print(f"   Tempo: {metrics.get('time', 0):.4f}s")
        
        if 'recommended_template' in metrics:
            print(f"   Recomendação: {metrics['recommended_template']} (conf: {metrics['confidence']:.2f})")
    
    def evolve(self, iterations: int = 10):
        """Executa evolução neural"""
        
        for i in range(iterations):
            self.generation += 1
            print(f"\n{'='*50}")
            print(f"🧬 Geração {self.generation}")
            print(f"{'='*50}")
            
            if not self.population:
                break
            
            # Selecionar melhor atual
            current = max(self.population, key=lambda x: x['fitness'])
            
            # Obter características
            features = FeatureExtractor.extract(current['code'])
            
            # Decidir template
            template = self._select_template(features)
            
            if not template:
                print("⚠️ Nenhum template selecionado")
                continue
            
            print(f"🎯 Template selecionado: {template}")
            
            # Aplicar template
            mutated = OptimizerTemplates.apply(current['code'], template)
            
            if mutated == current['code']:
                print("⚠️ Template não alterou o código")
                continue
            
            # Avaliar mutação
            new_fitness, metrics = self.evaluator.evaluate(mutated)
            improvement = new_fitness - current['fitness']
            
            # Registrar no banco vetorial
            self.vector_db.add_vector(
                mutated, template, improvement, 
                success=improvement > 0
            )
            
            # Adicionar à população
            version_id = hashlib.md5(mutated.encode()).hexdigest()[:8]
            
            self.population.append({
                'id': version_id,
                'code': mutated,
                'fitness': new_fitness,
                'metrics': metrics,
                'template': template,
                'parent': current['id'],
                'generation': self.generation,
                'improvement': improvement
            })
            
            # Mostrar resultado
            if improvement > 0:
                print(f"✅ MELHORIA! +{improvement:.4f}")
                print(f"   Novo fitness: {new_fitness:.4f}")
                print(f"   Tempo: {metrics.get('time', 0):.4f}s")
                
                # Coletar para treinamento
                self.training_data.append((features, template, improvement))
            else:
                print(f"❌ Sem melhoria: {improvement:.4f}")
            
            # Manter população
            self.population.sort(key=lambda x: x['fitness'], reverse=True)
            self.population = self.population[:Config.POPULATION_SIZE]
            
            # Estatísticas
            best = self.population[0]
            avg_fitness = sum(v['fitness'] for v in self.population) / len(self.population)
            
            print(f"\n📊 Melhor fitness: {best['fitness']:.4f}")
            print(f"📊 Fitness médio: {avg_fitness:.4f}")
            
            # Treinar rede neural periodicamente
            if len(self.training_data) >= Config.MIN_SAMPLES_FOR_TRAINING:
                if self.generation % 3 == 0:
                    self._train_neural_network()
    
    def _select_template(self, features: List[float]) -> Optional[str]:
        """Seleciona template usando rede neural ou fallback"""
        
        # Tentar rede neural primeiro
        if self.neural_net.trained:
            template, confidence = self.neural_net.predict(features)
            if template and confidence > 0.3:
                return template
        
        # Buscar casos similares
        similar = self.vector_db.get_similar_successes(features)
        if similar:
            return similar[0]['template']
        
        # Fallback: template aleatório
        return random.choice(self.neural_net.templates)
    
    def _train_neural_network(self):
        """Treina a rede neural com dados acumulados"""
        
        # Preparar dados
        X = [data[0] for data in self.training_data]
        y = [data[1] for data in self.training_data]
        
        # Treinar
        self.neural_net.train(X, y)
        
        # Limpar dados antigos (manter só os mais recentes)
        self.training_data = self.training_data[-100:]
    
    def report(self):
        """Gera relatório final"""
        
        print("\n" + "="*70)
        print("📊 RELATÓRIO FINAL")
        print("="*70)
        
        # Melhor versão
        if self.population:
            best = self.population[0]
            print(f"\n🏆 Melhor versão: {best['id']}")
            print(f"   Fitness: {best['fitness']:.4f}")
            print(f"   Template: {best.get('template', 'N/A')}")
            print(f"   Geração: {best['generation']}")
            
            if 'time' in best['metrics']:
                print(f"   Tempo: {best['metrics']['time']:.4f}s")
        
        # Estatísticas da rede neural
        if self.neural_net.trained:
            print(f"\n🧠 Rede Neural:")
            print(f"   Acurácia: {self.neural_net.accuracy:.2%}")
            print(f"   Templates: {len(self.neural_net.templates)}")
            print(f"   Exemplos de treino: {len(self.training_data)}")
        
        # Templates mais usados
        template_counts = defaultdict(int)
        for v in self.population:
            if 'template' in v:
                template_counts[v['template']] += 1
        
        if template_counts:
            print(f"\n📈 Templates utilizados:")
            for template, count in sorted(template_counts.items(), 
                                        key=lambda x: x[1], reverse=True):
                print(f"   • {template}: {count}x")
    
    def close(self):
        self.vector_db.close()

# =========================
# CÓDIGO DE EXEMPLO
# =========================
SAMPLE_CODE = '''
def fibonacci(n):
    """Calcula fibonacci recursivamente"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def process_numbers(numbers):
    """Processa números ineficientemente"""
    result = []
    for i in range(len(numbers)):
        result.append(numbers[i] * 2)
    return result

def find_duplicates(items):
    """Encontra duplicatas ineficientemente"""
    duplicates = []
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates

def main():
    # Teste
    fib = fibonacci(10)
    nums = process_numbers(list(range(100)))
    dups = find_duplicates([1,2,3,2,4,5,3,6,7,8,1])
    
    print(f"Fibonacci(10) = {fib}")
    print(f"Processados: {len(nums)} números")
    print(f"Duplicatas: {dups}")

if __name__ == "__main__":
    main()
'''

# =========================
# MAIN
# =========================
def main():
    """Função principal"""
    
    # Criar sistema
    system = NeuralEvolutionSystem()
    
    try:
        # Inicializar
        system.initialize(SAMPLE_CODE)
        
        # Evoluir
        system.evolve(iterations=Config.MAX_ITERATIONS)
        
        # Relatório
        system.report()
        
    except KeyboardInterrupt:
        print("\n👋 Interrompido")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        system.close()
        print("\n✨ Sistema finalizado")

if __name__ == "__main__":
    main()
