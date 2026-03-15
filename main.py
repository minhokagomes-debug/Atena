#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ATENA NEURAL - AUTO-EVOLUÇÃO PERFEITA
Versão definitiva com mutações reais, testes automáticos, aprendizado semântico,
preditor inteligente, meta-evolução e deploy seguro.
"""

import os
import sys
import time
import json
import sqlite3
import ast
import astor
import random
import subprocess
import tempfile
import shutil
import hashlib
import threading
import queue
import concurrent.futures
import requests
import numpy as np
import pickle
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set, Callable
from dataclasses import dataclass, field
from collections import Counter
import inspect
import textwrap

# Análise de código
import radon.complexity as radon_cc
import radon.raw as radon_raw

# Embeddings
try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE = True
except ImportError:
    HAS_SENTENCE = False
    print("[⚠️] sentence-transformers não instalado. Usando fallback TF-IDF.")

# Docker
try:
    import docker
    HAS_DOCKER_PY = True
except ImportError:
    HAS_DOCKER_PY = False

# Hypothesis para testes
try:
    import hypothesis
    from hypothesis import given, strategies as st, settings, Verbosity
    from hypothesis.errors import UnsatisfiedAssumption
    HAS_HYPOTHESIS = True
except ImportError:
    HAS_HYPOTHESIS = False
    print("[⚠️] hypothesis não instalado. Testes serão simplificados.")

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

@dataclass
class Config:
    # APIs
    XAI_API_KEY: str = os.getenv("XAI_API_KEY", "")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    
    # Diretórios
    BASE_DIR: Path = Path("./atena_evolution")
    CODE_DIR: Path = BASE_DIR / "code"
    BACKUP_DIR: Path = BASE_DIR / "backups"
    KNOWLEDGE_DIR: Path = BASE_DIR / "knowledge"
    EVOLUTIONS_DIR: Path = BASE_DIR / "evolutions"
    SANDBOX_DIR: Path = BASE_DIR / "sandbox"
    MODEL_DIR: Path = BASE_DIR / "models"
    DEPLOY_DIR: Path = BASE_DIR / "deploy"
    
    # Arquivos
    CURRENT_CODE_FILE: Path = CODE_DIR / "atena_current.py"
    NEW_CODE_FILE: Path = CODE_DIR / "atena_new.py"
    ENGINE_FILE: Path = CODE_DIR / "atena_engine.py"
    KNOWLEDGE_DB: Path = KNOWLEDGE_DIR / "knowledge.db"
    PREDICTOR_MODEL: Path = MODEL_DIR / "mutation_predictor.pkl"
    META_MODEL: Path = MODEL_DIR / "meta_predictor.pkl"
    
    # Parâmetros de evolução
    MAX_MUTATION_ATTEMPTS: int = 5
    EVALUATION_TIMEOUT: int = 10
    BACKUP_KEEP_DAYS: int = 7
    PARALLEL_WORKERS: int = 4
    EXPLORATION_RATE: float = 0.2      # chance de ignorar o preditor e escolher aleatório
    MUTATION_STRENGTH: float = 0.7     # probabilidade de mutações mais agressivas
    
    # GitHub
    GITHUB_MAX_REPOS_PER_QUERY: int = 50
    GITHUB_MAX_FILES_PER_REPO: int = 10
    GITHUB_LEARNING_INTERVAL: int = 3600  # 1 hora
    GITHUB_MAX_FUNCTIONS: int = 10000     # limite no banco
    
    # Treinamento
    TRAINING_INTERVAL: int = 3600
    MIN_TRAINING_SAMPLES: int = 100
    
    # Testes
    HYPOTHESIS_EXAMPLES: int = 50         # número de exemplos por função
    
    # Deploy
    DEPLOY_GIT_REPO: str = os.getenv("DEPLOY_GIT_REPO", "")
    DEPLOY_BRANCH: str = "main"
    DEPLOY_DOCKER_IMAGE: str = os.getenv("DEPLOY_DOCKER_IMAGE", "")
    DEPLOY_COMMAND: str = os.getenv("DEPLOY_COMMAND", "")
    DEPLOY_THRESHOLD: float = 1.05        # 5% de melhoria para acionar deploy
    
    # Modelo de embedding
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    @classmethod
    def setup(cls):
        for d in [cls.BASE_DIR, cls.CODE_DIR, cls.BACKUP_DIR, cls.KNOWLEDGE_DIR,
                  cls.EVOLUTIONS_DIR, cls.SANDBOX_DIR, cls.MODEL_DIR, cls.DEPLOY_DIR]:
            d.mkdir(exist_ok=True)
        if not cls.CURRENT_CODE_FILE.exists():
            cls._create_initial_code()
        if not cls.ENGINE_FILE.exists():
            shutil.copy(__file__, cls.ENGINE_FILE)

    @classmethod
    def _create_initial_code(cls):
        code = '''#!/usr/bin/env python3
\"\"\"
ATENA - Código evoluído automaticamente
\"\"\"

def main():
    print("Olá, eu sou a Atena!")
    return 0

def util_soma(a, b):
    return a + b

if __name__ == "__main__":
    main()
'''
        cls.CURRENT_CODE_FILE.write_text(code)


# ============================================================================
# BANCO DE CONHECIMENTO SEMÂNTICO
# ============================================================================

class KnowledgeBase:
    def __init__(self):
        self.conn = sqlite3.connect(str(Config.KNOWLEDGE_DB))
        self._init_tables()
        self.embedding_model = None
        if HAS_SENTENCE:
            try:
                self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
            except Exception as e:
                print(f"[⚠️] Erro ao carregar modelo de embedding: {e}")
        self.function_cache = []  # (code, embedding, purpose)
        self._load_cache()

    def _init_tables(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS learned_functions
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             source TEXT,
             function_name TEXT,
             code TEXT,
             hash TEXT UNIQUE,
             complexity REAL,
             lines INTEGER,
             first_seen TEXT,
             last_used TEXT,
             usage_count INTEGER DEFAULT 0,
             embedding BLOB,
             purpose TEXT)''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS github_repos
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             repo_full_name TEXT UNIQUE,
             stars INTEGER,
             last_processed TEXT,
             files_processed INTEGER)''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS objectives
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT UNIQUE,
             description TEXT,
             weight REAL DEFAULT 1.0,
             current_value REAL,
             target_value REAL,
             active BOOLEAN DEFAULT 1,
             created TEXT,
             last_updated TEXT)''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS evolution_metrics
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             timestamp TEXT,
             generation INTEGER,
             mutation TEXT,
             old_score REAL,
             new_score REAL,
             replaced BOOLEAN,
             features TEXT,
             test_results TEXT)''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS backups
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             timestamp TEXT,
             file_path TEXT,
             hash TEXT,
             score REAL)''')

        self.conn.commit()
        self._init_default_objectives()

    def _init_default_objectives(self):
        default = [
            ("reduzir_complexidade", "Reduzir complexidade ciclomática média", 1.0, 10.0, 5.0),
            ("aumentar_modularidade", "Aumentar número de funções", 0.8, 2.0, 10.0),
            ("melhorar_documentacao", "Aumentar proporção de comentários", 0.5, 0.0, 0.2),
            ("reduzir_tempo_execucao", "Reduzir tempo de execução da main", 1.0, 1.0, 0.1),
            ("aprender_algoritmos", "Introduzir algoritmos eficientes", 0.7, 0.0, 5.0),
            ("aumentar_cobertura_testes", "Aumentar cobertura de testes", 0.6, 0.0, 0.8),
        ]
        now = datetime.now().isoformat()
        for name, desc, weight, curr, target in default:
            self.conn.execute(
                """INSERT OR IGNORE INTO objectives 
                   (name, description, weight, current_value, target_value, created, last_updated) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (name, desc, weight, curr, target, now, now)
            )
        self.conn.commit()

    def _load_cache(self):
        cursor = self.conn.execute("SELECT code, embedding, purpose FROM learned_functions WHERE embedding IS NOT NULL")
        for code, emb_blob, purpose in cursor:
            if emb_blob:
                emb = pickle.loads(emb_blob)
                self.function_cache.append((code, emb, purpose))

    def add_function(self, code: str, source: str, purpose: str = "") -> bool:
        try:
            tree = ast.parse(code)
            functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            if not functions:
                return False
            func = functions[0]
            func_name = func.name
            func_code = astor.to_source(func)
            func_hash = hashlib.sha256(func_code.encode()).hexdigest()

            complexity = self._compute_complexity(func_code)
            lines = len(func_code.splitlines())

            embedding = None
            if self.embedding_model:
                docstring = ast.get_docstring(func) or ""
                text = f"{func_name} {docstring} " + " ".join([n.__class__.__name__ for n in ast.walk(func) if isinstance(n, (ast.Name, ast.Call))])
                emb = self.embedding_model.encode(text).astype(np.float32)
                embedding = pickle.dumps(emb)

            self.conn.execute(
                """INSERT OR IGNORE INTO learned_functions 
                   (source, function_name, code, hash, complexity, lines, first_seen, embedding, purpose)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (source, func_name, func_code, func_hash, complexity, lines,
                 datetime.now().isoformat(), embedding, purpose)
            )
            self.conn.commit()
            if embedding:
                self.function_cache.append((func_code, emb, purpose))
            return True
        except Exception as e:
            print(f"[⚠️] Erro ao adicionar função: {e}")
            return False

    def _compute_complexity(self, code: str) -> float:
        try:
            blocks = radon_cc.cc_visit(code)
            if blocks:
                return sum(b.complexity for b in blocks) / len(blocks)
            return 1.0
        except:
            return 1.0

    def search_similar(self, query_code: str, top_n: int = 5) -> List[Tuple[str, float, str]]:
        if not self.embedding_model or not self.function_cache:
            return []
        try:
            tree = ast.parse(query_code)
            funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            if not funcs:
                return []
            query_func = funcs[0]
            docstring = ast.get_docstring(query_func) or ""
            text = f"{query_func.name} {docstring} " + " ".join([n.__class__.__name__ for n in ast.walk(query_func) if isinstance(n, (ast.Name, ast.Call))])
            query_emb = self.embedding_model.encode(text).astype(np.float32)
        except:
            return []

        similarities = []
        for code, emb, purpose in self.function_cache:
            sim = np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb) + 1e-8)
            similarities.append((sim, code, purpose))
        similarities.sort(reverse=True)
        return [(code, sim, purpose) for sim, code, purpose in similarities[:top_n] if sim > 0.5]

    def get_function_by_purpose(self, keywords: List[str]) -> Optional[Tuple[str, str]]:
        placeholders = ','.join(['?'] * len(keywords))
        cursor = self.conn.execute(
            f"SELECT code, source FROM learned_functions WHERE purpose LIKE ? ORDER BY RANDOM() LIMIT 1",
            tuple(f'%{kw}%' for kw in keywords)
        )
        row = cursor.fetchone()
        if row:
            return row[0], row[1]
        return None

    def get_random_function(self) -> Optional[Tuple[str, str]]:
        cursor = self.conn.execute("SELECT code, source FROM learned_functions ORDER BY RANDOM() LIMIT 1")
        row = cursor.fetchone()
        if row:
            return row[0], row[1]
        return None

    def update_objective(self, name: str, value: float):
        self.conn.execute(
            "UPDATE objectives SET current_value = ?, last_updated = ? WHERE name = ?",
            (value, datetime.now().isoformat(), name)
        )
        self.conn.commit()

    def add_temporary_objective(self, name: str, description: str, target: float, weight: float = 0.5):
        now = datetime.now().isoformat()
        self.conn.execute(
            "INSERT OR IGNORE INTO objectives (name, description, weight, current_value, target_value, created, last_updated) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, description, weight, 0.0, target, now, now)
        )
        self.conn.commit()

    def get_objectives(self) -> List[Dict]:
        cursor = self.conn.execute("SELECT name, description, weight, current_value, target_value FROM objectives WHERE active=1")
        return [{"name": r[0], "description": r[1], "weight": r[2], "current": r[3], "target": r[4]} for r in cursor]

    def record_evolution(self, generation: int, mutation: str, old_score: float, new_score: float, replaced: bool, features: dict = None, test_results: dict = None):
        feat_json = json.dumps(features) if features else None
        test_json = json.dumps(test_results) if test_results else None
        self.conn.execute(
            "INSERT INTO evolution_metrics (timestamp, generation, mutation, old_score, new_score, replaced, features, test_results) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.now().isoformat(), generation, mutation, old_score, new_score, replaced, feat_json, test_json)
        )
        self.conn.commit()

    def record_backup(self, file_path: str, file_hash: str, score: float):
        self.conn.execute(
            "INSERT INTO backups (timestamp, file_path, hash, score) VALUES (?, ?, ?, ?)",
            (datetime.now().isoformat(), file_path, file_hash, score)
        )
        self.conn.commit()

    def get_training_data(self) -> Tuple[List[Dict], List[int]]:
        cursor = self.conn.execute("SELECT mutation, features, replaced FROM evolution_metrics WHERE features IS NOT NULL")
        X = []
        y = []
        for mutation, feat_json, replaced in cursor:
            feat = json.loads(feat_json)
            feat['mutation'] = mutation
            X.append(feat)
            y.append(1 if replaced else 0)
        return X, y

    def close(self):
        self.conn.close()


# ============================================================================
# SANDBOX SEGURO COM DOCKER
# ============================================================================

class Sandbox:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.use_docker = self._check_docker()

    def _check_docker(self) -> bool:
        try:
            subprocess.run(["docker", "--version"], capture_output=True, check=True)
            return True
        except:
            return False

    def run(self, code: str, input_data: str = "") -> Tuple[bool, str, float]:
        if self.use_docker:
            return self._run_docker(code, input_data)
        else:
            return self._run_subprocess(code, input_data)

    def _run_docker(self, code: str, input_data: str) -> Tuple[bool, str, float]:
        with tempfile.TemporaryDirectory(dir=Config.SANDBOX_DIR) as tmpdir:
            script_path = Path(tmpdir) / "script.py"
            script_path.write_text(code)

            cmd = [
                "docker", "run", "--rm",
                "-v", f"{tmpdir}:/app",
                "-w", "/app",
                "--memory", "256m",
                "--cpus", "0.5",
                "python:3.10-slim",
                "python", "script.py"
            ]
            try:
                start = time.time()
                proc = subprocess.run(cmd, input=input_data, capture_output=True, text=True, timeout=self.timeout)
                elapsed = time.time() - start
                success = proc.returncode == 0
                output = proc.stdout + proc.stderr
                return success, output, elapsed
            except subprocess.TimeoutExpired:
                return False, f"Timeout após {self.timeout}s", self.timeout
            except Exception as e:
                return False, str(e), 0

    def _run_subprocess(self, code: str, input_data: str) -> Tuple[bool, str, float]:
        if os.name != "nt":
            import resource
            def set_limits():
                resource.setrlimit(resource.RLIMIT_CPU, (self.timeout, self.timeout))
                resource.setrlimit(resource.RLIMIT_AS, (100 * 1024 * 1024, 100 * 1024 * 1024))
        else:
            def set_limits():
                pass

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            tmp_path = f.name

        try:
            start = time.time()
            proc = subprocess.run(
                [sys.executable, tmp_path],
                input=input_data,
                preexec_fn=set_limits if os.name != "nt" else None,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            elapsed = time.time() - start
            success = proc.returncode == 0
            output = proc.stdout + proc.stderr
            return success, output, elapsed
        except subprocess.TimeoutExpired:
            return False, f"Timeout após {self.timeout}s", self.timeout
        except Exception as e:
            return False, str(e), 0
        finally:
            os.unlink(tmp_path)


# ============================================================================
# TESTADOR AUTOMÁTICO COM HYPOTHESIS
# ============================================================================

class FunctionTester:
    def __init__(self, sandbox: Sandbox, timeout: int = 5):
        self.sandbox = sandbox
        self.timeout = timeout

    def test_function(self, func_name: str, original_code: str, mutated_code: str) -> Dict:
        """
        Testa uma função específica, comparando original e mutada com entradas aleatórias.
        Retorna {"passed": bool, "tests": int, "failing_inputs": list}
        """
        if not HAS_HYPOTHESIS:
            return self._simple_test(func_name, original_code, mutated_code)

        # Extrai a função de cada código
        orig_func = self._extract_function(original_code, func_name)
        mut_func = self._extract_function(mutated_code, func_name)
        if not orig_func or not mut_func:
            return {"passed": False, "tests": 0, "failing_inputs": []}

        # Determina os tipos dos argumentos (simplificado: assume int)
        args = [arg.arg for arg in orig_func.args.args]
        if not args:
            return {"passed": True, "tests": 1, "failing_inputs": []}  # sem argumentos, ok

        # Cria um código de teste que importa ambas e compara
        test_code = self._build_test_code(orig_func, mut_func, args)
        success, output, _ = self.sandbox.run(test_code)
        if not success:
            return {"passed": False, "tests": 0, "failing_inputs": [output[:200]]}

        # Parse output: esperamos algo como "PASSED" ou "FAILED with input (x,y)"
        lines = output.strip().split('\n')
        passed = 0
        total = 0
        failing = []
        for line in lines:
            if line.startswith("PASS:"):
                passed += 1
                total += 1
            elif line.startswith("FAIL:"):
                total += 1
                failing.append(line[5:].strip())
        return {"passed": passed == total, "tests": total, "failing_inputs": failing}

    def _extract_function(self, code: str, func_name: str) -> Optional[ast.FunctionDef]:
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == func_name:
                    return node
        except:
            pass
        return None

    def _build_test_code(self, orig_func: ast.FunctionDef, mut_func: ast.FunctionDef, args: List[str]) -> str:
        """Gera um código que testa a igualdade das duas funções com Hypothesis."""
        func_name = orig_func.name
        # Cria uma função de teste que gera entradas aleatórias
        strategy = ", ".join(["st.integers()" for _ in args])
        test_body = f"""
from hypothesis import given, strategies as st, settings, Verbosity
import sys

# Código original
{astor.to_source(orig_func)}

# Código mutado
{astor.to_source(mut_func)}

@settings(max_examples={Config.HYPOTHESIS_EXAMPLES}, deadline=None)
@given({strategy})
def test_{func_name}({', '.join(args)}):
    try:
        orig_result = {func_name}({', '.join(args)})
        mut_result = {func_name}_mut({', '.join(args)})
        assert orig_result == mut_result
        print("PASS:", {', '.join(args)})
    except Exception as e:
        print("FAIL:", {', '.join(args)}, "->", e)
        raise

if __name__ == "__main__":
    test_{func_name}()
"""
        return test_body

    def _simple_test(self, func_name: str, original_code: str, mutated_code: str) -> Dict:
        """Fallback sem Hypothesis: testa algumas entradas fixas."""
        # Gera algumas entradas aleatórias (simplificado)
        import random
        tests = 5
        passed = 0
        failing = []
        for _ in range(tests):
            inputs = [random.randint(-100, 100) for _ in range(2)]  # assume 2 args
            # Cria um pequeno script que executa ambas
            test_code = f"""
{original_code}
{mutated_code}
import sys
orig = {func_name}({', '.join(map(str, inputs))})
mut = {func_name}({', '.join(map(str, inputs))})
if orig != mut:
    sys.exit(1)
"""
            success, _, _ = self.sandbox.run(test_code)
            if success:
                passed += 1
            else:
                failing.append(str(inputs))
        return {"passed": passed == tests, "tests": tests, "failing_inputs": failing}


# ============================================================================
# AVALIADOR AVANÇADO
# ============================================================================

class CodeEvaluator:
    def __init__(self, sandbox: Sandbox, kb: KnowledgeBase):
        self.sandbox = sandbox
        self.kb = kb
        self.tester = FunctionTester(sandbox)

    def evaluate(self, code: str, original_code: str = None) -> Dict[str, Any]:
        result = {
            "valid": False,
            "syntax_error": None,
            "runtime_error": None,
            "execution_time": None,
            "lines": 0,
            "complexity": 0,
            "num_functions": 0,
            "comment_ratio": 0.0,
            "tests": {},          # resultados por função
            "tests_passed": 0,
            "tests_total": 0,
            "coverage": 0.0,
            "score": 0.0
        }

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            result["syntax_error"] = str(e)
            return result

        result["valid"] = True

        # Métricas estáticas
        try:
            raw = radon_raw.analyze(code)
            result["lines"] = raw.loc
            result["comments"] = raw.comments
            result["blank"] = raw.blank
            result["comment_ratio"] = raw.comments / (raw.loc + 1e-6)

            cc_blocks = radon_cc.cc_visit(code)
            if cc_blocks:
                result["complexity"] = sum(b.complexity for b in cc_blocks) / len(cc_blocks)
            else:
                result["complexity"] = 1.0

            functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            result["num_functions"] = len(functions)
        except:
            pass

        # Execução para medir tempo
        success, output, exec_time = self.sandbox.run(code)
        result["execution_time"] = exec_time
        if not success:
            result["runtime_error"] = output[:200]

        # Testes comparativos
        if original_code and success:
            test_results = self._run_all_tests(original_code, code)
            result["tests"] = test_results
            passed = sum(1 for r in test_results.values() if r.get("passed", False))
            total = len(test_results)
            result["tests_passed"] = passed
            result["tests_total"] = total

        score = self._compute_score(result)
        result["score"] = round(score, 2)
        return result

    def _run_all_tests(self, original: str, mutated: str) -> Dict:
        """Testa todas as funções comuns entre original e mutada."""
        try:
            orig_tree = ast.parse(original)
            mut_tree = ast.parse(mutated)
        except:
            return {}

        orig_funcs = {f.name: f for f in ast.walk(orig_tree) if isinstance(f, ast.FunctionDef)}
        mut_funcs = {f.name: f for f in ast.walk(mut_tree) if isinstance(f, ast.FunctionDef)}
        common = set(orig_funcs.keys()) & set(mut_funcs.keys())

        results = {}
        for name in common:
            results[name] = self.tester.test_function(name, original, mutated)
        return results

    def _compute_score(self, metrics: Dict) -> float:
        # Base: 50% dos pontos vêm dos testes
        test_score = 0.0
        if metrics["tests_total"] > 0:
            test_score = 50.0 * (metrics["tests_passed"] / metrics["tests_total"])
        else:
            test_score = 50.0 if not metrics["runtime_error"] else 0.0

        # Qualidade do código (até 50%)
        quality = 0.0
        comp = metrics.get("complexity", 10)
        if comp <= 3:
            quality += 15
        elif comp <= 5:
            quality += 10
        elif comp <= 8:
            quality += 5

        nfunc = metrics.get("num_functions", 0)
        if 3 <= nfunc <= 8:
            quality += 10
        elif nfunc > 8:
            quality += 5
        elif nfunc > 0:
            quality += 2

        if metrics.get("comment_ratio", 0) > 0.05:
            quality += 5

        if metrics.get("execution_time", 1.0) < 0.1:
            quality += 10

        # Cobertura (futuro)
        if metrics.get("coverage", 0) > 0.7:
            quality += 10
        elif metrics.get("coverage", 0) > 0.3:
            quality += 5

        return min(test_score + quality, 100.0)


# ============================================================================
# GERADOR GROK (XAI)
# ============================================================================

class GrokGenerator:
    def __init__(self):
        self.api_key = Config.XAI_API_KEY
        self.base_url = "https://api.x.ai/v1/chat/completions"

    def generate_function(self, prompt: str, max_tokens: int = 300) -> Optional[str]:
        if not self.api_key:
            print("[⚠️] XAI_API_KEY não configurada")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Instrução para gerar código Python limpo
        full_prompt = f"Generate a Python function (only code, no explanations) that {prompt}"

        payload = {
            "messages": [{"role": "user", "content": full_prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']

            # Extrai código se estiver em markdown
            if '```' in content:
                parts = content.split('```')
                for part in parts:
                    if 'def ' in part or 'class ' in part:
                        code = part.strip()
                        if code.startswith('python\n'):
                            code = code[7:]
                        return code
            return content.strip()
        except Exception as e:
            print(f"[⚠️] Erro ao chamar Grok: {e}")
            return None


# ============================================================================
# MUTAÇÕES AVANÇADAS
# ============================================================================

class MutationEngine:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.grok = GrokGenerator() if Config.XAI_API_KEY else None
        self.mutation_types = [
            "add_comment",
            "remove_line",
            "rename_var",
            "swap_operator",
            "extract_function",
            "inline_function",
            "simplify_expression",
            "add_docstring",
            "insert_learned",
            "loop_conversion",
            "change_algorithm",
            "add_error_handling",
            "parallelize_loop",
            "memoize_function",
            "introduce_recursion",
            "add_class",
            "extract_class",
            "add_import",
            "grok_generate"
        ]

    def mutate(self, code: str, mutation_type: str) -> Tuple[str, str]:
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return code, "Erro de sintaxe, mutação ignorada"

        # Mutações que operam na string
        if mutation_type == "add_comment":
            return self._add_comment(code)
        elif mutation_type == "remove_line":
            return self._remove_line(code)
        elif mutation_type == "grok_generate" and self.grok:
            return self._grok_generate(code)

        # Mutações baseadas em AST
        transformer = self._get_transformer(mutation_type)
        if transformer:
            new_tree = transformer.visit(tree)
            try:
                ast.fix_missing_locations(new_tree)
                new_code = astor.to_source(new_tree)
                return new_code, self._get_description(mutation_type)
            except Exception as e:
                return code, f"Falha na {mutation_type}: {e}"

        # Mutações complexas
        if mutation_type == "extract_function":
            return self._extract_function(code)
        elif mutation_type == "inline_function":
            return self._inline_function(code)
        elif mutation_type == "insert_learned":
            return self._insert_learned_function(code)
        elif mutation_type == "change_algorithm":
            return self._change_algorithm(code)
        elif mutation_type == "add_error_handling":
            return self._add_error_handling(code)
        elif mutation_type == "parallelize_loop":
            return self._parallelize_loop(code)
        elif mutation_type == "memoize_function":
            return self._memoize_function(code)
        elif mutation_type == "introduce_recursion":
            return self._introduce_recursion(code)
        elif mutation_type == "add_class":
            return self._add_class(code)
        elif mutation_type == "extract_class":
            return self._extract_class(code)
        elif mutation_type == "add_import":
            return self._add_import(code)

        return code, "Tipo de mutação desconhecido"

    def _get_transformer(self, mtype: str) -> Optional[ast.NodeTransformer]:
        mapping = {
            "rename_var": RenameVarTransformer,
            "swap_operator": SwapOperatorTransformer,
            "simplify_expression": SimplifyExpressionTransformer,
            "add_docstring": AddDocstringTransformer,
            "loop_conversion": LoopConversionTransformer,
        }
        cls = mapping.get(mtype)
        return cls() if cls else None

    def _get_description(self, mtype: str) -> str:
        desc = {
            "rename_var": "Renomeação de variável",
            "swap_operator": "Troca de operador",
            "simplify_expression": "Simplificação de expressão",
            "add_docstring": "Adição de docstring",
            "loop_conversion": "Conversão de loop",
        }
        return desc.get(mtype, mtype)

    def _add_comment(self, code: str) -> Tuple[str, str]:
        lines = code.splitlines()
        candidates = [i for i, line in enumerate(lines) if line.strip() and not line.strip().startswith('#')]
        if not candidates:
            return code, "Nenhum local para comentário"
        idx = random.choice(candidates)
        comment = random.choice([
            "# TODO: otimizar futuramente",
            "# Gerado por Atena",
            "# Esta linha pode ser melhorada",
            "# Magic number, talvez extrair constante",
            "# Versão mutante"
        ])
        lines.insert(idx, comment)
        return '\n'.join(lines), f"Comentário adicionado"

    def _remove_line(self, code: str) -> Tuple[str, str]:
        lines = code.splitlines()
        candidates = [i for i, line in enumerate(lines) 
                     if line.strip() and not line.strip().startswith(('def ', 'class ', 'import ', 'from ', '#'))]
        if not candidates:
            return code, "Nenhuma linha removível"
        idx = random.choice(candidates)
        removed = lines.pop(idx)
        return '\n'.join(lines), f"Linha removida: {removed[:30]}"

    def _grok_generate(self, code: str) -> Tuple[str, str]:
        prompt = random.choice([
            "calculates the factorial of a number",
            "checks if a number is prime",
            "sorts a list using quicksort",
            "returns the nth Fibonacci number",
            "converts Celsius to Fahrenheit",
            "finds the maximum in a list",
            "computes the average of a list"
        ])
        generated = self.grok.generate_function(prompt)
        if generated and "def " in generated:
            new_code = code + f"\n\n# Gerado por Grok: {prompt}\n" + generated
            return new_code, f"Função gerada por Grok: {prompt}"
        else:
            return code, "Falha na geração Grok"

    def _extract_function(self, code: str) -> Tuple[str, str]:
        try:
            tree = ast.parse(code)
            functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            if not functions:
                return code, "Nenhuma função para extrair"
            func = random.choice(functions)
            candidates = [n for n in ast.walk(func) if isinstance(n, (ast.If, ast.For, ast.While)) and n.body]
            if not candidates:
                return code, "Nenhum bloco candidato"
            block = random.choice(candidates)

            used_vars = set()
            for node in ast.walk(block):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    used_vars.add(node.id)
            builtins = dir(__builtins__)
            params = [ast.arg(arg=v, annotation=None) for v in used_vars if v not in builtins]

            new_name = f"extracted_{random.randint(1000,9999)}"
            args = ast.arguments(args=params, vararg=None, kwarg=None, defaults=[])
            new_func = ast.FunctionDef(
                name=new_name,
                args=args,
                body=block.body,
                decorator_list=[],
                returns=None
            )

            call_args = [ast.Name(id=v, ctx=ast.Load()) for v in used_vars if v not in builtins]
            call = ast.Expr(value=ast.Call(
                func=ast.Name(id=new_name, ctx=ast.Load()),
                args=call_args,
                keywords=[]
            ))
            block.body = [call]

            for node in ast.walk(tree):
                if isinstance(node, ast.Module):
                    node.body.append(new_func)
                    break

            new_code = astor.to_source(tree)
            return new_code, f"Função {new_name} extraída"
        except Exception as e:
            return code, f"Erro na extração: {e}"

    def _inline_function(self, code: str) -> Tuple[str, str]:
        return code, "Inline function (não implementado)"

    def _insert_learned_function(self, code: str) -> Tuple[str, str]:
        func_data = self.kb.get_random_function()
        if not func_data:
            return code, "Nenhuma função aprendida"
        func_code, source = func_data
        new_code = code + f"\n\n# Função aprendida de {source}\n" + func_code
        return new_code, f"Função inserida de {source}"

    def _change_algorithm(self, code: str) -> Tuple[str, str]:
        similar = self.kb.get_function_by_purpose(["sort", "order", "ordenar"])
        if not similar:
            return code, "Nenhum algoritmo similar encontrado"
        new_algo, source = similar
        # Identifica função candidata
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and "sort" in node.name.lower():
                    # Substituição simples: adiciona a nova função e mantém a antiga
                    new_code = code + f"\n\n# Algoritmo melhorado de {source}\n" + new_algo
                    return new_code, f"Algoritmo adicionado de {source}"
            return code, "Nenhuma função de ordenação encontrada"
        except:
            return code, "Falha na troca de algoritmo"

    def _add_error_handling(self, code: str) -> Tuple[str, str]:
        try:
            tree = ast.parse(code)
            transformer = AddErrorHandlingTransformer()
            new_tree = transformer.visit(tree)
            new_code = astor.to_source(new_tree)
            return new_code, "Adicionado tratamento de erros"
        except:
            return code, "Falha ao adicionar tratamento de erros"

    def _parallelize_loop(self, code: str) -> Tuple[str, str]:
        return code, "Paralelização de loop (não implementada)"

    def _memoize_function(self, code: str) -> Tuple[str, str]:
        try:
            tree = ast.parse(code)
            # Adiciona import functools no módulo se necessário
            has_functools = False
            for node in ast.walk(tree):
                if isinstance(node, ast.Import) and any(alias.name == "functools" for alias in node.names):
                    has_functools = True
                    break
                if isinstance(node, ast.ImportFrom) and node.module == "functools":
                    has_functools = True
                    break
            if not has_functools:
                # Adiciona import no início
                import_node = ast.Import(names=[ast.alias(name="functools", asname=None)])
                tree.body.insert(0, import_node)

            # Adiciona decorator @functools.lru_cache em funções puras (heurística)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not node.decorator_list:
                    # Heurística simples: função que não chama print, open, etc.
                    has_io = False
                    for n in ast.walk(node):
                        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ['print', 'open', 'input']:
                            has_io = True
                            break
                    if not has_io:
                        decorator = ast.Attribute(value=ast.Name(id='functools', ctx=ast.Load()), attr='lru_cache', ctx=ast.Load())
                        node.decorator_list.append(decorator)
            new_code = astor.to_source(tree)
            return new_code, "Adicionada memoização"
        except:
            return code, "Falha ao adicionar memoização"

    def _introduce_recursion(self, code: str) -> Tuple[str, str]:
        return code, "Introdução de recursão (não implementada)"

    def _add_class(self, code: str) -> Tuple[str, str]:
        class_template = '''
class NovaClasse:
    """Classe gerada pela Atena."""
    def __init__(self, valor=None):
        self.valor = valor
    
    def processar(self):
        if self.valor:
            return self.valor * 2
        return None
'''
        new_code = code + class_template
        return new_code, "Classe adicionada"

    def _extract_class(self, code: str) -> Tuple[str, str]:
        # Tenta agrupar funções relacionadas em uma classe
        return code, "Extração de classe (não implementada)"

    def _add_import(self, code: str) -> Tuple[str, str]:
        imports = ["import math", "import random", "from collections import Counter", "import itertools"]
        imp = random.choice(imports)
        # Verifica se já existe
        if imp in code:
            return code, "Import já existente"
        new_code = imp + "\n" + code
        return new_code, f"Import adicionado: {imp}"


# Transformers AST

class RenameVarTransformer(ast.NodeTransformer):
    def __init__(self):
        self.rename_map = {}
        self.counter = 0

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store) and node.id not in dir(__builtins__):
            if node.id not in self.rename_map:
                self.rename_map[node.id] = f"{node.id}_v{self.counter}"
                self.counter += 1
            new_id = self.rename_map[node.id]
            return ast.Name(id=new_id, ctx=node.ctx)
        elif isinstance(node.ctx, ast.Load) and node.id in self.rename_map:
            return ast.Name(id=self.rename_map[node.id], ctx=node.ctx)
        return node

class SwapOperatorTransformer(ast.NodeTransformer):
    def visit_BinOp(self, node):
        if random.random() < 0.3:
            if isinstance(node.op, ast.Add):
                node.op = ast.Sub()
            elif isinstance(node.op, ast.Sub):
                node.op = ast.Add()
            elif isinstance(node.op, ast.Mult):
                node.op = ast.Div() if random.random() < 0.5 else ast.FloorDiv()
            elif isinstance(node.op, ast.Div):
                node.op = ast.Mult()
        return node

class SimplifyExpressionTransformer(ast.NodeTransformer):
    def visit_BinOp(self, node):
        node = self.generic_visit(node)
        # x * 0 -> 0
        if isinstance(node.op, ast.Mult):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                return ast.Constant(value=0)
            if isinstance(node.left, ast.Constant) and node.left.value == 0:
                return ast.Constant(value=0)
        # x + 0 -> x
        if isinstance(node.op, ast.Add):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                return node.left
            if isinstance(node.left, ast.Constant) and node.left.value == 0:
                return node.right
        # x - 0 -> x
        if isinstance(node.op, ast.Sub):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                return node.left
        # x * 1 -> x
        if isinstance(node.op, ast.Mult):
            if isinstance(node.right, ast.Constant) and node.right.value == 1:
                return node.left
            if isinstance(node.left, ast.Constant) and node.left.value == 1:
                return node.right
        return node

class AddDocstringTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        if not ast.get_docstring(node):
            docstring = ast.Expr(value=ast.Constant(value="Função gerada/evoluída pela Atena."))
            node.body.insert(0, docstring)
        return node

class LoopConversionTransformer(ast.NodeTransformer):
    def visit_For(self, node):
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
            args = node.iter.args
            if len(args) == 1:
                start = ast.Constant(value=0)
                end = args[0]
                step = ast.Constant(value=1)
            elif len(args) == 2:
                start = args[0]
                end = args[1]
                step = ast.Constant(value=1)
            else:
                return node
            assign = ast.Assign(targets=[ast.Name(id=node.target.id, ctx=ast.Store())], value=start)
            test = ast.Compare(left=ast.Name(id=node.target.id, ctx=ast.Load()), ops=[ast.Lt()], comparators=[end])
            inc = ast.AugAssign(target=ast.Name(id=node.target.id, ctx=ast.Store()), op=ast.Add(), value=step)
            body = node.body + [inc]
            while_node = ast.While(test=test, body=body, orelse=[])
            ast.copy_location(assign, node)
            ast.copy_location(while_node, node)
            return [assign, while_node]
        return node

class AddErrorHandlingTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # Envolve o corpo em try/except (simplificado)
        if node.body and not any(isinstance(n, ast.Try) for n in node.body):
            try_body = node.body
            handler = ast.ExceptHandler(type=ast.Name(id='Exception', ctx=ast.Load()), name=None, body=[
                ast.Expr(value=ast.Call(func=ast.Name(id='print', ctx=ast.Load()), args=[ast.Constant(value="Erro na função")], keywords=[])),
                ast.Raise()
            ])
            new_body = [ast.Try(body=try_body, handlers=[handler], orelse=[], finalbody=[])]
            node.body = new_body
        return node


# ============================================================================
# APRENDIZADO GITHUB COM PROPÓSITO
# ============================================================================

class GitHubLearner(threading.Thread):
    def __init__(self, kb: KnowledgeBase):
        super().__init__(daemon=True)
        self.kb = kb
        self.session = requests.Session()
        if Config.GITHUB_TOKEN:
            self.session.headers.update({"Authorization": f"token {Config.GITHUB_TOKEN}"})
        self.running = True
        self.processed_count = 0
        self.queue = queue.Queue()

    def run(self):
        self._search_and_queue_repos()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            while self.running:
                try:
                    repo = self.queue.get(timeout=10)
                    executor.submit(self._process_repo, repo)
                except queue.Empty:
                    if not self._search_and_queue_repos():
                        break
                time.sleep(1)

    def _search_and_queue_repos(self) -> bool:
        for page in range(1, 20):
            repos = self._search_repositories(page=page, per_page=30)
            if not repos:
                break
            for repo in repos:
                self.queue.put(repo)
                self.processed_count += 1
                if self.processed_count >= Config.GITHUB_MAX_FUNCTIONS // 30:
                    return False
        return True

    def _search_repositories(self, page=1, per_page=30) -> List[Dict]:
        url = "https://api.github.com/search/repositories"
        params = {"q": "language:python", "sort": "stars", "order": "desc", "page": page, "per_page": per_page}
        try:
            resp = self.session.get(url, params=params, timeout=15)
            resp.raise_for_status()
            return resp.json().get("items", [])
        except Exception as e:
            return []

    def _process_repo(self, repo):
        repo_name = repo["full_name"]
        cur = self.kb.conn.execute("SELECT 1 FROM github_repos WHERE repo_full_name = ?", (repo_name,))
        if cur.fetchone():
            return
        print(f"[🌐] Processando {repo_name}...")
        files_processed = 0
        tree = self._get_repo_tree(repo_name)
        if tree:
            py_files = [f for f in tree if f["path"].endswith(".py") and f["type"] == "blob"]
            random.shuffle(py_files)
            for file_info in py_files[:Config.GITHUB_MAX_FILES_PER_REPO]:
                content = self._fetch_file(repo_name, file_info["path"])
                if content:
                    functions = self._extract_functions(content)
                    for func in functions:
                        purpose = self._infer_purpose(func)
                        self.kb.add_function(func, f"github:{repo_name}/{file_info['path']}", purpose)
                    files_processed += 1
                time.sleep(0.1)
        self.kb.conn.execute(
            "INSERT OR REPLACE INTO github_repos (repo_full_name, stars, last_processed, files_processed) VALUES (?, ?, ?, ?)",
            (repo_name, repo.get("stargazers_count", 0), datetime.now().isoformat(), files_processed)
        )
        self.kb.conn.commit()

    def _get_repo_tree(self, repo_full_name):
        url = f"https://api.github.com/repos/{repo_full_name}/git/trees/HEAD?recursive=1"
        try:
            resp = self.session.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json().get("tree", [])
        except:
            return None

    def _fetch_file(self, repo_full_name, path):
        url = f"https://api.github.com/repos/{repo_full_name}/contents/{path}"
        try:
            resp = self.session.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if data.get("encoding") == "base64":
                import base64
                return base64.b64decode(data["content"]).decode("utf-8")
            return None
        except:
            return None

    def _extract_functions(self, code):
        try:
            tree = ast.parse(code)
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_code = astor.to_source(node)
                    functions.append(func_code)
            return functions
        except:
            return []

    def _infer_purpose(self, func_code: str) -> str:
        try:
            tree = ast.parse(func_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    name = node.name
                    doc = ast.get_docstring(node) or ""
                    if "sort" in name or "order" in name or "orden" in name:
                        return "ordenacao"
                    if "sum" in name or "soma" in name or "add" in name:
                        return "soma"
                    if "avg" in name or "media" in name or "mean" in name:
                        return "media"
                    if "search" in name or "busca" in name:
                        return "busca"
                    if "fact" in name or "fatorial" in name:
                        return "fatorial"
                    if "prime" in name or "primo" in name:
                        return "primo"
                    if "fib" in name:
                        return "fibonacci"
            return "desconhecido"
        except:
            return "desconhecido"

    def stop(self):
        self.running = False


# ============================================================================
# NEWS API CLIENT
# ============================================================================

class NewsAPIClient:
    def __init__(self, kb):
        self.kb = kb
        self.api_key = Config.NEWS_API_KEY
        self.session = requests.Session()

    def fetch_tech_news(self, days=1):
        if not self.api_key:
            return []
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "artificial intelligence OR machine learning OR python programming",
            "from": (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d"),
            "sortBy": "relevancy",
            "language": "en",
            "pageSize": 20,
            "apiKey": self.api_key
        }
        try:
            resp = self.session.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return data.get("articles", [])
        except Exception as e:
            return []

    def update_objectives(self):
        articles = self.fetch_tech_news()
        if not articles:
            return
        text = " ".join([a.get("title", "") + " " + a.get("description", "") for a in articles])
        words = [w.lower() for w in text.split() if len(w) > 5 and w.isalpha()]
        keywords = [w for w, _ in Counter(words).most_common(5)]
        for kw in keywords[:3]:
            self.kb.add_temporary_objective(f"learn_{kw}", f"Aprender sobre {kw}", target=1.0, weight=0.3)
            print(f"[📰] Novo objetivo: aprender sobre {kw}")


# ============================================================================
# PREDITOR DE MUTAÇÕES (Random Forest)
# ============================================================================

class MutationPredictor:
    def __init__(self, kb):
        self.kb = kb
        self.model = None
        self.vectorizer = None
        self._load_model()

    def _load_model(self):
        if Config.PREDICTOR_MODEL.exists():
            with open(Config.PREDICTOR_MODEL, 'rb') as f:
                self.model, self.vectorizer = pickle.load(f)
            print("[✓] Modelo preditor carregado")

    def _save_model(self):
        with open(Config.PREDICTOR_MODEL, 'wb') as f:
            pickle.dump((self.model, self.vectorizer), f)

    def train(self):
        from sklearn.feature_extraction import DictVectorizer
        from sklearn.ensemble import RandomForestClassifier

        X_dict, y = self.kb.get_training_data()
        if len(X_dict) < Config.MIN_TRAINING_SAMPLES:
            print(f"[⚠️] Amostras insuficientes: {len(X_dict)} < {Config.MIN_TRAINING_SAMPLES}")
            return

        self.vectorizer = DictVectorizer(sparse=False)
        X = self.vectorizer.fit_transform(X_dict)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        self._save_model()
        print(f"[🤖] Modelo treinado com {len(X_dict)} amostras")

    def predict_proba(self, features: Dict) -> float:
        if not self.model or not self.vectorizer:
            return 0.5
        X = self.vectorizer.transform([features])
        prob = self.model.predict_proba(X)[0][1]
        return prob


# ============================================================================
# AUTO-DEPLOY
# ============================================================================

class AutoDeploy:
    @staticmethod
    def deploy():
        results = []
        if Config.DEPLOY_GIT_REPO:
            results.append(AutoDeploy._deploy_git())
        if Config.DEPLOY_DOCKER_IMAGE:
            results.append(AutoDeploy._deploy_docker())
        if Config.DEPLOY_COMMAND:
            results.append(AutoDeploy._run_command())
        return any(results)

    @staticmethod
    def _deploy_git():
        try:
            deploy_path = Config.DEPLOY_DIR / "repo"
            if not deploy_path.exists():
                subprocess.run(["git", "clone", Config.DEPLOY_GIT_REPO, str(deploy_path)], check=True)
            else:
                subprocess.run(["git", "-C", str(deploy_path), "pull"], check=True)
            shutil.copy(Config.CURRENT_CODE_FILE, deploy_path / "atena.py")
            subprocess.run(["git", "-C", str(deploy_path), "add", "atena.py"], check=True)
            subprocess.run(["git", "-C", str(deploy_path), "commit", "-m", f"Auto-deploy Atena {datetime.now().isoformat()}"], check=True)
            subprocess.run(["git", "-C", str(deploy_path), "push", "origin", Config.DEPLOY_BRANCH], check=True)
            print("[📤] Deploy Git realizado")
            return True
        except Exception as e:
            print(f"[⚠️] Erro Git deploy: {e}")
            return False

    @staticmethod
    def _deploy_docker():
        try:
            dockerfile = Config.DEPLOY_DIR / "Dockerfile"
            dockerfile.write_text(f"""FROM python:3.10-slim
WORKDIR /app
COPY {Config.CURRENT_CODE_FILE.name} /app/atena.py
CMD ["python", "atena.py"]
""")
            subprocess.run(["docker", "build", "-t", Config.DEPLOY_DOCKER_IMAGE, str(Config.DEPLOY_DIR)], check=True)
            subprocess.run(["docker", "push", Config.DEPLOY_DOCKER_IMAGE], check=True)
            print("[🐳] Deploy Docker realizado")
            return True
        except Exception as e:
            print(f"[⚠️] Erro Docker: {e}")
            return False

    @staticmethod
    def _run_command():
        try:
            subprocess.run(Config.DEPLOY_COMMAND, shell=True, check=True)
            print("[⚙️] Comando executado")
            return True
        except Exception as e:
            print(f"[⚠️] Erro comando: {e}")
            return False


# ============================================================================
# NÚCLEO DE EVOLUÇÃO
# ============================================================================

class AtenaCore:
    def __init__(self):
        Config.setup()
        self.kb = KnowledgeBase()
        self.sandbox = Sandbox(timeout=Config.EVALUATION_TIMEOUT)
        self.evaluator = CodeEvaluator(self.sandbox, self.kb)
        self.mutation_engine = MutationEngine(self.kb)
        self.predictor = MutationPredictor(self.kb)
        self.news = NewsAPIClient(self.kb) if Config.NEWS_API_KEY else None
        self.learner = GitHubLearner(self.kb) if Config.GITHUB_TOKEN else None
        self.current_code = self._read_current_code()
        self.generation = 0
        self.best_code = self.current_code
        self.best_score = self.evaluator.evaluate(self.current_code)["score"]
        self.original_code = self.current_code

    def _read_current_code(self):
        return Config.CURRENT_CODE_FILE.read_text()

    def _write_current_code(self, code):
        Config.CURRENT_CODE_FILE.write_text(code)
        self.current_code = code

    def _backup(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = Config.BACKUP_DIR / f"atena_backup_{timestamp}.py"
        shutil.copy(Config.CURRENT_CODE_FILE, backup_path)
        file_hash = hashlib.sha256(self.current_code.encode()).hexdigest()
        self.kb.record_backup(str(backup_path), file_hash, self.best_score)

    def evolve_one_cycle(self):
        self.generation += 1
        print(f"\n🧬 Geração {self.generation}")

        objectives = self.kb.get_objectives()
        mutation_types = self.mutation_engine.mutation_types
        weights = {mt: 1.0 for mt in mutation_types}

        # Ajusta pesos pelos objetivos
        for obj in objectives:
            if obj["name"] == "reduzir_complexidade" and obj["current"] > obj["target"]:
                weights["simplify_expression"] += 2.0
                weights["extract_function"] += 1.0
            if obj["name"] == "aumentar_modularidade":
                weights["extract_function"] += 2.0
                weights["insert_learned"] += 1.0
                weights["add_class"] += 1.0
            if obj["name"] == "melhorar_documentacao":
                weights["add_docstring"] += 2.0
                weights["add_comment"] += 1.0
            if obj["name"] == "aprender_algoritmos" and obj["current"] < obj["target"]:
                weights["insert_learned"] += 3.0
                weights["change_algorithm"] += 2.0
                weights["grok_generate"] += 2.0
            if obj["name"].startswith("learn_"):
                weights["insert_learned"] += 2.0
                weights["grok_generate"] += 1.0

        # Preditor com exploração
        if self.predictor.model and random.random() > Config.EXPLORATION_RATE:
            current_metrics = self.evaluator.evaluate(self.current_code)
            for mt in mutation_types:
                feat = {
                    "lines": current_metrics["lines"],
                    "num_functions": current_metrics["num_functions"],
                    "complexity": current_metrics["complexity"],
                    "mutation_type": mt
                }
                prob = self.predictor.predict_proba(feat)
                weights[mt] *= (0.5 + prob)

        # Escolhe mutação
        mtype = random.choices(list(weights.keys()), weights=list(weights.values()))[0]

        # Aplica mutação
        mutated, desc = self.mutation_engine.mutate(self.current_code, mtype)

        # Avalia
        metrics = self.evaluator.evaluate(mutated, original_code=self.original_code)
        new_score = metrics["score"]

        # Features para treino
        features = {
            "mutation_type": mtype,
            "old_score": self.best_score,
            "new_score": new_score,
            "lines": metrics["lines"],
            "complexity": metrics["complexity"],
            "num_functions": metrics["num_functions"],
            "tests_passed": metrics["tests_passed"],
            "tests_total": metrics["tests_total"]
        }
        test_results = metrics.get("tests", {})

        replaced = False
        if metrics["valid"] and new_score > self.best_score:
            print(f"✅ Melhorou: {new_score:.2f} > {self.best_score:.2f}")
            self._backup()
            self._write_current_code(mutated)
            self.best_score = new_score
            self.best_code = mutated
            replaced = True
        else:
            print(f"➡️ Não melhorou: {new_score:.2f} <= {self.best_score:.2f}")

        self.kb.record_evolution(self.generation, desc, self.best_score, new_score, replaced, features, test_results)

        # Atualiza objetivos
        self.kb.update_objective("reduzir_complexidade", metrics["complexity"])
        self.kb.update_objective("aumentar_modularidade", metrics["num_functions"])
        self.kb.update_objective("melhorar_documentacao", metrics["comment_ratio"])
        self.kb.update_objective("reduzir_tempo_execucao", metrics.get("execution_time", 1.0))
        self.kb.update_objective("aprender_algoritmos", metrics["num_functions"] // 2)
        self.kb.update_objective("aumentar_cobertura_testes", metrics["tests_passed"] / max(1, metrics["tests_total"]))

        return {"generation": self.generation, "mutation": desc, "score": new_score, "replaced": replaced}


# ============================================================================
# APLICATIVO PRINCIPAL
# ============================================================================

class AtenaApp:
    def __init__(self):
        self.core = AtenaCore()
        self.running = False
        self.last_train_time = 0
        self.last_news_time = 0
        self.last_deploy_score = self.core.best_score

    def start_autonomous(self, cycles=None):
        print("\n🚀 Modo autônomo iniciado.")
        self.running = True
        if self.core.learner:
            self.core.learner.start()
        try:
            cycle_count = 0
            while self.running and (cycles is None or cycle_count < cycles):
                result = self.core.evolve_one_cycle()
                cycle_count += 1

                if time.time() - self.last_train_time > Config.TRAINING_INTERVAL:
                    self.core.predictor.train()
                    self.last_train_time = time.time()

                if self.core.news and time.time() - self.last_news_time > 3600:
                    self.core.news.update_objectives()
                    self.last_news_time = time.time()

                if self.core.best_score > self.last_deploy_score * Config.DEPLOY_THRESHOLD:
                    print("📈 Melhoria significativa! Acionando deploy...")
                    AutoDeploy.deploy()
                    self.last_deploy_score = self.core.best_score

                if cycles is None:
                    time.sleep(60)
        except KeyboardInterrupt:
            print("\nEncerrando...")
        finally:
            if self.core.learner:
                self.core.learner.stop()
            self.core.kb.close()

    def run_interactive(self):
        print("\n" + "="*60)
        print("🚀 ATENA - MODO INTERATIVO")
        print("="*60)
        print("Comandos:")
        print("  /evoluir         - Executa 1 ciclo")
        print("  /ciclos N        - Executa N ciclos")
        print("  /status          - Mostra status")
        print("  /codigo          - Mostra código atual")
        print("  /melhor          - Mostra melhor código")
        print("  /objetivos       - Lista objetivos")
        print("  /treinar         - Treina preditor")
        print("  /deploy          - Executa deploy")
        print("  /sair            - Encerra")
        print("="*60)

        if self.core.learner:
            self.core.learner.start()

        while True:
            try:
                cmd = input("\nAtena> ").strip()
                if cmd == '/sair':
                    break
                elif cmd == '/evoluir':
                    self.core.evolve_one_cycle()
                elif cmd.startswith('/ciclos'):
                    try:
                        n = int(cmd.split()[1])
                        for i in range(n):
                            self.core.evolve_one_cycle()
                            if i < n-1:
                                time.sleep(2)
                    except:
                        print("Uso: /ciclos N")
                elif cmd == '/status':
                    s = self.core.kb.get_objectives()
                    print(f"\n📊 Geração: {self.core.generation}")
                    print(f"Score atual: {self.core.best_score:.2f}")
                    print("Objetivos:")
                    for o in s:
                        prog = (o['current'] / o['target']) * 100 if o['target'] > 0 else 0
                        print(f"  {o['name']}: {o['current']:.2f}/{o['target']:.2f} ({prog:.1f}%)")
                elif cmd == '/codigo':
                    print("\n" + self.core.current_code)
                elif cmd == '/melhor':
                    print("\n🏆 Melhor código (score {:.2f}):\n".format(self.core.best_score))
                    print(self.core.best_code)
                elif cmd == '/objetivos':
                    objs = self.core.kb.get_objectives()
                    for o in objs:
                        print(f"{o['name']}: {o['current']:.2f} / {o['target']:.2f} (peso {o['weight']})")
                elif cmd == '/treinar':
                    self.core.predictor.train()
                elif cmd == '/deploy':
                    AutoDeploy.deploy()
                else:
                    print("Comando não reconhecido")
            except KeyboardInterrupt:
                print("\n")
                continue

        if self.core.learner:
            self.core.learner.stop()
        self.core.kb.close()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto", action="store_true", help="Modo autônomo")
    parser.add_argument("--cycles", type=int, default=0, help="Número de ciclos (0 = infinito)")
    args = parser.parse_args()

    app = AtenaApp()
    if args.auto:
        if args.cycles > 0:
            for i in range(args.cycles):
                app.core.evolve_one_cycle()
                if i < args.cycles - 1:
                    time.sleep(2)
        else:
            app.start_autonomous()
    else:
        app.run_interactive()
