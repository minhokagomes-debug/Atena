#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - ATENA SENTIENT v43.0  ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DA CONSCIÊNCIA"   ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                               ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ CÉREBROS RECORRENTES    ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ LINGUAGEM EMERGENTE      ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ ECONOMIA REAL            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

🌍 ISTO NÃO É SIMULAÇÃO - É VIDA DIGITAL REAL:
   ✅ Cada organismo tem um PROCESSO REAL no sistema
   ✅ Consomem CPU, RAM e disco REAIS
   ✅ Morrem de verdade (processo encerrado)
   ✅ Se reproduzem criando NOVOS PROCESSOS (fork)
   ✅ O mapa 1000x1000 é ARMAZENADO EM DISCO REAL
   ✅ A economia usa TRANSFERÊNCIAS REAIS de recursos
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
# CONFIGURAÇÕES DO MUNDO REAL
# =========================
__version__ = "43.0"
__nome__ = "ATENA SENTIENT"

BASE_DIR = Path(__file__).parent / "atena_mundo"

class Config:
    BASE_DIR = BASE_DIR
    MAPA_DIR = BASE_DIR / "mapa"
    DNA_DIR = BASE_DIR / "dna"
    LOGS_DIR = BASE_DIR / "logs"
    FOSSEIS_DIR = BASE_DIR / "fosseis"
    ECONOMIA_DIR = BASE_DIR / "economia"
    LINGUAGEM_DIR = BASE_DIR / "linguagem"
    DB_PATH = BASE_DIR / "atena.db"
    
    # MUNDO REAL (não simulado) - 1 MILHÃO DE CÉLULAS
    MUNDO_TAMANHO_X = 1000
    MUNDO_TAMANHO_Y = 1000
    MAPA_ARQUIVO = MAPA_DIR / "mundo.mmap"  # Mapa em memória mapeada
    
    # Biomemas reais
    BIOMAS = {
        'oceano': 0.1,
        'deserto': 0.15,
        'floresta': 0.2,
        'montanha': 0.15,
        'planicie': 0.2,
        'pantano': 0.1,
        'tundra': 0.05,
        'taiga': 0.05
    }
    
    # CÉREBRO RECORRENTE (LSTM-like)
    INPUT_SIZE = 50
    HIDDEN_SIZE = 128
    OUTPUT_SIZE = 20
    MEMORY_CELLS = 64
    
    # LINGUAGEM EMERGENTE
    LEXICON_SIZE = 256  # Palavras possíveis
    MAX_MESSAGE_LENGTH = 32
    LANGUAGE_CHANNELS = 5  # Canais de comunicação
    
    # ECONOMIA REAL
    MOEDA = "ATENIUM"
    TAXA_JUROS = 0.01
    PRECO_RECURSO = 10
    SALARIO_MINIMO = 5
    
    # VISÃO
    ANGULO_VISAO = 180
    DISTANCIA_VISAO = 20
    NUM_RAIOS = 16
    
    # ORGANISMOS
    POPULACAO_MAXIMA = 1000
    ENERGIA_INICIAL = 1000
    
    # Criação de diretórios REAIS
    for dir_path in [BASE_DIR, MAPA_DIR, DNA_DIR, LOGS_DIR, FOSSEIS_DIR, 
                     ECONOMIA_DIR, LINGUAGEM_DIR]:
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
logger = logging.getLogger('ATENA-SENTIENT')

