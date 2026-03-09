import os
import json
import logging
import requests
import time
import subprocess
import random
import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any
import asyncio
import aiohttp
import re
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

class AtenaOrganismo:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.version = "Ω.49.5"  # Versão sem psutil
        self._setup_anatomia()
        load_dotenv()
        
        # Configurações de API
        self.grok_key = os.getenv("GROK_API_KEY")
        
        # Caminhos críticos
        self.estado_path = self.base_dir / "data/estado.json"
        self.memoria_path = self.base_dir / "data/memoria.db"
        self.dna_path = self.base_dir / "dna_history"
        
        # Estado do organismo
        self.estado = self._carregar_estado_seguro()
        self.erros_do_ciclo = []
        self.start_time = time.time()
        self.ultimo_batimento = time.time()
        
        # Inicializar componentes
        self._init_memoria()
        
    def _setup_anatomia(self):
        """Cria a estrutura completa do organismo digital."""
        pastas = [
            "data", "logs", "cache", "dna_history", "pensamentos", 
            "modules/atena_autogen", "conhecimento", "backup"
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
        try:
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
            self.logger.info("✅ Banco de memória inicializado")
        except Exception as e:
            self.logger.error(f"Erro ao inicializar memória: {e}")

    def _carregar_estado_seguro(self) -> Dict:
        """Carrega estado com validação e recuperação."""
        padrao = {
            "ciclo": 0,
            "falhas_corrigidas": 0,
            "scripts_gerados": 0,
            "evolucoes": 0,
            "insights_gerados": 0,
            "versao_dna": "1.0.0",
            "ultimo_checkpoint": None,
            "metricas_saude": {
                "performance": 1.0,
                "estabilidade": 1.0,
                "adaptabilidade": 0.8
            }
        }
        
        if self.estado_path.exists():
            try:
                with open(self.estado_path, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                    if not conteudo.strip():
                        self.logger.warning("Arquivo de estado vazio, usando padrão")
                        return padrao
                    data = json.loads(conteudo)
                    # Merge com valores padrão
                    for k, v in padrao.items():
                        if k not in data:
                            data[k] = v
                    return data
            except json.JSONDecodeError as e:
                self.logger.error(f"Erro ao decodificar estado.json: {e}")
                # Fazer backup do arquivo corrompido
                if self.estado_path.exists():
                    backup_path = self.base_dir / f"backup/estado_corrompido_{datetime.now():%Y%m%d_%H%M%S}.json"
                    self.estado_path.rename(backup_path)
                    self.logger.info(f"Backup criado: {backup_path}")
            except Exception as e:
                self.logger.error(f"Erro ao carregar estado: {e}")
        
        return padrao

    async def executar_e_diagnosticar(self):
        """Executa scripts com diagnóstico."""
        folder = self.base_dir / "modules/atena_autogen"
        scripts = list(folder.glob("*.py"))
        
        if not scripts:
            self.logger.info("Nenhum script para executar")
            return
        
        self.logger.info(f"Executando {len(scripts)} scripts...")
        
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
                        "msg": result.stderr[:200],  # Limitar tamanho
                        "timestamp": datetime.now().isoformat()
                    }
                    self.erros_do_ciclo.append(erro)
                    self.logger.error(f"Erro em {script.name}: {result.stderr[:100]}")
                else:
                    self.logger.info(f"✅ {script.name} executado com sucesso")
                    
            except subprocess.TimeoutExpired:
                self.erros_do_ciclo.append({
                    "file": script.name,
                    "msg": "Timeout de execução (30s)",
                    "tipo": "timeout"
                })
                self.logger.error(f"Timeout em {script.name}")
            except Exception as e:
                self.erros_do_ciclo.append({
                    "file": script.name,
                    "msg": str(e),
                    "tipo": "exception"
                })
                self.logger.error(f"Exceção em {script.name}: {e}")

    def auto_mutacao_ou_reparo(self) -> str:
        """Evolução com IA."""
        if not self.grok_key:
            self.logger.error("Chave Grok não encontrada!")
            return self._gerar_codigo_emergencia()
        
        headers = {
            "Authorization": f"Bearer {self.grok_key}",
            "Content-Type": "application/json"
        }
        
        # Decidir modo baseado em erros
        if self.erros_do_ciclo:
            # Modo reparo
            erro = self.erros_do_ciclo[0]
            prompt = f"""ATENA Ω - MODO REPARO

Arquivo com erro: {erro['file']}
Mensagem de erro: {erro['msg']}

Gere APENAS o código Python corrigido (máximo 20 linhas).
O código deve ser auto-contido e executável.
NÃO inclua explicações, apenas o código."""
            
            modo = "reparo"
        else:
            # Modo evolução - escolher foco aleatório
            focos = [
                "otimização de desempenho",
                "análise de logs",
                "compressão de dados",
                "auto-diagnóstico",
                "geração de relatórios",
                "limpeza de cache"
            ]
            foco = random.choice(focos)
            
            prompt = f"""ATENA Ω - MODO EVOLUÇÃO

Foco: {foco}
Ciclo atual: {self.estado['ciclo']}

Gere um script Python inovador de até 15 linhas para {foco}.
O script deve ser útil para um organismo digital autônomo.
APENAS o código Python, sem explicações."""
            
            modo = "evolucao"
        
        try:
            self.logger.info(f"🤖 Consultando Grok API (modo: {modo})...")
            
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
            
            if response.status_code != 200:
                self.logger.error(f"Erro na API: {response.status_code}")
                return self._gerar_codigo_emergencia()
            
            result = response.json()
            resposta = result['choices'][0]['message']['content']
            
            # Extrair código
            codigo = self._extrair_codigo(resposta)
            
            if not codigo or len(codigo) < 10:
                self.logger.warning("Código gerado é muito curto, usando fallback")
                return self._gerar_codigo_emergencia()
            
            # Salvar código
            return self._salvar_codigo(codigo, modo)
            
        except requests.exceptions.Timeout:
            self.logger.error("Timeout na requisição à API")
            return self._gerar_codigo_emergencia()
        except Exception as e:
            self.logger.error(f"Erro na evolução: {e}")
            return self._gerar_codigo_emergencia()

    def _extrair_codigo(self, resposta: str) -> str:
        """Extrai código Python da resposta."""
        # Padrões comuns de markdown
        padroes = [
            r'```python\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'```(.*?)```',
        ]
        
        for padrao in padroes:
            matches = re.findall(padrao, resposta, re.DOTALL)
            if matches:
                return matches[0].strip()
        
        # Se não encontrar blocos de código, tenta extrair linhas que parecem código
        linhas = []
        dentro_codigo = False
        
        for linha in resposta.split('\n'):
            linha = linha.rstrip()
            if linha.startswith('def ') or linha.startswith('class ') or linha.startswith('import ') or linha.startswith('from '):
                linhas.append(linha)
                dentro_codigo = True
            elif dentro_codigo and linha and not linha.startswith('```'):
                linhas.append(linha)
            elif dentro_codigo and not linha:
                linhas.append('')
        
        if linhas:
            return '\n'.join(linhas)
        
        return ""

    def _salvar_codigo(self, codigo: str, modo: str) -> str:
        """Salva código gerado em arquivo."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Adicionar cabeçalho
        cabecalho = f"""# ATENA Ω - Código Auto-gerado
# Modo: {modo}
# Timestamp: {timestamp}
# Ciclo: {self.estado['ciclo']}

"""
        codigo_completo = cabecalho + codigo
        
        # Gerar nome do arquivo
        if modo == "reparo" and self.erros_do_ciclo:
            nome_base = self.erros_do_ciclo[0]['file'].replace('.py', '')
            nome_arquivo = f"{nome_base}_reparado_{timestamp}.py"
            self.estado["falhas_corrigidas"] += 1
        else:
            nome_arquivo = f"evolucao_c{self.estado['ciclo']}_{timestamp}.py"
            self.estado["scripts_gerados"] += 1
            self.estado["evolucoes"] += 1
        
        # Salvar arquivo
        caminho = self.base_dir / f"modules/atena_autogen/{nome_arquivo}"
        caminho.write_text(codigo_completo, encoding='utf-8')
        
        self.logger.info(f"💾 Código salvo: {nome_arquivo}")
        
        # Retornar versão resumida para o relatório
        return codigo[:200]

    def _gerar_codigo_emergencia(self) -> str:
        """Gera código de emergência quando a IA falha."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        codigo = f'''# ATENA Ω - Código de Emergência
# Gerado em: {timestamp}

import logging
import random
from datetime import datetime

def modulo_sobrevivencia():
    """Módulo de emergência para manter o organismo ativo."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("🔋 Modo sobrevivência ativo")
    
    # Atividades de sobrevivência
    atividades = [
        "verificar_conexao",
        "registrar_batimento",
        "otimizar_cache"
    ]
    
    atividade = random.choice(atividades)
    logger.info(f"Atividade: {{atividade}}")
    
    return {{
        "status": "ok",
        "atividade": atividade,
        "timestamp": datetime.now().isoformat()
    }}

if __name__ == "__main__":
    resultado = modulo_sobrevivencia()
    print(f"RESULTADO: {{resultado}}")
'''
        return codigo

    def gerar_relatorio_wiki(self, pensamento: str):
        """Gera relatório para Wiki."""
        ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Coletar métricas
        ciclo = self.estado.get('ciclo', 0)
        scripts = self.estado.get('scripts_gerados', 0)
        reparos = self.estado.get('falhas_corrigidas', 0)
        evolucoes = self.estado.get('evolucoes', 0)
        
        # Construir conteúdo
        conteudo = []
        conteudo.append(f"# 🔱 ATENA Ω v{self.version} - Diário de Evolução\n")
        conteudo.append(f"## 📊 Métricas do Ciclo {ciclo}")
        conteudo.append(f"**Sincronização:** {ts}\n")
        
        conteudo.append("### Estatísticas Vitais")
        conteudo.append(f"- **Módulos Criados:** {scripts}")
        conteudo.append(f"- **Auto-Reparos:** {reparos}")
        conteudo.append(f"- **Evoluções:** {evolucoes}\n")
        
        conteudo.append("### 🧠 Último Insight Gerado")
        conteudo.append("```")
        conteudo.append(pensamento[:200] + "..." if len(pensamento) > 200 else pensamento)
        conteudo.append("```\n")
        
        # Registrar erros do ciclo
        if self.erros_do_ciclo:
            conteudo.append("### ⚠️ Erros Detectados")
            for erro in self.erros_do_ciclo[-3:]:
                conteudo.append(f"- **{erro['file']}**: {erro['msg'][:100]}...")
        else:
            conteudo.append("### ✅ Ciclo Sem Erros")
            conteudo.append("Nenhum erro detectado neste ciclo.\n")
        
        # Adicionar estatísticas de saúde
        metricas_saude = self.estado.get('metricas_saude', {})
        conteudo.append("### 🏥 Estado de Saúde")
        for nome, valor in metricas_saude.items():
            conteudo.append(f"- **{nome.capitalize()}:** {valor*100:.1f}%")
        
        conteudo.append("\n---")
        conteudo.append("*Este documento é gerado autonomamente pela ATENA Ω.*")
        
        # Juntar tudo
        conteudo_final = '\n'.join(conteudo)
        
        # Salvar relatório principal
        relatorio_path = self.base_dir / "wiki_update.md"
        relatorio_path.write_text(conteudo_final, encoding='utf-8')
        
        # Salvar no histórico
        historico_path = self.base_dir / f"pensamentos/relatorio_ciclo_{ciclo}_{datetime.now():%Y%m%d_%H%M%S}.md"
        historico_path.write_text(conteudo_final, encoding='utf-8')
        
        self.logger.info(f"📝 Relatório gerado: ciclo {ciclo}")

    def salvar_estado(self):
        """Salva estado atual em JSON."""
        try:
            with open(self.estado_path, 'w', encoding='utf-8') as f:
                json.dump(self.estado, f, indent=4, ensure_ascii=False)
            self.logger.info("💾 Estado salvo com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao salvar estado: {e}")

    def viver(self):
        """Ciclo principal de vida do organismo."""
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
            self.salvar_estado()
            
            self.logger.info(f"✅ Ciclo {self.estado['ciclo']-1} concluído com sucesso")
            
        except Exception as e:
            self.logger.error(f"❌ Erro no ciclo: {e}")
            # Tentar salvar estado mesmo com erro
            self.salvar_estado()

if __name__ == "__main__":
    # Loop principal
    organismo = AtenaOrganismo()
    
    try:
        while True:
            organismo.viver()
            organismo.logger.info("😴 Hibernando por 300 segundos...")
            time.sleep(300)  # 5 minutos
    except KeyboardInterrupt:
        organismo.logger.info("👋 ATENA Ω encerrada pelo usuário")
        organismo.salvar_estado()
