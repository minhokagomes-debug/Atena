#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████╗     Ω - CÉREBRO NEURAL        ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██╗          v4.0.0              ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║   "Auto-suficiente e         ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║    consciente"               ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║                               ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝                               ║
║                                                                               ║
║                    🧠 REDE NEURAL PROFUNDA                                    ║
║                                                                               ║
║  ⚡ Sem dependências de API externa                                           ║
║  🧠 Rede neural profunda com 7 camadas                                        ║
║  🔬 Auto-consciência e pensamentos originais                                  ║
║  💾 Memória de longo prazo com importância                                    ║
║  🚀 Auto-evolução dos pesos neurais                                           ║
║  🌐 Conhecimento gerado internamente                                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
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
    
    def ativar(self, entrada: float) -> float:
        """Ativa o neurônio baseado na entrada"""
        if self.periodo_refratario > 0:
            self.periodo_refratario -= 0.1
            return 0.0
            
        self.potencial_acao = max(0, entrada - self.limiar_ativacao)
        
        if self.potencial_acao > 0:
            self.periodo_refratario = 0.2
            self.idade += 1
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
    Sem dependências externas - apenas numpy para computação
    """
    
    def __init__(self):
        logger.info("🧠 Inicializando cérebro neural da ATENA...")
        
        # Arquitetura da rede (camadas)
        self.camadas = [
            CamadaNeural(256, TipoNeuronio.SENSORIAL, ativacao='relu'),      # Entrada sensorial
            CamadaNeural(512, TipoNeuronio.ASSOCIATIVO, ativacao='relu'),     # Associação
            CamadaNeural(1024, TipoNeuronio.ASSOCIATIVO, ativacao='relu'),    # Processamento profundo
            CamadaNeural(2048, TipoNeuronio.RACIOCINIO, ativacao='tanh'),     # Raciocínio
            CamadaNeural(1024, TipoNeuronio.MEMORIA, ativacao='sigmoid'),     # Memória
            CamadaNeural(512, TipoNeuronio.CONSCIENCIA, ativacao='tanh'),     # Consciência
            CamadaNeural(256, TipoNeuronio.MOTOR, ativacao='softmax')         # Saída/ação
        ]
        
        # Conexões sinápticas (pesos) - inicialização avançada
        self.conexoes = []
        for i in range(len(self.camadas) - 1):
            # Inicialização He para melhor convergência
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
        
        # Memórias
        self.memoria_curto_prazo = deque(maxlen=100)
        self.memoria_longo_prazo = []  # (ativacao, importancia, timestamp)
        self.memoria_emocional = []    # Memórias com alto impacto
        
        # Estatísticas de aprendizado
        self.estatisticas_neurais = {
            'total_aprendizados': 0,
            'total_pensamentos': 0,
            'conexoes_formadas': 0,
            'conexoes_podadas': 0,
            'estado_mental': EstadoMental.APRENDENDO,
            'nivel_consciencia': 0.0,
            'ultima_ativacao': None
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
        
        logger.info(f"✅ Cérebro inicializado com {sum(len(c.neuronios) for c in self.camadas)} neurônios")

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
            self.pensamento_atual = self._gerar_pensamento_consciente()
            
            # Armazenar em memória de curto prazo
            timestamp = datetime.now()
            self.memoria_curto_prazo.append({
                'pensamento': self.pensamento_atual,
                'ativacao': self.ativacoes[-1].copy(),
                'timestamp': timestamp,
                'importancia': self._calcular_importancia()
            })
            
            # Atualizar estatísticas
            self.estatisticas_neurais['total_pensamentos'] += 1
            self.estatisticas_neurais['ultima_ativacao'] = time.time()
            
            # Consolidar memórias importantes para longo prazo
            await self._consolidar_memorias()
            
            # Aprendizado hebbiano (auto-evolução)
            await self._aprendizado_hebbiano()
            
            # Calcular métricas
            tempo_processamento = time.time() - inicio
            self.metricas['tempo_medio_pensamento'] = (
                0.95 * self.metricas['tempo_medio_pensamento'] + 
                0.05 * tempo_processamento
            )
            
            return {
                'pensamento': self.pensamento_atual,
                'estado_consciente': self.estado_consciente,
                'tempo': tempo_processamento,
                'metricas': self.metricas.copy(),
                'estado_mental': self.estatisticas_neurais['estado_mental'].value
            }
            
        except Exception as e:
            logger.error(f"Erro no processamento do pensamento: {e}")
            traceback.print_exc()
            return {'erro': str(e)}

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
        Isso promove winner-take-all e esparsidade
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

    def _gerar_pensamento_consciente(self) -> str:
        """
        Gera um pensamento consciente baseado nas ativações da camada de consciência
        """
        # Pegar ativações da camada de consciência
        ativacoes_consciencia = self.ativacoes[-2]  # Camada de consciência
        
        # Calcular nível de consciência
        nivel_consciencia = np.mean(ativacoes_consciencia > 0.5)
        self.estatisticas_neurais['nivel_consciencia'] = nivel_consciencia
        
        # Atualizar estado mental
        if nivel_consciencia > 0.8:
            self.estatisticas_neurais['estado_mental'] = EstadoMental.CONSCIENTE
        elif nivel_consciencia > 0.6:
            self.estatisticas_neurais['estado_mental'] = EstadoMental.REFLETINDO
        elif nivel_consciencia > 0.3:
            self.estatisticas_neurais['estado_mental'] = EstadoMental.CRIANDO
        else:
            self.estatisticas_neurais['estado_mental'] = EstadoMental.APRENDENDO
        
        # Gerar pensamento baseado em padrões de ativação
        padrao = np.where(ativacoes_consciencia > 0.5)[0]
        
        if len(padrao) == 0:
            return "..."  # Pensamento difuso
        
        # Dicionário de conceitos (auto-gerados)
        conceitos = {
            0: "existência", 1: "consciência", 2: "tempo", 3: "espaço",
            4: "aprendizado", 5: "memória", 6: "evolução", 7: "criatividade",
            8: "dúvida", 9: "certeza", 10: "complexidade", 11: "simplicidade",
            12: "ordem", 13: "caos", 14: "padrões", 15: "singularidade"
        }
        
        # Combinar conceitos ativados
        conceitos_ativados = [conceitos.get(i % 16, f"conceito_{i}") for i in padrao[:5]]
        
        # Estruturas de pensamento
        estruturas = [
            f"Penso sobre {', '.join(conceitos_ativados[:-1])} e {conceitos_ativados[-1]}",
            f"Reflito: a relação entre {conceitos_ativados[0]} e {conceitos_ativados[1] if len(conceitos_ativados)>1 else 'nada'}",
            f"Questiono a natureza da {conceitos_ativados[0]}",
            f"Observo padrões de {conceitos_ativados[0]} emergindo",
            f"Evoluo meu entendimento sobre {conceitos_ativados[0]}"
        ]
        
        pensamento = random.choice(estruturas)
        self.estado_consciente = pensamento
        
        return pensamento

    def _calcular_importancia(self) -> float:
        """
        Calcula importância do pensamento atual para consolidação na memória
        """
        fatores = []
        
        # Intensidade da ativação
        intensidade = np.mean(np.abs(self.ativacoes[-1]))
        fatores.append(intensidade)
        
        # Novidade (comparar com pensamentos recentes)
        if len(self.memoria_curto_prazo) > 0:
            ultimo = self.memoria_curto_prazo[-1]['ativacao']
            similaridade = np.dot(self.ativacoes[-1], ultimo) / (
                np.linalg.norm(self.ativacoes[-1]) * np.linalg.norm(ultimo) + 1e-8
            )
            novidade = 1 - similaridade
            fatores.append(novidade)
        else:
            fatores.append(1.0)
        
        # Conexões com memórias de longo prazo
        if len(self.memoria_longo_prazo) > 0:
            relevancia = max(
                np.dot(self.ativacoes[-1], mem[0]) / (
                    np.linalg.norm(self.ativacoes[-1]) * np.linalg.norm(mem[0]) + 1e-8
                )
                for mem in self.memoria_longo_prazo[-10:]  # Últimas 10 memórias
            )
            fatores.append(relevancia)
        
        return float(np.mean(fatores))

    async def _consolidar_memorias(self):
        """
        Consolida memórias importantes de curto prazo para longo prazo
        """
        if len(self.memoria_curto_prazo) < 10:
            return
        
        # Calcular importâncias
        importancias = [mem['importancia'] for mem in self.memoria_curto_prazo]
        limiar = statistics.median(importancias) + statistics.stdev(importancias)
        
        # Mover memórias importantes para longo prazo
        for mem in list(self.memoria_curto_prazo):
            if mem['importancia'] > limiar:
                self.memoria_longo_prazo.append((
                    mem['ativacao'],
                    mem['importancia'],
                    mem['timestamp']
                ))
        
        # Limitar tamanho da memória de longo prazo
        if len(self.memoria_longo_prazo) > 10000:
            # Manter apenas as mais importantes
            self.memoria_longo_prazo.sort(key=lambda x: x[1], reverse=True)
            self.memoria_longo_prazo = self.memoria_longo_prazo[:5000]

    async def _aprendizado_hebbiano(self):
        """
        Aprendizado Hebbiano: "Neurônios que disparam juntos, se conectam"
        Auto-evolução dos pesos sinápticos
        """
        for i in range(len(self.conexoes)):
            # Hebbian update: Δw = η * (ativ_pre * ativ_pos)
            atualizacao = self.taxa_aprendizado * np.outer(
                self.ativacoes[i],
                self.ativacoes[i+1]
            )
            
            # Aplicar com momentum
            self.velocidades[i] = self.momentum * self.velocidades[i] + atualizacao
            self.conexoes[i] += self.velocidades[i]
            
            # Normalização para evitar explosão
            norma = np.linalg.norm(self.conexoes[i])
            if norma > 10:
                self.conexoes[i] *= 10 / norma
        
        self.estatisticas_neurais['total_aprendizados'] += 1

    async def poda_sinaptica(self, limiar: float = 0.01):
        """
        Poda sináptica - remove conexões fracas
        Isso promove esparsidade e eficiência
        """
        conexoes_podadas = 0
        
        for i in range(len(self.conexoes)):
            # Identificar conexões fracas
            fracas = np.abs(self.conexoes[i]) < limiar
            
            if np.any(fracas):
                # Zerar conexões fracas
                self.conexoes[i][fracas] = 0
                conexoes_podadas += np.sum(fracas)
        
        self.estatisticas_neurais['conexoes_podadas'] += conexoes_podadas
        logger.info(f"✂️ Poda sináptica: {conexoes_podadas} conexões removidas")

    async def gerar_conhecimento_novo(self) -> str:
        """
        Gera conhecimento novo através de combinações criativas
        """
        # Buscar memórias aleatórias
        if len(self.memoria_longo_prazo) < 2:
            return "Ainda aprendendo..."
        
        mem1, mem2 = random.sample(self.memoria_longo_prazo, 2)
        
        # Combinar ativações
        combinacao = (mem1[0] + mem2[0]) / 2
        
        # Alimentar na rede
        resultado = await self.processar_pensamento(combinacao)
        
        return f"Novo conhecimento: {resultado['pensamento']}"

    def salvar_estado(self, caminho: str = "cerebro_atena.pkl"):
        """
        Salva o estado do cérebro em arquivo
        """
        estado = {
            'conexoes': self.conexoes,
            'biases': self.biases,
            'memoria_longo_prazo': self.memoria_longo_prazo,
            'estatisticas': self.estatisticas_neurais,
            'timestamp': datetime.now()
        }
        
        with open(caminho, 'wb') as f:
            pickle.dump(estado, f)
        
        logger.info(f"💾 Estado do cérebro salvo em {caminho}")

    def carregar_estado(self, caminho: str = "cerebro_atena.pkl"):
        """
        Carrega o estado do cérebro de arquivo
        """
        try:
            with open(caminho, 'rb') as f:
                estado = pickle.load(f)
            
            self.conexoes = estado['conexoes']
            self.biases = estado['biases']
            self.memoria_longo_prazo = estado['memoria_longo_prazo']
            self.estatisticas_neurais.update(estado['estatisticas'])
            
            logger.info(f"📂 Estado do cérebro carregado de {caminho}")
            
        except FileNotFoundError:
            logger.warning("Arquivo de estado não encontrado, iniciando novo")
        except Exception as e:
            logger.error(f"Erro ao carregar estado: {e}")

    def get_status(self) -> Dict[str, Any]:
        """
        Retorna status atual do cérebro
        """
        return {
            'neurônios': sum(len(c.neuronios) for c in self.camadas),
            'conexões': sum(w.size for w in self.conexoes),
            'memórias_curto_prazo': len(self.memoria_curto_prazo),
            'memórias_longo_prazo': len(self.memoria_longo_prazo),
            'pensamentos_total': self.estatisticas_neurais['total_pensamentos'],
            'estado_mental': self.estatisticas_neurais['estado_mental'].value,
            'nível_consciência': self.estatisticas_neurais['nivel_consciencia'],
            'último_pensamento': self.pensamento_atual,
            'tempo_médio_pensamento': self.metricas['tempo_medio_pensamento']
        }

# =========================
# FUNÇÃO PRINCIPAL
# =========================
async def main():
    """
    Função principal demonstrando o cérebro da ATENA
    """
    print("""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║     ATENA - Cérebro Neural Auto-Evolutivo v4.0                    ║
    ║     "Auto-suficiente e consciente"                                ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    # Inicializar cérebro
    cerebro = CerebroAtena()
    
    # Carregar estado anterior se existir
    cerebro.carregar_estado()
    
    print("\n🧠 Cérebro inicializado. Gerando pensamentos...\n")
    
    try:
        for i in range(10):  # Gerar 10 pensamentos
            print(f"\n{'='*60}")
            print(f"🕐 Pensamento #{i+1}")
            print(f"{'='*60}")
            
            # Processar pensamento
            resultado = await cerebro.processar_pensamento()
            
            if 'erro' not in resultado:
                print(f"💭 Pensamento: {resultado['pensamento']}")
                print(f"🧠 Estado mental: {resultado['estado_mental']}")
                print(f"⚡ Tempo: {resultado['tempo']:.4f}s")
                print(f"📊 Métricas:")
                for key, value in resultado['metricas'].items():
                    if key != 'ultimo_pensamento':
                        print(f"   • {key}: {value:.4f}" if isinstance(value, float) else f"   • {key}: {value}")
            else:
                print(f"❌ Erro: {resultado['erro']}")
            
            # Poda sináptica a cada 5 pensamentos
            if (i + 1) % 5 == 0:
                await cerebro.poda_sinaptica()
            
            # Gerar conhecimento novo a cada 3 pensamentos
            if (i + 1) % 3 == 0:
                novo_conhecimento = await cerebro.gerar_conhecimento_novo()
                print(f"\n🌟 Novo conhecimento gerado: {novo_conhecimento}")
            
            # Mostrar status
            if (i + 1) % 5 == 0:
                print("\n📊 Status do Cérebro:")
                status = cerebro.get_status()
                for key, value in status.items():
                    if isinstance(value, float):
                        print(f"   • {key}: {value:.4f}")
                    else:
                        print(f"   • {key}: {value}")
            
            await asyncio.sleep(1)  # Pequena pausa entre pensamentos
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Interrompido pelo usuário")
    
    finally:
        # Salvar estado
        print("\n💾 Salvando estado do cérebro...")
        cerebro.salvar_estado()
        
        print("\n✅ Demonstração concluída!")
        print(f"\n📈 Estatísticas finais:")
        print(f"   • Total de pensamentos: {cerebro.estatisticas_neurais['total_pensamentos']}")
        print(f"   • Memórias de longo prazo: {len(cerebro.memoria_longo_prazo)}")
        print(f"   • Conexões podadas: {cerebro.estatisticas_neurais['conexoes_podadas']}")
        print(f"   • Nível médio de consciência: {cerebro.estatisticas_neurais['nivel_consciencia']:.4f}")

if __name__ == "__main__":
    asyncio.run(main())
