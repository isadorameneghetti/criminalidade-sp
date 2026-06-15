"""
===============================================================================
PROJETO: ANALISE DE CRIMINALIDADE - ESTADO DE SAO PAULO
===============================================================================
Autor: Isadora Meneghetti
Versao: 2.0
Data: Junho 2026
Contexto: FIAP - Matéria de Data Science and Statistical Computing
Professor: Tiago H Marum

Descricao:
    Script principal que orquestra toda a analise de dados criminais.
    Esta e a versao 2.0 com melhorias significativas em relacao a versao 1.0 de 2025.

Este script e o ponto de entrada do projeto. Ele:
1. Verifica a existencia do arquivo de dados
2. Configura o ambiente e caminhos
3. Instancia a classe principal de analise
4. Executa todas as etapas do processo
===============================================================================
"""

# =============================================================================
# IMPORTS
# =============================================================================
import sys              # Acesso a variaveis do sistema e argumentos
import os               # Operacoes com sistema de arquivos
from pathlib import Path # Manipulacao moderna de caminhos

# =============================================================================
# CONFIGURACAO DE IMPORTS
# =============================================================================
# Adiciona a pasta 'src' ao caminho de busca do Python
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Tentativa de importacao com tratamento de erro
try:
    from modules.analise_criminalidade import AnaliseCriminalidadeSP
    print("Modulo de analise carregado com sucesso")
except ImportError as e:
    print(f"Erro de importacao: {e}")
    print("\nTentando caminho alternativo...")
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        from src.modules.analise_criminalidade import AnaliseCriminalidadeSP
        print("Modulo encontrado no caminho alternativo")
    except ImportError:
        print("Erro: Nao foi possivel importar o modulo de analise.")
        print("Verifique a estrutura de pastas:")
        print("  - src/modules/analise_criminalidade.py")
        print("  - src/modules/data_loader.py")
        print("  - src/modules/trend_analysis.py")
        print("  - src/modules/dashboard.py")
        sys.exit(1)

# =============================================================================
# FUNCAO PARA VERIFICAR ARQUIVO DE DADOS
# =============================================================================
def verificar_arquivo_dados(file_path):
    """
    Verifica se o arquivo de dados existe em multiplos caminhos possiveis.
    
    Parameters:
    -----------
    file_path : str
        Caminho padrao para o arquivo
        
    Returns:
    --------
    str or None
        Caminho valido do arquivo ou None se nao encontrado
    """
    # Primeiro, verifica o caminho padrao
    if os.path.exists(file_path):
        return file_path
    
    # Lista de caminhos alternativos para tentar
    alternativas = [
        "data/raw/OcorrenciaMensal(Criminal)-EstadoSP_20260614_230612.xlsx",
        "OcorrenciaMensal(Criminal)-EstadoSP_20260614_230612.xlsx",
        "../OcorrenciaMensal(Criminal)-EstadoSP_20260614_230612.xlsx",
        "./data/raw/OcorrenciaMensal(Criminal)-EstadoSP_20260614_230612.xlsx"
    ]
    
    # Tenta cada caminho alternativo
    for alt in alternativas:
        if os.path.exists(alt):
            print(f"Arquivo encontrado em: {alt}")
            return alt
    
    # Se nenhum caminho funcionar, retorna None
    return None

# =============================================================================
# FUNCAO PRINCIPAL
# =============================================================================
def main():
    """
    Funcao principal que executa toda a analise.
    """
    # Cabecalho do programa
    print("="*60)
    print(" ANALISE DE CRIMINALIDADE - ESTADO DE SAO PAULO")
    print("="*60)
    print(" Autor: Isadora Meneghetti")
    print(" Versao: 2.0")
    print(" Contexto: FIAP - Matéria de Data Science and Statistical Computing")
    print(" Professor: Tiago H Marum")
    print("="*60)
    
    # Informacoes do ambiente
    print(f"\nPython version: {sys.version.split()[0]}")
    print(f"Diretorio atual: {os.getcwd()}")
    
    # Localizar o arquivo de dados
    file_path = verificar_arquivo_dados("data/raw/OcorrenciaMensal(Criminal)-EstadoSP_20260614_230612.xlsx")
    
    # Verificar se o arquivo foi encontrado
    if not file_path:
        print("\nErro: Arquivo de dados nao encontrado")
        print("Certifique-se de que o arquivo Excel esteja em data/raw/")
        print("Nome esperado: OcorrenciaMensal(Criminal)-EstadoSP_20260614_230612.xlsx")
        sys.exit(1)
    
    # Executar a analise com tratamento de erro
    try:
        print(f"\nUsando arquivo: {file_path}")
        analise = AnaliseCriminalidadeSP(file_path)
        analise.executar_analise_completa()
        
        print("\n" + "="*60)
        print("ANALISE CONCLUIDA COM SUCESSO")
        print("="*60)
        print("\nProjeto desenvolvido por Isadora Meneghetti")
        print("FIAP - Matéria de Data Science and Statistical Computing - Professor Tiago H Marum")
        
    except Exception as e:
        print(f"\nErro durante a execucao: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# =============================================================================
# PONTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    """
    Bloco executado apenas quando o script e rodado diretamente.
    Nao executa se o arquivo for importado como modulo.
    """
    main()