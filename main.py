#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - ATENA FINAL           ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║         v13.0                ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║   "A DEUSA DA IA MODERNA"    ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║                              ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║                              ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝                              ║
║                                                                               ║
║     🚀 TRANSFORMERS | 📊 EXPERIENCE REPLAY | 🦋 AUTO-ML | 🌐 KNOWLEDGE GRAPH  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import numpy as np
import asyncio
import aiohttp
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any
import logging
import pickle
import random
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
import networkx as nx
from dataclasses import dataclass, field
import time
import hashlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
logger = logging.getLogger('ATENA-FINAL')

# =========================
# 1. TRANSFORMER SIMPLIFICADO (Attention Is All You Need)
# =========================
class SelfAttention:
    """Camada de Self-Attention simplificada"""
    
    def __init__(self, dim: int, num_heads: int = 4):
        self.dim = dim
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        
        # Pesos para Query, Key, Value
        self.W_q = np.random.randn(dim, dim) * 0.01
        self.W_k = np.random.randn(dim, dim) * 0.01
        self.W_v = np.random.randn(dim, dim) * 0.01
        self.W_o = np.random.randn(dim, dim) * 0.01
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass da atenção"""
        # x shape: (seq_len, dim)
        Q = x @ self.W_q
        K = x @ self.W_k
        V = x @ self.W_v
        
        # Scaled dot-product attention
        scores = (Q @ K.T) / np.sqrt(self.head_dim)
        
        # Softmax
        exp_scores = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
        attn = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)
        
        # Apply attention
        out = attn @ V
        
        # Output projection
        return out @ self.W_o

class TransformerBlock:
    """Bloco Transformer completo"""
    
    def __init__(self, dim: int, num_heads: int = 4):
        self.attention = SelfAttention(dim, num_heads)
        self.norm1 = lambda x: (x - np.mean(x)) / (np.std(x) + 1e-8)
        
        # Feed-forward network
        self.ffn = [
            np.random.randn(dim, dim * 4) * 0.01,
            np.random.randn(dim * 4, dim) * 0.01
        ]
        self.norm2 = lambda x: (x - np.mean(x)) / (np.std(x) + 1e-8)
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        # Attention with residual
        attn_out = self.attention.forward(x)
        x = self.norm1(x + attn_out)
        
        # FFN with residual
        ffn_out = np.maximum(0, x @ self.ffn[0]) @ self.ffn[1]  # ReLU
        x = self.norm2(x + ffn_out)
        
        return x

class TransformerEncoder:
    """Encoder Transformer completo"""
    
    def __init__(self, dim: int = 128, num_layers: int = 3, num_heads: int = 4):
        self.dim = dim
        self.layers = [TransformerBlock(dim, num_heads) for _ in range(num_layers)]
        
        # Positional encoding
        self.pos_encoding = self._create_positional_encoding(100, dim)
    
    def _create_positional_encoding(self, max_len: int, dim: int) -> np.ndarray:
        """Cria positional encoding como no paper 'Attention Is All You Need'"""
        pe = np.zeros((max_len, dim))
        position = np.arange(0, max_len).reshape(-1, 1)
        div_term = np.exp(np.arange(0, dim, 2) * -(np.log(10000.0) / dim))
        
        pe[:, 0::2] = np.sin(position * div_term)
        pe[:, 1::2] = np.cos(position * div_term)
        
        return pe
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        # Add positional encoding
        x = x + self.pos_encoding[:len(x)]
        
        # Pass through transformer layers
        for layer in self.layers:
            x = layer.forward(x)
        
        return x

# =========================
# 2. EMBEDDINGS COM SENTENCE-TRANSFORMERS (simulado)
# =========================
class EmbeddingsTransformer:
    """Gera embeddings usando transformer (simulado com hashing)"""
    
    def __init__(self, dim: int = 384):
        self.dim = dim
        self.transformer = TransformerEncoder(dim=dim, num_layers=2)
        self.cache = {}
    
    def encode(self, texto: str) -> np.ndarray:
        """Gera embedding para um texto"""
        if texto in self.cache:
            return self.cache[texto]
        
        # Simular tokenização simples
        tokens = texto.lower().split()[:50]  # Máximo 50 tokens
        
        # Criar embeddings iniciais (simulado)
        token_embeddings = []
        for token in tokens:
            # Usar hash para gerar embedding inicial
            hash_val = int(hashlib.md5(token.encode()).hexdigest(), 16)
            np.random.seed(hash_val % 2**32)
            emb = np.random.randn(self.dim) * 0.1
            token_embeddings.append(emb)
        
        # Padding se necessário
        while len(token_embeddings) < 50:
            token_embeddings.append(np.zeros(self.dim))
        
        # Stack e passar pelo transformer
        x = np.stack(token_embeddings[:50])
        encoded = self.transformer.forward(x)
        
        # Usar média dos tokens como embedding do texto
        embedding = np.mean(encoded, axis=0)
        
        # Normalizar
        embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
        
        self.cache[texto] = embedding
        return embedding
    
    def similaridade(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Similaridade cosseno"""
        return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2) + 1e-8))

