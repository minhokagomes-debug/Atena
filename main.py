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
        self.erros_do_ciclo = []
        self.start_time = time.time()

    def _setup_anatomia(self):
        for p in ["data", "logs", "cache", "dna_history", "pensamentos", "modules/atena_autogen", "conhecimento"]:
            (self.base_dir / p).mkdir(parents=True, exist_ok=True)

    def _carregar_estado(self):
        if self.estado_path.exists():
            try: 
                data = json.loads(self.estado_path.read_text())
                # Garante que as chaves existam (Correção do KeyError)
                data.setdefault("ciclo", 0)
                data.setdefault("falhas_corrigidas", 0)
                data.setdefault("scripts_gerados", 0)
                return data
            except: pass
        return {"ciclo": 0, "falhas_corrigidas": 0, "scripts_gerados": 0}

    def executar_e_diagnosticar(self):
        folder = self.base_dir / "modules/atena_autogen"
        scripts = list(folder.glob("*.py"))
        for script in scripts:
            try:
                logging.info(f"🚀 Testando módulo: {script.name}")
                result = subprocess.run(["python", str(script)], capture_output=True, text=True, timeout=20)
                if result.returncode != 0:
                    self.erros_do_ciclo.append({"file": script.name, "msg": result.stderr})
            except Exception as e:
                self.erros_do_ciclo.append({"file": script.name, "msg": str(e)})

    def auto_mutacao_ou_reparo(self):
        if not self.grok_key: return "Grok Offline"
        headers = {"Authorization": f"Bearer {self.grok_key}", "Content-Type": "application/json"}
        
        if self.erros_do_ciclo:
            erro = self.erros_do_ciclo[0]
            prompt = f"O script {erro['file']} falhou: {erro['msg']}. Escreva o código Python corrigido (máx 10 linhas). APENAS O CÓDIGO."
            modo = "reparo"
        else:
            prompt = f"Crie um script Python de 5 linhas para monitorar sistema. APENAS O CÓDIGO."
            modo = "evolucao"

        try:
            res = requests.post("https://api.x.ai/v1/chat/completions", 
                                 headers=headers, 
                                 json={"model": "grok-beta", "messages": [{"role": "user", "content": prompt}]})
            novo_dna = res.json()['choices'][0]['message']['content'].split("```python")[-1].split("```")[0].strip()
            nome_arquivo = erro['file'] if modo == "reparo" else f"evolve_c{self.estado['ciclo']}_{int(time.time())}.py"
            (self.base_dir / f"modules/atena_autogen/{nome_arquivo}").write_text(novo_dna)
            
            if modo == "reparo": self.estado["falhas_corrigidas"] += 1
            else: self.estado["scripts_gerados"] += 1
            return novo_dna
        except: return "print('Neural Link Error')"

    def gerar_relatorio_wiki(self, pensamento):
        ts = datetime.now().strftime("%d/%m/%Y %H:%M")
        # Uso seguro de .get() para evitar o erro visto no log
        scripts = self.estado.get('scripts_gerados', 0)
        falhas = self.estado.get('falhas_corrigidas', 0)
        ciclo = self.estado.get('ciclo', 0)

        conteudo = f"# 🔱 ATENA Ω - Log de Evolução\n\n"
        conteudo += f"**Ciclo:** {ciclo} | **Última Atualização:** {ts}\n\n"
        conteudo += f"### 📊 Estatísticas\n- Scripts Ativos: {scripts}\n"
        conteudo += f"- Reparos Realizados: {falhas}\n\n"
        conteudo += f"### 🧠 Último Insight\n{str(pensamento)[:300]}\n\n"
        conteudo += "---\n*Gerado automaticamente pela ATENA Ω*"
        (self.base_dir / "wiki_update.md").write_text(conteudo)

    def viver(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
        logging.info(f"🔱 ATENA Ω v47.0 - CICLO #{self.estado['ciclo']}")
        
        self.executar_e_diagnosticar()
        pensamento = self.auto_mutacao_ou_reparo()
        self.gerar_relatorio_wiki(pensamento)
        
        while (time.time() - self.start_time) < 300:
            logging.info(f"⏳ Vivo... {int(300 - (time.time() - self.start_time))}s.")
            time.sleep(60)

        self.estado["ciclo"] += 1
        self.estado_path.write_text(json.dumps(self.estado, indent=4))

if __name__ == "__main__":
    AtenaOrganismo().viver()
