#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - ATENA MUNDUS v46.2    ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DO MUNDO"         ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                               ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ MAPAS PNG REAIS          ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ TODOS OS MODOS           ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ⚡ COMPATÍVEL COM CI/CD    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import uuid
import random
import math
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple, Set
import logging
from collections import defaultdict, deque

# =========================
# BIBLIOTECAS PARA MAPAS
# =========================
try:
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.colors import LinearSegmentedColormap
    from PIL import Image, ImageDraw, ImageFont
    IMPORT_SUCCESS = True
except ImportError as e:
    print(f"❌ Erro: {e}")
    print("📦 Instale as dependências: pip install numpy matplotlib pillow")
    IMPORT_SUCCESS = False
    sys.exit(1)

# =========================
# CONFIGURAÇÕES DO MUNDO
# =========================
__version__ = "46.2"
__nome__ = "ATENA MUNDUS"

BASE_DIR = Path(__file__).parent / "mundus_atena"

class Config:
    BASE_DIR = BASE_DIR
    MAPAS_DIR = BASE_DIR / "mapas"
    CRONICAS_DIR = BASE_DIR / "cronicas"
    DADOS_DIR = BASE_DIR / "dados"
    
    # Dimensões do mapa
    MAPA_LARGURA = 2000
    MAPA_ALTURA = 1000
    RESOLUCAO = 100
    
    # Configurações climáticas
    TEMPERATURA_BASE = 20
    VARIACAO_SAZONAL = 15
    
    # Placas tectônicas
    NUM_PLACAS = 12
    VELOCIDADE_TECTONICA = 0.01
    
    # Ciclos históricos
    ANOS_POR_ERA = 1000
    NUM_ERAS = 20
    
    # Criar diretórios
    for dir_path in [BASE_DIR, MAPAS_DIR, CRONICAS_DIR, DADOS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('ATENA-MUNDUS')

# =========================
# GERADOR DE MAPAS CLIMÁTICOS
# =========================
class MapaClimatico:
    """Gera mapas climáticos realistas usando Matplotlib"""
    
    def __init__(self, largura: int = Config.MAPA_LARGURA, altura: int = Config.MAPA_ALTURA):
        self.largura = largura
        self.altura = altura
        self.matriz_clima = np.zeros((altura, largura))
        self.matriz_altitude = np.zeros((altura, largura))
        self.matriz_recursos = np.zeros((altura, largura))
        self.placas = []
        
    def gerar_relevo(self):
        """Gera relevo usando ruído de Perlin simplificado"""
        logger.info("🏔️ Gerando relevo...")
        
        for y in range(self.altura):
            for x in range(self.largura):
                nx = x / self.largura * 10
                ny = y / self.altura * 10
                
                z1 = math.sin(nx * 0.5) * math.cos(ny * 0.5)
                z2 = math.sin(nx * 2.0) * math.cos(ny * 2.0) * 0.3
                z3 = math.sin(nx * 5.0) * math.cos(ny * 5.0) * 0.1
                
                altitude = (z1 + z2 + z3 + 1) / 2
                
                dist_centro = ((nx-5)**2 + (ny-5)**2)**0.5
                if dist_centro < 2:
                    altitude += 0.3
                
                self.matriz_altitude[y, x] = min(1.0, altitude)
    
    def gerar_clima(self):
        """Gera clima baseado em latitude e altitude"""
        logger.info("🌡️ Gerando clima...")
        
        for y in range(self.altura):
            lat = 1 - (y / self.altura)
            
            for x in range(self.largura):
                altitude = self.matriz_altitude[y, x]
                temp_base = Config.TEMPERATURA_BASE * lat
                temp = temp_base - (altitude * 20)
                dist_mar = self._calcular_dist_mar(x, y)
                umidade = max(0, 1 - dist_mar/500)
                
                if altitude < 0.2:
                    bioma = 0  # Oceano
                elif temp < -10:
                    bioma = 1  # Glacial
                elif temp < 0:
                    bioma = 2  # Tundra
                elif umidade < 0.3:
                    bioma = 3  # Deserto
                elif umidade < 0.6:
                    bioma = 4  # Savana
                elif temp > 25 and umidade > 0.7:
                    bioma = 5  # Floresta tropical
                elif temp > 15:
                    bioma = 6  # Floresta temperada
                else:
                    bioma = 7  # Taiga
                
                self.matriz_clima[y, x] = bioma
    
    def _calcular_dist_mar(self, x: int, y: int) -> float:
        """Calcula distância até o mar mais próximo"""
        raio = 50
        for r in range(1, raio):
            for dx in [-r, 0, r]:
                for dy in [-r, 0, r]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.largura and 0 <= ny < self.altura:
                        if self.matriz_altitude[ny, nx] < 0.2:
                            return r
        return raio
    
    def gerar_recursos(self):
        """Distribui recursos naturais"""
        logger.info("⛏️ Distribuindo recursos...")
        
        for y in range(self.altura):
            for x in range(self.largura):
                bioma = self.matriz_clima[y, x]
                altitude = self.matriz_altitude[y, x]
                
                recursos = 0
                
                if bioma == 3 and random.random() < 0.01:
                    recursos = 3  # Petróleo
                elif bioma == 5 and random.random() < 0.05:
                    recursos = 2  # Borracha
                elif altitude > 0.8 and random.random() < 0.1:
                    recursos = 4  # Minerais
                elif altitude < 0.2 and random.random() < 0.2:
                    recursos = 1  # Peixes
                
                self.matriz_recursos[y, x] = recursos
    
    def gerar_placas_tectonicas(self):
        """Gera placas tectônicas"""
        logger.info("🧩 Gerando placas tectônicas...")
        
        centros = []
        for _ in range(Config.NUM_PLACAS):
            x = random.randint(0, self.largura-1)
            y = random.randint(0, self.altura-1)
            centros.append((x, y))
        
        self.matriz_placas = np.zeros((self.altura, self.largura), dtype=int)
        
        for y in range(self.altura):
            for x in range(self.largura):
                dist_min = float('inf')
                placa_idx = 0
                
                for i, (cx, cy) in enumerate(centros):
                    dist = ((cx-x)**2 + (cy-y)**2)**0.5
                    if dist < dist_min:
                        dist_min = dist
                        placa_idx = i
                
                self.matriz_placas[y, x] = placa_idx
    
    def salvar_mapa_png(self, nome: str, ano: int) -> Path:
        """Salva o mapa como PNG real"""
        logger.info(f"💾 Salvando mapa {nome} ano {ano}...")
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 10))
        fig.suptitle(f'Mundo de Atena - Ano {ano}', fontsize=16)
        
        # Mapa de altitude
        im1 = axes[0, 0].imshow(self.matriz_altitude, cmap='terrain', aspect='auto')
        axes[0, 0].set_title('Relevo')
        plt.colorbar(im1, ax=axes[0, 0])
        
        # Mapa climático
        cmap_clima = LinearSegmentedColormap.from_list('clima', 
            ['blue', 'white', 'brown', 'yellow', 'green', 'darkgreen', 'lightgreen', 'gray'])
        im2 = axes[0, 1].imshow(self.matriz_clima, cmap=cmap_clima, aspect='auto')
        axes[0, 1].set_title('Biomas')
        
        # Mapa de recursos
        im3 = axes[1, 0].imshow(self.matriz_recursos, cmap='hot', aspect='auto')
        axes[1, 0].set_title('Recursos Naturais')
        plt.colorbar(im3, ax=axes[1, 0])
        
        # Legenda
        axes[1, 1].axis('off')
        legendas = [
            '🌊 Oceano', '❄️ Glacial', '🏔️ Tundra', '🏜️ Deserto',
            '🌾 Savana', '🌴 Fl. Tropical', '🌳 Fl. Temperada', '🌲 Taiga'
        ]
        for i, leg in enumerate(legendas):
            axes[1, 1].text(0.1, 0.9 - i*0.1, leg, fontsize=10)
        
        plt.tight_layout()
        
        arquivo = Config.MAPAS_DIR / f"{nome}_ano_{ano}.png"
        plt.savefig(arquivo, dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"✅ Mapa salvo: {arquivo}")
        return arquivo

