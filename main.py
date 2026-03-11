#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - ATENA CIVILIZATION v44.0║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DA CIVILIZAÇÃO"   ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                               ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ MIGRAÇÃO CONTINENTAL    ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ DIALETOS EVOLUTIVOS     ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ RELIGIÕES EMERGENTES    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import uuid
import random
import signal
import sqlite3
import hashlib
import numpy as np
import pickle
import mmap
import struct
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple, Set
import logging
import threading
from collections import defaultdict, deque
import math
import socket
import fcntl
import termios

# =========================
# CONFIGURAÇÕES DO MUNDO
# =========================
__version__ = "44.0"
__nome__ = "ATENA CIVILIZATION"

BASE_DIR = Path(__file__).parent / "atena_mundo"

class Config:
    BASE_DIR = BASE_DIR
    MAPA_DIR = BASE_DIR / "mapa"
    DNA_DIR = BASE_DIR / "dna"
    LOGS_DIR = BASE_DIR / "logs"
    FOSSEIS_DIR = BASE_DIR / "fosseis"
    ECONOMIA_DIR = BASE_DIR / "economia"
    LINGUAGEM_DIR = BASE_DIR / "linguagem"
    CIDADES_DIR = BASE_DIR / "cidades"
    RELIGIOES_DIR = BASE_DIR / "religioes"
    DB_PATH = BASE_DIR / "atena.db"
    
    # CONTINENTES (mapa gigante)
    MUNDO_TAMANHO_X = 2000
    MUNDO_TAMANHO_Y = 2000
    NUM_CONTINENTES = 7
    MAPA_ARQUIVO = MAPA_DIR / "mundo.mmap"
    
    # BIOMAS POR CONTINENTE
    CONTINENTES = {
        'continente_a': {'clima': 'tropical', 'recursos': 1.2, 'perigo': 0.8},
        'continente_b': {'clima': 'temperado', 'recursos': 1.0, 'perigo': 1.0},
        'continente_c': {'clima': 'desertico', 'recursos': 0.6, 'perigo': 1.5},
        'continente_d': {'clima': 'gelado', 'recursos': 0.8, 'perigo': 1.3},
        'continente_e': {'clima': 'montanhoso', 'recursos': 1.1, 'perigo': 1.4},
        'continente_f': {'clima': 'pantanoso', 'recursos': 1.3, 'perigo': 1.1},
        'continente_g': {'clima': 'fértil', 'recursos': 1.5, 'perigo': 0.6}
    }
    
    # REDE NEURAL
    INPUT_SIZE = 60
    HIDDEN_SIZE = 256
    OUTPUT_SIZE = 30
    MEMORY_CELLS = 128
    
    # CIDADES
    TAMANHO_MINIMO_CIDADE = 10
    RAIO_CIDADE = 50
    CRESCIMENTO_CIDADE = 0.01
    
    # RELIGIÕES
    NUM_DEUSES = 12
    RITUAIS = ['sacrificio', 'oferenda', 'meditacao', 'guerra_santa', 'peregrinacao']
    DOGMAS = ['paz', 'guerra', 'prosperidade', 'conhecimento', 'natureza']
    
    # MIGRAÇÃO
    TEMPO_MIGRACAO = 1000
    ROTAS_COMERCIAIS = True
    
    # GUERRAS
    MOTIVOS_GUERRA = ['territorio', 'religiao', 'recursos', 'vinganca', 'expansao']
    
    # Criação de diretórios
    for dir_path in [BASE_DIR, MAPA_DIR, DNA_DIR, LOGS_DIR, FOSSEIS_DIR, 
                     ECONOMIA_DIR, LINGUAGEM_DIR, CIDADES_DIR, RELIGIOES_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('ATENA-CIVILIZATION')

# =========================
# MAPA CONTINENTAL
# =========================
class MapaContinental:
    """Mapa gigante com continentes e recursos reais"""
    
    def __init__(self):
        self.tamanho_x = Config.MUNDO_TAMANHO_X
        self.tamanho_y = Config.MUNDO_TAMANHO_Y
        self.tamanho_total = self.tamanho_x * self.tamanho_y
        
        # Gerar continentes
        self.continentes = self._gerar_continentes()
        
        # Criar mapa
        if not Config.MAPA_ARQUIVO.exists():
            self._criar_mapa()
        
        self._abrir_mmap()
        
        logger.info(f"🗺️ Mapa continental {self.tamanho_x}x{self.tamanho_y} "
                   f"({self.tamanho_total:,} células) com {Config.NUM_CONTINENTES} continentes")
    
    def _gerar_continentes(self):
        """Gera centros de continentes"""
        continentes = []
        for i in range(Config.NUM_CONTINENTES):
            x = random.randint(200, self.tamanho_x - 200)
            y = random.randint(200, self.tamanho_y - 200)
            nome = f"continente_{chr(65 + i)}"
            continentes.append({
                'nome': nome,
                'centro': (x, y),
                'clima': Config.CONTINENTES[f'continente_{chr(97 + i)}']['clima'],
                'recursos': Config.CONTINENTES[f'continente_{chr(97 + i)}']['recursos'],
                'perigo': Config.CONTINENTES[f'continente_{chr(97 + i)}']['perigo']
            })
        return continentes
    
    def _criar_mapa(self):
        """Cria o mapa inicial no disco"""
        with open(Config.MAPA_ARQUIVO, 'wb') as f:
            for x in range(self.tamanho_x):
                for y in range(self.tamanho_y):
                    continente = self._continente_mais_proximo(x, y)
                    dist = self._distancia_centro(x, y, continente['centro'])
                    recurso_base = int(100 * continente['recursos'] * (1 - dist/1000))
                    recurso_base = max(0, min(1000, recurso_base))
                    altura = self._calcular_altura(x, y, continente)
                    bioma = self._determinar_bioma(altura, dist, continente['clima'])
                    dados = struct.pack('ffII', altura, bioma, recurso_base, 0)
                    f.write(dados)
        
        logger.info(f"✅ Mapa continental criado")
    
    def _continente_mais_proximo(self, x: int, y: int) -> Dict:
        """Encontra o continente mais próximo"""
        return min(self.continentes, 
                  key=lambda c: ((c['centro'][0]-x)**2 + (c['centro'][1]-y)**2)**0.5)
    
    def _distancia_centro(self, x: int, y: int, centro: Tuple[int, int]) -> float:
        """Distância ao centro do continente"""
        return ((centro[0]-x)**2 + (centro[1]-y)**2)**0.5
    
    def _calcular_altura(self, x: int, y: int, continente: Dict) -> float:
        """Calcula altura do terreno com variação"""
        noise_x = math.sin(x * 0.01) * math.cos(y * 0.01)
        noise_y = math.cos(x * 0.01) * math.sin(y * 0.01)
        base = 0.5 + (noise_x + noise_y) * 0.2
        dist = self._distancia_centro(x, y, continente['centro'])
        montanha = max(0, 1 - dist/500) * 0.3
        return min(1.0, max(0.0, base + montanha))
    
    def _determinar_bioma(self, altura: float, dist: float, clima: str) -> float:
        """Determina bioma baseado em altura e clima"""
        if altura < 0.2:
            return 0.0
        elif altura < 0.3:
            return 1.0
        elif altura < 0.5:
            if clima == 'desertico':
                return 2.0
            elif clima == 'gelado':
                return 3.0
            else:
                return 4.0
        elif altura < 0.7:
            if clima == 'tropical':
                return 5.0
            elif clima == 'temperado':
                return 6.0
            else:
                return 7.0
        else:
            return 8.0
    
    def _abrir_mmap(self):
        """Abre mapa em memória mapeada"""
        self.arquivo = open(Config.MAPA_ARQUIVO, 'r+b')
        self.mmap = mmap.mmap(self.arquivo.fileno(), 0)
    
    def ler_celula(self, x: int, y: int) -> Tuple[float, float, int, int]:
        """Lê célula do mapa"""
        pos = (y * self.tamanho_x + x) * 16
        self.mmap.seek(pos)
        dados = self.mmap.read(16)
        return struct.unpack('ffII', dados)

# =========================
# DIALETOS EVOLUTIVOS
# =========================
class DialetoEvolutivo:
    """Linguagem que evolui regionalmente"""
    
    def __init__(self, nome: str, lingua_mae: 'DialetoEvolutivo' = None):
        self.nome = nome
        self.lingua_mae = lingua_mae
        self.palavras = {}
        self.gramatica = defaultdict(float)
        self.idade = 0
        self.distancia_mae = 0 if not lingua_mae else random.uniform(0.1, 0.5)
        
        if lingua_mae:
            self._herdar_vocabulario()
        else:
            self._criar_vocabulario_base()
    
    def _criar_vocabulario_base(self):
        """Cria vocabulário inicial"""
        conceitos = [
            'comida', 'agua', 'perigo', 'amigo', 'inimigo', 'casa',
            'ir', 'vir', 'dar', 'pegar', 'matar', 'fugir',
            'bom', 'ruim', 'grande', 'pequeno', 'quente', 'frio',
            'eu', 'voce', 'nos', 'eles', 'meu', 'seu',
            'deus', 'espirito', 'sagrado', 'tabu', 'ritual'
        ]
        
        for conceito in conceitos:
            self.palavras[conceito] = self._gerar_palavra()
    
    def _herdar_vocabulario(self):
        """Herda e modifica vocabulário da língua mãe"""
        for conceito, palavra in self.lingua_mae.palavras.items():
            if random.random() < self.distancia_mae:
                self.palavras[conceito] = self._mutar_palavra(palavra)
            else:
                self.palavras[conceito] = palavra
    
    def _gerar_palavra(self) -> str:
        """Gera uma palavra aleatória"""
        consoantes = 'bcdfghjklmnpqrstvwxyz'
        vogais = 'aeiou'
        tamanho = random.randint(3, 8)
        palavra = ''
        for i in range(tamanho):
            if i % 2 == 0:
                palavra += random.choice(consoantes)
            else:
                palavra += random.choice(vogais)
        return palavra
    
    def _mutar_palavra(self, palavra: str) -> str:
        """Aplica mutação em uma palavra"""
        palavras = list(palavra)
        if random.random() < 0.3:
            idx = random.randint(0, len(palavras)-1)
            palavras[idx] = random.choice('abcdefghijklmnopqrstuvwxyz')
        if random.random() < 0.2 and len(palavras) < 10:
            idx = random.randint(0, len(palavras))
            palavras.insert(idx, random.choice('aeiou'))
        if random.random() < 0.1 and len(palavras) > 3:
            idx = random.randint(0, len(palavras)-1)
            palavras.pop(idx)
        return ''.join(palavras)

# =========================
# RELIGIÕES EMERGENTES
# =========================
class Religiao:
    """Sistema de crenças que emerge naturalmente"""
    
    def __init__(self, nome: str, fundador: str = None):
        self.id = uuid.uuid4().hex[:8]
        self.nome = nome
        self.fundador = fundador
        self.deuses = self._criar_deuses()
        self.dogmas = random.sample(Config.DOGMAS, random.randint(2, 4))
        self.rituais = random.sample(Config.RITUAIS, random.randint(2, 3))
        self.idade = 0
        self.seguidores = 0
        self.escrituras = []
        self.profetas = []
        self.milagres = []
        self.guerras_santas = []
        self.cismas = []
    
    def _criar_deuses(self) -> List[Dict]:
        """Cria o panteão de deuses"""
        deuses = []
        for i in range(random.randint(1, Config.NUM_DEUSES)):
            deus = {
                'nome': self._gerar_nome_divino(),
                'dominio': random.choice(['sol', 'lua', 'morte', 'vida', 'guerra', 
                                          'amor', 'sabedoria', 'natureza', 'fogo', 'agua']),
                'personalidade': random.choice(['benevolente', 'vingativo', 'justo', 
                                                'caprichoso', 'sábio', 'furiouso']),
                'sagrado': self._gerar_sagrado()
            }
            deuses.append(deus)
        return deuses
    
    def _gerar_nome_divino(self) -> str:
        """Gera nome para um deus"""
        prefixos = ['A', 'Ba', 'Ca', 'Da', 'E', 'Fa', 'Ga', 'Ha', 'I', 'Ja']
        sufixos = ['el', 'on', 'us', 'um', 'ar', 'or']
        return random.choice(prefixos) + random.choice(sufixos)
    
    def _gerar_sagrado(self) -> str:
        """Gera um símbolo ou objeto sagrado"""
        objetos = ['espada', 'cálice', 'livro', 'árvore', 'pedra', 'fogo']
        return random.choice(objetos)

# =========================
# CIDADES AUTO-ORGANIZADAS
# =========================
class Cidade:
    """Assentamento que emerge naturalmente"""
    
    def __init__(self, x: int, y: int, continente: str):
        self.id = uuid.uuid4().hex[:8]
        self.nome = self._gerar_nome()
        self.x = x
        self.y = y
        self.continente = continente
        self.fundacao = datetime.now()
        self.populacao = random.randint(5, 20)
        self.recursos = defaultdict(int)
        self.construcoes = []
        self.lider = None
        self.leis = []
        self.exercito = 0
        self.riqueza = random.randint(100, 1000)
        self.aliados = []
        self.inimigos = []
        self.rotas_comerciais = []
        
        logger.info(f"🏰 Cidade {self.nome} fundada em ({x},{y})")
    
    def _gerar_nome(self) -> str:
        """Gera nome para cidade"""
        prefixos = ['A', 'Al', 'An', 'Ar', 'At', 'Bel', 'Ber', 'Ca', 'Car']
        sufixos = ['ia', 'ópolis', 'burgo', 'ville', 'grad', 'cidade']
        return random.choice(prefixos) + random.choice(sufixos)

# =========================
# CIVILIZAÇÃO
# =========================
class Civilizacao:
    """Sociedade complexa auto-organizada"""
    
    def __init__(self, nome: str, continente: str):
        self.id = uuid.uuid4().hex[:8]
        self.nome = nome
        self.continente = continente
        self.fundacao = datetime.now()
        self.cidades = []
        self.populacao_total = 0
        self.religiao_dominante = None
        self.dialeto = DialetoEvolutivo(nome)
        self.tecnologias = []
        self.leis = []
        self.governo = random.choice(['monarquia', 'oligarquia', 'democracia', 'teocracia'])
        self.ouro = random.randint(1000, 10000)
        self.exercito = 0
        self.aliadas = []
        self.inimigas = []
    
    def fundar_cidade(self, x: int, y: int) -> Cidade:
        """Funda uma nova cidade"""
        cidade = Cidade(x, y, self.continente)
        cidade.lider = self
        self.cidades.append(cidade)
        self.populacao_total += cidade.populacao
        return cidade

# =========================
# ECOSSISTEMA CIVILIZADO
# =========================
class EcossistemaCivilizado:
    """Mundo com civilizações emergentes"""
    
    def __init__(self):
        self.mapa = MapaContinental()
        self.linguagens = {}
        self.religioes = []
        self.civilizacoes = []
        self.organismos = {}
        self.ano = 0
        self.eras = ['pré-história', 'idade antiga', 'idade média', 'renascimento', 'moderna']
        self.era_atual = 0
        
        self._inicializar_linguagens()
        self._criar_religiao_primordial()
        
        logger.info(f"\n{'='*70}")
        logger.info("🌍 CIVILIZAÇÕES AUTO-ORGANIZADAS INICIADAS")
        logger.info(f"{'='*70}")
    
    def _inicializar_linguagens(self):
        """Cria línguas para cada continente"""
        lingua_mae = DialetoEvolutivo("Proto-Humano")
        self.linguagens['proto'] = lingua_mae
        
        for continente in self.mapa.continentes:
            dialeto = DialetoEvolutivo(f"{continente['nome']}_lingua", lingua_mae)
            self.linguagens[continente['nome']] = dialeto
    
    def _criar_religiao_primordial(self):
        """Cria a primeira religião"""
        religiao = Religiao("Culto Ancestral")
        self.religioes.append(religiao)
    
    def _criar_civilizacao_inicial(self):
        """Cria primeira civilização"""
        for continente in random.sample(self.mapa.continentes, 2):
            civ = Civilizacao(f"Civilização {continente['nome']}", continente['nome'])
            
            for _ in range(random.randint(2, 4)):
                x = continente['centro'][0] + random.randint(-100, 100)
                y = continente['centro'][1] + random.randint(-100, 100)
                civ.fundar_cidade(x, y)
            
            self.civilizacoes.append(civ)
            logger.info(f"🏛️ Nova civilização: {civ.nome} com {len(civ.cidades)} cidades")
    
    def executar(self, anos: int = 1000):
        """Executa simulação por X anos"""
        logger.info(f"\n⏳ Simulando {anos} anos de evolução...\n")
        
        for ano in range(anos):
            self.ano += 1
            
            if self.ano % 1000 == 0 and self.era_atual < len(self.eras)-1:
                self.era_atual += 1
                logger.info(f"\n📅 NOVA ERA: {self.eras[self.era_atual].upper()}!\n")
            
            if ano % 100 == 0:
                logger.info(f"   Progresso: {ano/anos*100:.1f}%")
        
        self._relatorio_final()
    
    def _relatorio_final(self):
        """Relatório final da simulação"""
        logger.info(f"\n{'='*70}")
        logger.info("📜 RELATÓRIO FINAL DA CIVILIZAÇÃO")
        logger.info(f"{'='*70}")
        logger.info(f"\n⏱️  Anos simulados: {self.ano}")
        logger.info(f"🏛️ Civilizações: {len(self.civilizacoes)}")
        logger.info(f"\n🗣️ Línguas: {len(self.linguagens)}")

# =========================
# MAIN
# =========================
def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - CIVILIZATION v44.0║
    ║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DA HISTÓRIA"  ║
    ║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                           ║
    ║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ MIGRAÇÃO CONTINENTAL ║
    ║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ DIALETOS EVOLUTIVOS  ║
    ║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ GUERRAS ENTRE ESPÉCIES║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    🌍 MUNDO: {Config.MUNDO_TAMANHO_X}x{Config.MUNDO_TAMANHO_Y} ({Config.MUNDO_TAMANHO_X*Config.MUNDO_TAMANHO_Y:,} células)
    🏛️ CONTINENTES: {Config.NUM_CONTINENTES}
    """)
    
    # Parse argumentos da linha de comando
    modo = 'civilizacao'
    populacao = 20
    mundo_timestamp = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--modo' and i+1 < len(sys.argv):
            modo = sys.argv[i+1]
        elif arg == '--populacao' and i+1 < len(sys.argv):
            populacao = int(sys.argv[i+1])
        elif arg == '--mundo' and i+1 < len(sys.argv):
            mundo_timestamp = sys.argv[i+1]
    
    logger.info(f"🎮 Modo: {modo}")
    logger.info(f"👥 População: {populacao}")
    
    mundo = EcossistemaCivilizado()
    mundo._criar_civilizacao_inicial()
    mundo.executar(anos=1000)
    
    logger.info("\n✅ Simulação concluída!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n👋 Fim da história")
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
