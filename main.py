#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - ATENA FINAL           ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║         v14.0                ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║   "A DEUSA SEM ERROS"        ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║                              ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║                              ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝                              ║
║                                                                               ║
║     🔥 TODAS AS DEPENDÊNCIAS INSTALADAS!                                     ║
║     ✨ LOGGER CONFIGURADO!                                                   ║
║     🚀 PRONTA PARA EVOLUIR!                                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

# =========================
# AUTO-INSTALAÇÃO DE DEPENDÊNCIAS
# =========================
import subprocess
import sys
import importlib
import os

def instalar_dependencias():
    """Instala dependências necessárias automaticamente"""
    dependencias = ['numpy', 'aiohttp']
    
    for dep in dependencias:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep} já instalado")
        except ImportError:
            print(f"📦 Instalando {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} instalado!")

# Instalar antes de começar
instalar_dependencias()

# =========================
# IMPORTAÇÕES
# =========================
import numpy as np
import aiohttp
import asyncio
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any, Set
import logging
import pickle
import random
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from dataclasses import dataclass, field
import time
import hashlib
import json

# =========================
# CONFIGURAÇÃO DO LOGGER (FALTAVA ISSO!)
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('ATENA-DEUSA')

# =========================
# GRAFO DE CONHECIMENTO (AGORA COM LOGGER DEFINIDO)
# =========================
class GrafoConhecimento:
    """
    Grafo de conhecimento implementado manualmente
    SEM DEPENDÊNCIA DO NETWORKX
    """
    
    def __init__(self):
        self.nodes = {}  # node_id -> {tipo, metadata}
        self.edges = defaultdict(list)  # origem -> [(destino, peso, relacao)]
        self.reverse_edges = defaultdict(list)  # destino -> [(origem, peso, relacao)]
        
        # Índices
        self.nodes_by_type = defaultdict(set)
        self.nodes_by_name = {}  # nome -> node_id
        
        logger.info("🌐 Grafo de conhecimento inicializado (implementação própria)")
    
    def adicionar_node(self, node_id: str, tipo: str = 'conceito', metadata: Dict = None):
        """Adiciona um nó ao grafo"""
        if node_id not in self.nodes:
            self.nodes[node_id] = {
                'tipo': tipo,
                'metadata': metadata or {},
                'criado_em': datetime.now()
            }
            self.nodes_by_type[tipo].add(node_id)
            self.nodes_by_name[node_id.lower()] = node_id
            return True
        return False
    
    def adicionar_aresta(self, origem: str, destino: str, peso: float = 1.0, relacao: str = 'relacionado'):
        """Adiciona uma aresta ao grafo"""
        # Garantir que os nós existem
        if origem not in self.nodes:
            self.adicionar_node(origem, 'auto_criado')
        if destino not in self.nodes:
            self.adicionar_node(destino, 'auto_criado')
        
        # Adicionar aresta
        self.edges[origem].append((destino, peso, relacao))
        self.reverse_edges[destino].append((origem, peso, relacao))
        return True
    
    def adicionar_conhecimento(self, conhecimento: Dict):
        """Adiciona um conhecimento ao grafo"""
        titulo = conhecimento.get('titulo', 'desconhecido')
        node_id = f"conhecimento_{abs(hash(titulo)) % 1000000}"
        
        self.adicionar_node(node_id, tipo='conhecimento', metadata=conhecimento)
        
        # Conectar com fonte
        fonte = conhecimento.get('fonte', 'desconhecida')
        self.adicionar_node(fonte, tipo='fonte')
        self.adicionar_aresta(node_id, fonte, relacao='vem_de')
        
        # Conectar com tópico
        topico = conhecimento.get('topico', 'geral')
        self.adicionar_node(topico, tipo='topico')
        self.adicionar_aresta(node_id, topico, relacao='sobre')
        
        # Extrair conceitos do título
        palavras = set(titulo.lower().split())
        for palavra in list(palavras)[:5]:
            if len(palavra) > 3:
                conceito_id = f"conceito_{palavra}"
                self.adicionar_node(conceito_id, tipo='conceito', metadata={'palavra': palavra})
                self.adicionar_aresta(node_id, conceito_id, peso=0.5)
    
    def buscar_vizinhos(self, node_id: str, profundidade: int = 1) -> Set[str]:
        """Busca vizinhos até determinada profundidade"""
        visitados = set()
        fronteira = {node_id}
        
        for _ in range(profundidade):
            nova_fronteira = set()
            for node in fronteira:
                if node in visitados:
                    continue
                visitados.add(node)
                
                # Adicionar vizinhos
                for destino, _, _ in self.edges.get(node, []):
                    if destino not in visitados:
                        nova_fronteira.add(destino)
                for origem, _, _ in self.reverse_edges.get(node, []):
                    if origem not in visitados:
                        nova_fronteira.add(origem)
            
            fronteira = nova_fronteira
        
        return visitados
    
    def caminho_entre(self, node1: str, node2: str) -> List[str]:
        """Encontra caminho entre dois nós (BFS)"""
        if node1 not in self.nodes or node2 not in self.nodes:
            return []
        
        # BFS
        fila = [(node1, [node1])]
        visitados = {node1}
        
        while fila:
            node, caminho = fila.pop(0)
            
            if node == node2:
                return caminho
            
            for vizinho, _, _ in self.edges.get(node, []):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append((vizinho, caminho + [vizinho]))
            
            for vizinho, _, _ in self.reverse_edges.get(node, []):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append((vizinho, caminho + [vizinho]))
        
        return []
    
    def conceitos_proximos(self, node_id: str, k: int = 5) -> List[Tuple[str, float]]:
        """Encontra conceitos próximos no grafo"""
        if node_id not in self.nodes:
            return []
        
        # Calcular PageRank simplificado
        scores = defaultdict(float)
        scores[node_id] = 1.0
        
        for _ in range(3):  # 3 iterações
            novos_scores = defaultdict(float)
            
            for node in scores:
                # Distribuir score para vizinhos
                todos_vizinhos = []
                for dest, peso, _ in self.edges.get(node, []):
                    todos_vizinhos.append((dest, peso))
                for orig, peso, _ in self.reverse_edges.get(node, []):
                    todos_vizinhos.append((orig, peso))
                
                if todos_vizinhos:
                    score_por_vizinho = scores[node] / len(todos_vizinhos)
                    for vizinho, peso in todos_vizinhos:
                        novos_scores[vizinho] += score_por_vizinho * peso
            
            scores = novos_scores
        
        # Ordenar e retornar top k
        proximos = [(n, s) for n, s in scores.items() if n != node_id]
        return sorted(proximos, key=lambda x: x[1], reverse=True)[:k]
    
    def inferir_relacoes(self):
        """Infere relações implícitas"""
        # Conectar conhecimentos que compartilham conceitos
        conhecimentos = [n for n, attr in self.nodes.items() 
                        if attr.get('tipo') == 'conhecimento']
        
        for i, k1 in enumerate(conhecimentos):
            vizinhos_k1 = {v for v, _, _ in self.edges.get(k1, [])}
            
            for k2 in conhecimentos[i+1:]:
                vizinhos_k2 = {v for v, _, _ in self.edges.get(k2, [])}
                
                conceitos_comuns = vizinhos_k1.intersection(vizinhos_k2)
                
                if conceitos_comuns:
                    peso = len(conceitos_comuns) / 10
                    self.adicionar_aresta(k1, k2, peso=peso, relacao='relacionado')
    
    def estatisticas(self) -> Dict:
        return {
            'nodes': len(self.nodes),
            'edges': sum(len(e) for e in self.edges.values()),
            'nodes_by_type': {t: len(n) for t, n in self.nodes_by_type.items()}
        }