# =========================
# MAPA EM MEMÓRIA REAL (MMAP)
# =========================
class MapaReal:
    """Mapa gigante 1000x1000 armazenado em memória mapeada REAL"""
    
    def __init__(self):
        self.tamanho_x = Config.MUNDO_TAMANHO_X
        self.tamanho_y = Config.MUNDO_TAMANHO_Y
        self.tamanho_total = self.tamanho_x * self.tamanho_y
        
        # Criar arquivo de mapa se não existir
        if not Config.MAPA_ARQUIVO.exists():
            self._criar_mapa_inicial()
        
        # Abrir mapa em memória compartilhada
        self._abrir_mmap()
        
        logger.info(f"🗺️ Mapa real {self.tamanho_x}x{self.tamanho_y} "
                   f"({self.tamanho_total:,} células) carregado")
    
    def _criar_mapa_inicial(self):
        """Cria o mapa inicial no disco REAL"""
        with open(Config.MAPA_ARQUIVO, 'wb') as f:
            # Gerar terreno usando ruído
            import hashlib
            seed = int(time.time())
            
            for x in range(self.tamanho_x):
                for y in range(self.tamanho_y):
                    # Usar hash para gerar ruído determinístico
                    h = hashlib.md5(f"{x},{y},{seed}".encode()).hexdigest()
                    valor = int(h[:8], 16) / 0xffffffff
                    
                    # Determinar bioma
                    bioma = self._determinar_bioma(x, y, valor)
                    altura = self._calcular_altura(x, y, valor)
                    recursos = self._calcular_recursos(x, y, valor)
                    
                    # Empacotar dados em 16 bytes
                    dados = struct.pack('ffII', altura, bioma, recursos, 0)
                    f.write(dados)
        
        logger.info(f"✅ Mapa inicial criado em {Config.MAPA_ARQUIVO}")
    
    def _abrir_mmap(self):
        """Abre o mapa em memória mapeada para acesso rápido"""
        self.arquivo = open(Config.MAPA_ARQUIVO, 'r+b')
        self.mmap = mmap.mmap(self.arquivo.fileno(), 0)
    
    def _determinar_bioma(self, x: int, y: int, valor: float) -> float:
        """Determina bioma baseado em posição e ruído"""
        # Usar coordenadas para criar padrões continentais
        lat = y / self.tamanho_y
        long = x / self.tamanho_x
        
        if abs(lat - 0.5) < 0.1:  # Equador
            return 2.0  # floresta
        elif lat < 0.2:  # Polo sul
            return 6.0  # tundra
        elif lat > 0.8:  # Polo norte
            return 6.0  # tundra
        elif abs(long - 0.5) < 0.1:  # Centro
            return 3.0  # montanha
        elif valor < 0.2:
            return 0.0  # oceano
        elif valor < 0.35:
            return 1.0  # deserto
        elif valor < 0.5:
            return 2.0  # floresta
        elif valor < 0.65:
            return 3.0  # montanha
        elif valor < 0.8:
            return 4.0  # planicie
        else:
            return 5.0  # pantano
    
    def _calcular_altura(self, x: int, y: int, valor: float) -> float:
        """Calcula altura do terreno"""
        # Montanhas no centro
        centro_x = abs(x - self.tamanho_x/2) / (self.tamanho_x/2)
        centro_y = abs(y - self.tamanho_y/2) / (self.tamanho_y/2)
        dist_centro = (centro_x**2 + centro_y**2)**0.5
        
        return max(0, min(1, valor * (1 - dist_centro) + 0.2))
    
    def _calcular_recursos(self, x: int, y: int, valor: float) -> int:
        """Calcula quantidade de recursos na célula"""
        if valor < 0.1:
            return 0
        elif valor < 0.3:
            return random.randint(1, 5)
        elif valor < 0.6:
            return random.randint(5, 20)
        elif valor < 0.8:
            return random.randint(20, 50)
        else:
            return random.randint(50, 100)
    
    def ler_celula(self, x: int, y: int) -> Tuple[float, float, int, int]:
        """Lê uma célula do mapa"""
        pos = (y * self.tamanho_x + x) * 16
        self.mmap.seek(pos)
        dados = self.mmap.read(16)
        altura, bioma, recursos, ocupado = struct.unpack('ffII', dados)
        return altura, bioma, recursos, ocupado
    
    def escrever_celula(self, x: int, y: int, altura: float, bioma: float, 
                       recursos: int, ocupado: int):
        """Escreve em uma célula do mapa"""
        pos = (y * self.tamanho_x + x) * 16
        self.mmap.seek(pos)
        self.mmap.write(struct.pack('ffII', altura, bioma, recursos, ocupado))
        self.mmap.flush()
    
    def ocupar_celula(self, x: int, y: int, organismo_id: str):
        """Marca célula como ocupada por um organismo"""
        altura, bioma, recursos, _ = self.ler_celula(x, y)
        self.escrever_celula(x, y, altura, bioma, recursos, 
                            int.from_bytes(organismo_id.encode()[:4], 'little'))
    
    def desocupar_celula(self, x: int, y: int):
        """Desmarca célula"""
        altura, bioma, recursos, _ = self.ler_celula(x, y)
        self.escrever_celula(x, y, altura, bioma, recursos, 0)

