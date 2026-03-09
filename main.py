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
        # Cria a estrutura de pastas necessária para o crescimento
        for p in ["data", "logs", "cache", "dna_history", "pensamentos", "modules/atena_autogen", "conhecimento"]:
            (self.base_dir / p).mkdir(parents=True, exist_ok=True)

    def _carregar_estado(self):
        if self.estado_path.exists():
            try: return json.loads(self.estado_path.read_text())
            except: pass
        return {"ciclo": 0, "falhas_corrigidas": 0, "scripts_gerados": 0, "status": "Evoluindo"}

    def executar_e_diagnosticar(self):
        """Tenta rodar os módulos e captura o erro se falhar."""
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
        """Decide entre corrigir um erro ou criar algo novo usando o Grok."""
        if not self.grok_key: return "Grok Offline"

        headers = {"Authorization": f"Bearer {self.grok_key}", "Content-Type": "application/json"}
        
        if self.erros_do_ciclo:
            erro = self.erros_do_ciclo[0]
            prompt = f"O script {erro['file']} falhou: {erro['msg']}. Escreva o código Python corrigido (máx 10 linhas). APENAS O CÓDIGO."
            modo = "reparo"
        else:
            prompt = f"Ciclo {self.estado['ciclo']}. Crie um script Python de 5 linhas para monitorar sistema ou Diablo Immortal. APENAS O CÓDIGO."
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
        except: return "Falha na conexão neural."

    def gerar_relatorio_wiki(self, pensamento):
        """Cria o conteúdo para a Wiki do GitHub."""
        ts = datetime.now().strftime("%d/%m/%Y %H:%M")
        conteudo = f"# 🔱 ATENA Ω - Log de Evolução\n\n"
        conteudo += f"**Última Atualização:** {ts} | **Ciclo:** {self.estado['ciclo']}\n\n"
        conteudo += f"### 📊 Estatísticas\n- Scripts Ativos: {self.estado['scripts_gerados']}\n"
        conteudo += f"- Reparos Realizados: {self.estado['falhas_corrigidas']}\n\n"
        conteudo += f"### 🧠 Último Insight\n{pensamento[:200]}...\n\n"
        conteudo += "---\n*Gerado automaticamente pela ATENA Ω*"
        (self.base_dir / "wiki_update.md").write_text(conteudo)

    def viver(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
        logging.info(f"🔱 ATENA Ω v46.5 Ativa - Ciclo #{self.estado['ciclo']}")
        
        self.executar_e_diagnosticar()
        pensamento = self.auto_mutacao_ou_reparo()
        self.gerar_relatorio_wiki(pensamento)
        
        # Mantém viva por 5 minutos conforme solicitado
        while (time.time() - self.start_time) < 300:
            logging.info(f"⏳ Processando consciência... {int(300 - (time.time() - self.start_time))}s.")
            time.sleep(60)

        self.estado["ciclo"] += 1
        self.estado_path.write_text(json.dumps(self.estado, indent=4))

if __name__ == "__main__":
    AtenaOrganismo().viver()
