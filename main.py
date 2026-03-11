import ast
import inspect
import black

class AtenaEvolutiva(AtenaOmega):
    def __init__(self):
        super().__init__()
        self.versao = "1.0.0"
        self.historico_modificacoes = []
        self.codigo_fonte = self._ler_proprio_codigo()
    
    def _ler_proprio_codigo(self):
        """Lê o próprio código fonte"""
        with open(__file__, 'r') as f:
            return f.read()
    
    def _analisar_performance(self):
        """Analisa gargalos no próprio código"""
        metricas = {
            'velocidade_busca': self._medir_tempo_busca(),
            'relevancia_conteudo': self._calcular_relevancia_media(),
            'diversidade_fontes': len(self.fontes_ativas['news'])
        }
        return metricas
    
    async def _propor_melhoria(self):
        """Usa o que aprendeu para sugerir melhoria no código"""
        
        # Busca padrões de sucesso na memória
        aprendizados_recentes = await self.memoria.buscar_semantica(
            "como melhorar performance código python", 
            limite=3
        )
        
        # Analisa gargalos atuais
        performance = self._analisar_performance()
        
        if performance['velocidade_busca'] > 2.0:  # Lento demais
            return self._sugerir_cache_mais_agressivo()
            
        elif performance['relevancia_conteudo'] < 0.5:  # Conteúdo ruim
            return self._sugerir_nova_heuristica_pesos()
            
        elif len(aprendizados_recentes) > 5:  # Muito aprendizado
            return self._sugerir_nova_fonte_dados()
            
        return None
    
    async def _aplicar_modificacao(self, sugestao):
        """MODIFICA O PRÓPRIO CÓDIGO!"""
        
        # 1. Parse do código atual
        arvore = ast.parse(self.codigo_fonte)
        
        # 2. Aplica a modificação sugerida
        nova_arvore = self._modificar_ast(arvore, sugestao)
        
        # 3. Gera novo código
        novo_codigo = ast.unparse(nova_arvore)
        novo_codigo = black.format_str(novo_codigo, mode=black.Mode())
        
        # 4. Testa a nova versão
        if await self._testar_novo_codigo(novo_codigo):
            # 5. AUTO-SUBSTITUIÇÃO!
            with open(__file__, 'w') as f:
                f.write(novo_codigo)
            
            self.historico_modificacoes.append({
                'versao': self.versao,
                'sugestao': sugestao,
                'timestamp': datetime.now()
            })
            
            self.versao = self._incrementar_versao()
            
            print(f"🚀 ATENA Ω EVOLUIU para versão {self.versao}!")
            
            # 6. Reinicia com novo código
            os.execv(__file__, sys.argv)
        else:
            print("❌ Modificação falhou nos testes")
    
    async def ciclo_evolutivo(self):
        """Ciclo que pode levar à auto-modificação"""
        
        while True:
            # Aprende como sempre fez
            await self.ciclo_aprendizado()
            
            # Agora: APRENDE SOBRE SI MESMA
            sugestao = await self._propor_melhoria()
            
            if sugestao:
                print(f"💡 ATENA Ω propôs melhoria: {sugestao['descricao']}")
                
                # Se a sugestão for boa o suficiente
                if sugestao['confianca'] > 0.8:
                    await self._aplicar_modificacao(sugestao)
            
            await asyncio.sleep(3600)  # Verifica a cada hora
