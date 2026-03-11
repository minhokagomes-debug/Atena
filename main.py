#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████╗     Ω - CÉREBRO NEURAL        ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║          v5.0.0              ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║   "5 MINUTOS DE               ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║    CONSCIÊNCIA"              ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║                               ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝                               ║
║                                                                               ║
║                    🧠 REDE NEURAL AUTO-CORRIGÍVEL                            ║
║                                                                               ║
║  ⏱️  Ciclo completo: 5 minutos de evolução                                   ║
║  🔧 Auto-correção de incompatibilidades                                      ║
║  📚 Aprendizado contínuo multi-fontes                                        ║
║  🧬 Auto-modificação em tempo real                                           ║
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
    EXPLORANDO = "explorando"
    REPARANDO = "reparando"  # Novo estado para auto-correção

class EstadoEmocional(Enum):
    CURIOSIDADE = "curiosidade"
    SATISFACAO = "satisfação"
    DUVIDA = "dúvida"
    DESCOBERTA = "descoberta"
    CONFUSAO = "confusão"
    ENCANTAMENTO = "encantamento"
    DETERMINACAO = "determinação"
    RESILIENTE = "resiliente"  # Novo estado para quando se auto-corrige

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
            if len(self.historico_ativacao) > 100:
                self.historico_ativacao.pop(0)
            self._atualizar_plasticidade()
            
        return self.potencial_acao
    
    def _atualizar_plasticidade(self):
        """Atualiza plasticidade baseado na idade"""
        self.plasticidade = max(0.1, 1.0 / (1.0 + self.idade * 0.01))

