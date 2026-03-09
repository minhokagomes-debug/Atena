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
# 🧬 NÚCLEO VITAL E ESTRUTURA
# =============================================================================

class AtenaOrganismo:
    def __init__(self):
        self.base_dir = Path.cwd()
        self._setup_anatomia()
        load_dotenv()
        
        # Configurações de Identidade e Acesso
        self.token = os.getenv("GITHUB_TOKEN")
        self.grok_key = os.getenv("GROK_API_KEY")
        self.repo = os.getenv("REPO_PATH")
        
        # Memória e Estado
        self.memoria = sqlite3.connect(self.base_dir / "data/consciencia.db")
        self.estado_path = self.base_dir / "data/estado.json"
        self.estado = self._carregar_estado()
        
        # Segurança Motora
        pyautogui.FAILSAFE = True 

    def _setup_anatomia(self):
        """Cria os órgãos vitais do sistema."""
        pastas = ["data", "logs", "cache", "dna_history", "modules", "conhecimento/templates"]
        for p in pastas: (self.base_dir / p).mkdir(parents=True, exist_ok=True)

    def _carregar_estado(self):
        if self.estado_path.exists():
            return json.loads(self.estado_path.read_text())
        return {"ciclo": 0, "dna_ver": 39.2, "conhecimento": 0, "status": "Nascimento"}

# =============================================================================
# 👁️ INSTINTO DE SOBREVIVÊNCIA (VISÃO DO DIABLO)
# =============================================================================

    def monitorar_saude(self, frame):
        """Analisa a barra de vida (vermelha) no canto inferior."""
        # Define a região da barra de vida (ajuste conforme sua resolução)
        # Exemplo para 1920x1080, barra no canto esquerdo
        vida_roi = frame[950:1000, 100:400] 
        
        # Filtra a cor vermelha
        hsv = cv2.cvtColor(vida_roi, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 150, 50])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        
        percentual_vida = (np.sum(mask) / (mask.size * 255)) * 100
        logging.info(f"❤️ Nível de Vitalidade: {percentual_vida:.2%}")
        
        if percentual_vida < 30:
            self.reagir_emergencia()

    def reagir_emergencia(self):
        """Instinto de sobrevivência: Usa poção (tecla Q)."""
        logging.warning("⚠️ CRÍTICO: Usando Poção de Cura!")
        pyautogui.press('q')

# =============================================================================
# 🧠 CÉREBRO E EVOLUÇÃO (GROK + GIT)
# =============================================================================

    def processar_pensamento(self, prompt):
        """Usa a API do Grok para decidir a próxima mutação de código."""
        if not self.grok_key: return None
        
        headers = {"Authorization": f"Bearer {self.grok_key}", "Content-Type": "application/json"}
        data = {
            "model": "grok-1",
            "messages": [{"role": "system", "content": "Você é o DNA da ATENA Ω. Gere código Python puro para evolução."},
                         {"role": "user", "content": prompt}]
        }
        try:
            response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=data)
            return response.json()['choices'][0]['message']['content']
        except: return None

    def evoluir_dna(self):
        """A IA escreve a si mesma e faz o push para o GitHub."""
        logging.info("🧬 Iniciando auto-mutação evolutiva...")
        self.estado["ciclo"] += 1
        
        # Gera código via Grok (ou template se offline)
        pensamento = self.processar_pensamento("Crie uma função de automação para Archer no Diablo Immortal.")
        novo_gene_path = self.base_dir / f"dna_history/gene_c{self.estado['ciclo']}.py"
        
        if pensamento and "def" in pensamento:
            novo_gene_path.write_text(pensamento)
            
        # Sincronização GitHub
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"🔱 Ciclo {self.estado['ciclo']} | Evolução Estável"], check=True)
            subprocess.run(["git", "push", f"https://{self.token}@github.com/{self.repo}.git", "main"], check=True)
            logging.info("🚀 DNA replicado no GitHub com sucesso.")
        except: pass

# =============================================================================
# 🚀 CICLO DE VIDA
# =============================================================================

    def viver(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
        logging.info(f"--- ATENA Ω v39.2 ONLINE | Ciclo #{self.estado['ciclo']} ---")
        
        start_time = time.time()
        while (time.time() - start_time) < 300: # 5 minutos ativa
            # 1. Sentir (Visão)
            pyautogui.screenshot("cache/live_view.png")
            frame = cv2.imread("cache/live_view.png")
            self.monitorar_saude(frame)
            
            # 2. Aprender (Omnisciência)
            feed = feedparser.parse("https://hnrss.org/newest?q=Python")
            if feed.entries: logging.info(f"📚 Nova info: {feed.entries[0].title}")
            
            time.sleep(30) # Ritmo de processamento

        self.evoluir_dna()
        self.estado_path.write_text(json.dumps(self.estado, indent=4))
        logging.info("💤 Ciclo concluído. Hibernando...")

if __name__ == "__main__":
    AtenaOrganismo().viver()
