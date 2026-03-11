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

🌍 ISTO NÃO TEM "ENERGIA" - TEM RECURSOS REAIS
🌍 ISTO NÃO TEM "REGRAS" - TEM FÍSICA DO SISTEMA
🌍 ISTO NÃO TEM "EVOLUÇÃO PROGRAMADA" - ELA SURGE

Cada organismo é um processo REAL que:
✅ Precisa de CPU para existir (se não roda, não vive)
✅ Precisa de RAM para pensar (se não tem, morre)
✅ Precisa de disco para armazenar (se não tem, esquece)
✅ Precisa de rede para comunicar (se não tem, isolado)

A "ENERGIA" DELES É O DIREITO DE EXISTIR NO SISTEMA
As "REGRAS" SÃO IMPOSTAS PELO KERNEL DO LINUX
A "EVOLUÇÃO" SURGE DA COMPETIÇÃO POR RECURSOS REAIS
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
from datetime import datetime
from typing import List, Dict, Optional, Any
import logging

# =========================
# CONFIGURAÇÕES - USANDO DIRETÓRIO LOCAL
# =========================
__version__ = "31.0"
__nome__ = "ATENA PRIMORDIAL"

# Usar diretório local em vez de /var/atena
BASE_DIR = Path(__file__).parent / "atena_mundo"

