#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ATENA NEURAL - AUTO-EVOLUÇÃO REAL
Versão completa com:
- Mutações reais de código (AST)
- GitHub Learner com embeddings semânticos
- News API para tendências
- Sandbox Docker/isolado
- Banco SQLite com vetores
- Auto-treinamento com preditor
- Auto-deploy (Git/Docker/comando)
- Score baseado em testes e métricas
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
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field

# Bibliotecas de análise de código
import radon.complexity as radon_cc
import radon.raw as radon_raw

# Para embeddings (instale com: pip install sentence-transformers)
try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE = True
except ImportError:
    HAS_SENTENCE = False
    print("[⚠️] sentence-transformers não instalado. Usando fallback TF-IDF.")

# Para deploy Docker (opcional)
try:
    import docker
    HAS_DOCKER_PY = True
except ImportError:
    HAS_DOCKER_PY = False

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
    
    # Parâmetros de evolução
    MAX_MUTATION_ATTEMPTS: int = 5
    EVALUATION_TIMEOUT: int = 10
    BACKUP_KEEP_DAYS: int = 7
    PARALLEL_WORKERS: int = 4
    GITHUB_MAX_REPOS_PER_QUERY: int = 50
    GITHUB_MAX_FILES_PER_REPO: int = 10
    GITHUB_LEARNING_INTERVAL: int = 3600  # 1 hora
    TRAINING_INTERVAL: int = 3600
    MIN_TRAINING_SAMPLES: int = 100
    
    # Deploy
    DEPLOY_GIT_REPO: str = os.getenv("DEPLOY_GIT_REPO", "")
    DEPLOY_BRANCH: str = "main"
    DEPLOY_DOCKER_IMAGE: str = os.getenv("DEPLOY_DOCKER_IMAGE", "")
    DEPLOY_COMMAND: str = os.getenv("DEPLOY_COMMAND", "")
    
    # Modelo de embedding
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # leve e eficaz

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
# BANCO DE CONHECIMENTO COM EMBEDDINGS
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
        # Cache de funções para busca rápida
        self.function_cache = []
        self._load_cache()

    def _init_tables(self):
        # Tabela de funções aprendidas com vetor de embedding
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
             embedding BLOB)''')  # armazena o vetor como pickle

        # Tabela de repositórios GitHub processados
        self.conn.execute('''CREATE TABLE IF NOT EXISTS github_repos
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             repo_full_name TEXT UNIQUE,
             stars INTEGER,
             last_processed TEXT,
             files_processed INTEGER)''')

        # Tabela de objetivos
        self.conn.execute('''CREATE TABLE IF NOT EXISTS objectives
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT UNIQUE,
             description TEXT,
             weight REAL DEFAULT 1.0,
             current_value REAL,
             target_value REAL,
             active BOOLEAN DEFAULT 1)''')

        # Tabela de evoluções (histórico)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS evolution_metrics
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             timestamp TEXT,
             generation INTEGER,
             mutation TEXT,
             old_score REAL,
             new_score REAL,
             replaced BOOLEAN,
             features TEXT)''')  # features para treino

        # Tabela de backups
        self.conn.execute('''CREATE TABLE IF NOT EXISTS backups
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             timestamp TEXT,
             file_path TEXT,
             hash TEXT,
             score REAL)''')

        self.conn.commit()
        self._init_default_objectives()

    def _init_default_objectives(self):
        default_objectives = [
            ("reduzir_complexidade", "Reduzir complexidade ciclomática média", 1.0, 10.0, 5.0),
            ("aumentar_modularidade", "Aumentar número de funções", 0.8, 2.0, 10.0),
            ("melhorar_documentacao", "Aumentar proporção de comentários", 0.5, 0.0, 0.2),
            ("reduzir_tempo_execucao", "Reduzir tempo de execução da main", 1.0, 1.0, 0.1)
        ]
        for name, desc, weight, curr, target in default_objectives:
            self.conn.execute(
                "INSERT OR IGNORE INTO objectives (name, description, weight, current_value, target_value) VALUES (?, ?, ?, ?, ?)",
                (name, desc, weight, curr, target)
            )
        self.conn.commit()

    def _load_cache(self):
        cursor = self.conn.execute("SELECT code, embedding FROM learned_functions")
        for code, emb_blob in cursor:
            if emb_blob:
                emb = pickle.loads(emb_blob)
                self.function_cache.append((code, emb))

    def add_function(self, code: str, source: str) -> bool:
        """Adiciona função ao banco, com embedding."""
        try:
            tree = ast.parse(code)
            functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            if not functions:
                return False
            func = functions[0]
            func_name = func.name
            func_code = astor.to_source(func)
            func_hash = hashlib.sha256(func_code.encode()).hexdigest()

            # Métricas
            complexity = self._compute_complexity(func_code)
            lines = len(func_code.splitlines())

            # Embedding
            embedding = None
            if self.embedding_model:
                # Gera descrição textual da função (nome + corpo simplificado)
                text = f"{func_name} " + " ".join([n.__class__.__name__ for n in ast.walk(func) if isinstance(n, (ast.Name, ast.Call))])
                emb = self.embedding_model.encode(text).astype(np.float32)
                embedding = pickle.dumps(emb)

            self.conn.execute(
                """INSERT OR IGNORE INTO learned_functions 
                   (source, function_name, code, hash, complexity, lines, first_seen, embedding)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (source, func_name, func_code, func_hash, complexity, lines,
                 datetime.now().isoformat(), embedding)
            )
            self.conn.commit()
            if embedding:
                self.function_cache.append((func_code, emb))
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

    def search_similar(self, query_code: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """Busca funções semelhantes por embedding."""
        if not self.embedding_model or not self.function_cache:
            return []
        # Gera embedding da consulta
        try:
            tree = ast.parse(query_code)
            funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            if not funcs:
                return []
            query_func = funcs[0]
            text = f"{query_func.name} " + " ".join([n.__class__.__name__ for n in ast.walk(query_func) if isinstance(n, (ast.Name, ast.Call))])
            query_emb = self.embedding_model.encode(text).astype(np.float32)
        except:
            return []

        similarities = []
        for code, emb in self.function_cache:
            sim = np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb) + 1e-8)
            similarities.append((sim, code))
        similarities.sort(reverse=True)
        return [(code, sim) for sim, code in similarities[:top_n] if sim > 0.5]

    def get_random_function(self) -> Optional[Tuple[str, str]]:
        cursor = self.conn.execute("SELECT code, source FROM learned_functions ORDER BY RANDOM() LIMIT 1")
        row = cursor.fetchone()
        if row:
            return row[0], row[1]
        return None

    def update_objective(self, name: str, value: float):
        self.conn.execute("UPDATE objectives SET current_value = ? WHERE name = ?", (value, name))
        self.conn.commit()

    def get_objectives(self) -> List[Dict]:
        cursor = self.conn.execute("SELECT name, description, weight, current_value, target_value FROM objectives WHERE active=1")
        return [{"name": r[0], "description": r[1], "weight": r[2], "current": r[3], "target": r[4]} for r in cursor]

    def record_evolution(self, generation: int, mutation: str, old_score: float, new_score: float, replaced: bool, features: dict = None):
        feat_json = json.dumps(features) if features else None
        self.conn.execute(
            "INSERT INTO evolution_metrics (timestamp, generation, mutation, old_score, new_score, replaced, features) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (datetime.now().isoformat(), generation, mutation, old_score, new_score, replaced, feat_json)
        )
        self.conn.commit()

    def record_backup(self, file_path: str, file_hash: str, score: float):
        self.conn.execute(
            "INSERT INTO backups (timestamp, file_path, hash, score) VALUES (?, ?, ?, ?)",
            (datetime.now().isoformat(), file_path, file_hash, score)
        )
        self.conn.commit()

    def get_training_data(self) -> Tuple[List[Dict], List[int]]:
        """Retorna features e labels para treino do preditor."""
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
# SANDBOX COM DOCKER
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

    def run(self, code: str) -> Tuple[bool, str, float]:
        """Executa código no sandbox. Retorna (sucesso, stdout+stderr, tempo)"""
        if self.use_docker:
            return self._run_docker(code)
        else:
            return self._run_subprocess(code)

    def _run_docker(self, code: str) -> Tuple[bool, str, float]:
        with tempfile.TemporaryDirectory(dir=Config.SANDBOX_DIR) as tmpdir:
            script_path = Path(tmpdir) / "script.py"
            script_path.write_text(code)

            cmd = [
                "docker", "run", "--rm",
                "-v", f"{tmpdir}:/app",
                "-w", "/app",
                "python:3.10-slim",
                "python", "script.py"
            ]
            try:
                start = time.time()
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
                elapsed = time.time() - start
                success = proc.returncode == 0
                output = proc.stdout + proc.stderr
                return success, output, elapsed
            except subprocess.TimeoutExpired:
                return False, f"Timeout após {self.timeout}s", self.timeout
            except Exception as e:
                return False, str(e), 0

    def _run_subprocess(self, code: str) -> Tuple[bool, str, float]:
        import resource
        def set_limits():
            resource.setrlimit(resource.RLIMIT_CPU, (self.timeout, self.timeout))
            resource.setrlimit(resource.RLIMIT_AS, (100 * 1024 * 1024, 100 * 1024 * 1024))  # 100 MB

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            tmp_path = f.name

        try:
            start = time.time()
            proc = subprocess.run(
                [sys.executable, tmp_path],
                preexec_fn=set_limits,
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
# AVALIADOR COM TESTES AUTOMÁTICOS
# ============================================================================

class CodeEvaluator:
    def __init__(self, sandbox: Sandbox, kb: KnowledgeBase):
        self.sandbox = sandbox
        self.kb = kb
        self.original_code = None  # para comparação de testes

    def evaluate(self, code: str, original_code: str = None) -> Dict[str, Any]:
        """
        Avalia código com métricas e testes.
        Se original_code fornecido, gera testes comparando saídas.
        """
        result = {
            "valid": False,
            "syntax_error": None,
            "runtime_error": None,
            "execution_time": None,
            "lines": 0,
            "complexity": 0,
            "num_functions": 0,
            "comment_ratio": 0.0,
            "tests_passed": 0,
            "tests_total": 0,
            "score": 0.0
        }

        # Verifica sintaxe
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
        except Exception as e:
            pass

        # Execução em sandbox para medir tempo
        success, output, exec_time = self.sandbox.run(code)
        result["execution_time"] = exec_time
        if not success:
            result["runtime_error"] = output[:200]

        # Testes automáticos comparativos (se original fornecido)
        if original_code and success:
            # Gera entradas aleatórias para funções comuns
            test_results = self._run_comparative_tests(original_code, code)
            result["tests_passed"] = test_results["passed"]
            result["tests_total"] = test_results["total"]
        else:
            # Se não há original, considera que passou se executou sem erro
            result["tests_passed"] = 1 if success else 0
            result["tests_total"] = 1

        # Calcula score final
        score = self._compute_score(result)
        result["score"] = round(score, 2)

        return result

    def _run_comparative_tests(self, original: str, mutated: str) -> Dict:
        """
        Executa ambas as versões com as mesmas entradas e compara saídas.
        Para simplificar, assume que existe uma função 'main' sem argumentos ou
        tenta identificar funções com tipos simples.
        """
        # Estratégia: para cada função definida, gerar algumas chamadas com argumentos aleatórios
        # e comparar o retorno. Usaremos subprocessos separados.
        # Por simplicidade, vamos apenas executar o código e capturar a saída padrão,
        # assumindo que ele imprime algo determinístico.
        # Uma abordagem mais robusta seria usar um framework de testes, mas para este exemplo
        # faremos uma versão simples: se o código tiver uma função chamada 'test' que retorna bool, usamos.
        # Senão, executamos e comparamos stdout.

        passed = 0
        total = 1

        # Executa original e mutado com o mesmo ambiente
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f_orig:
            f_orig.write(original)
            orig_path = f_orig.name
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f_mut:
            f_mut.write(mutated)
            mut_path = f_mut.name

        try:
            # Executa original
            proc_orig = subprocess.run([sys.executable, orig_path], capture_output=True, text=True, timeout=2)
            out_orig = proc_orig.stdout

            # Executa mutado
            proc_mut = subprocess.run([sys.executable, mut_path], capture_output=True, text=True, timeout=2)
            out_mut = proc_mut.stdout

            if out_orig == out_mut:
                passed = 1
        except:
            pass
        finally:
            os.unlink(orig_path)
            os.unlink(mut_path)

        return {"passed": passed, "total": total}

    def _compute_score(self, metrics: Dict) -> float:
        """Combina métricas e testes num score 0-100."""
        base = 0.0
        # Se passou nos testes, ganha 60 pontos base
        if metrics["tests_total"] > 0 and metrics["tests_passed"] == metrics["tests_total"]:
            base = 60.0
        elif metrics["tests_passed"] > 0:
            base = 30.0 * (metrics["tests_passed"] / metrics["tests_total"])

        # Métricas de qualidade (até 40 pontos)
        quality = 0.0
        # Complexidade: quanto menor melhor (ideal <=5)
        comp = metrics.get("complexity", 10)
        if comp <= 3:
            quality += 15
        elif comp <= 5:
            quality += 10
        elif comp <= 10:
            quality += 5

        # Número de funções (ideal 5-10)
        nfunc = metrics.get("num_functions", 0)
        if 5 <= nfunc <= 10:
            quality += 10
        elif nfunc > 10:
            quality += 5
        elif nfunc > 0:
            quality += 2

        # Comentários (ideal >5% do código)
        if metrics.get("comment_ratio", 0) > 0.05:
            quality += 5

        # Tempo de execução (ideal <0.1s)
        if metrics.get("execution_time", 1.0) < 0.1:
            quality += 10

        return min(base + quality, 100.0)


# ============================================================================
# MUTAÇÕES REAIS USANDO AST
# ============================================================================

class MutationEngine:
    """Aplica mutações reais no código via transformação da AST."""

    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def mutate(self, code: str, mutation_type: str) -> Tuple[str, str]:
        """Retorna (código mutado, descrição)."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return code, "Erro de sintaxe, mutação ignorada"

        transformer = None
        desc = ""

        if mutation_type == "add_comment":
            # Inserir comentário aleatório (pós AST)
            return self._add_comment(code)
        elif mutation_type == "remove_line":
            return self._remove_line(code)
        elif mutation_type == "rename_var":
            transformer = RenameVarTransformer()
            desc = "Renomeação de variável"
        elif mutation_type == "swap_operator":
            transformer = SwapOperatorTransformer()
            desc = "Troca de operador"
        elif mutation_type == "extract_function":
            # Implementação real: extrai um bloco para nova função
            return self._extract_function(code)
        elif mutation_type == "inline_function":
            return self._inline_function(code)
        elif mutation_type == "simplify_expression":
            transformer = SimplifyExpressionTransformer()
            desc = "Simplificação de expressão"
        elif mutation_type == "add_docstring":
            transformer = AddDocstringTransformer()
            desc = "Adição de docstring"
        elif mutation_type == "insert_learned":
            return self._insert_learned_function(code)
        elif mutation_type == "loop_conversion":
            transformer = LoopConversionTransformer()
            desc = "Conversão de loop"
        else:
            return code, "Tipo de mutação desconhecido"

        if transformer:
            new_tree = transformer.visit(tree)
            try:
                new_code = astor.to_source(new_tree)
                return new_code, desc
            except:
                return code, f"Falha na {desc}"

        return code, "Mutação não implementada"

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
            "# Magic number, talvez extrair constante"
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

    def _extract_function(self, code: str) -> Tuple[str, str]:
        """Extrai um bloco de código para uma nova função."""
        try:
            tree = ast.parse(code)
            # Escolhe uma função aleatória
            functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
            if not functions:
                return code, "Nenhuma função para extrair"
            func = random.choice(functions)
            # Escolhe um bloco dentro da função (ex: um if, for, ou sequência de statements)
            # Para simplificar, vamos pegar um nó que não seja o último e que tenha corpo
            candidates = [n for n in ast.walk(func) if isinstance(n, (ast.If, ast.For, ast.While)) and n.body]
            if not candidates:
                return code, "Nenhum bloco candidato"
            block = random.choice(candidates)

            # Cria nova função com o corpo do bloco
            new_func_name = f"extracted_{random.randint(1000,9999)}"
            # Precisamos coletar variáveis usadas no bloco para torná-las parâmetros
            used_vars = set()
            for node in ast.walk(block):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    used_vars.add(node.id)
            # Remove builtins e parâmetros da função original
            params = [ast.arg(arg=v, annotation=None) for v in used_vars if v not in dir(__builtins__)]
            args = ast.arguments(args=params, vararg=None, kwarg=None, defaults=[])

            new_func = ast.FunctionDef(
                name=new_func_name,
                args=args,
                body=block.body,
                decorator_list=[],
                returns=None
            )

            # Substitui o bloco original por uma chamada à nova função
            call = ast.Expr(value=ast.Call(
                func=ast.Name(id=new_func_name, ctx=ast.Load()),
                args=[ast.Name(id=v, ctx=ast.Load()) for v in used_vars if v not in dir(__builtins__)],
                keywords=[]
            ))

            # Insere a nova função no módulo (fora de qualquer função)
            # Encontra o módulo e insere new_func no final
            for node in ast.walk(tree):
                if isinstance(node, ast.Module):
                    node.body.append(new_func)
                    break

            # Substitui o bloco no local original
            # Como é complexo, vamos apenas substituir o corpo do bloco pela chamada
            block.body = [call]

            new_code = astor.to_source(tree)
            return new_code, f"Função {new_func_name} extraída"
        except Exception as e:
            return code, f"Erro na extração: {e}"

    def _inline_function(self, code: str) -> Tuple[str, str]:
        """Inline de uma função curta (substitui chamada pelo corpo)."""
        # Implementação complexa; por ora, retorna original
        return code, "Inline function (não implementado)"

    def _insert_learned_function(self, code: str) -> Tuple[str, str]:
        """Insere uma função aprendida do GitHub no final do código."""
        func_data = self.kb.get_random_function()
        if not func_data:
            return code, "Nenhuma função aprendida"
        func_code, source = func_data
        new_code = code + f"\n\n# Função aprendida de {source}\n" + func_code
        return new_code, f"Função inserida de {source}"


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
    """Simplifica expressões algébricas básicas."""
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
        return node

class AddDocstringTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        if not ast.get_docstring(node):
            docstring = ast.Expr(value=ast.Constant(value="Função gerada/evoluída pela Atena."))
            node.body.insert(0, docstring)
        return node

class LoopConversionTransformer(ast.NodeTransformer):
    """Converte for em while e vice-versa quando possível."""
    def visit_For(self, node):
        # Converte for iter para while
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
            # for i in range(n): -> i=0; while i<n: ... i+=1
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
            # Cria nó de atribuição i = start
            assign = ast.Assign(targets=[ast.Name(id=node.target.id, ctx=ast.Store())], value=start)
            # Cria condição i < end
            test = ast.Compare(left=ast.Name(id=node.target.id, ctx=ast.Load()), ops=[ast.Lt()], comparators=[end])
            # Cria incremento i += step
            inc = ast.AugAssign(target=ast.Name(id=node.target.id, ctx=ast.Store()), op=ast.Add(), value=step)
            body = node.body + [inc]
            while_node = ast.While(test=test, body=body, orelse=[])
            return [assign, while_node]
        return node


# ============================================================================
# APRENDIZADO DO GITHUB COM EMBEDDINGS
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
        for page in range(1, 20):  # até 20 páginas
            repos = self._search_repositories(page=page, per_page=30)
            if not repos:
                break
            for repo in repos:
                self.queue.put(repo)
                self.processed_count += 1
                if self.processed_count >= 1000:  # limite razoável
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
            print(f"[⚠️] Erro na busca GitHub: {e}")
            return []

    def _process_repo(self, repo):
        repo_name = repo["full_name"]
        # Verifica se já processou
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
                        self.kb.add_function(func, f"github:{repo_name}/{file_info['path']}")
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
            print(f"[⚠️] NewsAPI: {e}")
            return []

    def update_objectives(self):
        articles = self.fetch_tech_news()
        if not articles:
            return
        text = " ".join([a.get("title", "") + " " + a.get("description", "") for a in articles])
        words = [w.lower() for w in text.split() if len(w) > 5 and w.isalpha()]
        from collections import Counter
        keywords = [w for w, _ in Counter(words).most_common(5)]
        for kw in keywords[:3]:
            # Cria objetivo temporário com peso baixo
            self.kb.conn.execute(
                "INSERT OR IGNORE INTO objectives (name, description, weight, current_value, target_value) VALUES (?, ?, ?, ?, ?)",
                (f"learn_{kw}", f"Aprender sobre {kw}", 0.3, 0.0, 1.0)
            )
            self.kb.conn.commit()


# ============================================================================
# PREDITOR DE MUTAÇÕES
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
                self.model = pickle.load(f)
                self.vectorizer = pickle.load(f)
            print("[✓] Modelo preditor carregado")

    def _save_model(self):
        with open(Config.PREDICTOR_MODEL, 'wb') as f:
            pickle.dump((self.model, self.vectorizer), f)

    def train(self):
        X_dict, y = self.kb.get_training_data()
        if len(X_dict) < Config.MIN_TRAINING_SAMPLES:
            print(f"[⚠️] Amostras insuficientes: {len(X_dict)} < {Config.MIN_TRAINING_SAMPLES}")
            return

        from sklearn.feature_extraction import DictVectorizer
        from sklearn.ensemble import RandomForestClassifier

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
        if not HAS_DOCKER_PY:
            print("[⚠️] docker-py não instalado. Tentando com CLI.")
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
        else:
            # Usar docker-py
            try:
                client = docker.from_env()
                image, logs = client.images.build(path=str(Config.DEPLOY_DIR), tag=Config.DEPLOY_DOCKER_IMAGE)
                client.images.push(Config.DEPLOY_DOCKER_IMAGE)
                print("[🐳] Deploy Docker (py) realizado")
                return True
            except Exception as e:
                print(f"[⚠️] Erro Docker-py: {e}")
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
# EVOLUÇÃO PRINCIPAL
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
        self.original_code = self.current_code  # referência para testes

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

        # Objetivos atuais
        objectives = self.kb.get_objectives()

        # Escolhe tipo de mutação baseado nos objetivos e preditor
        mutation_types = [
            "add_comment", "remove_line", "rename_var", "swap_operator",
            "extract_function", "simplify_expression", "add_docstring",
            "insert_learned", "loop_conversion"
        ]
        # Pesos iniciais
        weights = {mt: 1.0 for mt in mutation_types}
        # Ajustar por objetivos (exemplo: se quer reduzir complexidade, favorecer simplify_expression)
        for obj in objectives:
            if obj["name"] == "reduzir_complexidade" and obj["current"] > obj["target"]:
                weights["simplify_expression"] += 2.0
                weights["extract_function"] += 1.0
            if obj["name"] == "aumentar_modularidade":
                weights["extract_function"] += 2.0
                weights["insert_learned"] += 1.0
            if obj["name"] == "melhorar_documentacao":
                weights["add_docstring"] += 2.0
                weights["add_comment"] += 1.0

        # Preditor
        if self.predictor.model:
            for mt in mutation_types:
                # Extrair features do código atual
                feat = {
                    "lines": len(self.current_code.splitlines()),
                    "num_functions": self.current_code.count("def "),
                    "complexity": self.evaluator.evaluate(self.current_code).get("complexity", 5),
                    "mutation_type": mt
                }
                prob = self.predictor.predict_proba(feat)
                weights[mt] *= (0.5 + prob)  # entre 0.5 e 1.5

        # Escolhe mutação
        mtype = random.choices(list(weights.keys()), weights=list(weights.values()))[0]

        # Aplica mutação
        mutated, desc = self.mutation_engine.mutate(self.current_code, mtype)

        # Avalia
        metrics = self.evaluator.evaluate(mutated, original_code=self.original_code)
        new_score = metrics["score"]

        # Registra features para treino
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

        self.kb.record_evolution(self.generation, desc, self.best_score, new_score, replaced, features)

        # Atualiza objetivos com métricas atuais
        self.kb.update_objective("reduzir_complexidade", metrics["complexity"])
        self.kb.update_objective("aumentar_modularidade", metrics["num_functions"])
        self.kb.update_objective("melhorar_documentacao", metrics["comment_ratio"])
        self.kb.update_objective("reduzir_tempo_execucao", metrics.get("execution_time", 1.0))

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

    def start_autonomous(self):
        print("\n🚀 Modo autônomo iniciado. Pressione Ctrl+C para parar.")
        self.running = True
        if self.core.learner:
            self.core.learner.start()
        try:
            while self.running:
                # Ciclo de evolução
                result = self.core.evolve_one_cycle()

                # Treinamento periódico do preditor
                if time.time() - self.last_train_time > Config.TRAINING_INTERVAL:
                    self.core.predictor.train()
                    self.last_train_time = time.time()

                # Atualização de objetivos por notícias
                if self.core.news and time.time() - self.last_news_time > 3600:
                    self.core.news.update_objectives()
                    self.last_news_time = time.time()

                # Deploy se melhoria significativa
                if self.core.best_score > self.last_deploy_score * 1.05:
                    print("📈 Melhoria significativa! Acionando deploy...")
                    AutoDeploy.deploy()
                    self.last_deploy_score = self.core.best_score

                time.sleep(60)  # pausa entre ciclos
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
    parser.add_argument("--cycles", type=int, default=0, help="Número de ciclos a executar (0 = infinito)")
    args = parser.parse_args()

    app = AtenaApp()
    if args.auto:
        if args.cycles > 0:
            # Executa N ciclos e sai
            for i in range(args.cycles):
                app.core.evolve_one_cycle()
                if i < args.cycles - 1:
                    time.sleep(2)
        else:
            app.start_autonomous()
    else:
        app.run_interactive()