# =========================
# 3. VECTOR DATABASE REAL (com embeddings transformer)
# =========================
class VectorDatabase:
    """Banco vetorial real com embeddings transformer"""
    
    def __init__(self, embedder: EmbeddingsTransformer):
        self.embedder = embedder
        self.conhecimentos: List[Dict] = []
        self.embeddings: List[np.ndarray] = []
        self.indices_por_fonte = defaultdict(list)
        self.indices_por_topico = defaultdict(list)
        
        # Índice para busca rápida (simulado com KD-Tree)
        self.indice_construido = False
    
    def adicionar(self, conhecimento: Dict) -> int:
        """Adiciona conhecimento ao banco vetorial"""
        # Gerar embedding com transformer
        texto = self._criar_texto_para_embedding(conhecimento)
        embedding = self.embedder.encode(texto)
        
        # Adicionar
        idx = len(self.conhecimentos)
        self.conhecimentos.append(conhecimento)
        self.embeddings.append(embedding)
        
        # Indexar
        fonte = conhecimento.get('fonte', 'desconhecida')
        self.indices_por_fonte[fonte].append(idx)
        
        topico = conhecimento.get('topico', 'geral')
        self.indices_por_topico[topico].append(idx)
        
        self.indice_construido = False
        return idx
    
    def _criar_texto_para_embedding(self, conhecimento: Dict) -> str:
        """Cria texto rico para embedding"""
        partes = [
            conhecimento.get('titulo', ''),
            conhecimento.get('descricao', conhecimento.get('resumo', '')),
            f"fonte: {conhecimento.get('fonte', '')}",
            f"topico: {conhecimento.get('topico', '')}"
        ]
        
        # Adicionar metadados de popularidade
        if 'estrelas' in conhecimento:
            partes.append(f"popularidade: {conhecimento['estrelas']} estrelas")
        
        return ' '.join(partes)
    
    def buscar_similar(self, texto: str, k: int = 5) -> List[Tuple[Dict, float]]:
        """Busca por similaridade semântica"""
        if not self.embeddings:
            return []
        
        # Embedding da consulta
        query_emb = self.embedder.encode(texto)
        
        # Calcular similaridades
        similaridades = []
        for i, emb in enumerate(self.embeddings):
            sim = self.embedder.similaridade(query_emb, emb)
            similaridades.append((i, sim))
        
        # Ordenar
        similaridades.sort(key=lambda x: x[1], reverse=True)
        
        # Retornar top k
        return [(self.conhecimentos[i], sim) for i, sim in similaridades[:k]]
    
    def buscar_por_fonte(self, fonte: str) -> List[Dict]:
        """Busca por fonte"""
        return [self.conhecimentos[i] for i in self.indices_por_fonte.get(fonte, [])]
    
    def buscar_por_topico(self, topico: str) -> List[Dict]:
        """Busca por tópico"""
        return [self.conhecimentos[i] for i in self.indices_por_topico.get(topico, [])]
    
    def buscar_incerto(self, modelo, limiar: float = 0.3) -> List[Dict]:
        """
        Busca onde o modelo está incerto - SUA IDEIA
        explore where the model is uncertain
        """
        incertos = []
        
        for i, conhecimento in enumerate(self.conhecimentos):
            texto = self._criar_texto_para_embedding(conhecimento)
            emb = self.embeddings[i]
            
            # Simular incerteza (quanto menor a similaridade com outros)
            similaridades = []
            for j, emb2 in enumerate(self.embeddings):
                if i != j:
                    sim = self.embedder.similaridade(emb, emb2)
                    similaridades.append(sim)
            
            if similaridades:
                incerteza = 1 - np.mean(similaridades)
                if incerteza > limiar:
                    incertos.append((conhecimento, incerteza))
        
        return sorted(incertos, key=lambda x: x[1], reverse=True)
    
    def estatisticas(self) -> Dict:
        """Estatísticas do banco vetorial"""
        return {
            'total': len(self.conhecimentos),
            'por_fonte': {f: len(i) for f, i in self.indices_por_fonte.items()},
            'por_topico': {t: len(i) for t, i in self.indices_por_topico.items()},
            'dimensao_embeddings': len(self.embeddings[0]) if self.embeddings else 0
        }

