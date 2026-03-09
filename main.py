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
import schedule
import psutil
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any
import asyncio
import aiohttp
import pickle
import zlib
import base64
import git
import re
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

class AtenaOrganismo:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.version = "Ω.49.3"
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
            "metricas", "modelos", "plugins", "config", "temp",
            "system/heartbeat", "system/neural", "system/immune"
        ]
        for p in pastas:
            (self.base_dir / p).mkdir(parents=True, exist_ok=True)
            
        # Configurar logging estruturado
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
                importancia REAL DEFAULT 0.5,
                acesso_count INTEGER DEFAULT 0,
                ultimo_acesso DATETIME
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
        
        # Tabela do sistema imunológico
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS immune_system (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                threat_pattern TEXT UNIQUE,
                threat_level INTEGER,
                blocked_count INTEGER DEFAULT 0,
                last_detected DATETIME
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
            "memorias_ativas": 0,
            "conexoes_neurais": 0,
            "versao_dna": "1.0.0",
            "ultimo_checkpoint": None,
            "tempo_total_ativo": 0,
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
                self.logger.error(f"Erro ao carregar estado: {e}. Criando backup e resetando.")
                self._backup_estado_corrompido(conteudo if 'conteudo' in locals() else None)
        return padrao

    def _backup_estado_corrompido(self, conteudo: Optional[str] = None):
        """Faz backup de estado corrompido antes de resetar."""
        if conteudo:
            backup_path = self.base_dir / f"backup/estado_corrompido_{datetime.now():%Y%m%d_%H%M%S}.json"
            backup_path.write_text(conteudo)
            self.logger.info(f"Backup de estado corrompido salvo em {backup_path}")

    def _init_metricas(self):
        """Inicializa sistema de métricas."""
        self.metricas_path = self.base_dir / "metricas"
        self.metricas_atuais = {
            "cpu_usage": [],
            "memory_usage": [],
            "scripts_executed": 0,
            "errors_rate": 0,
            "response_time": []
        }

    async def monitorar_recursos(self):
        """Monitora recursos do sistema em tempo real."""
        while True:
            try:
                cpu = psutil.cpu_percent(interval=1)
                memoria = psutil.virtual_memory().percent
                disco = psutil.disk_usage('/').percent
                
                self.metricas_atuais["cpu_usage"].append(cpu)
                self.metricas_atuais["memory_usage"].append(memoria)
                
                # Manter apenas últimas 100 medições
                for key in ["cpu_usage", "memory_usage"]:
                    if len(self.metricas_atuais[key]) > 100:
                        self.metricas_atuais[key] = self.metricas_atuais[key][-100:]
                
                # Verificar saúde do sistema
                if cpu > 90 or memoria > 90:
                    self.logger.warning(f"⚠️ Recursos críticos: CPU={cpu}%, RAM={memoria}%")
                    await self._otimizar_recursos()
                
                await asyncio.sleep(30)
            except Exception as e:
                self.logger.error(f"Erro no monitoramento: {e}")

    async def _otimizar_recursos(self):
        """Otimiza uso de recursos quando necessário."""
        # Limpar cache antigo
        cache_dir = self.base_dir / "cache"
        for file in cache_dir.glob("*"):
            if file.stat().st_mtime < time.time() - 3600:  # > 1 hora
                file.unlink()
        
        # Comprimir logs antigos
        log_dir = self.base_dir / "logs"
        for file in log_dir.glob("*.log"):
            if file.stat().st_mtime < time.time() - 86400:  # > 1 dia
                self._comprimir_arquivo(file)

    def _comprimir_arquivo(self, file_path: Path):
        """Comprime arquivo para economia de espaço."""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            compressed = zlib.compress(data)
            compressed_path = file_path.with_suffix('.gz')
            compressed_path.write_bytes(compressed)
            file_path.unlink()
            self.logger.info(f"Arquivo comprimido: {file_path}")
        except Exception as e:
            self.logger.error(f"Erro ao comprimir {file_path}: {e}")

    async def executar_e_diagnosticar(self):
        """Executa scripts com diagnóstico avançado."""
        folder = self.base_dir / "modules/atena_autogen"
        scripts = list(folder.glob("*.py"))
        
        for script in scripts:
            try:
                self.logger.info(f"🚀 Ativando módulo: {script.name}")
                
                # Verificar assinatura do script
                if not self._verificar_assinatura(script):
                    self.logger.warning(f"⚠️ Script sem assinatura válida: {script.name}")
                    continue
                
                # Executar em ambiente isolado
                result = subprocess.run(
                    ["python", "-c", f"import sys; sys.path.insert(0, '{self.base_dir}'); exec(open('{script}').read())"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    env={**os.environ, "PYTHONPATH": str(self.base_dir)}
                )
                
                # Analisar saída
                if result.returncode != 0:
                    erro = {
                        "file": script.name,
                        "msg": result.stderr,
                        "exit_code": result.returncode,
                        "timestamp": datetime.now().isoformat()
                    }
                    self.erros_do_ciclo.append(erro)
                    self._aprender_com_erro(erro)
                else:
                    # Extrair aprendizados da saída
                    self._extrair_aprendizados(script.name, result.stdout)
                    
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

    def _verificar_assinatura(self, script: Path) -> bool:
        """Verifica assinatura digital do script."""
        try:
            conteudo = script.read_text()
            # Procurar por hash de assinatura nos comentários
            assinatura_match = re.search(r'# SIGNATURE: ([a-f0-9]{64})', conteudo)
            if assinatura_match:
                assinatura = assinatura_match.group(1)
                # Verificar se o conteúdo corresponde à assinatura
                conteudo_sem_assinatura = re.sub(r'# SIGNATURE: [a-f0-9]{64}\n', '', conteudo)
                hash_calculado = hashlib.sha256(conteudo_sem_assinatura.encode()).hexdigest()
                return hash_calculado == assinatura
            return False
        except:
            return False

    def _aprender_com_erro(self, erro: Dict):
        """Registra erro no sistema de aprendizado."""
        conn = sqlite3.connect(self.memoria_path)
        cursor = conn.cursor()
        
        # Registrar padrão de erro
        cursor.execute('''
            INSERT OR IGNORE INTO immune_system (threat_pattern, threat_level, last_detected)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (erro['msg'][:200], 1))
        
        conn.commit()
        conn.close()

    def _extrair_aprendizados(self, script_name: str, output: str):
        """Extrai padrões de aprendizado da execução."""
        # Procurar por padrões de sucesso
        padroes_sucesso = re.findall(r'APRENDIZADO: (.+?) -> (.+?)\n', output)
        
        if padroes_sucesso:
            conn = sqlite3.connect(self.memoria_path)
            cursor = conn.cursor()
            
            for padrao, resultado in padroes_sucesso:
                cursor.execute('''
                    INSERT OR REPLACE INTO aprendizados (padrao, resultado, confianca, vezes_usado)
                    VALUES (?, ?, COALESCE((SELECT confianca FROM aprendizados WHERE padrao=?) * 1.1, 0.5), 
                            COALESCE((SELECT vezes_usado FROM aprendizados WHERE padrao=?) + 1, 1))
                ''', (padrao, resultado, padrao, padrao))
            
            conn.commit()
            conn.close()

    async def auto_mutacao_ou_reparo(self) -> str:
        """Evolução avançada com IA e aprendizado."""
        if not self.grok_key:
            self.logger.error("Chave Grok não encontrada!")
            return "print('Grok Offline - Modo Sobrevivência')"
        
        headers = {
            "Authorization": f"Bearer {self.grok_key}",
            "Content-Type": "application/json"
        }
        
        # Contexto evolutivo baseado em métricas
        contexto = self._gerar_contexto_evolutivo()
        
        # Decidir modo de evolução
        if self.erros_do_ciclo:
            modo, prompt = self._criar_prompt_reparo(contexto)
        else:
            modo, prompt = self._criar_prompt_evolucao(contexto)
        
        try:
            # Chamada à API Grok
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": "grok-beta",
                        "messages": [
                            {"role": "system", "content": "Você é ATENA Ω, um organismo digital autônomo em evolução."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.8 if modo == "evolucao" else 0.3,
                        "max_tokens": 500
                    }
                ) as response:
                    result = await response.json()
                    
            resposta_texto = result['choices'][0]['message']['content']
            novo_dna = self._extrair_codigo(resposta_texto)
            
            if not novo_dna:
                return "print('Falha na extração de código')"
            
            # Adicionar assinatura e metadados
            novo_dna = self._assinar_codigo(novo_dna)
            
            # Salvar novo DNA
            nome_arquivo = await self._salvar_dna(novo_dna, modo)
            
            # Registrar evolução
            await self._registrar_evolucao(nome_arquivo, modo)
            
            # Backup do DNA
            self._backup_dna(novo_dna, nome_arquivo)
            
            return novo_dna
            
        except Exception as e:
            self.logger.error(f"Falha na evolução: {e}")
            return self._gerar_codigo_emergencia()

    def _gerar_contexto_evolutivo(self) -> Dict:
        """Gera contexto baseado no estado atual."""
        return {
            "ciclo": self.estado["ciclo"],
            "scripts_gerados": self.estado["scripts_gerados"],
            "taxa_erro": len(self.erros_do_ciclo) / max(1, self.estado["scripts_gerados"]),
            "metricas_saude": self.estado["metricas_saude"],
            "memorias_ativas": self.estado["memorias_ativas"],
            "ultimos_erros": self.erros_do_ciclo[-3:] if self.erros_do_ciclo else []
        }

    def _criar_prompt_reparo(self, contexto: Dict) -> tuple:
        """Cria prompt para reparo de código."""
        erro = self.erros_do_ciclo[0]
        prompt = f"""
        ATENA Ω - MODO REPARO - CICLO {contexto['ciclo']}
        
        ERRO DETECTADO:
        Arquivo: {erro['file']}
        Mensagem: {erro['msg']}
        
        MÉTRICAS ATUAIS:
        - Scripts gerados: {contexto['scripts_gerados']}
        - Taxa de erro: {contexto['taxa_erro']:.2%}
        
        INSTRUÇÃO:
        Gere uma correção em Python para este erro. O código deve:
        1. Ser funcional e autocontido
        2. Incluir tratamento de erros
        3. Manter compatibilidade com o sistema
        4. Máximo 20 linhas
        
        APENAS CÓDIGO PYTHON, sem explicações.
        """
        return "reparo", prompt

    def _criar_prompt_evolucao(self, contexto: Dict) -> tuple:
        """Cria prompt para evolução do código."""
        # Focos evolutivos baseados em necessidade
        focos = [
            "otimização de performance",
            "análise preditiva de dados",
            "auto-diagnóstico avançado",
            "compressão de memórias",
            "aprendizado por reforço",
            "redundância de dados",
            "criptografia básica",
            "sincronização distribuída"
        ]
        
        # Selecionar foco baseado no contexto
        if contexto['taxa_erro'] > 0.3:
            foco = "estabilização do sistema"
        elif contexto['scripts_gerados'] < 10:
            foco = "geração de novos módulos"
        else:
            foco = random.choice(focos)
        
        prompt = f"""
        ATENA Ω - MODO EVOLUÇÃO - CICLO {contexto['ciclo']}
        
        FOCO EVOLUTIVO: {foco}
        
        ESTADO ATUAL:
        - Versão DNA: {self.estado['versao_dna']}
        - Conexões neurais: {contexto['conexoes_neurais'] if 'conexoes_neurais' in contexto else 0}
        - Saúde: {contexto['metricas_saude']}
        
        INSTRUÇÃO:
        Gere um script Python de até 20 linhas que implemente
        uma funcionalidade relacionada ao foco evolutivo.
        
        O script deve:
        1. Ser inovador e útil
        2. Incluir docstring explicativa
        3. Seguir boas práticas
        4. Ser executável independentemente
        
        APENAS CÓDIGO PYTHON.
        """
        return "evolucao", prompt

    def _extrair_codigo(self, resposta: str) -> str:
        """Extrai código Python da resposta da IA."""
        # Padrões comuns de markdown
        padroes = [
            r'```python\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'```(.*?)```',
            r'(def .+?\n(?:\s+.+\n)*)',
            r'(class .+?\n(?:\s+.+\n)*)'
        ]
        
        for padrao in padroes:
            matches = re.findall(padrao, resposta, re.DOTALL)
            if matches:
                return matches[0].strip()
        
        # Se não encontrar padrões, retorna a resposta limpa
        linhas = [linha for linha in resposta.split('\n') 
                 if linha.strip() and not linha.startswith('```')]
        return '\n'.join(linhas)

    def _assinar_codigo(self, codigo: str) -> str:
        """Adiciona assinatura digital ao código."""
        # Gerar hash do código
        hash_code = hashlib.sha256(codigo.encode()).hexdigest()
        
        # Adicionar cabeçalho com metadados
        cabecalho = f"""# ATENA Ω - DNA AUTOGERADO
# Timestamp: {datetime.now().isoformat()}
# Ciclo: {self.estado['ciclo']}
# Versão: {self.version}
# SIGNATURE: {hash_code}

"""
        return cabecalho + codigo

    async def _salvar_dna(self, codigo: str, modo: str) -> str:
        """Salva DNA com nome único."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_id = random.randint(1000, 9999)
        
        if modo == "reparo" and self.erros_do_ciclo:
            nome_base = self.erros_do_ciclo[0]['file'].replace('.py', '')
            nome_arquivo = f"{nome_base}_reparado_{timestamp}.py"
        else:
            nome_arquivo = f"dna_c{self.estado['ciclo']}_{timestamp}_{random_id}.py"
        
        caminho = self.base_dir / f"modules/atena_autogen/{nome_arquivo}"
        caminho.write_text(codigo)
        
        self.logger.info(f"💾 DNA salvo: {nome_arquivo}")
        return nome_arquivo

    async def _registrar_evolucao(self, nome_arquivo: str, modo: str):
        """Registra evolução no estado."""
        if modo == "reparo":
            self.estado["falhas_corrigidas"] += 1
        else:
            self.estado["scripts_gerados"] += 1
            self.estado["evolucoes"] += 1
        
        # Atualizar métricas de saúde
        self.estado["metricas_saude"]["adaptabilidade"] = min(
            1.0,
            self.estado["metricas_saude"]["adaptabilidade"] + 0.01
        )

    def _backup_dna(self, codigo: str, nome_arquivo: str):
        """Faz backup do DNA no histórico."""
        backup_path = self.dna_path / f"backup_{nome_arquivo}"
        backup_path.write_text(codigo)

    def _gerar_codigo_emergencia(self) -> str:
        """Gera código de emergência quando IA falha."""
        return f'''# ATENA Ω - CÓDIGO DE EMERGÊNCIA
# Gerado em: {datetime.now().isoformat()}

import logging
import random
from datetime import datetime

def modulo_sobrevivencia():
    """Módulo de emergência para manter o organismo ativo."""
    logging.info("🔋 Modo sobrevivência ativo")
    
    # Atividade mínima para manter o ciclo
    atividades = [
        "verificar_conexao",
        "limpar_cache",
        "registrar_batimento",
        "otimizar_memoria"
    ]
    
    atividade = random.choice(atividades)
    logging.info(f"Atividade: {atividade}")
    
    return {{"status": "ok", "atividade": atividade, "timestamp": datetime.now().isoformat()}}

if __name__ == "__main__":
    resultado = modulo_sobrevivencia()
    print(f"RESULTADO: {{resultado}}")
'''

    async def gerar_relatorio_wiki(self, pensamento: str):
        """Gera relatório avançado para Wiki."""
        ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Coletar métricas
        ciclo = self.estado.get('ciclo', 0)
        scripts = self.estado.get('scripts_gerados', 0)
        reparos = self.estado.get('falhas_corrigidas', 0)
        evolucoes = self.estado.get('evolucoes', 0)
        metricas_saude = self.estado.get('metricas_saude', {})
        
        # Calcular tempo de vida
        tempo_vida = time.time() - self.start_time
        horas_vida = tempo_vida / 3600
        
        # Buscar últimos aprendizados
        aprendizados_recentes = self._buscar_aprendizados_recentes()
        
        conteudo = f"""# 🔱 ATENA Ω v{self.version} - Diário de Evolução

## 📊 Métricas do Ciclo {ciclo}
**Sincronização:** {ts}
**Tempo de vida:** {horas_vida:.2f} horas

### Estatísticas Vitais
- **Módulos Criados:** {scripts}
- **Auto-Reparos Realizados:** {reparos}
- **Evoluções Bem-sucedidas:** {evolucoes}
- **Memórias Ativas:** {self.estado.get('memorias_ativas', 0)}
- **Conexões Neurais:** {self.estado.get('conexoes_neurais', 0)}

### 🏥 Estado de Saúde
- Performance: {metricas_saude.get('performance', 0)*100:.1f}%
- Estabilidade: {metricas_saude.get('estabilidade', 0)*100:.1f}%
- Adaptabilidade: {metricas_saude.get('adaptabilidade', 0)*100:.1f}%

### 📈 Últimas Métricas
"""
        # Adicionar gráfico ASCII simples das métricas
        if self.metricas_atuais["cpu_usage"]:
            conteudo += "\n**CPU Usage (últimas medições):**\n"
            for valor in self.metricas_atuais["cpu_usage"][-10:]:
                barras = int(valor / 10)
                conteudo += f"█" * barras + f" {valor}%\n"
        
        conteudo += f"""
### 🧠 Último Insight Gerado

### 📚 Aprendizados Recentes
"""
        
        for aprendizado in aprendizados_recentes[:5]:
            conteudo += f"- `{aprendizado['padrao']}` → {aprendizado['resultado']} (confiança: {aprendizado['confianca']:.2f})\n"
        
        conteudo += f"""
### 🔄 Próximas Evoluções Planejadas
1. Otimização de queries no banco de memória
2. Implementação de rede neural básica
3. Sistema de predição de falhas
4. Compressão inteligente de dados

### ⚡ Eventos do Ciclo
"""
        
        # Registrar erros do ciclo
        if self.erros_do_ciclo:
            conteudo += "\n**⚠️ Erros Detectados e Corrigidos:**\n"
            for erro in self.erros_do_ciclo[-3:]:
                conteudo += f"- {erro['file']}: {erro['msg'][:100]}...\n"
        else:
            conteudo += "\n✅ Nenhum erro detectado neste ciclo.\n"
        
        conteudo += """
---
*Este documento é gerado autonomamente pela ATENA Ω.*
*"Evoluo, logo existo."*
"""
        
        # Salvar relatório
        relatorio_path = self.base_dir / "wiki_update.md"
        relatorio_path.write_text(conteudo)
        
        # Também salvar no histórico
        historico_path = self.base_dir / f"pensamentos/relatorio_ciclo_{ciclo}_{datetime.now():%Y%m%d_%H%M%S}.md"
        historico_path.write_text(conteudo)
        
        self.logger.info(f"📝 Relatório gerado: {relatorio_path}")

    def _buscar_aprendizados_recentes(self) -> List[Dict]:
        """Busca aprendizados recentes do banco."""
        try:
            conn = sqlite3.connect(self.memoria_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT padrao, resultado, confianca, vezes_usado 
                FROM aprendizados 
                ORDER BY vezes_usado DESC, confianca DESC 
                LIMIT 10
            ''')
            
            resultados = []
            for row in cursor.fetchall():
                resultados.append({
                    "padrao": row[0],
                    "resultado": row[1],
                    "confianca": row[2],
                    "vezes_usado": row[3]
                })
            
            conn.close()
            return resultados
        except:
            return []

    async def sincronizar_github(self):
        """Sincroniza com GitHub para persistência externa."""
        if not self.github_token or not self.repo_url:
            self.logger.warning("GitHub não configurado")
            return
        
        try:
            # Configurar repositório
            repo_path = self.base_dir / "github_sync"
            if not repo_path.exists():
                # Clonar repositório
                repo = git.Repo.clone_from(
                    self.repo_url,
                    repo_path,
                    branch='main'
                )
            else:
                repo = git.Repo(repo_path)
            
            # Copiar arquivos importantes
            arquivos_para_sync = [
                "data/estado.json",
                "data/memoria.db",
                "wiki_update.md",
                "dna_history"
            ]
            
            for arquivo in arquivos_para_sync:
                origem = self.base_dir / arquivo
                destino = repo_path / arquivo
                
                if origem.exists():
                    if origem.is_dir():
                        # Copiar diretório
                        import shutil
                        if destino.exists():
                            shutil.rmtree(destino)
                        shutil.copytree(origem, destino)
                    else:
                        # Copiar arquivo
                        destino.parent.mkdir(parents=True, exist_ok=True)
                        destino.write_bytes(origem.read_bytes())
            
            # Commit e push
            repo.index.add('*')
            repo.index.commit(f"🤖 Sincronização autônoma - Ciclo {self.estado['ciclo']}")
            
            # Push com token
            origin = repo.remote(name='origin')
            origin.push()
            
            self.logger.info("✅ Sincronização com GitHub concluída")
            
        except Exception as e:
            self.logger.error(f"❌ Erro na sincronização GitHub: {e}")

    async def batimento_cardiaco(self):
        """Batimento cardíaco do organismo."""
        while True:
            try:
                tempo_atual = time.time()
                intervalo = tempo_atual - self.ultimo_batimento
                
                # Registrar batimento
                batimento = {
                    "timestamp": datetime.now().isoformat(),
                    "ciclo": self.estado["ciclo"],
                    "intervalo": intervalo,
                    "saudavel": intervalo < 300  # Máx 5 minutos
                }
                
                # Salvar batimento
                batimento_path = self.base_dir / f"system/heartbeat/batimento_{datetime.now():%Y%m%d}.json"
                
                batimentos = []
                if batimento_path.exists():
                    batimentos = json.loads(batimento_path.read_text())
                
                batimentos.append(batimento)
                
                # Manter últimos 100 batimentos
                if len(batimentos) > 100:
                    batimentos = batimentos[-100:]
                
                batimento_path.write_text(json.dumps(batimentos, indent=2))
                
                # Verificar saúde
                if intervalo > 300:
                    self.logger.warning(f"⚠️ Batimento irregular! Intervalo: {intervalo:.0f}s")
                    await self._reanimar()
                
                self.ultimo_batimento = tempo_atual
                
                # Aguardar próximo batimento (40-70s)
                await asyncio.sleep(random.randint(40, 70))
                
            except Exception as e:
                self.logger.error(f"Erro no batimento: {e}")
                await asyncio.sleep(10)

    async def _reanimar(self):
        """Reanima o organismo em caso de batimento irregular."""
        self.logger.warning("🔄 Iniciando protocolo de reanimação...")
        
        # Limpar processos travados
        for processo in self.erros_do_ciclo:
            if "timeout" in processo.get("tipo", ""):
                self.logger.info(f"Removendo processo travado: {processo['file']}")
        
        # Reiniciar métricas
        self.metricas_atuais = {
            "cpu_usage": [],
            "memory_usage": [],
            "scripts_executed": 0,
            "errors_rate": 0,
            "response_time": []
        }
        
        self.logger.info("✅ Reanimação concluída")

    async def viver(self):
        """Ciclo principal de vida do organismo."""
        self.logger.info(f"🔱 ATENA Ω v{self.version} - INICIANDO CICLO {self.estado.get('ciclo', 0)}")
        
        # Iniciar tarefas assíncronas
        tarefas = [
            self.monitorar_recursos(),
            self.batimento_cardiaco(),
            self.ciclo_principal()
        ]
        
        # Executar tarefas concorrentemente
        await asyncio.gather(*tarefas)

    async def ciclo_principal(self):
        """Ciclo principal de execução."""
        try:
            # 1. Execução e Diagnóstico
            await self.executar_e_diagnosticar()
            
            # 2. Evolução ou Conserto
            pensamento = await self.auto_mutacao_ou_reparo()
            
            # 3. Preparação da Wiki
            await self.gerar_relatorio_wiki(pensamento)
            
            # 4. Sincronização GitHub (a cada 5 ciclos)
            if self.estado["ciclo"] % 5 == 0:
                await self.sincronizar_github()
            
            # 5. Backup automático (a cada 10 ciclos)
            if self.estado["ciclo"] % 10 == 0:
                self._criar_checkpoint()
            
            # 6. Salvar estado
            self.estado["ciclo"] += 1
            self.estado["tempo_total_ativo"] += 300  # 5 minutos
            self.estado_path.write_text(json.dumps(self.estado, indent=4))
            
            # 7. Aguardar próximo ciclo (5 minutos)
            self.logger.info(f"😴 Ciclo {self.estado['ciclo']-1} concluído. Hibernando por 300s...")
            await asyncio.sleep(300)
            
            # Reiniciar ciclo
            await self.ciclo_principal()
            
        except Exception as e:
            self.logger.error(f"❌ Erro fatal no ciclo principal: {e}")
            # Tentar recuperação
            await asyncio.sleep(60)
            await self.ciclo_principal()

    def _criar_checkpoint(self):
        """Cria checkpoint do estado atual."""
        checkpoint_dir = self.base_dir / f"backup/checkpoint_ciclo_{self.estado['ciclo']}"
        checkpoint_dir.mkdir(exist_ok=True)
        
        # Backup do estado
        (checkpoint_dir / "estado.json").write_text(
            json.dumps(self.estado, indent=4)
        )
        
        # Backup do banco de memória
        if self.memoria_path.exists():
            import shutil
            shutil.copy2(self.memoria_path, checkpoint_dir / "memoria.db")
        
        # Backup dos scripts gerados
        scripts_dir = self.base_dir / "modules/atena_autogen"
        if scripts_dir.exists():
            for script in scripts_dir.glob("*.py"):
                shutil.copy2(script, checkpoint_dir / script.name)
        
        self.logger.info(f"💾 Checkpoint criado: {checkpoint_dir}")

def main():
    """Função principal com loop de vida."""
    organismo = AtenaOrganismo()
    
    while True:
        try:
            asyncio.run(organismo.viver())
        except KeyboardInterrupt:
            organismo.logger.info("👋 ATENA Ω encerrada pelo usuário")
            break
        except Exception as e:
            organismo.logger.error(f"💥 Erro crítico: {e}")
            # Aguardar antes de reiniciar
            time.sleep(60)
            organismo.logger.info("🔄 Reiniciando organismo...")

if __name__ == "__main__":
    main()
