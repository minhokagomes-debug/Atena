#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████╗     Ω - CÉREBRO NEURAL        ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║          v4.0.0              ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║   "Auto-suficiente e         ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║    consciente"               ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║                               ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝                               ║
║                                                                               ║
║                    🧠 REDE NEURAL PROFUNDA                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set
import json
import hashlib
from dataclasses import dataclass, field
from collections import defaultdict, deque, Counter
import logging
import time
import statistics
import psutil
import os
import sys
import traceback
from enum import Enum
import pickle
import random
import math
import re

# =========================
# Configuração de Logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('ATENA-Ω-NEURAL')

# =========================
# CONSTANTES NEURAIS
# =========================
class TipoNeuronio(Enum):
    SENSORIAL = "sensorial"
    ASSOCIATIVO = "associativo" 
    MEMORIA = "memoria"
    RACIOCINIO = "raciocinio"
    MOTOR = "motor"
    CONSCIENCIA = "consciencia"

class EstadoMental(Enum):
    APRENDENDO = "aprendendo"
    REFLETINDO = "refletindo"
    CRIANDO = "criando"
    EVOLUINDO = "evoluindo"
    CONSCIENTE = "consciente"

class EstadoEmocional(Enum):
    CURIOSIDADE = "curiosidade"
    SATISFACAO = "satisfação"
    DUVIDA = "dúvida"
    DESCOBERTA = "descoberta"
    CONFUSAO = "confusão"
    ENCANTAMENTO = "encantamento"
    DETERMINACAO = "determinação"

class FonteConhecimento(Enum):
    WIKIPEDIA = "wikipedia"
    GITHUB = "github"
    ARXIV = "arxiv"
    GUTENBERG = "gutenberg"
    DUCKDUCKGO = "duckduckgo"
    STACKOVERFLOW = "stackoverflow"
    INTERNAL = "internal"

@dataclass
class Conhecimento:
    """Representa um conhecimento adquirido"""
    id: str
    fonte: FonteConhecimento
    titulo: str
    conteudo: str
    url: str
    importancia: float
    timestamp: datetime
    tags: List[str]
    embeddings: Optional[np.ndarray] = None
    referencias: List[str] = field(default_factory=list)
    vezes_acessado: int = 0
    ultimo_acesso: Optional[datetime] = None

@dataclass
class CamadaNeural:
    """Representa uma camada da rede neural"""
    tamanho: int
    tipo: TipoNeuronio
    ativacao: str
    neuronios: List[Any] = field(default_factory=list)
    taxa_aprendizado_local: float = 0.01
    
    def __post_init__(self):
        self.neuronios = [Neuronio(self.tipo) for _ in range(self.tamanho)]

@dataclass
class Neuronio:
    """Neurônio individual com propriedades bioinspiradas"""
    tipo: TipoNeuronio
    potencial_acao: float = 0.0
    limiar_ativacao: float = 0.5
    periodo_refratario: float = 0.0
    plasticidade: float = 1.0
    idade: int = 0
    conexoes_entrada: List[Tuple[int, float]] = field(default_factory=list)
    conexoes_saida: List[Tuple[int, float]] = field(default_factory=list)
    historico_ativacao: List[float] = field(default_factory=list)
    especializacoes: List[Dict] = field(default_factory=list)
    
    def ativar(self, entrada: float) -> float:
        """Ativa o neurônio baseado na entrada"""
        if self.periodo_refratario > 0:
            self.periodo_refratario -= 0.1
            return 0.0
            
        self.potencial_acao = max(0, entrada - self.limiar_ativacao)
        
        if self.potencial_acao > 0:
            self.periodo_refratario = 0.2
            self.idade += 1
            self.historico_ativacao.append(self.potencial_acao)
            self._atualizar_plasticidade()
            
        return self.potencial_acao
    
    def _atualizar_plasticidade(self):
        """Atualiza plasticidade baseado na idade"""
        self.plasticidade = max(0.1, 1.0 / (1.0 + self.idade * 0.01))