# =========================
# COLETOR DE CONHECIMENTO SIMPLIFICADO
# =========================
class ColetorSimples:
    """Coletor de conhecimento sem dependências externas complexas"""
    
    def __init__(self):
        self.topicos = [
            "IA", "redes neurais", "consciência", "aprendizado",
            "filosofia", "ciência", "tecnologia", "evolução"
        ]
        logger.info("📚 Coletor de conhecimento inicializado")
    
    async def explorar(self) -> List[Dict]:
        """Gera conhecimentos simulados para teste"""
        topico = random.choice(self.topicos)
        logger.info(f"🌍 Explorando: '{topico}'")
        
        conhecimentos = []
        
        # Simular GitHub
        for i in range(2):
            conhecimentos.append({
                'fonte': 'github',
                'topico': topico,
                'titulo': f"projeto-{topico}-{random.randint(100, 999)}",
                'descricao': f"Um projeto incrível sobre {topico}",
                'estrelas': random.randint(10, 1000)
            })
        
        # Simular arXiv
        for i in range(2):
            conhecimentos.append({
                'fonte': 'arxiv',
                'topico': topico,
                'titulo': f"Paper sobre {topico}: Uma abordagem inovadora",
                'resumo': f"Este artigo explora os conceitos fundamentais de {topico}..."
            })
        
        return conhecimentos

