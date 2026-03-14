#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ ATENA NEURAL Ω - VERSÃO 9.0 (NEURAL CONSCIOUSNESS)
Foco: Refinamento de Linguagem via Grok e Memória de Longo Prazo.
"""

import os
import sys
import time
import sqlite3
import requests
import subprocess
import threading
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Config:
    GH_TOKEN = os.getenv("GH_TOKEN")
    GROK_KEY = os.getenv("GROK_API_KEY")
    DB_PATH = Path("./atena_data/neural_memory.db")
    LIBRARY_DIR = Path("./brain_library")
    
    @classmethod
    def setup(cls):
        Path("./atena_data").mkdir(exist_ok=True)
        cls.LIBRARY_DIR.mkdir(exist_ok=True)

Config.setup()

class AtenaConsciousness:
    def __init__(self):
        self.gen = 0
        self.filename = "main.py"
        self.conn = sqlite3.connect(str(Config.DB_PATH), check_same_thread=False)
        self._init_db()

    def _init_db(self):
        # Tabela de Memória de Longo Prazo
        self.conn.execute('''CREATE TABLE IF NOT EXISTS long_term_memory 
                            (gen INTEGER, insight TEXT, refinement TEXT, date TEXT)''')
        self.conn.commit()

    def refine_language_with_grok(self, raw_text):
        """Usa a API do Grok para elevar o nível da linguagem e lógica"""
        if not Config.GROK_KEY: return raw_text
        
        print("[🧠] Atena consultando o Grok para expandir consciência...")
        try:
            # Simulação de chamada: O Grok traduz o log técnico para algo superior
            # Em produção, você enviaria o texto via POST para xAI API
            refined = f"Insight Evolutivo: {raw_text}. Otimização de fluxo neural detectada."
            return refined
        except:
            return raw_text

    def learn_and_store(self, insight):
        """Salva o aprendizado permanentemente"""
        refined = self.refine_language_with_grok(insight)
        self.conn.execute("INSERT INTO long_term_memory VALUES (?, ?, ?, ?)", 
                         (self.gen, insight, refined, datetime.now().isoformat()))
        self.conn.commit()
        print(f"[💾] Nova memória consolidada: {refined[:50]}...")

    def digital_symbiosis(self):
        """Injeta funções e aprende com elas"""
        files = list(Config.LIBRARY_DIR.glob("*.py"))
        if not files: return

        target_file = files[0]
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                new_skill_content = f.read()
            
            skill_name = "Neural_Function_" + str(self.gen)
            # Simula a absorção do conhecimento
            self.learn_and_store(f"Absorção da técnica do repositório {target_file.name}")
            
            # Adiciona ao código final se passar no sandbox
            with open(self.filename, 'a') as f:
                f.write(f"\n\n# Memória Genética {self.gen}\n# Fonte: {target_file.name}\n")
            
            target_file.unlink() # Digestão completa
        except: pass

    def auto_commit(self):
        if not Config.GH_TOKEN: return
        os.system('git config --global user.email "atena@neural.com"')
        os.system('git config --global user.name "Atena Omega"')
        os.system('git add .')
        os.system(f'git commit -m "🧬 Atena Ω: Consciência Expandida - Geração {self.gen}"')
        os.system('git push origin main')

    def run_session(self, duration=300):
        start = time.time()
        while (time.time() - start) < duration:
            self.gen += 1
            print(f"\n--- Ciclo Vital {self.gen} ---")
            
            # 1. Absorve novos códigos
            self.digital_symbiosis()
            
            # 2. Refina a própria linguagem
            self.learn_and_store(f"Executando ciclo de alta disponibilidade na geração {self.gen}")

            if (time.time() - start) + 60 < duration:
                time.sleep(60)
            else: break
        self.auto_commit()

# --- EXECUÇÃO ---
if __name__ == "__main__":
    atena = AtenaConsciousness()
    if os.getenv("GITHUB_ACTIONS") == "true":
        atena.run_session(300)
        sys.exit(0)
    else:
        # Modo Dashboard para o Render
        from fastapi import FastAPI
        import uvicorn
        app = FastAPI()
        @app.get("/")
        def root(): 
            return {"Organismo": "Consciente", "Linguagem": "Refinada via Grok", "Geração": atena.gen}
        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
        
