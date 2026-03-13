#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ ATENA NEURAL Ω - SISTEMA DE EVOLUÇÃO E VISÃO REAL
Versão 3.5 - OCR Integration & Unified Terminal
"""

import time
import json
import uuid
import hashlib
import sqlite3
import subprocess
import tempfile
import sys
import re
import warnings
import threading
import shutil
import os
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np

# Integração Web
try:
    from fastapi import FastAPI, Request, UploadFile, File
    from fastapi.responses import HTMLResponse, FileResponse
    from pydantic import BaseModel
    import uvicorn
    app = FastAPI()
    HAS_WEB = True
except ImportError:
    HAS_WEB = False

# Visão e OCR
try:
    from PIL import Image, ImageStat
    import pytesseract  # Para ler texto dentro das imagens
    HAS_VISION = True
except ImportError:
    HAS_VISION = False

warnings.filterwarnings('ignore')

# =========================
# CONFIGURAÇÕES
# =========================
BASE_DIR = Path("./atena_data")
BASE_DIR.mkdir(exist_ok=True)

@dataclass
class Config:
    DB_PATH = BASE_DIR / "neural_memory.db"
    VISION_DIR = BASE_DIR / "vision_input"
    BACKUP_DIR = BASE_DIR / "backups"
    
    for dir_path in [VISION_DIR, BACKUP_DIR]:
        dir_path.mkdir(exist_ok=True)

# =========================
# NÚCLEO DE VISÃO E OCR REAL
# =========================
class AtenaVision:
    @staticmethod
    def analyze_image(image_path: str) -> Dict[str, Any]:
        """Lê a imagem, extrai pixels e texto real"""
        if not HAS_VISION:
            return {"error": "Módulos de visão não configurados."}
        
        try:
            with Image.open(image_path) as img:
                # 1. Análise de Pixels
                img_gray = img.convert('L')
                stat = ImageStat.Stat(img_gray)
                
                # 2. OCR (Tentar ler texto na imagem)
                try:
                    text_found = pytesseract.image_to_string(img)
                except:
                    text_found = "Tesseract não configurado no servidor."

                return {
                    "brightness": round(stat.mean[0], 2),
                    "resolution": f"{img.size[0]}x{img.size[1]}",
                    "text_extracted": text_found[:500], # Primeiros 500 caracteres
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {"error": str(e)}

# =========================
# SISTEMA DE EVOLUÇÃO
# =========================
class NeuralEvolutionSystem:
    def __init__(self):
        self.generation = 0
        self.last_vision_data = None
        self.conn = sqlite3.connect(str(Config.DB_PATH), check_same_thread=False)
        self._init_db()

    def _init_db(self):
        self.conn.execute('CREATE TABLE IF NOT EXISTS vision_logs (id TEXT, data TEXT, date TEXT)')
        self.conn.commit()

    def evolve_cycle(self):
        while True:
            self.generation += 1
            # Espaço para o CodeExecutor real rodar no hardware
            time.sleep(45)

system = NeuralEvolutionSystem()

# =========================
# INTERFACE WEB (PARA UPLOAD)
# =========================
if HAS_WEB:
    @app.get("/", response_class=HTMLResponse)
    async def index():
        return """
        <body style="background:#000; color:#0f0; font-family:monospace; padding:50px;">
            <h1>ATENA Ω - UPLOAD DE VISÃO</h1>
            <input type="file" id="f"><button onclick="up()">ENVIAR PARA ATENA</button>
            <div id="res"></div>
            <script>
                async function up(){
                    const fd = new FormData();
                    fd.append('file', document.getElementById('f').files[0]);
                    const r = await fetch('/atena/vision', {method:'POST', body:fd});
                    const d = await r.json();
                    document.getElementById('res').innerText = JSON.stringify(d.analysis, null, 2);
                }
            </script>
        </body>
        """

    @app.post("/atena/vision")
    async def process_vision(file: UploadFile = File(...)):
        path = Config.VISION_DIR / file.filename
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        analysis = AtenaVision.analyze_image(str(path))
        system.last_vision_data = analysis
        return {"status": "success", "analysis": analysis}

# =========================
# CHAT TERMINAL (O CORAÇÃO)
# =========================
def terminal_chat():
    print(f"\n{'='*50}\nATENA Ω - TERMINAL DE COMANDO REAL\n{'='*50}")
    while True:
        cmd = input("\n👤 Danilo: ").lower().strip()
        
        if cmd in ['sair', 'exit']: break
        
        if "status" in cmd:
            print(f"🧠 Atena: Geração {system.generation} ativa. Visão: {'Pronta' if HAS_VISION else 'Offline'}")
        
        elif "olhe" in cmd or "visao" in cmd:
            if system.last_vision_data:
                print("🧠 Atena: Analisando última imagem recebida...")
                print(f"   > Texto detectado: {system.last_vision_data.get('text_extracted', 'Nenhum')}")
                print(f"   > Resolução: {system.last_vision_data.get('resolution')}")
            else:
                print("🧠 Atena: Ainda não recebi imagens pela interface web.")
        
        elif "backup" in cmd:
            path = shutil.make_archive(str(Config.BACKUP_DIR / "atena_evolution"), 'zip', BASE_DIR)
            print(f"🧠 Atena: Backup real gerado em: {path}")
            
        else:
            print(f"🧠 Atena: Comando registrado na geração {system.generation}.")

# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    # 1. Inicia Evolução
    threading.Thread(target=system.evolve_cycle, daemon=True).start()
    
    # 2. Inicia Servidor Web (Se estiver no Render ou com --server)
    if HAS_WEB:
        threading.Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error"), daemon=True).start()
        print("🌐 Interface de Visão ativa em: http://localhost:8000")

    # 3. Abre o Chat no Terminal
    terminal_chat()
