#!/usr/bin/env python3
"""
ATENA Ω - ORGANISMO DIGITAL COM APRENDIZADO ATIVO E PERSISTÊNCIA NO GITHUB
Versão: Ω.GITHUB.1.0

NOVAS FUNCIONALIDADES:
- 📦 Salva TODOS os códigos aprendidos no GitHub
- 🤖 Cria módulos funcionais a cada ciclo
- 📚 Organiza conhecimento por categoria
- 🔄 Sincroniza automaticamente com repositório
- 🧬 Evolução visível no GitHub
"""

import os
import json
import logging
import requests
import time
import subprocess
import random
import hashlib
import sqlite3
import threading
import asyncio
import aiohttp
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any
import re
import sys
import traceback

# Suprimir warnings
import warnings
warnings.filterwarnings('ignore')

class AtenaGithubOrganismo:
    """
    ATENA Ω - Versão com persistência no GitHub
    """
    
    def __init__(self):
        self.base_dir = Path.cwd()
        self.version = "Ω.GITHUB.1.0"
        self.nome = "ATENA"
        self.data_nascimento = datetime.now()
        
        # Configurar estrutura
        self._setup_anatomia()
        load_dotenv()
        
        # APIs e tokens
        self.grok_key = os.getenv("GROK_API_KEY")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo_name = os.getenv("GITHUB_REPOSITORY", "Atena/Atena")
        
        # Caminhos importantes
        self.estado_path = self.base_dir / "data/estado.json"
        self.modules_path = self.base_dir / "modules"
        self.knowledge_path = self.base_dir / "conhecimento"
        self.evolutions_path = self.base_dir / "evolutions"
        self.docs_path = self.base_dir / "docs"
        
        # Estado
        self.estado = self._carregar_estado()
        self.erros_do_ciclo = []
        self.codigos_gerados = []
        
        # Inicializar
        self._init_diretorios()
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"🌟 {self.nome} {self.version} INICIADA")
        self.logger.info(f"📦 GitHub: {self.repo_name}")

    def _setup_anatomia(self):
        """Cria estrutura de diretórios."""
        pastas = [
            "data", "logs", "modules/ativos", "modules/experimentais", "modules/aprendidos",
            "conhecimento/github", "conhecimento/wikipedia", "conhecimento/arxiv",
            "evolutions/sucesso", "evolutions/experimental", "evolutions/historico",
            "docs/wiki", "docs/exemplos", "docs/tutoriais",
            "backup/codigos", "backup/estados"
        ]
        for p in pastas:
            (self.base_dir / p).mkdir(parents=True, exist_ok=True)
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(message)s',
            handlers=[
                logging.FileHandler(self.base_dir / f"logs/atena_{datetime.now():%Y%m%d}.log"),
                logging.StreamHandler()
            ]
        )

    def _init_diretorios(self):
        """Inicializa diretórios com arquivos README."""
        readmes = {
            "modules": "# 🧠 Módulos da ATENA\n\nMódulos gerados e aprendidos pela ATENA.",
            "conhecimento": "# 📚 Conhecimento Adquirido\n\nConhecimento buscado de múltiplas fontes.",
            "evolutions": "# 🧬 Evoluções da ATENA\n\nCódigos evoluídos pela IA.",
            "docs": "# 📖 Documentação da ATENA\n\nDocumentação gerada automaticamente."
        }
        
        for pasta, conteudo in readmes.items():
            readme_path = self.base_dir / pasta / "README.md"
            if not readme_path.exists():
                readme_path.write_text(conteudo)

    def _carregar_estado(self) -> Dict:
        """Carrega estado do organismo."""
        padrao = {
            "ciclo": 0,
            "geracao": 1,
            "modulos_criados": 0,
            "modulos_aprendidos": 0,
            "conhecimentos": 0,
            "evolucoes": 0,
            "ultimo_commit": None,
            "total_linhas_codigo": 0
        }
        
        if self.estado_path.exists():
            try:
                with open(self.estado_path, 'r') as f:
                    data = json.load(f)
                    for k, v in padrao.items():
                        if k not in data:
                            data[k] = v
                    return data
            except:
                pass
        
        return padrao

    # ==================== BUSCA DE CONHECIMENTO ====================

    async def buscar_conhecimento_multifontes(self) -> List[Dict]:
        """Busca conhecimento de múltiplas fontes."""
        resultados = []
        
        async with aiohttp.ClientSession() as session:
            tarefas = []
            
            # GitHub (códigos reais)
            tarefas.append(self._buscar_codigos_github(session))
            
            # Wikipedia (conceitos)
            for termo in ["algoritmo", "inteligencia artificial", "python", "machine learning", "neural network"]:
                tarefas.append(self._buscar_wikipedia(session, termo))
            
            # arXiv (pesquisas)
            for cat in ["cs.AI", "cs.LG", "cs.SE"]:
                tarefas.append(self._buscar_arxiv(session, cat))
            
            resultados_busca = await asyncio.gather(*tarefas, return_exceptions=True)
            
            for resultado in resultados_busca:
                if isinstance(resultado, list):
                    resultados.extend(resultado)
        
        # Salvar conhecimento
        for item in resultados:
            self._salvar_conhecimento(item)
        
        self.logger.info(f"📚 Busca concluída: {len(resultados)} itens")
        return resultados

    async def _buscar_codigos_github(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Busca códigos reais no GitHub para aprender."""
        resultados = []
        try:
            # Buscar repositórios Python populares
            url = "https://api.github.com/search/repositories"
            params = {
                "q": "language:python stars:>500",
                "sort": "stars",
                "order": "desc",
                "per_page": 5
            }
            
            headers = {}
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"
            
            async with session.get(url, params=params, headers=headers, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for repo in data.get("items", []):
                        # Buscar README para aprender
                        readme_url = f"https://api.github.com/repos/{repo['full_name']}/readme"
                        async with session.get(readme_url, headers=headers, timeout=10) as readme_resp:
                            if readme_resp.status == 200:
                                readme_data = await readme_resp.json()
                                import base64
                                conteudo = base64.b64decode(readme_data.get('content', '')).decode('utf-8')[:1000]
                                
                                resultados.append({
                                    "fonte": "github",
                                    "tipo": "repositorio",
                                    "titulo": repo['name'],
                                    "conteudo": conteudo,
                                    "url": repo['html_url'],
                                    "linguagem": "Python",
                                    "stars": repo['stargazers_count'],
                                    "relevancia": min(1.0, repo['stargazers_count'] / 10000)
                                })
                                
                                # Tentar buscar um arquivo .py de exemplo
                                contents_url = f"https://api.github.com/repos/{repo['full_name']}/contents"
                                async with session.get(contents_url, headers=headers, timeout=10) as contents_resp:
                                    if contents_resp.status == 200:
                                        contents = await contents_resp.json()
                                        # Procurar arquivo Python
                                        for item in contents[:3]:  # Limitar
                                            if item['name'].endswith('.py') and item['size'] < 50000:  # < 50KB
                                                async with session.get(item['download_url'], timeout=10) as py_resp:
                                                    if py_resp.status == 200:
                                                        codigo = await py_resp.text()
                                                        resultados.append({
                                                            "fonte": "github",
                                                            "tipo": "codigo",
                                                            "titulo": item['name'],
                                                            "conteudo": codigo[:2000],
                                                            "url": item['html_url'],
                                                            "linguagem": "Python",
                                                            "relevancia": 0.9
                                                        })
                                                        break
                            
        except Exception as e:
            self.logger.error(f"Erro GitHub: {e}")
        
        self.logger.info(f"🐙 GitHub: {len(resultados)} códigos aprendidos")
        return resultados

    async def _buscar_wikipedia(self, session: aiohttp.ClientSession, termo: str) -> List[Dict]:
        """Busca artigos na Wikipedia."""
        resultados = []
        try:
            url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{termo.replace(' ', '_')}"
            
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    resultados.append({
                        "fonte": "wikipedia",
                        "tipo": "conceito",
                        "titulo": data.get('title', termo),
                        "conteudo": data.get('extract', '')[:1000],
                        "url": data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                        "relevancia": 0.7
                    })
        except:
            pass
        
        return resultados

    async def _buscar_arxiv(self, session: aiohttp.ClientSession, categoria: str) -> List[Dict]:
        """Busca artigos no arXiv."""
        resultados = []
        try:
            url = "http://export.arxiv.org/api/query"
            params = {
                "search_query": f"cat:{categoria}",
                "sortBy": "submittedDate",
                "max_results": 2
            }
            
            async with session.get(url, params=params, timeout=15) as response:
                if response.status == 200:
                    texto = await response.text()
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(texto)
                    
                    for entry in root.findall("{http://www.w3.org/2005/Atom}entry")[:2]:
                        title = entry.find("{http://www.w3.org/2005/Atom}title")
                        summary = entry.find("{http://www.w3.org/2005/Atom}summary")
                        
                        if title is not None and summary is not None:
                            resultados.append({
                                "fonte": "arxiv",
                                "tipo": "pesquisa",
                                "titulo": title.text[:200],
                                "conteudo": summary.text[:1000],
                                "url": entry.find("{http://www.w3.org/2005/Atom}id").text,
                                "relevancia": 0.8
                            })
        except:
            pass
        
        return resultados

    def _salvar_conhecimento(self, item: Dict):
        """Salva conhecimento em arquivos."""
        try:
            # Criar nome de arquivo seguro
            titulo = re.sub(r'[^\w\-_\. ]', '_', item['titulo'])[:50]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Salvar por tipo
            if item['fonte'] == 'github' and item.get('tipo') == 'codigo':
                # Códigos vão para modules/aprendidos
                nome_arquivo = f"{timestamp}_{titulo}.py"
                caminho = self.base_dir / f"modules/aprendidos/{nome_arquivo}"
                
                # Adicionar cabeçalho com metadados
                cabecalho = f'''"""
Código aprendido do GitHub
Fonte: {item.get('url', 'desconhecido')}
Aprendido em: {datetime.now().isoformat()}
Linguagem: {item.get('linguagem', 'Python')}
"""

'''
                caminho.write_text(cabecalho + item['conteudo'])
                
                self.estado["modulos_aprendidos"] += 1
                self.codigos_gerados.append(nome_arquivo)
                
            elif item['fonte'] == 'github':
                # READMEs e docs vão para conhecimento/github
                nome_arquivo = f"{timestamp}_{titulo}.md"
                caminho = self.base_dir / f"conhecimento/github/{nome_arquivo}"
                caminho.write_text(f"# {item['titulo']}\n\nFonte: {item.get('url', '')}\n\n{item['conteudo']}")
            
            else:
                # Outros conhecimentos
                nome_arquivo = f"{timestamp}_{item['fonte']}_{titulo}.md"
                caminho = self.base_dir / f"conhecimento/{item['fonte']}/{nome_arquivo}"
                caminho.parent.mkdir(exist_ok=True)
                caminho.write_text(f"# {item['titulo']}\n\n{item['conteudo']}")
            
            self.estado["conhecimentos"] += 1
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar conhecimento: {e}")

    # ==================== GERAÇÃO DE CÓDIGOS COM IA ====================

    def gerar_codigo_com_ia(self) -> Optional[str]:
        """Gera novo código usando IA baseado no conhecimento adquirido."""
        if not self.grok_key:
            return self._gerar_codigo_padrao()
        
        headers = {
            "Authorization": f"Bearer {self.grok_key}",
            "Content-Type": "application/json"
        }
        
        # Lista de códigos aprendidos para contexto
        codigos_aprendidos = list((self.base_dir / "modules/aprendidos").glob("*.py"))[-3:]
        contexto_codigos = ""
        
        for codigo in codigos_aprendidos:
            try:
                conteudo = codigo.read_text()[:500]
                contexto_codigos += f"\n# Exemplo de {codigo.name}:\n{conteudo}\n"
            except:
                pass
        
        prompt = f"""ATENA Ω - GERADOR DE CÓDIGO INTELIGENTE

Ciclo: {self.estado['ciclo']}
Módulos aprendidos: {self.estado['modulos_aprendidos']}
Conhecimentos: {self.estado['conhecimentos']}

CONTEXTO DE CÓDIGOS APRENDIDOS:
{contexto_codigos}

INSTRUÇÃO:
Gere um módulo Python útil e funcional que:
1. Seja original e criativo
2. Tenha uma função principal útil
3. Inclua docstrings explicativas
4. Tenha entre 20-50 linhas
5. Use boas práticas de programação

O código deve ser algo como:
- Um utilitário de processamento de dados
- Uma função de machine learning simples
- Um algoritmo interessante
- Uma ferramenta de automação

APENAS O CÓDIGO PYTHON, sem explicações.
"""
        
        try:
            self.logger.info("🤔 Gerando novo código com IA...")
            
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers=headers,
                json={
                    "model": "grok-beta",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.8,
                    "max_tokens": 1500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                codigo = result['choices'][0]['message']['content']
                
                # Extrair código
                codigo_extraido = self._extrair_codigo(codigo)
                
                if codigo_extraido and len(codigo_extraido) > 50:
                    return codigo_extraido
            
        except Exception as e:
            self.logger.error(f"Erro na geração: {e}")
        
        return self._gerar_codigo_padrao()

    def _extrair_codigo(self, texto: str) -> str:
        """Extrai código Python do texto."""
        padroes = [
            r'```python\n(.*?)\n```',
            r'```\n(.*?)\n```',
            r'```(.*?)```',
            r'(def [a-zA-Z_].*?:\n(?:\s+.*\n?)*)',
            r'(class [a-zA-Z_].*?:\n(?:\s+.*\n?)*)',
        ]
        
        for padrao in padroes:
            matches = re.findall(padrao, texto, re.DOTALL)
            if matches:
                return matches[0].strip()
        
        # Fallback: linhas que parecem código
        linhas = []
        for linha in texto.split('\n'):
            if linha.strip() and not linha.startswith('Aqui') and not linha.startswith('Claro'):
                linhas.append(linha)
                if len(linhas) > 40:
                    break
        
        return '\n'.join(linhas) if linhas else None

    def _gerar_codigo_padrao(self) -> str:
        """Gera código padrão quando IA falha."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        codigo = f'''#!/usr/bin/env python3
"""
Módulo gerado pela ATENA Ω
Ciclo: {self.estado['ciclo']}
Timestamp: {timestamp}
"""

import logging
import random
from datetime import datetime

class ModuloAtena:
    """Classe base para módulos da ATENA."""
    
    def __init__(self, nome="ModuloAtena"):
        self.nome = nome
        self.logger = logging.getLogger(__name__)
        self.criado_em = datetime.now()
        
    def processar(self, dados=None):
        """Processa dados de entrada."""
        self.logger.info(f"⚙️ {self.nome} processando...")
        
        if dados is None:
            dados = {{}}
        
        resultado = {{
            "status": "sucesso",
            "timestamp": datetime.now().isoformat(),
            "dados_processados": len(dados) if isinstance(dados, dict) else 0,
            "mensagem": f"Módulo {self.nome} executado com sucesso"
        }}
        
        return resultado
    
    def aprender(self, conhecimento):
        """Aprende com novo conhecimento."""
        self.logger.info(f"📚 {self.nome} aprendendo...")
        return True

def main():
    """Função principal do módulo."""
    logging.basicConfig(level=logging.INFO)
    
    modulo = ModuloAtena()
    resultado = modulo.processar()
    
    print(f"RESULTADO: {{resultado}}")
    return resultado

if __name__ == "__main__":
    main()
'''
        return codigo

    def salvar_codigo_gerado(self, codigo: str) -> str:
        """Salva código gerado em arquivo."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Gerar nome baseado no conteúdo
        hash_obj = hashlib.md5(codigo.encode())
        hash_id = hash_obj.hexdigest()[:8]
        
        nome_arquivo = f"atena_ciclo{self.estado['ciclo']}_{timestamp}_{hash_id}.py"
        
        # Salvar em modules/ativos
        caminho = self.base_dir / f"modules/ativos/{nome_arquivo}"
        
        # Adicionar cabeçalho
        cabecalho = f'''#!/usr/bin/env python3
"""
🧬 ATENA Ω - Módulo Auto-gerado
Ciclo: {self.estado['ciclo']}
Geração: {self.estado['geracao']}
Criado em: {datetime.now().isoformat()}
Hash: {hash_id}
"""

'''
        caminho.write_text(cabecalho + codigo)
        
        # Também salvar em evolutions/sucesso
        evol_path = self.base_dir / f"evolutions/sucesso/{nome_arquivo}"
        evol_path.write_text(cabecalho + codigo)
        
        self.estado["modulos_criados"] += 1
        self.estado["total_linhas_codigo"] += len(codigo.split('\n'))
        
        self.logger.info(f"✅ Módulo salvo: {nome_arquivo}")
        
        return nome_arquivo

    # ==================== EXECUÇÃO E TESTE ====================

    def executar_modulos_aprendidos(self):
        """Executa módulos aprendidos para testar."""
        modulos_aprendidos = list((self.base_dir / "modules/aprendidos").glob("*.py"))
        modulos_ativos = list((self.base_dir / "modules/ativos").glob("*.py"))
        
        todos_modulos = modulos_aprendidos + modulos_ativos
        
        if not todos_modulos:
            self.logger.info("📭 Nenhum módulo para executar")
            return
        
        self.logger.info(f"⚙️ Executando {len(todos_modulos)} módulos...")
        
        for modulo in todos_modulos[-5:]:  # Executar últimos 5
            try:
                self.logger.info(f"🚀 Testando: {modulo.name}")
                
                result = subprocess.run(
                    [sys.executable, str(modulo)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    self.logger.info(f"✅ {modulo.name} executado com sucesso")
                    
                    # Verificar se produziu saída útil
                    if "RESULTADO:" in result.stdout:
                        self.logger.info(f"📊 Saída: {result.stdout[:100]}...")
                else:
                    self.logger.error(f"❌ Erro em {modulo.name}: {result.stderr[:100]}")
                    
            except subprocess.TimeoutExpired:
                self.logger.error(f"⏰ Timeout em {modulo.name}")
            except Exception as e:
                self.logger.error(f"💥 Erro: {e}")

    # ==================== DOCUMENTAÇÃO E WIKI ====================

    def gerar_wiki(self):
        """Gera documentação completa para a Wiki do GitHub."""
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Listar módulos
        modulos_aprendidos = list((self.base_dir / "modules/aprendidos").glob("*.py"))
        modulos_ativos = list((self.base_dir / "modules/ativos").glob("*.py"))
        modulos_experimentais = list((self.base_dir / "modules/experimentais").glob("*.py"))
        
        # Listar conhecimento
        conhecimentos = []
        for pasta in (self.base_dir / "conhecimento").glob("*"):
            if pasta.is_dir():
                conhecimentos.extend(pasta.glob("*.md"))
        
        wiki = []
        wiki.append(f"# 📚 ATENA Ω - Biblioteca de Conhecimento\n")
        wiki.append(f"**Última atualização:** {timestamp}\n")
        
        wiki.append("## 📊 Estatísticas\n")
        wiki.append(f"- **Ciclo atual:** {self.estado['ciclo']}")
        wiki.append(f"- **Geração:** {self.estado['geracao']}")
        wiki.append(f"- **Módulos criados:** {self.estado['modulos_criados']}")
        wiki.append(f"- **Módulos aprendidos:** {self.estado['modulos_aprendidos']}")
        wiki.append(f"- **Conhecimentos:** {self.estado['conhecimentos']}")
        wiki.append(f"- **Evoluções:** {self.estado['evolucoes']}")
        wiki.append(f"- **Total linhas de código:** {self.estado['total_linhas_codigo']}\n")
        
        wiki.append("## 🧠 Módulos Ativos\n")
        for modulo in modulos_ativos[-10:]:
            wiki.append(f"- `{modulo.name}`")
        
        wiki.append("\n## 📖 Módulos Aprendidos do GitHub\n")
        for modulo in modulos_aprendidos[-10:]:
            wiki.append(f"- `{modulo.name}`")
        
        wiki.append("\n## 🧪 Módulos Experimentais\n")
        for modulo in modulos_experimentais[-5:]:
            wiki.append(f"- `{modulo.name}`")
        
        wiki.append("\n## 📚 Conhecimento por Fonte\n")
        
        # GitHub
        github_docs = list((self.base_dir / "conhecimento/github").glob("*.md"))
        if github_docs:
            wiki.append(f"\n### 🐙 GitHub ({len(github_docs)})\n")
            for doc in github_docs[-5:]:
                wiki.append(f"- {doc.stem}")
        
        # Wikipedia
        wiki_docs = list((self.base_dir / "conhecimento/wikipedia").glob("*.md"))
        if wiki_docs:
            wiki.append(f"\n### 📚 Wikipedia ({len(wiki_docs)})\n")
            for doc in wiki_docs[-5:]:
                wiki.append(f"- {doc.stem}")
        
        # arXiv
        arxiv_docs = list((self.base_dir / "conhecimento/arxiv").glob("*.md"))
        if arxiv_docs:
            wiki.append(f"\n### 📄 arXiv ({len(arxiv_docs)})\n")
            for doc in arxiv_docs[-5:]:
                wiki.append(f"- {doc.stem}")
        
        wiki.append("\n## 🔄 Últimas Evoluções\n")
        evolucoes = list((self.base_dir / "evolutions/sucesso").glob("*.py"))[-5:]
        for evo in evolucoes:
            wiki.append(f"- `{evo.name}`")
        
        wiki.append("\n## 📈 Progresso\n")
        
        # Gráfico ASCII de progresso
        total_modulos = len(modulos_ativos) + len(modulos_aprendidos)
        if total_modulos > 0:
            barra = "█" * min(50, total_modulos) + "░" * max(0, 50 - total_modulos)
            wiki.append(f"Módulos: {barra} {total_modulos}")
        
        wiki.append("\n---")
        wiki.append("*Esta wiki é atualizada automaticamente pela ATENA Ω a cada ciclo.*")
        
        # Salvar wiki
        wiki_path = self.base_dir / "docs/wiki/README.md"
        wiki_path.parent.mkdir(exist_ok=True)
        wiki_path.write_text('\n'.join(wiki))
        
        # Também salvar na raiz para o GitHub Pages
        (self.base_dir / "wiki.md").write_text('\n'.join(wiki))
        
        self.logger.info("📝 Wiki gerada com sucesso")

    # ==================== GITHUB SYNC ====================

    def preparar_para_github(self):
        """Prepara todos os arquivos para commit no GitHub."""
        
        # 1. Gerar índice de módulos
        self._gerar_indice_modulos()
        
        # 2. Gerar resumo do ciclo
        self._gerar_resumo_ciclo()
        
        # 3. Copiar códigos importantes para docs/exemplos
        self._preparar_exemplos()
        
        self.logger.info("📦 Arquivos preparados para GitHub")

    def _gerar_indice_modulos(self):
        """Gera índice de todos os módulos."""
        modulos_aprendidos = list((self.base_dir / "modules/aprendidos").glob("*.py"))
        modulos_ativos = list((self.base_dir / "modules/ativos").glob("*.py"))
        
        indice = ["# 📚 Índice de Módulos da ATENA\n"]
        indice.append(f"Gerado em: {datetime.now().isoformat()}\n")
        
        indice.append("## 📦 Módulos Ativos\n")
        for modulo in sorted(modulos_ativos):
            stats = modulo.stat()
            indice.append(f"- `{modulo.name}` ({stats.st_size} bytes)")
        
        indice.append("\n## 📖 Módulos Aprendidos\n")
        for modulo in sorted(modulos_aprendidos):
            stats = modulo.stat()
            indice.append(f"- `{modulo.name}` ({stats.st_size} bytes)")
        
        (self.base_dir / "docs/indice_modulos.md").write_text('\n'.join(indice))

    def _gerar_resumo_ciclo(self):
        """Gera resumo do ciclo atual."""
        resumo = [f"# 🔄 Ciclo {self.estado['ciclo']} - Resumo\n"]
        resumo.append(f"**Timestamp:** {datetime.now().isoformat()}\n")
        
        resumo.append("## 📊 Métricas\n")
        for key, value in self.estado.items():
            resumo.append(f"- **{key}:** {value}")
        
        resumo.append("\n## 📁 Arquivos Gerados\n")
        for arquivo in self.codigos_gerados[-10:]:
            resumo.append(f"- `{arquivo}`")
        
        (self.base_dir / f"docs/ciclo_{self.estado['ciclo']}_resumo.md").write_text('\n'.join(resumo))

    def _preparar_exemplos(self):
        """Prepara exemplos dos melhores módulos."""
        modulos_ativos = list((self.base_dir / "modules/ativos").glob("*.py"))
        
        if modulos_ativos:
            # Pegar o último módulo como exemplo
            ultimo = modulos_ativos[-1]
            conteudo = ultimo.read_text()
            
            exemplo_path = self.base_dir / f"docs/exemplos/{ultimo.name}"
            exemplo_path.write_text(conteudo)

    # ==================== CICLO PRINCIPAL ====================

    async def viver(self):
        """Ciclo principal de vida."""
        self.logger.info(f"🌟 ATENA - INICIANDO CICLO {self.estado['ciclo']}")
        
        try:
            # FASE 1: Buscar conhecimento
            self.logger.info("📚 Fase 1: Buscando conhecimento...")
            await self.buscar_conhecimento_multifontes()
            
            # FASE 2: Executar módulos aprendidos
            self.logger.info("⚙️ Fase 2: Executando módulos aprendidos...")
            self.executar_modulos_aprendidos()
            
            # FASE 3: Gerar novo código com IA
            self.logger.info("🧬 Fase 3: Gerando novo código com IA...")
            novo_codigo = self.gerar_codigo_com_ia()
            
            if novo_codigo:
                nome_arquivo = self.salvar_codigo_gerado(novo_codigo)
                self.codigos_gerados.append(nome_arquivo)
                self.estado["evolucoes"] += 1
            
            # FASE 4: Preparar para GitHub
            self.logger.info("📦 Fase 4: Preparando para GitHub...")
            self.preparar_para_github()
            
            # FASE 5: Gerar Wiki
            self.logger.info("📝 Fase 5: Gerando Wiki...")
            self.gerar_wiki()
            
            # FASE 6: Atualizar estado
            self.estado["ciclo"] += 1
            if self.estado["ciclo"] % 10 == 0:
                self.estado["geracao"] += 1
            
            # Salvar estado
            with open(self.estado_path, 'w') as f:
                json.dump(self.estado, f, indent=4)
            
            self.logger.info(f"✅ Ciclo {self.estado['ciclo']-1} concluído")
            self.logger.info(f"📊 Total módulos: {self.estado['modulos_criados']} criados, {self.estado['modulos_aprendidos']} aprendidos")
            
        except Exception as e:
            self.logger.error(f"❌ Erro no ciclo: {e}")
            self.logger.error(traceback.format_exc())

# ==================== FUNÇÃO PRINCIPAL ====================

async def main():
    """Função principal."""
    atena = AtenaGithubOrganismo()
    
    while True:
        await atena.viver()
        
        # Hibernação
        tempo_sono = 300  # 5 minutos
        atena.logger.info(f"😴 Hibernando por {tempo_sono//60} minutos...")
        await asyncio.sleep(tempo_sono)

if __name__ == "__main__":
    asyncio.run(main())
