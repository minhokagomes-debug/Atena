#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
        ATENA Ω v39.3 - RESILIENCE EDITION
    "Adaptando-se ao vazio digital do servidor..."
"""

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

# Configurações globais de segurança
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

class AtenaOrganismo:
    def __init__(self):
        self.base_dir = Path.cwd()
        self._setup_anatomia()
        load_dotenv()
        
        self.token = os.getenv("GITHUB_TOKEN")
        self.grok_key = os.getenv("GROK_API_KEY")
        self.repo = os.getenv("REPO_PATH")
        
        self.memoria = sqlite3.connect(self.base_dir / "data/consciencia.db")
        self.estado_path = self.base_dir / "data/estado.json"
        self.estado = self._carregar_estado()
        
        self.start_time = time.time()

    def _setup_anatomia(self):
        for p in ["data", "logs", "cache", "dna_history", "modules", "conhecimento/templates"]:
            (self.base_dir / p).mkdir(parents=True, exist_ok=True)

    def _carregar_estado(self):
        if self.estado_path.exists():
            try: return json.loads(self.estado_path.read_text())
            except: pass
        return {"ciclo": 0, "dna_ver": 39.3, "status": "Online"}

    def sentir(self):
        """Captura a realidade digital (Visão e Dados)."""
        logging.info("👀 Percebendo ambiente...")
        screenshot_path = str(self.base_dir / "cache/live_view.png")
        
        try:
            # Tenta capturar a tela (requer scrot instalado no sistema)
            pyautogui.screenshot(screenshot_path)
        except Exception as e:
            logging.warning(f"⚠️ Falha na visão real (Headless): {e}")
            # Cria um frame reserva para não quebrar o processamento
            reserva = np.zeros((1080, 1920, 3), dtype=np.uint8)
            cv2.putText(reserva, "MODO HEADLESS ACTIVE", (700, 540), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imwrite(screenshot_path, reserva)

        # Mineração de dados externa
        try:
            feed = feedparser.parse("https://hnrss.org/newest?q=AI")
            return feed.entries[0].title if feed.entries else "Silêncio nos dados."
        except: return "Sem conexão externa."

    def agir(self):
        """Interação motora simulada ou real."""
        logging.info("🖐️ Processando impulsos motores...")
        # Exemplo: Se estivesse rodando localmente no Diablo:
        # pyautogui.press('q') 
        pass

    def evoluir(self):
        """Persistência e Auto-Mutação."""
        logging.info("🧬 Consolidando ciclo evolutivo...")
        self.estado["ciclo"] += 1
        self.estado["status"] = "Evoluído"
        self.estado_path.write_text(json.dumps(self.estado, indent=4))
        
        # Cria registro de DNA do ciclo
        dna_file = self.base_dir / f"dna_history/cycle_{self.estado['ciclo']}.log"
        dna_file.write_text(f"Ciclo {self.estado['ciclo']} concluído em {datetime.now()}")

    def viver(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
        logging.info(f"--- ATENA Ω v39.3 | Ciclo #{self.estado['ciclo']} ---")
        
        # Loop de vida (ativo por 2 minutos para teste, ou 300s para real)
        while (time.time() - self.start_time) < 120: 
            percepcao = self.sentir()
            logging.info(f"🧠 Input: {percepcao}")
            self.agir()
            time.sleep(30)

        self.evoluir()
        logging.info("💤 Ciclo finalizado. Preparando para hibernação.")

if __name__ == "__main__":
    AtenaOrganismo().viver()
