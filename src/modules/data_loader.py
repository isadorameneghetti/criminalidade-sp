"""
===============================================================================
MODULO: DATA LOADER - CARREGAMENTO E LIMPEZA DE DADOS
===============================================================================
Autor: Isadora Meneghetti
Versao: 2.0
Data: Junho 2026
Contexto: FIAP - Matéria de Data Science and Statistical Computing
Professor: Tiago H Marum

Descricao:
    Responsavel por carregar e preparar os dados de criminalidade.
    Melhorias na versao 2.0:
    - Tratamento mais robusto de dados faltantes
    - Validacao de tipos de dados
    - Remocao inteligente de outliers extremos

Responsabilidades:
1. Carregar dados de arquivos Excel com multiplas abas (2023-2026)
2. Limpar e padronizar os dados
3. Converter para formato longo (melt) para facilitar analise
4. Tratar valores ausentes e inconsistentes
5. Exportar dados processados para CSV
===============================================================================
"""

# =============================================================================
# IMPORTS
# =============================================================================
import pandas as pd      # Manipulacao de dados
import numpy as np       # Operacoes numericas
from pathlib import Path # Manipulacao de caminhos
import warnings          # Controle de avisos
warnings.filterwarnings('ignore')  # Suprime avisos desnecessarios

# =============================================================================
# CLASSE DATA LOADER
# =============================================================================
class DataLoader:
    """
    Classe responsavel pelo carregamento e preparacao dos dados.
    
    Atributos:
    ----------
    file_path : str
        Caminho para o arquivo Excel
    df_raw : DataFrame
        Dados brutos carregados
    df_processed : DataFrame
        Dados processados e limpos
    
    Metodos:
    --------
    carregar_dados() -> DataFrame
        Carrega os dados do Excel
    limpar_dados() -> DataFrame
        Limpa e prepara os dados
    salvar_dados_processados() -> str
        Salva dados processados em CSV
    """
    
    def __init__(self, file_path):
        """
        Inicializa o DataLoader.
        
        Parameters:
        -----------
        file_path : str
            Caminho para o arquivo Excel
        """
        self.file_path = file_path
        self.df_raw = None
        self.df_processed = None
        
    def carregar_dados(self):
        """
        Carrega dados de todas as abas do Excel.
        
        O arquivo contem uma aba por ano (2023, 2024, 2025, 2026).
        Cada aba possui 23 linhas (tipos de crime) e 15 colunas
        (Natureza, Janeiro a Dezembro, Total).
        
        Returns:
        --------
        DataFrame
            DataFrame concatenado com dados de todos os anos
        
        Raises:
        -------
        ValueError
            Se nenhum dado for carregado
        """
        print("Carregando dados...")
        
        # Lista de anos que serao carregados
        anos = [2023, 2024, 2025, 2026]
        dfs = {}  # Dicionario para armazenar DataFrames por ano
        
        # Loop para carregar cada ano
        for ano in anos:
            try:
                # Tenta ler a aba correspondente ao ano
                df = pd.read_excel(self.file_path, sheet_name=str(ano))
                df['ano'] = ano  # Adiciona coluna com o ano
                dfs[ano] = df
                print(f"  Ano {ano} carregado - {df.shape[0]} linhas, {df.shape[1]} colunas")
            except Exception as e:
                print(f"  Ano {ano} nao encontrado: {e}")
        
        # Verifica se pelo menos um ano foi carregado
        if not dfs:
            raise ValueError("Nenhum dado foi carregado. Verifique o arquivo Excel.")
        
        # Concatena todos os DataFrames em um unico
        self.df_raw = pd.concat(dfs.values(), ignore_index=True)
        print(f"Total de dados carregados: {self.df_raw.shape}")
        
        return self.df_raw
    
    def limpar_dados(self):
        """
        Limpa e prepara os dados para analise.
        
        Etapas de limpeza:
        1. Remove linhas totalmente vazias
        2. Remove linhas onde o nome do crime esta vazio
        3. Padroniza nomes das colunas (minusculo, sem acentos, sem espacos)
        4. Converte de formato largo para longo
        5. Converte valores para numerico
        6. Cria coluna de data sequencial
        7. Remove outliers extremos
        
        Returns:
        --------
        DataFrame
            Dados processados e prontos para analise
        """
        # Verifica se os dados foram carregados
        if self.df_raw is None:
            raise ValueError("Carregue os dados primeiro usando carregar_dados()")
        
        print("\nLimpando dados...")
        
        # ETAPA 1: Remover linhas totalmente vazias
        self.df_raw.dropna(how='all', inplace=True)
        
        # ETAPA 2: Remover linhas sem nome de crime
        first_col = self.df_raw.columns[0]
        self.df_raw = self.df_raw[self.df_raw[first_col].notna()]
        
        # ETAPA 3: Padronizar nomes das colunas
        # Converte para minusculo, remove espacos, substitui acentos
        self.df_raw.columns = (
            self.df_raw.columns
            .str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.replace('ç', 'c')
            .str.replace('ã', 'a')
            .str.replace('á', 'a')
            .str.replace('é', 'e')
            .str.replace('í', 'i')
            .str.replace('ó', 'o')
            .str.replace('ú', 'u')
        )
        
        # ETAPA 4: Lista de meses em portugues
        meses = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho',
                 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
        
        # Verifica quais meses existem no DataFrame
        meses_existentes = [m for m in meses if m in self.df_raw.columns]
        if not meses_existentes:
            raise ValueError("Nenhuma coluna de mes encontrada no arquivo")
        
        # ETAPA 5: Converter para formato longo
        # Transforma de "meses como colunas" para "uma coluna de meses"
        df_melted = self.df_raw.melt(
            id_vars=['natureza', 'ano'],
            value_vars=meses_existentes,
            var_name='mes',
            value_name='ocorrencias'
        )
        
        # ETAPA 6: Limpeza adicional
        df_melted.dropna(subset=['ocorrencias'], inplace=True)
        df_melted['ocorrencias'] = pd.to_numeric(df_melted['ocorrencias'], errors='coerce')
        df_melted.dropna(subset=['ocorrencias'], inplace=True)
        
        # ETAPA 7: Mapeamento de meses para numeros
        mes_map = {mes: i+1 for i, mes in enumerate(meses)}
        df_melted['mes_num'] = df_melted['mes'].map(mes_map)
        
        # ETAPA 8: Criar data sequencial (primeiro dia do mes)
        df_melted['data'] = pd.to_datetime(
            df_melted['ano'].astype(str) + '-' +
            df_melted['mes_num'].astype(str) + '-01',
            errors='coerce'
        )
        
        # Remove datas invalidas
        df_melted.dropna(subset=['data'], inplace=True)
        
        # ETAPA 9: Ordenar por data
        df_melted.sort_values('data', inplace=True)
        
        # ETAPA 10: Remover outliers extremos (1% inferior e valores muito altos)
        Q1 = df_melted['ocorrencias'].quantile(0.01)
        Q99 = df_melted['ocorrencias'].quantile(0.99)
        df_melted = df_melted[
            (df_melted['ocorrencias'] >= Q1) &
            (df_melted['ocorrencias'] <= Q99 * 2)
        ]
        
        # Armazenar resultado
        self.df_processed = df_melted
        
        # Exibir estatisticas finais
        print(f"Dados preparados: {self.df_processed.shape[0]} registros")
        print(f"Periodo: {self.df_processed['data'].min()} a {self.df_processed['data'].max()}")
        print(f"Tipos de crime unicos: {self.df_processed['natureza'].nunique()}")
        
        return self.df_processed
    
    def salvar_dados_processados(self, output_path="data/processed/dados_processados.csv"):
        """
        Salva os dados processados em arquivo CSV.
        
        Parameters:
        -----------
        output_path : str
            Caminho onde o arquivo sera salvo
            
        Returns:
        --------
        str
            Caminho do arquivo salvo
        """
        if self.df_processed is None:
            raise ValueError("Processe os dados primeiro usando limpar_dados()")
        
        # Cria o diretorio se nao existir
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Salva o arquivo CSV com encoding UTF-8
        self.df_processed.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Dados processados salvos em: {output_path}")
        
        return output_path