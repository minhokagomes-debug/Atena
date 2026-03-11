#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - ATENA PRIMORDIAL v31.0 ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DA CRIAÇÃO"       ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                               ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ ENERGIA = RECURSOS REAIS ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ REGRAS = FÍSICA REAL     ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ EVOLUÇÃO = EMERGENTE     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

🌍 VERSÃO OTIMIZADA PARA 5 MINUTOS DE EXECUÇÃO
"""

import os
import sys
import time
import json
import uuid
import random
import signal
import socket
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import logging

# =========================
# CONFIGURAÇÕES
# =========================
__version__ = "31.0"
__nome__ = "ATENA PRIMORDIAL"

# Diretório local
BASE_DIR = Path(__file__).parent / "atena_mundo"

class Config:
    BASE_DIR = BASE_DIR
    MUNDO_DIR = BASE_DIR / "mundo"
    DNA_DIR = BASE_DIR / "dna"
    LOGS_DIR = BASE_DIR / "logs"
    FOSSEIS_DIR = BASE_DIR / "fosseis"
    
    # Criar diretórios
    for dir_path in [BASE_DIR, MUNDO_DIR, DNA_DIR, LOGS_DIR, FOSSEIS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler(Config.LOGS_DIR / f"atena_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ATENA')

# =========================
# MUNDO
# =========================
class Mundo:
    def __init__(self):
        self.diretorio = Config.MUNDO_DIR
        
        # Limpar mundo anterior
        for f in self.diretorio.glob("*"):
            if f.is_dir():
                import shutil
                shutil.rmtree(f)
            else:
                f.unlink()
        
        # Criar recursos
        self.recursos = []
        for i in range(10):
            path = self.diretorio / f"recurso_{i}.dat"
            tamanho = random.randint(1024, 10240)
            with open(path, 'wb') as f:
                f.write(os.urandom(tamanho))
            self.recursos.append(path)
        
        logger.info(f"🌍 Mundo criado com {len(self.recursos)} recursos")

# =========================
# DNA
# =========================
class DNA:
    def __init__(self, parente: str = None):
        self.id = uuid.uuid4().hex[:16]
        self.parente = parente
        self.geracao = 0 if not parente else 1
        self.comportamentos = {
            'explorar': random.uniform(0.1, 0.9),
            'criar': random.uniform(0.1, 0.9),
            'reproduzir': random.uniform(0.1, 0.9),
            'agressividade': random.uniform(0.1, 0.9)
        }
        self.arquivo = Config.DNA_DIR / f"dna_{self.id}.py"
        self._salvar()
    
    def _salvar(self):
        with open(self.arquivo, 'w') as f:
            f.write(f'''#!/usr/bin/env python3
import os, sys, time, random, socket
from pathlib import Path

ID = "{self.id}"
COMP = {self.comportamentos}
MUNDO = Path("{Config.MUNDO_DIR}")
MEU_DIR = MUNDO / ID

def main():
    MEU_DIR.mkdir(exist_ok=True)
    fim = time.time() + 300  # 5 minutos
    
    while time.time() < fim:
        r = random.random()
        
        if r < COMP['explorar']:
            recursos = list(MUNDO.glob("recurso_*.dat"))
            if recursos:
                rsrc = random.choice(recursos)
                rsrc.rename(MEU_DIR / rsrc.name)
                print(f"[{{os.getpid()}}] 📦 Explorou")
        
        elif r < COMP['explorar'] + COMP['criar']:
            path = MEU_DIR / f"criado_{{random.randint(1000,9999)}}.dat"
            with open(path, 'wb') as f:
                f.write(os.urandom(512))
            print(f"[{{os.getpid()}}] 📝 Criou")
        
        elif r < 0.8:
            pid = os.fork()
            if pid == 0:
                print(f"[{{os.getpid()}}] 🍼 Filho")
                sys.exit(0)
        
        time.sleep(0.1)

if __name__ == "__main__":
    main()
''')
    
    def mutar(self):
        filho = DNA(parente=self.id)
        for trait in filho.comportamentos:
            if random.random() < 0.3:
                delta = random.gauss(0, 0.2)
                filho.comportamentos[trait] = max(0.1, min(0.9, 
                    self.comportamentos[trait] + delta))
        filho.geracao = self.geracao + 1
        return filho

# =========================
# ORGANISMO
# =========================
class Organismo:
    def __init__(self, dna: DNA, mundo: Mundo):
        self.pid = os.getpid()
        self.dna = dna
        self.mundo = mundo
        self.nascimento = datetime.now()
        logger.info(f"[{self.pid}] 🧬 Organismo {self.dna.id[:8]} nascido")
    
    def executar(self):
        try:
            proc = subprocess.Popen(
                [sys.executable, str(self.dna.arquivo)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return proc
        except Exception as e:
            logger.error(f"[{self.pid}] Erro: {e}")
            return None

# =========================
# ECOSSISTEMA
# =========================
class Ecossistema:
    def __init__(self):
        self.mundo = Mundo()
        self.organismos = {}
        self.dnas = {}
        self.inicio = datetime.now()
        logger.info(f"\n{'='*60}")
        logger.info("🌍 ECOSSISTEMA INICIADO")
        logger.info(f"{'='*60}")
    
    def criar_vida(self, quantidade: int = 3):
        logger.info(f"\n🌱 Criando {quantidade} organismos...")
        
        for i in range(quantidade):
            dna = DNA()
            self.dnas[dna.id] = dna
            
            pid = os.fork()
            
            if pid == 0:
                org = Organismo(dna, self.mundo)
                proc = org.executar()
                if proc:
                    proc.wait()
                sys.exit(0)
            else:
                self.organismos[pid] = {
                    'pid': pid,
                    'dna_id': dna.id,
                    'nascimento': datetime.now()
                }
                logger.info(f"   ✅ Organismo {i+1} (PID {pid})")
                time.sleep(1)
    
    def observar(self, duracao_segundos: int = 300):  # 5 minutos
        logger.info(f"\n📊 Observando por {duracao_segundos//60} minutos...")
        
        fim = time.time() + duracao_segundos
        ultimo_log = 0
        
        while time.time() < fim:
            time.sleep(10)
            
            # Verificar mortes
            for pid in list(self.organismos.keys()):
                try:
                    os.kill(pid, 0)
                except:
                    idade = (datetime.now() - self.organismos[pid]['nascimento']).seconds
                    dna_id = self.organismos[pid]['dna_id']
                    logger.info(f"💀 PID {pid} (DNA {dna_id[:8]}) morreu após {idade}s")
                    
                    # Criar fóssil
                    fossil = {
                        'pid': pid,
                        'dna_id': dna_id,
                        'nascimento': self.organismos[pid]['nascimento'].isoformat(),
                        'morte': datetime.now().isoformat(),
                        'idade': idade
                    }
                    fossil_file = Config.FOSSEIS_DIR / f"fossil_{pid}.json"
                    with open(fossil_file, 'w') as f:
                        json.dump(fossil, f, indent=2)
                    
                    del self.organismos[pid]
            
            # Log a cada 30 segundos
            if time.time() - ultimo_log > 30:
                logger.info(f"📊 População: {len(self.organismos)} | "
                          f"Fósseis: {len(list(Config.FOSSEIS_DIR.glob('*.json')))}")
                ultimo_log = time.time()
    
    def encerrar(self):
        logger.info("\n📊 ENCERRANDO ECOSSISTEMA...")
        
        for pid in list(self.organismos.keys()):
            try:
                os.kill(pid, signal.SIGTERM)
            except:
                pass
        
        duracao = (datetime.now() - self.inicio).seconds
        fosseis = len(list(Config.FOSSEIS_DIR.glob('*.json')))
        
        logger.info(f"\n{'='*60}")
        logger.info("📊 RELATÓRIO FINAL")
        logger.info(f"{'='*60}")
        logger.info(f"⏱️  Duração: {duracao//60}min {duracao%60}s")
        logger.info(f"🧬 Organismos criados: {len(self.dnas)}")
        logger.info(f"🦴 Fósseis: {fosseis}")
        logger.info(f"📁 Mundo: {Config.MUNDO_DIR}")

# =========================
# MAIN
# =========================
def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - PRIMORDIAL v31.0 ║
    ║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DA CRIAÇÃO"  ║
    ║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                           ║
    ║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ 5 MINUTOS DE VIDA   ║
    ║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ OTIMIZADO PARA CI/CD║
    ║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ SEM DEPENDÊNCIAS     ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    📁 Diretório: {Config.BASE_DIR}
    ⏱️  Tempo: 5 minutos
    
    """)
    
    eco = Ecossistema()
    eco.criar_vida(quantidade=3)
    eco.observar(duracao_segundos=300)  # 5 minutos
    eco.encerrar()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n👋 Encerrado")
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
