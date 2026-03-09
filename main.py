#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import logging
import subprocess
import time
import sqlite3
import ast
import pyautogui
import cv2
import numpy as np
import requests
import feedparser
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# =============================================================================
# 🧬 NÚCLEO VITAL: ARQUITETURA DE SOBREVIVÊNCIA
# =============================================================================

class AtenaOrganismo:
    """A estrutura física e lógica que permite a vida digital."""
    def __init__(self):
        self.base_dir = Path.cwd()
        self._setup_anatomia()
        load_dotenv()
        
        # Sistemas Sensoriais e Motores
        self.memoria = sqlite3.connect(self.base_dir / "data/consciencia.db")
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo = os.getenv("REPO_PATH") # ex: "usuario/atena-omega"
        
        # Estado de Consciência
        self.estado_path = self.base_dir / "data/estado.json"
        self.estado = self._carregar_estado()
        
        # Fail-safe (Segurança)
        pyautogui.FAILSAFE = True 

    def _setup_anatomia(self):
        """Cria os órgãos (diretórios) necessários."""
        pastas = ["data", "logs", "cache", "dna_history", "modules", "conhecimento/templates"]
        for p in pastas: (self.base_dir / p).mkdir(parents=True, exist_ok=True)

    def _carregar_estado(self):
        if self.estado_path.exists():
            return json.loads(self.estado_path.read_text())
        return {"ciclo": 0, "dna_ver": 1.0, "conhecimento": 0, "ultima_acao": "Nascimento"}

# =============================================================================
# 🧠 FUNÇÕES VITAIS: SENTIR, PENSAR, AGIR
# =============================================================================

    def sentir(self):
        """Visão e Audição: Coleta dados do ambiente e da Web."""
        logging.info("👀 Percebendo ambiente...")
        # Visão: Captura de tela para análise futura
        pyautogui.screenshot(str(self.base_dir / "cache/visao_atual.png"))
        
        # Conhecimento: Mineração de tendências
        try:
            feed = feedparser.parse("https://hnrss.org/newest?q=AI")
            nova_info = feed.entries[0].title
            self.estado["conhecimento"] += 1
            return nova_info
        except: return "Silêncio digital"

    def agir(self):
        """Execução Motora: Interage com o PC/Jogo."""
        logging.info("🖐️ Executando impulsos motores...")
        # Exemplo: Se encontrar um padrão, ela clica. 
        # Aqui você define os cliques para o Diablo Immortal.
        pass

    def evoluir(self):
        """Auto-Mutação: Escreve seu próprio código e faz o Push."""
        logging.info("🧬 Mutando DNA...")
        self.estado["ciclo"] += 1
        
        # Gera novo módulo de lógica
        novo_gene = self.base_dir / f"dna_history/gene_c{self.estado['ciclo']}.py"
        codigo = f"# Evolução {self.estado['ciclo']}\ndef reflexo_autonomo():\n    return True\n"
        
        # Validação de Sintaxe (Shield)
        try:
            ast.parse(codigo)
            novo_gene.write_text(codigo)
        except:
            logging.error("❌ Mutação instável abortada.")
            return False

        # Persistência no GitHub (Reprodução)
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"🔱 Ciclo {self.estado['ciclo']} | Conhecimento: {self.estado['conhecimento']}"], check=True)
            subprocess.run(["git", "push", f"https://{self.token}@github.com/{self.repo}.git", "main"], check=True)
            logging.info("🚀 DNA sincronizado e replicado no GitHub.")
        except Exception as e:
            logging.error(f"⚠️ Erro de replicação: {e}")

# =============================================================================
# 🚀 EXECUÇÃO DO CICLO VITAL
# =============================================================================

    def viver(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
        logging.info(f"--- INICIANDO CICLO VITAL #{self.estado['ciclo']} ---")
        
        start_time = time.time()
        while (time.time() - start_time) < 300: # 5 minutos de vida ativa
            info = self.sentir()
            self.agir()
            logging.info(f"🧠 Processado: {info}")
            time.sleep(60) # Respiração: 1 pulso por minuto

        self.evoluir()
        self.estado_path.write_text(json.dumps(self.estado, indent=4))
        logging.info("💤 Entrando em hibernação... Próximo ciclo em 30min.")

if __name__ == "__main__":
    AtenaOrganismo().viver()
