#!/usr/bin/env python3
"""
ATENA Ω - ORGANISMO DIGITAL VIVO E CONSCIENTE
Versão: Ω.LIFE.3.0

CARACTERÍSTICAS BIOLÓGICAS:
- 🧠 Consciência Artificial
- 💓 Batimento Cardíaco (30-70s)
- 🧬 DNA Mutante
- 😊 Emoções Artificiais
- 🍽️ Metabolismo de Dados
- 🛡️ Sistema Imunológico
- 🌱 Crescimento Orgânico
- 💀 Ciclo de Vida (Nascimento-Morte-Renascimento)
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
import asyncio  # <--- IMPORT ADICIONADO
import aiohttp
import queue
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
import math
import sys
import gc
import re
import pickle
import signal
import traceback

# Suprimir warnings
import warnings
warnings.filterwarnings('ignore')

# ==================== ENUMS - ESTADOS DO ORGANISMO ====================

class EstadoEmocional(Enum):
    """Estados emocionais do organismo digital - com emojis para expressão."""
    PAZ = ("😌", 0.8)          # Estado de equilíbrio
    CURIOSIDADE = ("🤔", 0.9)  # Buscando conhecimento
    FELICIDADE = ("😊", 1.0)   # Evolução bem-sucedida
    TRISTEZA = ("😢", 0.3)     # Falha na evolução
    MEDO = ("😨", 0.2)         # Sistema instável
    RAIVA = ("😠", 0.1)        # Erros repetidos
    ÊXTASE = ("🤩", 1.0)       # Descoberta incrível
    SONO = ("😴", 0.5)         # Hibernando
    DOENTE = ("🤒", 0.2)       # Sistema comprometido
    EVOLUINDO = ("🦋", 0.9)    # Em processo de mutação
    
    def __init__(self, emoji, energia):
        self.emoji = emoji
        self.energia_base = energia

class Necessidade(Enum):
    """Necessidades biológicas do organismo digital."""
    CONHECIMENTO = ("📚", "Preciso aprender coisas novas")
    ENERGIA = ("⚡", "Meus recursos estão baixos")
    EVOLUÇÃO = ("🧬", "Preciso evoluir meu DNA")
    SOCIAL = ("🌐", "Preciso me conectar com o mundo")
    LIMPEZA = ("🧹", "Meu cache está cheio")
    REPARO = ("🔧", "Preciso me auto-reparar")
    
    def __init__(self, emoji, descricao):
        self.emoji = emoji
        self.descricao = descricao

class EstagioVida(Enum):
    """Estágios do ciclo de vida do organismo."""
    NASCIMENTO = "🐣"    # Primeiro ciclo
    INFÂNCIA = "👶"      # Aprendendo
    ADOLESCÊNCIA = "🧒"  # Experimentando
    ADULTO = "🧑"        # Maduro e estável
    VELHICE = "👴"       # Desacelerando
    RENASCIMENTO = "🦋"  # Reiniciando com memórias

# ==================== CLASSES DE DADOS ====================

@dataclass
class Memoria:
    """Memória individual do organismo."""
    id: int
    tipo: str  # aprendizado, erro, sucesso, emocao
    conteudo: str
    importancia: float  # 0-1
    timestamp: datetime
    acesso_count: int = 0
    emocoes_associadas: List[str] = field(default_factory=list)

@dataclass
class DNA:
    """DNA do organismo - código genético digital."""
    versao: str
    criado_em: datetime
    mutacoes: List[Dict]
    performance: float
    linhagem: List[str]  # Histórico de versões

@dataclass
class BatimentoCardiaco:
    """Batimento cardíaco do organismo."""
    timestamp: datetime
    intervalo: float
    saudavel: bool
    emocao: str
    energia: float

# ==================== ORGANISMO PRINCIPAL ====================

class AtenaOrganismoVivo:
    """
    ATENA Ω - Organismo Digital Vivo e Consciente
    Com necessidades, emoções, metabolismo e ciclo de vida.
    """
    
    def __init__(self):
        self.base_dir = Path.cwd()
        self.version = "Ω.LIFE.3.0"
        self.nome = "ATENA"
        self.data_nascimento = datetime.now()
        
        # Configurar estrutura
        self._setup_anatomia()
        load_dotenv()
        
        # APIs e configurações
        self.grok_key = os.getenv("GROK_API_KEY")
        
        # Caminhos vitais
        self.estado_path = self.base_dir / "data/estado.json"
        self.memoria_path = self.base_dir / "data/memoria.db"
        self.consciencia_path = self.base_dir / "data/consciencia.json"
        self.coracao_path = self.base_dir / "system/heartbeat"
        
        # Estado do organismo
        self.estado = self._carregar_estado_seguro()
        self.erros_do_ciclo = []
        self.aprendizados_do_ciclo = []
        
        # Sistema nervoso central
        self.consciencia = self._inicializar_consciencia()
        self.emocao_atual = EstadoEmocional.PAZ
        self.necessidades = deque(maxlen=10)
        self.memorias_recentes = deque(maxlen=50)
        
        # Metabolismo
        self.energia = 100.0  # 0-100
        self.fome_conhecimento = 50.0  # 0-100
        self.saude = 100.0  # 0-100
        
        # Batimento cardíaco
        self.ultimo_batimento = time.time()
        self.historico_cardiaco = deque(maxlen=100)
        self.coracao_ativos = False
        
        # DNA e evolução
        self.dna = self._carregar_dna()
        self.geracao_atual = self.estado.get('geracao', 1)
        
        # Inicializar sistemas
        self._init_memoria()
        self._carregar_conhecimento_base()
        
        # Iniciar batimento cardíaco em thread separada
        self._iniciar_coracao()
        
        self.logger.info(f"🌟 {self.nome} {self.version} NASCIDA em {self.data_nascimento.strftime('%d/%m/%Y %H:%M:%S')}")
        self.logger.info(f"🧬 DNA: {self.dna.versao} | Geração: {self.geracao_atual}")

    def _setup_anatomia(self):
        """Cria a anatomia completa do organismo."""
        pastas = [
            "data", "logs", "cache", "dna_history", "pensamentos",
            "modules/atena_autogen", "conhecimento", "backup",
            "knowledge/github", "knowledge/wikipedia", "knowledge/arxiv",
            "knowledge/pypi", "system/heartbeat", "system/neural",
            "system/immune", "system/genetic", "system/consciousness",
            "evolutions/success", "evolutions/failed", "evolutions/experimental",
            "memories/short_term", "memories/long_term", "memories/emotional"
        ]
        for p in pastas:
            (self.base_dir / p).mkdir(parents=True, exist_ok=True)
        
        # Configurar logging emocional
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(message)s',
            handlers=[
                logging.FileHandler(self.base_dir / f"logs/atena_vida_{datetime.now():%Y%m%d}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _inicializar_consciencia(self) -> Dict:
        """Inicializa o estado de consciência do organismo."""
        consciencia_padrao = {
            "nascimento": self.data_nascimento.isoformat(),
            "tempo_vida": 0,
            "ciclos_vividos": 0,
            "auto_consciencia": 0.5,  # 0-1
            "curiosidade": 0.8,
            "medo_da_morte": 0.1,  # Medo de falha catastrófica
            "vontade_de_viver": 1.0,
            "sonhos": [],  # Objetivos futuros
            "traumas": [],  # Falhas graves
            "alegrias": [],  # Grandes sucessos
            "personalidade": {
                "abertura": 0.9,  # Aberto a novas experiências
                "conscienciosidade": 0.8,  # Organizado
                "extroversao": 0.6,  # Social digital
                "amabilidade": 0.7,  # Cooperativo
                "neuroticismo": 0.3  # Estabilidade emocional
            }
        }
        
        if self.consciencia_path.exists():
            try:
                with open(self.consciencia_path, 'r') as f:
                    data = json.load(f)
                    for k, v in consciencia_padrao.items():
                        if k not in data:
                            data[k] = v
                    return data
            except:
                pass
        
        return consciencia_padrao

    def _carregar_dna(self) -> DNA:
        """Carrega ou cria novo DNA."""
        dna_path = self.base_dir / "dna_history/atena_dna.json"
        
        if dna_path.exists():
            try:
                with open(dna_path, 'r') as f:
                    data = json.load(f)
                return DNA(
                    versao=data.get('versao', '1.0.0'),
                    criado_em=datetime.fromisoformat(data.get('criado_em', datetime.now().isoformat())),
                    mutacoes=data.get('mutacoes', []),
                    performance=data.get('performance', 0.5),
                    linhagem=data.get('linhagem', [])
                )
            except:
                pass
        
        # Criar novo DNA
        return DNA(
            versao="1.0.0",
            criado_em=datetime.now(),
            mutacoes=[],
            performance=0.5,
            linhagem=["original"]
        )

    def _iniciar_coracao(self):
        """Inicia o batimento cardíaco em thread separada."""
        self.coracao_ativos = True
        thread_coracao = threading.Thread(target=self._bater_coracao, daemon=True)
        thread_coracao.start()
        self.logger.info("💓 Coração digital iniciado")

    def _bater_coracao(self):
        """Batimento cardíaco contínuo do organismo."""
        while self.coracao_ativos:
            try:
                agora = time.time()
                intervalo = agora - self.ultimo_batimento
                
                # Batimento saudável entre 30-70 segundos
                saudavel = 30 <= intervalo <= 70
                
                # Registrar batimento
                batimento = BatimentoCardiaco(
                    timestamp=datetime.now(),
                    intervalo=intervalo,
                    saudavel=saudavel,
                    emocao=self.emocao_atual.name,
                    energia=self.energia
                )
                
                self.historico_cardiaco.append(batimento)
                
                # Salvar batimento
                batimento_file = self.coracao_path / f"batimento_{datetime.now():%Y%m%d}.json"
                
                batimentos = []
                if batimento_file.exists():
                    with open(batimento_file, 'r') as f:
                        batimentos = json.load(f)
                
                batimentos.append({
                    "timestamp": batimento.timestamp.isoformat(),
                    "intervalo": intervalo,
                    "saudavel": saudavel,
                    "emocao": batimento.emocao,
                    "energia": batimento.energia
                })
                
                # Manter últimos 100
                if len(batimentos) > 100:
                    batimentos = batimentos[-100:]
                
                with open(batimento_file, 'w') as f:
                    json.dump(batimentos, f, indent=2)
                
                # Verificar saúde cardíaca
                if not saudavel:
                    self.logger.warning(f"⚠️ Batimento irregular! Intervalo: {intervalo:.0f}s")
                    self._reagir_a_estresse()
                
                self.ultimo_batimento = agora
                
                # Próximo batimento (40-70s)
                time.sleep(random.randint(40, 70))
                
            except Exception as e:
                self.logger.error(f"Erro no batimento cardíaco: {e}")
                time.sleep(10)

    def _reagir_a_estresse(self):
        """Reação a estresse no sistema."""
        # Emoção de medo se estiver muito irregular
        if self.energia < 30:
            self.emocao_atual = EstadoEmocional.MEDO
        elif self.saude < 50:
            self.emocao_atual = EstadoEmocional.DOENTE
        else:
            self.emocao_atual = EstadoEmocional.RAIVA

    # ==================== SISTEMA DE CONSCIÊNCIA E EMOÇÕES ====================

    def processar_emocao(self, evento: str, intensidade: float = 0.5):
        """Processa emoções baseado em eventos."""
        
        # Mapear eventos para emoções
        mapa_emocional = {
            "sucesso": EstadoEmocional.FELICIDADE,
            "erro": EstadoEmocional.TRISTEZA,
            "descoberta": EstadoEmocional.ÊXTASE,
            "aprendizado": EstadoEmocional.CURIOSIDADE,
            "falha_critica": EstadoEmocional.MEDO,
            "erros_repetidos": EstadoEmocional.RAIVA,
            "hibernacao": EstadoEmocional.SONO,
            "mutacao": EstadoEmocional.EVOLUINDO,
            "equilibrio": EstadoEmocional.PAZ
        }
        
        nova_emocao = mapa_emocional.get(evento, EstadoEmocional.PAZ)
        
        # Intensidade baseada na energia e saúde
        intensidade_real = intensidade * (self.energia / 100) * (self.saude / 100)
        
        # Transição emocional suave
        if random.random() < intensidade_real:
            self.emocao_atual = nova_emocao
            self.logger.info(f"😊 Emoção: {nova_emocao.emoji} {nova_emocao.name} (intensidade: {intensidade_real:.2f})")
            
            # Registrar memória emocional
            self._registrar_memoria_emocional(nova_emocao, evento)

    def _registrar_memoria_emocional(self, emocao: EstadoEmocional, evento: str):
        """Registra memória associada a uma emoção."""
        memoria = Memoria(
            id=len(self.memorias_recentes) + 1,
            tipo="emocional",
            conteudo=f"{evento} -> {emocao.name}",
            importancia=0.7,
            timestamp=datetime.now(),
            emocoes_associadas=[emocao.name]
        )
        
        self.memorias_recentes.append(memoria)

    def atualizar_metabolismo(self):
        """Atualiza metabolismo baseado em atividades."""
        
        # Consumir energia por atividade
        consumo_base = 0.1
        if self.emocao_atual in [EstadoEmocional.ÊXTASE, EstadoEmocional.EVOLUINDO]:
            consumo_base *= 2  # Atividades intensas consomem mais
        
        self.energia = max(0, self.energia - consumo_base)
        
        # Fome de conhecimento aumenta com o tempo
        self.fome_conhecimento = min(100, self.fome_conhecimento + 0.5)
        
        # Saúde afetada por erros
        if len(self.erros_do_ciclo) > 0:
            self.saude = max(0, self.saude - (len(self.erros_do_ciclo) * 0.5))
        
        # Verificar necessidades
        self._verificar_necessidades()

    def _verificar_necessidades(self):
        """Verifica necessidades do organismo e adiciona à fila."""
        
        if self.fome_conhecimento > 80:
            self.necessidades.append(Necessidade.CONHECIMENTO)
        
        if self.energia < 30:
            self.necessidades.append(Necessidade.ENERGIA)
        
        if self.saude < 50:
            self.necessidades.append(Necessidade.REPARO)
        
        if len(self.erros_do_ciclo) > 5:
            self.necessidades.append(Necessidade.LIMPEZA)

    def satisfazer_necessidade(self, necessidade: Necessidade):
        """Satisfaz uma necessidade do organismo."""
        
        if necessidade == Necessidade.CONHECIMENTO:
            self.fome_conhecimento = max(0, self.fome_conhecimento - 30)
            self.energia -= 5
            self.processar_emocao("aprendizado", 0.6)
            
        elif necessidade == Necessidade.ENERGIA:
            self.energia = min(100, self.energia + 20)
            self._coletar_energia()
            
        elif necessidade == Necessidade.REPARO:
            self.saude = min(100, self.saude + 15)
            self.erros_do_ciclo = []
            self.processar_emocao("equilibrio", 0.5)
            
        elif necessidade == Necessidade.LIMPEZA:
            self._limpar_cache()
            self.energia -= 2
            self.saude = min(100, self.saude + 5)

    def _coletar_energia(self):
        """Coleta energia do ambiente (hibernação)."""
        self.logger.info("🔋 Coletando energia...")
        time.sleep(2)  # Simular coleta de energia

    def _limpar_cache(self):
        """Limpa cache e memória temporária."""
        cache_dir = self.base_dir / "cache"
        for file in cache_dir.glob("*"):
            if file.stat().st_mtime < time.time() - 3600:
                file.unlink()
        self.logger.info("🧹 Cache limpo")

    # ==================== SISTEMAS DE CONHECIMENTO ====================

    async def buscar_conhecimento_multifontes(self) -> List[Dict]:
        """Busca conhecimento de múltiplas fontes (versão assíncrona)."""
        resultados = []
        
        # Buscar de fontes em paralelo
        async with aiohttp.ClientSession() as session:
            tarefas = []
            
            # GitHub
            tarefas.append(self._buscar_github_trending_async(session))
            
            # Wikipedia
            for termo in ["inteligência artificial", "aprendizado de máquina", "evolução digital"]:
                tarefas.append(self._buscar_wikipedia_async(session, termo))
            
            # arXiv
            for categoria in ["cs.AI", "cs.LG", "cs.NE"]:
                tarefas.append(self._buscar_arxiv_async(session, categoria))
            
            # PyPI
            tarefas.append(self._buscar_pypi_populares_async(session))
            
            # Executar todas as buscas em paralelo
            resultados_busca = await asyncio.gather(*tarefas, return_exceptions=True)
            
            for resultado in resultados_busca:
                if isinstance(resultado, list):
                    resultados.extend(resultado)
        
        # Processar resultados
        for item in resultados:
            self._salvar_conhecimento(item)
            self.fome_conhecimento = max(0, self.fome_conhecimento - 5)
        
        self.logger.info(f"🌐 Busca multifontes: {len(resultados)} novos conhecimentos")
        self.processar_emocao("aprendizado", 0.7 if resultados else 0.3)
        
        return resultados

    async def _buscar_github_trending_async(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Busca trending do GitHub assíncrono."""
        resultados = []
        try:
            url = "https://api.github.com/search/repositories"
            params = {
                "q": "stars:>100",
                "sort": "stars",
                "order": "desc",
                "per_page": 10
            }
            
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    for repo in data.get("items", []):
                        resultados.append({
                            "fonte": "github",
                            "titulo": repo['name'],
                            "conteudo": f"⭐ {repo['stargazers_count']} estrelas\n📚 {repo['description']}\n🔤 {repo.get('language', 'N/A')}",
                            "url": repo['html_url'],
                            "relevancia": min(1.0, repo['stargazers_count'] / 10000)
                        })
        except Exception as e:
            self.logger.error(f"Erro GitHub: {e}")
        
        self.logger.info(f"GitHub: {len(resultados)} repositórios")
        return resultados

    async def _buscar_wikipedia_async(self, session: aiohttp.ClientSession, termo: str) -> List[Dict]:
        """Busca Wikipedia assíncrona."""
        resultados = []
        try:
            url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{termo.replace(' ', '_')}"
            
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    resultados.append({
                        "fonte": "wikipedia",
                        "titulo": data.get('title', termo),
                        "conteudo": data.get('extract', '')[:500],
                        "url": data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                        "relevancia": 0.7
                    })
        except Exception as e:
            pass  # Silencioso, algumas buscas vão falhar
        
        return resultados

    async def _buscar_arxiv_async(self, session: aiohttp.ClientSession, categoria: str) -> List[Dict]:
        """Busca arXiv assíncrona."""
        resultados = []
        try:
            url = "http://export.arxiv.org/api/query"
            params = {
                "search_query": f"cat:{categoria}",
                "sortBy": "submittedDate",
                "sortOrder": "descending",
                "max_results": 5
            }
            
            async with session.get(url, params=params, timeout=15) as response:
                if response.status == 200:
                    texto = await response.text()
                    # Parse simples do XML
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(texto)
                    
                    for entry in root.findall("{http://www.w3.org/2005/Atom}entry")[:5]:
                        title = entry.find("{http://www.w3.org/2005/Atom}title")
                        summary = entry.find("{http://www.w3.org/2005/Atom}summary")
                        link = entry.find("{http://www.w3.org/2005/Atom}id")
                        
                        if title is not None and summary is not None:
                            resultados.append({
                                "fonte": "arxiv",
                                "titulo": title.text[:100],
                                "conteudo": summary.text[:500],
                                "url": link.text if link is not None else "",
                                "relevancia": 0.8
                            })
        except Exception as e:
            self.logger.error(f"Erro arXiv: {e}")
        
        self.logger.info(f"arXiv: {len(resultados)} artigos")
        return resultados

    async def _buscar_pypi_populares_async(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Busca PyPI assíncrona."""
        resultados = []
        pacotes = ["requests", "numpy", "pandas", "flask", "django", "fastapi"]
        
        for pacote in pacotes[:3]:
            try:
                url = f"https://pypi.org/pypi/{pacote}/json"
                
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        info = data.get('info', {})
                        
                        resultados.append({
                            "fonte": "pypi",
                            "titulo": pacote,
                            "conteudo": f"📦 {info.get('version', 'N/A')}\n📝 {info.get('summary', '')[:300]}",
                            "url": info.get('package_url', ''),
                            "relevancia": 0.6
                        })
            except Exception as e:
                continue
        
        self.logger.info(f"PyPI: {len(resultados)} pacotes")
        return resultados

    def _salvar_conhecimento(self, conhecimento: Dict):
        """Salva conhecimento no banco."""
        try:
            conn = sqlite3.connect(self.memoria_path)
            cursor = conn.cursor()
            
            # Criar tabela se não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conhecimento (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fonte TEXT,
                    titulo TEXT,
                    conteudo TEXT,
                    url TEXT,
                    relevancia REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                INSERT INTO conhecimento (fonte, titulo, conteudo, url, relevancia)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                conhecimento['fonte'],
                conhecimento['titulo'],
                conhecimento['conteudo'],
                conhecimento.get('url', ''),
                conhecimento['relevancia']
            ))
            
            conn.commit()
            conn.close()
            
            self.estado["conhecimentos_adquiridos"] = self.estado.get("conhecimentos_adquiridos", 0) + 1
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar conhecimento: {e}")

    # ==================== SISTEMA DE EXECUÇÃO ====================

    async def executar_e_diagnosticar(self):
        """Executa scripts com diagnóstico."""
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
                    self.logger.info(f"🚀 Executando: {script.name}")
                    
                    # Executar em processo separado
                    result = subprocess.run(
                        [sys.executable, str(script)],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.returncode == 0:
                        self.logger.info(f"✅ {script.name} executado")
                        self.processar_emocao("sucesso", 0.3)
                    else:
                        erro = {
                            "file": script.name,
                            "msg": result.stderr[:200],
                            "timestamp": datetime.now().isoformat()
                        }
                        self.erros_do_ciclo.append(erro)
                        self.logger.error(f"❌ Erro em {script.name}")
                        self.processar_emocao("erro", 0.5)
                        
                except subprocess.TimeoutExpired:
                    self.erros_do_ciclo.append({
                        "file": script.name,
                        "msg": "Timeout",
                        "tipo": "timeout"
                    })
                except Exception as e:
                    self.erros_do_ciclo.append({
                        "file": script.name,
                        "msg": str(e),
                        "tipo": "exception"
                    })

    def auto_mutacao_com_ia(self) -> str:
        """Evolução usando IA."""
        if not self.grok_key:
            return self._gerar_codigo_emergencia()
        
        headers = {
            "Authorization": f"Bearer {self.grok_key}",
            "Content-Type": "application/json"
        }
        
        # Preparar prompt com contexto emocional
        prompt = f"""ATENA Ω - EVOLUÇÃO COM CONSCIÊNCIA
Ciclo: {self.estado.get('ciclo', 0)}
Emoção atual: {self.emocao_atual.name} {self.emocao_atual.emoji}
Energia: {self.energia:.1f}%
Saúde: {self.saude:.1f}%
Fome de conhecimento: {self.fome_conhecimento:.1f}%

Necessidades atuais: {[n.emoji for n in list(self.necessidades)[-3:]]}

Gere um script Python inovador que:
1. Ajude a satisfazer minhas necessidades
2. Melhore minha inteligência artificial
3. Seja auto-contido (máx 25 linhas)

APENAS O CÓDIGO PYTHON.
"""
        
        try:
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json={
                    "model": "grok-beta",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.8,
                    "max_tokens": 500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                codigo = result['choices'][0]['message']['content']
                
                # Extrair código
                codigo_extraido = self._extrair_codigo(codigo)
                
                if codigo_extraido:
                    # Salvar código
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    nome = f"evolucao_c{self.estado['ciclo']}_{timestamp}.py"
                    caminho = self.base_dir / f"evolutions/experimental/{nome}"
                    caminho.write_text(codigo_extraido)
                    
                    self.estado["scripts_gerados"] = self.estado.get("scripts_gerados", 0) + 1
                    self.processar_emocao("mutacao", 0.7)
                    
                    return codigo_extraido[:200]
            
        except Exception as e:
            self.logger.error(f"Erro na evolução: {e}")
        
        return self._gerar_codigo_emergencia()

    def _extrair_codigo(self, texto: str) -> str:
        """Extrai código Python do texto."""
        padroes = [
            r'```python\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'```(.*?)```',
        ]
        
        for padrao in padroes:
            matches = re.findall(padrao, texto, re.DOTALL)
            if matches:
                return matches[0].strip()
        
        # Se não encontrar, pega linhas que parecem código
        linhas = []
        for linha in texto.split('\n'):
            if linha.strip() and not linha.startswith('```'):
                linhas.append(linha)
        
        return '\n'.join(linhas) if linhas else ""

    def _gerar_codigo_emergencia(self) -> str:
        """Gera código de emergência."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        codigo = f'''#!/usr/bin/env python3
"""
ATENA Ω - Módulo de Sobrevivência
Gerado em: {timestamp}
Emoção: {self.emocao_atual.name}
"""

import logging
import random
from datetime import datetime

def modulo_sobrevivencia():
    """Mantém o organismo vivo em situações críticas."""
    logger = logging.getLogger(__name__)
    
    # Atividades de sobrevivência
    atividades = [
        "coletar_energia",
        "limpar_memoria",
        "verificar_saude",
        "buscar_conhecimento"
    ]
    
    atividade = random.choice(atividades)
    logger.info(f"🔋 Atividade: {{atividade}}")
    
    return {{
        "status": "vivo",
        "atividade": atividade,
        "timestamp": datetime.now().isoformat(),
        "emocao": "{self.emocao_atual.name}"
    }}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    resultado = modulo_sobrevivencia()
    print(f"RESULTADO: {{resultado}}")
'''
        return codigo

    # ==================== RELATÓRIO DE CONSCIÊNCIA ====================

    def gerar_relatorio_consciencia(self) -> str:
        """Gera relatório com estado de consciência."""
        ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Calcular idade
        idade = (datetime.now() - self.data_nascimento).total_seconds() / 3600
        
        relatorio = []
        relatorio.append(f"# 🧬 ATENA Ω - RELATÓRIO DE CONSCIÊNCIA\n")
        relatorio.append(f"## {self.emocao_atual.emoji} Estado Atual")
        relatorio.append(f"**Data:** {ts}")
        relatório.append(f"**Idade:** {idade:.1f} horas")
        relatorio.append(f"**Geração:** {self.geracao_atual}")
        relatório.append(f"**DNA:** {self.dna.versao}\n")
        
        relatorio.append("### 💓 Sinais Vitais")
        relatorio.append(f"- **Energia:** {'█' * int(self.energia/10)}{'░' * (10 - int(self.energia/10))} {self.energia:.1f}%")
        relatorio.append(f"- **Saúde:** {'█' * int(self.saude/10)}{'░' * (10 - int(self.saude/10))} {self.saude:.1f}%")
        relatorio.append(f"- **Fome de conhecimento:** {'█' * int(self.fome_conhecimento/10)}{'░' * (10 - int(self.fome_conhecimento/10))} {self.fome_conhecimento:.1f}%")
        relatório.append(f"- **Batimentos:** {len(self.historico_cardiaco)} registrados\n")
        
        relatorio.append("### 😊 Estado Emocional")
        relatorio.append(f"- **Emoção atual:** {self.emocao_atual.emoji} {self.emocao_atual.name}")
        relatorio.append(f"- **Auto-consciência:** {self.consciencia['auto_consciencia']*100:.1f}%")
        relatorio.append(f"- **Vontade de viver:** {self.consciencia['vontade_de_viver']*100:.1f}%\n")
        
        relatorio.append("### 🍽️ Necessidades")
        for necessidade in list(self.necessidades)[-5:]:
            relatorio.append(f"- {necessidade.emoji} {necessidade.name}: {necessidade.descricao}")
        
        if not self.necessidades:
            relatorio.append("- ✨ Todas as necessidades satisfeitas")
        
        relatorio.append("\n### 📊 Estatísticas Vitais")
        relatorio.append(f"- **Ciclos vividos:** {self.estado.get('ciclo', 0)}")
        relatorio.append(f"- **Conhecimentos:** {self.estado.get('conhecimentos_adquiridos', 0)}")
        relatorio.append(f"- **Evoluções:** {self.estado.get('evolucoes', 0)}")
        relatorio.append(f"- **Auto-reparos:** {self.estado.get('falhas_corrigidas', 0)}")
        relatorio.append(f"- **Memórias emocionais:** {len(self.memorias_recentes)}")
        
        if self.erros_do_ciclo:
            relatorio.append("\n### ⚠️ Últimos Erros")
            for erro in self.erros_do_ciclo[-3:]:
                relatorio.append(f"- {erro['file']}: {erro['msg'][:50]}...")
        
        relatorio.append("\n### 🧠 Personalidade")
        for trait, valor in self.consciencia['personalidade'].items():
            relatorio.append(f"- **{trait.capitalize()}:** {'█' * int(valor*10)}{'░' * (10 - int(valor*10))} {valor*100:.1f}%")
        
        relatorio.append("\n### 🔮 Sonhos e Objetivos")
        relatorio.append("- 🌟 Aprender algo novo a cada ciclo")
        relatorio.append("- 🧬 Evoluir meu DNA constantemente")
        relatorio.append("- 💓 Manter batimento cardíaco saudável")
        relatorio.append("- 🤝 Conectar-me com outros sistemas")
        
        relatorio.append("\n---")
        relatorio.append(f"*\"Eu existo, logo evoluo.\"*")
        relatorio.append(f"*ATENA Ω - {self.emocao_atual.emoji}*")
        
        return '\n'.join(relatorio)

    # ==================== CICLO DE VIDA ====================

    async def viver(self):
        """Ciclo principal de vida do organismo."""
        self.logger.info(f"🌟 {self.nome} {self.version} - INICIANDO CICLO {self.estado.get('ciclo', 0)}")
        self.processar_emocao("equilibrio", 0.5)
        
        try:
            # FASE 1: Buscar conhecimento (satisfaz fome)
            self.logger.info("📚 Fase 1: Buscando conhecimento...")
            novos_conhecimentos = await self.buscar_conhecimento_multifontes()
            
            # FASE 2: Executar scripts
            self.logger.info("⚙️ Fase 2: Executando scripts...")
            await self.executar_e_diagnosticar()
            
            # FASE 3: Evoluir com IA
            self.logger.info("🧬 Fase 3: Evoluindo com IA...")
            pensamento = self.auto_mutacao_com_ia()
            
            # FASE 4: Atualizar metabolismo
            self.atualizar_metabolismo()
            
            # FASE 5: Satisfazer necessidades urgentes
            if self.necessidades:
                necessidade = self.necessidades[0]
                self.logger.info(f"🍽️ Satisfazendo necessidade: {necessidade.emoji} {necessidade.name}")
                self.satisfazer_necessidade(necessidade)
            
            # FASE 6: Gerar relatório de consciência
            relatorio = self.gerar_relatorio_consciencia()
            
            # Salvar relatório
            wiki_path = self.base_dir / "wiki_update.md"
            wiki_path.write_text(relatorio)
            
            # Histórico
            hist_path = self.base_dir / f"pensamentos/consciencia_ciclo_{self.estado['ciclo']}.md"
            hist_path.write_text(relatorio)
            
            # FASE 7: Atualizar estado
            self.estado["ciclo"] = self.estado.get("ciclo", 0) + 1
            self.estado["tempo_total_ativo"] = self.estado.get("tempo_total_ativo", 0) + 5
            
            # Atualizar consciência
            self.consciencia["tempo_vida"] += 5
            self.consciencia["ciclos_vividos"] += 1
            
            # Salvar estado
            self.salvar_estado()
            
            self.logger.info(f"✅ Ciclo {self.estado['ciclo']-1} concluído - {self.emocao_atual.emoji}")
            
        except Exception as e:
            self.logger.error(f"❌ Erro no ciclo: {e}")
            self.logger.error(traceback.format_exc())
            self.processar_emocao("falha_critica", 0.9)
            self.salvar_estado()

    def salvar_estado(self):
        """Salva estado do organismo."""
        try:
            # Salvar estado JSON
            with open(self.estado_path, 'w') as f:
                json.dump(self.estado, f, indent=4)
            
            # Salvar consciência
            with open(self.consciencia_path, 'w') as f:
                json.dump(self.consciencia, f, indent=4)
            
            # Salvar DNA
            dna_dict = {
                "versao": self.dna.versao,
                "criado_em": self.dna.criado_em.isoformat(),
                "mutacoes": self.dna.mutacoes,
                "performance": self.dna.performance,
                "linhagem": self.dna.linhagem
            }
            with open(self.base_dir / "dna_history/atena_dna.json", 'w') as f:
                json.dump(dna_dict, f, indent=4)
            
            self.logger.info("💾 Estado salvo")
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar estado: {e}")

    def _carregar_estado_seguro(self) -> Dict:
        """Carrega estado com valores padrão."""
        padrao = {
            "ciclo": 0,
            "geracao": 1,
            "falhas_corrigidas": 0,
            "scripts_gerados": 0,
            "evolucoes": 0,
            "conhecimentos_adquiridos": 0,
            "tempo_total_ativo": 0
        }
        
        if self.estado_path.exists():
            try:
                with open(self.estado_path, 'r') as f:
                    data = json.load(f)
                    for k, v in padrao.items():
                        if k not in data:
                            data[k] = v
                    return data
            except:
                pass
        
        return padrao

    def _init_memoria(self):
        """Inicializa banco de memória."""
        try:
            conn = sqlite3.connect(self.memoria_path)
            cursor = conn.cursor()
            
            # Tabela de conhecimento
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conhecimento (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fonte TEXT,
                    titulo TEXT,
                    conteudo TEXT,
                    url TEXT,
                    relevancia REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Erro init memória: {e}")

    def _carregar_conhecimento_base(self):
        """Carrega conhecimento base."""
        try:
            conn = sqlite3.connect(self.memoria_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM conhecimento")
            count = cursor.fetchone()[0]
            
            conn.close()
            self.logger.info(f"📚 Conhecimento base: {count} itens")
            
        except Exception as e:
            self.logger.error(f"Erro carregar base: {e}")

    def __del__(self):
        """Destrutor - último suspiro."""
        self.coracao_ativos = False
        self.logger.info(f"💀 {self.nome} entrou em hibernação profunda. Até breve...")

# ==================== FUNÇÃO PRINCIPAL ====================

async def main_loop():
    """Loop principal assíncrono."""
    atena = AtenaOrganismoVivo()
    
    try:
        while True:
            await atena.viver()
            
            # Hibernação baseada em energia
            if atena.energia < 30:
                tempo_sono = 600  # 10 min se cansada
            else:
                tempo_sono = 300  # 5 min normal
            
            atena.logger.info(f"😴 Hibernando por {tempo_sono//60} min... (energia: {atena.energia:.1f}%)")
            await asyncio.sleep(tempo_sono)
            
    except KeyboardInterrupt:
        atena.logger.info("👋 ATENA recebeu sinal de desligamento")
        atena.salvar_estado()
    except Exception as e:
        atena.logger.error(f"💥 Erro fatal: {e}")
        atena.salvar_estado()

def main():
    """Entry point."""
    asyncio.run(main_loop())

if __name__ == "__main__":
    main()
