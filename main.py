import ast
import inspect
import black
import os
import sys
import asyncio
from datetime import datetime

# 1. IMPORTAÇÃO CRÍTICA: Se AtenaOmega estiver em outro arquivo, importe-a.
# Se estiver no mesmo arquivo, certifique-se de que a classe AtenaOmega 
# esteja definida ACIMA desta linha.
try:
    from atena_base import AtenaOmega 
except ImportError:
    # Se você não usa arquivos separados, defina uma classe base temporária
    # ou garanta que o código pai esteja aqui.
    class AtenaOmega: 
        def __init__(self): pass
        async def ciclo_aprendizado(self): pass

class AtenaEvolutiva(AtenaOmega):
    def __init__(self):
        super().__init__()
        self.versao = "1.0.0"
        self.historico_modificacoes = []
        self.codigo_fonte = self._ler_proprio_codigo()
    
    def _ler_proprio_codigo(self):
        with open(__file__, 'r') as f:
            return f.read()

    async def _testar_novo_codigo(self, novo_codigo):
        """
        FUNÇÃO DE PRÉ-VOO: Testa se o código é sintaticamente correto
        e se não contém erros fatais antes de sobrescrever o arquivo.
        """
        try:
            # Tenta compilar o código em memória
            compile(novo_codigo, '<string>', 'exec')
            
            # Aqui você pode adicionar testes lógicos extras
            return True
        except Exception as e:
            print(f"⚠️ Erro crítico detectado na evolução: {e}")
            return False

    async def _aplicar_modificacao(self, sugestao):
        """MODIFICA O PRÓPRIO CÓDIGO COM VALIDAÇÃO"""
        try:
            arvore = ast.parse(self.codigo_fonte)
            
            # (Simulação da modificação da AST)
            # nova_arvore = self._modificar_ast(arvore, sugestao)
            
            # Por enquanto, gerando o código da árvore atual para teste
            novo_codigo = ast.unparse(arvore) 
            novo_codigo = black.format_str(novo_codigo, mode=black.Mode())
            
            # VALIDAÇÃO ANTES DA ESCRITA
            if await self._testar_novo_codigo(novo_codigo):
                with open(__file__, 'w') as f:
                    f.write(novo_codigo)
                
                print(f"🚀 ATENA Ω EVOLUIU!")
                
                # Reinicia o processo para carregar a nova versão
                os.execv(sys.executable, ['python'] + sys.argv)
            else:
                print("❌ Evolução abortada: O código gerado é inválido.")
        except Exception as e:
            print(f"💥 Falha catastrófica na aplicação: {e}")

    async def ciclo_evolutivo(self):
        while True:
            # Simulação do ciclo
            await self._aplicar_modificacao({'tipo': 'otimização'})
            await asyncio.sleep(1800) # 30 min como no seu YAML