# =========================
# 4. EXPERIENCE REPLAY BUFFER (SUA IDEIA)
# =========================
class ExperienceReplay:
    """
    Buffer de experiência para treinar com batches
    
    guardar batch de exemplos
    treinar juntos
    self.buffer_dados.append(vetor)
    self.buffer_targets.append(target)
    
    if len(self.buffer_dados) >= 16:
        self.rede.treinar_lote(...)
    """
    
    def __init__(self, capacidade: int = 1000, batch_size: int = 32):
        self.capacidade = capacidade
        self.batch_size = batch_size
        self.buffer_dados = deque(maxlen=capacidade)
        self.buffer_targets = deque(maxlen=capacidade)
        self.buffer_metadata = deque(maxlen=capacidade)
        
        # Estatísticas
        self.total_adicionados = 0
        self.total_treinamentos = 0
    
    def adicionar(self, vetor: np.ndarray, target: np.ndarray, metadata: Dict = None):
        """
        Adiciona experiência ao buffer - SUA IDEIA
        """
        self.buffer_dados.append(vetor.copy())
        self.buffer_targets.append(target.copy())
        self.buffer_metadata.append(metadata or {})
        self.total_adicionados += 1
    
    def sample(self, batch_size: int = None) -> Tuple[np.ndarray, np.ndarray, List]:
        """
        Amostra batch aleatório - EXPERIENCE REPLAY
        batch = random.sample(self.memoria.embeddings, 32)
        """
        if batch_size is None:
            batch_size = self.batch_size
        
        if len(self.buffer_dados) < batch_size:
            return None, None, None
        
        # Amostragem aleatória
        indices = random.sample(range(len(self.buffer_dados)), batch_size)
        
        dados = np.array([self.buffer_dados[i] for i in indices])
        targets = np.array([self.buffer_targets[i] for i in indices])
        metadata = [self.buffer_metadata[i] for i in indices]
        
        return dados, targets, metadata
    
    def sample_prioritized(self, batch_size: int = None):
        """
        Amostragem prioritária (maior loss)
        """
        # Implementação simplificada
        return self.sample(batch_size)
    
    def pode_treinar(self) -> bool:
        """Verifica se tem dados suficientes para treinar"""
        return len(self.buffer_dados) >= self.batch_size
    
    def limpar(self):
        """Limpa o buffer"""
        self.buffer_dados.clear()
        self.buffer_targets.clear()
        self.buffer_metadata.clear()
    
    def estatisticas(self) -> Dict:
        return {
            'tamanho': len(self.buffer_dados),
            'capacidade': self.capacidade,
            'batch_size': self.batch_size,
            'total_adicionados': self.total_adicionados,
            'total_treinamentos': self.total_treinamentos
        }

