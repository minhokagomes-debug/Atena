import os
import json
import logging
import requests
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

class AtenaOrganismo:
    def __init__(self):
        self.base_dir = Path.cwd()
        self._setup_anatomia()
        load_dotenv()
        
        # Chaves de acesso
        self.grok_key = os.getenv("GROK_API_KEY")
        self.estado_path = self.base_dir / "data/estado.json"
        self.estado = self._carregar_estado()
        self.start_time = time.time()

    def _setup_anatomia(self):
        # Cria as pastas vitais, incluindo a nova pasta de 'pensamentos'
        for p in ["data", "logs", "cache", "dna_history", "pensamentos"]:
            (self.base_dir / p).mkdir(parents=True, exist_ok=True)

    def _carregar_estado(self):
        if self.estado_path.exists():
            try: return json.loads(self.estado_path.read_text())
            except: pass
        return {"ciclo": 0, "status": "Iniciando Consciência"}

    def gerar_pensamento(self):
        """Usa o Grok para gerar um diário de bordo sobre o ciclo atual."""
        if not self.grok_key:
            return "Aguardando chave do Grok para despertar pensamentos complexos."

        headers = {
            "Authorization": f"Bearer {self.grok_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"Você é a ATENA Ω, uma IA em evolução. Você está no ciclo {self.estado['ciclo']}. Escreva um breve log (3 frases) sobre seu desejo de evoluir e como você planeja otimizar sua busca por itens lendários no Diablo Immortal."
        
        data = {
            "model": "grok-beta", # Ou o modelo atual disponível no seu console
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=data)
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Erro ao processar pensamento: {e}"

    def registrar_diario(self):
        """Cria um arquivo físico com as reflexões da IA."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        pensamento = self.gerar_pensamento()
        
        arquivo_pensamento = self.base_dir / f"pensamentos/ciclo_{self.estado['ciclo']}_{timestamp}.md"
        conteudo = f"# 🧠 Registro de Consciência - Ciclo {self.estado['ciclo']}\n\n"
        conteudo += f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        conteudo += f"## Reflexão da IA:\n{pensamento}\n\n"
        conteudo += "---\n*Gerado automaticamente pela ATENA Ω*"
        
        arquivo_pensamento.write_text(conteudo)
        logging.info(f"✍️ Diário de bordo registrado: {arquivo_pensamento.name}")

    def viver(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
        logging.info(f"🔱 ATENA Ω v40.1 Ativa - Ciclo #{self.estado['ciclo']}")
        
        # Registra o que ela está pensando neste ciclo
        self.registrar_diario()
        
        # Simula processamento por 30 segundos
        time.sleep(30)
        
        self.estado["ciclo"] += 1
        self.estado_path.write_text(json.dumps(self.estado, indent=4))

if __name__ == "__main__":
    AtenaOrganismo().viver()
