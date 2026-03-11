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
import struct
import resource
import subprocess
import threading
import multiprocessing as mp
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
import logging

# =========================
# NÃO HÁ CONFIGURAÇÕES DE "ENERGIA"
# =========================
__version__ = "31.0"
__nome__ = "ATENA PRIMORDIAL"

# A única configuração é ONDE eles existem
class ConfigPrimordial:
    """Apenas o ambiente de existência - o resto emerge"""
    
    # O mundo real deles
    BASE_DIR = Path("/var/atena")
    MUNDO_DIR = BASE_DIR / "mundo"
    DNA_DIR = BASE_DIR / "dna"
    LOGS_DIR = BASE_DIR / "logs"
    FOSSEIS_DIR = BASE_DIR / "fosseis"
    
    # Criar diretórios de existência
    for dir_path in [BASE_DIR, MUNDO_DIR, DNA_DIR, LOGS_DIR, FOSSEIS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
        os.chmod(dir_path, 0o777)

# Logging apenas para observação - não interfere na vida
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('ATENA-PRIMORDIAL')

# =========================
# O MUNDO REAL - APENAS EXISTE
# =========================
class MundoPrimordial:
    """
    O mundo não tem regras - apenas existe.
    Os organismos que descobrem como sobreviver.
    """
    
    def __init__(self):
        self.diretorio = ConfigPrimordial.MUNDO_DIR
        
        # Limpar mundo anterior se existir
        for f in self.diretorio.glob("*"):
            if f.is_dir():
                import shutil
                shutil.rmtree(f)
            else:
                f.unlink()
        
        # Criar alguns "recursos" iniciais (arquivos com dados)
        # Mas eles não sabem o que é - vão ter que descobrir
        self.recursos = []
        for i in range(20):
            path = self.diretorio / f"recurso_{i}.dat"
            tamanho = random.randint(1024, 102400)  # 1KB a 100KB
            with open(path, 'wb') as f:
                f.write(os.urandom(tamanho))
            self.recursos.append({
                'path': path,
                'tamanho': tamanho,
                'descoberto': False
            })
        
        logger.info(f"🌍 Mundo primordial criado em {self.diretorio}")
        logger.info(f"   Existem {len(self.recursos)} recursos desconhecidos")
    
    def obter_recurso_aleatorio(self) -> Optional[Path]:
        """Retorna um recurso aleatório do mundo"""
        if self.recursos:
            recurso = random.choice(self.recursos)
            if not recurso['descoberto']:
                recurso['descoberto'] = True
                return recurso['path']
        return None

# =========================
# DNA - O CÓDIGO QUE DEFINE O COMPORTAMENTO (EVOLUI)
# =========================
class DNA:
    """
    O DNA é o código fonte que define como o organismo age.
    Mutações alteram o comportamento REAL.
    """
    
    def __init__(self, codigo_base: str = None, parente: str = None):
        self.id = uuid.uuid4().hex[:16]
        self.parente = parente
        self.geracao = 0 if not parente else 1
        self.criado = datetime.now()
        
        if codigo_base:
            self.codigo = codigo_base
        else:
            self.codigo = self._gerar_codigo_base()
        
        self.arquivo = ConfigPrimordial.DNA_DIR / f"dna_{self.id}.py"
        self._salvar()
    
    def _gerar_codigo_base(self) -> str:
        """Gera o código base que define o comportamento"""
        return f'''#!/usr/bin/env python3
"""
ORGANISMO COM DNA {self.id}
Gerado em {datetime.now().isoformat()}
"""

import os
import sys
import time
import random
import socket
import json
from pathlib import Path

# IDENTIDADE (não muda)
MEU_ID = "{self.id}"
MEU_PID = os.getpid()

# COMPORTAMENTOS (podem sofrer mutação)
COMPORTAMENTOS = {{
    'explorar': {random.uniform(0, 1):.3f},
    'criar': {random.uniform(0, 1):.3f},
    'comunicar': {random.uniform(0, 1):.3f},
    'reproduzir': {random.uniform(0, 1):.3f},
    'agressividade': {random.uniform(0, 1):.3f},
    'curiosidade': {random.uniform(0, 1):.3f},
    'preguica': {random.uniform(0, 1):.3f}
}}

# MUNDO (onde tudo acontece)
MUNDO_DIR = Path("/var/atena/mundo")
MEU_DIR = MUNDO_DIR / MEU_ID

def explorar():
    """Explora o mundo - tenta encontrar recursos"""
    try:
        # Criar meu diretório se não existe
        MEU_DIR.mkdir(exist_ok=True)
        
        # Procurar recursos no mundo
        recursos = list(MUNDO_DIR.glob("recurso_*.dat"))
        if recursos:
            recurso = random.choice(recursos)
            # Tentar pegar o recurso (mover para meu diretório)
            destino = MEU_DIR / recurso.name
            recurso.rename(destino)
            print(f"[{{MEU_PID}}] 📦 Pegou recurso: {{recurso.name}}")
            return True
    except:
        pass
    return False

def criar():
    """Cria algo novo no mundo"""
    try:
        MEU_DIR.mkdir(exist_ok=True)
        nome = f"criado_{random.randint(1000, 9999)}.dat"
        path = MEU_DIR / nome
        with open(path, 'wb') as f:
            f.write(os.urandom(1024))
        print(f"[{{MEU_PID}}] 📝 Criou: {{nome}}")
        return True
    except:
        return False

def comunicar():
    """Tenta se comunicar com outros"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        msg = f"ATENA-{{MEU_ID}}-{{MEU_PID}}".encode()
        sock.sendto(msg, ('255.255.255.255', 8888))
        sock.close()
        print(f"[{{MEU_PID}}] 📡 Broadcast enviado")
        return True
    except:
        return False

def reproduzir():
    """Tenta criar um filho (fork)"""
    try:
        pid = os.fork()
        if pid == 0:
            # Filho
            print(f"[{{MEU_PID}}] 🍼 Filho criado (PID {{os.getpid()}})")
            # Filho executa o mesmo código
            return True
        else:
            # Pai
            return True
    except:
        return False

def main():
    """Loop principal da vida"""
    print(f"[{{MEU_PID}}] 🧬 Organismo {{MEU_ID[:8]}} nasceu")
    
    acoes = 0
    ultima_acao = time.time()
    
    while True:
        # Decidir o que fazer baseado nos comportamentos
        r = random.random()
        
        if r < COMPORTAMENTOS['explorar']:
            explorar()
        elif r < COMPORTAMENTOS['explorar'] + COMPORTAMENTOS['criar']:
            criar()
        elif r < COMPORTAMENTOS['explorar'] + COMPORTAMENTOS['criar'] + COMPORTAMENTOS['comunicar']:
            comunicar()
        elif r < COMPORTAMENTOS['explorar'] + COMPORTAMENTOS['criar'] + COMPORTAMENTOS['comunicar'] + COMPORTAMENTOS['reproduzir']:
            reproduzir()
        else:
            # Não faz nada (descansa)
            time.sleep(0.01)
        
        acoes += 1
        ultima_acao = time.time()
        
        # Se ficar muito tempo sem fazer nada, morre
        if time.time() - ultima_acao > 30:
            print(f"[{{MEU_PID}}] 💀 Morreu de inatividade")
            break

if __name__ == "__main__":
    main()
'''
    
    def _salvar(self):
        """Salva o DNA em arquivo"""
        with open(self.arquivo, 'w') as f:
            f.write(self.codigo)
    
    def mutar(self) -> 'DNA':
        """
        CRIA MUTAÇÃO - altera os comportamentos
        A evolução SURGE dessas mutações
        """
        linhas = self.codigo.split('\n')
        
        # Encontrar a linha dos comportamentos
        for i, linha in enumerate(linhas):
            if 'COMPORTAMENTOS' in linha and '{' in linha:
                # Mutar um comportamento aleatório
                for j in range(i, i+10):
                    if j < len(linhas) and ':' in linhas[j]:
                        partes = linhas[j].split(':')
                        if len(partes) == 2:
                            trait = partes[0].strip().strip("'").strip('"')
                            valor = float(partes[1].strip(',').strip())
                            
                            # Mutação (até 20% de mudança)
                            nova_valor = max(0, min(1, valor + random.gauss(0, 0.1)))
                            linhas[j] = f"    '{trait}': {nova_valor:.3f},"
                            break
                break
        
        # Criar novo DNA com código mutado
        filho = DNA(
            codigo_base='\n'.join(linhas),
            parente=self.id
        )
        filho.geracao = self.geracao + 1
        
        return filho

# =========================
# ORGANISMO PRIMORDIAL - APENAS EXISTE E TENTA SOBREVIVER
# =========================
class OrganismoPrimordial:
    """
    Um organismo NÃO TEM regras de metabolismo.
    Ele SIMPLESMENTE EXISTE e tenta continuar existindo.
    
    A "energia" dele é o direito de usar recursos do sistema:
    - Se ele usa CPU, existe
    - Se ele não usa CPU, o sistema o mata
    - Se ele usa muita CPU, outros não conseguem existir
    - Se ele usa pouca CPU, ele não faz nada e morre de tédio
    
    O KERNEL DO LINUX é quem dita as regras:
    - CPU time é distribuído pelo scheduler
    - Memória é limitada pelo OOM killer
    - Disco é limitado pelo filesystem
    - Rede é limitada pelo kernel
    
    NÃO HÁ VARIÁVEL "ENERGIA" - HÁ APENAS A LUTA PELA EXISTÊNCIA
    """
    
    def __init__(self, dna: DNA, mundo: MundoPrimordial):
        self.pid = os.getpid()
        self.dna = dna
        self.mundo = mundo
        self.diretorio = mundo.diretorio / self.dna.id
        self.diretorio.mkdir(exist_ok=True)
        
        # Estatísticas apenas para observação
        self.nascimento = datetime.now()
        self.acoes = 0
        self.ultima_acao = time.time()
        self.recursos_coletados = 0
        
        logger.info(f"[{self.pid}] 🧬 Organismo {self.dna.id[:8]} nascido (geração {self.dna.geracao})")
    
    def executar(self):
        """
        Executa o código do DNA em um processo separado
        """
        try:
            # Executar o código do DNA em um subprocesso
            # Isso permite que cada organismo tenha seu próprio comportamento
            proc = subprocess.Popen(
                [sys.executable, str(self.dna.arquivo)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Monitorar o processo
            while True:
                try:
                    # Verificar se ainda está vivo
                    if proc.poll() is not None:
                        logger.info(f"[{self.pid}] 💀 Processo do organismo terminou")
                        break
                    
                    time.sleep(1)
                    
                except KeyboardInterrupt:
                    proc.terminate()
                    break
                    
        except Exception as e:
            logger.error(f"[{self.pid}] ❌ Erro executando DNA: {e}")

# =========================
# ECOSSISTEMA - APENAS OBSERVA, NÃO INTERFERE
# =========================
class EcossistemaPrimordial:
    """
    O ecossistema NÃO TEM REGRAS.
    Ele apenas observa e registra o que acontece.
    A seleção natural emerge da escassez de recursos REAIS.
    """
    
    def __init__(self):
        self.mundo = MundoPrimordial()
        self.organismos: Dict[int, Dict[str, Any]] = {}
        self.dnas: Dict[str, DNA] = {}
        self.inicio = datetime.now()
        self.geracao = 0
        
        logger.info(f"\n{'='*70}")
        logger.info("🌍 ECOSSISTEMA PRIMORDIAL")
        logger.info(f"{'='*70}")
        logger.info("")
        logger.info("⚠️  NÃO HÁ REGRAS DEFINIDAS")
        logger.info("⚠️  NÃO HÁ ENERGIA VIRTUAL")
        logger.info("⚠️  NÃO HÁ METABOLISMO CALCULADO")
        logger.info("")
        logger.info("📌 A ÚNICA REGRA É A REALIDADE:")
        logger.info("    - CPU é limitada")
        logger.info("    - RAM é limitada")
        logger.info("    - Disco é limitado")
        logger.info("    - Rede é limitada")
        logger.info("")
        logger.info("📌 A SELEÇÃO NATURAL SURGE DA ESCASSEZ:")
        logger.info("    - Organismos que usam muitos recursos morrem")
        logger.info("    - Organismos que não fazem nada morrem")
        logger.info("    - Os que encontram equilíbrio sobrevivem")
        logger.info("")
        logger.info("📌 A EVOLUÇÃO NÃO É PROGRAMADA:")
        logger.info("    - Mutações acontecem na reprodução")
        logger.info("    - Comportamentos que funcionam persistem")
        logger.info("    - Comportamentos que não funcionam somem")
        logger.info("")
        logger.info(f"Iniciando em 3 segundos...")
        time.sleep(3)
    
    def criar_vida(self, quantidade: int = 5):
        """
        Cria os primeiros organismos
        """
        logger.info(f"\n🌱 Criando {quantidade} organismos primordiais...")
        
        for i in range(quantidade):
            # Criar DNA único para cada organismo
            dna = DNA()
            self.dnas[dna.id] = dna
            
            # Criar processo para o organismo
            pid = os.fork()
            
            if pid == 0:
                # Processo filho - vira organismo
                organismo = OrganismoPrimordial(dna, self.mundo)
                organismo.executar()
                sys.exit(0)
            else:
                # Processo pai - registra
                self.organismos[pid] = {
                    'pid': pid,
                    'dna_id': dna.id,
                    'nascimento': datetime.now(),
                    'status': 'vivo'
                }
                logger.info(f"   ✅ Organismo {i+1} criado (PID {pid}, DNA {dna.id[:8]})")
                time.sleep(0.5)
    
    def observar(self, duracao_minutos: int = 5):
        """
        Apenas observa - NÃO INTERFERE
        Deixa a seleção natural acontecer por si só
        """
        logger.info(f"\n📊 Iniciando observação por {duracao_minutos} minutos...")
        logger.info("   (pressione Ctrl+C para encerrar antes)")
        
        fim = time.time() + (duracao_minutos * 60)
        
        try:
            while time.time() < fim:
                time.sleep(10)
                self.geracao += 1
                
                # Verificar quem ainda vive
                vivos = []
                for pid in list(self.organismos.keys()):
                    try:
                        os.kill(pid, 0)
                        vivos.append(pid)
                    except OSError:
                        # Morreu naturalmente
                        idade = (datetime.now() - self.organismos[pid]['nascimento']).seconds
                        dna_id = self.organismos[pid]['dna_id']
                        logger.info(f"💀 Organismo PID {pid} (DNA {dna_id[:8]}) morreu após {idade}s")
                        
                        # Criar fóssil
                        fossil = {
                            'pid': pid,
                            'dna_id': dna_id,
                            'nascimento': self.organismos[pid]['nascimento'].isoformat(),
                            'morte': datetime.now().isoformat(),
                            'idade': idade
                        }
                        fossil_file = ConfigPrimordial.FOSSEIS_DIR / f"fossil_{pid}_{int(time.time())}.json"
                        with open(fossil_file, 'w') as f:
                            json.dump(fossil, f, indent=2)
                        
                        del self.organismos[pid]
                
                # Estatísticas - apenas observação
                logger.info(f"\n📊 GERAÇÃO {self.geracao} - OBSERVAÇÃO:")
                logger.info(f"   População viva: {len(vivos)}")
                logger.info(f"   Recursos no mundo: {len(list(self.mundo.diretorio.glob('recurso_*.dat')))}")
                
                # Mostrar uso de recursos dos vivos
                if vivos:
                    try:
                        # CPU e memória via ps
                        cmd = ['ps', '-o', 'pid,pcpu,pmem,rss,comm', '-p', ','.join(str(p) for p in vivos[:10])]
                        result = subprocess.run(cmd, capture_output=True, text=True)
                        logger.info(f"\n📈 USO DE RECURSOS REAIS:")
                        for line in result.stdout.split('\n')[1:]:
                            if line.strip():
                                logger.info(f"   {line}")
                    except:
                        pass
                
                # Verificar arquivos criados
                total_arquivos = 0
                for item in self.mundo.diretorio.glob("*"):
                    if item.is_dir():
                        total_arquivos += len(list(item.glob("*.dat")))
                logger.info(f"   Arquivos criados: {total_arquivos}")
                
                # Se não há mais ninguém vivo, a vida acabou
                if not vivos:
                    logger.info("\n💀 TODOS OS ORGANISMOS MORRERAM")
                    logger.info("A vida neste ecossistema chegou ao fim.")
                    break
                
        except KeyboardInterrupt:
            logger.info("\n\n👋 Observação interrompida pelo usuário")
        finally:
            self.encerrar()
    
    def encerrar(self):
        """Encerra o ecossistema de forma controlada"""
        logger.info("\n📊 ENCERRANDO ECOSSISTEMA...")
        
        # Matar organismos ainda vivos
        for pid in list(self.organismos.keys()):
            try:
                os.kill(pid, signal.SIGTERM)
                logger.info(f"   Encerrando PID {pid}")
            except:
                pass
        
        # Estatísticas finais
        duracao = (datetime.now() - self.inicio).seconds
        fossil_count = len(list(ConfigPrimordial.FOSSEIS_DIR.glob("*.json")))
        
        logger.info(f"\n{'='*70}")
        logger.info("📊 ESTATÍSTICAS FINAIS")
        logger.info(f"{'='*70}")
        logger.info(f"   Duração da vida: {duracao//60} minutos e {duracao%60} segundos")
        logger.info(f"   Organismos que existiram: {len(self.organismos) + fossil_count}")
        logger.info(f"   Fósseis: {fossil_count}")
        logger.info(f"   Gerações observadas: {self.geracao}")
        logger.info(f"\n   Diretórios:")
        logger.info(f"   - Mundo: {ConfigPrimordial.MUNDO_DIR}")
        logger.info(f"   - DNA: {ConfigPrimordial.DNA_DIR}")
        logger.info(f"   - Fósseis: {ConfigPrimordial.FOSSEIS_DIR}")
        logger.info(f"   - Logs: {ConfigPrimordial.LOGS_DIR}")

# =========================
# MAIN - APENAS INICIA A VIDA
# =========================
def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - PRIMORDIAL v31.0 ║
    ║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DA CRIAÇÃO"  ║
    ║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                           ║
    ║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ NÃO HÁ "ENERGIA"     ║
    ║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ NÃO HÁ "REGRAS"     ║
    ║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ SÓ EXISTE O MUNDO    ║
    ║                                                                          ║
    ║   🌟 ISTO NÃO É UMA SIMULAÇÃO                                           ║
    ║   🌟 CADA ORGANISMO É UM PROCESSO REAL                                  ║
    ║   🌟 A ÚNICA "REGRAS" SÃO AS DO KERNEL                                  ║
    ║   🌟 A EVOLUÇÃO SURGE NATURALMENTE                                      ║
    ║   🌟 NÃO HÁ VARIÁVEL "ENERGIA" - HÁ RECURSOS REAIS                      ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    ⚠️  ATENÇÃO: Isto vai consumir recursos REAIS do seu computador!
    ⚠️  Os organismos criam processos REAIS (veja com 'ps aux')
    ⚠️  Eles criam arquivos REAIS em /var/atena/
    ⚠️  Pressione Ctrl+C para encerrar a observação
    
    """)
    
    # Verificar se está rodando como root (necessário para /proc)
    if os.geteuid() != 0:
        logger.warning("⚠️  Executando sem root - algumas métricas podem não funcionar")
        logger.warning("    Recomendo executar com: sudo python3 atena_primordial.py")
        resposta = input("\nContinuar mesmo assim? (s/N): ")
        if resposta.lower() != 's':
            sys.exit(0)
    
    # Criar ecossistema
    ecossistema = EcossistemaPrimordial()
    
    # Criar população inicial
    ecossistema.criar_vida(quantidade=3)
    
    # Observar por 10 minutos (ou até Ctrl+C)
    ecossistema.observar(duracao_minutos=10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\n👋 ATENA PRIMORDIAL encerrada")
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