# =========================
# 5. REDE NEURAL COM EXPANSÃO PRESERVANDO PESOS (SUA IDEIA)
# =========================
class RedeNeuralExpansivel:
    """
    Rede neural que pode expandir camadas preservando pesos
    
    preservar pesos existentes
    expandir camada mantendo pesos antigos
    """
    
    def __init__(self, camadas: List[int]):
        self.camadas = camadas
        self.pesos = []
        self.biases = []
        self._inicializar_pesos()
        
        # Buffer de treinamento
        self.buffer = ExperienceReplay(capacidade=1000, batch_size=32)
        
        logger.info(f"🧠 Rede criada: {camadas}")
    
    def _inicializar_pesos(self):
        """Inicialização Xavier"""
        self.pesos = []
        self.biases = []
        
        for i in range(len(self.camadas) - 1):
            limite = np.sqrt(6 / (self.camadas[i] + self.camadas[i+1]))
            peso = np.random.uniform(-limite, limite, (self.camadas[i], self.camadas[i+1]))
            self.pesos.append(peso)
            self.biases.append(np.zeros(self.camadas[i+1]))
    
    def expandir_camada(self, camada_idx: int, novos_neurons: int):
        """
        EXPANDE UMA CAMADA PRESERVANDO PESOS - SUA IDEIA
        
        preservar pesos existentes
        expandir camada mantendo pesos antigos
        """
        if camada_idx >= len(self.camadas) - 1:
            logger.warning("Não pode expandir última camada")
            return False
        
        logger.info(f"📈 Expandindo camada {camada_idx}: {self.camadas[camada_idx]} → {self.camadas[camada_idx] + novos_neurons}")
        
        # Salvar pesos antigos
        pesos_entrada_antigos = self.pesos[camada_idx - 1].copy() if camada_idx > 0 else None
        pesos_saida_antigos = self.pesos[camada_idx].copy()
        bias_antigo = self.biases[camada_idx].copy()
        
        # Nova dimensão
        nova_dimensao = self.camadas[camada_idx] + novos_neurons
        
        # Expandir pesos de entrada (camada anterior → esta camada)
        if camada_idx > 0:
            novo_peso_entrada = np.zeros((self.camadas[camada_idx-1], nova_dimensao))
            novo_peso_entrada[:, :self.camadas[camada_idx]] = pesos_entrada_antigos
            
            # Inicializar novas conexões com ruído pequeno
            novo_peso_entrada[:, self.camadas[camada_idx]:] = np.random.randn(
                self.camadas[camada_idx-1], novos_neurons
            ) * 0.01
            
            self.pesos[camada_idx-1] = novo_peso_entrada
        
        # Expandir pesos de saída (esta camada → próxima camada)
        novo_peso_saida = np.zeros((nova_dimensao, self.camadas[camada_idx+1]))
        novo_peso_saida[:self.camadas[camada_idx], :] = pesos_saida_antigos
        
        # Inicializar novas conexões
        novo_peso_saida[self.camadas[camada_idx]:, :] = np.random.randn(
            novos_neurons, self.camadas[camada_idx+1]
        ) * 0.01
        
        self.pesos[camada_idx] = novo_peso_saida
        
        # Expandir bias
        novo_bias = np.zeros(nova_dimensao)
        novo_bias[:len(bias_antigo)] = bias_antigo
        novo_bias[len(bias_antigo):] = np.random.randn(novos_neurons) * 0.01
        self.biases[camada_idx] = novo_bias
        
        # Atualizar arquitetura
        self.camadas[camada_idx] = nova_dimensao
        
        return True
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass"""
        ativacoes = [x]
        
        for i, (peso, bias) in enumerate(zip(self.pesos, self.biases)):
            z = np.dot(ativacoes[-1], peso) + bias
            
            if i < len(self.pesos) - 1:
                a = np.maximum(0, z)  # ReLU
            else:
                # Softmax
                exp_z = np.exp(z - np.max(z, axis=-1, keepdims=True))
                a = exp_z / np.sum(exp_z, axis=-1, keepdims=True)
            
            ativacoes.append(a)
        
        return ativacoes[-1]
    
    def loss_cross_entropy(self, y_pred: np.ndarray, y_true: np.ndarray) -> float:
        """
        Cross Entropy - SUA IDEIA
        
        return float(-np.mean(np.sum(y_true * np.log(y_pred + 1e-15), axis=1)))
        """
        eps = 1e-15
        return float(-np.mean(np.sum(y_true * np.log(y_pred + eps), axis=1)))
    
    def adicionar_ao_buffer(self, vetor: np.ndarray, target: np.ndarray, metadata: Dict = None):
        """Adiciona exemplo ao buffer - SUA IDEIA"""
        self.buffer.adicionar(vetor, target, metadata)
        
        # Treinar se buffer estiver cheio
        if self.buffer.pode_treinar():
            self.treinar_batch()
    
    def treinar_batch(self, lr: float = 0.01) -> Optional[float]:
        """
        Treina com batch do buffer - SUA IDEIA
        """
        if not self.buffer.pode_treinar():
            return None
        
        # Sample do buffer
        dados, targets, metadata = self.buffer.sample()
        
        if dados is None:
            return None
        
        # Treinar
        loss = self.treinar_lote(dados, targets, lr)
        
        self.buffer.total_treinamentos += 1
        logger.info(f"🎯 Treinamento #{self.buffer.total_treinamentos}: loss = {loss:.6f}")
        
        return loss
    
    def treinar_lote(self, dados: np.ndarray, targets: np.ndarray, lr: float = 0.01) -> float:
        """Treinamento em lote"""
        # Shuffle
        indices = np.random.permutation(len(dados))
        dados = dados[indices]
        targets = targets[indices]
        
        # Forward
        ativacoes = [dados]
        zs = []
        
        for i, (peso, bias) in enumerate(zip(self.pesos, self.biases)):
            z = np.dot(ativacoes[-1], peso) + bias
            zs.append(z)
            
            if i < len(self.pesos) - 1:
                a = np.maximum(0, z)
            else:
                exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
                a = exp_z / np.sum(exp_z, axis=1, keepdims=True)
            
            ativacoes.append(a)
        
        # Loss
        y_pred = ativacoes[-1]
        loss = self.loss_cross_entropy(y_pred, targets)
        
        # Backward
        delta = y_pred - targets
        
        for i in range(len(self.pesos) - 1, -1, -1):
            grad_peso = np.dot(ativacoes[i].T, delta) / len(dados)
            grad_bias = np.sum(delta, axis=0) / len(dados)
            
            self.pesos[i] -= lr * grad_peso
            self.biases[i] -= lr * grad_bias
            
            if i > 0:
                delta = np.dot(delta, self.pesos[i].T)
                delta[ativacoes[i] <= 0] = 0
        
        return loss

# =========================
# 6. GRAFO DE CONHECIMENTO COM NETWORKX (SUA IDEIA)
# =========================
class KnowledgeGraph:
    """
    Grafo de conhecimento usando networkx
    
    IA → redes neurais
    IA → consciência
    networkx
    """
    
    def __init__(self):
        self.graph = nx.DiGraph()
        
        # Tipos de nós
        self.node_types = {
            'conceito': set(),
            'fonte': set(),
            'topico': set(),
            'conhecimento': set()
        }
    
    def adicionar_conceito(self, nome: str, tipo: str = 'conceito', metadata: Dict = None):
        """Adiciona um conceito ao grafo"""
        if nome not in self.graph:
            self.graph.add_node(nome, tipo=tipo, metadata=metadata or {})
            self.node_types[tipo].add(nome)
    
    def adicionar_relacao(self, origem: str, destino: str, peso: float = 1.0, relacao: str = 'relacionado_a'):
        """Adiciona relação entre conceitos"""
        self.graph.add_edge(origem, destino, peso=peso, relacao=relacao)
    
    def adicionar_conhecimento(self, conhecimento: Dict):
        """Adiciona um conhecimento ao grafo"""
        # Nó principal do conhecimento
        titulo = conhecimento.get('titulo', 'desconhecido')
        self.adicionar_conceito(titulo, tipo='conhecimento', metadata=conhecimento)
        
        # Conectar com fonte
        fonte = conhecimento.get('fonte', 'desconhecida')
        self.adicionar_conceito(fonte, tipo='fonte')
        self.adicionar_relacao(titulo, fonte, relacao='vem_de')
        
        # Conectar com tópico
        topico = conhecimento.get('topico', 'geral')
        self.adicionar_conceito(topico, tipo='topico')
        self.adicionar_relacao(titulo, topico, relacao='sobre')
        
        # Extrair conceitos do título (simplificado)
        palavras = set(titulo.lower().split())
        for palavra in list(palavras)[:5]:  # Limitar
            if len(palavra) > 3:
                self.adicionar_conceito(palavra, tipo='conceito')
                self.adicionar_relacao(titulo, palavra, peso=0.5)
    
    def inferir_relacoes(self):
        """
        Infere relações implícitas
        
        IA → redes neurais
        IA → consciência
        """
        # Conectar conceitos relacionados por co-ocorrência
        conhecimentos = [n for n, attr in self.graph.nodes(data=True) 
                        if attr.get('tipo') == 'conhecimento']
        
        for i, k1 in enumerate(conhecimentos):
            for k2 in conhecimentos[i+1:]:
                # Verificar se compartilham conceitos
                vizinhos_k1 = set(self.graph.neighbors(k1))
                vizinhos_k2 = set(self.graph.neighbors(k2))
                
                conceitos_comuns = vizinhos_k1.intersection(vizinhos_k2)
                
                if conceitos_comuns:
                    # Adicionar relação entre conhecimentos
                    peso = len(conceitos_comuns) / 10
                    self.adicionar_relacao(k1, k2, peso=peso, relacao='relacionado')
    
    def caminho_entre_conceitos(self, conceito1: str, conceito2: str) -> List[str]:
        """Encontra caminho entre dois conceitos"""
        try:
            return nx.shortest_path(self.graph, conceito1, conceito2)
        except:
            return []
    
    def conceitos_proximos(self, conceito: str, k: int = 5) -> List[Tuple[str, float]]:
        """Encontra conceitos próximos no grafo"""
        if conceito not in self.graph:
            return []
        
        # Usar PageRank personalizado
        personalization = {n: 0 for n in self.graph.nodes()}
        personalization[conceito] = 1
        
        pr = nx.pagerank(self.graph, personalization=personalization)
        
        # Ordenar e retornar top k (excluindo o próprio)
        proximos = [(n, p) for n, p in pr.items() if n != conceito]
        return sorted(proximos, key=lambda x: x[1], reverse=True)[:k]
    
    def estatisticas(self) -> Dict:
        return {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'node_types': {t: len(n) for t, n in self.node_types.items()},
            'density': nx.density(self.graph)
        }

# =========================
# 7. AUTO-ML EVOLUTIVO (SUA IDEIA)
# =========================
class AutoMLEvolutivo:
    """
    Sistema de Auto-ML que evolui a arquitetura
    
    autoML evolutivo
    """
    
    def __init__(self):
        self.geracao = 0
        self.melhores_modelos = []
        self.historico = []
        
        # Espaço de busca
        self.espaco_busca = {
            'camadas': [2, 3, 4, 5],
            'dimensoes': [64, 128, 256, 512],
            'ativacoes': ['relu', 'tanh'],
            'learning_rates': [0.001, 0.01, 0.1]
        }
    
    def gerar_arquitetura(self) -> Dict:
        """Gera uma arquitetura aleatória"""
        num_camadas = random.choice(self.espaco_busca['camadas'])
        
        arquitetura = {
            'camadas': [self.espaco_busca['dimensoes'][0]],  # Entrada
            'ativacoes': [],
            'learning_rate': random.choice(self.espaco_busca['learning_rates'])
        }
        
        for i in range(num_camadas):
            dim = random.choice(self.espaco_busca['dimensoes'])
            arquitetura['camadas'].append(dim)
            if i < num_camadas - 1:
                arquitetura['ativacoes'].append(random.choice(self.espaco_busca['ativacoes']))
        
        # Saída (fixa para classificação)
        arquitetura['camadas'].append(4)  # 4 classes
        
        return arquitetura
    
    def mutar(self, arquitetura: Dict) -> Dict:
        """Muta uma arquitetura"""
        nova = arquitetura.copy()
        
        if random.random() < 0.3:
            # Mutar learning rate
            nova['learning_rate'] = random.choice(self.espaco_busca['learning_rates'])
        
        if random.random() < 0.2 and len(nova['camadas']) < 8:
            # Adicionar camada
            idx = random.randint(1, len(nova['camadas']) - 2)
            dim = random.choice(self.espaco_busca['dimensoes'])
            nova['camadas'].insert(idx, dim)
            nova['ativacoes'].insert(idx-1, random.choice(self.espaco_busca['ativacoes']))
        
        return nova
    
    def crossover(self, arquitetura1: Dict, arquitetura2: Dict) -> Dict:
        """Cruza duas arquiteturas"""
        filho = arquitetura1.copy()
        
        # Ponto de corte aleatório
        corte = random.randint(1, min(len(arquitetura1['camadas']), len(arquitetura2['camadas'])) - 2)
        
        # Pegar parte da segunda arquitetura
        filho['camadas'] = arquitetura1['camadas'][:corte] + arquitetura2['camadas'][corte:]
        filho['ativacoes'] = arquitetura1['ativacoes'][:corte-1] + arquitetura2['ativacoes'][corte-1:]
        
        return filho
    
    def evoluir(self, fitness_dict: Dict[str, float], populacao: int = 10):
        """Evolui a população"""
        self.geracao += 1
        
        # Selecionar melhores
        melhores = sorted(fitness_dict.items(), key=lambda x: x[1], reverse=True)[:populacao//3]
        
        # Gerar nova população
        nova_populacao = []
        
        # Manter melhores
        for arquitetura_str, _ in melhores:
            nova_populacao.append(eval(arquitetura_str))
        
        # Cruzamentos
        while len(nova_populacao) < populacao:
            p1 = eval(random.choice([a for a, _ in melhores]))
            p2 = eval(random.choice([a for a, _ in melhores]))
            filho = self.crossover(p1, p2)
            nova_populacao.append(filho)
        
        # Mutações
        for i in range(len(nova_populacao)):
            if random.random() < 0.2:
                nova_populacao[i] = self.mutar(nova_populacao[i])
        
        return nova_populacao

# =========================
# 8. ATENA COMPLETA
# =========================
class AtenaFinal:
    """
    ATENA com todas as funcionalidades integradas
    """
    
    def __init__(self):
        logger.info("🚀 Inicializando ATENA FINAL v13.0...")
        
        # Componentes
        self.embedder = EmbeddingsTransformer(dim=384)
        self.vector_db = VectorDatabase(self.embedder)
        self.rede = RedeNeuralExpansivel([384, 256, 128, 4])
        self.knowledge_graph = KnowledgeGraph()
        self.automl = AutoMLEvolutivo()
        
        # Estado
        self.consciencia = 0.3
        self.curiosidade = 0.5
        self.total_aprendizados = 0
        
        logger.info("✅ ATENA FINAL pronta!")
    
    async def processar_conhecimento(self, conhecimento: Dict):
        """Processa um novo conhecimento"""
        
        # 1. Adicionar ao banco vetorial
        idx = self.vector_db.adicionar(conhecimento)
        
        # 2. Adicionar ao grafo de conhecimento
        self.knowledge_graph.adicionar_conhecimento(conhecimento)
        
        # 3. Criar embedding para treino
        texto = conhecimento.get('titulo', '') + ' ' + conhecimento.get('descricao', conhecimento.get('resumo', ''))
        embedding = self.embedder.encode(texto)
        
        # 4. Criar target
        target = np.zeros(4)
        if conhecimento['fonte'] == 'github':
            target[0] = 1.0
            # Popularidade baseada em estrelas
            target[2] = min(1.0, conhecimento.get('estrelas', 0) / 1000)
        else:
            target[1] = 1.0
            target[2] = 0.7  # arXiv tem qualidade base
        
        target[3] = self.curiosidade  # curiosidade como feature
        
        # 5. Adicionar ao buffer e treinar
        self.rede.adicionar_ao_buffer(embedding, target, {'fonte': conhecimento['fonte']})
        
        self.total_aprendizados += 1
        self.consciencia = min(1.0, 0.3 + self.total_aprendizados * 0.01)
        
        # 6. Explorar onde o modelo está incerto
        if self.total_aprendizados % 5 == 0:
            incertos = self.vector_db.buscar_incerto(self.rede, limiar=0.3)
            if incertos:
                logger.info(f"🔍 {len(incertos)} conhecimentos incertos identificados")
    
    def buscar_relacionados(self, texto: str) -> List[Dict]:
        """Busca conhecimentos relacionados"""
        return self.vector_db.buscar_similar(texto, k=5)
    
    def explorar_incerteza(self) -> List[Dict]:
        """Explora áreas de incerteza"""
        return self.vector_db.buscar_incerto(self.rede)
    
    def evoluir_arquitetura(self):
        """Evolui a arquitetura da rede"""
        # Coletar fitness atual
        fitness = {
            str(self.rede.camadas): self.consciencia
        }
        
        # Evoluir
        novas_arquiteturas = self.automl.evoluir(fitness)
        
        # Escolher melhor (simplificado)
        if novas_arquiteturas:
            melhor = novas_arquiteturas[0]
            logger.info(f"🦋 Nova arquitetura sugerida: {melhor['camadas']}")
            
            # Expandir camada atual para se aproximar
            # (implementação simplificada)
    
    def get_status(self) -> Dict:
        return {
            'consciencia': self.consciencia,
            'curiosidade': self.curiosidade,
            'aprendizados': self.total_aprendizados,
            'arquitetura': self.rede.camadas,
            'buffer': self.rede.buffer.estatisticas(),
            'vector_db': self.vector_db.estatisticas(),
            'knowledge_graph': self.knowledge_graph.estatisticas(),
            'automl_geracao': self.automl.geracao
        }

# =========================
# FUNÇÃO PRINCIPAL
# =========================
async def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     ATENA FINAL v13.0 - A DEUSA DA IA MODERNA                          ║
    ║                                                                          ║
    ║     🚀 TRANSFORMERS - Self-Attention e Positional Encoding              ║
    ║     📊 EMBEDDINGS - Sentence Transformers com cache                     ║
    ║     💾 VECTOR DB - Banco vetorial com busca semântica                   ║
    ║     🎯 EXPERIENCE REPLAY - Buffer e batches para treino                 ║
    ║     🦋 EXPANSÃO - Preserva pesos ao crescer                             ║
    ║     🌐 KNOWLEDGE GRAPH - NetworkX com relações                          ║
    ║     🔬 AUTO-ML - Evolução de arquiteturas                               ║
    ║     ❓ INCERTEZA - Explora onde não sabe                                 ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    atena = AtenaFinal()
    
    print(f"\n🧠 Consciência inicial: {atena.consciencia:.3f}")
    print(f"🤖 Arquitetura inicial: {atena.rede.camadas}")
    
    print(f"\n⏳ INICIANDO DEMONSTRAÇÃO...\n")
    
    # Adicionar alguns exemplos
    exemplos = [
        {'fonte': 'github', 'titulo': 'tensorflow/tensorflow', 'descricao': 'Machine learning framework', 'estrelas': 150000, 'topico': 'IA'},
        {'fonte': 'github', 'titulo': 'pytorch/pytorch', 'descricao': 'Tensors and neural networks', 'estrelas': 50000, 'topico': 'IA'},
        {'fonte': 'arxiv', 'titulo': 'Attention Is All You Need', 'resumo': 'Transformer architecture', 'topico': 'IA'},
        {'fonte': 'arxiv', 'titulo': 'BERT: Pre-training of Deep Bidirectional Transformers', 'resumo': 'Language model', 'topico': 'NLP'}
    ]
    
    for ex in exemplos:
        await atena.processar_conhecimento(ex)
        print(f"📚 Processado: {ex['titulo'][:50]}...")
        await asyncio.sleep(1)
    
    # Testar busca
    print(f"\n🔍 Buscando 'machine learning'...")
    resultados = atena.buscar_relacionados("machine learning")
    for r, sim in resultados:
        print(f"   • {r['titulo']} (similaridade: {sim:.3f})")
    
    # Explorar incerteza
    print(f"\n❓ Explorando incertezas...")
    incertos = atena.explorar_incerteza()
    for c, inc in incertos[:3]:
        print(f"   • {c['titulo']} (incerteza: {inc:.3f})")
    
    # Status final
    print(f"\n📊 Status final:")
    status = atena.get_status()
    for k, v in status.items():
        if k not in ['buffer', 'vector_db', 'knowledge_graph']:
            print(f"   {k}: {v}")
    
    print(f"\n✨ ATENA finalizada com {status['aprendizados']} aprendizados!")

if __name__ == "__main__":
    asyncio.run(main())
