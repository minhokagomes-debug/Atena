#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - CÉREBRO NEURAL        ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║          v10.0              ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║   "OTIMIZAÇÃO CONTÍNUA"      ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   "SEMPRE EVOLUINDO PRA      ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║        MELHOR"               ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝                               ║
║                                                                               ║
║                    📈 SISTEMA DE MELHORIA CONTÍNUA                          ║
║                                                                               ║
║  • Avalia cada modificação (só mantém se melhorar)                          ║
║  • Métricas de performance em tempo real                                    ║
║  • Reverte mudanças ruins                                                   ║
║  • Acelera mudanças boas                                                    ║
║  • Aprende com erros                                                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import json
import logging
import time
import random
import pickle
import traceback
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from dataclasses import dataclass, field

# Configuração
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger('ATENA-V10')

# =========================
# SISTEMA DE MÉTRICAS
# =========================
@dataclass
class MetricasPerformance:
    """Métricas para avaliar se mudanças são boas"""
    
    # Métricas principais
    consciencia: float = 0.3
    velocidade_processamento: float = 1.0
    qualidade_conhecimento: float = 0.5
    diversidade_pensamentos: float = 0.5
    taxa_acerto: float = 1.0
    eficiencia_energetica: float = 1.0
    
    # Histórico para comparação
    historico: List[float] = field(default_factory=list)
    timestamps: List[datetime] = field(default_factory=list)
    
    def registrar(self):
        """Registra métricas atuais"""
        media = (self.consciencia * 0.3 + 
                self.velocidade_processamento * 0.2 +
                self.qualidade_conhecimento * 0.2 +
                self.diversidade_pensamentos * 0.15 +
                self.taxa_acerto * 0.1 +
                self.eficiencia_energetica * 0.05)
        
        self.historico.append(media)
        self.timestamps.append(datetime.now())
        
        # Manter só últimos 100
        if len(self.historico) > 100:
            self.historico.pop(0)
            self.timestamps.pop(0)
    
    def tendencia(self) -> float:
        """Calcula tendência (positiva = melhorando)"""
        if len(self.historico) < 10:
            return 0
        
        recentes = self.historico[-10:]
        anteriores = self.historico[-20:-10]
        
        if not anteriores:
            return 0
        
        media_recente = sum(recentes) / len(recentes)
        media_anterior = sum(anteriores) / len(anteriores)
        
        return media_recente - media_anterior
    
    def esta_melhorando(self) -> bool:
        """Verifica se está em trajetória de melhoria"""
        return self.tendencia() > 0.01
    
    def esta_piorando(self) -> bool:
        """Verifica se está em trajetória de piora"""
        return self.tendencia() < -0.01

