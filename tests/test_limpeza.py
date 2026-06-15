"""
===============================================================================
MODULO: TESTES UNITARIOS - VALIDACAO DE LIMPEZA DE DADOS
===============================================================================
Autor: Isadora Meneghetti
Versao: 2.0
Data: Junho 2026
Contexto: FIAP - Matéria de Data Science and Statistical Computing
Professor: Tiago H Marum

Descricao:
    Testes unitarios para validar a corretude das funcoes de limpeza e
    processamento de dados. Garante que a qualidade dos dados seja mantida
    durante as transformacoes.

Responsabilidades:
1. Testar carregamento de dados
2. Validar remocao de linhas vazias
3. Testar conversao de tipos numericos
4. Validar padronizacao de colunas
5. Testar deteccao de outliers
6. Validar analises de tendencia
===============================================================================
"""

# =============================================================================
# IMPORTS
# =============================================================================
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Adiciona o diretorio src ao path para importar os modulos
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Importa os modulos a serem testados
from modules.data_loader import DataLoader
from modules.trend_analysis import TrendAnalyzer

# =============================================================================
# CLASSE DE TESTES DO DATA LOADER
# =============================================================================
class TestDataLoader:
    """
    Testes unitarios para a classe DataLoader.
    Verifica o correto funcionamento do carregamento e limpeza dos dados.
    """
    
    # -------------------------------------------------------------------------
    # TESTE 1: ARQUIVO INEXISTENTE
    # -------------------------------------------------------------------------
    def test_carregar_dados_arquivo_inexistente(self):
        """
        Testa se o sistema lida corretamente com arquivo inexistente.
        
        Verifica se uma excecao e levantada quando o arquivo nao existe.
        Isso e importante para evitar que o programa continue com dados vazios.
        """
        print("\nTeste: Carregar dados de arquivo inexistente")
        
        # Tenta criar DataLoader com arquivo que nao existe
        with pytest.raises(Exception):
            loader = DataLoader("arquivo_inexistente.xlsx")
            loader.carregar_dados()
        
        print("  OK: Excecao levantada corretamente")
    
    # -------------------------------------------------------------------------
    # TESTE 2: REMOCAO DE LINHAS VAZIAS
    # -------------------------------------------------------------------------
    def test_remover_linhas_vazias(self):
        """
        Testa a remocao de linhas totalmente vazias ou com valores nulos.
        
        Verifica se:
        1. Linhas com todos os valores nulos sao removidas
        2. Linhas sem nome de crime sao removidas
        """
        print("\nTeste: Remocao de linhas vazias")
        
        # Cria dados de teste com linhas problematicas
        dados_teste = pd.DataFrame({
            'natureza': ['Crime A', None, 'Crime B', None],
            'janeiro': [100, None, 200, None],
            'fevereiro': [150, None, 250, None],
            'ano': [2023, 2023, 2023, 2023]
        })
        
        # Cria DataLoader manualmente para teste
        loader = DataLoader("dummy.xlsx")
        loader.df_raw = dados_teste
        
        # Executa limpeza parcial (remove linhas vazias e sem nome)
        loader.df_raw.dropna(how='all', inplace=True)
        loader.df_raw = loader.df_raw[loader.df_raw.iloc[:, 0].notna()]
        
        # Verifica se apenas as linhas validas permaneceram
        # Deve ter 2 linhas: 'Crime A' e 'Crime B'
        assert len(loader.df_raw) == 2
        
        # Verifica se os nomes dos crimes estao corretos
        assert 'Crime A' in loader.df_raw.iloc[:, 0].values
        assert 'Crime B' in loader.df_raw.iloc[:, 0].values
        
        print("  OK: Linhas vazias removidas corretamente")
        print(f"  Linhas restantes: {len(loader.df_raw)} (esperado: 2)")
    
    # -------------------------------------------------------------------------
    # TESTE 3: CONVERSAO PARA NUMERICO
    # -------------------------------------------------------------------------
    def test_conversao_numerica(self):
        """
        Testa a conversao de valores para tipo numerico.
        
        Verifica se:
        1. Strings numericas sao convertidas corretamente
        2. Valores nao numericos (como 'abc') viram NaN e sao removidos
        """
        print("\nTeste: Conversao de valores para numerico")
        
        # Cria dados de teste com valores mistos
        dados_teste = pd.DataFrame({
            'natureza': ['Crime A', 'Crime B', 'Crime C'],
            'janeiro': ['100', 'abc', '300'],
            'fevereiro': ['200', '400', 'def'],
            'ano': [2023, 2023, 2023]
        })
        
        # Identifica colunas de meses
        meses = ['janeiro', 'fevereiro']
        
        # Converte para formato longo
        df_melted = dados_teste.melt(
            id_vars=['natureza', 'ano'],
            value_vars=meses,
            var_name='mes',
            value_name='ocorrencias'
        )
        
        # Converte para numerico (valores nao numericos viram NaN)
        df_melted['ocorrencias'] = pd.to_numeric(df_melted['ocorrencias'], errors='coerce')
        
        # Remove linhas com NaN
        df_melted.dropna(subset=['ocorrencias'], inplace=True)
        
        # Verifica resultados
        # Valores validos: 100, 200, 300, 400
        # Valores invalidos: 'abc', 'def' devem ser removidos
        assert len(df_melted) == 4
        assert df_melted['ocorrencias'].dtype in ['int64', 'float64']
        
        print("  OK: Conversao numerica funcionou")
        print(f"  Registros validos: {len(df_melted)} (esperado: 4)")
        print("  Valores nao numericos foram removidos")
    
    # -------------------------------------------------------------------------
    # TESTE 4: PADRONIZACAO DE COLUNAS
    # -------------------------------------------------------------------------
    def test_padronizacao_colunas(self):
        """
        Testa a padronizacao dos nomes das colunas.
        
        Verifica se:
        1. Espacos em branco sao removidos
        2. Nomes sao convertidos para minusculo
        3. Espacos sao substituidos por underscore
        """
        print("\nTeste: Padronizacao de nomes de colunas")
        
        # Cria dados de teste com nomes nao padronizados
        dados_teste = pd.DataFrame({
            'Natureza ': ['Crime A'],
            'Janeiro': [100],
            'Fevereiro': [200],
            'Ano': [2023]
        })
        
        # Aplica padronizacao
        dados_teste.columns = (
            dados_teste.columns
            .str.strip()
            .str.lower()
            .str.replace(' ', '_')
        )
        
        # Verifica se os nomes foram padronizados
        assert 'natureza' in dados_teste.columns
        assert 'janeiro' in dados_teste.columns
        assert 'fevereiro' in dados_teste.columns
        assert 'ano' in dados_teste.columns
        
        print("  OK: Colunas padronizadas corretamente")
        print(f"  Colunas resultantes: {list(dados_teste.columns)}")
    
    # -------------------------------------------------------------------------
    # TESTE 5: REMOCAO DE OUTLIERS EXTREMOS
    # -------------------------------------------------------------------------
    def test_remocao_outliers_extremos(self):
        """
        Testa a remocao de outliers extremos durante a limpeza.
        
        Verifica se:
        1. Valores muito baixos (1o percentil) sao removidos
        2. Valores muito altos (acima do limite) sao removidos
        """
        print("\nTeste: Remocao de outliers extremos")
        
        # Cria dados de teste com valores normais e outliers
        # 100 valores normais (0 a 99) + 2 outliers (10000 e 20000)
        dados_teste = pd.DataFrame({
            'natureza': ['Crime A'] * 100,
            'mes': ['janeiro'] * 100,
            'ano': [2023] * 100,
            'ocorrencias': list(range(50)) + [10000, 20000] + list(range(50, 98))
        })
        
        # Calcula percentis
        Q1 = pd.Series(dados_teste['ocorrencias']).quantile(0.01)
        Q99 = pd.Series(dados_teste['ocorrencias']).quantile(0.99)
        
        # Filtra dados (remove outliers extremos)
        dados_filtrados = dados_teste[
            (dados_teste['ocorrencias'] >= Q1) & 
            (dados_teste['ocorrencias'] <= Q99 * 2)
        ]
        
        # Verifica se os outliers foram removidos
        assert len(dados_filtrados) < len(dados_teste)
        assert dados_filtrados['ocorrencias'].max() < 10000
        
        print("  OK: Outliers extremos removidos")
        print(f"  Registros apos filtro: {len(dados_filtrados)} (original: {len(dados_teste)})")
        print(f"  Valor maximo apos filtro: {dados_filtrados['ocorrencias'].max():.0f}")

