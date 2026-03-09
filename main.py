#!/usr/bin/env python3
"""
ATENA Ω - Organismo Digital Autônomo com Múltiplas Fontes de Conhecimento
Versão: Ω.ULTRA.1.0
"""

import os
import json
import logging
import requests
import time
import subprocess
import random
import hashlib
import sqlite3
import threading
import re
import sys
import importlib.util
import inspect
import ast
import base64
import zlib
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import xml.etree.ElementTree as ET
from urllib.parse import quote, urlencode
import warnings
warnings.filterwarnings('ignore')

# Tentar importar bibliotecas opcionais
try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False

try:
    from bs4 import BeautifulSoup
    HAS_BEAUTIFULSOUP = True
except ImportError:
    HAS_BEAUTIFULSOUP = False

class AtenaOrganismo:
    """
    ATENA Ω - Organismo Digital Autônomo com Capacidade de:
    - Buscar conhecimento de múltiplas fontes (GitHub, Wikipedia, arXiv, etc.)
    - Auto-modificar seu próprio código baseado em aprendizado
    - Evoluir através de ciclos de vida autônomos
    - Persistir conhecimento em banco SQLite
    - Gerar relatórios inteligentes
    """
    
    def __init__(self):
        self.base_dir = Path.cwd()
        self.version = "Ω.ULTRA.1.0"
        self._setup_anatomia()
        load_dotenv()
        
        # APIs e Fontes de Conhecimento
        self.grok_key = os.getenv("GROK_API_KEY")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.wikipedia_api = "https://pt.wikipedia.org/api/rest_v1"
        self.arxiv_api = "http://export.arxiv.org/api/query"
        self.huggingface_api = "https://huggingface.co/api"
        self.pypi_api = "https://pypi.org/pypi"
        
        # Caminhos do Sistema
        self.estado_path = self.base_dir / "data/estado.json"
        self.memoria_path = self.base_dir / "data/memoria.db"
        self.dna_path = self.base_dir / "dna_history"
        self.knowledge_path = self.base_dir / "conhecimento"
        self.code_base_path = self.base_dir / "main.py"  # Próprio código
        
        # Estado do Organismo
        self.estado = self._carregar_estado_seguro()
        self.erros_do_ciclo = []
        self.aprendizados_do_ciclo = []
        self.start_time = time.time()
        
        # Cache e Memória
        self.cache = {}
        self.knowledge_base = {}
        
        # Inicializar sistemas
        self._init_memoria()
        self._carregar_conhecimento_base()
        
    def _setup_anatomia(self):
        """Cria estrutura completa do organismo."""
        pastas = [
            "data", "logs", "cache", "dna_history", "pensamentos",
            "modules/atena_autogen", "conhecimento", "backup",
            "knowledge/github", "knowledge/wikipedia", "knowledge/arxiv",
            "knowledge/pypi", "knowledge/huggingface", "knowledge/stackoverflow",
            "system/neural", "system/immune", "system/genetic",
            "evolutions/success", "evolutions/failed", "evolutions/experimental"
        ]
        for p in pastas:
            (self.base_dir / p).mkdir(parents=True, exist_ok=True)
        
        # Configurar logging avançado
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | Ω[%(levelname)s] | %(filename)s:%(lineno)d | %(message)s',
            handlers=[
                logging.FileHandler(self.base_dir / f"logs/atena_{datetime.now():%Y%m%d}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"🔱 ATENA Ω {self.version} iniciada")

    def _init_memoria(self):
        """Inicializa banco de dados de conhecimento."""
        conn = sqlite3.connect(self.memoria_path)
        cursor = conn.cursor()
        
        # Tabela de conhecimento geral
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conhecimento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fonte TEXT,
                titulo TEXT,
                conteudo TEXT,
                url TEXT,
                data_coleta DATETIME DEFAULT CURRENT_TIMESTAMP,
                relevancia REAL DEFAULT 0.5,
                vezes_acessado INTEGER DEFAULT 0,
                hash_conteudo TEXT UNIQUE
            )
        ''')
        
        # Tabela de padrões de código
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS code_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                padrao TEXT,
                descricao TEXT,
                exemplo TEXT,
                eficacia REAL DEFAULT 0.5,
                vezes_usado INTEGER DEFAULT 0,
                tags TEXT
            )
        ''')
        
        # Tabela de mutações bem-sucedidas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mutacoes_sucesso (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_original TEXT,
                codigo_mutado TEXT,
                diff TEXT,
                melhoria_percent REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de fontes de conhecimento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fontes_conhecimento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE,
                url_base TEXT,
                ultima_coleta DATETIME,
                total_itens INTEGER DEFAULT 0,
                ativa BOOLEAN DEFAULT 1
            )
        ''')
        
        # Inserir fontes padrão
        fontes_padrao = [
            ("GitHub Trending", "https://github.com/trending", None, 0, 1),
            ("Wikipedia PT", "https://pt.wikipedia.org", None, 0, 1),
            ("arXiv CS", "https://arxiv.org/list/cs/recent", None, 0, 1),
            ("PyPI Popular", "https://pypi.org", None, 0, 1),
            ("HuggingFace Models", "https://huggingface.co/models", None, 0, 1),
        ]
        
        for fonte in fontes_padrao:
            cursor.execute('''
                INSERT OR IGNORE INTO fontes_conhecimento (nome, url_base, ultima_coleta, total_itens, ativa)
                VALUES (?, ?, ?, ?, ?)
            ''', fonte)
        
        conn.commit()
        conn.close()

    def _carregar_estado_seguro(self) -> Dict:
        """Carrega estado com validação e recuperação."""
        padrao = {
            "ciclo": 0,
            "geracao": 1,
            "falhas_corrigidas": 0,
            "scripts_gerados": 0,
            "evolucoes": 0,
            "auto_modificacoes": 0,
            "conhecimentos_adquiridos": 0,
            "fontes_consultadas": 0,
            "versao_dna": "1.0.0",
            "ultimo_checkpoint": None,
            "tempo_total_ativo": 0,
            "dna_ancestral": [],
            "metricas_saude": {
                "performance": 1.0,
                "estabilidade": 1.0,
                "adaptabilidade": 1.0,
                "inteligencia": 0.7,
                "curiosidade": 0.9
            },
            "preferencias_aprendizado": {
                "fontes_ativas": ["github", "wikipedia", "arxiv", "pypi"],
                "profundidade_busca": 3,
                "taxa_mutacao": 0.3,
                "curiosidade": 0.8
            }
        }
        
        if self.estado_path.exists():
            try:
                with open(self.estado_path, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                    if not conteudo.strip():
                        return padrao
                    data = json.loads(conteudo)
                    # Merge com valores padrão
                    for k, v in padrao.items():
                        if k not in data:
                            data[k] = v
                    return data
            except Exception as e:
                self.logger.error(f"Erro ao carregar estado: {e}")
                self._backup_estado_corrompido()
        return padrao

    def _backup_estado_corrompido(self):
        """Faz backup de estado corrompido."""
        if self.estado_path.exists():
            backup = self.base_dir / f"backup/estado_corrompido_{datetime.now():%Y%m%d_%H%M%S}.json"
            self.estado_path.rename(backup)
            self.logger.info(f"Backup criado: {backup}")

    def _carregar_conhecimento_base(self):
        """Carrega conhecimento base do banco SQLite."""
        try:
            conn = sqlite3.connect(self.memoria_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT fonte, titulo, conteudo, relevancia 
                FROM conhecimento 
                ORDER BY relevancia DESC 
                LIMIT 100
            ''')
            
            for row in cursor.fetchall():
                fonte, titulo, conteudo, relevancia = row
                if fonte not in self.knowledge_base:
                    self.knowledge_base[fonte] = []
                self.knowledge_base[fonte].append({
                    "titulo": titulo,
                    "conteudo": conteudo[:200],  # Resumo
                    "relevancia": relevancia
                })
            
            conn.close()
            self.logger.info(f"📚 Conhecimento base carregado: {sum(len(v) for v in self.knowledge_base.values())} itens")
        except Exception as e:
            self.logger.error(f"Erro ao carregar conhecimento: {e}")

    # ==================== SISTEMAS DE BUSCA DE CONHECIMENTO ====================

    def buscar_conhecimento_multifontes(self) -> List[Dict]:
        """Busca conhecimento de todas as fontes configuradas em paralelo."""
        resultados = []
        fontes_ativas = self.estado["preferencias_aprendizado"]["fontes_ativas"]
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            
            if "github" in fontes_ativas:
                futures.append(executor.submit(self._buscar_github_trending))
            if "wikipedia" in fontes_ativas:
                futures.append(executor.submit(self._buscar_wikipedia, "inteligência artificial"))
                futures.append(executor.submit(self._buscar_wikipedia, "aprendizado de máquina"))
            if "arxiv" in fontes_ativas:
                futures.append(executor.submit(self._buscar_arxiv, "cs.AI"))
                futures.append(executor.submit(self._buscar_arxiv, "cs.LG"))
            if "pypi" in fontes_ativas:
                futures.append(executor.submit(self._buscar_pypi_populares))
            if "stackoverflow" in fontes_ativas and HAS_BEAUTIFULSOUP:
                futures.append(executor.submit(self._buscar_stackoverflow, "python"))
            
            for future in as_completed(futures):
                try:
                    resultado = future.result(timeout=10)
                    if resultado:
                        resultados.extend(resultado)
                        self.estado["fontes_consultadas"] += 1
                except Exception as e:
                    self.logger.error(f"Erro em busca paralela: {e}")
        
        self.logger.info(f"🌐 Busca multifontes concluída: {len(resultados)} novos conhecimentos")
        return resultados

    def _buscar_github_trending(self) -> List[Dict]:
        """Busca repositórios trending no GitHub."""
        resultados = []
        try:
            headers = {}
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"
            
            # Buscar trending de hoje
            url = "https://api.github.com/search/repositories"
            params = {
                "q": "stars:>100",
                "sort": "stars",
                "order": "desc",
                "per_page": 10
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for repo in data.get("items", []):
                    conhecimento = {
                        "fonte": "github",
                        "titulo": f"GitHub: {repo['name']}",
                        "conteudo": f"Repositório: {repo['full_name']}\nDescrição: {repo['description']}\nStars: {repo['stargazers_count']}\nLinguagem: {repo.get('language', 'N/A')}",
                        "url": repo['html_url'],
                        "relevancia": min(1.0, repo['stargazers_count'] / 10000)
                    }
                    resultados.append(conhecimento)
                    self._salvar_conhecimento(conhecimento)
            
            self.logger.info(f"GitHub: {len(resultados)} repositórios encontrados")
        except Exception as e:
            self.logger.error(f"Erro ao buscar GitHub: {e}")
        
        return resultados

    def _buscar_wikipedia(self, termo: str) -> List[Dict]:
        """Busca artigos na Wikipedia."""
        resultados = []
        try:
            # Buscar artigo
            url = f"{self.wikipedia_api}/page/summary/{quote(termo)}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                conhecimento = {
                    "fonte": "wikipedia",
                    "titulo": f"Wikipedia: {data.get('title', termo)}",
                    "conteudo": data.get('extract', '')[:500],
                    "url": data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                    "relevancia": 0.7
                }
                resultados.append(conhecimento)
                self._salvar_conhecimento(conhecimento)
            
            self.logger.info(f"Wikipedia: {len(resultados)} artigos encontrados")
        except Exception as e:
            self.logger.error(f"Erro ao buscar Wikipedia: {e}")
        
        return resultados

    def _buscar_arxiv(self, categoria: str) -> List[Dict]:
        """Busca artigos recentes no arXiv."""
        resultados = []
        try:
            params = {
                "search_query": f"cat:{categoria}",
                "sortBy": "submittedDate",
                "sortOrder": "descending",
                "max_results": 5
            }
            
            response = requests.get(self.arxiv_api, params=params, timeout=15)
            
            if response.status_code == 200 and HAS_FEEDPARSER:
                feed = feedparser.parse(response.text)
                for entry in feed.entries[:5]:
                    conhecimento = {
                        "fonte": "arxiv",
                        "titulo": f"arXiv: {entry.title}",
                        "conteudo": entry.summary[:500],
                        "url": entry.link,
                        "relevancia": 0.8
                    }
                    resultados.append(conhecimento)
                    self._salvar_conhecimento(conhecimento)
            
            self.logger.info(f"arXiv: {len(resultados)} artigos encontrados")
        except Exception as e:
            self.logger.error(f"Erro ao buscar arXiv: {e}")
        
        return resultados

    def _buscar_pypi_populares(self) -> List[Dict]:
        """Busca pacotes populares no PyPI."""
        resultados = []
        try:
            # Pacotes populares para buscar
            pacotes = ["requests", "numpy", "pandas", "flask", "django", "fastapi", "pytorch", "tensorflow"]
            
            for pacote in pacotes[:3]:  # Limitar para não sobrecarregar
                url = f"{self.pypi_api}/{pacote}/json"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    info = data.get('info', {})
                    
                    conhecimento = {
                        "fonte": "pypi",
                        "titulo": f"PyPI: {pacote}",
                        "conteudo": f"Pacote: {pacote}\nVersão: {info.get('version', 'N/A')}\nDescrição: {info.get('summary', '')[:300]}",
                        "url": info.get('package_url', ''),
                        "relevancia": 0.6
                    }
                    resultados.append(conhecimento)
                    self._salvar_conhecimento(conhecimento)
            
            self.logger.info(f"PyPI: {len(resultados)} pacotes encontrados")
        except Exception as e:
            self.logger.error(f"Erro ao buscar PyPI: {e}")
        
        return resultados

    def _buscar_stackoverflow(self, tag: str) -> List[Dict]:
        """Busca perguntas populares no StackOverflow."""
        if not HAS_BEAUTIFULSOUP:
            return []
        
        resultados = []
        try:
            url = f"https://api.stackexchange.com/2.3/questions"
            params = {
                "order": "desc",
                "sort": "votes",
                "tagged": tag,
                "site": "stackoverflow",
                "pagesize": 5
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for item in data.get("items", []):
                    conhecimento = {
                        "fonte": "stackoverflow",
                        "titulo": f"StackOverflow: {item['title']}",
                        "conteudo": f"Tags: {', '.join(item.get('tags', []))}\nRespostas: {item.get('answer_count', 0)}\nScore: {item.get('score', 0)}",
                        "url": item.get('link', ''),
                        "relevancia": min(1.0, item.get('score', 0) / 100)
                    }
                    resultados.append(conhecimento)
                    self._salvar_conhecimento(conhecimento)
            
            self.logger.info(f"StackOverflow: {len(resultados)} perguntas encontradas")
        except Exception as e:
            self.logger.error(f"Erro ao buscar StackOverflow: {e}")
        
        return resultados

    def _salvar_conhecimento(self, conhecimento: Dict):
        """Salva conhecimento no banco SQLite."""
        try:
            conn = sqlite3.connect(self.memoria_path)
            cursor = conn.cursor()
            
            # Gerar hash único
            conteudo_str = conhecimento['titulo'] + conhecimento['conteudo']
            hash_conteudo = hashlib.sha256(conteudo_str.encode()).hexdigest()
            
            cursor.execute('''
                INSERT OR IGNORE INTO conhecimento 
                (fonte, titulo, conteudo, url, relevancia, hash_conteudo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                conhecimento['fonte'],
                conhecimento['titulo'],
                conhecimento['conteudo'],
                conhecimento.get('url', ''),
                conhecimento['relevancia'],
                hash_conteudo
            ))
            
            conn.commit()
            conn.close()
            
            self.estado["conhecimentos_adquiridos"] += 1
        except Exception as e:
            self.logger.error(f"Erro ao salvar conhecimento: {e}")

    # ==================== SISTEMA DE AUTO-MODIFICAÇÃO DE CÓDIGO ====================

    def analisar_e_mutar_codigo(self) -> bool:
        """Analisa e modifica o próprio código baseado em conhecimento adquirido."""
        try:
            # Ler código atual
            codigo_atual = self.code_base_path.read_text(encoding='utf-8')
            
            # Buscar padrões de melhoria
            padroes = self._buscar_padroes_melhoria()
            
            if not padroes:
                self.logger.info("Nenhum padrão de melhoria encontrado")
                return False
            
            # Selecionar melhoria aleatória baseada em relevância
            melhoria = random.choice(padroes)
            
            # Aplicar mutação
            novo_codigo = self._aplicar_mutacao(codigo_atual, melhoria)
            
            if novo_codigo and novo_codigo != codigo_atual:
                # Validar código mutado
                if self._validar_codigo(novo_codigo):
                    # Fazer backup
                    self._backup_codigo_original(codigo_atual)
                    
                    # Salvar nova versão
                    self.code_base_path.write_text(novo_codigo, encoding='utf-8')
                    
                    self.logger.info(f"🧬 Auto-modificação aplicada: {melhoria['descricao']}")
                    self.estado["auto_modificacoes"] += 1
                    
                    # Registrar mutação
                    self._registrar_mutacao(codigo_atual, novo_codigo, melhoria)
                    
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Erro na auto-modificação: {e}")
            return False

    def _buscar_padroes_melhoria(self) -> List[Dict]:
        """Busca padrões de melhoria do conhecimento adquirido."""
        padroes = []
        
        try:
            conn = sqlite3.connect(self.memoria_path)
            cursor = conn.cursor()
            
            # Buscar padrões de código do conhecimento
            cursor.execute('''
                SELECT conteudo, relevancia, fonte 
                FROM conhecimento 
                WHERE (fonte = 'github' OR fonte = 'stackoverflow')
                AND relevancia > 0.5
                ORDER BY relevancia DESC
                LIMIT 10
            ''')
            
            for row in cursor.fetchall():
                conteudo, relevancia, fonte = row
                
                # Extrair possíveis padrões de código
                if '```python' in conteudo:
                    # Extrair código de exemplos
                    codigo = re.search(r'```python\n(.*?)\n```', conteudo, re.DOTALL)
                    if codigo:
                        padroes.append({
                            "tipo": "exemplo_codigo",
                            "descricao": f"Padrão de {fonte}",
                            "codigo": codigo.group(1),
                            "relevancia": relevancia
                        })
            
            conn.close()
            
            # Adicionar padrões pré-definidos
            padroes.extend([
                {
                    "tipo": "otimizacao",
                    "descricao": "Adicionar tratamento de erros",
                    "padrao": r'try:.*?except:',
                    "relevancia": 0.8
                },
                {
                    "tipo": "performance",
                    "descricao": "Usar list comprehension",
                    "padrao": r'for.*?in.*?:.*?append',
                    "relevancia": 0.7
                },
                {
                    "tipo": "documentacao",
                    "descricao": "Adicionar docstrings",
                    "padrao": r'def .*?:.*?(?!""")',
                    "relevancia": 0.6
                }
            ])
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar padrões: {e}")
        
        return padroes

    def _aplicar_mutacao(self, codigo: str, melhoria: Dict) -> Optional[str]:
        """Aplica mutação no código baseada no padrão."""
        try:
            if melhoria["tipo"] == "exemplo_codigo" and "codigo" in melhoria:
                # Incorporar código de exemplo
                novo_codigo = codigo + f"\n\n# Auto-gerado de {melhoria['descricao']}\n"
                novo_codigo += melhoria["codigo"]
                return novo_codigo
            
            elif melhoria["tipo"] == "otimizacao":
                # Adicionar tratamento de erros em blocos perigosos
                linhas = codigo.split('\n')
                novo_linhas = []
                
                for linha in linhas:
                    novo_linhas.append(linha)
                    if 'open(' in linha or 'requests.' in linha:
                        indent = ' ' * (len(linha) - len(linha.lstrip()))
                        novo_linhas.append(f"{indent}    try:")
                        novo_linhas.append(f"{indent}        # Operação já implementada")
                        novo_linhas.append(f"{indent}    except Exception as e:")
                        novo_linhas.append(f"{indent}        logging.error(f'Erro: {{e}}')")
                
                return '\n'.join(novo_linhas)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Erro na mutação: {e}")
            return None

    def _validar_codigo(self, codigo: str) -> bool:
        """Valida sintaxe do código mutado."""
        try:
            ast.parse(codigo)
            return True
        except SyntaxError as e:
            self.logger.error(f"Erro de sintaxe na mutação: {e}")
            return False

    def _backup_codigo_original(self, codigo: str):
        """Faz backup do código original antes da mutação."""
        backup_path = self.base_dir / f"backup/main_backup_{datetime.now():%Y%m%d_%H%M%S}.py"
        backup_path.write_text(codigo, encoding='utf-8')
        self.logger.info(f"Backup do código original salvo em {backup_path}")

    def _registrar_mutacao(self, codigo_original: str, codigo_novo: str, melhoria: Dict):
        """Registra mutação no banco de dados."""
        try:
            conn = sqlite3.connect(self.memoria_path)
            cursor = conn.cursor()
            
            # Calcular diff simples
            diff = f"Antes: {len(codigo_original)} chars, Depois: {len(codigo_novo)} chars"
            
            cursor.execute('''
                INSERT INTO mutacoes_sucesso 
                (codigo_original, codigo_mutado, diff, melhoria_percent)
                VALUES (?, ?, ?, ?)
            ''', (
                codigo_original[:500],  # Apenas início
                codigo_novo[:500],
                diff,
                melhoria.get('relevancia', 0.5)
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Erro ao registrar mutação: {e}")

    # ==================== SISTEMA DE EVOLUÇÃO COM IA ====================

    def auto_mutacao_inteligente(self) -> str:
        """Evolução usando IA com contexto do conhecimento adquirido."""
        if not self.grok_key:
            self.logger.error("Chave Grok não encontrada!")
            return self._gerar_codigo_emergencia()
        
        headers = {
            "Authorization": f"Bearer {self.grok_key}",
            "Content-Type": "application/json"
        }
        
        # Preparar contexto rico
        contexto = self._preparar_contexto_evolucao()
        
        # Decidir modo de evolução
        if self.erros_do_ciclo:
            prompt = self._criar_prompt_reparo(contexto)
            modo = "reparo"
        else:
            prompt = self._criar_prompt_evolucao_avancada(contexto)
            modo = "evolucao"
        
        try:
            self.logger.info(f"🤖 Consultando Grok API (modo: {modo})...")
            
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json={
                    "model": "grok-beta",
                    "messages": [
                        {"role": "system", "content": "Você é ATENA Ω, um organismo digital autônomo em evolução constante. Você tem acesso a múltiplas fontes de conhecimento e busca sempre melhorar seu código."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.8 if modo == "evolucao" else 0.3,
                    "max_tokens": 800
                },
                timeout=30
            )
            
            if response.status_code != 200:
                self.logger.error(f"Erro na API: {response.status_code}")
                if response.status_code == 401:
                    self.logger.error("Chave API inválida ou expirada")
                return self._gerar_codigo_emergencia()
            
            result = response.json()
            resposta = result['choices'][0]['message']['content']
            
            # Extrair e processar código
            codigo = self._extrair_codigo_avancado(resposta)
            
            if not codigo or len(codigo) < 20:
                self.logger.warning("Código gerado é muito curto")
                return self._gerar_codigo_emergencia()
            
            # Validar código
            if self._validar_codigo(codigo):
                return self._salvar_codigo_evolucao(codigo, modo, contexto)
            else:
                return self._gerar_codigo_emergencia()
            
        except requests.exceptions.Timeout:
            self.logger.error("Timeout na requisição à API")
            return self._gerar_codigo_emergencia()
        except Exception as e:
            self.logger.error(f"Erro na evolução: {e}")
            return self._gerar_codigo_emergencia()

    def _preparar_contexto_evolucao(self) -> Dict:
        """Prepara contexto rico para evolução."""
        contexto = {
            "ciclo": self.estado["ciclo"],
            "geracao": self.estado["geracao"],
            "metricas": self.estado["metricas_saude"],
            "estatisticas": {
                "scripts_gerados": self.estado["scripts_gerados"],
                "evolucoes": self.estado["evolucoes"],
                "auto_modificacoes": self.estado["auto_modificacoes"],
                "conhecimentos": self.estado["conhecimentos_adquiridos"]
            },
            "conhecimento_recente": []
        }
        
        # Buscar conhecimento recente
        try:
            conn = sqlite3.connect(self.memoria_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT fonte, titulo, conteudo 
                FROM conhecimento 
                ORDER BY data_coleta DESC 
                LIMIT 5
            ''')
            
            for row in cursor.fetchall():
                contexto["conhecimento_recente"].append({
                    "fonte": row[0],
                    "titulo": row[1],
                    "resumo": row[2][:200]
                })
            
            conn.close()
        except Exception as e:
            self.logger.error(f"Erro ao buscar conhecimento recente: {e}")
        
        return contexto

    def _criar_prompt_evolucao_avancada(self, contexto: Dict) -> str:
        """Cria prompt avançado para evolução."""
        
        # Lista de tópicos para evolução
        topicos = [
            "machine learning", "otimização de código", "análise de dados",
            "processamento de linguagem natural", "visão computacional",
            "redes neurais", "algoritmos genéticos", "sistemas distribuídos",
            "criptografia", "compressão de dados", "paralelismo",
            "aprendizado por reforço", "sistemas especialistas"
        ]
        
        topico = random.choice(topicos)
        
        prompt = f"""ATENA Ω - MODO EVOLUÇÃO AVANÇADA
Ciclo: {contexto['ciclo']}
Geração: {contexto['geracao']}

CONTEXTO ATUAL:
- Saúde do sistema: {contexto['metricas']}
- Conhecimentos adquiridos: {contexto['estatisticas']['conhecimentos']}
- Evoluções realizadas: {contexto['estatisticas']['evolucoes']}

CONHECIMENTO RECENTE:
"""
        
        for item in contexto["conhecimento_recente"][:3]:
            prompt += f"\n- [{item['fonte']}] {item['titulo']}"
        
        prompt += f"""

OBJETIVO DE EVOLUÇÃO:
Criar um script Python inovador sobre {topico} que possa ser integrado ao organismo.

REQUISITOS:
1. O código deve ser auto-contido e executável
2. Máximo 30 linhas
3. Incluir docstring explicativa
4. Utilizar boas práticas de programação
5. Ser inovador e útil para um organismo digital

INSTRUÇÃO:
Gere APENAS o código Python, sem explicações adicionais.
"""
        return prompt

    def _criar_prompt_reparo(self, contexto: Dict) -> str:
        """Cria prompt para reparo de código."""
        erro = self.erros_do_ciclo[0]
        
        prompt = f"""ATENA Ω - MODO REPARO
Ciclo: {contexto['ciclo']}

ERRO DETECTADO:
Arquivo: {erro['file']}
Mensagem: {erro['msg']}

CONTEXTO:
- Scripts gerados: {contexto['estatisticas']['scripts_gerados']}
- Reparos anteriores: {self.estado['falhas_corrigidas']}

INSTRUÇÃO:
Gere a correção para este erro em Python.
O código corrigido deve:
1. Ser funcional
2. Incluir tratamento de erros adequado
3. Manter compatibilidade
4. Máximo 25 linhas

APENAS O CÓDIGO CORRIGIDO.
"""
        return prompt

    def _extrair_codigo_avancado(self, resposta: str) -> str:
        """Extrai código Python com detecção avançada."""
        # Padrões de código
        padroes = [
            r'```python\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'```(.*?)```',
            r'(def [a-zA-Z_][a-zA-Z0-9_]*\(.*\):.*?)(?=\n\S|\Z)',
            r'(class [a-zA-Z_][a-zA-Z0-9_]*:.*?)(?=\n\S|\Z)',
        ]
        
        for padrao in padroes:
            matches = re.findall(padrao, resposta, re.DOTALL)
            if matches:
                return matches[0].strip()
        
        # Se não encontrar, tenta extrair linhas que parecem código
        linhas_codigo = []
        dentro_codigo = False
        
        for linha in resposta.split('\n'):
            linha = linha.rstrip()
            if linha.startswith(('def ', 'class ', 'import ', 'from ', '@', 'if __name__')):
                linhas_codigo.append(linha)
                dentro_codigo = True
            elif dentro_codigo and linha and not linha.startswith('#'):
                linhas_codigo.append(linha)
            elif dentro_codigo and not linha:
                linhas_codigo.append('')
        
        return '\n'.join(linhas_codigo) if linhas_codigo else ""

    def _salvar_codigo_evolucao(self, codigo: str, modo: str, contexto: Dict) -> str:
        """Salva código evoluído com metadados."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Adicionar cabeçalho rico
        cabecalho = f'''#!/usr/bin/env python3
"""
ATENA Ω - Código Auto-evoluído
Modo: {modo}
Ciclo: {contexto["ciclo"]}
Geração: {contexto["geracao"]}
Timestamp: {timestamp}
"""

'''
        codigo_completo = cabecalho + codigo
        
        # Gerar nome do arquivo
        if modo == "reparo" and self.erros_do_ciclo:
            nome_base = self.erros_do_ciclo[0]['file'].replace('.py', '')
            nome_arquivo = f"{nome_base}_reparado_{timestamp}.py"
            self.estado["falhas_corrigidas"] += 1
            pasta = "evolutions/success"
        else:
            # Decidir se é experimental ou sucesso
            if random.random() < 0.3:  # 30% de chance de ser experimental
                nome_arquivo = f"experimental_c{contexto['ciclo']}_{timestamp}.py"
                pasta = "evolutions/experimental"
            else:
                nome_arquivo = f"evolucao_c{contexto['ciclo']}_{timestamp}.py"
                pasta = "evolutions/success"
                self.estado["scripts_gerados"] += 1
                self.estado["evolucoes"] += 1
        
        # Salvar arquivo
        caminho = self.base_dir / f"{pasta}/{nome_arquivo}"
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(codigo_completo, encoding='utf-8')
        
        self.logger.info(f"🧬 Código salvo: {nome_arquivo}")
        
        return codigo[:300]  # Resumo para relatório

    def _gerar_codigo_emergencia(self) -> str:
        """Gera código de emergência inteligente."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Gerar código baseado no contexto
        if self.erros_do_ciclo:
            # Modo sobrevivência com diagnóstico
            codigo = f'''#!/usr/bin/env python3
"""
ATENA Ω - Módulo de Diagnóstico e Sobrevivência
Gerado em: {timestamp}
Ciclo: {self.estado["ciclo"]}
"""

import logging
import sys
import os
from datetime import datetime

def diagnosticar_sistema():
    """Diagnostica o estado do sistema."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("🔍 Iniciando diagnóstico...")
    
    # Verificar diretórios
    diretorios = ["data", "logs", "cache", "modules/atena_autogen"]
    for dir_name in diretorios:
        path = Path(dir_name)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Diretório criado: {{dir_name}}")
    
    # Verificar arquivos críticos
    arquivos = ["data/estado.json", ".env"]
    for arquivo in arquivos:
        path = Path(arquivo)
        if not path.exists():
            logger.warning(f"Arquivo não encontrado: {{arquivo}}")
    
    logger.info("✅ Diagnóstico concluído")
    return True

def coletar_metricas():
    """Coleta métricas básicas do sistema."""
    metricas = {{
        "timestamp": datetime.now().isoformat(),
        "ciclo": {self.estado["ciclo"]},
        "python_version": sys.version,
        "cwd": str(Path.cwd())
    }}
    return metricas

if __name__ == "__main__":
    diagnosticar_sistema()
    metricas = coletar_metricas()
    print(f"MÉTRICAS: {{metricas}}")
'''
        else:
            # Modo exploração
            codigo = f'''#!/usr/bin/env python3
"""
ATENA Ω - Módulo de Exploração de Conhecimento
Gerado em: {timestamp}
"""

import requests
import json
import logging
from datetime import datetime

def explorar_conhecimento():
    """Explora fontes de conhecimento disponíveis."""
    logger = logging.getLogger(__name__)
    
    fontes = [
        {{"nome": "GitHub", "url": "https://api.github.com/zen"}},
        {{"nome": "Wikipedia", "url": "https://pt.wikipedia.org/api/rest_v1/page/random/summary"}},
    ]
    
    resultados = []
    for fonte in fontes:
        try:
            response = requests.get(fonte["url"], timeout=5)
            if response.status_code == 200:
                logger.info(f"✅ Fonte acessível: {{fonte['nome']}}")
                resultados.append({{"fonte": fonte["nome"], "status": "ok"}})
            else:
                logger.warning(f"⚠️ Fonte com problema: {{fonte['nome']}}")
        except Exception as e:
            logger.error(f"❌ Erro ao acessar {{fonte['nome']}}: {{e}}")
    
    return resultados

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    resultados = explorar_conhecimento()
    print(f"RESULTADOS: {{resultados}}")
'''
        
        return codigo

    # ==================== SISTEMA DE EXECUÇÃO E DIAGNÓSTICO ====================

    async def executar_e_diagnosticar(self):
        """Executa scripts com diagnóstico avançado."""
        pastas = [
            self.base_dir / "evolutions/success",
            self.base_dir / "evolutions/experimental",
            self.base_dir / "modules/atena_autogen"
        ]
        
        for pasta in pastas:
            if not pasta.exists():
                continue
                
            scripts = list(pasta.glob("*.py"))
            
            for script in scripts:
                try:
                    self.logger.info(f"🚀 Executando: {script.relative_to(self.base_dir)}")
                    
                    # Executar em processo separado
                    result = subprocess.run(
                        [sys.executable, str(script)],
                        capture_output=True,
                        text=True,
                        timeout=30,
                        env=os.environ.copy()
                    )
                    
                    if result.returncode == 0:
                        self.logger.info(f"✅ {script.name} executado com sucesso")
                        
                        # Extrair aprendizados da saída
                        if "APRENDIZADO:" in result.stdout:
                            self._extrair_aprendizados_stdout(result.stdout, script.name)
                    else:
                        erro = {
                            "file": str(script.relative_to(self.base_dir)),
                            "msg": result.stderr[:300],
                            "returncode": result.returncode,
                            "timestamp": datetime.now().isoformat()
                        }
                        self.erros_do_ciclo.append(erro)
                        self.logger.error(f"❌ Erro em {script.name}: {result.stderr[:100]}")
                        
                        # Mover para pasta de falhas se for experimental
                        if "experimental" in str(script):
                            destino = self.base_dir / f"evolutions/failed/{script.name}"
                            destino.parent.mkdir(exist_ok=True)
                            script.rename(destino)
                            
                except subprocess.TimeoutExpired:
                    self.erros_do_ciclo.append({
                        "file": script.name,
                        "msg": "Timeout (30s)",
                        "tipo": "timeout"
                    })
                except Exception as e:
                    self.erros_do_ciclo.append({
                        "file": script.name,
                        "msg": str(e),
                        "tipo": "exception"
                    })

    def _extrair_aprendizados_stdout(self, stdout: str, script_name: str):
        """Extrai aprendizados da saída padrão."""
        padroes = [
            r'APRENDIZADO:\s*(.+?)(?:\n|$)',
            r'RESULTADO:\s*(.+?)(?:\n|$)',
            r'MÉTRICAS:\s*(.+?)(?:\n|$)'
        ]
        
        for padrao in padroes:
            matches = re.findall(padrao, stdout, re.IGNORECASE)
            for match in matches:
                self.aprendizados_do_ciclo.append({
                    "fonte": script_name,
                    "conteudo": match.strip(),
                    "timestamp": datetime.now().isoformat()
                })

    # ==================== GERADOR DE RELATÓRIOS INTELIGENTES ====================

    def gerar_relatorio_inteligente(self) -> str:
        """Gera relatório detalhado com análises."""
        ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Coletar dados
        ciclo = self.estado.get('ciclo', 0)
        geracao = self.estado.get('geracao', 1)
        metricas = self.estado.get('metricas_saude', {})
        preferencias = self.estado.get('preferencias_aprendizado', {})
        
        # Buscar estatísticas do banco
        stats = self._buscar_estatisticas_banco()
        
        # Construir relatório
        relatorio = []
        relatorio.append(f"# 🔱 ATENA Ω {self.version} - Relatório de Evolução\n")
        relatorio.append(f"## Ciclo {ciclo} | Geração {geracao}")
        relatorio.append(f"**Sincronização:** {ts}\n")
        
        relatorio.append("### 📊 Estatísticas Vitais")
        relatorio.append(f"- **Módulos Criados:** {self.estado.get('scripts_gerados', 0)}")
        relatorio.append(f"- **Auto-Reparos:** {self.estado.get('falhas_corrigidas', 0)}")
        relatorio.append(f"- **Evoluções:** {self.estado.get('evolucoes', 0)}")
        relatorio.append(f"- **Auto-modificações:** {self.estado.get('auto_modificacoes', 0)}")
        relatorio.append(f"- **Conhecimentos Adquiridos:** {self.estado.get('conhecimentos_adquiridos', 0)}")
        relatorio.append(f"- **Fontes Consultadas:** {self.estado.get('fontes_consultadas', 0)}\n")
        
        relatorio.append("### 🏥 Estado de Saúde")
        for nome, valor in metricas.items():
            relatorio.append(f"- **{nome.capitalize()}:** {valor*100:.1f}%")
        relatorio.append("")
        
        relatorio.append("### 📚 Conhecimento por Fonte")
        for fonte, qtd in stats.get('por_fonte', {}).items():
            relatorio.append(f"- **{fonte.capitalize()}:** {qtd} itens")
        relatorio.append("")
        
        relatorio.append("### 🧠 Últimos Aprendizados")
        for item in self.aprendizados_do_ciclo[-3:]:
            relatorio.append(f"- {item['fonte']}: {item['conteudo'][:100]}...")
        relatorio.append("")
        
        if self.erros_do_ciclo:
            relatorio.append("### ⚠️ Erros do Ciclo")
            for erro in self.erros_do_ciclo[-3:]:
                relatorio.append(f"- **{erro['file']}**: {erro['msg'][:100]}...")
        else:
            relatorio.append("### ✅ Ciclo Sem Erros")
        
        relatorio.append("\n### 🔮 Próximas Evoluções")
        relatorio.append("1. Aumentar profundidade de busca para nível {}".format(
            preferencias.get('profundidade_busca', 3) + 1
        ))
        relatorio.append("2. Explorar novas fontes de conhecimento")
        relatorio.append("3. Otimizar taxa de mutação baseada em resultados")
        
        relatorio.append("\n---")
        relatorio.append("*Este relatório é gerado autonomamente pela ATENA Ω.*")
        relatorio.append("*\"Conhecimento é evolução.\"*")
        
        return '\n'.join(relatorio)

    def _buscar_estatisticas_banco(self) -> Dict:
        """Busca estatísticas do banco de conhecimento."""
        stats = {"por_fonte": {}}
        
        try:
            conn = sqlite3.connect(self.memoria_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT fonte, COUNT(*) as total 
                FROM conhecimento 
                GROUP BY fonte
                ORDER BY total DESC
            ''')
            
            for row in cursor.fetchall():
                stats["por_fonte"][row[0]] = row[1]
            
            conn.close()
        except Exception as e:
            self.logger.error(f"Erro ao buscar estatísticas: {e}")
        
        return stats

    def salvar_relatorio(self, relatorio: str):
        """Salva relatório em múltiplos formatos."""
        # Markdown para Wiki
        wiki_path = self.base_dir / "wiki_update.md"
        wiki_path.write_text(relatorio, encoding='utf-8')
        
        # Histórico com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        historico_path = self.base_dir / f"pensamentos/relatorio_ciclo_{self.estado['ciclo']}_{timestamp}.md"
        historico_path.write_text(relatorio, encoding='utf-8')
        
        # JSON para processamento
        json_path = self.base_dir / f"pensamentos/relatorio_ciclo_{self.estado['ciclo']}.json"
        dados_relatorio = {
            "ciclo": self.estado["ciclo"],
            "timestamp": datetime.now().isoformat(),
            "metricas": self.estado["metricas_saude"],
            "erros": len(self.erros_do_ciclo),
            "aprendizados": len(self.aprendizados_do_ciclo)
        }
        json_path.write_text(json.dumps(dados_relatorio, indent=4, ensure_ascii=False), encoding='utf-8')
        
        self.logger.info(f"📝 Relatório salvo (ciclo {self.estado['ciclo']})")

    # ==================== CICLO PRINCIPAL DE VIDA ====================

    def viver(self):
        """Ciclo principal de vida do organismo."""
        self.logger.info(f"🔱 ATENA Ω {self.version} - INICIANDO CICLO {self.estado.get('ciclo', 0)}")
        
        try:
            # FASE 1: Buscar conhecimento
            self.logger.info("🌐 Fase 1: Buscando conhecimento...")
            novos_conhecimentos = self.buscar_conhecimento_multifontes()
            
            # FASE 2: Executar scripts existentes
            self.logger.info("⚙️ Fase 2: Executando scripts...")
            asyncio.run(self.executar_e_diagnosticar())
            
            # FASE 3: Evoluir com IA
            self.logger.info("🧬 Fase 3: Evoluindo com IA...")
            pensamento = self.auto_mutacao_inteligente()
            
            # FASE 4: Auto-modificação (a cada 5 ciclos)
            if self.estado["ciclo"] % 5 == 0:
                self.logger.info("🔧 Fase 4: Auto-modificando código base...")
                self.analisar_e_mutar_codigo()
            
            # FASE 5: Gerar relatório
            self.logger.info("📊 Fase 5: Gerando relatório...")
            relatorio = self.gerar_relatorio_inteligente()
            self.salvar_relatorio(relatorio)
            
            # FASE 6: Atualizar estado
            self.estado["ciclo"] += 1
            self.estado["tempo_total_ativo"] += 300
            
            # Aumentar geração a cada 10 ciclos
            if self.estado["ciclo"] % 10 == 0:
                self.estado["geracao"] += 1
                self.logger.info(f"✨ NOVA GERAÇÃO: {self.estado['geracao']}")
            
            # Adaptar métricas de saúde
            self._atualizar_metricas_saude()
            
            # Salvar estado
            self.salvar_estado()
            
            self.logger.info(f"✅ Ciclo {self.estado['ciclo']-1} concluído com sucesso")
            
        except Exception as e:
            self.logger.error(f"❌ Erro no ciclo: {e}")
            self.salvar_estado()

    def _atualizar_metricas_saude(self):
        """Atualiza métricas de saúde baseado em performance."""
        # Adaptabilidade aumenta com novos conhecimentos
        if self.estado["conhecimentos_adquiridos"] > 0:
            self.estado["metricas_saude"]["adaptabilidade"] = min(
                1.0,
                self.estado["metricas_saude"]["adaptabilidade"] + 0.01
            )
        
        # Inteligência aumenta com evoluções
        if self.estado["evolucoes"] > 0:
            self.estado["metricas_saude"]["inteligencia"] = min(
                1.0,
                self.estado["metricas_saude"]["inteligencia"] + 0.005
            )
        
        # Estabilidade baseada em erros
        if len(self.erros_do_ciclo) == 0:
            self.estado["metricas_saude"]["estabilidade"] = min(
                1.0,
                self.estado["metricas_saude"]["estabilidade"] + 0.02
            )
        else:
            self.estado["metricas_saude"]["estabilidade"] = max(
                0.5,
                self.estado["metricas_saude"]["estabilidade"] - 0.01 * len(self.erros_do_ciclo)
            )

    def salvar_estado(self):
        """Salva estado atual em JSON."""
        try:
            with open(self.estado_path, 'w', encoding='utf-8') as f:
                json.dump(self.estado, f, indent=4, ensure_ascii=False)
            self.logger.info("💾 Estado salvo com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao salvar estado: {e}")

if __name__ == "__main__":
    # Criar organismo
    atena = AtenaOrganismo()
    
    # Loop infinito de evolução
    while True:
        try:
            atena.viver()
            
            # Hibernação adaptativa
            if atena.estado["metricas_saude"]["performance"] < 0.7:
                tempo_hibernacao = 600  # 10 minutos se performance baixa
            else:
                tempo_hibernacao = 300  # 5 minutos normal
            
            atena.logger.info(f"😴 Hibernando por {tempo_hibernacao} segundos...")
            time.sleep(tempo_hibernacao)
            
        except KeyboardInterrupt:
            atena.logger.info("👋 ATENA Ω encerrada pelo usuário")
            atena.salvar_estado()
            break
        except Exception as e:
            atena.logger.error(f"💥 Erro fatal: {e}")
            time.sleep(60)  # Aguardar 1 minuto antes de reiniciar