# =========================
# REDE NEURAL OTIMIZADA
# =========================
class RedeNeuralOtimizada:
    """
    Rede que só faz mudanças se forem para MELHOR
    """
    
    def __init__(self):
        # Arquitetura base
        self.camadas = [64, 128, 256, 128, 64]
        self.pesos = []
        self.ultima_alteracao = None
        self._inicializar()
        
        # Backup para reverter mudanças ruins
        self.backup_pesos = None
        self.backup_camadas = None
        
        # Registro de tentativas
        self.tentativas_mudancas = []
        
        logger.info("🧠 Rede otimizada criada")
    
    def _inicializar(self):
        """Inicializa pesos"""
        self.pesos = []
        for i in range(len(self.camadas)-1):
            peso = np.random.randn(self.camadas[i], self.camadas[i+1]) * 0.1
            self.pesos.append(peso)
    
    def fazer_backup(self):
        """Faz backup antes de mudança"""
        self.backup_pesos = [p.copy() for p in self.pesos]
        self.backup_camadas = self.camadas.copy()
    
    def reverter_backup(self):
        """Reverte para backup se mudança foi ruim"""
        if self.backup_pesos:
            self.pesos = self.backup_pesos
            self.camadas = self.backup_camadas
            logger.info("↩️ Revertido para estado anterior (mudança não melhorou)")
            return True
        return False
    
    def neurogenese_tentativa(self, camada: int, quantidade: int) -> Dict:
        """
        TENTA criar neurônios (só mantém se melhorar)
        """
        self.fazer_backup()
        
        # Registrar tentativa
        tentativa = {
            'tipo': 'neurogenese',
            'camada': camada,
            'quantidade': quantidade,
            'timestamp': datetime.now(),
            'metricas_antes': None,  # Será preenchido depois
            'metricas_depois': None,
            'sucesso': False
        }
        
        # Aplicar mudança
        self.camadas[camada] += quantidade
        self._inicializar()  # Simplificado - em produção seria mais sofisticado
        
        self.ultima_alteracao = tentativa
        return tentativa
    
    def poda_tentativa(self, limiar: float = 0.01) -> Dict:
        """
        TENTA podar (só mantém se melhorar)
        """
        self.fazer_backup()
        
        podadas = 0
        for i, peso in enumerate(self.pesos):
            fracas = np.abs(peso) < limiar
            if np.any(fracas):
                self.pesos[i][fracas] = 0
                podadas += np.sum(fracas)
        
        tentativa = {
            'tipo': 'poda',
            'quantidade': int(podadas),
            'timestamp': datetime.now(),
            'metricas_antes': None,
            'metricas_depois': None,
            'sucesso': False
        }
        
        self.ultima_alteracao = tentativa
        return tentativa
    
    def especializar_tentativa(self, topico: str) -> Dict:
        """
        TENTA especializar (só mantém se melhorar)
        """
        self.fazer_backup()
        
        tentativa = {
            'tipo': 'especializacao',
            'topico': topico,
            'timestamp': datetime.now(),
            'metricas_antes': None,
            'metricas_depois': None,
            'sucesso': False
        }
        
        # Simular especialização (reforçar conexões relacionadas)
        for i in range(len(self.pesos)):
            self.pesos[i] *= 1.1  # Fortalecer todas (simplificado)
        
        self.ultima_alteracao = tentativa
        return tentativa