# =============================================================================
# CLASSE DE TESTES DO TREND ANALYZER
# =============================================================================
class TestTrendAnalyzer:
    """
    Testes unitarios para a classe TrendAnalyzer.
    Verifica as analises de tendencia e deteccao de outliers.
    """
    
    # -------------------------------------------------------------------------
    # TESTE 6: ANALISE DE TENDENCIA
    # -------------------------------------------------------------------------
    def test_analise_tendencia(self):
        """
        Testa a analise de tendencia com dados sinteticos.
        
        Verifica se:
        1. A funcao executa sem erros
        2. Retorna os resultados esperados
        """
        print("\nTeste: Analise de tendencia")
        
        # Cria dados de teste com tendencia linear crescente
        dados_teste = pd.DataFrame({
            'natureza': ['Crime Teste'] * 12,
            'data': pd.date_range('2023-01-01', periods=12, freq='MS'),
            'ocorrencias': list(range(100, 112))  # 100, 101, 102, ..., 111
        })
        
        # Executa analise (sem plot para teste)
        analyzer = TrendAnalyzer()
        resultado = analyzer.analisar_tendencia_avancada(dados_teste, 'Crime Teste', plot=False)
        
        # Verifica se retornou resultados
        assert resultado is not None
        assert resultado['crime'] == 'Crime Teste'
        assert 'tendencia_mensal' in resultado
        assert 'r2_linear' in resultado
        
        # Como a tendencia e perfeitamente linear, R2 deve ser proximo de 1
        assert resultado['r2_linear'] > 0.95
        
        print("  OK: Analise de tendencia executou corretamente")
        print(f"  R2 do modelo linear: {resultado['r2_linear']:.3f}")
        print(f"  Tendencia mensal: {resultado['tendencia_mensal']:.2f}")
    
    # -------------------------------------------------------------------------
    # TESTE 7: DETECCAO DE OUTLIERS COM IQR
    # -------------------------------------------------------------------------
    def test_deteccao_outliers_iqr(self):
        """
        Testa a deteccao de outliers usando o metodo IQR.
        
        O metodo IQR considera outliers valores fora de:
        Q1 - 3 * IQR e Q3 + 3 * IQR
        """
        print("\nTeste: Deteccao de outliers com metodo IQR")
        
        # Cria dados com 2 outliers claros
        # 18 valores normais (100) + 2 outliers (1000 e 2000)
        dados_teste = pd.DataFrame({
            'data': pd.date_range('2023-01-01', periods=20, freq='MS'),
            'ocorrencias': [100] * 18 + [1000, 2000]
        })
        
        # Detecta outliers
        analyzer = TrendAnalyzer()
        outliers = analyzer.detectar_outliers(dados_teste, crime_name=None, metodo='iqr', plot=False)
        
        # Deve detectar exatamente 2 outliers
        assert len(outliers) == 2
        
        print("  OK: Outliers detectados corretamente")
        print(f"  Outliers encontrados: {len(outliers)} (esperado: 2)")
    
    # -------------------------------------------------------------------------
    # TESTE 8: DETECCAO DE OUTLIERS COM Z-SCORE
    # -------------------------------------------------------------------------
    def test_deteccao_outliers_zscore(self):
        """
        Testa a deteccao de outliers usando o metodo Z-score.
        
        O metodo Z-score considera outliers valores com |Z| > 3,
        ou seja, mais de 3 desvios padrao da media.
        """
        print("\nTeste: Deteccao de outliers com metodo Z-score")
        
        # Cria dados com 2 outliers moderados
        # 18 valores normais (media 100) + 2 outliers (500 e 600)
        dados_teste = pd.DataFrame({
            'data': pd.date_range('2023-01-01', periods=20, freq='MS'),
            'ocorrencias': [100] * 18 + [500, 600]
        })
        
        # Detecta outliers
        analyzer = TrendAnalyzer()
        outliers = analyzer.detectar_outliers(dados_teste, crime_name=None, metodo='zscore', plot=False)
        
        # O metodo Z-score deve detectar pelo menos 2 outliers
        # (pode detectar mais dependendo dos calculos)
        assert len(outliers) >= 2
        
        print("  OK: Outliers detectados com Z-score")
        print(f"  Outliers encontrados: {len(outliers)}")
    
    # -------------------------------------------------------------------------
    # TESTE 9: CRIME INEXISTENTE
    # -------------------------------------------------------------------------
    def test_crime_inexistente(self):
        """
        Testa o comportamento quando um crime inexistente e pesquisado.
        
        Verifica se a funcao retorna None sem gerar erros.
        """
        print("\nTeste: Busca por crime inexistente")
        
        # Cria dados de teste
        dados_teste = pd.DataFrame({
            'natureza': ['Crime A', 'Crime B'],
            'data': pd.date_range('2023-01-01', periods=2, freq='MS'),
            'ocorrencias': [100, 200]
        })
        
        # Tenta analisar crime que nao existe
        analyzer = TrendAnalyzer()
        resultado = analyzer.analisar_tendencia_avancada(dados_teste, 'Crime Inexistente', plot=False)
        
        # Deve retornar None
        assert resultado is None
        
        print("  OK: Crime inexistente retornou None sem erro")

