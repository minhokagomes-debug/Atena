#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ ATENA NEURAL - SISTEMA COM REDES NEURAIS REAIS
Versão 2.0 - Cloud Edition (100% Real Execution)
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
import sys
import re
import pickle
import warnings
import threading
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass
import numpy as np

# Integração Web para o Render
try:
    from fastapi import FastAPI
    app = FastAPI()
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

warnings.filterwarnings('ignore')

# =========================
# BIBLIOTECAS DE ML
# =========================
try:
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

# =========================
# CONFIGURAÇÕES
# =========================
BASE_DIR = Path("./atena_data")
BASE_DIR.mkdir(exist_ok=True)

@dataclass
class Config:
    DB_PATH = BASE_DIR / "neural_memory.db"
    MODELS_DIR = BASE_DIR / "models"
    
    INPUT_FEATURES = 50
    HIDDEN_LAYERS = (100, 50, 25)
    MAX_ITER = 500
    LEARNING_RATE = 0.001
    
    MAX_ITERATIONS = 20 
    TIMEOUT_SECONDS = 3
    POPULATION_SIZE = 15
    MIN_SAMPLES_FOR_TRAINING = 10
    
    for dir_path in [MODELS_DIR]:
        dir_path.mkdir(exist_ok=True)

# =========================
# MEMÓRIA VETORIAL (SQLite)
# =========================
class VectorDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(str(Config.DB_PATH), check_same_thread=True)
        self._init_db()
    
    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS feature_vectors 
            (id TEXT PRIMARY KEY, code_hash TEXT, features TEXT, template_used TEXT, 
             improvement REAL, success BOOLEAN, created_at TIMESTAMP)''')
        self.conn.commit()

    def add_vector(self, code: str, template: str, improvement: float, success: bool):
        code_hash = hashlib.md5(code.encode()).hexdigest()
        features = FeatureExtractor.extract(code)
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO feature_vectors VALUES (?, ?, ?, ?, ?, ?, ?)', 
                      (str(uuid.uuid4()), code_hash, json.dumps(features), template, 
                       improvement, success, datetime.now().isoformat()))
        self.conn.commit()
        return features

    def get_training_data(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT features, template_used FROM feature_vectors WHERE success = 1')
        X, y = [], []
        for row in cursor.fetchall():
            X.append(json.loads(row[0]))
            y.append(row[1])
        return X, y

class FeatureExtractor:
    @staticmethod
    def extract(code: str) -> List[float]:
        features = []
        lines = code.split('\n')
        features.append(min(len(lines) / 100, 1.0))
        features.append(min(len(code) / 5000, 1.0))
        features.append(len(re.findall(r'if |for |while ', code)) / 20)
        features.append(len(re.findall(r'def |class ', code)) / 10)
        while len(features) < Config.INPUT_FEATURES: features.append(0.0)
        return features[:Config.INPUT_FEATURES]

# =========================
# EXECUTOR REAL
# =========================
class CodeExecutor:
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "atena_exec"
        self.temp_dir.mkdir(exist_ok=True)

    def execute(self, code: str) -> Dict[str, Any]:
        result = {'success': False, 'time': 999.0, 'error': ''}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', dir=self.temp_dir, delete=False) as f:
            f.write(code)
            temp_file = f.name
        try:
            start = time.perf_counter()
            # Executa o código mutado no processador real
            proc = subprocess.run([sys.executable, temp_file], capture_output=True, text=True, timeout=Config.TIMEOUT_SECONDS)
            end = time.perf_counter()
            result.update({'success': proc.returncode == 0, 'time': end - start, 'error': proc.stderr})
        except Exception as e:
            result['error'] = str(e)
        finally:
            if Path(temp_file).exists(): Path(temp_file).unlink()
        return result

# =========================
# NÚCLEO NEURAL
# =========================
class NeuralOptimizer:
    def __init__(self):
        self.model = MLPClassifier(hidden_layer_sizes=Config.HIDDEN_LAYERS, max_iter=Config.MAX_ITER)
        self.scaler = StandardScaler()
        self.encoder = LabelEncoder()
        self.trained = False
        self.templates = ['list_comprehension', 'cache_results']

    def train(self, X, y):
        if len(X) < Config.MIN_SAMPLES_FOR_TRAINING: return
        try:
            X_scaled = self.scaler.fit_transform(X)
            y_encoded = self.encoder.fit_transform(y)
            self.model.fit(X_scaled, y_encoded)
            self.trained = True
        except: pass

    def predict(self, features):
        if not self.trained: return random.choice(self.templates)
        X = self.scaler.transform([features])
        return self.encoder.inverse_transform(self.model.predict(X))[0]

class OptimizerTemplates:
    @staticmethod
    def apply(code: str, template: str) -> str:
        if template == 'list_comprehension':
            return re.sub(r'(\w+)\s*=\s*\[\]\s*\n\s+for\s+(\w+)\s+in\s+(\w+):\s*\n\s+\1\.append\(([^)]+)\)', 
                          r'\1 = [\4 for \2 in \3]', code)
        if template == 'cache_results' and 'lru_cache' not in code:
            return "from functools import lru_cache\n@lru_cache(None)\n" + code
        return code

# =========================
# SISTEMA DE EVOLUÇÃO
# =========================
class NeuralEvolutionSystem:
    def __init__(self):
        self.db = VectorDatabase()
        self.nn = NeuralOptimizer()
        self.executor = CodeExecutor()
        self.population = []
        self.generation = 0

    def initialize(self, code: str):
        res = self.executor.execute(code)
        fit = 1.0 / (res['time'] + 0.001)
        self.population.append({'code': code, 'fitness': fit, 'gen': 0})

    def evolve_cycle(self):
        if not self.population: return
        self.generation += 1
        best_so_far = max(self.population, key=lambda x: x['fitness'])
        
        features = FeatureExtractor.extract(best_so_far['code'])
        template = self.nn.predict(features)
        
        mutated_code = OptimizerTemplates.apply(best_so_far['code'], template)
        res = self.executor.execute(mutated_code)
        
        new_fitness = 1.0 / (res['time'] + 0.001) if res['success'] else 0.0
        improvement = new_fitness - best_so_far['fitness']
        
        self.db.add_vector(mutated_code, template, improvement, success=(improvement > 0))
        
        if res['success']:
            self.population.append({'code': mutated_code, 'fitness': new_fitness, 'gen': self.generation})
        
        self.population.sort(key=lambda x: x['fitness'], reverse=True)
        self.population = self.population[:Config.POPULATION_SIZE]

        if self.generation % 5 == 0:
            X, y = self.db.get_training_data()
            if X: self.nn.train(X, y)

# =========================
# EXECUÇÃO E API
# =========================
system = NeuralEvolutionSystem()
INITIAL_CODE = "def run():\n    res = []\n    for i in range(100):\n        res.append(i * 2)\n    return res\nrun()"

def background_evolution():
    system.initialize(INITIAL_CODE)
    while True:
        system.evolve_cycle()
        time.sleep(45) # Intervalo seguro para o Render Free

if HAS_FASTAPI:
    @app.get("/")
    def status():
        best = system.population[0] if system.population else {}
        return {
            "atena_status": "ONLINE",
            "generation": system.generation,
            "best_fitness": round(best.get('fitness', 0), 4),
            "evolution_active": True
        }
    
    threading.Thread(target=background_evolution, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
