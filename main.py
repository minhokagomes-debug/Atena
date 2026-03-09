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
import psutil
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any
import asyncio
import aiohttp
import zlib
import base64
import re
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

class AtenaOrganismo:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.version = "Ω.49.4"  # Versão corrigida
        self._setup_anatomia()
        load_dotenv()
        
        # Configurações de API
        self.grok_key = os.getenv("GROK_API_KEY")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo_url = os.getenv("GITHUB_REPO")
        
        # Caminhos críticos
        self.estado_path = self.base_dir / "data/estado.json"
        self.memoria_path = self.base_dir / "data/memoria.db"
        self.dna_path = self.base_dir / "dna_history"
        self.knowledge_path = self.base_dir / "conhecimento"
        
        # Estado do organismo
        self.estado = self._carregar_estado_seguro()
        self.erros_do_ciclo = []
        self.metricas = defaultdict(list)
        self.start_time = time.time()
        self.ultimo_batimento = time.time()
        
        # Inicializar componentes
        self._init_memoria()
        self._init_metricas()
        
    def _setup_anatomia(self):
        """Cria a estrutura completa do organismo digital."""
        pastas = [
            "data", "logs", "cache", "dna_history", "pensamentos", 
            "modules/atena_autogen", "conhecimento", "backup", 
            "metricas", "system/heartbeat"
        ]
        for p in pastas:
            (self.base_dir / p).mkdir(parents=True, exist_ok=True)
            
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | Ω[%(levelname)s] | %(message)s',
            handlers=[
                logging.FileHandler(self.base_dir / f"logs/atena_{datetime.now():%Y%m%d}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _init_memoria(self):
        """Inicializa banco SQLite para memória persistente."""
        conn = sqlite3.connect(self.memoria_path)
        cursor = conn.cursor()
        
        # Tabela de memórias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                tipo TEXT,
                conteudo TEXT,
                hash TEXT UNIQUE,
                importancia REAL DEFAULT 0.5
            )
        ''')
        
        # Tabela de aprendizados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS aprendizados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                padrao TEXT,
                resultado TEXT,
                confianca REAL,
                vezes_usado INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()

    def _carregar_estado_seguro(self) -> Dict:
        """Carrega estado com validação e recuperação."""
        padrao = {
            "ciclo": 0,
            "falhas_corrigidas": 0,
            "scripts_gerados": 0,
            "evolucoes": 0,
            "insights_gerados": 0,
            "versao_dna": "1.0.0",
            "metricas_saude": {
                "performance": 1.0,
                "estabilidade": 1.0,
                "adaptabilidade": 0.8
            }
        }
        
        if self.estado_path.exists():
            try:
                with open(self.estado_path, 'r') as f:
                    conteudo = f.read()
                    if not conteudo.strip():
                        return padrao
                    data = json.loads(conteudo)
                    # Merge com valores padrão
                    for k, v in padrao.items():
                        if k not in data:
                            data[k] = v
                    return data
            except (json.JSONDecodeError, Exception) as e:
                self.logger.error(f"Erro ao carregar estado: {e}")
        return padrao

    def _init_metricas(self):
        """Inicializa sistema de métricas."""
        self.metricas_atuais = {
            "cpu_usage": [],
            "memory_usage": [],
            "scripts_executed": 0,
            "errors_rate": 0
        }

    async def executar_e_diagnosticar(self):
        """Executa scripts com diagnóstico."""
        folder = self.base_dir / "modules/atena_autogen"
        scripts = list(folder.glob("*.py"))
        
        for script in scripts:
            try:
                self.logger.info(f"🚀 Ativando módulo: {script.name}")
                
                # Executar script
                result = subprocess.run(
                    ["python", str(script)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode != 0:
                    erro = {
                        "file": script.name,
                        "msg": result.stderr,
                        "timestamp": datetime.now().isoformat()
                    }
                    self.erros_do_ciclo.append(erro)
                    
            except subprocess.TimeoutExpired:
                self.erros_do_ciclo.append({
                    "file": script.name,
                    "msg": "Timeout de execução",
                    "tipo": "timeout"
                })
            except Exception as e:
                self.erros_do_ciclo.append({
                    "file": script.name,
                    "msg": str(e),
                    "tipo": "exception"
                })

    def auto_mutacao_ou_reparo(self) -> str:
        """Evolução com IA."""
        if not self.grok_key:
            self.logger.error("Chave Grok não encontrada!")
            return "print('Grok Offline')"
        
        headers = {
            "Authorization": f"Bearer {self.grok_key}",
            "Content-Type": "application/json"
        }
        
        # Decidir modo
        if self.erros_do_ciclo:
            erro = self.erros_do_ciclo[0]
            prompt = f"""Corrija este erro em Python:
Arquivo: {erro['file']}
Erro: {erro['msg']}

Gere apenas o código corrigido, máximo 20 linhas."""
            modo = "reparo"
        else:
            focos = ["otimização", "análise de dados", "auto-diagnóstico", "compressão"]
            foco = random.choice(focos)
            prompt = f"Gere um script Python de até 15 linhas para {foco}. Apenas código."
            modo = "evolucao"
        
        try:
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json={
                    "model": "grok-beta",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 300
                },
                timeout=30
            )
            
            result = response.json()
            resposta = result['choices'][0]['message']['content']
            
            # Extrair código
            codigo = self._extrair_codigo(resposta)
            
            if not codigo:
                return "print('Falha na geração')"
            
            # Salvar código
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if modo == "reparo":
                nome = f"correcao_{timestamp}.py"
                self.estado["falhas_corrigidas"] += 1
            else:
                nome = f"evolucao_c{self.estado['ciclo']}_{timestamp}.py"
                self.estado["scripts_gerados"] += 1
                self.estado["evolucoes"] += 1
            
            caminho = self.base_dir / f"modules/atena_autogen/{nome}"
            caminho.write_text(codigo)
            
            return codigo
            
        except Exception as e:
            self.logger.error(f"Erro na evolução: {e}")
            return "print('Erro de comunicação')"

    def _extrair_codigo(self, resposta: str) -> str:
        """Extrai código Python da resposta."""
        # Padrões comuns
        padroes = [
            r'```python\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'```(.*?)```',
        ]
        
        for padrao in padroes:
            matches = re.findall(padrao, resposta, re.DOTALL)
            if matches:
                return matches[0].strip()
        
        # Se não encontrar, retorna linhas que parecem código
        linhas = []
        for linha in resposta.split('\n'):
            if linha.strip() and not linha.startswith('```'):
                linhas.append(linha)
        
        return '\n'.join(linhas) if linhas else "print('Código não gerado')"

    def gerar_relatorio_wiki(self, pensamento: str):
        """Gera relatório para Wiki - VERSÃO CORRIGIDA."""
        ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Coletar métricas
        ciclo = self.estado.get('ciclo', 0)
        scripts = self.estado.get('scripts_gerados', 0)
        reparos = self.estado.get('falhas_corrigidas', 0)
        evolucoes = self.estado.get('evolucoes', 0)
        
        # Construir conteúdo - CORRIGIDO: strings fechadas corretamente
        conteudo = f"# 🔱 ATENA Ω v{self.version} - Diário de Evolução\n\n"
        conteudo += f"## 📊 Métricas do Ciclo {ciclo}\n"
        conteudo += f"**Sincronização:** {ts}\n\n"
        
        conteudo += "### Estatísticas Vitais\n"
        conteudo += f"- **Módulos Criados:** {scripts}\n"
        conteudo += f"- **Auto-Reparos:** {reparos}\n"
        conteudo += f"- **Evoluções:** {evolucoes}\n\n"
        
        conteudo += "### 🧠 Último Insight Gerado\n"
        conteudo += f"```\n{pensamento[:200]}...\n```\n\n"
        
        # Registrar erros
        if self.erros_do_ciclo:
            conteudo += "### ⚠️ Erros Detectados\n"
            for erro in self.erros_do_ciclo[-3:]:
                conteudo += f"- {erro['file']}: {erro['msg'][:50]}...\n"
        else:
            conteudo += "### ✅ Ciclo Sem Erros\n"
            conteudo += "Nenhum erro detectado.\n"
        
        conteudo += "\n---\n"
        conteudo += "*Este documento é gerado autonomamente pela ATENA Ω.*"
        
        # Salvar relatório
        relatorio_path = self.base_dir / "wiki_update.md"
        relatorio_path.write_text(conteudo)
        
        # Histórico
        historico_path = self.base_dir / f"pensamentos/relatorio_ciclo_{ciclo}.md"
        historico_path.write_text(conteudo)
        
        self.logger.info(f"📝 Relatório gerado")

    def viver(self):
        """Ciclo principal de vida do organismo - Versão simplificada."""
        self.logger.info(f"🔱 ATENA Ω v{self.version} - INICIANDO CICLO {self.estado.get('ciclo', 0)}")
        
        try:
            # 1. Execução e Diagnóstico
            asyncio.run(self.executar_e_diagnosticar())
            
            # 2. Evolução ou Conserto
            pensamento = self.auto_mutacao_ou_reparo()
            
            # 3. Preparação da Wiki
            self.gerar_relatorio_wiki(pensamento)
            
            # 4. Atualizar estado
            self.estado["ciclo"] += 1
            self.estado_path.write_text(json.dumps(self.estado, indent=4))
            
            self.logger.info(f"✅ Ciclo {self.estado['ciclo']-1} concluído com sucesso")
            
        except Exception as e:
            self.logger.error(f"❌ Erro no ciclo: {e}")
            # Salvar estado mesmo com erro
            self.estado_path.write_text(json.dumps(self.estado, indent=4))

if __name__ == "__main__":
    # Loop principal simplificado
    organismo = AtenaOrganismo()
    while True:
        organismo.viver()
        time.sleep(300)  # 5 minutos