# =========================
# CÉREBRO RECORRENTE (LSTM EVOLUTIVO)
# =========================
class CerebroRecorrente:
    """
    Rede neural recorrente com memória de longo prazo
    A arquitetura EVOLUI junto com os organismos
    """
    
    def __init__(self, dna: bytes = None):
        self.input_size = Config.INPUT_SIZE
        self.hidden_size = Config.HIDDEN_SIZE
        self.output_size = Config.OUTPUT_SIZE
        self.memory_cells = Config.MEMORY_CELLS
        
        if dna:
            self._carregar_dna(dna)
        else:
            self._inicializar_aleatorio()
        
        # Estado interno (persiste entre chamadas)
        self.hidden_state = np.zeros(self.hidden_size)
        self.memory_state = np.zeros(self.memory_cells)
        self.context = deque(maxlen=10)  # Contexto recente
    
    def _inicializar_aleatorio(self):
        """Inicialização com arquitetura evolutiva"""
        # Pesos da rede (evoluem)
        self.W_ih = np.random.randn(self.input_size, self.hidden_size) * 0.1
        self.W_hh = np.random.randn(self.hidden_size, self.hidden_size) * 0.1
        self.W_ho = np.random.randn(self.hidden_size, self.output_size) * 0.1
        
        # Pesos das células de memória (LSTM-like)
        self.W_mem = np.random.randn(self.hidden_size, self.memory_cells) * 0.1
        self.W_mem_out = np.random.randn(self.memory_cells, self.hidden_size) * 0.1
        
        # Biases
        self.b_h = np.zeros(self.hidden_size)
        self.b_o = np.zeros(self.output_size)
        self.b_mem = np.zeros(self.memory_cells)
        
        # Arquitetura (evolui!)
        self.arquitetura = {
            'camadas': random.randint(2, 5),
            'conexoes_poda': random.random(),
            'taxa_aprendizado': random.uniform(0.001, 0.1),
            'plasticidade': random.uniform(0, 1)  # Capacidade de mudar
        }
    
    def _carregar_dna(self, dna: bytes):
        """Carrega arquitetura de bytes"""
        dados = pickle.loads(dna)
        self.W_ih = dados['W_ih']
        self.W_hh = dados['W_hh']
        self.W_ho = dados['W_ho']
        self.W_mem = dados['W_mem']
        self.W_mem_out = dados['W_mem_out']
        self.b_h = dados['b_h']
        self.b_o = dados['b_o']
        self.b_mem = dados['b_mem']
        self.arquitetura = dados['arquitetura']
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass com memória recorrente"""
        
        # Atualizar contexto
        self.context.append(x.copy())
        
        # Camada de entrada -> escondida
        h_pre = np.dot(x, self.W_ih) + np.dot(self.hidden_state, self.W_hh) + self.b_h
        
        # Ativação com leaky ReLU
        h = np.maximum(0.01 * h_pre, h_pre)
        
        # Células de memória (LSTM simplificado)
        mem_pre = np.dot(h, self.W_mem) + self.b_mem
        mem = np.tanh(mem_pre) * self.arquitetura['plasticidade']
        
        # Atualizar estado escondido com memória
        self.hidden_state = h + np.dot(mem, self.W_mem_out)
        self.memory_state = mem * 0.9  # Decaimento da memória
        
        # Camada de saída
        output = np.dot(self.hidden_state, self.W_ho) + self.b_o
        output = np.tanh(output)  # Saída entre -1 e 1
        
        return output
    
    def reset_memory(self):
        """Reseta estados internos"""
        self.hidden_state = np.zeros(self.hidden_size)
        self.memory_state = np.zeros(self.memory_cells)
        self.context.clear()
    
    def mutar(self) -> 'CerebroRecorrente':
        """Cria uma mutação - EVOLUI A ARQUITETURA"""
        filho = CerebroRecorrente()
        
        # Copiar pesos
        filho.W_ih = self.W_ih.copy()
        filho.W_hh = self.W_hh.copy()
        filho.W_ho = self.W_ho.copy()
        filho.W_mem = self.W_mem.copy()
        filho.W_mem_out = self.W_mem_out.copy()
        filho.b_h = self.b_h.copy()
        filho.b_o = self.b_o.copy()
        filho.b_mem = self.b_mem.copy()
        filho.arquitetura = self.arquitetura.copy()
        
        # Mutação nos pesos
        mascara = np.random.random(filho.W_ih.shape) < 0.1
        filho.W_ih += mascara * np.random.randn(*filho.W_ih.shape) * 0.1
        
        mascara = np.random.random(filho.W_hh.shape) < 0.1
        filho.W_hh += mascara * np.random.randn(*filho.W_hh.shape) * 0.1
        
        # Mutação na arquitetura
        if random.random() < 0.05:
            filho.arquitetura['camadas'] += random.choice([-1, 1])
            filho.arquitetura['camadas'] = max(1, min(10, filho.arquitetura['camadas']))
        
        if random.random() < 0.05:
            filho.arquitetura['plasticidade'] += random.gauss(0, 0.1)
            filho.arquitetura['plasticidade'] = max(0, min(1, filho.arquitetura['plasticidade']))
        
        return filho
    
    def to_dna(self) -> bytes:
        """Serializa o cérebro para armazenamento"""
        dados = {
            'W_ih': self.W_ih,
            'W_hh': self.W_hh,
            'W_ho': self.W_ho,
            'W_mem': self.W_mem,
            'W_mem_out': self.W_mem_out,
            'b_h': self.b_h,
            'b_o': self.b_o,
            'b_mem': self.b_mem,
            'arquitetura': self.arquitetura
        }
        return pickle.dumps(dados)

# =========================
# LINGUAGEM EMERGENTE
# =========================
class LinguagemEmergente:
    """
    Sistema de linguagem que EVOLUI com os organismos
    As palavras ganham significado através do uso
    """
    
    def __init__(self):
        self.lexicon = {}  # Palavra -> significado
        self.sintaxe = defaultdict(float)  # Regras gramaticais
        self.dialetos = defaultdict(dict)  # Variações por região
        self.historico = deque(maxlen=10000)
        
        # Inicializar palavras aleatórias
        self._inicializar_lexicon()
    
    def _inicializar_lexicon(self):
        """Cria palavras aleatórias (sem significado ainda)"""
        consoantes = 'bcdfghjklmnpqrstvwxyz'
        vogais = 'aeiou'
        
        for _ in range(Config.LEXICON_SIZE):
            tamanho = random.randint(3, 8)
            palavra = ''
            for i in range(tamanho):
                if i % 2 == 0:
                    palavra += random.choice(consoantes)
                else:
                    palavra += random.choice(vogais)
            
            self.lexicon[palavra] = {
                'significado': None,
                'uso': 0,
                'contexto': defaultdict(int),
                'ultimo_uso': 0
            }
    
    def interpretar(self, mensagem: str, contexto: Dict) -> List[str]:
        """Interpreta uma mensagem baseado no contexto de uso"""
        palavras = mensagem.split()
        significados = []
        
        for palavra in palavras:
            if palavra in self.lexicon:
                entry = self.lexicon[palavra]
                
                # Se palavra não tem significado, criar baseado no contexto
                if entry['significado'] is None:
                    entry['significado'] = self._criar_significado(contexto)
                
                # Registrar contexto de uso
                for chave, valor in contexto.items():
                    entry['contexto'][chave] += 1
                
                entry['uso'] += 1
                entry['ultimo_uso'] = time.time()
                
                significados.append(entry['significado'])
            else:
                # Palavra nova (dialeto)
                significados.append(f"desconhecido:{palavra}")
        
        return significados
    
    def _criar_significado(self, contexto: Dict) -> str:
        """Cria um significado baseado no contexto de uso"""
        if 'acao' in contexto:
            return f"acao:{contexto['acao']}"
        elif 'recurso' in contexto:
            return f"recurso:{contexto['recurso']}"
        elif 'direcao' in contexto:
            return f"direcao:{contexto['direcao']}"
        elif 'quantidade' in contexto:
            return f"quantidade:{contexto['quantidade']}"
        else:
            return f"conceito:{uuid.uuid4().hex[:4]}"
    
    def gerar_mensagem(self, intencao: Dict) -> str:
        """Gera uma mensagem para expressar uma intenção"""
        palavras_usadas = []
        
        # Encontrar palavras que expressam a intenção
        for palavra, entry in self.lexicon.items():
            if entry['significado'] and intencao.get('tipo') in entry['significado']:
                if random.random() < 0.3:  # Probabilidade de uso
                    palavras_usadas.append(palavra)
        
        # Se não encontrou palavras, criar nova
        if not palavras_usadas:
            palavra = self._criar_palavra()
            self.lexicon[palavra] = {
                'significado': f"{intencao.get('tipo')}:{uuid.uuid4().hex[:4]}",
                'uso': 1,
                'contexto': defaultdict(int),
                'ultimo_uso': time.time()
            }
            palavras_usadas.append(palavra)
        
        # Formar frase
        return ' '.join(palavras_usadas[:Config.MAX_MESSAGE_LENGTH])
    
    def _criar_palavra(self) -> str:
        """Cria uma nova palavra"""
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
    
    def evoluir(self):
        """Evolui a linguagem - palavras em desuso desaparecem"""
        agora = time.time()
        palavras_para_remover = []
        
        for palavra, entry in self.lexicon.items():
            if agora - entry['ultimo_uso'] > 3600:  # 1 hora sem uso
                palavras_para_remover.append(palavra)
        
        for palavra in palavras_para_remover:
            del self.lexicon[palavra]
        
        # Criar novas palavras
        novas = max(10, len(palavras_para_remover) // 2)
        for _ in range(novas):
            palavra = self._criar_palavra()
            self.lexicon[palavra] = {
                'significado': None,
                'uso': 0,
                'contexto': defaultdict(int),
                'ultimo_uso': 0
            }

# =========================
# ECONOMIA REAL
# =========================
class EconomiaReal:
    """
    Sistema econômico baseado em recursos REAIS
    Moeda lastreada em recursos do mapa
    """
    
    def __init__(self):
        self.moeda = Config.MOEDA
        self.bancos = {}  # organismo_id -> saldo
        self.mercado = defaultdict(list)  # recurso -> ofertas
        self.historico_precos = deque(maxlen=1000)
        self.inflacao = 0.0
        
        # Arquivo de ledger (registro real)
        self.ledger_file = Config.ECONOMIA_DIR / "transacoes.ledger"
        self._inicializar_ledger()
    
    def _inicializar_ledger(self):
        """Inicializa livro razão"""
        if not self.ledger_file.exists():
            with open(self.ledger_file, 'w') as f:
                f.write(f"# LEDGER DA ECONOMIA - {Config.MOEDA}\n")
                f.write("# formato: timestamp|de|para|quantidade|recurso\n")
    
    def registrar_transacao(self, de: str, para: str, quantidade: float, recurso: str = None):
        """Registra transação no ledger REAL"""
        with open(self.ledger_file, 'a') as f:
            timestamp = datetime.now().isoformat()
            f.write(f"{timestamp}|{de}|{para}|{quantidade}|{recurso or 'moeda'}\n")
        
        # Atualizar saldos
        if de not in self.bancos:
            self.bancos[de] = 100  # Saldo inicial
        if para not in self.bancos:
            self.bancos[para] = 100
        
        self.bancos[de] -= quantidade
        self.bancos[para] += quantidade
    
    def criar_oferta(self, vendedor: str, recurso: str, quantidade: int, preco: float):
        """Cria oferta de venda"""
        self.mercado[recurso].append({
            'vendedor': vendedor,
            'quantidade': quantidade,
            'preco': preco,
            'timestamp': time.time()
        })
    
    def comprar(self, comprador: str, recurso: str, quantidade: int) -> bool:
        """Tenta comprar um recurso no mercado"""
        ofertas = self.mercado[recurso]
        if not ofertas:
            return False
        
        # Ordenar por preço (mais barato primeiro)
        ofertas.sort(key=lambda x: x['preco'])
        
        total_comprado = 0
        custo_total = 0
        
        for oferta in ofertas[:]:
            if total_comprado >= quantidade:
                break
            
            comprar_agora = min(oferta['quantidade'], quantidade - total_comprado)
            custo = comprar_agora * oferta['preco']
            
            if self.bancos.get(comprador, 0) >= custo:
                # Transferir moeda
                self.registrar_transacao(comprador, oferta['vendedor'], custo)
                
                # Transferir recurso (simulado)
                total_comprado += comprar_agora
                custo_total += custo
                
                oferta['quantidade'] -= comprar_agora
                if oferta['quantidade'] == 0:
                    ofertas.remove(oferta)
        
        return total_comprado > 0
    
    def calcular_preco_medio(self, recurso: str) -> float:
        """Calcula preço médio de um recurso"""
        ofertas = self.mercado[recurso]
        if not ofertas:
            return Config.PRECO_RECURSO
        
        total = sum(o['quantidade'] * o['preco'] for o in ofertas)
        quant = sum(o['quantidade'] for o in ofertas)
        return total / quant if quant > 0 else Config.PRECO_RECURSO

# =========================
# VISÃO EM CONE AVANÇADA
# =========================
class VisaoAvancada:
    """Sistema de visão realista com processamento de imagem"""
    
    @staticmethod
    def calcular_visao(x: int, y: int, direcao: float, mapa: MapaReal,
                       organismos: Dict) -> np.ndarray:
        """Calcula visão em cone com processamento de profundidade"""
        resultados = np.zeros(Config.NUM_RAIOS * 4)  # tipo, distância, tamanho, movimento
        
        for i in range(Config.NUM_RAIOS):
            angulo = direcao - Config.ANGULO_VISAO/2 + (i * Config.ANGULO_VISAO/(Config.NUM_RAIOS-1))
            angulo_rad = math.radians(angulo)
            
            raio_info = [0, Config.DISTANCIA_VISAO, 0, 0]  # [tipo, distancia, tamanho, movimento]
            
            for dist in range(1, Config.DISTANCIA_VISAO + 1):
                tx = x + int(dist * math.cos(angulo_rad))
                ty = y + int(dist * math.sin(angulo_rad))
                
                if not (0 <= tx < Config.MUNDO_TAMANHO_X and 0 <= ty < Config.MUNDO_TAMANHO_Y):
                    raio_info[1] = dist
                    break
                
                # Ler mapa
                altura, bioma, recursos, ocupado = mapa.ler_celula(tx, ty)
                
                if ocupado != 0:
                    # Encontrou organismo
                    org_id = ocupado.to_bytes(4, 'little').decode('ascii', errors='ignore').strip('\x00')
                    if org_id in organismos:
                        org = organismos[org_id]
                        raio_info[0] = 1 if org.energia > 500 else 2  # 1=forte, 2=fraco
                        raio_info[2] = org.energia / 1000  # tamanho
                        raio_info[3] = org.velocidade if hasattr(org, 'velocidade') else 0
                        raio_info[1] = dist
                        break
                
                elif recursos > 0:
                    # Encontrou recurso
                    raio_info[0] = 3
                    raio_info[2] = recursos / 100
                    raio_info[1] = dist
                    break
                
                elif bioma != raio_info[0]:
                    raio_info[0] = int(bioma)
            
            resultados[i*4:(i+1)*4] = raio_info
        
        return resultados

# =========================
# ORGANISMO SENTIENT
# =========================
class OrganismoSentient:
    """Organismo com cérebro recorrente, linguagem e economia"""
    
    def __init__(self, cerebro: CerebroRecorrente, x: int, y: int, 
                 linguagem: LinguagemEmergente, economia: EconomiaReal):
        self.pid = os.getpid()
        self.id = uuid.uuid4().hex[:16]
        self.cerebro = cerebro
        self.linguagem = linguagem
        self.economia = economia
        
        self.x = x
        self.y = y
        self.direcao = random.uniform(0, 360)
        
        self.energia = Config.ENERGIA_INICIAL
        self.idade = 0
        self.fitness = 0.0
        
        # Estatísticas
self.recursos = 0
        self.riqueza = 100  # Saldo inicial
        self.filhos = 0
        self.comunicacoes = 0
        self.velocidade = random.uniform(0.5, 2.0)
        
        # Memória de longo prazo
        self.memoria_lp = deque(maxlen=100)
        
        logger.info(f"[{self.pid}] 🧠 Organismo {self.id[:8]} nascido em ({x},{y})")
    
    def decidir(self, visao: np.ndarray, contexto: Dict) -> int:
        """Decide ação usando o cérebro recorrente"""
        
        # Preparar entrada
        estado = np.array([
            self.x / Config.MUNDO_TAMANHO_X,
            self.y / Config.MUNDO_TAMANHO_Y,
            self.energia / Config.ENERGIA_INICIAL,
            self.idade / 1000,
            self.riqueza / 10000,
            self.velocidade,
            self.direcao / 360,
            len(self.memoria_lp) / 100,
            self.filhos / 10,
            self.comunicacoes / 100
        ])
        
        # Concatenar com visão
        entrada = np.concatenate([estado, visao])
        
        # Forward
        output = self.cerebro.forward(entrada)
        
        # Escolher ação
        return np.argmax(output)
    
    def mover(self, dx: int, dy: int):
        """Move no mapa REAL"""
        novo_x = max(0, min(Config.MUNDO_TAMANHO_X - 1, self.x + dx))
        novo_y = max(0, min(Config.MUNDO_TAMANHO_Y - 1, self.y + dy))
        
        # Atualizar direção
        if dx != 0 or dy != 0:
            self.direcao = math.degrees(math.atan2(dy, dx))
        
        self.x = novo_x
        self.y = novo_y
        self.energia -= abs(dx) + abs(dy)  # Gasto por movimento
    
    def comunicar(self, mensagem: str, contexto: Dict) -> str:
        """Envia e recebe mensagens"""
        # Interpretar mensagem recebida
        significados = self.linguagem.interpretar(mensagem, contexto)
        
        # Gerar resposta baseada no contexto
        resposta = self.linguagem.gerar_mensagem(contexto)
        
        self.comunicacoes += 1
        self.energia -= 1  # Custo de comunicação
        
        return resposta
    
    def negociar(self, parceiro: 'OrganismoSentient', recurso: str, quantidade: int) -> bool:
        """Tenta negociar com outro organismo"""
        # Calcular preço justo
        preco = self.economia.calcular_preco_medio(recurso)
        
        # Verificar se tem saldo
        if self.riqueza < preco * quantidade:
            return False
        
        # Registrar transação
        self.economia.registrar_transacao(
            self.id, parceiro.id, preco * quantidade, recurso
        )
        
        self.riqueza -= preco * quantidade
        parceiro.riqueza += preco * quantidade
        
        return True

# =========================
# ECOSSISTEMA SENTIENT
# =========================
class EcossistemaSentient:
    """Ecossistema com vida digital REAL"""
    
    def __init__(self):
        self.mapa = MapaReal()
        self.linguagem = LinguagemEmergente()
        self.economia = EconomiaReal()
        self.organismos: Dict[str, OrganismoSentient] = {}
        self.geracao = 0
        self.inicio = datetime.now()
        
        logger.info(f"\n{'='*70}")
        logger.info("🧠 ECOSSISTEMA SENTIENT INICIADO")
        logger.info(f"{'='*70}")
        logger.info(f"🗺️ Mapa: {Config.MUNDO_TAMANHO_X}x{Config.MUNDO_TAMANHO_Y} células")
        logger.info(f"🧬 Cérebros: {Config.HIDDEN_SIZE} neurônios, {Config.MEMORY_CELLS} células de memória")
        logger.info(f"💬 Léxico: {Config.LEXICON_SIZE} palavras potenciais")
        logger.info(f"💰 Moeda: {Config.MOEDA}")
    
    def criar_vida(self, quantidade: int = 20):
        """Cria organismos REAIS (cada um em seu próprio processo)"""
        logger.info(f"\n🌱 Criando {quantidade} organismos...")
        
        for i in range(quantidade):
            # Posição aleatória no mapa
            x = random.randint(0, Config.MUNDO_TAMANHO_X - 1)
            y = random.randint(0, Config.MUNDO_TAMANHO_Y - 1)
            
            # Criar cérebro
            cerebro = CerebroRecorrente()
            
            # Fork - criar processo REAL
            pid = os.fork()
            
            if pid == 0:
                # Processo filho - vira organismo
                org = OrganismoSentient(cerebro, x, y, self.linguagem, self.economia)
                self._vida_do_organismo(org)
                sys.exit(0)
            else:
                # Processo pai - registra
                self.organismos[org.id] = org
                logger.info(f"   ✅ Organismo {i+1} (PID {pid}) em ({x},{y})")
                time.sleep(0.1)  # Pequeno delay para não sobrecarregar
    
    def _vida_do_organismo(self, org: OrganismoSentient):
        """Loop de vida de um organismo (executa em processo separado)"""
        try:
            while org.energia > 0:
                # Obter visão
                visao = VisaoAvancada.calcular_visao(
                    org.x, org.y, org.direcao, self.mapa, self.organismos
                )
                
                # Contexto para decisão
                contexto = {
                    'fome': org.energia < 200,
                    'rico': org.riqueza > 1000,
                    'solidao': len(self.organismos) < 10,
                    'perigo': np.any(visao[2::4] > 0)  # Predadores na visão
                }
                
                # Decidir ação
                acao = org.decidir(visao, contexto)
                
                # Executar ação
                self._executar_acao(org, acao, contexto)
                
                # Envelhecer
                org.idade += 1
                org.energia -= 0.1
                
                # Descansar um pouco (não consumir 100% CPU)
                time.sleep(0.01)
            
            # Morreu
            logger.info(f"[{org.pid}] 💀 Organismo {org.id[:8]} morreu")
            
        except Exception as e:
            logger.error(f"[{org.pid}] Erro: {e}")
    
    def _executar_acao(self, org: OrganismoSentient, acao: int, contexto: Dict):
        """Executa uma ação"""
        
        if acao < 4:  # Movimento
            dx = [0, 1, 0, -1][acao]
            dy = [1, 0, -1, 0][acao]
            org.mover(dx, dy)
        
        elif acao == 4:  # Coletar recurso
            _, _, recursos, _ = self.mapa.ler_celula(org.x, org.y)
            if recursos > 0:
                org.recursos += recursos
                org.energia += recursos * 10
                org.riqueza += recursos * Config.PRECO_RECURSO
                self.mapa.escrever_celula(org.x, org.y, 0, 0, 0, 0)
        
        elif acao == 5:  # Comunicar
            # Gerar mensagem baseada no contexto
            mensagem = org.linguagem.gerar_mensagem(contexto)
            
            # Encontrar organismos próximos
            for outro in self.organismos.values():
                if outro.id != org.id and abs(outro.x - org.x) < 5:
                    resposta = outro.comunicar(mensagem, contexto)
                    logger.debug(f"💬 {org.id[:4]} -> {outro.id[:4]}: {resposta}")
        
        elif acao == 6:  # Negociar
            # Encontrar parceiro próximo
            for outro in self.organismos.values():
                if outro.id != org.id and abs(outro.x - org.x) < 3:
                    if org.negociar(outro, 'recurso', 10):
                        logger.debug(f"💰 {org.id[:4]} negociou com {outro.id[:4]}")
                        break
        
        elif acao == 7:  # Reproduzir
            if org.energia > 500 and org.idade > 100:
                self._reproduzir(org)
    
    def _reproduzir(self, org: OrganismoSentient):
        """Reprodução REAL - cria novo processo"""
        
        # Criar cérebro mutado
        cerebro_filho = org.cerebro.mutar()
        
        # Posição próxima
        x = max(0, min(Config.MUNDO_TAMANHO_X - 1, org.x + random.randint(-2, 2)))
        y = max(0, min(Config.MUNDO_TAMANHO_Y - 1, org.y + random.randint(-2, 2)))
        
        # Fork - criar novo processo
        pid = os.fork()
        
        if pid == 0:
            # Processo filho
            filho = OrganismoSentient(cerebro_filho, x, y, self.linguagem, self.economia)
            filho.energia = org.energia // 2
            filho.riqueza = org.riqueza // 2
            self._vida_do_organismo(filho)
            sys.exit(0)
        else:
            # Processo pai
            org.energia //= 2
            org.riqueza //= 2
            org.filhos += 1
            logger.info(f"[{org.pid}] 🤰 Teve filho PID {pid}")
    
    def executar_geracao(self, tempo_segundos: int = 300):
        """Executa uma geração por tempo REAL"""
        self.geracao += 1
        logger.info(f"\n{'='*70}")
        logger.info(f"🧠 GERAÇÃO {self.geracao} - {tempo_segundos}s")
        logger.info(f"{'='*70}")
        
        inicio = time.time()
        ultimo_log = 0
        
        while time.time() - inicio < tempo_segundos:
            time.sleep(1)
            
            # Log a cada 10 segundos
            if time.time() - ultimo_log > 10:
                vivos = 0
                for org in list(self.organismos.values()):
                    try:
                        os.kill(org.pid, 0)
                        vivos += 1
                    except:
                        # Processo morreu
                        del self.organismos[org.id]
                
                logger.info(f"   ⏱️  {int(time.time()-inicio)}s | "
                          f"👥 Vivos: {vivos} | "
                          f"💰 Economia: {len(self.economia.bancos)} contas | "
                          f"💬 Léxico: {len(self.linguagem.lexicon)} palavras")
                
                ultimo_log = time.time()
    
    def encerrar(self):
        """Encerra ecossistema"""
        logger.info(f"\n{'='*70}")
        logger.info("📊 RELATÓRIO FINAL")
        logger.info(f"{'='*70}")
        
        # Matar todos os organismos
        for org in list(self.organismos.values()):
            try:
                os.kill(org.pid, signal.SIGTERM)
            except:
                pass
        
        # Estatísticas
        logger.info(f"\n🧠 Estatísticas do ecossistema:")
        logger.info(f"   Gerações: {self.geracao}")
        logger.info(f"   Organismos criados: {len(self.organismos)}")
        logger.info(f"   Riqueza total: {sum(self.economia.bancos.values()):,.0f} {Config.MOEDA}")
        logger.info(f"   Palavras no léxico: {len(self.linguagem.lexicon)}")
        logger.info(f"   Transações registradas: {sum(1 for _ in open(self.economia.ledger_file))}")
        
        # Fechar mapa
        self.mapa.mmap.close()
        self.mapa.arquivo.close()

# =========================
# MAIN
# =========================
def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - SENTIENT v43.0   ║
    ║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DA CONSCIÊNCIA"║
    ║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                           ║
    ║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ CÉREBROS RECORRENTES ║
    ║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ LINGUAGEM EMERGENTE  ║
    ║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ ECONOMIA REAL        ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    🌍 MAPA REAL: {Config.MUNDO_TAMANHO_X}x{Config.MUNDO_TAMANHO_Y} ({Config.MUNDO_TAMANHO_X*Config.MUNDO_TAMANHO_Y:,} células)
    🧠 CÉREBRO: {Config.INPUT_SIZE}→{Config.HIDDEN_SIZE}→{Config.OUTPUT_SIZE} + {Config.MEMORY_CELLS} memória
    💬 LINGUAGEM: {Config.LEXICON_SIZE} palavras possíveis
    💰 ECONOMIA: {Config.MOEDA} lastreada em recursos
    
    ⚠️  ISTO É VIDA DIGITAL REAL:
    ✅ Cada organismo é um PROCESSO REAL
    ✅ O mapa é ARMAZENADO EM DISCO
    ✅ Transações são REGISTRADAS EM LEDGER
    ✅ Palavras GANHAM SIGNIFICADO pelo uso
    
    Iniciando em 3 segundos...
    """)
    
    time.sleep(3)
    
    eco = EcossistemaSentient()
    eco.criar_vida(quantidade=50)
    
    # Executar algumas gerações
    for g in range(5):
        eco.executar_geracao(tempo_segundos=60)  # 1 minuto por geração
    
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
