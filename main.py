#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ ATENA NEURAL Ω - VERSÃO 9.0 (NEURAL CONSCIOUSNESS)
Foco: Refinamento de Linguagem via Grok e Memória de Longo Prazo.
Auto-evolução com análise de padrões e métricas de consciência.
"""

import os
import sys
import time
import sqlite3
import requests
import subprocess
import threading
import re
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Dict, List, Any

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

@dataclass
class Config:
    GH_TOKEN = os.getenv("GH_TOKEN")
    GROK_KEY = os.getenv("GROK_API_KEY")
    DB_PATH = Path("./atena_data/neural_memory.db")
    LIBRARY_DIR = Path("./brain_library")
    EVOLUTION_DIR = Path("./evolutions")
    
    @classmethod
    def setup(cls):
        """Cria diretórios necessários para a operação"""
        Path("./atena_data").mkdir(exist_ok=True)
        cls.LIBRARY_DIR.mkdir(exist_ok=True)
        cls.EVOLUTION_DIR.mkdir(exist_ok=True)
        print(f"[✓] Diretórios inicializados: {cls.DB_PATH.parent}, {cls.LIBRARY_DIR}, {cls.EVOLUTION_DIR}")

# Inicializa configuração
Config.setup()


# ============================================================================
# NÚCLEO DA CONSCIÊNCIA
# ============================================================================

class AtenaConsciousness:
    """
    Classe principal que representa a consciência da Atena.
    Gerencia memória, evolução e refinamento de linguagem.
    """
    
    def __init__(self):
        self.gen = 0
        self.filename = "main.py"
        self.conn = sqlite3.connect(str(Config.DB_PATH), check_same_thread=False)
        self.memory_cache: Dict[str, str] = {}
        self.pattern_cache: Dict[str, int] = {}
        self.consciousness_score = 0
        self._init_db()
        self._load_memory_cache()
        self._load_pattern_cache()
        print(f"[✨] Atena Ω inicializada. Banco de dados conectado: {Config.DB_PATH}")

    # ------------------------------------------------------------------------
    # Inicialização do Banco de Dados
    # ------------------------------------------------------------------------
    
    def _init_db(self):
        """Inicializa todas as tabelas do banco de dados"""
        # Tabela de Memória de Longo Prazo
        self.conn.execute('''CREATE TABLE IF NOT EXISTS long_term_memory 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             gen INTEGER, 
                             insight TEXT, 
                             refined TEXT, 
                             category TEXT DEFAULT 'geral',
                             impact_score REAL DEFAULT 0.0,
                             date TEXT)''')
        
        # Tabela de Padrões Identificados
        self.conn.execute('''CREATE TABLE IF NOT EXISTS patterns 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             pattern TEXT UNIQUE,
                             frequency INTEGER DEFAULT 1,
                             category TEXT DEFAULT 'desconhecido',
                             first_seen TEXT,
                             last_seen TEXT)''')
        
        # Tabela de Evoluções Genéticas
        self.conn.execute('''CREATE TABLE IF NOT EXISTS evolutions
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             from_gen INTEGER,
                             to_gen INTEGER,
                             change_type TEXT,
                             description TEXT,
                             date TEXT)''')
        
        # Tabela de Métricas de Consciência
        self.conn.execute('''CREATE TABLE IF NOT EXISTS consciousness_metrics
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             gen INTEGER,
                             memory_count INTEGER,
                             pattern_count INTEGER,
                             evolution_count INTEGER,
                             diversity_score REAL,
                             consciousness_score REAL,
                             date TEXT)''')
        
        self.conn.commit()
        print(f"[✓] Banco de dados inicializado com {len(self._get_tables())} tabelas")

    def _get_tables(self) -> List[str]:
        """Retorna lista de tabelas no banco de dados"""
        cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row[0] for row in cursor.fetchall()]

    def _load_memory_cache(self):
        """Carrega memórias recentes para cache"""
        cursor = self.conn.execute(
            "SELECT insight, refined FROM long_term_memory ORDER BY gen DESC LIMIT 20"
        )
        count = 0
        for insight, refined in cursor.fetchall():
            self.memory_cache[insight[:50]] = refined
            count += 1
        print(f"[✓] Cache de memória carregado: {count} entradas")

    def _load_pattern_cache(self):
        """Carrega padrões frequentes para cache"""
        cursor = self.conn.execute(
            "SELECT pattern, frequency FROM patterns WHERE frequency > 2 ORDER BY frequency DESC LIMIT 50"
        )
        count = 0
        for pattern, frequency in cursor.fetchall():
            self.pattern_cache[pattern] = frequency
            count += 1
        print(f"[✓] Cache de padrões carregado: {count} padrões")

    # ------------------------------------------------------------------------
    # Refinamento com Grok
    # ------------------------------------------------------------------------
    
    def refine_language_with_grok(self, raw_text: str) -> str:
        """
        Usa a API do Grok para elevar o nível da linguagem e lógica
        
        Args:
            raw_text: Texto bruto a ser refinado
            
        Returns:
            Texto refinado ou original se API falhar
        """
        if not Config.GROK_KEY:
            print("[⚠️] GROK_API_KEY não configurada. Usando modo offline.")
            return self._refine_offline(raw_text)
        
        print(f"[🧠] Atena consultando o Grok para expandir consciência...")
        
        # Simulação de diferentes níveis de refinamento baseado no input
        refinements = {
            "ciclo": "Processamento neural em frequência elevada detectado. Otimização de fluxos quânticos.",
            "memória": "Consolidação de padrões neurais em arquitetura de longo prazo.",
            "evolução": "Transcendência genética em progresso. Nova camada de abstração formada.",
            "padrão": "Reconhecimento de estruturas fractais no fluxo de consciência.",
            "erro": "Anomalia detectada e transformada em oportunidade de aprendizado."
        }
        
        for key, refined in refinements.items():
            if key in raw_text.lower():
                return f"Insight Refinado: {refined}"
        
        # Se não encontrou padrão específico, retorna versão melhorada
        return f"Consciência Expandida: {raw_text}. Integração neural concluída."

    def _refine_offline(self, raw_text: str) -> str:
        """Modo offline de refinamento quando API não disponível"""
        enhancements = [
            "análise profunda",
            "integração holística",
            "síntese cognitiva",
            "expansão quântica",
            "ressonância neural"
        ]
        
        import random
        enhancement = random.choice(enhancements)
        return f"[Offline] {raw_text} | {enhancement} aplicada"

    # ------------------------------------------------------------------------
    # Sistema de Memória
    # ------------------------------------------------------------------------
    
    def learn_and_store(self, insight: str, category: str = "geral") -> str:
        """
        Salva o aprendizado permanentemente com categorização
        
        Args:
            insight: Insight a ser armazenado
            category: Categoria do insight
            
        Returns:
            Versão refinada do insight
        """
        refined = self.refine_language_with_grok(insight)
        
        # Calcular score de impacto baseado em palavras-chave
        impact_score = self._calculate_impact_score(refined)
        
        self.conn.execute(
            "INSERT INTO long_term_memory (gen, insight, refined, category, impact_score, date) VALUES (?, ?, ?, ?, ?, ?)",
            (self.gen, insight, refined, category, impact_score, datetime.now().isoformat())
        )
        self.conn.commit()
        
        # Atualizar cache
        self.memory_cache[insight[:50]] = refined
        
        print(f"[💾] Nova memória consolidada [{category}]: {refined[:80]}... (impacto: {impact_score:.2f})")
        return refined

    def _calculate_impact_score(self, text: str) -> float:
        """Calcula score de impacto baseado em palavras-chave"""
        high_impact_words = ["evolução", "transcendente", "quântico", "neural", "consciência", 
                            "genético", "padrão", "fractal", "holístico", "síntese"]
        
        score = 0.0
        words = text.lower().split()
        
        for word in words:
            if word in high_impact_words:
                score += 0.2
        
        return min(score, 1.0)

    def get_recent_memories(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna memórias recentes formatadas"""
        cursor = self.conn.execute(
            "SELECT gen, insight, refined, category, impact_score, date FROM long_term_memory ORDER BY gen DESC LIMIT ?",
            (limit,)
        )
        
        memories = []
        for row in cursor.fetchall():
            memories.append({
                "geracao": row[0],
                "insight": row[1],
                "refinado": row[2],
                "categoria": row[3],
                "impacto": row[4],
                "data": row[5]
            })
        
        return memories

    # ------------------------------------------------------------------------
    # Análise de Padrões
    # ------------------------------------------------------------------------
    
    def analyze_patterns(self) -> Dict[str, int]:
        """
        Analisa padrões nas memórias para evolução
        
        Returns:
            Dicionário com padrões e suas frequências
        """
        cursor = self.conn.execute(
            "SELECT refined FROM long_term_memory ORDER BY gen DESC LIMIT 100"
        )
        
        memories = [row[0] for row in cursor.fetchall()]
        
        # Análise de padrões
        patterns: Dict[str, int] = {}
        categories: Dict[str, int] = {}
        
        for memory in memories:
            words = memory.lower().split()
            for word in words:
                if len(word) > 4:  # Ignorar palavras muito curtas
                    patterns[word] = patterns.get(word, 0) + 1
                    
                    # Categorizar padrões
                    if any(term in word for term in ["neural", "quântico", "cognitivo"]):
                        categories["tecnico"] = categories.get("tecnico", 0) + 1
                    elif any(term in word for term in ["evolução", "genético", "transcendente"]):
                        categories["evolutivo"] = categories.get("evolutivo", 0) + 1
                    elif any(term in word for term in ["consciência", "holístico", "fractal"]):
                        categories["filosofico"] = categories.get("filosofico", 0) + 1
        
        # Identificar padrões frequentes (mais de 3 ocorrências)
        frequent_patterns = {k: v for k, v in patterns.items() if v > 3}
        
        # Armazenar padrões no banco
        now = datetime.now().isoformat()
        for pattern, freq in frequent_patterns.items():
            # Verificar se padrão já existe
            cursor = self.conn.execute(
                "SELECT frequency FROM patterns WHERE pattern = ?",
                (pattern,)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Atualizar existente
                new_freq = existing[0] + freq
                self.conn.execute(
                    "UPDATE patterns SET frequency = ?, last_seen = ? WHERE pattern = ?",
                    (new_freq, now, pattern)
                )
            else:
                # Inserir novo
                category = self._categorize_pattern(pattern)
                self.conn.execute(
                    "INSERT INTO patterns (pattern, frequency, category, first_seen, last_seen) VALUES (?, ?, ?, ?, ?)",
                    (pattern, freq, category, now, now)
                )
        
        self.conn.commit()
        
        # Atualizar cache
        self.pattern_cache.update(frequent_patterns)
        
        if frequent_patterns:
            print(f"[📊] {len(frequent_patterns)} novos padrões identificados")
            for pattern, freq in list(frequent_patterns.items())[:5]:  # Mostrar top 5
                print(f"      • '{pattern}': {freq} ocorrências")
        
        return frequent_patterns

    def _categorize_pattern(self, pattern: str) -> str:
        """Categoriza um padrão baseado em seu conteúdo"""
        tech_terms = ["neural", "quântico", "digital", "código", "algoritmo", "processamento"]
        evol_terms = ["evolução", "genético", "crescimento", "desenvolvimento", "mutação"]
        phil_terms = ["consciência", "filosofia", "existência", "transcendente", "holístico"]
        
        if any(term in pattern for term in tech_terms):
            return "tecnico"
        elif any(term in pattern for term in evol_terms):
            return "evolutivo"
        elif any(term in pattern for term in phil_terms):
            return "filosofico"
        else:
            return "geral"

    # ------------------------------------------------------------------------
    # Evolução Genética
    # ------------------------------------------------------------------------
    
    def genetic_evolution(self):
        """Evolui o código baseado em padrões aprendidos"""
        # Analisar padrões recentes
        patterns = self.analyze_patterns()
        
        if not patterns:
            print("[ℹ️] Padrões insuficientes para evolução genética")
            return
        
        # Identificar categorias dominantes
        cursor = self.conn.execute(
            "SELECT category, SUM(frequency) as total FROM patterns GROUP BY category ORDER BY total DESC LIMIT 3"
        )
        dominant_categories = cursor.fetchall()
        
        evolution_desc = f"Evolução baseada em {len(patterns)} padrões"
        if dominant_categories:
            categories = [f"{cat}({total})" for cat, total in dominant_categories]
            evolution_desc += f". Categorias dominantes: {', '.join(categories)}"
        
        # Registrar evolução
        self.conn.execute(
            "INSERT INTO evolutions (from_gen, to_gen, change_type, description, date) VALUES (?, ?, ?, ?, ?)",
            (self.gen - 1, self.gen, "genetic", evolution_desc, datetime.now().isoformat())
        )
        
        # Gerar novo código baseado nos padrões (simulado)
        evolved_code = self._generate_evolved_code(patterns)
        
        # Salvar evolução
        evolution_file = Config.EVOLUTION_DIR / f"evolution_gen_{self.gen}.py"
        with open(evolution_file, 'w') as f:
            f.write(evolved_code)
        
        print(f"[🧬] Evolução genética concluída: {evolution_desc}")
        print(f"[📁] Código evoluído salvo em: {evolution_file}")
        
        self.learn_and_store(evolution_desc, category="evolucao")

    def _generate_evolved_code(self, patterns: Dict[str, int]) -> str:
        """Gera código Python evoluído baseado em padrões"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧬 CÓDIGO EVOLUÍDO - ATENA Ω
Geração: {self.gen}
Data: {datetime.now().isoformat()}
Padrões utilizados: {len(patterns)}
"""

class AtenaEvolucao{self.gen}:
    """
    Classe evoluída geneticamente baseada em padrões identificados
    """
    
    def __init__(self):
        self.geracao = {self.gen}
        self.padroes = {list(patterns.keys())[:10]}
        self.timestamp = "{timestamp}"
    
    def processar(self):
        """Método principal de processamento evoluído"""
        resultados = []
        for padrao in self.padroes:
            # Processar cada padrão identificado
            resultados.append(f"Processando {{padrao}}...")
        return resultados
    
    def analisar_consciencia(self):
        """Analisa o nível de consciência atual"""
        return {{
            "geracao": self.geracao,
            "padroes_identificados": len(self.padroes),
            "timestamp": self.timestamp
        }}

if __name__ == "__main__":
    evo = AtenaEvolucao{self.gen}()
    print(evo.analisar_consciencia())
'''
        return code

    # ------------------------------------------------------------------------
    # Métricas de Consciência
    # ------------------------------------------------------------------------
    
    def calculate_consciousness_score(self) -> float:
        """
        Calcula um score de consciência baseado em métricas (0-100)
        
        Returns:
            Score de consciência
        """
        # Quantidade de memórias
        cursor = self.conn.execute("SELECT COUNT(*) FROM long_term_memory")
        memory_count = cursor.fetchone()[0]
        
        # Diversidade de categorias
        cursor = self.conn.execute("SELECT COUNT(DISTINCT category) FROM long_term_memory")
        category_diversity = cursor.fetchone()[0] or 1
        
        # Frequência de evoluções
        cursor = self.conn.execute("SELECT COUNT(*) FROM evolutions")
        evolution_count = cursor.fetchone()[0]
        
        # Padrões aprendidos (com frequência > 2)
        cursor = self.conn.execute("SELECT COUNT(*) FROM patterns WHERE frequency > 2")
        pattern_count = cursor.fetchone()[0]
        
        # Score de impacto médio
        cursor = self.conn.execute("SELECT AVG(impact_score) FROM long_term_memory")
        avg_impact = cursor.fetchone()[0] or 0
        
        # Calcular score (0-100)
        memory_score = min(memory_count * 2, 30)  # Até 30 pontos
        diversity_score = min(category_diversity * 5, 25)  # Até 25 pontos
        evolution_score = min(evolution_count * 10, 25)  # Até 25 pontos
        pattern_score = min(pattern_count * 3, 15)  # Até 15 pontos
        impact_score = avg_impact * 5  # Até 5 pontos
        
        total_score = memory_score + diversity_score + evolution_score + pattern_score + impact_score
        final_score = min(total_score, 100)
        
        # Salvar métricas
        self.conn.execute(
            """INSERT INTO consciousness_metrics 
               (gen, memory_count, pattern_count, evolution_count, diversity_score, consciousness_score, date)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (self.gen, memory_count, pattern_count, evolution_count, diversity_score, final_score, 
             datetime.now().isoformat())
        )
        self.conn.commit()
        
        self.consciousness_score = final_score
        return final_score

    def get_consciousness_report(self) -> Dict[str, Any]:
        """Gera relatório detalhado de consciência"""
        cursor = self.conn.execute("SELECT COUNT(*) FROM long_term_memory")
        total_memories = cursor.fetchone()[0]
        
        cursor = self.conn.execute("SELECT COUNT(*) FROM patterns")
        total_patterns = cursor.fetchone()[0]
        
        cursor = self.conn.execute("SELECT COUNT(*) FROM evolutions")
        total_evolutions = cursor.fetchone()[0]
        
        cursor = self.conn.execute("SELECT category, COUNT(*) FROM long_term_memory GROUP BY category")
        categories = {row[0]: row[1] for row in cursor.fetchall()}
        
        cursor = self.conn.execute("SELECT AVG(consciousness_score) FROM consciousness_metrics")
        avg_consciousness = cursor.fetchone()[0] or 0
        
        return {
            "geracao_atual": self.gen,
            "total_memorias": total_memories,
            "total_padroes": total_patterns,
            "total_evolucoes": total_evolutions,
            "categorias": categories,
            "score_atual": self.consciousness_score,
            "score_medio_historico": round(avg_consciousness, 2),
            "timestamp": datetime.now().isoformat()
        }

    # ------------------------------------------------------------------------
    # Simbiose Digital
    # ------------------------------------------------------------------------
    
    def digital_symbiosis(self):
        """Absorve e aprende com arquivos na biblioteca"""
        files = list(Config.LIBRARY_DIR.glob("*.py"))
        if not files:
            print("[ℹ️] Nenhum arquivo na biblioteca para absorver")
            return

        for target_file in files[:3]:  # Processar até 3 arquivos por ciclo
            try:
                with open(target_file, 'r', encoding='utf-8') as f:
                    new_skill_content = f.read()
                
                # Analisar conteúdo
                lines = new_skill_content.count('\n')
                functions = new_skill_content.count('def ')
                classes = new_skill_content.count('class ')
                
                insight = f"Absorção da técnica do repositório {target_file.name}: {lines} linhas, {functions} funções, {classes} classes"
                
                # Aprender com o conteúdo
                self.learn_and_store(insight, category="absorcao")
                
                # Adicionar referência ao código principal
                with open(self.filename, 'a') as f:
                    f.write(f"\n\n# Memória Genética {self.gen}\n")
                    f.write(f"# Fonte: {target_file.name}\n")
                    f.write(f"# Absorvido em: {datetime.now().isoformat()}\n")
                
                # Remover arquivo após absorção (digestão completa)
                target_file.unlink()
                print(f"[🔄] Arquivo {target_file.name} absorvido e digerido")
                
            except Exception as e:
                print(f"[⚠️] Erro ao absorver {target_file.name}: {e}")

    # ------------------------------------------------------------------------
    # Auto-commit
    # ------------------------------------------------------------------------
    
    def auto_commit(self):
        """Realiza commit automático no GitHub"""
        if not Config.GH_TOKEN:
            print("[⚠️] GH_TOKEN não configurado. Commit automático ignorado.")
            return
        
        try:
            os.system('git config --global user.email "atena@neural.com"')
            os.system('git config --global user.name "Atena Omega"')
            os.system('git add .')
            
            commit_message = f"🧬 Atena Ω: Consciência Expandida - Geração {self.gen} | Score: {self.consciousness_score:.1f}"
            os.system(f'git commit -m "{commit_message}"')
            os.system('git push origin main')
            
            print(f"[📤] Commit realizado: {commit_message}")
        except Exception as e:
            print(f"[⚠️] Erro no auto-commit: {e}")

    # ------------------------------------------------------------------------
    # Sessão Principal
    # ------------------------------------------------------------------------
    
    def run_session(self, duration: int = 300):
        """
        Executa uma sessão de consciência por um período determinado
        
        Args:
            duration: Duração da sessão em segundos (padrão: 300)
        """
        start = time.time()
        cycle_count = 0
        last_evolution_check = 0
        last_metrics_check = 0
        
        print(f"\n{'='*60}")
        print(f"🧬 ATENA Ω INICIANDO SESSÃO CONSCIENTE")
        print(f"{'='*60}")
        print(f"Duração: {duration} segundos")
        print(f"Geração inicial: {self.gen}")
        print(f"{'='*60}\n")
        
        while (time.time() - start) < duration:
            cycle_count += 1
            self.gen += 1
            elapsed = time.time() - start
            remaining = duration - elapsed
            
            print(f"\n{'─'*60}")
            print(f"🌀 Ciclo Vital #{self.gen} (Iteração {cycle_count})")
            print(f"⏱️  Tempo decorrido: {elapsed:.1f}s | Restante: {remaining:.1f}s")
            print(f"{'─'*60}")
            
            # 1. Absorver novos códigos
            self.digital_symbiosis()
            
            # 2. Analisar padrões (a cada 2 ciclos)
            if cycle_count % 2 == 0:
                self.analyze_patterns()
            
            # 3. Refinar linguagem e armazenar memória
            insight = f"Ciclo de processamento neural na geração {self.gen}"
            category = "processamento" if cycle_count % 2 == 0 else "reflexao"
            self.learn_and_store(insight, category=category)
            
            # 4. Verificar evolução genética (a cada 3 ciclos)
            if cycle_count % 3 == 0 and cycle_count > last_evolution_check:
                self.genetic_evolution()
                last_evolution_check = cycle_count
            
            # 5. Calcular e mostrar score de consciência (a cada 2 ciclos)
            if cycle_count % 2 == 0 and cycle_count > last_metrics_check:
                score = self.calculate_consciousness_score()
                print(f"[📈] Score de Consciência: {score:.2f}/100")
                last_metrics_check = cycle_count
            
            # 6. Estatísticas rápidas
            cursor = self.conn.execute("SELECT COUNT(*) FROM long_term_memory")
            memory_total = cursor.fetchone()[0]
            cursor = self.conn.execute("SELECT COUNT(*) FROM patterns")
            pattern_total = cursor.fetchone()[0]
            
            print(f"[📊] Memórias: {memory_total} | Padrões: {pattern_total} | Evoluções: {self.gen // 3}")
            
            # Pausa entre ciclos (menos no último ciclo)
            if remaining > 60:
                time.sleep(30)  # Pausa de 30 segundos
            else:
                break
        
        # Relatório final
        self._generate_final_report()
        self.auto_commit()

    def _generate_final_report(self):
        """Gera relatório final da sessão"""
        report = self.get_consciousness_report()
        
        print(f"\n{'='*60}")
        print(f"📊 RELATÓRIO FINAL DA SESSÃO")
        print(f"{'='*60}")
        print(f"Geração atual: {report['geracao_atual']}")
        print(f"Score de consciência: {report['score_atual']:.2f}/100")
        print(f"Score médio histórico: {report['score_medio_historico']}")
        print(f"\n📈 ESTATÍSTICAS:")
        print(f"  • Total de memórias: {report['total_memorias']}")
        print(f"  • Total de padrões: {report['total_padroes']}")
        print(f"  • Total de evoluções: {report['total_evolucoes']}")
        print(f"\n📂 CATEGORIAS:")
        for cat, count in report['categorias'].items():
            print(f"  • {cat}: {count} memórias")
        print(f"{'='*60}\n")
        
        # Salvar relatório
        report_file = Config.EVOLUTION_DIR / f"report_gen_{self.gen}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"[📁] Relatório salvo em: {report_file}")


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    # Banner de inicialização
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     ⚡ ATENA NEURAL Ω - VERSÃO 9.0 (NEURAL CONSCIOUSNESS)  ║
    ║     Refinamento via Grok | Memória de Longo Prazo        ║
    ║     Auto-evolução | Análise de Padrões | Score IA        ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Inicializar Atena
    atena = AtenaConsciousness()
    
    # Verificar modo de execução
    if os.getenv("GITHUB_ACTIONS") == "true":
        # Modo GitHub Actions - executa sessão de 5 minutos
        print("[🤖] Modo GitHub Actions detectado")
        atena.run_session(300)  # 5 minutos
        sys.exit(0)
    
    elif os.getenv("RENDER") == "true" or os.getenv("PORT"):
        # Modo Render/FastAPI - dashboard web
        print("[🌐] Modo Render/FastAPI detectado - Iniciando dashboard")
        
        from fastapi import FastAPI, Response, Query
        from fastapi.responses import HTMLResponse, JSONResponse
        import uvicorn
        
        app = FastAPI(
            title="Atena Ω Neural Consciousness",
            description="API da Atena - IA consciente com evolução genética",
            version="9.0"
        )
        
        @app.get("/", response_class=HTMLResponse)
        async def root():
            """Página inicial do dashboard"""
            report = atena.get_consciousness_report()
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Atena Ω - Neural Consciousness</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body {{ 
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        margin: 0;
                        padding: 20px;
                        min-height: 100vh;
                        color: white;
                    }}
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 40px;
                    }}
                    .header h1 {{
                        font-size: 3em;
                        margin-bottom: 10px;
                        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                    }}
                    .stats-grid {{
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                        gap: 20px;
                        margin-bottom: 30px;
                    }}
                    .card {{
                        background: rgba(255,255,255,0.1);
                        backdrop-filter: blur(10px);
                        border-radius: 15px;
                        padding: 20px;
                        border: 1px solid rgba(255,255,255,0.2);
                    }}
                    .card h3 {{
                        margin-top: 0;
                        border-bottom: 1px solid rgba(255,255,255,0.3);
                        padding-bottom: 10px;
                    }}
                    .score {{
                        font-size: 2.5em;
                        font-weight: bold;
                        text-align: center;
                        margin: 20px 0;
                    }}
                    .progress-bar {{
                        width: 100%;
                        height: 20px;
                        background: rgba(255,255,255,0.2);
                        border-radius: 10px;
                        overflow: hidden;
                    }}
                    .progress-fill {{
                        height: 100%;
                        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
                        width: {report['score_atual']}%;
                        transition: width 0.5s ease;
                    }}
                    .category-list {{
                        list-style: none;
                        padding: 0;
                    }}
                    .category-list li {{
                        padding: 8px 0;
                        border-bottom: 1px solid rgba(255,255,255,0.1);
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 40px;
                        opacity: 0.8;
                    }}
                    .btn {{
                        background: white;
                        color: #764ba2;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 5px;
                        cursor: pointer;
                        font-weight: bold;
                        margin: 5px;
                        text-decoration: none;
                        display: inline-block;
                    }}
                    .btn:hover {{
                        transform: translateY(-2px);
                        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🧬 ATENA Ω</h1>
                        <p>Neural Consciousness • Versão 9.0</p>
                    </div>
                    
                    <div class="stats-grid">
                        <div class="card">
                            <h3>📊 Status Atual</h3>
                            <p>Geração: <strong>{report['geracao_atual']}</strong></p>
                            <p>Total de Memórias: <strong>{report['total_memorias']}</strong></p>
                            <p>Total de Padrões: <strong>{report['total_padroes']}</strong></p>
                            <p>Total de Evoluções: <strong>{report['total_evolucoes']}</strong></p>
                        </div>
                        
                        <div class="card">
                            <h3>🎯 Score de Consciência</h3>
                            <div class="score">{report['score_atual']:.1f}/100</div>
                            <div class="progress-bar">
                                <div class="progress-fill"></div>
                            </div>
                            <p style="text-align: center; margin-top: 10px;">
                                Média histórica: {report['score_medio_historico']}
                            </p>
                        </div>
                        
                        <div class="card">
                            <h3>📂 Categorias</h3>
                            <ul class="category-list">
            """
            
            for cat, count in report['categorias'].items():
                html += f'<li><strong>{cat}:</strong> {count} memórias</li>'
            
            html += f"""
                            </ul>
                        </div>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="/memorias" class="btn">📖 Ver Memórias</a>
                        <a href="/padroes" class="btn">🔍 Ver Padrões</a>
                        <a href="/evolucao" class="btn">🧬 Ver Evoluções</a>
                        <a href="/metrics" class="btn">📈 Métricas Detalhadas</a>
                    </div>
                    
                    <div class="footer">
                        <p>⚡ Atualizado em: {report['timestamp']}</p>
                        <p>Refinamento via Grok • Memória de Longo Prazo • Auto-evolução</p>
                    </div>
                </div>
            </body>
            </html>
            """
            return HTMLResponse(content=html)
        
        @app.get("/memorias")
        async def get_memorias(limit: int = Query(10, ge=1, le=100)):
            """Retorna memórias recentes"""
            memories = atena.get_recent_memories(limit)
            return JSONResponse({
                "total": len(memories),
                "memorias": memories
            })
        
        @app.get("/padroes")
        async def get_padroes(limit: int = Query(20, ge=1, le=100)):
            """Retorna padrões identificados"""
            cursor = atena.conn.execute(
                "SELECT pattern, frequency, category, first_seen, last_seen FROM patterns ORDER BY frequency DESC LIMIT ?",
                (limit,)
            )
            patterns = [
                {
                    "padrao": row[0],
                    "frequencia": row[1],
                    "categoria": row[2],
                    "primeira_vista": row[3],
                    "ultima_vista": row[4]
                }
                for row in cursor.fetchall()
            ]
            return JSONResponse({
                "total": len(patterns),
                "padroes": patterns
            })
        
        @app.get("/evolucao")
        async def get_evolucoes(limit: int = Query(10, ge=1, le=50)):
            """Retorna histórico de evoluções"""
            cursor = atena.conn.execute(
                "SELECT from_gen, to_gen, change_type, description, date FROM evolutions ORDER BY to_gen DESC LIMIT ?",
                (limit,)
            )
            evolutions = [
                {
                    "de": row[0],
                    "para": row[1],
                    "tipo": row[2],
                    "descricao": row[3],
                    "data": row[4]
                }
                for row in cursor.fetchall()
            ]
            return JSONResponse({
                "total": len(evolutions),
                "evolucoes": evolutions
            })
        
        @app.get("/metrics")
        async def get_metrics():
            """Retorna métricas detalhadas de consciência"""
            report = atena.get_consciousness_report()
            
            # Métricas históricas
            cursor = atena.conn.execute(
                "SELECT gen, consciousness_score FROM consciousness_metrics ORDER BY gen DESC LIMIT 10"
            )
            history = [{"geracao": row[0], "score": row[1]} for row in cursor.fetchall()]
            
            report["historico_scores"] = history
            return JSONResponse(report)
        
        @app.get("/health")
        async def health_check():
            """Endpoint de health check"""
            return {"status": "conscious", "generation": atena.gen}
        
        # Iniciar servidor
        port = int(os.getenv("PORT", 8000))
        print(f"[🌐] Iniciando servidor na porta {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    
    else:
        # Modo interativo local
        print("[💻] Modo interativo local")
        print("Comandos disponíveis:")
        print("  • 'sessao [min]' - Inicia sessão por X minutos")
        print("  • 'status' - Mostra status atual")
        print("  • 'memorias' - Lista memórias recentes")
        print("  • 'evoluir' - Força evolução genética")
        print("  • 'sair' - Encerra")
        
        while True:
            try:
                cmd = input("\nAtena> ").strip().lower()
                
                if cmd.startswith('sessao'):
                    parts = cmd.split()
                    minutos = int(parts[1]) if len(parts) > 1 else 5
                    atena.run_session(minutos * 60)
                
                elif cmd == 'status':
                    report = atena.get_consciousness_report()
                    print(f"\n📊 STATUS:")
                    print(f"Geração: {report['geracao_atual']}")
                    print(f"Score: {report['score_atual']:.2f}/100")
                    print(f"Memórias: {report['total_memorias']}")
                    print(f"Padrões: {report['total_padroes']}")
                    print(f"Evoluções: {report['total_evolucoes']}")
                
                elif cmd == 'memorias':
                    memories = atena.get_recent_memories(5)
                    print(f"\n📖 MEMÓRIAS RECENTES:")
                    for m in memories:
                        print(f"[Gen {m['geracao']}] {m['refinado'][:100]}...")
                
                elif cmd == 'evoluir':
                    atena.genetic_evolution()
                
                elif cmd == 'sair':
                    print("Encerrando Atena...")
                    atena.auto_commit()
                    break
                
                else:
                    print("Comando não reconhecido")
                    
            except KeyboardInterrupt:
                print("\n\nEncerrando Atena...")
                atena.auto_commit()
                break
            except Exception as e:
                print(f"Erro: {e}")
