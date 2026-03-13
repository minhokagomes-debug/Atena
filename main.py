#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ ATENA NEURAL Ω - SISTEMA DE EVOLUÇÃO E VISÃO REAL
Versão 3.6 - Gemini-Style Dashboard & Unified Logic
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
    import pytesseract  
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
        if not HAS_VISION:
            return {"error": "Módulos de visão não configurados."}
        try:
            with Image.open(image_path) as img:
                img_gray = img.convert('L')
                stat = ImageStat.Stat(img_gray)
                try:
                    text_found = pytesseract.image_to_string(img)
                except:
                    text_found = "Tesseract não configurado."

                return {
                    "brightness": round(stat.mean[0], 2),
                    "resolution": f"{img.size[0]}x{img.size[1]}",
                    "text_extracted": text_found[:500],
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
            time.sleep(45)

system = NeuralEvolutionSystem()

# =========================
# DASHBOARD GEMINI-STYLE
# =========================
if HAS_WEB:
    @app.get("/", response_class=HTMLResponse)
    async def index():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>ATENA Ω - DASHBOARD</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { background: #0e0e10; color: #e1e1e6; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
                header { background: #1a191e; padding: 15px; border-bottom: 2px solid #00ff41; display: flex; justify-content: space-between; align-items: center; }
                #chat { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 10px; }
                .bubble { padding: 12px; border-radius: 10px; max-width: 80%; font-size: 14px; line-height: 1.4; }
                .atena { background: #1f1f23; border-left: 4px solid #00ff41; align-self: flex-start; }
                .user { background: #00ff41; color: #000; align-self: flex-end; font-weight: bold; }
                #controls { background: #1a191e; padding: 15px; display: flex; gap: 10px; border-top: 1px solid #333; }
                input[type="text"] { flex: 1; background: #000; border: 1px solid #333; color: #0f0; padding: 10px; border-radius: 5px; }
                button { background: #00ff41; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-weight: bold; }
                #file-info { font-size: 10px; color: #888; margin-top: 5px; }
            </style>
        </head>
        <body>
            <header>
                <span><b>ATENA Ω</b> [ONLINE]</span>
                <span id="gen-tag">GERAÇÃO: 0</span>
            </header>
            <div id="chat">
                <div class="bubble atena">Núcleo Neural ativo, Danilo. Aguardando comandos ou análise visual.</div>
            </div>
            <div id="controls">
                <input type="file" id="file" style="display:none" onchange="upload()">
                <button onclick="document.getElementById('file').click()">📸</button>
                <input type="text" id="msg" placeholder="Digite um comando...">
                <button onclick="send()">OK</button>
            </div>
            <script>
                async function updateStatus() {
                    const r = await fetch('/status_api');
                    const d = await r.json();
                    document.getElementById('gen-tag').innerText = "GERAÇÃO: " + d.gen;
                }
                setInterval(updateStatus, 5000);

                async function send() {
                    const i = document.getElementById('msg');
                    const c = document.getElementById('chat');
                    if(!i.value) return;
                    c.innerHTML += `<div class="bubble user">${i.value}</div>`;
                    const val = i.value; i.value = '';
                    setTimeout(() => {
                        c.innerHTML += `<div class="bubble atena">Comando "${val}" processado no núcleo de evolução.</div>`;
                        c.scrollTop = c.scrollHeight;
                    }, 500);
                }

                async function upload() {
                    const f = document.getElementById('file').files[0];
                    const fd = new FormData(); fd.append('file', f);
                    const c = document.getElementById('chat');
                    c.innerHTML += `<div class="bubble user"><i>Enviando imagem: ${f.name}</i></div>`;
                    const r = await fetch('/atena/vision', {method:'POST', body:fd});
                    const d = await r.json();
                    c.innerHTML += `<div class="bubble atena"><b>Análise Visual:</b><br>Resolução: ${d.analysis.resolution}<br>Texto: ${d.analysis.text_extracted || 'Nenhum'}</div>`;
                    c.scrollTop = c.scrollHeight;
                }
            </script>
        </body>
        </html>
        """

    @app.get("/status_api")
    async def status_api():
        return {"gen": system.generation}

    @app.post("/atena/vision")
    async def process_vision(file: UploadFile = File(...)):
        path = Config.VISION_DIR / file.filename
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        analysis = AtenaVision.analyze_image(str(path))
        system.last_vision_data = analysis
        return {"status": "success", "analysis": analysis}

# =========================
# CHAT TERMINAL (MANTIDO)
# =========================
def terminal_chat():
    print(f"\n{'='*50}\nATENA Ω - TERMINAL DE COMANDO REAL\n{'='*50}")
    while True:
        cmd = input("\n👤 Danilo: ").lower().strip()
        if cmd in ['sair', 'exit']: break
        if "status" in cmd:
            print(f"🧠 Atena: Geração {system.generation} ativa. Visão: {'Pronta' if HAS_VISION else 'Offline'}")
        elif "backup" in cmd:
            path = shutil.make_archive(str(Config.BACKUP_DIR / "atena_evolution"), 'zip', BASE_DIR)
            print(f"🧠 Atena: Backup gerado em: {path}")
        else:
            print(f"🧠 Atena: Registrado geração {system.generation}.")

# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    threading.Thread(target=system.evolve_cycle, daemon=True).start()
    if HAS_WEB:
        threading.Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error"), daemon=True).start()
        print("🌐 Dashboard ativo em: http://localhost:8000")
    terminal_chat()
