"""
===============================================================================
MODULO: TREND ANALYSIS - ANALISE DE TENDENCIAS E PREVISOES
===============================================================================
Autor: Isadora Meneghetti
Versao: 2.0
Data: Junho 2026
Contexto: FIAP - Matéria de Data Science and Statistical Computing
Professor: Tiago H Marum

Descricao:
    Analise avancada de tendencias criminais com multiplos modelos.
    Melhorias significativas em relacao a versao 1.0 (2025):
    - Adicao de regressao polinomial
    - Implementacao do modelo Holt-Winters para previsao sazonal
    - Decomposicao classica de series temporais
    - Deteccao robusta de outliers com IQR e Z-score

Responsabilidades:
1. Analisar tendencias temporais usando multiplos modelos
2. Fazer previsoes sazonais com Holt-Winters
3. Decompor series temporais em componentes
4. Detectar outliers usando metodos IQR e Z-score
5. Gerar graficos profissionais das analises
===============================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from scipy import stats
from sklearn.preprocessing import PolynomialFeatures
import warnings
warnings.filterwarnings('ignore')

# Tenta importar statsmodels (necessario para previsao sazonal)
try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    from statsmodels.tsa.seasonal import seasonal_decompose
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False
    print("Statsmodels nao disponivel. Instale com: pip install statsmodels")

class TrendAnalyzer:
    """
    Classe para analise de tendencias temporais e previsoes.
    
    Implementa multiplas tecnicas de analise de series temporais:
    - Regressao linear (tendencia simples)
    - Regressao polinomial (captura nao-linearidades)
    - Media movel (suavizacao)
    - Holt-Winters (previsao com sazonalidade)
    - Decomposicao classica
    """
    
    @staticmethod
    def analisar_tendencia_avancada(df, crime_name, plot=True, save_path=None):
        """
        Analise de tendencia com multiplos modelos.
        
        Compara diferentes abordagens para encontrar o melhor modelo.
        
        Parameters:
        -----------
        df : DataFrame
            Dados processados
        crime_name : str
            Nome do crime a ser analisado
        plot : bool
            Se True, gera graficos
        save_path : str
            Caminho para salvar o grafico
            
        Returns:
        --------
        dict
            Resultados da analise
        """
        # Filtrar dados do crime especifico
        df_crime = df[df['natureza'] == crime_name].copy()
        
        if df_crime.empty:
            print(f"Crime '{crime_name}' nao encontrado")
            return None
        
        # Preparar dados para regressao
        df_crime.sort_values('data', inplace=True)
        df_crime['time_index'] = np.arange(len(df_crime))
        
        X = df_crime['time_index'].values.reshape(-1, 1)
        y = df_crime['ocorrencias'].values
        
        # MODELO 1: Regressao Linear
        model_linear = LinearRegression()
        model_linear.fit(X, y)
        y_pred_linear = model_linear.predict(X)
        r2_linear = r2_score(y, y_pred_linear)
        mae_linear = mean_absolute_error(y, y_pred_linear)
        rmse_linear = np.sqrt(mean_squared_error(y, y_pred_linear))
        
        # MODELO 2: Regressao Polinomial (grau 2)
        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)
        model_poly = LinearRegression()
        model_poly.fit(X_poly, y)
        y_pred_poly = model_poly.predict(X_poly)
        r2_poly = r2_score(y, y_pred_poly)
        
        # MODELO 3: Media Movel (suavizacao)
        janela = min(3, len(y))
        ma = pd.Series(y).rolling(window=janela).mean()
        
        # Selecionar melhor modelo
        if r2_poly > r2_linear + 0.05:
            melhor_modelo = "Polinomial (grau 2)"
            melhor_r2 = r2_poly
        else:
            melhor_modelo = "Linear"
            melhor_r2 = r2_linear
        
        # Exibir resultados
        print(f"\n--- ANALISE DE TENDENCIA AVANCADA: {crime_name[:40]} ---")
        print(f"Modelo Linear: R2={r2_linear:.3f}, MAE={mae_linear:.1f}, RMSE={rmse_linear:.1f}")
        print(f"Modelo Polinomial: R2={r2_poly:.3f}")
        print(f"Melhor modelo: {melhor_modelo} (R2={melhor_r2:.3f})")
        
        direcao = "Crescimento" if model_linear.coef_[0] > 0 else "Queda"
        print(f"Tendencia: {direcao} de {abs(model_linear.coef_[0]):.2f} ocorrencias/mes")
        print(f"Projecao anual: {abs(model_linear.coef_[0] * 12):.0f} ocorrencias/ano")
        
        # Gerar graficos
        if plot:
            fig, axes = plt.subplots(1, 3, figsize=(15, 5))
            fig.suptitle(f'Analise de Tendencia - {crime_name[:50]}', fontsize=14, fontweight='bold')
            
            # Grafico 1: Regressao Linear
            axes[0].plot(df_crime['data'], y, 'o-', label='Dados reais', markersize=4, alpha=0.7)
            axes[0].plot(df_crime['data'], y_pred_linear, '--', label=f'Linear (R2={r2_linear:.3f})', linewidth=2)
            axes[0].set_title('Regressao Linear')
            axes[0].set_xlabel('Data')
            axes[0].set_ylabel('Ocorrencias')
            axes[0].legend()
            axes[0].grid(True, alpha=0.3)
            
            # Grafico 2: Regressao Polinomial
            axes[1].plot(df_crime['data'], y, 'o-', label='Dados reais', markersize=4, alpha=0.7)
            axes[1].plot(df_crime['data'], y_pred_poly, '--', label=f'Polinomial (R2={r2_poly:.3f})', linewidth=2)
            axes[1].set_title('Regressao Polinomial')
            axes[1].set_xlabel('Data')
            axes[1].set_ylabel('Ocorrencias')
            axes[1].legend()
            axes[1].grid(True, alpha=0.3)
            
            # Grafico 3: Media Movel
            axes[2].plot(df_crime['data'], y, 'o-', label='Dados reais', markersize=4, alpha=0.5)
            axes[2].plot(df_crime['data'], ma, 'r-', label=f'Media Movel ({janela} meses)', linewidth=2)
            axes[2].set_title('Suavizacao com Media Movel')
            axes[2].set_xlabel('Data')
            axes[2].set_ylabel('Ocorrencias')
            axes[2].legend()
            axes[2].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path.replace('.png', '_avancado.png'), dpi=150, bbox_inches='tight')
            
            plt.show()
        
        return {
            'crime': crime_name,
            'r2_linear': r2_linear,
            'r2_polynomial': r2_poly,
            'melhor_modelo': melhor_modelo,
            'melhor_r2': melhor_r2,
            'tendencia_mensal': model_linear.coef_[0],
            'tendencia_anual': model_linear.coef_[0] * 12,
            'mae': mae_linear,
            'rmse': rmse_linear,
            'modelo_linear': model_linear
        }
    
    @staticmethod
    def previsao_sazonal_holtwinters(df, crime_name, periodo_previsao=12, plot=True, save_path=None):
        """
        Previsao usando modelo Holt-Winters para series com sazonalidade.
        
        O modelo Holt-Winters e ideal para series temporais que apresentam:
        - Tendencia (crescimento ou queda ao longo do tempo)
        - Sazonalidade (padroes que se repetem anualmente)
        
        Parameters:
        -----------
        df : DataFrame
            Dados processados
        crime_name : str
            Nome do crime
        periodo_previsao : int
            Numero de meses para previsao (padrao: 12 meses)
        plot : bool
            Se True, gera grafico
        save_path : str
            Caminho para salvar o grafico
            
        Returns:
        --------
        dict
            Resultados da previsao
        """
        if not STATSMODELS_AVAILABLE:
            print("Statsmodels nao disponivel. Instale com: pip install statsmodels")
            return None
        
        # Filtrar dados
        df_crime = df[df['natureza'] == crime_name].copy()
        
        if df_crime.empty:
            print(f"Crime '{crime_name}' nao encontrado")
            return None
        
        # Preparar serie temporal completa
        df_crime.sort_values('data', inplace=True)
        serie = df_crime.set_index('data')['ocorrencias']
        
        # Preencher meses faltantes com a media
        todos_meses = pd.date_range(start=serie.index.min(), end=serie.index.max(), freq='MS')
        serie_completa = serie.reindex(todos_meses)
        serie_completa.fillna(serie_completa.mean(), inplace=True)
        
        # Verificar dados suficientes (minimo 24 meses)
        if len(serie_completa) < 24:
            print(f"Dados insuficientes para Holt-Winters (minimo 24 meses, tem {len(serie_completa)})")
            return None
        
        try:
            # Modelo Holt-Winters com tendencia e sazonalidade aditivas
            modelo = ExponentialSmoothing(
                serie_completa,
                seasonal_periods=12,
                trend='add',
                seasonal='add',
                initialization_method='estimated'
            ).fit()
            
            # Gerar previsoes
            previsao = modelo.forecast(periodo_previsao)
            datas_futuras = pd.date_range(
                start=serie_completa.index[-1] + pd.DateOffset(months=1),
                periods=periodo_previsao,
                freq='MS'
            )
            
            # Calcular intervalo de confianca (95%)
            residuos = modelo.resid
            if len(residuos) > 0 and not np.isnan(residuos).all():
                erro_padrao = np.std(residuos)
            else:
                erro_padrao = previsao.std() * 0.1
            
            intervalo_superior = previsao + 1.96 * erro_padrao
            intervalo_inferior = previsao - 1.96 * erro_padrao
            intervalo_inferior = intervalo_inferior.clip(lower=0)
            
            # Gerar grafico
            if plot:
                fig, ax = plt.subplots(figsize=(14, 6))
                fig.suptitle(f'Previsao Sazonal - {crime_name[:50]}', fontsize=14, fontweight='bold')
                
                ax.plot(serie_completa.index, serie_completa.values, 'o-', label='Historico', markersize=4, alpha=0.7)
                ax.plot(datas_futuras, previsao, 's-', label=f'Previsao ({periodo_previsao} meses)', color='red', markersize=5, linewidth=2)
                ax.fill_between(datas_futuras, intervalo_inferior, intervalo_superior, alpha=0.2, color='red', label='IC 95%')
                
                ax.set_xlabel('Data')
                ax.set_ylabel('Ocorrencias')
                ax.legend()
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                
                if save_path:
                    plt.savefig(save_path.replace('.png', '_holtwinters.png'), dpi=150, bbox_inches='tight')
                
                plt.show()
            
            print(f"\n--- PREVISAO SAZONAL: {crime_name[:40]} ---")
            print(f"AIC do modelo: {modelo.aic:.1f}")
            print(f"\nPrevisao para os proximos {periodo_previsao} meses:")
            for i in range(min(6, periodo_previsao)):
                print(f"  {datas_futuras[i].strftime('%B %Y')}: {previsao.iloc[i]:.0f} ocorrencias")
            
            return {
                'crime': crime_name,
                'previsao': previsao,
                'datas': datas_futuras,
                'intervalo_superior': intervalo_superior,
                'intervalo_inferior': intervalo_inferior,
                'aic': modelo.aic
            }
            
        except Exception as e:
            print(f"Erro no modelo Holt-Winters: {e}")
            return None
    
    @staticmethod
    def decompor_serie_temporal(df, crime_name, plot=True, save_path=None):
        """
        Decompoe a serie temporal em tendencia, sazonalidade e residuo.
        
        A decomposicao classica separa a serie em tres componentes:
        - Tendencia: movimento de longo prazo
        - Sazonalidade: padrao que se repete anualmente
        - Residuo: variacao aleatoria (ruido)
        
        Parameters:
        -----------
        df : DataFrame
            Dados processados
        crime_name : str
            Nome do crime
        plot : bool
            Se True, gera grafico
        save_path : str
            Caminho para salvar o grafico
            
        Returns:
        --------
        dict
            Componentes da decomposicao
        """
        if not STATSMODELS_AVAILABLE:
            print("Statsmodels nao disponivel. Instale com: pip install statsmodels")
            return None
        
        # Filtrar dados
        df_crime = df[df['natureza'] == crime_name].copy()
        
        if len(df_crime) < 24:
            print(f"Dados insuficientes para decomposicao (minimo 24 meses, tem {len(df_crime)})")
            return None
        
        # Preparar serie completa
        df_crime.sort_values('data', inplace=True)
        
        todos_meses = pd.date_range(
            start=df_crime['data'].min(),
            end=df_crime['data'].max(),
            freq='MS'
        )
        
        serie_completa = pd.Series(index=todos_meses)
        serie_completa.update(df_crime.set_index('data')['ocorrencias'])
        serie_completa.fillna(serie_completa.mean(), inplace=True)
        
        try:
            # Decomposicao aditiva: Y = Tendencia + Sazonalidade + Residuo
            decomposicao = seasonal_decompose(serie_completa, model='additive', period=12)
            
            # Calcular contribuicao de cada componente
            var_total = np.var(decomposicao.observed)
            var_trend = np.var(decomposicao.trend) if not np.isnan(decomposicao.trend).all() else 0
            var_seasonal = np.var(decomposicao.seasonal) if not np.isnan(decomposicao.seasonal).all() else 0
            var_resid = np.var(decomposicao.resid) if not np.isnan(decomposicao.resid).all() else 0
            
            if var_total > 0:
                pct_trend = (var_trend / var_total) * 100
                pct_seasonal = (var_seasonal / var_total) * 100
                pct_resid = (var_resid / var_total) * 100
            else:
                pct_trend = pct_seasonal = pct_resid = 0
            
            print(f"\n--- DECOMPOSICAO DA SERIE: {crime_name[:40]} ---")
            print(f"Tendencia explica {pct_trend:.1f}% da variacao")
            print(f"Sazonalidade explica {pct_seasonal:.1f}% da variacao")
            print(f"Ruido explica {pct_resid:.1f}% da variacao")
            
            # Gerar grafico
            if plot:
                fig, axes = plt.subplots(4, 1, figsize=(14, 12))
                fig.suptitle(f'Decomposicao da Serie Temporal - {crime_name[:50]}', fontsize=14, fontweight='bold')
                
                axes[0].plot(decomposicao.observed.index, decomposicao.observed.values, 'o-', markersize=3)
                axes[0].set_title('1. Serie Original')
                axes[0].set_ylabel('Ocorrencias')
                axes[0].grid(True, alpha=0.3)
                
                axes[1].plot(decomposicao.trend.index, decomposicao.trend.values, 'g-', linewidth=2)
                axes[1].set_title(f'2. Tendencia ({pct_trend:.1f}% da variacao)')
                axes[1].set_ylabel('Ocorrencias')
                axes[1].grid(True, alpha=0.3)
                
                axes[2].plot(decomposicao.seasonal.index, decomposicao.seasonal.values, 'orange', linewidth=2)
                axes[2].set_title(f'3. Sazonalidade ({pct_seasonal:.1f}% da variacao)')
                axes[2].set_ylabel('Efeito sazonal')
                axes[2].grid(True, alpha=0.3)
                
                axes[3].plot(decomposicao.resid.index, decomposicao.resid.values, 'r.', markersize=3)
                axes[3].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
                axes[3].set_title(f'4. Residuos (Ruido) - {pct_resid:.1f}% da variacao')
                axes[3].set_ylabel('Residuos')
                axes[3].set_xlabel('Data')
                axes[3].grid(True, alpha=0.3)
                
                plt.tight_layout()
                
                if save_path:
                    plt.savefig(save_path.replace('.png', '_decomposicao.png'), dpi=150, bbox_inches='tight')
                
                plt.show()
            
            return {
                'crime': crime_name,
                'tendencia': decomposicao.trend,
                'sazonalidade': decomposicao.seasonal,
                'residuos': decomposicao.resid,
                'variancia_trend_pct': pct_trend,
                'variancia_seasonal_pct': pct_seasonal,
                'variancia_resid_pct': pct_resid
            }
            
        except Exception as e:
            print(f"Erro na decomposicao: {e}")
            return None
    
    @staticmethod
    def detectar_outliers(df, crime_name=None, metodo='iqr', plot=True, save_path=None):
        """
        Detecta outliers (valores anormais) em series temporais.
        
        Duas abordagens:
        - IQR: valores fora de Q1-3*IQR ou Q3+3*IQR
        - Z-score: valores com mais de 3 desvios padrao da media
        
        Parameters:
        -----------
        df : DataFrame
            Dados processados
        crime_name : str or None
            Nome do crime ou None para total geral
        metodo : str
            'iqr' ou 'zscore'
        plot : bool
            Se True, gera grafico
        save_path : str
            Caminho para salvar o grafico
            
        Returns:
        --------
        DataFrame
            Outliers detectados
        """
        # Filtrar dados
        if crime_name:
            df_filtrado = df[df['natureza'] == crime_name].copy()
            titulo = f"Outliers - {crime_name}"
        else:
            df_filtrado = df.groupby('data')['ocorrencias'].sum().reset_index()
            titulo = "Outliers - Total Geral"
        
        # Metodo IQR (Intervalo Interquartil)
        if metodo == 'iqr':
            Q1 = df_filtrado['ocorrencias'].quantile(0.25)
            Q3 = df_filtrado['ocorrencias'].quantile(0.75)
            IQR = Q3 - Q1
            limite_inferior = Q1 - 3 * IQR
            limite_superior = Q3 + 3 * IQR
            outliers = df_filtrado[
                (df_filtrado['ocorrencias'] < limite_inferior) |
                (df_filtrado['ocorrencias'] > limite_superior)
            ]
        # Metodo Z-score
        else:
            z_scores = np.abs(stats.zscore(df_filtrado['ocorrencias']))
            outliers = df_filtrado[z_scores > 3]
            limite_superior = df_filtrado['ocorrencias'].mean() + 3 * df_filtrado['ocorrencias'].std()
            limite_inferior = df_filtrado['ocorrencias'].mean() - 3 * df_filtrado['ocorrencias'].std()
        
        # Gerar grafico
        if plot:
            fig, ax = plt.subplots(figsize=(14, 6))
            fig.suptitle(f'Deteccao de Outliers - {titulo}', fontsize=14, fontweight='bold')
            
            x_data = df_filtrado['data'] if 'data' in df_filtrado.columns else df_filtrado.index
            ax.plot(x_data, df_filtrado['ocorrencias'], 'o-', label='Dados', markersize=4, alpha=0.7)
            
            if not outliers.empty:
                x_outliers = outliers['data'] if 'data' in outliers.columns else outliers.index
                ax.scatter(x_outliers, outliers['ocorrencias'], color='red', s=100, zorder=5, label=f'Outliers ({len(outliers)} pontos)')
            
            ax.axhline(y=limite_superior, color='orange', linestyle='--', label=f'Limite superior: {limite_superior:.0f}')
            if limite_inferior > 0:
                ax.axhline(y=limite_inferior, color='orange', linestyle='--', label=f'Limite inferior: {limite_inferior:.0f}')
            
            ax.set_xlabel('Data')
            ax.set_ylabel('Ocorrencias')
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=150, bbox_inches='tight')
            
            plt.show()
        
        # Exibir resultados
        if not outliers.empty:
            print(f"\n--- OUTLIERS DETECTADOS: {titulo} ---")
            print(f"Total de outliers: {len(outliers)}")
            print("\nTop 5 outliers:")
            for i, (idx, row) in enumerate(outliers.head(5).iterrows()):
                if 'data' in row:
                    data_str = row['data'].strftime('%B %Y')
                else:
                    data_str = f"Ponto {idx}"
                print(f"  {i+1}. {data_str}: {row['ocorrencias']:.0f} ocorrencias")
        
        return outliers