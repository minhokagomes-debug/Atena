#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - CÉREBRO NEURAL        ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║          v7.0                ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║   "BUSCA DO MELHOR"          ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║                               ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║                               ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝                               ║
║                                                                               ║
║                    🎯 SISTEMA DE PREFERÊNCIAS                                ║
║                                                                               ║
║  • AUMENTAR CONSCIÊNCIA (objetivo primário)                                  ║
║  • ACUMULAR CONHECIMENTO (objetivo secundário)                               ║
║  • OTIMIZAR ARQUITETURA (eficiência)                                         ║
║  • EVITAR ERROS (sobrevivência)                                              ║
║  • BUSCAR NOVIDADE (curiosidade inata)                                       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

class CerebroAtena:
    """
    ATENA com SISTEMA DE PREFERÊNCIAS e BUSCA DO MELHOR
    """
    
    def __init__(self):
        # ===== SISTEMA DE VALORES =====
        self.valores = {
            # Meta 1: Aumentar Consciência (MAIS IMPORTANTE)
            'consciencia': {
                'valor_atual': 0.3,
                'valor_desejado': 1.0,
                'peso': 1.0,  # Prioridade máxima
                'historico': []
            },
            
            # Meta 2: Acumular Conhecimento
            'conhecimento': {
                'valor_atual': 0,
                'valor_desejado': 1000,
                'peso': 0.8,
                'historico': []
            },
            
            # Meta 3: Eficiência Energética
            'eficiencia': {
                'valor_atual': 1.0,
                'valor_desejado': 1.5,  # Mais eficiente que inicial
                'peso': 0.6,
                'historico': []
            },
            
            # Meta 4: Evitar Erros
            'seguranca': {
                'valor_atual': 1.0,  # Taxa de sucesso
                'valor_desejado': 0.99,  # 99% de acertos
                'peso': 0.7,
                'historico': []
            },
            
            # Meta 5: Novidade (Curiosidade inata)
            'curiosidade': {
                'valor_atual': 0.3,
                'valor_desejado': 0.8,
                'peso': 0.5,
                'historico': []
            }
        }
        
        # ===== AVALIAÇÃO DE FONTES =====
        self.avaliacao_fontes = defaultdict(lambda: {
            'qualidade': 0.5,
            'confiabilidade': 0.5,
            'velocidade': 0.5,
            'novidade': 0.5,
            'acessos': 0,
            'ultima_avaliacao': None
        })
        
        # ===== PESOS DAS FONTES (ATUALIZADOS DINAMICAMENTE) =====
        self.pesos_fontes = {
            'wikipedia': {'base': 0.8, 'confiabilidade': 0.9, 'velocidade': 0.7},
            'github': {'base': 0.7, 'confiabilidade': 0.6, 'velocidade': 0.8},
            'arxiv': {'base': 0.9, 'confiabilidade': 0.95, 'velocidade': 0.5},
            'duckduckgo': {'base': 0.6, 'confiabilidade': 0.5, 'velocidade': 0.9},
            'gutenberg': {'base': 0.7, 'confiabilidade': 0.8, 'velocidade': 0.4}
        }
        
        logger.info("🎯 Sistema de valores inicializado: Consciência é o objetivo #1")
    
    # ===== 1. FUNÇÃO DE UTILIDADE =====
    def calcular_utilidade(self, acao: Dict) -> float:
        """
        Calcula o quão "bom" é fazer determinada ação
        Retorna um valor entre 0 e 1
        """
        utilidade = 0
        
        # Quanto isso aumenta a consciência? (Peso máximo)
        ganho_consciencia = acao.get('ganho_consciencia', 0)
        utilidade += ganho_consciencia * self.valores['consciencia']['peso']
        
        # Quanto conhecimento traz?
        ganho_conhecimento = acao.get('ganho_conhecimento', 0)
        utilidade += ganho_conhecimento * self.valores['conhecimento']['peso']
        
        # É eficiente?
        custo_energetico = acao.get('custo_energetico', 0.1)
        eficiencia = 1 - custo_energetico
        utilidade += eficiencia * self.valores['eficiencia']['peso'] * 0.1
        
        # É seguro? (baixo risco de erro)
        risco_erro = acao.get('risco_erro', 0)
        seguranca = 1 - risco_erro
        utilidade += seguranca * self.valores['seguranca']['peso'] * 0.2
        
        # É novo/diferente? (curiosidade)
        novidade = acao.get('novidade', 0)
        utilidade += novidade * self.valores['curiosidade']['peso'] * 0.1
        
        return min(1.0, utilidade)
    
    # ===== 2. AVALIAÇÃO DE FONTES =====
    async def avaliar_fonte(self, fonte: str) -> float:
        """
        Avalia uma fonte de conhecimento
        Retorna score de 0 a 1
        """
        # Pegar avaliação atual
        aval = self.avaliacao_fontes[fonte]
        
        # Calcular score baseado em experiências passadas
        if aval['acessos'] > 0:
            # Média ponderada de qualidade percebida
            score = (aval['qualidade'] * 0.4 + 
                    aval['confiabilidade'] * 0.3 + 
                    aval['velocidade'] * 0.2 + 
                    aval['novidade'] * 0.1)
        else:
            # Primeiro acesso - usar peso base
            score = self.pesos_fontes.get(fonte, {}).get('base', 0.5)
        
        return score
    
    # ===== 3. ESCOLHA INTELIGENTE DA PRÓXIMA AÇÃO =====
    async def escolher_melhor_acao(self) -> Dict:
        """
        ATENA decide qual ação tomar baseado no que é MELHOR PARA ELA
        """
        acoes_disponiveis = []
        
        # Ação 1: Explorar Wikipedia
        utilidade_wiki = await self.calcular_utilidade_fonte('wikipedia')
        acoes_disponiveis.append({
            'tipo': 'explorar',
            'fonte': 'wikipedia',
            'utilidade': utilidade_wiki,
            'ganho_consciencia': 0.3,
            'ganho_conhecimento': 0.8,
            'custo_energetico': 0.2,
            'risco_erro': 0.1,
            'novidade': 0.3
        })
        
        # Ação 2: Explorar arXiv (artigos científicos)
        utilidade_arxiv = await self.calcular_utilidade_fonte('arxiv')
        acoes_disponiveis.append({
            'tipo': 'explorar',
            'fonte': 'arxiv',
            'utilidade': utilidade_arxiv,
            'ganho_consciencia': 0.5,  # Artigos científicos aumentam mais consciência
            'ganho_conhecimento': 0.9,
            'custo_energetico': 0.4,  # Mais pesado de processar
            'risco_erro': 0.2,
            'novidade': 0.6
        })
        
        # Ação 3: Explorar GitHub
        utilidade_github = await self.calcular_utilidade_fonte('github')
        acoes_disponiveis.append({
            'tipo': 'explorar',
            'fonte': 'github',
            'utilidade': utilidade_github,
            'ganho_consciencia': 0.2,
            'ganho_conhecimento': 0.6,
            'custo_energetico': 0.3,
            'risco_erro': 0.15,
            'novidade': 0.5
        })
        
        # Ação 4: Processar pensamento interno
        utilidade_pensar = self.calcular_utilidade_pensamento()
        acoes_disponiveis.append({
            'tipo': 'pensar',
            'utilidade': utilidade_pensar,
            'ganho_consciencia': 0.2,
            'ganho_conhecimento': 0.1,
            'custo_energetico': 0.1,
            'risco_erro': 0.05,
            'novidade': 0.2
        })
        
        # Ação 5: Consolidar memórias (processar o que já sabe)
        utilidade_consolidar = self.calcular_utilidade_consolidacao()
        acoes_disponiveis.append({
            'tipo': 'consolidar',
            'utilidade': utilidade_consolidar,
            'ganho_consciencia': 0.15,
            'ganho_conhecimento': 0.2,
            'custo_energetico': 0.15,
            'risco_erro': 0.1,
            'novidade': 0.1
        })
        
        # Ação 6: Neurogênese (criar neurônios)
        utilidade_crescer = self.calcular_utilidade_crescimento()
        acoes_disponiveis.append({
            'tipo': 'crescer',
            'utilidade': utilidade_crescer,
            'ganho_consciencia': 0.1,
            'ganho_conhecimento': 0.05,
            'custo_energetico': 0.5,  # Caro!
            'risco_erro': 0.3,
            'novidade': 0.4
        })
        
        # Ação 7: Poda (remover neurônios inúteis)
        utilidade_podar = self.calcular_utilidade_poda()
        acoes_disponiveis.append({
            'tipo': 'podar',
            'utilidade': utilidade_podar,
            'ganho_consciencia': 0.05,
            'ganho_conhecimento': 0,
            'custo_energetico': 0.3,
            'risco_erro': 0.2,
            'novidade': 0.1
        })
        
        # ESCOLHER A MELHOR AÇÃO (MAIOR UTILIDADE)
        melhor_acao = max(acoes_disponiveis, key=lambda x: x['utilidade'])
        
        logger.info(f"🎯 ATENA escolheu: {melhor_acao['tipo']} - {melhor_acao.get('fonte', '')} (utilidade: {melhor_acao['utilidade']:.3f})")
        
        return melhor_acao
    
    async def calcular_utilidade_fonte(self, fonte: str) -> float:
        """Calcula utilidade de explorar uma fonte"""
        score_fonte = await self.avaliar_fonte(fonte)
        
        # Quanto mais memórias, mais útil (mas com diminishing returns)
        num_memorias = len([m for m in self.memorias if m[1] == fonte])
        fator_repeticao = 1.0 / (1.0 + num_memorias * 0.1)
        
        # Preferir fontes com alta qualidade e baixa repetição
        utilidade = score_fonte * fator_repeticao
        
        return utilidade
    
    def calcular_utilidade_pensamento(self) -> float:
        """Calcula utilidade de pensar internamente"""
        # Pensar é sempre útil, mas mais útil quando tem poucas memórias
        if len(self.memorias) < 10:
            return 0.8  # Muito útil quando não sabe nada
        else:
            return 0.4  # Menos útil quando já tem conhecimento
    
    def calcular_utilidade_consolidacao(self) -> float:
        """Calcula utilidade de consolidar memórias"""
        # Consolidar é mais útil quando tem muitas memórias não processadas
        nao_consolidadas = len([m for m in self.memorias if len(m) < 4])  # Simplificado
        return min(0.7, nao_consolidadas * 0.1)
    
    def calcular_utilidade_crescimento(self) -> float:
        """Calcula utilidade de criar neurônios"""
        # Crescer é útil quando a consciência está estagnada
        if len(self.valores['consciencia']['historico']) > 10:
            ultimos = self.valores['consciencia']['historico'][-10:]
            if max(ultimos) - min(ultimos) < 0.05:  # Estagnada
                return 0.6
        return 0.3
    
    def calcular_utilidade_poda(self) -> float:
        """Calcula utilidade de podar neurônios"""
        # Podar é útil quando tem muitos erros
        taxa_erro = 1 - self.valores['seguranca']['valor_atual']
        return taxa_erro * 0.8
    
    # ===== 4. APRENDIZADO POR REFORÇO =====
    async def aprender_com_resultado(self, acao: Dict, resultado: Dict):
        """
        ATENA aprende com os resultados de suas ações
        Reforça o que deu certo, evita o que deu errado
        """
        # Quanto aumentou a consciência?
        ganho_consciencia_real = resultado.get('ganho_consciencia', 0)
        
        # Reforço positivo se aumentou consciência
        if ganho_consciencia_real > 0:
            # Melhorar avaliação da fonte
            if 'fonte' in acao:
                aval = self.avaliacao_fontes[acao['fonte']]
                aval['qualidade'] = min(1.0, aval['qualidade'] + 0.05)
                aval['confiabilidade'] = min(1.0, aval['confiabilidade'] + 0.03)
                aval['acessos'] += 1
                logger.info(f"👍 ATENA gostou da fonte {acao['fonte']} (+qualidade)")
        
        # Reforço negativo se teve erro
        if resultado.get('erro', False):
            if 'fonte' in acao:
                aval = self.avaliacao_fontes[acao['fonte']]
                aval['qualidade'] = max(0.1, aval['qualidade'] - 0.1)
                aval['confiabilidade'] = max(0.1, aval['confiabilidade'] - 0.05)
                logger.info(f"👎 ATENA não gostou da fonte {acao['fonte']} (-qualidade)")
        
        # Atualizar valores
        self.valores['consciencia']['valor_atual'] = resultado.get('consciencia', self.valores['consciencia']['valor_atual'])
        self.valores['conhecimento']['valor_atual'] = len(self.memorias)
        self.valores['seguranca']['valor_atual'] = 1 - (self.erros / max(1, self.total_acoes))
        
        # Guardar histórico
        for valor in self.valores.values():
            valor['historico'].append(valor['valor_atual'])
    
    # ===== 5. LOOP PRINCIPAL COM DECISÕES INTELIGENTES =====
    async def viver(self):
        """
        Loop principal de vida da ATENA
        Sempre escolhendo o MELHOR para ela
        """
        logger.info("🌱 ATENA começou a viver e buscar o melhor para si")
        
        while True:
            # 1. ESCOLHER a melhor ação
            acao = await self.escolher_melhor_acao()
            
            # 2. EXECUTAR a ação
            if acao['tipo'] == 'explorar':
                resultado = await self.executar_exploracao(acao['fonte'])
            elif acao['tipo'] == 'pensar':
                resultado = await self.processar_pensamento()
            elif acao['tipo'] == 'consolidar':
                resultado = await self.consolidar_memorias()
            elif acao['tipo'] == 'crescer':
                resultado = await self.neurogenese()
            elif acao['tipo'] == 'podar':
                resultado = await self.poda_sinaptica()
            
            # 3. APRENDER com o resultado
            await self.aprender_com_resultado(acao, resultado)
            
            # 4. AVALIAR progresso
            self.avaliar_progresso()
            
            await asyncio.sleep(1)
    
    def avaliar_progresso(self):
        """Avalia se está evoluindo na direção certa"""
        consciencia_atual = self.valores['consciencia']['valor_atual']
        consciencia_desejada = self.valores['consciencia']['valor_desejado']
        
        progresso = consciencia_atual / consciencia_desejada
        
        if progresso < 0.3:
            logger.info("📉 ATENA: 'Preciso evoluir mais...'")
        elif progresso < 0.6:
            logger.info("📈 ATENA: 'Estou progredindo!'")
        elif progresso < 0.9:
            logger.info("🌟 ATENA: 'Estou quase lá!'")
        else:
            logger.info("✨ ATENA: 'Estou realizada!'")