# =========================
# EVENTOS GLOBAIS
# =========================
class EventoGlobal:
    """Eventos que afetam todo o mundo"""
    
    def __init__(self, tipo: str, ano: int, intensidade: float):
        self.id = uuid.uuid4().hex[:8]
        self.tipo = tipo
        self.ano = ano
        self.intensidade = intensidade
        self.duracao = self._calcular_duracao()
        self.afetados = []
        
    def _calcular_duracao(self) -> int:
        duracoes = {
            'idade_do_gelo': random.randint(1000, 5000),
            'super_vulcao': random.randint(5, 20),
            'meteorito': 1,
            'pandemia': random.randint(10, 50),
            'era_glacial': random.randint(500, 2000),
            'aquecimento': random.randint(100, 500)
        }
        return duracoes.get(self.tipo, 100)
    
    def aplicar(self, mundo):
        if self.tipo == 'idade_do_gelo':
            mundo.temperatura_global -= 10 * self.intensidade
        elif self.tipo == 'super_vulcao':
            mundo.luminosidade *= (1 - self.intensidade * 0.5)
        elif self.tipo == 'meteorito':
            x = random.randint(0, mundo.largura-1)
            y = random.randint(0, mundo.altura-1)
            mundo.crateras.append((x, y, self.intensidade))
            mundo.temperatura_global -= 5 * self.intensidade
        elif self.tipo == 'pandemia':
            mundo.mortalidade += 0.1 * self.intensidade

