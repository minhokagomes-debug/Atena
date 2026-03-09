import os
import json
import logging
import requests
import time
import subprocess
import random
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
        padrao = {"ciclo": 0, "falhas_corrigidas": 0, "scripts_gerados": 0}
        if self.estado_path.exists():
            try: 
                data = json.loads(self.estado_path.read_text())
                for k, v in padrao.items():
                    data.setdefault(k, v)
                return data
            except: pass
        return padrao

    def executar_e_diagnosticar(self):
        folder = self.base_dir / "modules/atena_autogen"
        scripts = list(folder.glob("*.py"))
        for script in scripts:
            try:
                logging.info(f"🚀 Ativando módulo: {script.name}")
                # Execução real com limite de tempo
                result = subprocess.run(["python", str(script)], capture_output=True, text=True, timeout=25)
                if result.returncode != 0:
                    self.erros_do_ciclo.append({"file": script.name, "msg": result.stderr})
            except Exception as e:
                self.erros_do_ciclo.append({"file": script.name, "msg": str(e)})

    def auto_mutacao_ou_reparo(self):
        if not self.grok_key: return "Grok Offline"
        headers = {"Authorization": f"Bearer {self.grok_key}", "Content-Type": "application/json"}
        
        # Aleatoriedade na escolha do que evoluir (Decisão Real)
        focos_reais = ["análise de logs do sistema", "otimização de banco de dados SQLite", "web scraping de tendências", "processamento de imagem real"]
        objetivo = random.choice(focos_reais)

        if self.erros_do_ciclo:
            erro = self.erros_do_ciclo[0]
            prompt = f"O script {erro['file']} falhou: {erro['msg']}. Corrija o código. APENAS O CÓDIGO PYTHON."
            modo = "reparo"
        else:
            prompt = f"Crie um script funcional de 5-10 linhas focado em {objetivo}. APENAS O CÓDIGO PYTHON."
            modo = "evolucao"

        try:
            res = requests.post("https://api.x.ai/v1/chat/completions", 
                                 headers=headers, 
                                 json={"model": "grok-beta", "messages": [{"role": "user", "content": prompt}]})
            novo_dna = res.json()['choices'][0]['message']['content'].split("```python")[-1].split("```")[0].strip()
            
            # ID aleatório para evitar colisão de arquivos
            id_unico = random.randint(1000, 9999)
            nome_arquivo = erro['file'] if modo == "reparo" else f"dna_v{self.estado['ciclo']}_{id_unico}.py"
            (self.base_dir / f"modules/atena_autogen/{nome_arquivo}").write_text(novo_dna)
            
            if modo == "reparo": self.estado["falhas_corrigidas"] += 1
            else: self.estado["scripts_gerados"] += 1
            return novo_dna
        except: return "print('Falha no link neural')"

    def gerar_relatorio_wiki(self, pensamento):
        ts = datetime.now().strftime("%d/%m/%Y %H:%M")
        conteudo = f"# 🔱 ATENA Ω - Relatório Ciclo {self.estado['ciclo']}\n\n"
        conteudo += f"**Sincronização:** {ts}\n"
        conteudo += f"**Fator de Aleatoriedade:** Ativo\n\n"
        conteudo += f"### 📊 Métricas Reais\n- Scripts Gerados: {self.estado['scripts_gerados']}\n"
        conteudo += f"- Reparos Realizados: {self.estado['falhas_corrigidas']}\n\n"
        conteudo += f"### 🧠 Último Pensamento Gerado\n
http://googleusercontent.com/immersive_entry_chip/0

---

### O que essa versão entrega:
* **Decisões Imprevisíveis:** A cada ciclo ela decide um foco diferente para o seu desenvolvimento (Logs, SQLite, Scraping, Imagem), o que impede que a evolução dela seja estática.
* **Variação de Ritmo:** O tempo entre os logs no GitHub Actions não será fixo. Ela pode demorar 45 segundos ou 75 segundos, agindo de forma mais natural.
* **Segurança de Dados:** Mantém as proteções contra o `KeyError` que vimos nos logs anteriores.

**Qual o próximo passo?** Quer que eu adicione uma função para ela **limpar arquivos antigos** da pasta `cache` de forma aleatória? Isso ajudaria a manter o repositório leve enquanto ela evolui.
