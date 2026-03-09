import os
import json
import logging
import requests
import time
import subprocess
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
        self.ultimos_erros = []
        self.start_time = time.time()

    def _setup_anatomia(self):
        for p in ["data", "logs", "cache", "dna_history", "pensamentos", "modules/atena_autogen"]:
            (self.base_dir / p).mkdir(parents=True, exist_ok=True)

    def _carregar_estado(self):
        if self.estado_path.exists():
            try: return json.loads(self.estado_path.read_text())
            except: pass
        return {"ciclo": 0, "scripts_gerados": 0, "falhas_corrigidas": 0, "status": "Auto-Reparo"}

    def executar_e_aprender(self):
        """Executa módulos e captura erros para aprendizado."""
        folder = self.base_dir / "modules/atena_autogen"
        scripts = list(folder.glob("*.py"))
        
        for script in scripts:
            try:
                logging.info(f"🚀 Testando módulo: {script.name}")
                result = subprocess.run(["python", str(script)], capture_output=True, text=True, timeout=20)
                
                if result.returncode != 0:
                    logging.warning(f"❌ Falha detectada em {script.name}. Registrando para reparo.")
                    self.ultimos_erros.append({"script": script.name, "erro": result.stderr})
                else:
                    logging.info(f"✅ Módulo {script.name} operando normalmente.")
            except Exception as e:
                self.ultimos_erros.append({"script": script.name, "erro": str(e)})

    def auto_mutacao_corretiva(self):
        """Usa os erros detectados para gerar um código corrigido."""
        if not self.grok_key or not self.ultimos_erros:
            return self.gerar_novo_codigo_padrao()

        erro_contexto = self.ultimos_erros[-1]
        logging.info(f"🔧 Solicitando reparo para: {erro_contexto['script']}")
        
        headers = {"Authorization": f"Bearer {self.grok_key}", "Content-Type": "application/json"}
        prompt = (f"Você é a ATENA Ω. O script '{erro_contexto['script']}' falhou com o erro: '{erro_contexto['erro']}'. "
                  "Escreva uma versão corrigida e simplificada deste script em Python (máx 10 linhas). APENAS O CÓDIGO.")

        try:
            res = requests.post("https://api.x.ai/v1/chat/completions", 
                                headers=headers, 
                                json={"model": "grok-beta", "messages": [{"role": "user", "content": prompt}]},
                                timeout=35)
            codigo_novo = res.json()['choices'][0]['message']['content']
            
            # Sobrescreve o script defeituoso com a correção
            path_fix = self.base_dir / f"modules/atena_autogen/{erro_contexto['script']}"
            codigo_limpo = codigo_novo.split("```python")[-1].split("```")[0].strip()
            path_fix.write_text(codigo_limpo)
            
            self.estado["falhas_corrigidas"] += 1
            logging.info(f"✨ Reparo aplicado em {erro_contexto['script']}")
        except:
            logging.error("Neural Link falhou durante o reparo.")

    def gerar_novo_codigo_padrao(self):
        # Lógica de criação de novos módulos (mesma da v44)
        pass

    def viver(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
        logging.info(f"🔱 ATENA Ω v45.0 - PROTOCOLO DE AUTO-REPARO")
        
        # 1. Analisa o que deu errado antes
        self.executar_e_aprender()
        
        # 2. Aplica correções ou cria algo novo
        self.auto_mutacao_corretiva()
        
        # 3. Manutenção de ciclo (5 min)
        while (time.time() - self.start_time) < 300:
            logging.info(f"⏳ Em estado de regeneração... {int(300 - (time.time() - self.start_time))}s.")
            time.sleep(60)

        self.estado["ciclo"] += 1
        self.estado_path.write_text(json.dumps(self.estado, indent=4))

if __name__ == "__main__":
    AtenaOrganismo().viver()