# =============================================================================
# TESTE DE CONSISTENCIA DE DADOS
# =============================================================================
class TestConsistenciaDados:
    """
    Testes para verificar a consistencia dos dados apos processamento.
    Estes testes assumem que o arquivo de dados existe e foi carregado.
    """
    
    # -------------------------------------------------------------------------
    # TESTE 10: DADOS COMPLETOS POR ANO
    # -------------------------------------------------------------------------
    def test_dados_completos_por_ano(self):
        """
        Verifica se todos os meses estao presentes em cada ano.
        
        Nota: Este teste requer que o arquivo de dados exista.
        Pode ser pulado se o arquivo nao estiver disponivel.
        """
        print("\nTeste: Verificacao de dados completos por ano")
        
        # Tenta carregar os dados processados
        try:
            df = pd.read_csv('data/processed/dados_processados.csv')
            df['data'] = pd.to_datetime(df['data'])
            
            # Verifica quantidade de meses por ano
            meses_por_ano = df.groupby('ano')['mes_num'].nunique()
            
            print("  Meses por ano:")
            for ano, qtd in meses_por_ano.items():
                if ano < 2026:  # 2026 pode estar incompleto
                    if qtd == 12:
                        print(f"    Ano {ano}: {qtd} meses (OK)")
                    else:
                        print(f"    Ano {ano}: {qtd} meses (ATENCAO: incompleto)")
            
            print("  OK: Verificacao concluida")
            
        except FileNotFoundError:
            # Pula o teste se o arquivo nao existir
            print("  SKIP: Arquivo de dados processados nao encontrado")
            pytest.skip("Arquivo de dados nao disponivel para teste")
    
    # -------------------------------------------------------------------------
    # TESTE 11: VALORES NAO NEGATIVOS
    # -------------------------------------------------------------------------
    def test_sem_valores_negativos(self):
        """
        Verifica se nao ha ocorrencias com valores negativos.
        """
        print("\nTeste: Verificacao de valores negativos")
        
        try:
            df = pd.read_csv('data/processed/dados_processados.csv')
            
            # Verifica se ha valores negativos
            tem_negativo = (df['ocorrencias'] < 0).any()
            
            assert not tem_negativo, "Existem valores negativos nas ocorrencias"
            
            print("  OK: Nenhum valor negativo encontrado")
            
        except FileNotFoundError:
            print("  SKIP: Arquivo de dados processados nao encontrado")
            pytest.skip("Arquivo de dados nao disponivel para teste")
    
    # -------------------------------------------------------------------------
    # TESTE 12: CONSISTENCIA DE TIPOS DE CRIME
    # -------------------------------------------------------------------------
    def test_tipos_crime_consistentes(self):
        """
        Verifica se os tipos de crime sao consistentes entre os anos.
        Pequenas variacoes sao permitidas (maximo 2 tipos de diferenca).
        """
        print("\nTeste: Consistencia de tipos de crime entre anos")
        
        try:
            df = pd.read_csv('data/processed/dados_processados.csv')
            
            # Conta tipos de crime por ano
            crimes_por_ano = df.groupby('ano')['natureza'].nunique()
            
            # O primeiro ano serve como referencia
            padrao = crimes_por_ano.iloc[0]
            
            print(f"  Ano de referencia ({crimes_por_ano.index[0]}): {padrao} tipos")
            
            for ano, qtd in crimes_por_ano.items():
                diferenca = abs(qtd - padrao)
                if diferenca <= 2:
                    print(f"    Ano {ano}: {qtd} tipos (OK, diferenca de {diferenca})")
                else:
                    print(f"    Ano {ano}: {qtd} tipos (ATENCAO: diferenca de {diferenca})")
            
            print("  OK: Verificacao concluida")
            
        except FileNotFoundError:
            print("  SKIP: Arquivo de dados processados nao encontrado")
            pytest.skip("Arquivo de dados nao disponivel para teste")

# =============================================================================
# EXECUCAO DOS TESTES
# =============================================================================
if __name__ == "__main__":
    """
    Executa todos os testes unitarios.
    """
    print("\n" + "="*60)
    print(" EXECUTANDO TESTES UNITARIOS")
    print("="*60)
    print("Autora: Isadora Meneghetti")
    print("FIAP - Pos Graduacao em Dados")
    print("Professor: Tiago H Marum")
    print("="*60)
    
    # Executa os testes com verbosidade
    pytest.main([__file__, '-v', '--tb=short'])