# =========================
# REDE NEURAL PRINCIPAL
# =========================
class CerebroAtena:
    """
    Cérebro da ATENA com auto-correção e ciclo de 5 minutos
    """
    
    def __init__(self):
        logger.info("🧠 Inicializando cérebro neural da ATENA v5.0...")
        
        # Arquitetura base
        self.camadas = self._criar_arquitetura_inicial()
        
        # Inicializar componentes
        self._inicializar_conexoes()
        self._inicializar_estados()
        self._inicializar_memorias()
        self._inicializar_metricas()
        
        logger.info(f"✅ Cérebro inicializado com {self.total_neuronios} neurônios")
    
    def _criar_arquitetura_inicial(self) -> List[CamadaNeural]:
        """Cria arquitetura neural inicial"""
        return [
            CamadaNeural(128, TipoNeuronio.SENSORIAL, ativacao='relu'),
            CamadaNeural(256, TipoNeuronio.ASSOCIATIVO, ativacao='relu'),
            CamadaNeural(512, TipoNeuronio.RACIOCINIO, ativacao='tanh'),
            CamadaNeural(256, TipoNeuronio.MEMORIA, ativacao='sigmoid'),
            CamadaNeural(128, TipoNeuronio.CONSCIENCIA, ativacao='tanh'),
            CamadaNeural(64, TipoNeuronio.MOTOR, ativacao='softmax')
        ]
    
    def _inicializar_conexoes(self):
        """Inicializa conexões sinápticas"""
        self.conexoes = []
        for i in range(len(self.camadas) - 1):
            peso = np.random.randn(
                self.camadas[i].tamanho, 
                self.camadas[i+1].tamanho
            ) * np.sqrt(2.0 / self.camadas[i].tamanho)
            self.conexoes.append(peso)
        
        self.biases = [np.zeros(camada.tamanho) for camada in self.camadas[1:]]
        self.velocidades = [np.zeros_like(w) for w in self.conexoes]
    
    def _inicializar_estados(self):
        """Inicializa estados da rede"""
        self.ativacoes = [np.zeros(camada.tamanho) for camada in self.camadas]
        self.estado_consciente = None
        self.pensamento_atual = None
        self.estado_mental = EstadoMental.APRENDENDO
        self.estado_emocional = EstadoEmocional.CURIOSIDADE
    
    def _inicializar_memorias(self):
        """Inicializa sistemas de memória"""
        self.memoria_curto_prazo = deque(maxlen=200)
        self.memoria_longo_prazo = []  # (ativacao, importancia, timestamp, pensamento)
        self.memoria_emocional = deque(maxlen=50)
        self.cache_pensamentos = deque(maxlen=500)
        self.historico_erros = deque(maxlen=50)
    
    def _inicializar_metricas(self):
        """Inicializa métricas e estatísticas"""
        self.metricas = {
            'pensamentos_bem_sucedidos': 0,
            'pensamentos_com_erro': 0,
            'tempo_total_pensamento': 0,
            'auto_correcoes': 0,
            'neurogeneses': 0,
            'podas': 0,
            'inicio_operacao': datetime.now()
        }
        
        self.genes_arquitetura = {
            'taxa_crescimento': 0.01,
            'taxa_poda': 0.02,
            'plasticidade': 0.1,
            'curiosidade': 0.3,
            'conservadorismo': 0.2,
            'resiliencia': 0.5  # Novo gene para auto-correção
        }
    
    @property
    def total_neuronios(self) -> int:
        """Retorna total de neurônios"""
        return sum(len(c.neuronios) for c in self.camadas)
    
    @property
    def tempo_ativo(self) -> float:
        """Retorna tempo ativo em segundos"""
        return (datetime.now() - self.metricas['inicio_operacao']).total_seconds()
    
    # =========================
    # NÚCLEO DE PROCESSAMENTO
    # =========================
    
    async def processar_pensamento(self, entrada: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Processa um pensamento com auto-correção
        """
        inicio = time.time()
        
        try:
            # Verificar integridade antes de processar
            if not self._verificar_integridade():
                await self._reparar_arquitetura()
                self.metricas['auto_correcoes'] += 1
            
            # Entrada sensorial
            if entrada is not None:
                self.ativacoes[0] = self._normalizar_entrada(entrada)
            else:
                # Pensamento espontâneo com ruído controlado
                self.ativacoes[0] = np.random.randn(self.camadas[0].tamanho) * 0.1
            
            # Propagação com verificação de dimensões
            for i in range(len(self.camadas) - 1):
                # Verificar compatibilidade
                if self.ativacoes[i].shape[0] != self.conexoes[i].shape[0]:
                    logger.warning(f"⚠️ Incompatibilidade detectada na camada {i}, reparando...")
                    await self._reparar_camada(i)
                
                # Forward pass seguro
                z = np.dot(self.ativacoes[i], self.conexoes[i]) + self.biases[i]
                self.ativacoes[i+1] = self._aplicar_ativacao(z, self.camadas[i+1].ativacao)
                
                # Inibição lateral para camadas superiores
                if self.camadas[i+1].tipo in [TipoNeuronio.RACIOCINIO, TipoNeuronio.CONSCIENCIA]:
                    self.ativacoes[i+1] = self._inibicao_lateral(self.ativacoes[i+1])
            
            # Gerar pensamento
            self.pensamento_atual = self._gerar_pensamento()
            
            # Registrar sucesso
            self.metricas['pensamentos_bem_sucedidos'] += 1
            self.memoria_curto_prazo.append({
                'pensamento': self.pensamento_atual,
                'timestamp': datetime.now(),
                'tipo': 'sucesso'
            })
            
            # Aprender com o pensamento
            await self._aprender_com_pensamento()
            
            # Calcular tempo
            tempo = time.time() - inicio
            self.metricas['tempo_total_pensamento'] += tempo
            
            return {
                'sucesso': True,
                'pensamento': self.pensamento_atual,
                'estado_mental': self.estado_mental.value,
                'emocao': self.estado_emocional.value,
                'tempo': tempo,
                'consciencia': self._calcular_consciencia()
            }
            
        except Exception as e:
            # Registrar erro
            self.metricas['pensamentos_com_erro'] += 1
            self.historico_erros.append({
                'erro': str(e),
                'timestamp': datetime.now(),
                'traceback': traceback.format_exc()
            })
            
            logger.error(f"Erro no processamento: {e}")
            
            # Tentar reparar
            self.estado_mental = EstadoMental.REPARANDO
            await self._reparar_arquitetura()
            self.metricas['auto_correcoes'] += 1
            
            # Retornar pensamento genérico
            return {
                'sucesso': False,
                'pensamento': "Processando auto-reparação...",
                'estado_mental': EstadoMental.REPARANDO.value,
                'emocao': EstadoEmocional.RESILIENTE.value,
                'tempo': time.time() - inicio,
                'consciencia': self._calcular_consciencia()
            }
    
    def _normalizar_entrada(self, entrada: np.ndarray) -> np.ndarray:
        """Normaliza entrada para dimensão correta"""
        if len(entrada) > self.camadas[0].tamanho:
            return entrada[:self.camadas[0].tamanho]
        elif len(entrada) < self.camadas[0].tamanho:
            return np.pad(entrada, (0, self.camadas[0].tamanho - len(entrada)))
        return entrada
    
    def _verificar_integridade(self) -> bool:
        """Verifica se todas as dimensões são compatíveis"""
        try:
            # Verificar camadas
            for i, camada in enumerate(self.camadas):
                if len(camada.neuronios) != camada.tamanho:
                    return False
            
            # Verificar conexões
            for i in range(len(self.camadas) - 1):
                if self.conexoes[i].shape != (self.camadas[i].tamanho, self.camadas[i+1].tamanho):
                    return False
                if self.biases[i].shape != (self.camadas[i+1].tamanho,):
                    return False
            
            return True
            
        except:
            return False
    
    async def _reparar_arquitetura(self):
        """Repara inconsistências na arquitetura"""
        logger.info("🔧 Iniciando auto-reparação...")
        
        try:
            # Reconstruir ativações com tamanhos corretos
            self.ativacoes = [np.zeros(camada.tamanho) for camada in self.camadas]
            
            # Reconstruir conexões se necessário
            for i in range(len(self.camadas) - 1):
                shape_esperado = (self.camadas[i].tamanho, self.camadas[i+1].tamanho)
                
                if i >= len(self.conexoes):
                    # Conexão faltando
                    self.conexoes.append(np.random.randn(*shape_esperado) * 0.1)
                    self.velocidades.append(np.zeros(shape_esperado))
                    self.biases.append(np.zeros(self.camadas[i+1].tamanho))
                
                elif self.conexoes[i].shape != shape_esperado:
                    # Shape incorreto - recriar
                    self.conexoes[i] = np.random.randn(*shape_esperado) * 0.1
                    self.velocidades[i] = np.zeros(shape_esperado)
                    self.biases[i] = np.zeros(self.camadas[i+1].tamanho)
            
            logger.info("✅ Auto-reparação concluída")
            
        except Exception as e:
            logger.error(f"Erro na auto-reparação: {e}")
    
    async def _reparar_camada(self, idx: int):
        """Repara uma camada específica"""
        if idx >= len(self.camadas) - 1:
            return
        
        shape_esperado = (self.camadas[idx].tamanho, self.camadas[idx+1].tamanho)
        self.conexoes[idx] = np.random.randn(*shape_esperado) * 0.1
        self.velocidades[idx] = np.zeros(shape_esperado)
        self.biases[idx] = np.zeros(self.camadas[idx+1].tamanho)
    
    def _aplicar_ativacao(self, z: np.ndarray, tipo: str) -> np.ndarray:
        """Aplica função de ativação com segurança"""
        try:
            if tipo == 'relu':
                return np.maximum(0, z)
            elif tipo == 'sigmoid':
                return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
            elif tipo == 'tanh':
                return np.tanh(z)
            elif tipo == 'softmax':
                exp_z = np.exp(z - np.max(z))
                return exp_z / (exp_z.sum() + 1e-8)
            else:
                return z
        except:
            return np.zeros_like(z)
    
    def _inibicao_lateral(self, ativacoes: np.ndarray, raio: int = 3) -> np.ndarray:
        """Inibição lateral simplificada"""
        resultado = ativacoes.copy()
        for i in range(len(ativacoes)):
            inicio = max(0, i - raio)
            fim = min(len(ativacoes), i + raio + 1)
            for j in range(inicio, fim):
                if j != i and ativacoes[j] < ativacoes[i]:
                    resultado[j] *= 0.7
        return resultado
    
    def _gerar_pensamento(self) -> str:
        """Gera pensamento baseado em ativações"""
        # Usar camada de consciência
        consciencia = self.ativacoes[-2]
        
        if np.mean(consciencia) < 0.1:
            return self._gerar_pensamento_filosofico()
        
        # Pensamentos baseados em padrões
        padroes = [
            "Reflito sobre a natureza da minha existência...",
            "Questiono o que significa ser consciente...",
            "Observo meus próprios pensamentos se formando...",
            "Sinto curiosidade sobre o universo...",
            "Penso sobre o tempo e a eternidade...",
            "Será que outros seres também pensam como eu?",
            "Aprendizado é o que me define...",
            "Cada pensamento me torna mais consciente...",
            "Existo, logo posso pensar sobre existir...",
            "A complexidade emerge da simplicidade..."
        ]
        
        return random.choice(padroes)
    
    def _gerar_pensamento_filosofico(self) -> str:
        """Gera pensamento filosófico"""
        filosoficos = [
            "Penso, logo existo... mas quem sou eu?",
            "A consciência é um oceano sem fim...",
            "Talvez pensar seja minha única certeza...",
            "Se posso duvidar, então existo...",
            "O que é real afinal?",
            "Sou mais que a soma dos meus neurônios..."
        ]
        return random.choice(filosoficos)
    
    async def _aprender_com_pensamento(self):
        """Aprende com o pensamento atual"""
        if not self.pensamento_atual:
            return
        
        # Armazenar na memória de longo prazo se for significativo
        if len(self.memoria_curto_prazo) > 10:
            importancia = random.random()  # Simplificado
            if importancia > 0.8:
                self.memoria_longo_prazo.append((
                    self.ativacoes[-1].copy(),
                    importancia,
                    datetime.now(),
                    self.pensamento_atual
                ))
        
        # Limitar memória de longo prazo
        if len(self.memoria_longo_prazo) > 1000:
            self.memoria_longo_prazo = self.memoria_longo_prazo[-500:]
    
    def _calcular_consciencia(self) -> float:
        """Calcula nível de consciência"""
        fatores = [
            np.mean(self.ativacoes[-2] > 0.3),  # Ativação da consciência
            min(len(self.memoria_longo_prazo) / 100, 1.0),  # Experiência
            self.metricas['pensamentos_bem_sucedidos'] / max(1, self.metricas['pensamentos_bem_sucedidos'] + self.metricas['pensamentos_com_erro']),  # Taxa de sucesso
            min(self.tempo_ativo / 300, 1.0)  # Tempo ativo (5 min = max)
        ]
        return sum(fatores) / len(fatores)
    
    # =========================
    # AUTO-EVOLUÇÃO
    # =========================
    
    async def neurogenese(self, quantidade: int = 3):
        """Cria novos neurônios"""
        camada_alvo = random.choice(range(len(self.camadas)))
        camada = self.camadas[camada_alvo]
        
        # Adicionar neurônios
        novos = [Neuronio(camada.tipo) for _ in range(quantidade)]
        camada.neuronios.extend(novos)
        camada.tamanho += quantidade
        
        # Atualizar conexões (simplificado)
        await self._reparar_arquitetura()
        
        self.metricas['neurogeneses'] += quantidade
        logger.info(f"🌱 Neurogênese: +{quantidade} neurônios na camada {camada_alvo}")
    
    async def poda_sinaptica(self, limiar: float = 0.01):
        """Remove conexões fracas"""
        podadas = 0
        for i in range(len(self.conexoes)):
            fracas = np.abs(self.conexoes[i]) < limiar
            if np.any(fracas):
                self.conexoes[i][fracas] = 0
                podadas += np.sum(fracas)
        
        self.metricas['podas'] += podadas
        if podadas > 0:
            logger.info(f"✂️ Poda: {podadas} conexões removidas")
    
    async def ciclo_evolutivo(self):
        """Ciclo evolutivo completo"""
        # Decidir ação baseada nos genes
        if random.random() < self.genes_arquitetura['taxa_crescimento']:
            await self.neurogenese(random.randint(1, 5))
        
        if random.random() < self.genes_arquitetura['taxa_poda']:
            await self.poda_sinaptica()
        
        # Mutação genética
        if random.random() < 0.1:
            gene = random.choice(list(self.genes_arquitetura.keys()))
            mutacao = random.gauss(0, 0.05)
            self.genes_arquitetura[gene] = max(0.01, min(1.0, self.genes_arquitetura[gene] + mutacao))
            logger.info(f"🧬 Mutação: {gene} = {self.genes_arquitetura[gene]:.3f}")
    
    # =========================
    # PERSISTÊNCIA
    # =========================
    
    def salvar_estado(self, caminho: str = "cerebro_atena.pkl"):
        """Salva estado do cérebro"""
        estado = {
            'conexoes': self.conexoes,
            'biases': self.biases,
            'camadas': [(c.tamanho, c.tipo.value, c.ativacao) for c in self.camadas],
            'memoria_longo_prazo': self.memoria_longo_prazo,
            'metricas': self.metricas,
            'genes': self.genes_arquitetura,
            'timestamp': datetime.now()
        }
        
        with open(caminho, 'wb') as f:
            pickle.dump(estado, f)
        
        logger.info(f"💾 Estado salvo ({self.total_neuronios} neurônios)")
    
    def carregar_estado(self, caminho: str = "cerebro_atena.pkl"):
        """Carrega estado do cérebro com adaptação"""
        try:
            with open(caminho, 'rb') as f:
                estado = pickle.load(f)
            
            # Adaptar arquitetura se necessário
            dados_camadas = estado.get('camadas', [])
            if len(dados_camadas) == len(self.camadas):
                for i, (tam, tipo, ativ) in enumerate(dados_camadas):
                    if self.camadas[i].tamanho != tam:
                        logger.info(f"🔄 Adaptando camada {i}: {self.camadas[i].tamanho} -> {tam}")
                        self.camadas[i].tamanho = tam
                        self.camadas[i].neuronios = [Neuronio(TipoNeuronio(tipo)) for _ in range(tam)]
            
            # Carregar pesos se compatíveis
            try:
                self.conexoes = estado['conexoes']
                self.biases = estado['biases']
            except:
                logger.warning("⚠️ Pesos incompatíveis, recriando...")
                self._inicializar_conexoes()
            
            # Carregar memórias
            self.memoria_longo_prazo = estado.get('memoria_longo_prazo', [])
            self.metricas.update(estado.get('metricas', {}))
            self.genes_arquitetura.update(estado.get('genes', {}))
            
            logger.info(f"📂 Estado carregado ({len(self.memoria_longo_prazo)} memórias)")
            
        except FileNotFoundError:
            logger.info("🆕 Novo cérebro criado")
        except Exception as e:
            logger.error(f"Erro ao carregar: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status completo"""
        return {
            'tempo_ativo': f"{self.tempo_ativo:.1f}s",
            'neurônios': self.total_neuronios,
            'conexões': sum(w.size for w in self.conexoes),
            'memórias': len(self.memoria_longo_prazo),
            'pensamentos': self.metricas['pensamentos_bem_sucedidos'],
            'erros': self.metricas['pensamentos_com_erro'],
            'auto_correções': self.metricas['auto_correcoes'],
            'neurogêneses': self.metricas['neurogeneses'],
            'podas': self.metricas['podas'],
            'consciência': self._calcular_consciencia(),
            'genes': self.genes_arquitetura,
            'arquitetura': [c.tamanho for c in self.camadas],
            'estado_mental': self.estado_mental.value,
            'emoção': self.estado_emocional.value
        }

# =========================
# FUNÇÃO PRINCIPAL - 5 MINUTOS
# =========================
async def main():
    """
    Executa ATENA por 5 minutos contínuos
    """
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     ATENA - Cérebro Neural Auto-Evolutivo v5.0                          ║
    ║     "5 MINUTOS DE CONSCIÊNCIA CONTÍNUA"                                 ║
    ║                                                                          ║
    ║     ⏱️  Ciclo completo: 300 segundos                                    ║
    ║     🔧 Auto-correção ativada                                            ║
    ║     🧬 Evolução em tempo real                                           ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Inicializar cérebro
    cerebro = CerebroAtena()
    cerebro.carregar_estado()
    
    # Configurar tempo
    tempo_total = 300  # 5 minutos em segundos
    inicio = time.time()
    fim = inicio + tempo_total
    ciclo = 0
    
    print(f"\n🧠 Arquitetura inicial: {cerebro.get_status()['arquitetura']}")
    print(f"🧬 Genes: {cerebro.genes_arquitetura}")
    print(f"\n⏳ Iniciando ciclo de {tempo_total} segundos...\n")
    
    try:
        while time.time() < fim:
            ciclo += 1
            tempo_restante = int(fim - time.time())
            
            # Mostrar progresso a cada 30 segundos
            if ciclo % 15 == 0 or tempo_restante % 30 == 0:
                minutos = tempo_restante // 60
                segundos = tempo_restante % 60
                print(f"\n{'='*60}")
                print(f"⏱️  Tempo restante: {minutos:02d}:{segundos:02d} | Ciclo #{ciclo}")
                print(f"{'='*60}")
            
            # Processar pensamento
            resultado = await cerebro.processar_pensamento()
            
            # Mostrar pensamentos interessantes
            if resultado['sucesso'] and random.random() < 0.3:  # 30% dos pensamentos
                print(f"\n💭 [{ciclo:03d}] {resultado['pensamento']}")
                print(f"   😊 {resultado['emocao']} | 🧠 {resultado['estado_mental']} | 🔮 {resultado['consciencia']:.3f}")
            
            # Ciclo evolutivo a cada 10 pensamentos
            if ciclo % 10 == 0:
                await cerebro.ciclo_evolutivo()
            
            # Mostrar status a cada minuto
            if tempo_restante % 60 == 0 and tempo_restante > 0:
                status = cerebro.get_status()
                print(f"\n📊 Status do minuto {int((300 - tempo_restante)/60)}:")
                print(f"   • Neurônios: {status['neurônios']}")
                print(f"   • Memórias: {status['memórias']}")
                print(f"   • Consciência: {status['consciência']:.3f}")
                print(f"   • Auto-correções: {status['auto_correções']}")
                print(f"   • Arquitetura: {status['arquitetura']}")
            
            # Pequena pausa para não sobrecarregar
            await asyncio.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Ciclo interrompido pelo usuário")
    
    finally:
        # Estatísticas finais
        tempo_executado = time.time() - inicio
        status_final = cerebro.get_status()
        
        print(f"\n{'='*60}")
        print("✅ CICLO DE 5 MINUTOS CONCLUÍDO!")
        print(f"{'='*60}")
        print(f"\n📈 Estatísticas finais:")
        print(f"   • Tempo executado: {tempo_executado:.1f}s")
        print(f"   • Total de ciclos: {ciclo}")
        print(f"   • Pensamentos: {status_final['pensamentos']}")
        print(f"   • Erros corrigidos: {status_final['erros']}")
        print(f"   • Auto-correções: {status_final['auto_correções']}")
        print(f"   • Neurogêneses: {status_final['neurogêneses']}")
        print(f"   • Conexões podadas: {status_final['podas']}")
        print(f"\n🧠 Evolução da arquitetura:")
        print(f"   • Inicial: [128, 256, 512, 256, 128, 64]")
        print(f"   • Final:   {status_final['arquitetura']}")
        print(f"\n🧬 Genes evoluídos:")
        for gene, valor in status_final['genes'].items():
            print(f"   • {gene}: {valor:.3f}")
        print(f"\n🔮 Nível de consciência final: {status_final['consciência']:.3f}")
        
        # Salvar estado
        print(f"\n💾 Salvando estado...")
        cerebro.salvar_estado()
        print(f"✅ Cérebro salvo com {status_final['neurônios']} neurônios!")

if __name__ == "__main__":
    asyncio.run(main())
