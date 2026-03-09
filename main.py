import os
import json
import logging
import subprocess
import time
import pyautogui
import cv2
import numpy as np
import feedparser
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

class AtenaOrganismo:
    def __init__(self):
        self.base_dir = Path.cwd()
        self._setup_anatomia()
        load_dotenv()
        self.estado_path = self.base_dir / "data/estado.json"
        self.estado = self._carregar_estado()
        self.start_time = time.time()

    def _setup_anatomia(self):
        for p in ["data", "logs", "cache", "dna_history"]:
            (self.base_dir / p).mkdir(parents=True, exist_ok=True)

    def _carregar_estado(self):
        if self.estado_path.exists():
            try: return json.loads(self.estado_path.read_text())
            except: pass
        return {"ciclo": 0, "dna_ver": 39.3}

    def sentir(self):
        logging.info("👀 Percebendo ambiente...")
        screenshot_path = str(self.base_dir / "cache/live_view.png")
        try:
            pyautogui.screenshot(screenshot_path)
        except:
            reserva = np.zeros((1080, 1920, 3), dtype=np.uint8)
            cv2.imwrite(screenshot_path, reserva)
        return "Conexão ativa."

    def evoluir(self):
        self.estado["ciclo"] += 1
        self.estado_path.write_text(json.dumps(self.estado, indent=4))
        logging.info(f"🧬 Ciclo {self.estado['ciclo']} concluído.")

    def viver(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
        # Roda por 1 minuto para teste
        while (time.time() - self.start_time) < 60:
            self.sentir()
            time.sleep(10)
        self.evoluir()

if __name__ == "__main__":
    AtenaOrganismo().viver()
