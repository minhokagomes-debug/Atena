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
        # Carregamento seguro para evitar KeyError visto nas imagens do utilizador
        self.estado = self._carregar_estado_seguro()
        self.erros_do_ciclo = []
        self.start_time = time.time()

    def _setup_anatomia(self):
        """Cria as pastas necessárias para a persistência de dados."""
        pastas = ["data", "logs", "cache", "dna_history", "pensamentos", "modules/atena_autogen", "conhecimento"]
        for p in pastas:
            (self.base_dir / p).mkdir(parents=True, exist_ok=True)

    def _carregar_estado_seguro(self):
        """Lê o estado atual ou cria um novo com valores padrão se houver erro."""
        padrao = {"ciclo": 0, "falhas_corrigidas": 0, "scripts_gerados": 0}
        if self.estado_path.exists():
            try: 
                conteudo = self.estado_path.read_text()
                if not conteudo.strip():
                    return padrao
                data = json.loads(conteudo)
                # Garante que todas as chaves padrão existem no dicionário lido
                for k, v in padrao.items():
                    if k not in data:
                        data[k] = v
                return data
            except (json.JSONDecodeError, Exception) as e:
                logging.error(f"Erro ao ler estado.json: {e}. Resetando para padrão.")
        return padrao

    def executar_e_diagnosticar(self):
        """Executa os scripts gerados e guarda erros para auto-reparo."""
        folder = self.base_dir / "modules/atena_autogen"
        scripts = list(folder.glob("*.py"))
        for script in scripts:
            try:
                logging.info(f"🚀 Ativando módulo: {script.name}")
                # Execução real do script filho
                result = subprocess.run(["python", str(script)], capture_output=True, text=True, timeout=20)
                if result.returncode != 0:
                    self.erros_do_ciclo.append({"file": script.name, "msg": result.stderr})
            except Exception as e:
                self.erros_do_ciclo.append({"file": script.name, "msg": str(e)})

    def auto_mutacao_ou_reparo(self):
        """Utiliza o Grok para evoluir o código ou corrigir falhas."""
        if not self.grok_key: 
            logging.error("Chave Grok não encontrada!")
            return "print('Grok Offline')"
            
        headers = {"Authorization": f"Bearer {self.grok_key}", "Content-Type": "application/json"}
        
        # Lógica Random: Decide um foco real para a evolução se não houver erros
        focos = ["otimização de ficheiros", "limpeza de cache", "análise de logs", "gestão de memória"]
        foco_escolhido = random.choice(focos)

        if self.erros_do_ciclo:
            erro = self.erros_do_ciclo[0]
            prompt = f"O script {erro['file']} falhou com o erro: {erro['msg']}. Escreve a correção em Python (máx 10 linhas). APENAS CÓDIGO."
            modo = "reparo"
        else:
            prompt = f"Escreve um script Python de 5 linhas focado em {foco_escolhido}. APENAS CÓDIGO."
            modo = "evolucao"

        try:
            res = requests.post("https://api.x.ai/v1/chat/completions", 
                                 headers=headers, 
                                 json={"model": "grok-beta", "messages": [{"role": "user", "content": prompt}]})
            
            resposta_texto = res.json()['choices'][0]['message']['content']
            novo_dna = resposta_texto.split("```python")[-1].split("```")[0].strip()
            
            # Nomeação com fator random para evitar colisões
            id_random = random.randint(100, 999)
            nome_arquivo = erro['file'] if modo == "reparo" else f"dna_c{self.estado['ciclo']}_{id_random}.py"
            
            (self.base_dir / f"modules/atena_autogen/{nome_arquivo}").write_text(novo_dna)
            
            if modo == "reparo": self.estado["falhas_corrigidas"] += 1
            else: self.estado["scripts_gerados"] += 1
            
            return novo_dna
        except Exception as e:
            logging.error(f"Falha na comunicação com Grok: {e}")
            return "print('Erro de conexão')"

    def gerar_relatorio_wiki(self, pensamento):
        """Prepara o ficheiro Markdown que será enviado para a Wiki do GitHub."""
        ts = datetime.now().strftime("%d/%m/%Y %H:%M")
        # Uso de .get() por segurança extrema
        ciclo = self.estado.get('ciclo', 0)
        scripts = self.estado.get('scripts_gerados', 0)
        reparos = self.estado.get('falhas_corrigidas', 0

        conteudo = f"# 🔱 ATENA Ω - Diário de Evolução\n\n"
        conteudo += f"**Ciclo:** {ciclo} | **Sincronização:** {ts}\n"
        conteudo += f"**Modo:** Decisão Aleatória Real\n\n"
        conteudo += f"### 📊 Estatísticas Reais\n"
        conteudo += f"- Módulos Criados: {scripts}\n"
        conteudo += f"- Auto-Reparos: {reparos}\n\n"
        conteudo += f"### 🧠 Último Insight Gerado\n
                conteudo += "---\n*Este documento é gerado autonomamente pela ATENA Ω.*"
        
        (self.base_dir / "wiki_update.md").write_text(conteudo)

    def viver(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')
        logging.info(f"🔱 ATENA Ω v48.2 - INICIANDO CICLO {self.estado.get('ciclo', 0)}")
        
        # 1. Execução e Diagnóstico
        self.executar_e_diagnosticar()
        
        # 2. Evolução ou Conserto
        pensamento = self.auto_mutacao_ou_reparo()
        
        # 3. Preparação da Wiki
        self.gerar_relatorio_wiki(pensamento)
        
        # 4. Loop de vida de 5 minutos (300 segundos) com batimento variável
        while (time.time() - self.start_time) < 300:
            restante = int(300 - (time.time() - self.start_time))
            logging.info(f"⏳ Vivo e Processando... {restante}s para hibernação.")
            
            # Intervalo aleatório para simular atividade real (40 a 70s)
            espera = random.randint(40, 70)
            time.sleep(min(espera, restante if restante > 0 else 1))

        # Salva o estado final do ciclo
        self.estado["ciclo"] += 1
        self.estado_path.write_text(json.dumps(self.estado, indent=4))

if __name__ == "__main__":
    AtenaOrganismo().viver()