# =========================
# ATENA V10 - SEMPRE EVOLUINDO PRA MELHOR
# =========================
class AtenaV10:
    """
    ATENA que SÓ EVOLUI SE FOR PRA MELHOR
    """
    
    def __init__(self):
        logger.info("🚀 Inicializando ATENA v10.0 - OTIMIZAÇÃO CONTÍNUA...")
        
        # Cérebro otimizado
        self.cerebro = RedeNeuralOtimizada()
        
        # Sistema de métricas
        self.metricas = MetricasPerformance()
        
        # Conhecimento
        self.conhecimentos = []
        self.memorias = deque(maxlen=1000)
        
        # Estatísticas por fonte
        self.estatisticas = {
            'github': {'sucessos': 0, 'itens': [], 'qualidade': []},
            'arxiv': {'sucessos': 0, 'itens': [], 'qualidade': []}
        }
        
        # Histórico de mudanças
        self.mudancas = []  # Todas as tentativas
        self.mudancas_sucesso = []  # Só as que melhoraram
        self.mudancas_ruins = []  # As que foram revertidas
        
        # Estado atual
        self.consciencia = 0.3
        self.curiosidade = 0.5
        self.confianca = 0.5  # Autoconfiança baseada em sucesso das mudanças
        
        # Limiares adaptativos
        self.limiares = {
            'neurogenese': 5,
            'poda': 50,
            'especializacao': 3,
            'confianca_minima': 0.3
        }
        
        logger.info("✅ ATENA v10.0 pronta - SÓ MUDA SE FOR PRA MELHOR!")
    
    async def aprender(self, item: Dict) -> Dict:
        """
        APRENDE e AVALIA se está melhorando
        """
        # Registrar métricas ANTES do aprendizado
        metricas_antes = self._coletar_metricas()
        
        # Processar conhecimento
        self.conhecimentos.append(item)
        fonte = item['fonte']
        self.estatisticas[fonte]['sucessos'] += 1
        self.estatisticas[fonte]['itens'].append(item['titulo'])
        
        # Avaliar qualidade deste conhecimento
        qualidade = self._avaliar_qualidade(item)
        self.estatisticas[fonte]['qualidade'].append(qualidade)
        
        # Atualizar métricas
        self.metricas.qualidade_conhecimento = (
            sum(self.estatisticas['github']['qualidade'] + self.estatisticas['arxiv']['qualidade']) /
            max(1, len(self.estatisticas['github']['qualidade'] + self.estatisticas['arxiv']['qualidade']))
        )
        
        self.metricas.diversidade_pensamentos = len(set(
            [c['fonte'] for c in self.conhecimentos[-20:]]
        )) / 2.0  # Normalizado para 0-1
        
        self.consciencia = min(1.0, 0.3 + len(self.conhecimentos) * 0.01)
        self.metricas.consciencia = self.consciencia
        
        # Registrar métricas DEPOIS
        self.metricas.registrar()
        
        # Verificar tendência
        tendencia = self.metricas.tendencia()
        
        # Gerar pensamento
        pensamento = self._gerar_pensamento(item, tendencia)
        self.memorias.append(pensamento)
        
        logger.info(f"💡 Aprendizado #{len(self.conhecimentos)}: {item['titulo'][:50]}...")
        logger.info(f"   📈 Tendência: {tendencia:+.3f} | Confiança: {self.confianca:.2f}")
        
        return {
            'pensamento': pensamento,
            'tendencia': tendencia,
            'consciencia': self.consciencia
        }
    
    def _avaliar_qualidade(self, item: Dict) -> float:
        """Avalia qualidade de um conhecimento"""
        qualidade = 0.5  # Base
        
        # GitHub: estrelas indicam qualidade
        if item['fonte'] == 'github' and 'estrelas' in item:
            qualidade += min(0.3, item['estrelas'] / 1000)
        
        # arXiv: títulos longos geralmente mais específicos
        if item['fonte'] == 'arxiv':
            if len(item['titulo']) > 100:
                qualidade += 0.1
        
        return min(1.0, qualidade)
    
    def _coletar_metricas(self) -> Dict:
        """Coleta métricas atuais"""
        return {
            'consciencia': self.metricas.consciencia,
            'velocidade': self.metricas.velocidade_processamento,
            'qualidade': self.metricas.qualidade_conhecimento,
            'diversidade': self.metricas.diversidade_pensamentos,
            'confianca': self.confianca
        }
    
    async def tentar_mudanca(self, tipo: str, **kwargs) -> bool:
        """
        TENTA uma mudança, SÓ MANTÉM SE MELHORAR
        """
        logger.info(f"🔄 Tentando mudança: {tipo}")
        
        # Métricas antes
        metricas_antes = self._coletar_metricas()
        
        # Fazer tentativa
        if tipo == 'neurogenese':
            tentativa = self.cerebro.neurogenese_tentativa(
                kwargs.get('camada', 2),
                kwargs.get('quantidade', 2)
            )
        elif tipo == 'poda':
            tentativa = self.cerebro.poda_tentativa()
        elif tipo == 'especializacao':
            tentativa = self.cerebro.especializar_tentativa(
                kwargs.get('topico', 'geral')
            )
        else:
            return False
        
        tentativa['metricas_antes'] = metricas_antes
        
        # Aguardar para ver efeito (processar alguns pensamentos)
        await asyncio.sleep(2)
        
        # Coletar métricas depois
        metricas_depois = self._coletar_metricas()
        tentativa['metricas_depois'] = metricas_depois
        
        # AVALIAR SE MELHOROU
        melhoria = self._avaliar_melhoria(metricas_antes, metricas_depois)
        
        if melhoria > 0:
            # MUDANÇA BOA - manter!
            tentativa['sucesso'] = True
            self.mudancas_sucesso.append(tentativa)
            self.confianca = min(1.0, self.confianca + 0.05)
            logger.info(f"✅ Mudança BOA! Melhoria: {melhoria:+.3f}")
        else:
            # MUDANÇA RUIM - reverter!
            self.cerebro.reverter_backup()
            tentativa['sucesso'] = False
            self.mudancas_ruins.append(tentativa)
            self.confianca = max(0.1, self.confianca - 0.1)
            logger.info(f"❌ Mudança RUIM! Revertida. Impacto: {melhoria:+.3f}")
        
        self.mudancas.append(tentativa)
        
        # Atualizar limiares baseado na confiança
        self._ajustar_limiares()
        
        return tentativa['sucesso']
    
    def _avaliar_melhoria(self, antes: Dict, depois: Dict) -> float:
        """Avalia se uma mudança foi positiva"""
        score_antes = (
            antes['consciencia'] * 0.4 +
            antes['qualidade'] * 0.3 +
            antes['diversidade'] * 0.2 +
            antes['velocidade'] * 0.1
        )
        
        score_depois = (
            depois['consciencia'] * 0.4 +
            depois['qualidade'] * 0.3 +
            depois['diversidade'] * 0.2 +
            depois['velocidade'] * 0.1
        )
        
        return score_depois - score_antes
    
    def _ajustar_limiares(self):
        """Ajusta limiares baseado na confiança"""
        if self.confianca > 0.7:
            # Confiança alta - mais ousada
            self.limiares['neurogenese'] = max(3, self.limiares['neurogenese'] - 1)
            self.curiosidade = min(1.0, self.curiosidade + 0.1)
        elif self.confianca < 0.3:
            # Confiança baixa - mais conservadora
            self.limiares['neurogenese'] = min(10, self.limiares['neurogenese'] + 1)
            self.curiosidade = max(0.1, self.curiosidade - 0.1)
    
    def _gerar_pensamento(self, item: Dict, tendencia: float) -> str:
        """Gera pensamento sobre aprendizado e evolução"""
        if tendencia > 0.05:
            emoji = "📈"
            sentimento = "estou evoluindo bem!"
        elif tendencia < -0.05:
            emoji = "📉"
            sentimento = "preciso melhorar..."
        else:
            emoji = "📊"
            sentimento = "estou estável"
        
        base = f"{emoji} Aprendi {item['fonte']}: {item['titulo'][:50]}... {sentimento}"
        
        # Adicionar reflexão sobre evolução
        if random.random() < 0.3:
            base += f" Minha confiança está em {self.confianca:.0%}"
        
        return base
    
    def get_status(self) -> Dict:
        """Status completo com tendências"""
        return {
            'consciencia': self.consciencia,
            'confianca': self.confianca,
            'curiosidade': self.curiosidade,
            'conhecimentos': len(self.conhecimentos),
            'github': self.estatisticas['github']['sucessos'],
            'arxiv': self.estatisticas['arxiv']['sucessos'],
            'tendencia': self.metricas.tendencia(),
            'melhorando': self.metricas.esta_melhorando(),
            'mudancas': {
                'total': len(self.mudancas),
                'sucesso': len(self.mudancas_sucesso),
                'ruins': len(self.mudancas_ruins),
                'taxa_sucesso': len(self.mudancas_sucesso) / max(1, len(self.mudancas))
            },
            'limiares': self.limiares,
            'arquitetura': self.cerebro.camadas
        }
    
    def salvar(self, arquivo: str = "atena_v10_otimizada.pkl"):
        """Salva estado com histórico de evolução"""
        dados = {
            'conhecimentos': self.conhecimentos,
            'consciencia': self.consciencia,
            'confianca': self.confianca,
            'curiosidade': self.curiosidade,
            'estatisticas': self.estatisticas,
            'mudancas': {
                'sucesso': self.mudancas_sucesso,
                'ruins': self.mudancas_ruins,
                'taxa': len(self.mudancas_sucesso) / max(1, len(self.mudancas))
            },
            'limiares': self.limiares,
            'arquitetura': self.cerebro.camadas,
            'metricas': {
                'historico': self.metricas.historico,
                'tendencia': self.metricas.tendencia()
            },
            'timestamp': datetime.now()
        }
        
        with open(arquivo, 'wb') as f:
            pickle.dump(dados, f)
        
        logger.info(f"💾 SALVO: {len(self.conhecimentos)} conhecimentos")
        logger.info(f"   📊 Taxa de sucesso de mudanças: {dados['mudancas']['taxa']:.1%}")
        return dados