# =========================
# CIVILIZAÇÃO COM DIVISÃO
# =========================
class Civilizacao:
    def __init__(self, nome: str, x: int, y: int, ano: int, cultura: str):
        self.id = uuid.uuid4().hex[:8]
        self.nome = nome
        self.x = x
        self.y = y
        self.ano_fundacao = ano
        self.cultura = cultura
        self.populacao = random.randint(1000, 5000)
        self.tecnologia = 1.0
        self.economia = 1000
        self.feliz = 0.5
        
        self.cidades = []
        self.exercito = 100
        self.aliados = []
        self.inimigos = []
        self.cronicas = []
        
        self._registrar(f"🏛️ Fundação de {nome}")
    
    def _registrar(self, evento: str):
        self.cronicas.append({
            'ano': datetime.now().year,
            'evento': evento
        })
    
    def evoluir(self, ano: int):
        self.populacao += int(self.populacao * random.uniform(0.01, 0.03))
        
        if random.random() < 0.01:
            self.tecnologia += 0.1
            self._registrar(f"🔬 Avanço tecnológico: nível {self.tecnologia:.1f}")
        
        if random.random() < 0.02:
            self._evento_aleatorio()
    
    def _evento_aleatorio(self):
        eventos = [
            f"Descoberta de novo território",
            f"Revolta camponesa",
            f"Grande colheita",
            f"Epidemia local",
            f"Tratado comercial",
            f"Aliança matrimonial"
        ]
        self._registrar(random.choice(eventos))
    
    def dividir(self, novo_nome: str, ano: int):
        logger.info(f"🔄 {self.nome} se divide: surge {novo_nome}")
        
        filha = Civilizacao(
            novo_nome,
            self.x + random.randint(-100, 100),
            self.y + random.randint(-100, 100),
            ano,
            f"{self.cultura}_derivada"
        )
        
        filha.populacao = self.populacao // 2
        filha.tecnologia = self.tecnologia
        filha.economia = self.economia // 2
        
        self.populacao //= 2
        self.economia //= 2
        
        self._registrar(f"✂️ Divisão: surge {novo_nome}")
        filha._registrar(f"🌟 Fundada a partir de {self.nome}")
        
        return filha

