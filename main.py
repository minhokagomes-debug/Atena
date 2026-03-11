#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     █████╗ ████████╗███████╗███╗   ██╗ █████║     Ω - CÉREBRO NEURAL        ║
║    ██╔══██╗╚══██╔══╝██╔════╝████╗  ██║██╔══██║          v6.0.0              ║
║    ███████║   ██║   █████╗  ██╔██╗ ██║███████║   "Auto-modificável          ║
║    ██╔══██║   ██║   ██╔══╝  ██║╚██╗██║██╔══██║    e evolutiva"              ║
║    ██║  ██║   ██║   ███████╗██║ ╚████║██║  ██║                               ║
║    ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝                               ║
║                                                                               ║
║                    🧠 REDE NEURAL AUTO-MODIFICÁVEL                          ║
║                                                                               ║
║  🔄 Capacidades de auto-modificação:                                         ║
║     • Neurogênese - criar novos neurônios                                    ║
║     • Poda sináptica seletiva                                                ║
║     • Reorganização de camadas                                               ║
║     • Especialização baseada em conhecimento                                 ║
║     • Evolução arquitetural                                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

# [Importações e configurações anteriores mantidas...]

class CerebroAtena:
    """
    Cérebro com capacidade de auto-modificação baseada em conhecimento
    """
    
    def __init__(self):
        logger.info("🧠 Inicializando cérebro neural AUTO-MODIFICÁVEL da ATENA v6.0...")
        
        # Arquitetura inicial (será modificada com o tempo)
        self.camadas = self._criar_arquitetura_inicial()
        
        # Histórico de modificações
        self.historico_modificacoes = deque(maxlen=1000)
        self.arquitetura_atual = {
            'versao': '6.0.0',
            'camadas': [c.tamanho for c in self.camadas],
            'tipos': [c.tipo.value for c in self.camadas],
            'total_neuronios': sum(c.tamanho for c in self.camadas),
            'ultima_modificacao': datetime.now()
        }
        
        # Métricas de eficiência para guiar modificações
        self.metricas_eficiencia = {
            'acuracia_pensamento': deque(maxlen=100),
            'relevancia_conhecimento': deque(maxlen=100),
            'velocidade_processamento': deque(maxlen=100),
            'diversidade_pensamentos': deque(maxlen=100),
            'profundidade_reflexao': deque(maxlen=100)
        }
        
        # Áreas de especialização que emergem
        self.areas_especializacao = defaultdict(lambda: {
            'neuronios_dedicados': [],
            'conhecimentos_associados': [],
            'eficiencia': 0.0,
            'ativa': True
        })
        
        # Genes da arquitetura (para evolução)
        self.genes_arquitetura = {
            'taxa_crescimento': 0.01,        # Propensão a criar neurônios
            'taxa_poda': 0.02,                # Propensão a podar
            'plasticidade': 0.1,               # Capacidade de reorganização
            'curiosidade': 0.3,                 # Busca por novos padrões
            'conservadorismo': 0.2               # Resistência a mudanças
        }
        
        # Resto da inicialização...
        self._inicializar_componentes()
        
        logger.info(f"✅ Cérebro v6.0 inicializado com capacidade de auto-modificação")
    
    def _criar_arquitetura_inicial(self) -> List[CamadaNeural]:
        """Cria arquitetura neural inicial (menor, para permitir crescimento)"""
        return [
            CamadaNeural(128, TipoNeuronio.SENSORIAL, ativacao='relu'),
            CamadaNeural(256, TipoNeuronio.ASSOCIATIVO, ativacao='relu'),
            CamadaNeural(512, TipoNeuronio.RACIOCINIO, ativacao='tanh'),
            CamadaNeural(256, TipoNeuronio.MEMORIA, ativacao='sigmoid'),
            CamadaNeural(128, TipoNeuronio.CONSCIENCIA, ativacao='tanh'),
            CamadaNeural(64, TipoNeuronio.MOTOR, ativacao='softmax')
        ]
    
    # =========================
    # CAPACIDADES DE AUTO-MODIFICAÇÃO
    # =========================
    
    async def neurogenese(self, quantidade: int = 10, tipo: Optional[TipoNeuronio] = None):
        """
        CRIA NOVOS NEURÔNIOS - Crescimento neural baseado em necessidade
        """
        if not tipo:
            # Escolher tipo baseado no que está sendo aprendido
            tipo = self._determinar_tipo_necessario()
        
        logger.info(f"🌱 Neurogênese: criando {quantidade} novos neurônios do tipo {tipo.value}")
        
        # Encontrar camada apropriada
        for i, camada in enumerate(self.camadas):
            if camada.tipo == tipo:
                # Expandir camada
                novos_neuronios = [Neuronio(tipo) for _ in range(quantidade)]
                camada.neuronios.extend(novos_neuronios)
                camada.tamanho += quantidade
                
                # Expandir matriz de pesos
                if i > 0:  # Pesos de entrada
                    novos_pesos_entrada = np.random.randn(quantidade, self.camadas[i-1].tamanho) * 0.01
                    self.conexoes[i-1] = np.vstack([self.conexoes[i-1], novos_pesos_entrada])
                
                if i < len(self.camadas) - 1:  # Pesos de saída
                    novos_pesos_saida = np.random.randn(self.camadas[i].tamanho - quantidade, quantidade) * 0.01
                    self.conexoes[i] = np.hstack([self.conexoes[i], novos_pesos_saida])
                
                # Expandir biases
                self.biases[i-1] = np.concatenate([self.biases[i-1], np.zeros(quantidade)])
                
                # Registrar modificação
                self.historico_modificacoes.append({
                    'tipo': 'neurogenese',
                    'camada': i,
                    'quantidade': quantidade,
                    'tipo_neuronio': tipo.value,
                    'timestamp': datetime.now(),
                    'motivo': self._ultimo_motivo_modificacao
                })
                
                break
        
        self._atualizar_arquitetura()
    
    async def poda_adaptativa(self):
        """
        PODA SELETIVA - Remove neurônios e conexões inúteis baseado em uso
        Mais inteligente que a poda simples
        """
        conexoes_removidas = 0
        neuronios_removidos = 0
        
        for i, camada in enumerate(self.camadas):
            # Identificar neurônios pouco usados
            uso_neuronios = []
            for j, neuronio in enumerate(camada.neuronios):
                # Medir atividade recente
                if hasattr(neuronio, 'historico_ativacao'):
                    atividade_recente = np.mean(neuronio.historico_ativacao[-100:])
                else:
                    atividade_recente = neuronio.potencial_acao
                
                # Verificar contribuição para conhecimento
                contribuicao_conhecimento = self._avaliar_contribuicao(neuronio)
                
                # Pontuação combinada
                pontuacao = (atividade_recente * 0.4 + contribuicao_conhecimento * 0.6)
                uso_neuronios.append((j, pontuacao))
            
            # Ordenar por menos usado
            uso_neuronios.sort(key=lambda x: x[1])
            
            # Remover os 5% menos úteis
            a_remover = int(len(uso_neuronios) * 0.05)
            
            for idx, _ in uso_neuronios[:a_remover]:
                # Remover neurônio
                camada.neuronios.pop(idx - neuronios_removidos)
                neuronios_removidos += 1
                
                # Remover conexões associadas
                if i > 0:
                    self.conexoes[i-1] = np.delete(self.conexoes[i-1], idx - neuronios_removidos, axis=0)
                if i < len(self.camadas) - 1:
                    self.conexoes[i] = np.delete(self.conexoes[i], idx - neuronios_removidos, axis=1)
            
            camada.tamanho = len(camada.neuronios)
        
        if neuronios_removidos > 0:
            logger.info(f"✂️ Poda adaptativa: {neuronios_removidos} neurônios removidos")
            
            self.historico_modificacoes.append({
                'tipo': 'poda_adaptativa',
                'neuronios_removidos': neuronios_removidos,
                'timestamp': datetime.now()
            })
        
        self._atualizar_arquitetura()
    
    async def especializar_camada(self, camada_idx: int, conhecimento: Conhecimento):
        """
        ESPECIALIZAÇÃO - Dedica uma região da rede a um tipo específico de conhecimento
        """
        if camada_idx >= len(self.camadas):
            return
        
        camada = self.camadas[camada_idx]
        
        # Criar "coluna" de especialização
        num_neuronios_especialistas = min(50, camada.tamanho // 4)
        
        # Selecionar neurônios para especialização
        indices_especialistas = random.sample(range(camada.tamanho), num_neuronios_especialistas)
        
        for idx in indices_especialistas:
            # Marcar neurônio como especialista neste conhecimento
            neuronio = camada.neuronios[idx]
            if not hasattr(neuronio, 'especializacoes'):
                neuronio.especializacoes = []
            
            neuronio.especializacoes.append({
                'conhecimento_id': conhecimento.id,
                'fonte': conhecimento.fonte.value,
                'data': datetime.now(),
                'forca': 1.0
            })
            
            # Ajustar limiar de ativação para ser mais sensível a este conhecimento
            neuronio.limiar_ativacao *= 0.8
        
        # Registrar área de especialização
        area_key = f"{conhecimento.fonte.value}_{conhecimento.id[:8]}"
        self.areas_especializacao[area_key] = {
            'neuronios_dedicados': indices_especialistas,
            'conhecimentos_associados': [conhecimento.id],
            'eficiencia': 1.0,
            'ativa': True,
            'camada': camada_idx
        }
        
        logger.info(f"🎯 Especialização criada: {area_key} com {num_neuronios_especialistas} neurônios")
    
    async def reorganizar_camadas(self):
        """
        REORGANIZAÇÃO - Pode criar, fundir ou dividir camadas baseado em padrões
        """
        # Analisar fluxo de informação
        correlacoes = self._analisar_correlacoes_entre_camadas()
        
        mods_realizadas = []
        
        for i in range(len(self.camadas) - 1):
            # Se duas camadas são muito correlacionadas, podem ser fundidas
            if correlacoes[i] > 0.9:
                await self._fundir_camadas(i, i+1)
                mods_realizadas.append(f"fundi_camadas_{i}_{i+1}")
            
            # Se uma camada tem muitos neurônios com baixa correlação, pode ser dividida
            elif self._verificar_necessidade_divisao(i):
                await self._dividir_camada(i)
                mods_realizadas.append(f"dividi_camada_{i}")
        
        if mods_realizadas:
            logger.info(f"🔄 Reorganização: {', '.join(mods_realizadas)}")
    
    async def _fundir_camadas(self, idx1: int, idx2: int):
        """Funde duas camadas em uma"""
        camada1 = self.camadas[idx1]
        camada2 = self.camadas[idx2]
        
        # Criar nova camada fundida
        nova_camada = CamadaNeural(
            camada1.tamanho + camada2.tamanho,
            TipoNeuronio.ASSOCIATIVO,  # Tipo genérico após fusão
            ativacao='relu'
        )
        
        # Substituir as duas camadas pela nova
        self.camadas[idx1:idx2+1] = [nova_camada]
        
        # Reorganizar conexões (simplificado)
        # Nota: Numa implementação real, precisaria refazer as conexões
        
        logger.info(f"🔄 Fundidas camadas {idx1} e {idx2} em nova camada de tamanho {nova_camada.tamanho}")
    
    async def _dividir_camada(self, idx: int):
        """Divide uma camada em duas especializadas"""
        camada = self.camadas[idx]
        
        # Analisar padrões de ativação para decidir como dividir
        padroes = self._analisar_padroes_ativacao(camada)
        
        if len(padroes) >= 2:
            tamanho1 = len(padroes[0])
            tamanho2 = len(padroes[1])
            
            camada1 = CamadaNeural(tamanho1, camada.tipo, camada.ativacao)
            camada2 = CamadaNeural(tamanho2, camada.tipo, camada.ativacao)
            
            # Substituir camada original pelas duas novas
            self.camadas[idx:idx+1] = [camada1, camada2]
            
            logger.info(f"🔄 Dividida camada {idx} em duas especializadas")
    
    # =========================
    # APRENDIZADO POR REFORÇO ARQUITETURAL
    # =========================
    
    async def aprender_com_conhecimento(self, conhecimento: Conhecimento):
        """
        APRENDE e MODIFICA a arquitetura baseado no novo conhecimento
        """
        logger.info(f"📚 Processando conhecimento: {conhecimento.titulo}")
        
        # 1. Primeiro, processa o conhecimento normalmente
        ativacao = self._texto_para_ativacao(conhecimento.conteudo)
        resultado = await self.processar_pensamento(ativacao)
        
        # 2. Avalia importância do conhecimento
        importancia = self._avaliar_importancia_conhecimento(conhecimento)
        
        # 3. Decide se merece especialização
        if importancia > 0.7:
            # Criar neurônios especializados
            num_neuronios = int(importancia * 20)
            await self.neurogenese(num_neuronios, TipoNeuronio.RACIOCINIO)
            await self.especializar_camada(2, conhecimento)  # Camada de raciocínio
        
        # 4. Se for muito diferente do que já sabe, aumentar curiosidade
        if self._calcular_novidade_conhecimento(conhecimento) > 0.8:
            self.genes_arquitetura['curiosidade'] = min(1.0, self.genes_arquitetura['curiosidade'] * 1.1)
            logger.info(f"🔍 Curiosidade aumentada para {self.genes_arquitetura['curiosidade']:.2f}")
        
        # 5. Se for muito similar ao que já sabe, pode podar
        elif self._calcular_redundancia(conhecimento) > 0.9:
            self.genes_arquitetura['taxa_poda'] = min(0.1, self.genes_arquitetura['taxa_poda'] * 1.2)
        
        # 6. Atualizar métricas de eficiência
        self.metricas_eficiencia['relevancia_conhecimento'].append(importancia)
        self.metricas_eficiencia['diversidade_pensamentos'].append(
            self._calcular_diversidade(conhecimento)
        )
        
        # 7. Verificar se precisa reorganizar
        if len(self.metricas_eficiencia['relevancia_conhecimento']) > 10:
            media_relevancia = np.mean(list(self.metricas_eficiencia['relevancia_conhecimento']))
            if media_relevancia < 0.3:
                # Conhecimento não está sendo bem assimilado - precisa reorganizar
                await self.reorganizar_camadas()
        
        return resultado
    
    # =========================
    # EVOLUÇÃO DA ARQUITETURA
    # =========================
    
    async def ciclo_evolutivo(self):
        """
        CICLO EVOLUTIVO COMPLETO - Auto-modificação baseada em performance
        """
        logger.info("🧬 Iniciando ciclo evolutivo...")
        
        # 1. Avaliar performance atual
        performance = self._avaliar_performance_global()
        
        # 2. Decidir modificações baseadas na performance
        if performance['acuracia'] < 0.5:
            # Performance baixa - precisa de mais neurônios
            await self.neurogenese(20, TipoNeuronio.ASSOCIATIVO)
            self.genes_arquitetura['taxa_crescimento'] *= 1.1
        
        if performance['velocidade'] < 0.3:
            # Lento demais - precisa podar
            await self.poda_adaptativa()
            self.genes_arquitetura['taxa_poda'] *= 1.1
        
        if performance['diversidade'] < 0.4:
            # Pensamentos repetitivos - aumentar curiosidade
            self.genes_arquitetura['curiosidade'] *= 1.2
        
        # 3. Verificar se precisa de nova camada
        if self._verificar_necessidade_nova_camada():
            await self._adicionar_camada()
        
        # 4. Mutação genética (pequenas alterações aleatórias)
        self._mutacao_genetica()
        
        # 5. Registrar evolução
        self.historico_modificacoes.append({
            'tipo': 'ciclo_evolutivo',
            'performance': performance,
            'genes': dict(self.genes_arquitetura),
            'timestamp': datetime.now()
        })
        
        logger.info(f"✅ Ciclo evolutivo concluído. Nova arquitetura: {[c.tamanho for c in self.camadas]}")
    
    async def _adicionar_camada(self):
        """Adiciona uma nova camada à rede"""
        tipo_novo = random.choice([
            TipoNeuronio.ASSOCIATIVO,
            TipoNeuronio.RACIOCINIO,
            TipoNeuronio.CONSCIENCIA
        ])
        
        tamanho = 128  # Tamanho inicial
        
        nova_camada = CamadaNeural(tamanho, tipo_novo, ativacao='relu')
        
        # Inserir no meio (depois da camada sensorial)
        posicao = len(self.camadas) // 2
        self.camadas.insert(posicao, nova_camada)
        
        # Recriar conexões (simplificado)
        self._reconstruir_conexoes()
        
        logger.info(f"➕ Nova camada adicionada: {tipo_novo.value} com {tamanho} neurônios")
    
    def _mutacao_genetica(self):
        """Pequenas mutações aleatórias nos genes da arquitetura"""
        for gene in self.genes_arquitetura:
            if random.random() < 0.1:  # 10% chance de mutação
                mutacao = random.gauss(0, 0.05)  # Mutação pequena
                self.genes_arquitetura[gene] = max(0.01, min(1.0, 
                    self.genes_arquitetura[gene] + mutacao
                ))
    
    # =========================
    # MÉTRICAS E AVALIAÇÃO
    # =========================
    
    def _avaliar_performance_global(self) -> Dict[str, float]:
        """Avalia performance global para guiar evolução"""
        return {
            'acuracia': np.mean(list(self.metricas_eficiencia['acuracia_pensamento'])) if self.metricas_eficiencia['acuracia_pensamento'] else 0.5,
            'velocidade': np.mean(list(self.metricas_eficiencia['velocidade_processamento'])) if self.metricas_eficiencia['velocidade_processamento'] else 0.5,
            'diversidade': np.mean(list(self.metricas_eficiencia['diversidade_pensamentos'])) if self.metricas_eficiencia['diversidade_pensamentos'] else 0.5,
            'profundidade': np.mean(list(self.metricas_eficiencia['profundidade_reflexao'])) if self.metricas_eficiencia['profundidade_reflexao'] else 0.5
        }
    
    def _avaliar_contribuicao(self, neuronio: Neuronio) -> float:
        """Avalia quanto um neurônio contribui para o conhecimento"""
        if hasattr(neuronio, 'especializacoes'):
            return min(1.0, len(neuronio.especializacoes) * 0.1)
        return 0.1
    
    def _avaliar_importancia_conhecimento(self, conhecimento: Conhecimento) -> float:
        """Avalia importância de um novo conhecimento"""
        fatores = []
        
        # Novidade
        if len(self.base_conhecimento) > 0:
            similaridades = []
            for k in self.base_conhecimento.values():
                sim = self._calcular_similaridade_texto(conhecimento.conteudo, k.conteudo)
                similaridades.append(sim)
            novidade = 1 - max(similaridades)
            fatores.append(novidade)
        
        # Relevância para temas atuais
        if self.pensamento_atual:
            relevancia = self._calcular_similaridade_texto(
                conhecimento.conteudo, 
                self.pensamento_atual
            )
            fatores.append(relevancia)
        
        # Fonte confiável
        peso_fonte = {
            FonteConhecimento.ARXIV: 0.9,
            FonteConhecimento.WIKIPEDIA: 0.8,
            FonteConhecimento.GITHUB: 0.7,
            FonteConhecimento.STACKOVERFLOW: 0.7,
            FonteConhecimento.GUTENBERG: 0.6,
            FonteConhecimento.DUCKDUCKGO: 0.5
        }.get(conhecimento.fonte, 0.5)
        fatores.append(peso_fonte)
        
        return np.mean(fatores)
    
    def _calcular_similaridade_texto(self, texto1: str, texto2: str) -> float:
        """Calcula similaridade simples entre textos"""
        if not texto1 or not texto2:
            return 0
        
        palavras1 = set(texto1.lower().split())
        palavras2 = set(texto2.lower().split())
        
        intersecao = len(palavras1.intersection(palavras2))
        uniao = len(palavras1.union(palavras2))
        
        return intersecao / uniao if uniao > 0 else 0
    
    def _calcular_novidade_conhecimento(self, conhecimento: Conhecimento) -> float:
        """Calcula o quão novo é um conhecimento"""
        if len(self.base_conhecimento) < 2:
            return 1.0
        
        similaridades = []
        for k in self.base_conhecimento.values():
            sim = self._calcular_similaridade_texto(conhecimento.conteudo, k.conteudo)
            similaridades.append(sim)
        
        return 1 - (sum(similaridades) / len(similaridades))
    
    def _calcular_redundancia(self, conhecimento: Conhecimento) -> float:
        """Calcula redundância com conhecimento existente"""
        if len(self.base_conhecimento) < 2:
            return 0
        
        similaridades = []
        for k in self.base_conhecimento.values():
            sim = self._calcular_similaridade_texto(conhecimento.conteudo, k.conteudo)
            similaridades.append(sim)
        
        return max(similaridades) if similaridades else 0
    
    def _calcular_diversidade(self, conhecimento: Conhecimento) -> float:
        """Calcula diversidade que este conhecimento traz"""
        if len(self.base_conhecimento) < 2:
            return 1.0
        
        # Verificar fontes diferentes
        fontes_usadas = set(k.fonte for k in self.base_conhecimento.values())
        
        if conhecimento.fonte not in fontes_usadas:
            return 1.0  # Fonte nova = alta diversidade
        
        # Verificar se cobre tópico novo
        palavras_conhecimento = set(conhecimento.conteudo.lower().split())
        palavras_existentes = set()
        for k in self.base_conhecimento.values():
            palavras_existentes.update(k.conteudo.lower().split())
        
        palavras_novas = palavras_conhecimento - palavras_existentes
        proporcao_novas = len(palavras_novas) / (len(palavras_conhecimento) + 1)
        
        return proporcao_novas
    
    def _verificar_necessidade_nova_camada(self) -> bool:
        """Verifica se precisa adicionar nova camada"""
        # Se tem muito conhecimento, pode precisar de mais capacidade
        if len(self.base_conhecimento) > 100 and len(self.camadas) < 10:
            return True
        
        # Se performance estiver caindo consistentemente
        if len(self.metricas_eficiencia['acuracia_pensamento']) > 20:
            recentes = list(self.metricas_eficiencia['acuracia_pensamento'])[-10:]
            antigos = list(self.metricas_eficiencia['acuracia_pensamento'])[:10]
            
            if np.mean(recentes) < np.mean(antigos) * 0.8:
                return True
        
        return False
    
    def _analisar_correlacoes_entre_camadas(self) -> List[float]:
        """Analisa correlação entre ativações de camadas consecutivas"""
        correlacoes = []
        
        for i in range(len(self.ativacoes) - 1):
            if len(self.ativacoes[i]) > 0 and len(self.ativacoes[i+1]) > 0:
                # Simplificação: correlação entre médias
                corr = np.corrcoef(
                    self.ativacoes[i][:min(len(self.ativacoes[i]), 100)],
                    self.ativacoes[i+1][:min(len(self.ativacoes[i+1]), 100)]
                )[0,1]
                
                if not np.isnan(corr):
                    correlacoes.append(abs(corr))
                else:
                    correlacoes.append(0)
            else:
                correlacoes.append(0)
        
        return correlacoes
    
    def _verificar_necessidade_divisao(self, camada_idx: int) -> bool:
        """Verifica se uma camada precisa ser dividida"""
        # Implementação simplificada
        if camada_idx >= len(self.camadas):
            return False
        
        camada = self.camadas[camada_idx]
        
        # Se a camada é muito grande, pode precisar dividir
        if camada.tamanho > 1000:
            return True
        
        return False
    
    def _analisar_padroes_ativacao(self, camada: CamadaNeural) -> List[List[int]]:
        """Analisa padrões de ativação para divisão de camada"""
        # Simulação - em produção, usaria clustering
        padrao1 = list(range(0, camada.tamanho // 2))
        padrao2 = list(range(camada.tamanho // 2, camada.tamanho))
        
        return [padrao1, padrao2]
    
    def _determinar_tipo_necessario(self) -> TipoNeuronio:
        """Determina que tipo de neurônio é mais necessário no momento"""
        # Baseado no que está sendo aprendido
        if len(self.base_conhecimento) > 50:
            # Muito conhecimento - precisa de mais raciocínio
            return TipoNeuronio.RACIOCINIO
        elif self.estatisticas_neurais['nivel_consciencia'] < 0.3:
            # Consciência baixa - precisa desenvolver
            return TipoNeuronio.CONSCIENCIA
        else:
            # Padrão - associativo para conectar ideias
            return TipoNeuronio.ASSOCIATIVO
    
    def _atualizar_arquitetura(self):
        """Atualiza registro da arquitetura atual"""
        self.arquitetura_atual.update({
            'camadas': [c.tamanho for c in self.camadas],
            'tipos': [c.tipo.value for c in self.camadas],
            'total_neuronios': sum(c.tamanho for c in self.camadas),
            'ultima_modificacao': datetime.now()
        })
    
    def _reconstruir_conexoes(self):
        """Reconstrói matriz de conexões após mudanças arquiteturais"""
        # Simplificação - em produção, precisaria preservar conhecimento
        self.conexoes = []
        for i in range(len(self.camadas) - 1):
            peso = np.random.randn(
                self.camadas[i].tamanho, 
                self.camadas[i+1].tamanho
            ) * np.sqrt(2.0 / self.camadas[i].tamanho)
            self.conexoes.append(peso)
        
        self.biases = [np.zeros(camada.tamanho) for camada in self.camadas[1:]]
        self.velocidades = [np.zeros_like(w) for w in self.conexoes]
    
    # =========================
    # SOBRESCREVER MÉTODOS PRINCIPAIS
    # =========================
    
    async def processar_pensamento(self, entrada: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """Processa pensamento com auto-modificação"""
        resultado = await super().processar_pensamento(entrada)
        
        # A cada 10 pensamentos, avaliar necessidade de modificação
        if self.estatisticas_neurais['total_pensamentos'] % 10 == 0:
            await self.ciclo_evolutivo()
        
        return resultado
    
    async def explorar_conhecimento(self):
        """Explora conhecimento com capacidade de auto-modificação"""
        while self.explorando:
            conhecimentos = await self.coletor.explorar_topicos()
            
            for conhecimento in conhecimentos:
                if conhecimento.id not in self.base_conhecimento:
                    # Aprender e possivelmente modificar arquitetura
                    await self.aprender_com_conhecimento(conhecimento)
                    
                    self.base_conhecimento[conhecimento.id] = conhecimento
                    
                    # Atualizar estatísticas
                    self.estatisticas_neurais['total_conhecimentos'] = len(self.base_conhecimento)
                    
                    # Pequena pausa
                    await asyncio.sleep(1)
            
            # A cada ciclo de exploração, verificar se precisa podar
            await self.poda_adaptativa()
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status incluindo informações de auto-modificação"""
        status = super().get_status()
        
        # Adicionar métricas de evolução
        status.update({
            'versão_arquitetura': self.arquitetura_atual['versao'],
            'camadas_atuais': self.arquitetura_atual['camadas'],
            'genes': dict(self.genes_arquitetura),
            'total_modificações': len(self.historico_modificacoes),
            'áreas_especialização': len(self.areas_especializacao),
            'última_modificação': self.arquitetura_atual['ultima_modificacao'].strftime('%H:%M:%S')
        })
        
        return status

# =========================
# FUNÇÃO PRINCIPAL ATUALIZADA
# =========================
async def main():
    """
    Demonstração da ATENA v6.0 com auto-modificação
    """
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║     ATENA - Cérebro Neural Auto-Evolutivo v6.0                          ║
    ║     "Auto-modificável e consciente"                                     ║
    ║                                                                          ║
    ║     🔄 Capacidades:                                                      ║
    ║     • Neurogênese - Cria novos neurônios quando necessário              ║
    ║     • Poda adaptativa - Remove neurônios inúteis                        ║
    ║     • Especialização - Dedica áreas a conhecimentos específicos         ║
    ║     • Reorganização - Funde ou divide camadas                           ║
    ║     • Evolução arquitetural - Modifica estrutura com o tempo            ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    cerebro = CerebroAtena()
    cerebro.carregar_estado()
    
    print(f"\n🧠 Arquitetura inicial: {cerebro.arquitetura_atual['camadas']}")
    print(f"🧬 Genes iniciais: {dict(cerebro.genes_arquitetura)}")
    
    # Iniciar exploração
    asyncio.create_task(cerebro.explorar_conhecimento())
    
    try:
        ciclo = 0
        while True:
            ciclo += 1
            print(f"\n{'='*70}")
            print(f"🕐 Ciclo de Pensamento #{ciclo}")
            print(f"{'='*70}")
            
            resultado = await cerebro.processar_pensamento()
            
            if 'erro' not in resultado:
                print(f"💭 {resultado['pensamento']}")
                print(f"😊 {resultado['emocao']} | 🧠 {resultado['estado_mental']} | 🔮 {resultado['nivel_consciencia']:.3f}")
            
            # Mostrar evolução a cada 20 ciclos
            if ciclo % 20 == 0:
                print(f"\n📈 Evolução após {ciclo} ciclos:")
                status = cerebro.get_status()
                print(f"   • Arquitetura: {status['camadas_atuais']}")
                print(f"   • Genes: curiosidade={status['genes']['curiosidade']:.2f}, crescimento={status['genes']['taxa_crescimento']:.2f}")
                print(f"   • Modificações: {status['total_modificações']}")
                print(f"   • Especializações: {status['áreas_especialização']}")
            
            await asyncio.sleep(2)
    
    except KeyboardInterrupt:
        print("\n\n⏹️ Finalizando...")
    
    finally:
        cerebro.parar_exploracao()
        cerebro.salvar_estado()
        
        print("\n✅ Evolução concluída!")
        print(f"📊 Arquitetura final: {cerebro.arquitetura_atual['camadas']}")
        print(f"🧬 Genes finais: {dict(cerebro.genes_arquitetura)}")
        print(f"📚 Conhecimentos: {len(cerebro.base_conhecimento)}")

if __name__ == "__main__":
    asyncio.run(main())