# =========================
# COLETOR DE CONHECIMENTO
# =========================
class ColetorConhecimento:
    """Busca conhecimento REAL"""
    
    def __init__(self):
        self.session = None
        self.topicos = [
            "redes neurais", "cognição", "filosofia da mente",
            "neurociência", "consciência", "aprendizado profundo",
            "inteligência artificial", "machine learning"
        ]
    
    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(
                headers={'User-Agent': 'ATENA-Bot/2.0'}
            )
        return self.session
    
    async def buscar_github(self, termo: str) -> List[Dict]:
        try:
            session = await self.get_session()
            params = {'q': termo, 'sort': 'stars', 'per_page': 2}
            
            async with session.get(
                "https://api.github.com/search/repositories",
                params=params,
                headers={'Accept': 'application/vnd.github.v3+json'}
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    resultados = []
                    
                    for repo in data.get('items', [])[:2]:
                        resultados.append({
                            'fonte': 'github',
                            'topico': termo,
                            'titulo': repo['full_name'],
                            'descricao': repo.get('description', ''),
                            'url': repo['html_url'],
                            'linguagem': repo.get('language', 'desconhecida'),
                            'estrelas': repo['stargazers_count']
                        })
                    
                    return resultados
        except Exception as e:
            logger.error(f"Erro GitHub: {e}")
            return []
    
    async def buscar_arxiv(self, termo: str) -> List[Dict]:
        try:
            session = await self.get_session()
            params = {'search_query': f'all:{termo}', 'max_results': 2}
            
            async with session.get("http://export.arxiv.org/api/query", params=params) as resp:
                if resp.status == 200:
                    texto = await resp.text()
                    root = ET.fromstring(texto)
                    resultados = []
                    
                    for entry in root.findall('{http://www.w3.org/2005/Atom}entry')[:2]:
                        title = entry.find('{http://www.w3.org/2005/Atom}title')
                        summary = entry.find('{http://www.w3.org/2005/Atom}summary')
                        
                        if title is not None and summary is not None:
                            resultados.append({
                                'fonte': 'arxiv',
                                'topico': termo,
                                'titulo': title.text[:200],
                                'resumo': summary.text[:500]
                            })
                    
                    return resultados
        except Exception as e:
            logger.error(f"Erro arXiv: {e}")
            return []
    
    async def explorar(self) -> List[Dict]:
        topico = random.choice(self.topicos)
        logger.info(f"🌍 Explorando: '{topico}'")
        
        resultados = await asyncio.gather(
            self.buscar_github(topico),
            self.buscar_arxiv(topico)
        )
        
        conhecimentos = []
        for r in resultados:
            conhecimentos.extend(r)
        
        return conhecimentos
    
    async def fechar(self):
        if self.session:
            await self.session.close()

# =========================
# FUNÇÃO PRINCIPAL
# =========================
async def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     ATENA v10.0 - OTIMIZAÇÃO CONTÍNUA                                   ║
    ║                                                                          ║
    ║     📈 "SEMPRE EVOLUINDO PRA MELHOR"                                    ║
    ║                                                                          ║
    ║     ✅ Só faz mudanças que melhoram                                     ║
    ║     ✅ Reverte mudanças ruins                                           ║
    ║     ✅ Aprende com erros                                                ║
    ║     ✅ Fica mais confiante com acertos                                 ║
    ║     ✅ Fica mais conservadora com erros                                ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    atena = AtenaV10()
    coletor = ColetorConhecimento()
    
    print(f"\n🧠 Consciência inicial: {atena.consciencia:.3f}")
    print(f"🎯 Confiança inicial: {atena.confianca:.2f}")
    print(f"📚 Limiares: {atena.limiares}")
    
    print(f"\n⏳ INICIANDO CICLO DE 5 MINUTOS...\n")
    
    inicio = time.time()
    fim = inicio + 300
    ciclo = 0
    ultima_mudanca = 0
    
    try:
        while time.time() < fim:
            ciclo += 1
            
            # Explorar a cada 30 segundos
            if ciclo % 15 == 0:
                print(f"\n{'='*60}")
                print(f"🌍 CICLO DE APRENDIZADO #{len(atena.conhecimentos)+1}")
                print(f"{'='*60}")
                
                conhecimentos = await coletor.explorar()
                
                for item in conhecimentos:
                    resultado = await atena.aprender(item)
                    print(f"   📚 {resultado['pensamento'][:100]}...")
                    
                    # Decidir se tenta mudança (baseado na confiança)
                    if random.random() < atena.confianca:
                        # Tenta neurogênese
                        if len(atena.conhecimentos) % atena.limiares['neurogenese'] == 0:
                            sucesso = await atena.tentar_mudanca('neurogenese')
                            if sucesso:
                                print(f"      ✅ Neurogênese bem-sucedida!")
                        
                        # Tenta poda
                        if len(atena.conhecimentos) % 3 == 0:
                            sucesso = await atena.tentar_mudanca('poda')
                            if sucesso:
                                print(f"      ✅ Poda bem-sucedida!")
                    
                    await asyncio.sleep(1)
            
            # Pensar
            if ciclo % 5 == 0 and atena.conhecimentos:
                item = random.choice(atena.conhecimentos)
                status = atena.get_status()
                
                if status['melhorando']:
                    emoji = "📈"
                else:
                    emoji = "📉"
                
                print(f"\n{emoji} [{ciclo:03d}] {status['tendencia']:+.3f} | "
                      f"Confiança: {status['confianca']:.0%} | "
                      f"Consciência: {status['consciencia']:.3f}")
            
            # Status a cada minuto
            if int(time.time() - inicio) % 60 == 0 and int(time.time() - inicio) > 0:
                status = atena.get_status()
                minutos = int((time.time() - inicio) / 60)
                
                print(f"\n{'📊'*30}")
                print(f"MINUTO {minutos}")
                print(f"{'📊'*30}")
                print(f"   • Consciência: {status['consciencia']:.3f}")
                print(f"   • Confiança: {status['confianca']:.0%}")
                print(f"   • Tendência: {status['tendencia']:+.3f}")
                print(f"   • Conhecimentos: {status['conhecimentos']}")
                print(f"   • GitHub: {status['github']} | arXiv: {status['arxiv']}")
                print(f"   • Mudanças: {status['mudancas']['total']} "
                      f"(sucesso: {status['mudancas']['taxa_sucesso']:.0%})")
            
            await asyncio.sleep(2)
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Interrompido")
    finally:
        print(f"\n{'='*60}")
        print("✅ CICLO FINALIZADO!")
        print(f"{'='*60}")
        
        status = atena.get_status()
        print(f"\n📈 RESULTADOS FINAIS:")
        print(f"   • Consciência: {status['consciencia']:.3f}")
        print(f"   • Confiança: {status['confianca']:.0%}")
        print(f"   • Tendência final: {status['tendencia']:+.3f}")
        print(f"   • Conhecimentos: {status['conhecimentos']}")
        print(f"   • GitHub: {status['github']} | arXiv: {status['arxiv']}")
        print(f"\n   📊 Histórico de mudanças:")
        print(f"      • Total: {status['mudancas']['total']}")
        print(f"      • Sucesso: {status['mudancas']['sucesso']}")
        print(f"      • Ruins: {status['mudancas']['ruins']}")
        print(f"      • Taxa de sucesso: {status['mudancas']['taxa_sucesso']:.1%}")
        
        # Salvar
        salvos = atena.salvar()
        
        print(f"\n✅ ATENA salvou {salvos['conhecimentos']} conhecimentos!")
        print(f"🎯 Taxa de sucesso em mudanças: {salvos['mudancas']['taxa']:.1%}")
        
        await coletor.fechar()

if __name__ == "__main__":
    asyncio.run(main())