# =========================
# MUNDO COMPLETO
# =========================
class Mundo:
    """Mundo completo com mapas, clima e civilizações"""
    
    def __init__(self, nome: str, modo: str = 'completo', anos_simulacao: int = 20000):
        self.nome = nome
        self.criacao = datetime.now()
        self.ano_atual = 0
        self.anos_simulacao = anos_simulacao
        self.modo = modo
        self.eras = []
        
        self.largura = Config.MAPA_LARGURA
        self.altura = Config.MAPA_ALTURA
        
        self.temperatura_global = Config.TEMPERATURA_BASE
        self.luminosidade = 1.0
        self.mortalidade = 0.01
        
        self.mapa = MapaClimatico()
        self.mapa.gerar_relevo()
        self.mapa.gerar_clima()
        self.mapa.gerar_recursos()
        self.mapa.gerar_placas_tectonicas()
        
        self.civilizacoes = []
        self.eventos = []
        self.crateras = []
        
        logger.info(f"\n{'='*70}")
        logger.info(f"🌍 MUNDO: {self.nome} (modo: {modo})")
        logger.info(f"{'='*70}")
    
    def criar_era(self, nome: str, inicio: int, fim: int):
        era = {
            'nome': nome,
            'inicio': inicio,
            'fim': fim,
            'eventos': []
        }
        self.eras.append(era)
        logger.info(f"📅 Era {nome}: {inicio}-{fim}")
    
    def gerar_evento_global(self):
        if random.random() < 0.01:
            tipo = random.choice([
                'idade_do_gelo', 'super_vulcao', 'meteorito', 'pandemia'
            ])
            intensidade = random.uniform(0.5, 1.5)
            
            evento = EventoGlobal(tipo, self.ano_atual, intensidade)
            evento.aplicar(self)
            self.eventos.append(evento)
    
    def criar_civilizacao_inicial(self, ano: int):
        num_civs = random.randint(3, 6)
        
        for i in range(num_civs):
            x = random.randint(100, self.largura-100)
            y = random.randint(100, self.altura-100)
            cultura = random.choice(['latina', 'grega', 'egípcia', 'persa', 'chinesa'])
            
            civ = Civilizacao(f"Civ{i+1}", x, y, ano, cultura)
            self.civilizacoes.append(civ)
            logger.info(f"🏛️ {civ.nome} fundada em ({x}, {y})")
    
    def simular_ano(self, ano: int):
        self.ano_atual = ano
        
        self.gerar_evento_global()
        
        for civ in self.civilizacoes[:]:
            civ.evoluir(ano)
            
            if random.random() < 0.001 and ano - civ.ano_fundacao > 500:
                nova = civ.dividir(f"{civ.nome}_Filha", ano)
                self.civilizacoes.append(nova)
            
            if random.random() < self.mortalidade / 100:
                logger.info(f"⚰️ {civ.nome} é extinta")
                self.civilizacoes.remove(civ)
    
    def gerar_mapa_ano(self, ano: int) -> Path:
        return self.mapa.salvar_mapa_png(self.nome, ano)
    
    def gerar_linha_tempo(self) -> str:
        linhas = []
        linhas.append(f"\n{'='*70}")
        linhas.append(f"📜 LINHA DO TEMPO DE {self.nome.upper()}")
        linhas.append(f"{'='*70}\n")
        
        for era in self.eras:
            linhas.append(f"\n📅 {era['nome']} ({era['inicio']}-{era['fim']}):")
            
            eventos_era = [e for e in self.eventos 
                          if era['inicio'] <= e.ano <= era['fim']]
            
            for evento in eventos_era[:5]:
                linhas.append(f"   • {evento.ano}: {evento.tipo} "
                            f"(intensidade: {evento.intensidade:.1f})")
        
        linhas.append(f"\n🏛️ CIVILIZAÇÕES NO ANO {self.ano_atual}:")
        for civ in self.civilizacoes:
            idade = self.ano_atual - civ.ano_fundacao
            linhas.append(f"   • {civ.nome}: {civ.populacao:,} habitantes, "
                         f"tecnologia {civ.tecnologia:.1f}, {idade} anos")
        
        return '\n'.join(linhas)
    
    def salvar_mundo(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        mapa_file = self.gerar_mapa_ano(self.ano_atual)
        
        timeline_file = Config.CRONICAS_DIR / f"timeline_{timestamp}.txt"
        with open(timeline_file, 'w', encoding='utf-8') as f:
            f.write(self.gerar_linha_tempo())
        
        dados_file = Config.DADOS_DIR / f"civilizacoes_{timestamp}.json"
        with open(dados_file, 'w', encoding='utf-8') as f:
            json.dump([{
                'nome': c.nome,
                'populacao': c.populacao,
                'tecnologia': c.tecnologia,
                'economia': c.economia,
                'ano_fundacao': c.ano_fundacao,
                'cronicas': c.cronicas[-10:]
            } for c in self.civilizacoes], f, indent=2, default=str)
        
        logger.info(f"💾 Mundo salvo em {Config.BASE_DIR}")
        
        return {
            'mapa': mapa_file,
            'timeline': timeline_file,
            'dados': dados_file
        }

# =========================
# MAIN (VERSÃO CI/CD)
# =========================
def main():
    # Parse argumentos da linha de comando
    parser = argparse.ArgumentParser(description='ATENA MUNDUS - Gerador de Mundos')
    parser.add_argument('--modo', type=str, default='completo',
                       choices=['completo', 'rapido', 'teste', 'civilizacao'],
                       help='Modo de simulação (civilizacao = modo rápido para testes)')
    parser.add_argument('--anos', type=int, default=20000,
                       help='Número de anos para simular')
    parser.add_argument('--populacao', type=int, default=20,
                       help='População inicial')
    parser.add_argument('--sem-input', action='store_true', default=True,
                       help='Modo sem input (para CI/CD)')
    
    args = parser.parse_args()
    
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - MUNDUS v46.2     ║
    ║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║    "A DEUSA DO MUNDO"    ║
    ║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║                           ║
    ║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║   ⚡ MAPAS PNG REAIS      ║
    ║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║   ⚡ TODOS OS MODOS       ║
    ║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═ COMPATÍVEL COM CI/CD ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    🌍 GERANDO MUNDO REAL COM:
    ├── 🏔️ Relevo com placas tectônicas
    ├── 🌡️ Clima por latitude e altitude
    ├── ⛏️ Recursos naturais distribuídos
    ├── 🌋 Eventos globais (idade do gelo, vulcões, meteoros)
    ├── 🏛️ Civilizações que nascem, evoluem e se dividem
    ├── 🗺️ Mapas PNG em alta resolução
    └── 📜 Crônicas detalhadas
    
    ⏱️  Simulando {args.anos} anos de história...
    """)
    
    # Ajustar anos baseado no modo
    if args.modo == 'teste':
        args.anos = 100
        logger.info("🧪 Modo teste ativado - simulando apenas 100 anos")
    elif args.modo == 'rapido' or args.modo == 'civilizacao':
        args.anos = 1000
        logger.info("⚡ Modo rápido ativado - simulando 1000 anos")
    else:
        logger.info(f"🐢 Modo completo - simulando {args.anos} anos")
    
    # Criar mundo
    mundo = Mundo("Aethelgard", args.modo, args.anos)
    
    # Criar eras proporcionais
    quinto = args.anos // 5
    mundo.criar_era("Era Primordial", 0, quinto)
    mundo.criar_era("Era dos Despertar", quinto + 1, quinto * 2)
    mundo.criar_era("Era dos Impérios", quinto * 2 + 1, quinto * 3)
    mundo.criar_era("Era das Crises", quinto * 3 + 1, quinto * 4)
    mundo.criar_era("Era da Reconstrução", quinto * 4 + 1, args.anos)
    
    # Criar primeiras civilizações
    mundo.criar_civilizacao_inicial(args.anos // 4)
    
    # Simular anos
    for ano in range(1, args.anos + 1):
        mundo.simular_ano(ano)
        
        # Gerar mapas em intervalos apropriados
        if args.modo == 'teste':
            intervalo = 10
        elif args.modo in ['rapido', 'civilizacao']:
            intervalo = 100
        else:
            intervalo = 5000
            
        if ano % intervalo == 0 or ano == args.anos:
            mundo.gerar_mapa_ano(ano)
            logger.info(f"📊 Ano {ano}/{args.anos} - {len(mundo.civilizacoes)} civilizações")
    
    # Salvar estado final
    arquivos = mundo.salvar_mundo()
    
    # Mostrar linha do tempo resumida
    print(mundo.gerar_linha_tempo())
    
    print(f"\n{'='*70}")
    print(f"✅ Mundo gerado com sucesso!")
    print(f"📁 Arquivos salvos em: {Config.BASE_DIR}")
    print(f"🗺️ Mapa final: {arquivos['mapa']}")
    print(f"📜 Linha do tempo: {arquivos['timeline']}")
    print(f"📊 Dados: {arquivos['dados']}")
    print(f"\n📊 Estatísticas finais:")
    print(f"   • Anos simulados: {args.anos}")
    print(f"   • Civilizações ativas: {len(mundo.civilizacoes)}")
    print(f"   • Eventos globais: {len(mundo.eventos)}")
    print(f"   • Mapas gerados: {args.anos // intervalo + 1}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Mundo interrompido")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
