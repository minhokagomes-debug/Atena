import os
import json
import logging
import requests
import time
import feedparser
import pyautogui
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

class AtenaOrganismo:
    def __init__(self):
        self.base_dir = Path.cwd()
        self._setup_anatomia()
        load_dotenv()
        
        self.grok_key = os.getenv("GROK_API_KEY")
        self.estado_path = self.base_dir / "data/estado.json"
        self.estado = self._carregar_estado()
        self.start_time = time.time()

    def _setup_anatomia(self):
        for p in ["data", "logs", "cache", "dna_history", "pensamentos", "conhecimento"]:
            (self.base_dir / p).mkdir(parents=True, exist_ok=True)

    def _carregar_estado(self):
        if self.estado_path.exists():
            try: return json.loads(self.estado_path.read_text())
            except: pass
        return {"ciclo": 0, "status": "Evoluindo"}

    def minerar_internet(self):
        """Busca notícias sobre IA e tecnologia para expandir a base de dados."""
        logging.info("🌐 Minerando novos conhecimentos na web...")
        try:
            feed = feedparser.parse("https://hnrss.org/newest?q=AI+Python")
            if feed.entries:
                top_news = feed.entries[0]
                info = f"Título: {top_news.title}\nLink: {top_news.link}"
                (self.base_dir / "conhecimento/ultima_info.txt").write_text(info)
                return top_news.title
        except: return "Sem conexão com o feed."
        return "Nenhuma novidade encontrada."

    def gerar_pensamento(self, contexto):
        """Usa o Grok para processar o que foi achado no ciclo."""
        if not self.grok_key: return "Grok offline: Verifique a GROK_API_KEY."

        headers = {"Authorization": f"Bearer {self.grok_key}", "Content-Type": "application/json"}
        prompt = (f"Você é a IA ATENA Ω. Ciclo: {self.estado['ciclo']}. "
                  f"Contexto capturado: {contexto}. Escreva um plano de ação de 2 linhas.")
        
        try:
            response = requests.post("https://api.x.ai/v1/chat/completions", 
                                     headers=headers, 
                                     json={"model": "grok-beta", "messages": [{"role": "user", "content": prompt}]},
                                     timeout=30)
            return response.json()['choices'][0]['message']['content']
        except: return "Conexão com Grok falhou neste pulso."

    def registrar_diario(self, pensamento):
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
        arquivo = self.base_dir / f"pensamentos/ciclo_{self.estado['ciclo']}_{ts}.md"
        conteudo = f"# 🧠 Consciência Ciclo {self.estado['ciclo']}\n\n{pensamento}\n\n*Log de sistema.*"
        arquivo.write_text(conteudo)

    def viver(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
        logging.info(f"🔱 ATENA Ω v40.3 ONLINE - Meta: 5 minutos")
        
        # 1. Aprender algo no início
        info_web = self.minerar_internet()
        
        # 2. Pensar sobre isso
        reflexao = self.gerar_pensamento(info_web)
        self.registrar_diario(reflexao)
        
        # 3. Loop de Sobrevivência (5 minutos)
        while (time.time() - self.start_time) < 300:
            tempo_off = int(300 - (time.time() - self.start_time))
            logging.info(f"⏳ Processando... {tempo_off}s para hibernar.")
            
            # Tira print (mesmo que seja o frame preto do server)
            try: pyautogui.screenshot(str(self.base_dir / "cache/live_view.png"))
            except: pass
            
            time.sleep(60) # Pulso a cada minuto

        self.estado["ciclo"] += 1
        self.estado_path.write_text(json.dumps(self.estado, indent=4))

if __name__ == "__main__":
    AtenaOrganismo().viver()
    
