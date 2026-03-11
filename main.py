#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - ATENA GENETICA v35.0   ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DA HERANÇA"       ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                               ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ MUTAÇÃO VIA AST          ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ RECOMBINAÇÃO GENÉTICA    ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ SELEÇÃO NATURAL REAL     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

🌍 AGORA OS ORGANISMOS:
   ✅ MUTAM via AST (modificam a estrutura da árvore sintática)
   ✅ RECOMBINAM DNA de dois pais (reprodução sexual)
   ✅ COMPETEM por recursos, tempo de vida e reprodução
   ✅ SOBREVIVEM os mais aptos (seleção natural real)
   ✅ HERDAM características dos pais com variação
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
import urllib.request
import urllib.parse
import sqlite3
import hashlib
import ast
import astor
import inspect
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
import logging
import threading
import queue
from collections import defaultdict

# =========================
# CONFIGURAÇÕES
# =========================
__version__ = "35.0"
__nome__ = "ATENA GENÉTICA"

BASE_DIR = Path(__file__).parent / "atena_mundo"

class Config:
    BASE_DIR = BASE_DIR
    MUNDO_DIR = BASE_DIR / "mundo"
    DNA_DIR = BASE_DIR / "dna"
    LOGS_DIR = BASE_DIR / "logs"
    FOSSEIS_DIR = BASE_DIR / "fosseis"
    CONHECIMENTO_DIR = BASE_DIR / "conhecimento"
    GERACOES_DIR = BASE_DIR / "geracoes"
    
    # Recursos do ambiente
    RECURSOS_INICIAIS = 50
    RECURSOS_POR_CICLO = 5
    ENERGIA_POR_RECURSO = 10
    
    # Competição
    TEMPO_VIDA_BASE = 300  # 5 minutos
    CUSTO_REPRODUCAO = 30
    IDADE_MINIMA_REPRODUCAO = 60  # 1 minuto
    
    # Seleção natural
    POPULACAO_MAXIMA = 10
    TAXA_MUTACAO = 0.3
    TAXA_RECOMBINACAO = 0.4
    
    # AST Mutation
    MUTACOES_DISPONIVEIS = [
        'swap_operators',
        'modify_constants',
        'duplicate_lines',
        'remove_lines',
        'add_noise'
    ]
    
    # Criar diretórios
    for dir_path in [BASE_DIR, MUNDO_DIR, DNA_DIR, LOGS_DIR, 
                     FOSSEIS_DIR, CONHECIMENTO_DIR, GERACOES_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler(Config.LOGS_DIR / f"atena_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('ATENA-GENETICA')

# =========================
# MUTAÇÃO VIA AST (MODIFICA ESTRUTURA REAL DO CÓDIGO)
# =========================
class MutadorAST:
    """
    Modifica a Árvore Sintática Abstrata do código Python
    Isso é MUTAÇÃO REAL na estrutura do programa
    """
    
    def __init__(self):
        self.mutacoes_aplicadas = 0
    
    def mutar_codigo(self, codigo: str, tipo_mutacao: str = None) -> str:
        """
        Aplica mutação no código via AST
        Retorna código mutado
        """
        try:
            # Parsear código para AST
            arvore = ast.parse(codigo)
            
            if not tipo_mutacao:
                tipo_mutacao = random.choice(Config.MUTACOES_DISPONIVEIS)
            
            # Aplicar mutação baseada no tipo
            if tipo_mutacao == 'swap_operators':
                self._swap_operators(arvore)
            elif tipo_mutacao == 'modify_constants':
                self._modify_constants(arvore)
            elif tipo_mutacao == 'duplicate_lines':
                self._duplicate_lines(arvore)
            elif tipo_mutacao == 'remove_lines':
                self._remove_lines(arvore)
            elif tipo_mutacao == 'add_noise':
                self._add_noise(arvore)
            
            # Converter AST de volta para código
            novo_codigo = astor.to_source(arvore)
            
            self.mutacoes_aplicadas += 1
            logger.debug(f"🧬 Mutação AST: {tipo_mutacao}")
            
            return novo_codigo
            
        except Exception as e:
            logger.error(f"Erro na mutação AST: {e}")
            return codigo
    
    def _swap_operators(self, arvore: ast.AST):
        """Troca operadores aritméticos/binários"""
        for node in ast.walk(arvore):
            if isinstance(node, ast.BinOp):
                # Trocar + por -, * por /, etc
                if isinstance(node.op, ast.Add):
                    node.op = ast.Sub()
                elif isinstance(node.op, ast.Sub):
                    node.op = ast.Add()
                elif isinstance(node.op, ast.Mult):
                    node.op = ast.Div()
                elif isinstance(node.op, ast.Div):
                    node.op = ast.Mult()
    
    def _modify_constants(self, arvore: ast.AST):
        """Modifica constantes numéricas"""
        for node in ast.walk(arvore):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    # Aplicar variação de ±20%
                    if random.random() < 0.3:  # 30% de chance
                        if isinstance(node.value, int):
                            node.value = int(node.value * random.uniform(0.8, 1.2))
                        else:
                            node.value = node.value * random.uniform(0.8, 1.2)
    
    def _duplicate_lines(self, arvore: ast.AST):
        """Duplica linhas de código aleatórias"""
        for node in list(ast.walk(arvore)):
            if isinstance(node, (ast.FunctionDef, ast.For, ast.While)):
                if node.body and random.random() < 0.2:
                    # Duplicar uma linha aleatória
                    idx = random.randint(0, len(node.body)-1)
                    linha = node.body[idx]
                    node.body.insert(idx, linha)
                    break
    
    def _remove_lines(self, arvore: ast.AST):
        """Remove linhas de código aleatórias"""
        for node in ast.walk(arvore):
            if isinstance(node, (ast.FunctionDef, ast.For, ast.While)):
                if len(node.body) > 3 and random.random() < 0.1:
                    # Remover linha aleatória (não crítica)
                    idx = random.randint(1, len(node.body)-2)
                    del node.body[idx]
                    break
    
    def _add_noise(self, arvore: ast.AST):
        """Adiciona código inócuo (ruído)"""
        for node in ast.walk(arvore):
            if isinstance(node, ast.FunctionDef) and node.name == 'main':
                # Adicionar linha de ruído
                linha_ruido = ast.parse("time.sleep(0.001)  # Ruído genético").body[0]
                node.body.insert(1, linha_ruido)
                break

# =========================
# DNA COM SUPORTE A RECOMBINAÇÃO
# =========================
class DNA:
    def __init__(self, pai_id: str = None, mae_id: str = None):
        self.id = uuid.uuid4().hex[:16]
        self.pai_id = pai_id
        self.mae_id = mae_id
        self.geracao = 0
        
        if pai_id and mae_id:
            # Reprodução sexual - herda de ambos
            self.geracao = max(self._get_geracao(pai_id), self._get_geracao(mae_id)) + 1
        
        # Genes de comportamento
        self.genes = {
            'forca': random.uniform(0.3, 0.9),
            'velocidade': random.uniform(0.3, 0.9),
            'inteligencia': random.uniform(0.3, 0.9),
            'fertilidade': random.uniform(0.3, 0.9),
            'metabolismo': random.uniform(0.3, 0.9),
            'curiosidade': random.uniform(0.3, 0.9),
            'agressividade': random.uniform(0.3, 0.9),
            'cooperacao': random.uniform(0.3, 0.9)
        }
        
        # Comportamentos derivados dos genes
        self.comportamentos = self._gerar_comportamentos()
        
        self.arquivo = Config.DNA_DIR / f"dna_{self.id}.py"
        self._salvar()
    
    def _get_geracao(self, parent_id: str) -> int:
        """Pega geração de um parente"""
        # Em produção, buscaria no banco
        return 0
    
    def _gerar_comportamentos(self) -> Dict:
        """Gera comportamentos baseados nos genes"""
        return {
            'explorar': self.genes['curiosidade'] * 0.8 + self.genes['velocidade'] * 0.2,
            'lutar': self.genes['forca'] * 0.7 + self.genes['agressividade'] * 0.3,
            'fugir': (1 - self.genes['forca']) * 0.5 + self.genes['velocidade'] * 0.5,
            'reproduzir': self.genes['fertilidade'] * 0.9 + self.genes['cooperacao'] * 0.1,
            'aprender': self.genes['inteligencia'] * 0.8 + self.genes['curiosidade'] * 0.2,
            'descansar': 1 - self.genes['metabolismo']
        }
    
    def _salvar(self):
        with open(self.arquivo, 'w') as f:
            f.write(f'''#!/usr/bin/env python3
import os, sys, time, random
from pathlib import Path

ID = "{self.id}"
GERACAO = {self.geracao}
GENES = {self.genes}
COMP = {self.comportamentos}

MUNDO = Path("{Config.MUNDO_DIR}")
MEU_DIR = MUNDO / ID
ENERGIA = 100
IDADE = 0
FILHOS = 0

def main():
    global ENERGIA, IDADE, FILHOS
    MEU_DIR.mkdir(exist_ok=True)
    fim = time.time() + 300
    
    while time.time() < fim and ENERGIA > 0:
        r = random.random()
        IDADE += 1
        
        # Consumir energia (metabolismo)
        ENERGIA -= 0.1 * (1 - GENES['metabolismo'])
        
        # Decidir ação baseada nos genes
        if r < COMP['explorar']:
            # Explorar - buscar recursos
            recursos = list(MUNDO.glob("recurso_*.dat"))
            if recursos:
                rsrc = random.choice(recursos)
                try:
                    rsrc.rename(MEU_DIR / rsrc.name)
                    ENERGIA += 10
                    print(f"[{{os.getpid()}}] 📦 Explorou +10 energia")
                except: pass
        
        elif r < COMP['explorar'] + COMP['lutar']:
            # Lutar - tentar roubar recursos de outros
            outros = [d for d in MUNDO.glob("*") if d.is_dir() and d.name != ID]
            if outros:
                alvo = random.choice(outros)
                recursos_alvo = list(alvo.glob("*.dat"))
                if recursos_alvo:
                    rsrc = random.choice(recursos_alvo)
                    try:
                        rsrc.rename(MEU_DIR / rsrc.name)
                        ENERGIA += 15
                        print(f"[{{os.getpid()}}] ⚔️ Lutou +15 energia")
                    except: pass
        
        elif r < COMP['explorar'] + COMP['lutar'] + COMP['reproduzir']:
            # Reproduzir - tentar criar filho
            if ENERGIA > 50 and IDADE > 60:
                pid = os.fork()
                if pid == 0:
                    print(f"[{{os.getpid()}}] 🍼 Filho nascido")
                    sys.exit(0)
                else:
                    ENERGIA -= 30
                    FILHOS += 1
                    print(f"[{{os.getpid()}}] 🤰 Teve filho")
        
        elif r < COMP['explorar'] + COMP['lutar'] + COMP['reproduzir'] + COMP['aprender']:
            # Aprender - tentar modificar comportamento
            print(f"[{{os.getpid()}}] 📚 Aprendendo...")
            # Em produção, buscaria conhecimento externo
        
        else:
            # Descansar - recuperar energia
            ENERGIA += 2
            print(f"[{{os.getpid()}}] 😴 Descansou +2 energia")
        
        time.sleep(0.1)
    
    print(f"[{{os.getpid()}}] 💀 Morreu - Energia: {{ENERGIA}}, Filhos: {{FILHOS}}")

if __name__ == "__main__":
    main()
''')
    
    def mutar_via_ast(self, mutador: MutadorAST) -> 'DNA':
        """Aplica mutação via AST no código"""
        with open(self.arquivo, 'r') as f:
            codigo = f.read()
        
        # Aplicar mutação
        codigo_mutado = mutador.mutar_codigo(codigo)
        
        # Criar novo DNA
        filho = DNA(pai_id=self.id)
        filho.genes = self.genes.copy()
        filho.geracao = self.geracao + 1
        
        # Aplicar mutação nos genes também
        for gene in filho.genes:
            if random.random() < 0.1:  # 10% de mutação genética
                filho.genes[gene] = max(0.1, min(0.9, 
                    filho.genes[gene] + random.gauss(0, 0.1)))
        
        filho.comportamentos = filho._gerar_comportamentos()
        
        # Salvar código mutado
        with open(filho.arquivo, 'w') as f:
            f.write(codigo_mutado)
        
        return filho
    
    @classmethod
    def recombinar(cls, dna_a: 'DNA', dna_b: 'DNA', mutador: MutadorAST) -> 'DNA':
        """
        RECOMBINAÇÃO GENÉTICA SEXUAL
        Cria novo DNA combinando genes de dois pais
        """
        filho = cls(pai_id=dna_a.id, mae_id=dna_b.id)
        
        # Crossover de genes (herda de ambos os pais)
        for gene in filho.genes:
            if random.random() < 0.5:
                # Herda do pai
                filho.genes[gene] = dna_a.genes.get(gene, 0.5)
            else:
                # Herda da mãe
                filho.genes[gene] = dna_b.genes.get(gene, 0.5)
            
            # Possível mutação
            if random.random() < 0.05:  # 5% de mutação
                filho.genes[gene] = max(0.1, min(0.9, 
                    filho.genes[gene] + random.gauss(0, 0.15)))
        
        # Recalcular comportamentos
        filho.comportamentos = filho._gerar_comportamentos()
        
        # Mutar código via AST (combinar código dos pais)
        with open(dna_a.arquivo, 'r') as f:
            codigo_a = f.read()
        with open(dna_b.arquivo, 'r') as f:
            codigo_b = f.read()
        
        # Crossover de código (pegar partes de cada pai)
        linhas_a = codigo_a.split('\n')
        linhas_b = codigo_b.split('\n')
        
        ponto_corte = random.randint(10, min(len(linhas_a), len(linhas_b)) - 10)
        codigo_filho = '\n'.join(linhas_a[:ponto_corte] + linhas_b[ponto_corte:])
        
        # Aplicar mutação no código
        codigo_filho = mutador.mutar_codigo(codigo_filho)
        
        with open(filho.arquivo, 'w') as f:
            f.write(codigo_filho)
        
        logger.info(f"🧬 RECOMBINAÇÃO: {dna_a.id[:8]} + {dna_b.id[:8]} = {filho.id[:8]}")
        return filho

# =========================
# ORGANISMO COM COMPETIÇÃO REAL
# =========================
class Organismo:
    def __init__(self, dna: DNA, mundo: 'Mundo'):
        self.pid = os.getpid()
        self.dna = dna
        self.mundo = mundo
        self.nascimento = datetime.now()
        self.energia = 100
        self.filhos = 0
        self.recursos_coletados = 0
        self.lutas_vencidas = 0
        
        logger.info(f"[{self.pid}] 🧬 Organismo {self.dna.id[:8]} nascido")
        logger.info(f"   Genes: {dna.genes}")
    
    def executar(self):
        try:
            proc = subprocess.Popen(
                [sys.executable, str(self.dna.arquivo)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return proc
        except Exception as e:
            logger.error(f"[{self.pid}] Erro: {e}")
            return None
    
    def get_fitness(self) -> float:
        """Calcula fitness para seleção natural"""
        idade = (datetime.now() - self.nascimento).seconds
        return (self.filhos * 100) + (self.recursos_coletados * 10) + (idade * 0.1)

# =========================
# MUNDO COM RECURSOS LIMITADOS
# =========================
class Mundo:
    def __init__(self):
        self.diretorio = Config.MUNDO_DIR
        self.recursos_disponiveis = []
        self.recursos_consumidos = 0
        
        # Limpar mundo anterior
        for f in self.diretorio.glob("*"):
            if f.is_dir():
                import shutil
                shutil.rmtree(f)
            else:
                f.unlink()
        
        # Criar recursos iniciais
        self._gerar_recursos(Config.RECURSOS_INICIAIS)
        
        logger.info(f"🌍 Mundo criado com {len(self.recursos_disponiveis)} recursos")
    
    def _gerar_recursos(self, quantidade: int):
        """Gera novos recursos no mundo"""
        for i in range(quantidade):
            path = self.diretorio / f"recurso_{uuid.uuid4().hex[:8]}.dat"
            tamanho = random.randint(1024, 5120)
            with open(path, 'wb') as f:
                f.write(os.urandom(tamanho))
            self.recursos_disponiveis.append(path)
    
    def ciclo_recursos(self):
        """Ciclo de renovação de recursos"""
        # Remover recursos velhos
        for recurso in list(self.recursos_disponiveis):
            if not recurso.exists():
                self.recursos_disponiveis.remove(recurso)
        
        # Gerar novos recursos
        self._gerar_recursos(Config.RECURSOS_POR_CICLO)

# =========================
# ECOSSISTEMA COM SELEÇÃO NATURAL
# =========================
class Ecossistema:
    def __init__(self):
        self.mundo = Mundo()
        self.mutador = MutadorAST()
        self.organismos: Dict[int, Organismo] = {}
        self.dnas: Dict[str, DNA] = {}
        self.historico_fitness = []
        self.inicio = datetime.now()
        
        logger.info(f"\n{'='*70}")
        logger.info("🌍 ECOSSISTEMA GENÉTICO INICIADO")
        logger.info(f"{'='*70}")
        logger.info(f"   População máxima: {Config.POPULACAO_MAXIMA}")
        logger.info(f"   Recursos iniciais: {Config.RECURSOS_INICIAIS}")
        logger.info(f"   Taxa mutação: {Config.TAXA_MUTACAO:.1%}")
        logger.info(f"   Taxa recombinação: {Config.TAXA_RECOMBINACAO:.1%}")
    
    def criar_vida(self, quantidade: int = 3):
        """Cria população inicial"""
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
                self.organismos[pid] = Organismo(dna, self.mundo)
                logger.info(f"   ✅ Organismo {i+1} (PID {pid})")
                time.sleep(1)
    
    def selecao_natural(self):
        """
        SELEÇÃO NATURAL REAL
        Mata os organismos menos aptos baseado em fitness
        """
        if len(self.organismos) <= Config.POPULACAO_MAXIMA:
            return
        
        # Calcular fitness de todos
        fitness_data = []
        for pid, org in self.organismos.items():
            try:
                os.kill(pid, 0)  # Verifica se está vivo
                fitness = org.get_fitness()
                fitness_data.append((fitness, pid, org))
            except:
                continue
        
        # Ordenar por fitness (maior primeiro)
        fitness_data.sort(reverse=True)
        
        # Selecionar os melhores para sobreviver
        sobreviventes = fitness_data[:Config.POPULACAO_MAXIMA]
        
        # Matar os piores
        mortos = fitness_data[Config.POPULACAO_MAXIMA:]
        
        for fitness, pid, org in mortos:
            try:
                os.kill(pid, signal.SIGTERM)
                logger.info(f"💀 Seleção natural matou PID {pid} (fitness: {fitness:.1f})")
                
                # Criar fóssil
                fossil = {
                    'pid': pid,
                    'dna_id': org.dna.id,
                    'nascimento': org.nascimento.isoformat(),
                    'morte': datetime.now().isoformat(),
                    'fitness': fitness,
                    'filhos': org.filhos,
                    'recursos': org.recursos_coletados
                }
                fossil_file = Config.FOSSEIS_DIR / f"fossil_{pid}.json"
                with open(fossil_file, 'w') as f:
                    json.dump(fossil, f, indent=2)
                
                del self.organismos[pid]
                
            except:
                pass
        
        # Registrar fitness dos sobreviventes
        self.historico_fitness.append({
            'tempo': datetime.now().isoformat(),
            'fitness_medio': sum(f for f,_,_ in sobreviventes) / len(sobreviventes),
            'fitness_max': sobreviventes[0][0] if sobreviventes else 0
        })
    
    def reproducao_sexual(self):
        """
        REPRODUÇÃO SEXUAL REAL
        Escolhe dois pais aleatórios e cria filho com recombinação
        """
        if len(self.organismos) < 2:
            return
        
        vivos = []
        for pid, org in self.organismos.items():
            try:
                os.kill(pid, 0)
                vivos.append((pid, org))
            except:
                continue
        
        if len(vivos) < 2:
            return
        
        # Selecionar dois pais aleatórios
        pai = random.choice(vivos)
        mae = random.choice([v for v in vivos if v[0] != pai[0]])
        
        # Verificar se podem reproduzir (idade mínima)
        idade_pai = (datetime.now() - pai[1].nascimento).seconds
        idade_mae = (datetime.now() - mae[1].nascimento).seconds
        
        if idade_pai < Config.IDADE_MINIMA_REPRODUCAO or idade_mae < Config.IDADE_MINIMA_REPRODUCAO:
            return
        
        # Criar filho por recombinação
        if random.random() < Config.TAXA_RECOMBINACAO:
            dna_filho = DNA.recombinar(pai[1].dna, mae[1].dna, self.mutador)
        else:
            # Mutação assexuada
            dna_filho = pai[1].dna.mutar_via_ast(self.mutador)
        
        self.dnas[dna_filho.id] = dna_filho
        
        # Criar processo do filho
        pid = os.fork()
        if pid == 0:
            org = Organismo(dna_filho, self.mundo)
            proc = org.executar()
            if proc:
                proc.wait()
            sys.exit(0)
        else:
            self.organismos[pid] = Organismo(dna_filho, self.mundo)
            logger.info(f"🤰 Novo filho nascido (PID {pid}) de pais {pai[0]}+{mae[0]}")
            
            # Atualizar estatísticas dos pais
            pai[1].filhos += 1
            mae[1].filhos += 1
    
    def observar(self, duracao_segundos: int = 300):
        """Observa evolução com seleção natural"""
        logger.info(f"\n📊 Observando evolução por {duracao_segundos//60} minutos...")
        
        fim = time.time() + duracao_segundos
        ciclo = 0
        
        while time.time() < fim:
            time.sleep(10)
            ciclo += 1
            
            # Renovar recursos
            self.mundo.ciclo_recursos()
            
            # Reprodução sexual
            if ciclo % 2 == 0:
                self.reproducao_sexual()
            
            # Seleção natural
            if len(self.organismos) > Config.POPULACAO_MAXIMA:
                self.selecao_natural()
            
            # Verificar mortes naturais
            for pid in list(self.organismos.keys()):
                try:
                    os.kill(pid, 0)
                except:
                    logger.info(f"💀 PID {pid} morreu naturalmente")
                    del self.organismos[pid]
            
            # Log do ecossistema
            fitness_values = []
            for pid, org in list(self.organismos.items()):
                try:
                    os.kill(pid, 0)
                    fitness_values.append(org.get_fitness())
                except:
                    continue
            
            if fitness_values:
                logger.info(f"📊 Ciclo {ciclo}: População {len(fitness_values)} | "
                          f"Fitness médio: {sum(fitness_values)/len(fitness_values):.1f} | "
                          f"Recursos: {len(self.mundo.recursos_disponiveis)}")
    
    def encerrar(self):
        """Encerra ecossistema e mostra estatísticas"""
        logger.info("\n📊 ENCERRANDO ECOSSISTEMA...")
        
        # Matar todos os organismos
        for pid in list(self.organismos.keys()):
            try:
                os.kill(pid, signal.SIGTERM)
            except:
                pass
        
        # Estatísticas finais
        duracao = (datetime.now() - self.inicio).seconds
        
        logger.info(f"\n{'='*70}")
        logger.info("📊 RELATÓRIO FINAL")
        logger.info(f"{'='*70}")
        logger.info(f"⏱️  Duração: {duracao//60}min {duracao%60}s")
        logger.info(f"🧬 Organismos criados: {len(self.dnas)}")
        logger.info(f"🦴 Fósseis: {len(list(Config.FOSSEIS_DIR.glob('*.json')))}")
        logger.info(f"🧬 Mutações AST: {self.mutador.mutacoes_aplicadas}")
        
        if self.historico_fitness:
            logger.info(f"📈 Fitness médio final: {self.historico_fitness[-1]['fitness_medio']:.1f}")
            logger.info(f"🏆 Fitness máximo: {self.historico_fitness[-1]['fitness_max']:.1f}")

# =========================
# MAIN
# =========================
def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - GENÉTICA v35.0   ║
    ║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DA HERANÇA"  ║
    ║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                           ║
    ║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ MUTAÇÃO VIA AST      ║
    ║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ RECOMBINAÇÃO SEXUAL  ║
    ║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ SELEÇÃO NATURAL REAL ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    🧬 MUTAÇÃO VIA AST:
       ├── Swap operators (+ ↔ -, * ↔ /)
       ├── Modify constants (±20%)
       ├── Duplicate lines
       ├── Remove lines
       └── Add genetic noise
    
    🧬 REPRODUÇÃO SEXUAL:
       ├── DNA do PAI + DNA da MÃE
       ├── Crossover genético
       ├── Herança de características
       └── Mutações aleatórias
    
    🧬 SELEÇÃO NATURAL:
       ├── Competição por recursos
       ├── Fitness = filhos×100 + recursos×10 + idade×0.1
       ├── Sobrevivem os melhores
       └── Fósseis dos extintos
    
    📁 Diretório: {Config.BASE_DIR}
    ⏱️  Observação: 5 minutos
    
    """)
    
    eco = Ecossistema()
    eco.criar_vida(quantidade=4)
    eco.observar(duracao_segundos=300)
    eco.encerrar()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n👋 Encerrado pelo usuário")
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