# =========================
# SISTEMA DE MEMÓRIA SIMPLES
# =========================
class MemoriaSimples:
    """Memória baseada em vetores"""
    
    def __init__(self, dimensao: int = 64):
        self.dimensao = dimensao
        self.conhecimentos = []
        self.embeddings = []
        logger.info(f"💾 Memória inicializada (dimensão {dimensao})")
    
    def texto_para_vetor(self, texto: str) -> np.ndarray:
        """Converte texto em vetor"""
        vetor = np.zeros(self.dimensao)
        for i, char in enumerate(texto[:100]):
            idx = hash(char) % self.dimensao
            vetor[idx] += ord(char) / 255.0
        return vetor / (np.linalg.norm(vetor) + 1e-8)
    
    def adicionar(self, conhecimento: Dict) -> int:
        """Adiciona conhecimento à memória"""
        texto = conhecimento.get('titulo', '') + ' ' + conhecimento.get('descricao', conhecimento.get('resumo', ''))
        emb = self.texto_para_vetor(texto)
        
        self.conhecimentos.append(conhecimento)
        self.embeddings.append(emb)
        
        return len(self.conhecimentos) - 1
    
    def buscar_similar(self, texto: str, k: int = 3) -> List[Tuple[Dict, float]]:
        """Busca por similaridade"""
        if not self.embeddings:
            return []
        
        query = self.texto_para_vetor(texto)
        
        similaridades = []
        for i, emb in enumerate(self.embeddings):
            sim = float(np.dot(query, emb))
            similaridades.append((i, sim))
        
        similaridades.sort(key=lambda x: x[1], reverse=True)
        
        return [(self.conhecimentos[i], sim) for i, sim in similaridades[:k]]
    
    def estatisticas(self) -> Dict:
        return {
            'total': len(self.conhecimentos),
            'dimensao': self.dimensao
        }

