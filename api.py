#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATENA NEURAL - API REST
Conecta o backend Python ao frontend no GitHub Pages
"""

import ast
import time
import json
import uuid
import random
import hashlib
import sqlite3
import subprocess
import sys
import tempfile
import re
import pickle
import warnings
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import numpy as np

warnings.filterwarnings('ignore')

# ========================= FASTAPI =========================
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# ========================= ML =========================
try:
    from sklearn.neural_network import MLPClassifier
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# =========================
# CONFIGURAÇÕES
# =========================
BASE_DIR = Path.home() / ".atena_neural"
BASE_DIR.mkdir(exist_ok=True)

for d in ["models", "code", "logs", "vectors"]:
    (BASE_DIR / d).mkdir(exist_ok=True)

DB_PATH    = BASE_DIR / "neural_memory.db"
MODELS_DIR = BASE_DIR / "models"

INPUT_FEATURES   = 50
HIDDEN_LAYERS    = (100, 50, 25)
MAX_ITER         = 500
LEARNING_RATE    = 0.001
MAX_ITERATIONS   = 10
TIMEOUT_SECONDS  = 3
POPULATION_SIZE  = 20
MIN_SAMPLES      = 10

# =========================
# BANCO DE DADOS VETORIAL
# =========================
class VectorDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self._init_db()

    def _init_db(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS feature_vectors (
            id TEXT PRIMARY KEY, code_hash TEXT UNIQUE,
            features TEXT, template_used TEXT,
            improvement REAL, success BOOLEAN, created_at TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS versions (
            id TEXT PRIMARY KEY, code_hash TEXT, fitness REAL,
            parent_id TEXT, generation INTEGER, template TEXT, features TEXT)''')
        c.execute('CREATE INDEX IF NOT EXISTS idx_code_hash ON feature_vectors(code_hash)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_success ON feature_vectors(success)')
        self.conn.commit()

    def add_vector(self, code: str, template: str, improvement: float, success: bool):
        code_hash = hashlib.md5(code.encode()).hexdigest()
        features  = FeatureExtractor.extract(code)
        c = self.conn.cursor()
        c.execute('''INSERT OR REPLACE INTO feature_vectors
            (id, code_hash, features, template_used, improvement, success, created_at)
            VALUES (?,?,?,?,?,?,?)''',
            (str(uuid.uuid4()), code_hash, json.dumps(features),
             template, improvement, success, datetime.now().isoformat()))
        self.conn.commit()
        return features

    def get_training_data(self):
        c = self.conn.cursor()
        c.execute('''SELECT features, template_used, improvement FROM feature_vectors
            WHERE success = 1 ORDER BY created_at DESC LIMIT 1000''')
        X, y = [], []
        for row in c.fetchall():
            if row[2] > 0.01:
                X.append(json.loads(row[0]))
                y.append(row[1])
        return X, y

    def get_similar_successes(self, features, threshold=0.7):
        c = self.conn.cursor()
        c.execute('SELECT features, template_used, improvement FROM feature_vectors WHERE success = 1')
        results = []
        fa = np.array(features)
        for row in c.fetchall():
            db_f  = np.array(json.loads(row[0]))
            n1, n2 = np.linalg.norm(fa), np.linalg.norm(db_f)
            if n1 > 0 and n2 > 0:
                sim = np.dot(fa, db_f) / (n1 * n2)
                if sim > threshold:
                    results.append({'template': row[1], 'improvement': row[2], 'similarity': float(sim)})
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:5]

    def get_stats(self):
        c = self.conn.cursor()
        c.execute('SELECT COUNT(*) FROM feature_vectors')
        total = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM feature_vectors WHERE success = 1')
        success = c.fetchone()[0]
        return {'total': total, 'success': success,
                'rate': round(success / total * 100, 1) if total > 0 else 0}

    def close(self):
        self.conn.close()

# =========================
# EXTRATOR DE CARACTERÍSTICAS
# =========================
class FeatureExtractor:
    @staticmethod
    def extract(code: str) -> List[float]:
        features = []
        lines = code.split('\n')
        features.append(min(len(lines) / 100, 1.0))
        features.append(min(len(code) / 5000, 1.0))
        features.append(len(re.findall(r'if |elif |else:', code)) / 20)
        features.append(len(re.findall(r'for |while ', code)) / 10)
        features.append(len(re.findall(r'try:|except:|finally:', code)) / 5)
        features.append(len(re.findall(r'def ', code)) / 10)
        features.append(len(re.findall(r'class ', code)) / 5)
        features.append(len(re.findall(r'lambda', code)) / 5)
        features.append(len(re.findall(r'\[\]|\{\}|\(\)', code)) / 20)
        features.append(len(re.findall(r'\.append\(|\.extend\(', code)) / 10)
        features.append(len(re.findall(r'\.join\(', code)) / 5)
        imports = len(re.findall(r'^import |^from ', code, re.MULTILINE))
        features.append(min(imports / 10, 1.0))
        comments = len(re.findall(r'#.*$', code, re.MULTILINE))
        features.append(min(comments / 20, 1.0))
        docstrings = len(re.findall(r'""".*?"""', code, re.DOTALL))
        features.append(min(docstrings / 5, 1.0))
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
        for pattern in [r'numpy|np\.', r'@lru_cache', r'yield',
                        r'\[\s*\w+\s+for', r'\.join\(.*\)', r'__slots__',
                        r'with open', r'multiprocessing', r'asyncio', r'f"']:
            features.append(1.0 if re.search(pattern, code) else 0.0)
        while len(features) < INPUT_FEATURES:
            features.append(0.0)
        return features[:INPUT_FEATURES]

# =========================
# REDE NEURAL
# =========================
class NeuralOptimizer:
    TEMPLATES = [
        'list_comprehension', 'string_join', 'use_set_for_membership',
        'cache_results', 'use_generators', 'remove_dead_code',
        'use_local_vars', 'vectorize_loop'
    ]

    def __init__(self):
        self.model         = None
        self.scaler        = StandardScaler() if HAS_SKLEARN else None
        self.label_encoder = LabelEncoder()   if HAS_SKLEARN else None
        self.accuracy      = 0.0
        self.trained       = False
        self._load_model()

    def train(self, X, y):
        if not HAS_SKLEARN or len(X) < MIN_SAMPLES:
            return False
        X = np.array(X)
        X_scaled  = self.scaler.fit_transform(X)
        y_encoded = self.label_encoder.fit_transform(y)
        if len(set(y_encoded)) < 2:
            return False
        X_tr, X_val, y_tr, y_val = train_test_split(
            X_scaled, y_encoded, test_size=0.2, random_state=42)
        self.model = MLPClassifier(
            hidden_layer_sizes=HIDDEN_LAYERS, activation='relu',
            solver='adam', alpha=0.001, learning_rate='adaptive',
            learning_rate_init=LEARNING_RATE, max_iter=MAX_ITER,
            random_state=42, early_stopping=True, verbose=False)
        self.model.fit(X_tr, y_tr)
        self.accuracy = accuracy_score(y_val, self.model.predict(X_val))
        self.trained  = True
        self._save_model()
        return True

    def predict(self, features):
        if not self.trained or self.model is None:
            return None, 0.0
        f = np.array(features).reshape(1, -1)
        f_scaled = self.scaler.transform(f)
        probs    = self.model.predict_proba(f_scaled)[0]
        idx      = np.argmax(probs)
        conf     = probs[idx]
        if conf > 0.3:
            return self.label_encoder.inverse_transform([idx])[0], float(conf)
        return None, float(conf)

    def get_all_probabilities(self, features):
        if not self.trained or self.model is None:
            return {}
        f = np.array(features).reshape(1, -1)
        f_scaled = self.scaler.transform(f)
        probs    = self.model.predict_proba(f_scaled)[0]
        return {t: float(p) for t, p in zip(self.label_encoder.classes_, probs)}

    def _save_model(self):
        path = MODELS_DIR / "neural_optimizer.pkl"
        with open(path, 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler,
                         'label_encoder': self.label_encoder, 'accuracy': self.accuracy}, f)

    def _load_model(self):
        path = MODELS_DIR / "neural_optimizer.pkl"
        if path.exists():
            try:
                with open(path, 'rb') as f:
                    d = pickle.load(f)
                self.model, self.scaler = d['model'], d['scaler']
                self.label_encoder     = d['label_encoder']
                self.accuracy          = d['accuracy']
                self.trained           = True
            except Exception:
                pass

# =========================
# TEMPLATES DE OTIMIZAÇÃO
# =========================
class OptimizerTemplates:
    @staticmethod
    def apply(code: str, template: str) -> str:
        if template == 'list_comprehension':
            pattern = r'(\w+)\s*=\s*\[\]\s*\n\s+for\s+(\w+)\s+in\s+(\w+):\s*\n\s+\1\.append\(([^)]+)\)'
            return re.sub(pattern, lambda m: f"{m.group(1)} = [{m.group(4)} for {m.group(2)} in {m.group(3)}]",
                          code, flags=re.MULTILINE)
        if template == 'cache_results':
            if 'from functools import lru_cache' not in code:
                code = 'from functools import lru_cache\n' + code
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('def '):
                    fname = line.split('def ')[1].split('(')[0]
                    for j in range(i+1, min(i+20, len(lines))):
                        if f'{fname}(' in lines[j] and 'return' in lines[j]:
                            if i > 0 and not lines[i-1].strip().startswith('@'):
                                lines.insert(i, '@lru_cache(maxsize=128)')
                            break
            return '\n'.join(lines)
        if template == 'use_generators':
            return re.sub(
                r'\[\s*(\w+)\s+for\s+(\w+)\s+in\s+range\(\s*(\d{4,})\s*\)\s*\]',
                lambda m: f"({m.group(1)} for {m.group(2)} in range({m.group(3)}))", code)
        if template == 'vectorize_loop':
            if 'import numpy' not in code and 'for i in range' in code:
                code = 'import numpy as np\n' + code
                code += '\n# TODO: considere vetorizar loops com numpy\n'
        return code

# =========================
# EXECUTOR DE CÓDIGO
# =========================
class CodeExecutor:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()

    def execute(self, code: str) -> Dict[str, Any]:
        result = {'success': False, 'time': float('inf'), 'memory': 0, 'output': '', 'error': ''}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', dir=self.temp_dir, delete=False) as f:
            f.write(code)
            tmp = f.name
        try:
            start = time.perf_counter()
            proc  = subprocess.run([sys.executable, tmp],
                capture_output=True, text=True, timeout=TIMEOUT_SECONDS)
            result['time']    = time.perf_counter() - start
            result['output']  = proc.stdout
            result['success'] = proc.returncode == 0
            result['error']   = proc.stderr
            if HAS_PSUTIL:
                result['memory'] = psutil.Process().memory_info().rss / 1024 / 1024
        except subprocess.TimeoutExpired:
            result['error'] = 'Timeout'
        except Exception as e:
            result['error'] = str(e)
        finally:
            try: Path(tmp).unlink()
            except: pass
        return result

# =========================
# SISTEMA PRINCIPAL
# =========================
class AtenaSystem:
    def __init__(self):
        self.vector_db   = VectorDatabase()
        self.neural_net  = NeuralOptimizer()
        self.executor    = CodeExecutor()
        self.population  = []
        self.generation  = 0
        self.training_data = []
        self.event_log   = []

    def _log(self, msg: str):
        self.event_log.append({'msg': msg, 'ts': datetime.now().isoformat()})
        if len(self.event_log) > 100:
            self.event_log.pop(0)

    def load_code(self, code: str):
        result   = self.executor.execute(code)
        features = FeatureExtractor.extract(code)
        t_score  = 1.0 / (result.get('time', 1) + 0.1)
        m_score  = 1.0 / (result.get('memory', 1) + 1)
        fitness  = t_score * 0.6 + m_score * 0.4
        vid      = hashlib.md5(code.encode()).hexdigest()[:8]
        self.population = [{'id': vid, 'code': code, 'fitness': fitness,
                             'metrics': result, 'generation': 0}]
        self._log(f"Código carregado — fitness inicial: {fitness:.4f}")
        return fitness, result

    def evolve_once(self):
        if not self.population:
            return None
        self.generation += 1
        current  = max(self.population, key=lambda x: x['fitness'])
        features = FeatureExtractor.extract(current['code'])
        template = self._select_template(features)
        mutated  = OptimizerTemplates.apply(current['code'], template)
        if mutated == current['code']:
            self._log(f"Template {template} não alterou o código")
            return {'improved': False, 'template': template, 'generation': self.generation}
        result   = self.executor.execute(mutated)
        if not result['success']:
            self._log(f"Mutação {template} gerou erro de execução")
            return {'improved': False, 'template': template, 'generation': self.generation}
        t_score  = 1.0 / (result.get('time', 1) + 0.1)
        m_score  = 1.0 / (result.get('memory', 1) + 1)
        new_fit  = t_score * 0.6 + m_score * 0.4
        improvement = new_fit - current['fitness']
        self.vector_db.add_vector(mutated, template, improvement, success=improvement > 0)
        vid = hashlib.md5(mutated.encode()).hexdigest()[:8]
        self.population.append({'id': vid, 'code': mutated, 'fitness': new_fit,
                                 'metrics': result, 'template': template,
                                 'generation': self.generation, 'improvement': improvement})
        self.population.sort(key=lambda x: x['fitness'], reverse=True)
        self.population = self.population[:POPULATION_SIZE]
        if improvement > 0:
            self.training_data.append((features, template, improvement))
            self._log(f"✅ Mutação bem-sucedida: {template} (+{improvement:.4f})")
        else:
            self._log(f"❌ Sem melhoria: {template} ({improvement:.4f})")
        if len(self.training_data) >= MIN_SAMPLES and self.generation % 3 == 0:
            self.neural_net.train(
                [d[0] for d in self.training_data],
                [d[1] for d in self.training_data])
        return {
            'improved': improvement > 0,
            'template': template,
            'generation': self.generation,
            'old_fitness': round(current['fitness'], 4),
            'new_fitness': round(new_fit, 4),
            'improvement': round(improvement, 4),
            'time': round(result.get('time', 0), 4)
        }

    def _select_template(self, features):
        if self.neural_net.trained:
            t, conf = self.neural_net.predict(features)
            if t and conf > 0.3:
                return t
        similar = self.vector_db.get_similar_successes(features)
        if similar:
            return similar[0]['template']
        return random.choice(NeuralOptimizer.TEMPLATES)

    def get_metrics(self):
        best    = self.population[0] if self.population else {}
        db_stats = self.vector_db.get_stats()
        return {
            'generation':    self.generation,
            'population':    len(self.population),
            'best_fitness':  round(best.get('fitness', 0), 4),
            'avg_fitness':   round(sum(v['fitness'] for v in self.population) / max(len(self.population),1), 4),
            'diversity':     round(len(set(v.get('template','') for v in self.population)) / max(len(NeuralOptimizer.TEMPLATES),1), 2),
            'neural_trained': self.neural_net.trained,
            'neural_accuracy': round(self.neural_net.accuracy * 100, 1),
            'total_vectors': db_stats['total'],
            'success_rate':  db_stats['rate'],
            'training_samples': len(self.training_data),
            'recent_events': self.event_log[-10:]
        }

    def process_chat(self, message: str) -> str:
        msg = message.lower()
        if any(w in msg for w in ['métricas', 'metrica', 'status', 'stats']):
            m = self.get_metrics()
            return (f"📊 Status atual:\n"
                    f"• Geração: {m['generation']}\n"
                    f"• Fitness: {m['best_fitness']}\n"
                    f"• Taxa de sucesso: {m['success_rate']}%\n"
                    f"• Rede neural: {'treinada ✅' if m['neural_trained'] else 'aguardando dados'}\n"
                    f"• Vetores no banco: {m['total_vectors']}")
        if any(w in msg for w in ['evoluir', 'evolui', 'mutação', 'mutacao', 'evol']):
            result = self.evolve_once()
            if not result:
                return "⚠️ Nenhum código carregado. Envie um código primeiro."
            if result['improved']:
                return (f"✅ Evolução bem-sucedida!\n"
                        f"• Template: {result['template']}\n"
                        f"• Fitness: {result['old_fitness']} → {result['new_fitness']}\n"
                        f"• Melhoria: +{result['improvement']}\n"
                        f"• Geração: {result['generation']}")
            return f"❌ Template {result['template']} não melhorou o código desta vez. Tente novamente."
        if any(w in msg for w in ['analisar', 'analise', 'análise', 'código', 'codigo']):
            if not self.population:
                return "⚠️ Nenhum código carregado ainda."
            best     = self.population[0]
            features = FeatureExtractor.extract(best['code'])
            template, conf = self.neural_net.predict(features)
            probs    = self.neural_net.get_all_probabilities(features)
            top      = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:3] if probs else []
            resp = (f"🔍 Análise do código atual:\n"
                    f"• Fitness: {best['fitness']:.4f}\n"
                    f"• Geração: {best['generation']}\n"
                    f"• Template usado: {best.get('template', 'original')}\n")
            if template:
                resp += f"• Recomendação da rede neural: {template} (conf: {conf:.0%})\n"
            if top:
                resp += "• Top templates:\n"
                for t, p in top:
                    resp += f"  - {t}: {p:.0%}\n"
            return resp
        if any(w in msg for w in ['ajuda', 'help', 'comandos', 'o que']):
            return ("🧬 Comandos disponíveis:\n"
                    "• 'métricas' — ver status do sistema\n"
                    "• 'evoluir' — rodar um ciclo de mutação\n"
                    "• 'analisar' — inspecionar o código atual\n"
                    "• 'ajuda' — mostrar este menu\n\n"
                    "Você também pode enviar código Python diretamente para eu otimizar.")
        if len(message) > 50 and ('def ' in message or 'class ' in message or 'import ' in message):
            fitness, result = self.load_code(message)
            if result['success']:
                return (f"✅ Código carregado com sucesso!\n"
                        f"• Fitness inicial: {fitness:.4f}\n"
                        f"• Tempo de execução: {result['time']:.4f}s\n"
                        f"• Digite 'evoluir' para iniciar a otimização.")
            return f"⚠️ Código carregado, mas com erro de execução:\n{result['error'][:200]}"
        return ("🤖 Olá! Sou a ATENA Neural — sistema de otimização de código com deep learning.\n"
                "Digite 'ajuda' para ver os comandos disponíveis, ou envie um código Python para eu analisar.")


# =========================
# INSTÂNCIA GLOBAL
# =========================
atena = AtenaSystem()

# =========================
# APP FASTAPI
# =========================
app = FastAPI(title="ATENA Neural API", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://minhokagomes-debug.github.io",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:5500",  # Live Server VS Code
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# SCHEMAS
# =========================
class ChatRequest(BaseModel):
    message: str

class CodeRequest(BaseModel):
    code: str

# =========================
# ROTAS
# =========================

@app.get("/")
def root():
    return {"status": "online", "system": "ATENA Neural API v3.0",
            "docs": "/docs"}

@app.get("/metrics")
def get_metrics():
    """Métricas reais do sistema — substitui Math.random() do frontend"""
    return atena.get_metrics()

@app.post("/chat")
def chat(req: ChatRequest):
    """Chat com a ATENA — substitui as respostas hardcoded do frontend"""
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Mensagem vazia")
    response = atena.process_chat(req.message.strip())
    return {"response": response, "timestamp": datetime.now().isoformat()}

@app.post("/evolve")
def evolve():
    """Executa um ciclo de evolução real"""
    result = atena.evolve_once()
    if result is None:
        raise HTTPException(status_code=400, detail="Nenhum código carregado")
    return result

@app.post("/load")
def load_code(req: CodeRequest):
    """Carrega código Python para otimização"""
    if not req.code or not req.code.strip():
        raise HTTPException(status_code=400, detail="Código vazio")
    fitness, result = atena.load_code(req.code.strip())
    return {
        "fitness": round(fitness, 4),
        "success": result['success'],
        "time":    round(result.get('time', 0), 4),
        "error":   result.get('error', '')
    }

@app.get("/events")
def get_events():
    """Log de eventos recentes do sistema"""
    return {"events": atena.event_log[-20:]}

@app.get("/population")
def get_population():
    """Versões da população atual (sem o código completo)"""
    return {
        "population": [
            {"id": v['id'], "fitness": round(v['fitness'], 4),
             "generation": v['generation'], "template": v.get('template', 'original')}
            for v in atena.population
        ]
    }

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=10000, reload=False)