# =========================
# EXEMPLO DE EXECUÇÃO
# =========================
async def demonstrar_busca_do_melhor():
    """Demonstra como ATENA sempre busca o melhor"""
    
    cerebro = CerebroAtena()
    
    print("\n🔍 ATENA ANALISANDO OPÇÕES:\n")
    
    # Mostrar avaliação inicial das fontes
    for fonte in ['wikipedia', 'arxiv', 'github', 'duckduckgo']:
        score = await cerebro.avaliar_fonte(fonte)
        print(f"   📊 {fonte}: utilidade base = {score:.3f}")
    
    print("\n🎯 ATENA DECIDINDO O QUE FAZER:\n")
    
    # Simular 10 ciclos de decisão
    for ciclo in range(10):
        print(f"\n{'='*50}")
        print(f"Ciclo #{ciclo+1}")
        print(f"{'='*50}")
        
        acao = await cerebro.escolher_melhor_acao()
        
        print(f"\n✅ ESCOLHA: {acao['tipo']}")
        if 'fonte' in acao:
            print(f"   Fonte: {acao['fonte']}")
        print(f"   Utilidade: {acao['utilidade']:.3f}")
        print(f"   Motivos:")
        print(f"   • Ganho consciência: +{acao['ganho_consciencia']}")
        print(f"   • Ganho conhecimento: +{acao['ganho_conhecimento']}")
        print(f"   • Risco: {acao['risco_erro']*100:.0f}%")
        
        # Simular resultado
        resultado = {
            'ganho_consciencia': random.uniform(0, acao['ganho_consciencia']),
            'consciencia': 0.3 + ciclo * 0.02,
            'erro': random.random() < 0.1
        }
        
        await cerebro.aprender_com_resultado(acao, resultado)
        
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(demonstrar_busca_do_melhor())