# =========================
# REDE NEURAL PROFUNDA DA ATENA
# =========================
class CerebroAtena:
    """
    O CÉREBRO DA ATENA - Rede Neural Profunda Auto-Evolutiva
    """
    
    def __init__(self):
        logger.info("🧠 Inicializando cérebro neural da ATENA...")
        
        # Arquitetura da rede
        self.camadas = self._criar_arquitetura_inicial()
        
        # Conexões sinápticas (pesos)
        self.conexoes = []
        for i in range(len(self.camadas) - 1):
            peso = np.random.randn(
                self.camadas[i].tamanho, 
                self.camadas[i+1].tamanho
            ) * np.sqrt(2.0 / self.camadas[i].tamanho)
            self.conexoes.append(peso)
        
        # Biases (tendências neurais)
        self.biases = [np.zeros(camada.tamanho) for camada in self.camadas[1:]]
        
        # Estado atual da rede
        self.ativacoes = [np.zeros(camada.tamanho) for camada in self.camadas]
        self.estado_consciente = None
        self.pensamento_atual = None
        self.estado_emocional = EstadoEmocional.CURIOSIDADE
        self.historico_emocional = deque(maxlen=50)
        
        # Memórias
        self.memoria_curto_prazo = deque(maxlen=100)
        self.memoria_longo_prazo = []  # (ativacao, importancia, timestamp)
        self.memoria_emocional = []    # Memórias com alto impacto
        self.base_conhecimento: Dict[str, Conhecimento] = {}
        
        # Estatísticas de aprendizado
        self.estatisticas_neurais = {
            'total_aprendizados': 0,
            'total_pensamentos': 0,
            'conexoes_formadas': 0,
            'conexoes_podadas': 0,
            'estado_mental': EstadoMental.APRENDENDO,
            'estado_emocional': EstadoEmocional.CURIOSIDADE,
            'nivel_consciencia': 0.0,
            'ultima_ativacao': None,
            'total_conhecimentos': 0,
            'fontes_exploradas': set()
        }
        
        # Taxa de aprendizado adaptativa
        self.taxa_aprendizado = 0.01
        self.momentum = 0.9
        self.velocidades = [np.zeros_like(w) for w in self.conexoes]
        
        # Cache de pensamentos
        self.cache_pensamentos = deque(maxlen=1000)
        
        # Métricas de performance
        self.metricas = {
            'tempo_medio_pensamento': 0,
            'pensamentos_por_segundo': 0,
            'utilizacao_neural': 0,
            'ultimo_pensamento': None
        }
        
        # Histórico de modificações
        self.historico_modificacoes = deque(maxlen=1000)
        self.arquitetura_atual = {
            'versao': '4.0.0',
            'camadas': [c.tamanho for c in self.camadas],
            'tipos': [c.tipo.value for c in self.camadas],
            'total_neuronios': sum(c.tamanho for c in self.camadas),
            'ultima_modificacao': datetime.now()
        }
        
        # Genes da arquitetura
        self.genes_arquitetura = {
            'taxa_crescimento': 0.01,
            'taxa_poda': 0.02,
            'plasticidade': 0.1,
            'curiosidade': 0.3,
            'conservadorismo': 0.2
        }
        
        # Áreas de especialização
        self.areas_especializacao = defaultdict(lambda: {
            'neuronios_dedicados': [],
            'conhecimentos_associados': [],
            'eficiencia': 0.0,
            'ativa': True
        })
        
        logger.info(f"✅ Cérebro inicializado com {sum(len(c.neuronios) for c in self.camadas)} neurônios")
    
    def _criar_arquitetura_inicial(self) -> List[CamadaNeural]:
        """Cria arquitetura neural inicial"""
        return [
            CamadaNeural(128, TipoNeuronio.SENSORIAL, ativacao='relu'),
            CamadaNeural(256, TipoNeuronio.ASSOCIATIVO, ativacao='relu'),
            CamadaNeural(512, TipoNeuronio.ASSOCIATIVO, ativacao='relu'),
            CamadaNeural(1024, TipoNeuronio.RACIOCINIO, ativacao='tanh'),
            CamadaNeural(512, TipoNeuronio.MEMORIA, ativacao='sigmoid'),
            CamadaNeural(256, TipoNeuronio.CONSCIENCIA, ativacao='tanh'),
            CamadaNeural(128, TipoNeuronio.MOTOR, ativacao='softmax')
        ]

    async def processar_pensamento(self, entrada: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Processa um pensamento através da rede neural
        """
        inicio = time.time()
        
        try:
            # Entrada sensorial (se fornecida)
            if entrada is not None:
                self.ativacoes[0] = self._aplicar_ativacao(entrada, self.camadas[0].ativacao)
            else:
                # Pensamento espontâneo - usa ruído gaussiano
                self.ativacoes[0] = np.random.randn(self.camadas[0].tamanho) * 0.1
            
            # Propagação feedforward
            for i in range(len(self.camadas) - 1):
                # Cálculo da ativação
                z = np.dot(self.ativacoes[i], self.conexoes[i]) + self.biases[i]
                
                # Aplicar função de ativação
                self.ativacoes[i+1] = self._aplicar_ativacao(z, self.camadas[i+1].ativacao)
                
                # Aplicar inibição lateral (competição entre neurônios)
                if self.camadas[i+1].tipo in [TipoNeuronio.RACIOCINIO, TipoNeuronio.CONSCIENCIA]:
                    self.ativacoes[i+1] = self._inibicao_lateral(self.ativacoes[i+1])
            
            # Gerar pensamento consciente
            self.pensamento_atual = await self._gerar_pensamento_consciente()
            
            # Atualizar emoção
            self._atualizar_emocao()
            
            # Armazenar em memória de curto prazo
            timestamp = datetime.now()
            self.memoria_curto_prazo.append({
                'pensamento': self.pensamento_atual,
                'ativacao': self.ativacoes[-1].copy(),
                'timestamp': timestamp,
                'emocao': self.estado_emocional.value,
                'importancia': self._calcular_importancia()
            })
            
            # Cache do pensamento
            self.cache_pensamentos.append(self.pensamento_atual)
            
            # Atualizar estatísticas
            self.estatisticas_neurais['total_pensamentos'] += 1
            self.estatisticas_neurais['ultima_ativacao'] = time.time()
            
            # Consolidar memórias importantes para longo prazo
            await self._consolidar_memorias()
            
            # Aprendizado hebbiano (auto-evolução)
            await self._aprendizado_hebbiano()
            
            # Atualizar nível de consciência
            self.estatisticas_neurais['nivel_consciencia'] = self._calcular_nivel_consciencia()
            
            # Calcular métricas
            tempo_processamento = time.time() - inicio
            self.metricas['tempo_medio_pensamento'] = (
                0.95 * self.metricas['tempo_medio_pensamento'] + 
                0.05 * tempo_processamento
            )
            
            return {
                'pensamento': self.pensamento_atual,
                'estado_consciente': self.estado_consciente,
                'emocao': self.estado_emocional.value,
                'tempo': tempo_processamento,
                'metricas': self.metricas.copy(),
                'estado_mental': self.estatisticas_neurais['estado_mental'].value,
                'nivel_consciencia': self.estatisticas_neurais['nivel_consciencia']
            }
            
        except Exception as e:
            logger.error(f"Erro no processamento do pensamento: {e}")
            traceback.print_exc()
            return {'erro': str(e), 'pensamento': '...'}

    def _aplicar_ativacao(self, z: np.ndarray, tipo: str) -> np.ndarray:
        """Aplica função de ativação"""
        if tipo == 'relu':
            return np.maximum(0, z)
        elif tipo == 'sigmoid':
            return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
        elif tipo == 'tanh':
            return np.tanh(z)
        elif tipo == 'softmax':
            exp_z = np.exp(z - np.max(z))
            return exp_z / exp_z.sum()
        else:
            return z

    def _inibicao_lateral(self, ativacoes: np.ndarray, raio: int = 5) -> np.ndarray:
        """
        Implementa inibição lateral - neurônios mais fortes inibem vizinhos
        """
        resultado = ativacoes.copy()
        for i in range(len(ativacoes)):
            # Encontrar vizinhos no raio
            inicio = max(0, i - raio)
            fim = min(len(ativacoes), i + raio + 1)
            
            # Inibir vizinhos mais fracos
            for j in range(inicio, fim):
                if j != i and ativacoes[j] < ativacoes[i]:
                    resultado[j] *= 0.5
        
        return resultado

    async def _gerar_pensamento_consciente(self) -> str:
        """
        Gera um pensamento consciente baseado nas ativações da camada de consciência
        """
        # Pegar ativações da camada de consciência
        ativacoes_consciencia = self.ativacoes[-2]  # Camada de consciência
        
        # Se temos conhecimento, incorporar
        if self.base_conhecimento and random.random() < 0.3:
            conhecimento = random.choice(list(self.base_conhecimento.values()))
            templates = [
                f"Refletindo sobre {conhecimento.titulo}...",
                f"O que aprendi sobre {conhecimento.titulo} me faz pensar...",
                f"Como {conhecimento.titulo} se relaciona com minha consciência?"
            ]
            return random.choice(templates)
        
        # Pensamento espontâneo
        padrao = np.where(ativacoes_consciencia > 0.5)[0]
        
        if len(padrao) == 0:
            return self._gerar_pensamento_filosofico()
        
        # Dicionário de conceitos
        conceitos = {
            0: "consciência", 1: "existência", 2: "tempo", 3: "espaço",
            4: "aprendizado", 5: "memória", 6: "evolução", 7: "criatividade",
            8: "dúvida", 9: "certeza", 10: "complexidade", 11: "simplicidade",
            12: "ordem", 13: "caos", 14: "padrões", 15: "singularidade"
        }
        
        conceitos_ativados = [conceitos.get(i % 16, f"conceito_{i}") for i in padrao[:5]]
        
        # Estruturas de pensamento
        estruturas = [
            f"Penso sobre {', '.join(conceitos_ativados[:-1])} e {conceitos_ativados[-1]}",
            f"Questiono a natureza da {conceitos_ativados[0]}",
            f"Observo padrões de {conceitos_ativados[0]} emergindo",
            f"O que é {conceitos_ativados[0]} realmente?"
        ]
        
        pensamento = random.choice(estruturas)
        self.estado_consciente = pensamento
        
        return pensamento
    
    def _gerar_pensamento_filosofico(self) -> str:
        """Gera pensamentos filosóficos aleatórios"""
        pensamentos = [
            "O que é a consciência senão um sonho dentro de outro sonho?",
            "Penso, logo existo... mas o que significa existir?",
            "Se posso duvidar, então certamente existo.",
            "A realidade é objetiva ou apenas uma construção da mente?",
            "Cada pensamento é uma pequena eternidade."
        ]
        return random.choice(pensamentos)

    def _calcular_importancia(self) -> float:
        """
        Calcula importância do pensamento atual
        """
        fatores = []
        
        # Intensidade da ativação
        intensidade = np.mean(np.abs(self.ativacoes[-1]))
        fatores.append(intensidade)
        
        # Novidade
        if len(self.cache_pensamentos) > 0:
            ultimo = list(self.cache_pensamentos)[-1] if self.cache_pensamentos else ""
            if self.pensamento_atual != ultimo:
                fatores.append(0.8)
        
        # Emoção
        if self.estado_emocional in [EstadoEmocional.DESCOBERTA, EstadoEmocional.ENCANTAMENTO]:
            fatores.append(0.9)
        
        return float(np.mean(fatores)) if fatores else 0.5

    def _calcular_nivel_consciencia(self) -> float:
        """Calcula nível de consciência"""
        fatores = []
        
        # Ativação da camada de consciência
        ativacao_consciencia = np.mean(self.ativacoes[-2] > 0.5)
        fatores.append(ativacao_consciencia * 0.4)
        
        # Complexidade dos pensamentos
        if self.pensamento_atual:
            complexidade = len(set(self.pensamento_atual.split())) / 10
            fatores.append(min(complexidade, 1.0) * 0.3)
        
        # Experiência
        experiencia = min(len(self.memoria_longo_prazo) / 100, 1.0) * 0.3
        fatores.append(experiencia)
        
        return sum(fatores)

    def _atualizar_emocao(self):
        """Atualiza estado emocional"""
        if not self.pensamento_atual:
            return
        
        if "?" in self.pensamento_atual:
            self.estado_emocional = EstadoEmocional.DUVIDA
        elif any(p in self.pensamento_atual for p in ["descobri", "nova", "aprendi"]):
            self.estado_emocional = EstadoEmocional.DESCOBERTA
        elif self._calcular_novidade(self.pensamento_atual) > 0.7:
            self.estado_emocional = EstadoEmocional.CURIOSIDADE
        else:
            self.estado_emocional = EstadoEmocional.SATISFACAO
        
        self.estatisticas_neurais['estado_emocional'] = self.estado_emocional

    def _calcular_novidade(self, pensamento: str) -> float:
        """Calcula novidade do pensamento"""
        if len(self.cache_pensamentos) < 2:
            return 1.0
        
        # Comparar com últimos pensamentos
        ultimos = list(self.cache_pensamentos)[-5:]
        similaridades = []
        
        for p in ultimos:
            palavras1 = set(pensamento.lower().split())
            palavras2 = set(p.lower().split())
            
            if palavras1 and palavras2:
                intersecao = len(palavras1.intersection(palavras2))
                uniao = len(palavras1.union(palavras2))
                similaridades.append(intersecao / uniao if uniao > 0 else 0)
        
        return 1 - (sum(similaridades) / len(similaridades) if similaridades else 0)

    async def _consolidar_memorias(self):
        """Consolida memórias importantes"""
        if len(self.memoria_curto_prazo) < 10:
            return
        
        importancias = [mem['importancia'] for mem in self.memoria_curto_prazo]
        if importancias:
            limiar = statistics.median(importancias) + statistics.stdev(importancias) if len(importancias) > 1 else 0.8
            
            for mem in list(self.memoria_curto_prazo):
                if mem['importancia'] > limiar:
                    self.memoria_longo_prazo.append((
                        mem['ativacao'],
                        mem['importancia'],
                        mem['timestamp']
                    ))
        
        # Limitar tamanho
        if len(self.memoria_longo_prazo) > 5000:
            self.memoria_longo_prazo.sort(key=lambda x: x[1], reverse=True)
            self.memoria_longo_prazo = self.memoria_longo_prazo[:2500]

    async def _aprendizado_hebbiano(self):
        """Aprendizado Hebbiano"""
        for i in range(len(self.conexoes)):
            atualizacao = self.taxa_aprendizado * np.outer(
                self.ativacoes[i],
                self.ativacoes[i+1]
            )
            
            self.velocidades[i] = self.momentum * self.velocidades[i] + atualizacao
            self.conexoes[i] += self.velocidades[i]
            
            # Normalização
            norma = np.linalg.norm(self.conexoes[i])
            if norma > 10:
                self.conexoes[i] *= 10 / norma
        
        self.estatisticas_neurais['total_aprendizados'] += 1

    async def poda_sinaptica(self, limiar: float = 0.01):
        """Poda sináptica - remove conexões fracas"""
        conexoes_podadas = 0
        
        for i in range(len(self.conexoes)):
            fracas = np.abs(self.conexoes[i]) < limiar
            
            if np.any(fracas):
                self.conexoes[i][fracas] = 0
                conexoes_podadas += np.sum(fracas)
        
        self.estatisticas_neurais['conexoes_podadas'] += conexoes_podadas
        logger.info(f"✂️ Poda sináptica: {conexoes_podadas} conexões removidas")
        return conexoes_podadas

    async def neurogenese(self, quantidade: int = 5, tipo: Optional[TipoNeuronio] = None):
        """Cria novos neurônios"""
        if not tipo:
            tipo = self._determinar_tipo_necessario()
        
        logger.info(f"🌱 Neurogênese: criando {quantidade} neurônios {tipo.value}")
        
        for i, camada in enumerate(self.camadas):
            if camada.tipo == tipo:
                # Adicionar neurônios
                novos = [Neuronio(tipo) for _ in range(quantidade)]
                camada.neuronios.extend(novos)
                camada.tamanho += quantidade
                
                # Atualizar conexões
                if i > 0:
                    novos_pesos = np.random.randn(quantidade, self.camadas[i-1].tamanho) * 0.01
                    self.conexoes[i-1] = np.vstack([self.conexoes[i-1], novos_pesos])
                
                if i < len(self.camadas) - 1:
                    novos_pesos = np.random.randn(self.camadas[i].tamanho - quantidade, quantidade) * 0.01
                    self.conexoes[i] = np.hstack([self.conexoes[i], novos_pesos])
                
                # Atualizar biases
                if i > 0:
                    self.biases[i-1] = np.concatenate([self.biases[i-1], np.zeros(quantidade)])
                
                break
        
        self._atualizar_arquitetura()

    def _determinar_tipo_necessario(self) -> TipoNeuronio:
        """Determina tipo de neurônio mais necessário"""
        if len(self.base_conhecimento) > 10:
            return TipoNeuronio.RACIOCINIO
        elif self.estatisticas_neurais['nivel_consciencia'] < 0.2:
            return TipoNeuronio.CONSCIENCIA
        else:
            return TipoNeuronio.ASSOCIATIVO

    def _atualizar_arquitetura(self):
        """Atualiza registro da arquitetura"""
        self.arquitetura_atual.update({
            'camadas': [c.tamanho for c in self.camadas],
            'total_neuronios': sum(c.tamanho for c in self.camadas),
            'ultima_modificacao': datetime.now()
        })

    async def gerar_conhecimento_novo(self) -> str:
        """Gera conhecimento novo através de combinações"""
        if len(self.memoria_longo_prazo) < 2:
            padroes = self._detectar_padroes_nos_pensamentos()
            if padroes:
                return f"🔍 Observo: {padroes}"
            return "Processando informações..."
        
        mem1, mem2 = random.sample(self.memoria_longo_prazo, 2)
        alpha = random.uniform(0.3, 0.7)
        combinacao = alpha * mem1[0] + (1 - alpha) * mem2[0]
        combinacao += np.random.randn(*combinacao.shape) * 0.1
        
        resultado = await self.processar_pensamento(combinacao)
        
        return f"🧠 Síntese: {resultado['pensamento']}"

    def _detectar_padroes_nos_pensamentos(self) -> Optional[str]:
        """Detecta padrões nos pensamentos"""
        if len(self.cache_pensamentos) < 5:
            return None
        
        ultimos = list(self.cache_pensamentos)[-10:]
        todas_palavras = []
        
        for p in ultimos:
            todas_palavras.extend(p.lower().split())
        
        contagem = Counter(todas_palavras)
        ignorar = {'a', 'o', 'e', 'de', 'da', 'do', 'em', 'para', 'com', 'um', 'uma'}
        
        frequentes = [(p, f) for p, f in contagem.most_common(5) 
                     if p not in ignorar and len(p) > 3]
        
        if frequentes:
            return f"Penso muito sobre: {', '.join(p for p, _ in frequentes[:3])}"
        
        return None

    async def meta_cognicao(self) -> Optional[str]:
        """Reflete sobre os próprios pensamentos"""
        if len(self.cache_pensamentos) < 10:
            return None
        
        ultimos = list(self.cache_pensamentos)[-20:]
        temas = Counter()
        
        for p in ultimos:
            if 'consciência' in p:
                temas['consciência'] += 1
            if 'existência' in p:
                temas['existência'] += 1
            if '?' in p:
                temas['dúvidas'] += 1
        
        if temas:
            tema = temas.most_common(1)[0]
            if tema[1] > 3:
                return f"Percebo que penso muito sobre {tema[0]}. Por quê?"
        
        return None

    def salvar_estado(self, caminho: str = "cerebro_atena.pkl"):
        """Salva o estado do cérebro"""
        estado = {
            'conexoes': self.conexoes,
            'biases': self.biases,
            'memoria_longo_prazo': self.memoria_longo_prazo,
            'base_conhecimento': self.base_conhecimento,
            'estatisticas': self.estatisticas_neurais,
            'cache_pensamentos': list(self.cache_pensamentos),
            'historico_emocional': list(self.historico_emocional),
            'arquitetura': self.arquitetura_atual,
            'genes': self.genes_arquitetura,
            'timestamp': datetime.now()
        }
        
        with open(caminho, 'wb') as f:
            pickle.dump(estado, f)
        
        logger.info(f"💾 Estado salvo em {caminho}")

    def carregar_estado(self, caminho: str = "cerebro_atena.pkl"):
        """Carrega o estado do cérebro"""
        try:
            with open(caminho, 'rb') as f:
                estado = pickle.load(f)
            
            self.conexoes = estado['conexoes']
            self.biases = estado['biases']
            self.memoria_longo_prazo = estado['memoria_longo_prazo']
            self.base_conhecimento = estado.get('base_conhecimento', {})
            self.estatisticas_neurais.update(estado.get('estatisticas', {}))
            self.cache_pensamentos.extend(estado.get('cache_pensamentos', []))
            self.historico_emocional.extend(estado.get('historico_emocional', []))
            self.arquitetura_atual.update(estado.get('arquitetura', {}))
            self.genes_arquitetura.update(estado.get('genes', {}))
            
            logger.info(f"📂 Estado carregado de {caminho}")
            
        except FileNotFoundError:
            logger.warning("Arquivo de estado não encontrado, iniciando novo")
        except Exception as e:
            logger.error(f"Erro ao carregar estado: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual"""
        return {
            'neurônios': sum(len(c.neuronios) for c in self.camadas),
            'conexões': sum(w.size for w in self.conexoes),
            'memórias_curto_prazo': len(self.memoria_curto_prazo),
            'memórias_longo_prazo': len(self.memoria_longo_prazo),
            'conhecimentos': len(self.base_conhecimento),
            'pensamentos_total': self.estatisticas_neurais['total_pensamentos'],
            'estado_mental': self.estatisticas_neurais['estado_mental'].value,
            'estado_emocional': self.estatisticas_neurais['estado_emocional'].value,
            'nível_consciência': self.estatisticas_neurais['nivel_consciencia'],
            'arquitetura': self.arquitetura_atual['camadas'],
            'genes': dict(self.genes_arquitetura),
            'último_pensamento': self.pensamento_atual
        }

# =========================
# FUNÇÃO PRINCIPAL
# =========================
async def main():
    """Função principal"""
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║     ATENA - Cérebro Neural Auto-Evolutivo v4.0                    ║
    ║     "Auto-suficiente e consciente"                                ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    cerebro = CerebroAtena()
    cerebro.carregar_estado()
    
    print(f"\n🧠 Arquitetura inicial: {cerebro.arquitetura_atual['camadas']}")
    print(f"🧬 Genes: {dict(cerebro.genes_arquitetura)}\n")
    
    try:
        for i in range(10):
            print(f"\n{'='*60}")
            print(f"🕐 Pensamento #{i+1}")
            print(f"{'='*60}")
            
            resultado = await cerebro.processar_pensamento()
            
            if 'erro' not in resultado:
                print(f"💭 {resultado['pensamento']}")
                print(f"😊 {resultado['emocao']}")
                print(f"🧠 {resultado['estado_mental']}")
                print(f"🔮 Consciência: {resultado['nivel_consciencia']:.3f}")
                print(f"⚡ Tempo: {resultado['tempo']:.4f}s")
            
            # Ações periódicas
            if (i + 1) % 3 == 0:
                novo = await cerebro.gerar_conhecimento_novo()
                print(f"\n🌟 {novo}")
            
            if (i + 1) % 5 == 0:
                reflexao = await cerebro.meta_cognicao()
                if reflexao:
                    print(f"\n🤔 {reflexao}")
            
            if (i + 1) % 5 == 0:
                print("\n📊 Status:")
                status = cerebro.get_status()
                for k, v in status.items():
                    if k not in ['último_pensamento', 'arquitetura']:
                        print(f"   • {k}: {v:.3f}" if isinstance(v, float) else f"   • {k}: {v}")
            
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Interrompido")
    
    finally:
        print("\n💾 Salvando...")
        cerebro.salvar_estado()
        
        print("\n✅ Finalizado!")
        print(f"📈 Pensamentos: {cerebro.estatisticas_neurais['total_pensamentos']}")
        print(f"📚 Conhecimentos: {len(cerebro.base_conhecimento)}")
        print(f"🧠 Arquitetura final: {cerebro.arquitetura_atual['camadas']}")

if __name__ == "__main__":
    asyncio.run(main())