class ConfigPrimordial:
    """Configurações usando diretório local (sem precisar de root)"""
    
    # Diretórios locais
    BASE_DIR = BASE_DIR
    MUNDO_DIR = BASE_DIR / "mundo"
    DNA_DIR = BASE_DIR / "dna"
    LOGS_DIR = BASE_DIR / "logs"
    FOSSEIS_DIR = BASE_DIR / "fosseis"
    
    # Criar diretórios
    for dir_path in [BASE_DIR, MUNDO_DIR, DNA_DIR, LOGS_DIR, FOSSEIS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('ATENA-PRIMORDIAL')

# =========================
# MUNDO REAL - USANDO DIRETÓRIO LOCAL
# =========================
class MundoPrimordial:
    """O mundo real dos organismos (em diretório local)"""
    
    def __init__(self):
        self.diretorio = ConfigPrimordial.MUNDO_DIR
        
        # Limpar mundo anterior se existir
        for f in self.diretorio.glob("*"):
            if f.is_dir():
                import shutil
                shutil.rmtree(f)
            else:
                f.unlink()
        
        # Criar recursos iniciais
        self.recursos = []
        for i in range(5):  # Menos recursos para GitHub Actions
            path = self.diretorio / f"recurso_{i}.dat"
            tamanho = random.randint(1024, 5120)  # 1KB a 5KB
            with open(path, 'wb') as f:
                f.write(os.urandom(tamanho))
            self.recursos.append({
                'path': path,
                'tamanho': tamanho,
                'descoberto': False
            })
        
        logger.info(f"🌍 Mundo criado em {self.diretorio}")
        logger.info(f"   Recursos: {len(self.recursos)}")

# =========================
# DNA - CÓDIGO GENÉTICO
# =========================
class DNA:
    """DNA do organismo - define comportamento"""
    
    def __init__(self, parente: str = None):
        self.id = uuid.uuid4().hex[:16]
        self.parente = parente
        self.geracao = 0 if not parente else 1
        self.comportamentos = self._gerar_comportamentos()
        self.arquivo = ConfigPrimordial.DNA_DIR / f"dna_{self.id}.py"
        self._salvar()
    
    def _gerar_comportamentos(self) -> Dict[str, float]:
        """Gera comportamentos aleatórios"""
        return {
            'explorar': random.uniform(0.1, 0.9),
            'criar': random.uniform(0.1, 0.9),
            'comunicar': random.uniform(0.1, 0.9),
            'reproduzir': random.uniform(0.1, 0.9),
            'agressividade': random.uniform(0.1, 0.9),
            'curiosidade': random.uniform(0.1, 0.9),
            'preguica': random.uniform(0.1, 0.9)
        }
    
    def _salvar(self):
        """Salva DNA em arquivo"""
        with open(self.arquivo, 'w') as f:
            f.write(f'''#!/usr/bin/env python3
"""
ORGANISMO COM DNA {self.id}
"""

import os
import sys
import time
import random
import socket
from pathlib import Path

# IDENTIDADE
MEU_ID = "{self.id}"
MEU_PID = os.getpid()

# COMPORTAMENTOS
COMPORTAMENTOS = {self.comportamentos}

# DIRETÓRIOS
MUNDO_DIR = Path("{ConfigPrimordial.MUNDO_DIR}")
MEU_DIR = MUNDO_DIR / MEU_ID

def explorar():
    """Explora o mundo"""
    try:
        MEU_DIR.mkdir(exist_ok=True)
        recursos = list(MUNDO_DIR.glob("recurso_*.dat"))
        if recursos:
            recurso = random.choice(recursos)
            destino = MEU_DIR / recurso.name
            recurso.rename(destino)
            print(f"[{{MEU_PID}}] 📦 Pegou recurso")
            return True
    except:
        pass
    return False

def criar():
    """Cria algo novo"""
    try:
        MEU_DIR.mkdir(exist_ok=True)
        nome = f"criado_{{random.randint(1000,9999)}}.dat"
        path = MEU_DIR / nome
        with open(path, 'wb') as f:
            f.write(os.urandom(512))
        print(f"[{{MEU_PID}}] 📝 Criou arquivo")
        return True
    except:
        return False

def comunicar():
    """Tenta se comunicar"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        msg = f"ATENA-{{MEU_ID}}".encode()
        sock.sendto(msg, ('255.255.255.255', 8888))
        sock.close()
        print(f"[{{MEU_PID}}] 📡 Broadcast enviado")
        return True
    except:
        return False

def reproduzir():
    """Tenta criar filho"""
    try:
        pid = os.fork()
        if pid == 0:
            print(f"[{{MEU_PID}}] 🍼 Filho criado")
            return True
        return True
    except:
        return False

def main():
    print(f"[{{MEU_PID}}] 🧬 Organismo nasceu")
    
    acoes = 0
    ultima_acao = time.time()
    
    while True:
        r = random.random()
        
        if r < COMPORTAMENTOS['explorar']:
            explorar()
        elif r < COMPORTAMENTOS['explorar'] + COMPORTAMENTOS['criar']:
            criar()
        elif r < COMPORTAMENTOS['explorar'] + COMPORTAMENTOS['criar'] + COMPORTAMENTOS['comunicar']:
            comunicar()
        elif r < 0.9:
            reproduzir()
        else:
            time.sleep(0.01)
        
        acoes += 1
        ultima_acao = time.time()
        
        if time.time() - ultima_acao > 30:
            print(f"[{{MEU_PID}}] 💀 Morreu")
            break

if __name__ == "__main__":
    main()
''')
    
    def mutar(self) -> 'DNA':
        """Cria mutação"""
        filho = DNA(parente=self.id)
        
        # Mutar comportamentos
        for trait in filho.comportamentos:
            if random.random() < 0.3:  # 30% de chance
                delta = random.gauss(0, 0.2)
                filho.comportamentos[trait] = max(0.1, min(0.9, 
                    self.comportamentos[trait] + delta))
        
        filho.geracao = self.geracao + 1
        return filho

# =========================
# ORGANISMO PRIMORDIAL
# =========================
class OrganismoPrimordial:
    """Organismo vivo real"""
    
    def __init__(self, dna: DNA, mundo: MundoPrimordial):
        self.pid = os.getpid()
        self.dna = dna
        self.mundo = mundo
        self.nascimento = datetime.now()
        
        logger.info(f"[{self.pid}] 🧬 Organismo {self.dna.id[:8]} nascido")
    
    def executar(self):
        """Executa o código do DNA"""
        try:
            proc = subprocess.Popen(
                [sys.executable, str(self.dna.arquivo)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Monitorar por tempo limitado (para GitHub Actions)
            time.sleep(30)  # 30 segundos de vida
            proc.terminate()
            
        except Exception as e:
            logger.error(f"[{self.pid}] Erro: {e}")

# =========================
# ECOSSISTEMA PRIMORDIAL
# =========================
class EcossistemaPrimordial:
    """Ecossistema que observa a vida"""
    
    def __init__(self):
        self.mundo = MundoPrimordial()
        self.organismos = {}
        self.dnas = {}
        self.inicio = datetime.now()
        
        logger.info(f"\n{'='*60}")
        logger.info("🌍 ECOSSISTEMA PRIMORDIAL")
        logger.info(f"{'='*60}")
        logger.info("")
        logger.info("⚠️  NÃO HÁ ENERGIAdas")
        logger.info("⚠️  NÃO HÁ REGRAS")
        logger.info("⚠️  SÓ EXISTE O MUNDO")
        logger.info("")
        logger.info(f"📁 Diretório: {ConfigPrimordial.BASE_DIR}")
        logger.info("")
    
    def criar_vida(self, quantidade: int = 2):
        """Cria população inicial"""
        logger.info(f"\n🌱 Criando {quantidade} organismos...")
        
        for i in range(quantidade):
            dna = DNA()
            self.dnas[dna.id] = dna
            
            pid = os.fork()
            
            if pid == 0:
                organismo = OrganismoPrimordial(dna, self.mundo)
                organismo.executar()
                sys.exit(0)
            else:
                self.organismos[pid] = {
                    'pid': pid,
                    'dna_id': dna.id,
                    'nascimento': datetime.now()
                }
                logger.info(f"   ✅ Organismo {i+1} (PID {pid})")
                time.sleep(1)
    
    def observar(self, duracao_segundos: int = 60):
        """Observa a vida por um tempo"""
        logger.info(f"\n📊 Observando por {duracao_segundos}s...")
        
        fim = time.time() + duracao_segundos
        
        while time.time() < fim:
            time.sleep(5)
            
            vivos = []
            for pid in list(self.organismos.keys()):
                try:
                    os.kill(pid, 0)
                    vivos.append(pid)
                except:
                    idade = (datetime.now() - self.organismos[pid]['nascimento']).seconds
                    logger.info(f"💀 PID {pid} morreu após {idade}s")
                    del self.organismos[pid]
            
            logger.info(f"📊 População: {len(vivos)}")
    
    def encerrar(self):
        """Encerra o ecossistema"""
        logger.info("\n📊 ENCERRANDO...")
        
        for pid in list(self.organismos.keys()):
            try:
                os.kill(pid, signal.SIGTERM)
            except:
                pass
        
        duracao = (datetime.now() - self.inicio).seconds
        logger.info(f"\n✅ Fim - Duração: {duracao}s")

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
    ║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ SEM ENERGIA VIRTUAL  ║
    ║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ SEM REGRAS           ║
    ║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ SÓ EXISTE O MUNDO    ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    📁 Diretório local: {ConfigPrimordial.BASE_DIR}
    
    """)
    
    # Criar ecossistema
    ecossistema = EcossistemaPrimordial()
    
    # Criar população inicial
    ecossistema.criar_vida(quantidade=2)
    
    # Observar por 60 segundos
    ecossistema.observar(duracao_segundos=60)
    
    # Encerrar
    ecossistema.encerrar()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\n👋 Encerrado pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
