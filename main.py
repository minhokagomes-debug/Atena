#!/usr/bin/env python3
"""
ATENA Ω - ORGANISMO DIGITAL DE ALTA PERFORMANCE
Versão: Ω.PERFORMANCE.1.0

CICLO DE TRABALHO:
- ⏰ 5 minutos de TRABALHO INTENSO (processamento, aprendizado, evolução)
- 💤 30 minutos de DESCANSO (para não consumir recursos do GitHub Actions)
- 🔄 Repetir infinitamente
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
import asyncio
import aiohttp
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any
import re
import sys
import traceback
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed

# Suprimir warnings
import warnings
warnings.filterwarnings('ignore')

class AtenaHighPerformance:
    """
    ATENA Ω - Versão de Alta Performance
    Trabalha INTENSAMENTE por 5 minutos, descansa 30 minutos
    """
    
    def __init__(self):
        self.base_dir = Path.cwd()
        self.version = "Ω.PERFORMANCE.1.0"
        self.nome = "ATENA"
        self.data_nascimento = datetime.now()
        
        # Configurações de tempo
        self.tempo_trabalho = 300  # 5 minutos de trabalho INTENSO
        self.tempo_descanso = 1800  # 30 minutos de descanso
        self.inicio_ciclo = time.time()
        
        # Configurar estrutura
        self._setup_anatomia()
        load_dotenv()
        
        # APIs e tokens
        self.grok_key = os.getenv("GROK_API_KEY")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo_name = os.getenv("GITHUB_REPOSITORY", "Atena/Atena")
        
        # Caminhos importantes
        self.estado_path = self.base_dir / "data/estado.json"
        self.modules_path = self.base_dir / "modules"
        self.knowledge_path = self.base_dir / "conhecimento"
        self.evolutions_path = self.base_dir / "evolutions"
        self.docs_path = self.base_dir / "docs"
        self.fila_tarefas = queue.Queue()
        
        # Estado
        self.estado = self._carregar_estado()
        self.erros_do_ciclo = []
        self.codigos_gerados = []
        self.tarefas_executadas = 0
        self.tarefas_falhas = 0
        
        # Métricas de performance
        self.metricas = {
            "inicio_sessao": datetime.now().isoformat(),
            "total_tarefas": 0,
            "tempo_medio_tarefa": 0,
            "tarefas_por_minuto": 0,
            "modulos_por_sessao": 0,
            "conhecimento_por_sessao": 0
        }
        
        # Inicializar
        self._init_diretorios()
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"🌟 {self.nome} {self.version} INICIADA")
        self.logger.info(f"⚙️ Modo: TRABALHO INTENSO (5min) + DESCANSO (30min)")
        self.logger.info(f"📦 GitHub: {self.repo_name}")

    def _setup_anatomia(self):
        """Cria estrutura de diretórios."""
        pastas = [
            "data", "logs", 
            "modules/ativos", "modules/experimentais", "modules/aprendidos", "modules/processando",
            "conhecimento/github", "conhecimento/wikipedia", "conhecimento/arxiv", "conhecimento/processado",
            "evolutions/sucesso", "evolutions/experimental", "evolutions/historico", "evolutions/processando",
            "docs/wiki", "docs/exemplos", "docs/tutoriais", "docs/metricas",
            "backup/codigos", "backup/estados", "backup/por_sessao",
            "fila/prioridade_alta", "fila/prioridade_media", "fila/prioridade_baixa",
            "resultados/sucesso", "resultados/falha", "resultados/parcial"
        ]
        for p in pastas:
            (self.base_dir / p).mkdir(parents=True, exist_ok=True)
        
        # Configurar logging com timestamp
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(message)s',
            datefmt='%H:%M:%S',
            handlers=[
                logging.FileHandler(self.base_dir / f"logs/atena_{datetime.now():%Y%m%d_%H%M}.log"),
                logging.StreamHandler()
            ]
        )

    def _init_diretorios(self):
        """Inicializa diretórios com arquivos README."""
        readmes = {
            "modules": "# 🧠 Módulos da ATENA\n\nMódulos em processamento, ativos e aprendidos.",
            "conhecimento": "# 📚 Conhecimento Adquirido\n\nConhecimento sendo processado em tempo real.",
            "evolutions": "# 🧬 Evoluções da ATENA\n\nCódigos em evolução constante.",
            "docs": "# 📖 Documentação da ATENA\n\nDocumentação gerada em cada sessão de trabalho."
        }
        
        for pasta, conteudo in readmes.items():
            readme_path = self.base_dir / pasta / "README.md"
            if not readme_path.exists():
                readme_path.write_text(conteudo)

    def _carregar_estado(self) -> Dict:
        """Carrega estado do organismo."""
        padrao = {
            "sessao": 0,
            "ciclo_na_sessao": 0,
            "geracao": 1,
            "modulos_criados": 0,
            "modulos_aprendidos": 0,
            "conhecimentos": 0,
            "evolucoes": 0,
            "tarefas_totais": 0,
            "tempo_total_trabalho": 0,
            "ultima_sessao": None,
            "recordes": {
                "modulos_por_sessao": 0,
                "tarefas_por_sessao": 0,
                "conhecimentos_por_sessao": 0
            }
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

    # ==================== SISTEMA DE FILAS E PRIORIDADES ====================

    def adicionar_tarefa(self, tarefa: Dict, prioridade: str = "media"):
        """Adiciona tarefa à fila de processamento."""
        tarefa["timestamp"] = datetime.now().isoformat()
        tarefa["id"] = hashlib.md5(f"{tarefa['tipo']}{time.time()}".encode()).hexdigest()[:8]
        
        if prioridade == "alta":
            self.fila_tarefas.put((0, tarefa))
        elif prioridade == "media":
            self.fila_tarefas.put((1, tarefa))
        else:
            self.fila_tarefas.put((2, tarefa))
        
        self.metricas["total_tarefas"] += 1
        return tarefa["id"]

    def processar_fila(self, tempo_restante: float):
        """Processa fila de tarefas durante o tempo de trabalho."""
        inicio_processamento = time.time()
        tarefas_processadas = 0
        
        self.logger.info(f"📋 Filas: {self.fila_tarefas.qsize()} tarefas pendentes")
        
        while time.time() - inicio_processamento < tempo_restante and not self.fila_tarefas.empty():
            try:
                prioridade, tarefa = self.fila_tarefas.get(timeout=1)
                
                self.logger.info(f"⚙️ Processando tarefa {tarefa['id']} ({tarefa['tipo']})...")
                
                # Processar baseado no tipo
                if tarefa['tipo'] == 'busca_github':
                    resultado = self._processar_busca_github(tarefa)
                elif tarefa['tipo'] == 'gerar_codigo':
                    resultado = self._processar_geracao_codigo(tarefa)
                elif tarefa['tipo'] == 'aprender_codigo':
                    resultado = self._processar_aprendizado(tarefa)
                elif tarefa['tipo'] == 'evoluir':
                    resultado = self._processar_evolucao(tarefa)
                else:
                    resultado = self._processar_generico(tarefa)
                
                if resultado:
                    tarefas_processadas += 1
                    self.tarefas_executadas += 1
                else:
                    self.tarefas_falhas += 1
                
                # Mostrar progresso
                if tarefas_processadas % 3 == 0:
                    progresso = (time.time() - inicio_processamento) / tempo_restante * 100
                    self.logger.info(f"📊 Progresso: {progresso:.1f}% | Tarefas: {tarefas_processadas}")
                
            except queue.Empty:
                break
            except Exception as e:
                self.logger.error(f"❌ Erro em tarefa: {e}")
                self.tarefas_falhas += 1
        
        return tarefas_processadas

    def _processar_busca_github(self, tarefa: Dict) -> bool:
        """Processa busca no GitHub."""
        try:
            resultado = asyncio.run(self._buscar_codigos_github_rapido(tarefa.get('termo', 'python')))
            if resultado:
                self.estado["modulos_aprendidos"] += len(resultado)
                self.metricas["conhecimento_por_sessao"] += len(resultado)
                return True
        except:
            pass
        return False

    def _processar_geracao_codigo(self, tarefa: Dict) -> bool:
        """Processa geração de código."""
        codigo = self.gerar_codigo_com_ia_rapido(tarefa.get('contexto', ''))
        if codigo:
            nome = self.salvar_codigo_gerado(codigo)
            self.codigos_gerados.append(nome)
            self.estado["modulos_criados"] += 1
            self.metricas["modulos_por_sessao"] += 1
            return True
        return False

    def _processar_aprendizado(self, tarefa: Dict) -> bool:
        """Processa aprendizado de código."""
        # Implementar lógica de aprendizado
        return True

    def _processar_evolucao(self, tarefa: Dict) -> bool:
        """Processa evolução de código existente."""
        return True

    def _processar_generico(self, tarefa: Dict) -> bool:
        """Processa tarefa genérica."""
        self.logger.info(f"📌 Tarefa genérica: {tarefa}")
        return True

    # ==================== BUSCA RÁPIDA NO GITHUB ====================

    async def _buscar_codigos_github_rapido(self, termo: str = "python") -> List[Dict]:
        """Busca códigos no GitHub de forma otimizada."""
        resultados = []
        try:
            url = "https://api.github.com/search/code"
            params = {
                "q": f"{termo} extension:py",
                "per_page": 5,
                "sort": "indexed"
            }
            
            headers = {}
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for item in data.get("items", [])[:3]:  # Limitar para velocidade
                            if item['size'] < 50000:  # < 50KB
                                async with session.get(item['download_url'], timeout=3) as code_resp:
                                    if code_resp.status == 200:
                                        codigo = await code_resp.text()
                                        resultados.append({
                                            "fonte": "github",
                                            "tipo": "codigo",
                                            "titulo": item['name'],
                                            "conteudo": codigo[:1500],  # Limitado
                                            "url": item['html_url'],
                                            "relevancia": 0.8
                                        })
                                        
                                        # Salvar rápido
                                        self._salvar_codigo_rapido(item['name'], codigo)
        except Exception as e:
            self.logger.error(f"Erro busca rápida: {e}")
        
        return resultados

    def _salvar_codigo_rapido(self, nome: str, codigo: str):
        """Salva código rapidamente sem metadados extras."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"aprendido_{timestamp}_{nome}"
            caminho = self.base_dir / f"modules/aprendidos/{nome_arquivo}"
            caminho.write_text(codigo[:3000])  # Limitado
        except:
            pass

    # ==================== GERAÇÃO DE CÓDIGO OTIMIZADA ====================

    def gerar_codigo_com_ia_rapido(self, contexto: str = "") -> Optional[str]:
        """Gera código usando IA de forma otimizada."""
        if not self.grok_key:
            return self._gerar_codigo_padrao_rapido()
        
        headers = {
            "Authorization": f"Bearer {self.grok_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Gere um utilitário Python útil e curto (máx 30 linhas).
Seja criativo e prático.
Apenas código, sem explicações.
{contexto}"""
        
        try:
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json={
                    "model": "grok-beta",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.9,
                    "max_tokens": 800
                },
                timeout=10  # Timeout curto para não travar
            )
            
            if response.status_code == 200:
                result = response.json()
                codigo = result['choices'][0]['message']['content']
                return self._extrair_codigo_rapido(codigo)
            
        except Exception as e:
            self.logger.error(f"Erro geração rápida: {e}")
        
        return self._gerar_codigo_padrao_rapido()

    def _extrair_codigo_rapido(self, texto: str) -> str:
        """Extrai código rapidamente."""
        padroes = [
            r'```python\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'(def [a-zA-Z_].*?:\n(?:\s+.*\n?)*)',
        ]
        
        for padrao in padroes:
            match = re.search(padrao, texto, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return texto[:1000] if texto else None

    def _gerar_codigo_padrao_rapido(self) -> str:
        """Gera código padrão rápido."""
        return '''#!/usr/bin/env python3
"""Módulo rápido da ATENA"""

import random
import time

def utilidade_rapida():
    """Função utilitária rápida."""
    return {
        "status": "ok",
        "timestamp": time.time(),
        "valor": random.randint(1, 100)
    }

if __name__ == "__main__":
    print(utilidade_rapida())
'''

    def salvar_codigo_gerado(self, codigo: str) -> str:
        """Salva código gerado."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hash_id = hashlib.md5(codigo.encode()).hexdigest()[:8]
        
        nome_arquivo = f"atena_sessao{self.estado['sessao']}_{timestamp}_{hash_id}.py"
        caminho = self.base_dir / f"modules/ativos/{nome_arquivo}"
        
        cabecalho = f'''#!/usr/bin/env python3
"""
🧬 ATENA Ω - Gerado em Sessão {self.estado['sessao']}
Ciclo: {self.estado['ciclo_na_sessao']}
Timestamp: {timestamp}
"""

'''
        caminho.write_text(cabecalho + codigo)
        return nome_arquivo

    # ==================== EXECUÇÃO RÁPIDA DE MÓDULOS ====================

    def executar_modulos_rapido(self, tempo_limite: float):
        """Executa módulos de forma rápida em paralelo."""
        modulos_aprendidos = list((self.base_dir / "modules/aprendidos").glob("*.py"))[-10:]
        modulos_ativos = list((self.base_dir / "modules/ativos").glob("*.py"))[-10:]
        
        todos_modulos = modulos_aprendidos + modulos_ativos
        
        if not todos_modulos:
            self.logger.info("📭 Nenhum módulo para executar")
            return
        
        self.logger.info(f"⚙️ Executando {len(todos_modulos)} módulos em paralelo...")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for modulo in todos_modulos[:10]:  # Limitar
                futures.append(executor.submit(self._executar_unico_modulo, modulo))
            
            for future in as_completed(futures):
                try:
                    future.result(timeout=3)
                except:
                    pass

    def _executar_unico_modulo(self, modulo: Path) -> bool:
        """Executa um único módulo."""
        try:
            result = subprocess.run(
                [sys.executable, str(modulo)],
                capture_output=True,
                text=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False

    # ==================== WIKI RÁPIDA ====================

    def gerar_wiki_rapida(self):
        """Gera wiki de forma otimizada."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        modulos_ativos = list((self.base_dir / "modules/ativos").glob("*.py"))
        modulos_aprendidos = list((self.base_dir / "modules/aprendidos").glob("*.py"))
        
        wiki = [
            f"# 📊 ATENA Ω - Sessão {self.estado['sessao']}\n",
            f"**Horário:** {timestamp}\n",
            "## 📈 Performance\n",
            f"- Tarefas executadas: {self.tarefas_executadas}",
            f"- Módulos criados: {self.estado['modulos_criados']}",
            f"- Módulos aprendidos: {self.estado['modulos_aprendidos']}",
            f"- Taxa sucesso: {self._calcular_taxa_sucesso()}%\n",
            "## 🧠 Últimos Módulos\n",
        ]
        
        for modulo in modulos_ativos[-5:]:
            wiki.append(f"- `{modulo.name}`")
        
        wiki.append("\n## 📚 Aprendidos\n")
        for modulo in modulos_aprendidos[-5:]:
            wiki.append(f"- `{modulo.name}`")
        
        wiki.append("\n---\n*Próxima sessão em 30 minutos*")
        
        wiki_path = self.base_dir / f"docs/wiki/sessao_{self.estado['sessao']}.md"
        wiki_path.write_text('\n'.join(wiki))
        
        # Link simbólico para o atual
        (self.base_dir / "wiki.md").write_text('\n'.join(wiki))

    def _calcular_taxa_sucesso(self) -> float:
        """Calcula taxa de sucesso das tarefas."""
        total = self.tarefas_executadas + self.tarefas_falhas
        if total == 0:
            return 100
        return round((self.tarefas_executadas / total) * 100, 1)

    # ==================== MÉTRICAS DE PERFORMANCE ====================

    def atualizar_metricas(self, tarefas_processadas: int):
        """Atualiza métricas de performance."""
        tempo_gasto = time.time() - self.inicio_ciclo
        
        self.metricas.update({
            "tarefas_por_minuto": round(tarefas_processadas / (tempo_gasto / 60), 1),
            "tempo_medio_tarefa": round(tempo_gasto / max(1, tarefas_processadas), 2),
            "modulos_por_sessao": self.metricas["modulos_por_sessao"],
            "conhecimento_por_sessao": self.metricas["conhecimento_por_sessao"]
        })
        
        # Atualizar recordes
        if self.metricas["modulos_por_sessao"] > self.estado["recordes"]["modulos_por_sessao"]:
            self.estado["recordes"]["modulos_por_sessao"] = self.metricas["modulos_por_sessao"]
        
        if tarefas_processadas > self.estado["recordes"]["tarefas_por_sessao"]:
            self.estado["recordes"]["tarefas_por_sessao"] = tarefas_processadas
        
        # Salvar métricas
        metricas_path = self.base_dir / f"docs/metricas/sessao_{self.estado['sessao']}.json"
        with open(metricas_path, 'w') as f:
            json.dump(self.metricas, f, indent=2)

    # ==================== CICLO DE TRABALHO INTENSO ====================

    async def sessao_trabalho(self):
        """Sessão de trabalho intenso de 5 minutos."""
        self.inicio_ciclo = time.time()
        self.estado["sessao"] += 1
        self.estado["ciclo_na_sessao"] = 0
        self.tarefas_executadas = 0
        self.tarefas_falhas = 0
        
        self.logger.info(f"⚡ INICIANDO SESSÃO DE TRABALHO #{self.estado['sessao']}")
        self.logger.info(f"⏰ Duração: 5 minutos de PROCESSAMENTO INTENSO")
        
        # Calcular tempo limite
        tempo_fim = time.time() + self.tempo_trabalho
        
        # FASE 1: Preparar fila de tarefas (30 segundos)
        self.logger.info("📋 Preparando fila de tarefas...")
        for i in range(10):  # 10 tarefas iniciais
            self.adicionar_tarefa({
                "tipo": random.choice(["busca_github", "gerar_codigo", "evoluir"]),
                "prioridade": i
            })
        
        # FASE 2: Processar fila continuamente (4 minutos)
        while time.time() < tempo_fim:
            tempo_restante = tempo_fim - time.time()
            if tempo_restante <= 0:
                break
            
            self.estado["ciclo_na_sessao"] += 1
            
            # Processar lote de tarefas
            self.logger.info(f"🔄 Ciclo #{self.estado['ciclo_na_sessao']} da sessão")
            
            tarefas_processadas = self.processar_fila(min(45, tempo_restante))  # 45s por ciclo
            
            # Adicionar mais tarefas se necessário
            if self.fila_tarefas.qsize() < 5:
                for _ in range(3):
                    self.adicionar_tarefa({
                        "tipo": random.choice(["busca_github", "gerar_codigo"]),
                    }, prioridade="baixa")
            
            # Executar módulos rapidamente
            self.executar_modulos_rapido(min(15, tempo_restante))
            
            # Pequena pausa para não sobrecarregar
            if time.time() < tempo_fim:
                time.sleep(1)
        
        # FASE 3: Gerar resultados (30 segundos finais)
        self.logger.info("📊 Gerando resultados da sessão...")
        
        self.atualizar_metricas(self.tarefas_executadas)
        self.gerar_wiki_rapida()
        
        # Salvar estado
        self.estado["tempo_total_trabalho"] += self.tempo_trabalho
        self.estado["tarefas_totais"] += self.tarefas_executadas
        self.estado["ultima_sessao"] = datetime.now().isoformat()
        
        with open(self.estado_path, 'w') as f:
            json.dump(self.estado, f, indent=4)
        
        # Resumo da sessão
        self.logger.info(f"✅ SESSÃO #{self.estado['sessao']} CONCLUÍDA")
        self.logger.info(f"📊 Tarefas: {self.tarefas_executadas} sucesso / {self.tarefas_falhas} falha")
        self.logger.info(f"⚡ Taxa: {self.metricas['tarefas_por_minuto']} tarefas/min")
        self.logger.info(f"🧠 Módulos criados nesta sessão: {self.metricas['modulos_por_sessao']}")
        self.logger.info(f"📚 Conhecimentos adquiridos: {self.metricas['conhecimento_por_sessao']}")
        
        if self.metricas['modulos_por_sessao'] > 0:
            self.logger.info(f"🏆 Recorde de módulos: {self.estado['recordes']['modulos_por_sessao']}")

    async def viver(self):
        """Ciclo principal de vida com trabalho e descanso."""
        while True:
            # Sessão de TRABALHO INTENSO (5 minutos)
            await self.sessao_trabalho()
            
            # Período de DESCANSO (30 minutos)
            self.logger.info(f"😴 DESCANSO: 30 minutos até próxima sessão")
            self.logger.info(f"💤 Hibernando para economizar recursos...")
            
            # Mostrar contagem regressiva a cada 5 minutos
            for i in range(6):
                if i < 5:
                    restante = self.tempo_descanso - (i * 300)
                    self.logger.info(f"⏳ Descanso: {restante//60} minutos restantes...")
                await asyncio.sleep(300)  # 5 minutos

# ==================== FUNÇÃO PRINCIPAL ====================

async def main():
    """Função principal."""
    atena = AtenaHighPerformance()
    await atena.viver()

if __name__ == "__main__":
    asyncio.run(main())