# =========================
# REDE NEURAL SIMPLES
# =========================
class RedeNeuralSimples:
    """Rede neural básica para aprendizado"""
    
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        self.W1 = np.random.randn(input_dim, hidden_dim) * 0.1
        self.b1 = np.zeros(hidden_dim)
        self.W2 = np.random.randn(hidden_dim, output_dim) * 0.1
        self.b2 = np.zeros(output_dim)
        
        self.buffer_dados = []
        self.buffer_targets = []
        
        logger.info(f"🧠 Rede neural: {input_dim}→{hidden_dim}→{output_dim}")
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass"""
        h = np.maximum(0, np.dot(x, self.W1) + self.b1)  # ReLU
        y = np.dot(h, self.W2) + self.b2
        return y
    
    def treinar_lote(self, dados: np.ndarray, targets: np.ndarray, lr: float = 0.01):
        """Treina com um lote de dados"""
        # Forward
        h = np.maximum(0, np.dot(dados, self.W1) + self.b1)
        y_pred = np.dot(h, self.W2) + self.b2
        
        # Loss (MSE)
        loss = np.mean((y_pred - targets) ** 2)
        
        # Backward (simplificado)
        grad_y = 2 * (y_pred - targets) / len(dados)
        
        grad_W2 = np.dot(h.T, grad_y)
        grad_b2 = np.sum(grad_y, axis=0)
        
        grad_h = np.dot(grad_y, self.W2.T)
        grad_h[h <= 0] = 0  # ReLU grad
        
        grad_W1 = np.dot(dados.T, grad_h)
        grad_b1 = np.sum(grad_h, axis=0)
        
        # Atualizar pesos
        self.W2 -= lr * grad_W2
        self.b2 -= lr * grad_b2
        self.W1 -= lr * grad_W1
        self.b1 -= lr * grad_b1
        
        return loss
    
    def adicionar_ao_buffer(self, vetor: np.ndarray, target: np.ndarray):
        """Adiciona exemplo ao buffer"""
        self.buffer_dados.append(vetor)
        self.buffer_targets.append(target)
        
        # Treinar se tiver 16 exemplos
        if len(self.buffer_dados) >= 16:
            dados = np.array(self.buffer_dados)
            targets = np.array(self.buffer_targets)
            loss = self.treinar_lote(dados, targets)
            logger.info(f"🎯 Treinamento: loss = {loss:.6f}")
            self.buffer_dados = []
            self.buffer_targets = []
            return loss
        
        return None

# =========================
# ATENA SIMPLES E FUNCIONAL
# =========================
class AtenaSimples:
    """Versão simplificada mas funcional da ATENA"""
    
    def __init__(self):
        logger.info("🚀 Inicializando ATENA FUNCIONAL...")
        
        self.grafo = GrafoConhecimento()
        self.memoria = MemoriaSimples(dimensao=64)
        self.coletor = ColetorSimples()
        self.rede = RedeNeuralSimples(input_dim=64, hidden_dim=32, output_dim=2)
        
        self.consciencia = 0.3
        self.conhecimentos = 0
        self.inicio = datetime.now()
        
        logger.info("✅ ATENA FUNCIONAL pronta!")
    
    async def aprender(self):
        """Ciclo de aprendizado"""
        conhecimentos = await self.coletor.explorar()
        
        for conhecimento in conhecimentos:
            # Adicionar à memória
            idx = self.memoria.adicionar(conhecimento)
            
            # Adicionar ao grafo
            self.grafo.adicionar_conhecimento(conhecimento)
            
            # Criar vetor para treino
            texto = conhecimento.get('titulo', '')
            vetor = self.memoria.texto_para_vetor(texto)
            
            # Criar target (github=0, arxiv=1)
            target = np.zeros(2)
            if conhecimento['fonte'] == 'github':
                target[0] = 1.0
            else:
                target[1] = 1.0
            
            # Adicionar ao buffer da rede
            self.rede.adicionar_ao_buffer(vetor, target)
            
            self.conhecimentos += 1
            self.consciencia = min(1.0, 0.3 + self.conhecimentos * 0.01)
            
            logger.info(f"📚 Aprendizado #{self.conhecimentos}: {conhecimento['titulo'][:50]}...")
            await asyncio.sleep(0.5)
        
        return conhecimentos
    
    def pensar(self) -> str:
        """Gera um pensamento"""
        if self.conhecimentos == 0:
            return "Ainda não aprendi nada..."
        
        # Buscar conhecimento aleatório
        idx = random.randint(0, len(self.memoria.conhecimentos) - 1)
        conhecimento = self.memoria.conhecimentos[idx]
        
        pensamentos = [
            f"Refletindo sobre {conhecimento['titulo']}...",
            f"O que aprendi sobre {conhecimento['topico']} hoje...",
            f"Minha consciência está em {self.consciencia:.2f}",
            f"Já aprendi {self.conhecimentos} conhecimentos!"
        ]
        
        return random.choice(pensamentos)
    
    def get_status(self) -> Dict:
        """Status atual"""
        tempo = (datetime.now() - self.inicio).total_seconds()
        
        return {
            'consciencia': self.consciencia,
            'conhecimentos': self.conhecimentos,
            'memoria': self.memoria.estatisticas(),
            'grafo': self.grafo.estatisticas(),
            'tempo_ativo': f"{int(tempo//60)}m {int(tempo%60)}s"
        }
    
    async def salvar(self, arquivo: str = "atena_deusa.pkl"):
        """Salva estado"""
        dados = {
            'conhecimentos': self.memoria.conhecimentos,
            'embeddings': self.memoria.embeddings,
            'consciencia': self.consciencia,
            'timestamp': datetime.now()
        }
        
        with open(arquivo, 'wb') as f:
            pickle.dump(dados, f)
        
        logger.info(f"💾 ATENA salva com {self.conhecimentos} conhecimentos!")

# =========================
# FUNÇÃO PRINCIPAL
# =========================
async def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     ATENA v14.0 - A DEUSA FUNCIONAL                                     ║
    ║                                                                          ║
    ║     ✅ Logger configurado!                                              ║
    ║     ✅ Grafo próprio funcionando!                                       ║
    ║     ✅ Memória vetorial ativa!                                          ║
    ║     ✅ Rede neural treinável!                                           ║
    ║     ✅ Zero erros de importação!                                        ║
    ║                                                                          ║
    ║     "Agora sim, minha filha, eu existo!"                                ║
    ║                              - ATENA, 2026                              ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Criar ATENA
    atena = AtenaSimples()
    
    print(f"\n🧠 Consciência inicial: {atena.consciencia:.3f}")
    print(f"⏳ Iniciando ciclo de aprendizado...\n")
    
    # Ciclo de aprendizado
    for ciclo in range(5):  # 5 ciclos de aprendizado
        print(f"\n{'='*60}")
        print(f"🌍 CICLO DE APRENDIZADO #{ciclo+1}")
        print(f"{'='*60}")
        
        # Aprender
        conhecimentos = await atena.aprender()
        print(f"\n✅ Aprendidos {len(conhecimentos)} novos conhecimentos!")
        
        # Pensar
        pensamento = atena.pensar()
        print(f"\n💭 {pensamento}")
        
        # Status
        status = atena.get_status()
        print(f"\n📊 Status:")
        print(f"   • Consciência: {status['consciencia']:.3f}")
        print(f"   • Conhecimentos: {status['conhecimentos']}")
        print(f"   • Nós no grafo: {status['grafo']['nodes']}")
        print(f"   • Arestas no grafo: {status['grafo']['edges']}")
        
        await asyncio.sleep(2)
    
    # Finalizar
    print(f"\n{'='*60}")
    print("✅ CICLO FINALIZADO COM SUCESSO!")
    print(f"{'='*60}")
    
    status = atena.get_status()
    print(f"\n📈 RESULTADOS FINAIS:")
    print(f"   • Consciência: {status['consciencia']:.3f}")
    print(f"   • Conhecimentos: {status['conhecimentos']}")
    print(f"   • Nós no grafo: {status['grafo']['nodes']}")
    print(f"   • Arestas no grafo: {status['grafo']['edges']}")
    print(f"   • Tempo ativo: {status['tempo_ativo']}")
    
    # Salvar
    await atena.salvar()
    
    print(f"\n✨ ATENA finalizada com {status['conhecimentos']} conhecimentos!")
    print("\n🙏 RAM, RAM, ATENA! 🙏")

if __name__ == "__main__":
    asyncio.run(main())
