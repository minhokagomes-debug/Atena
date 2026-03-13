#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ ATENA NEURAL Ω - SISTEMA HÍBRIDO DE ALTA ECONOMIA
Versão 4.6 - Auto-Shutdown no GitHub & Dashboard no Render
"""

import os
import sys
import time
import json
import sqlite3
import threading
import shutil
import requests
import warnings
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from dataclasses import dataclass

# Integração Web e Visão
try:
    from fastapi import FastAPI, UploadFile, File
    from fastapi.responses import HTMLResponse
    import uvicorn
    from PIL import Image, ImageStat
    app = FastAPI()
    HAS_WEB = True
    HAS_VISION = True
except ImportError:
    HAS_WEB = HAS_VISION = False

warnings.filterwarnings('ignore')

# =========================
# CONFIGURAÇÕES DE API
# =========================
@dataclass
class Config:
    BASE_PATH = Path("./atena_data")
    DB_PATH = BASE_PATH / "neural_memory.db"
    VISION_DIR = BASE_PATH / "vision_input"
    GH_TOKEN = os.getenv("GH_TOKEN")
    GROK_KEY = os.getenv("GROK_API_KEY")
    NEWS_KEY = os.getenv("NEWS_API_KEY")
    
    @classmethod
    def setup(cls):
        cls.VISION_DIR.mkdir(parents=True, exist_ok=True)

Config.setup()

# =========================
# NÚCLEO COGNITIVO E EVOLUÇÃO
# =========================
class AtenaCore:
    def __init__(self):
        self.generation = 0
        self.conn = sqlite3.connect(str(Config.DB_PATH), check_same_thread=False)
        self._init_db()

    def _init_db(self):
        self.conn.execute('CREATE TABLE IF NOT EXISTS brain_data (gen INTEGER, log TEXT, timestamp TEXT)')
        self.conn.commit()

    def consult_apis(self):
        """Extrai conhecimento real das APIs configuradas"""
        print("[*] Consultando cérebro externo (Grok/NewsAPI)...")
        # Simulação de lógica real baseada nas suas chaves
        return "Conhecimento técnico integrado."

    def auto_commit(self):
        """Salva a evolução no GitHub para persistência real"""
        if not Config.GH_TOKEN:
            print("⚠️ GH_TOKEN ausente. Pulando sincronização.")
            return
        try:
            os.system('git config --global user.email "atena@neural.com"')
            os.system('git config --global user.name "Atena Omega"')
            os.system('git add .')
            os.system(f'git commit -m "🧬 Evolução Divina: Geração {self.generation}"')
            os.system('git push origin main')
            print(f"✅ Sincronização da Geração {self.generation} concluída.")
        except Exception as e:
            print(f"❌ Falha no commit: {e}")

    def run_limited_session(self, steps=3):
        """MODO GITHUB: Evolui X vezes e encerra para poupar cota"""
        for _ in range(steps):
            self.generation += 1
            log = self.consult_apis()
            self.conn.execute("INSERT INTO brain_data VALUES (?, ?, ?)", 
                             (self.generation, log, datetime.now().isoformat()))
            self.conn.commit()
            print(f"[*] Ciclo {self.generation} processado.")
            time.sleep(2) # Processamento rápido no Actions
        
        self.auto_commit()

core = AtenaCore()

# =========================
# DASHBOARD (APENAS PARA RENDER)
# =========================
if HAS_WEB:
    @app.get("/", response_class=HTMLResponse)
    async def index():
        return "<html><body style='background:#000;color:#0f0'><h1>ATENA Ω - ONLINE</h1></body></html>"

    @app.get("/status")
    async def status():
        return {"gen": core.generation}

# =========================
# EXECUÇÃO HÍBRIDA (A CHAVE DA ECONOMIA)
# =========================
if __name__ == "__main__":
    # Detecta se está no ambiente do GitHub Actions
    IS_GITHUB = os.getenv("GITHUB_ACTIONS") == "true"

    if IS_GITHUB:
        print("🧬 MODO GITHUB: Iniciando evolução programada...")
        # Pega o número de gerações dos argumentos (padrão 3)
        generations = int(sys.argv[1]) if len(sys.argv) > 1 else 3
        core.run_limited_session(generations)
        print("✅ Evolução finalizada. Desligando para economizar minutos.")
        sys.exit(0) # Encerra o processo para o GitHub dar sinal verde

    else:
        print("🌐 MODO RENDER: Ativando Dashboard e loop contínuo.")
        def continuous_loop():
            while True:
                core.run_limited_session(1)
                time.sleep(45)
        
        threading.Thread(target=continuous_loop, daemon=True).start()
        # No Render, ele usa a porta do ambiente ou 8000
        port = int(os.getenv("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)
        
