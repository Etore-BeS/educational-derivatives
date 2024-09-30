import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import plotly.graph_objects as go
import time
import base64
from PIL import Image

# Configuração inicial do Streamlit
st.set_page_config(page_title="Derivativos e Black-Scholes", layout="wide")

# Estilos CSS para melhorar a responsividade e acessibilidade
st.markdown("""
<style>
/* Ajustes gerais */
body {
    background-color: #ffffff;
    color: #000000;
}

/* Ajuste do tamanho dos sliders */
.stSlider > div > div > div > div {
    background-color: #e0e0e0;
    height: 1.5rem;
}
.stSlider > div > div > div > div > div {
    height: 1.5rem;
}

/* Ajuste da barra lateral */
.css-1d391kg {
    width: 300px;
}
@media (max-width: 768px) {
    .css-1d391kg {
        width: 100%;
    }
}

/* Contraste de cores para acessibilidade */
.stButton button {
    background-color: #0052cc;
    color: #ffffff;
}

/* Ajuste do tamanho da fonte para telas menores */
@media only screen and (max-width: 600px) {
    .katex-html {
        font-size: 0.9em !important;
    }
}

/* Permitir rolagem horizontal para as fórmulas LaTeX */
.stLatex {
    overflow-x: auto;
}
</style>
""", unsafe_allow_html=True)

# Função para converter imagem para base64 (opcional, se necessário)
def get_image_base64(image_path):
    try:
        with open(image_path, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

image_base64 = get_image_base64('images/IMG_1269.jpg') 

# Funções auxiliares para cálculos financeiros
def calculate_option_price(S, K, T, r, sigma, option_type):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "Call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

def calculate_delta(S, K, T, r, sigma, option_type):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    if option_type == "Call":
        return norm.cdf(d1)
    else:
        return norm.cdf(d1) - 1

def calculate_gamma(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    return gamma

def calculate_theta(S, K, T, r, sigma, option_type):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "Call":
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))) - r * K * np.exp(-r * T) * norm.cdf(d2)
    else:
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))) + r * K * np.exp(-r * T) * norm.cdf(-d2)
    return theta

def calculate_vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    return vega / 100  # Vega é geralmente expresso por mudança de 1% na volatilidade

def calculate_rho(S, K, T, r, sigma, option_type):
    d2 = (np.log(S / K) + (r - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    if option_type == "Call":
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    else:
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
    return rho / 100  # Rho é geralmente expresso por mudança de 1% na taxa de juros

# Função para criar gráficos responsivos
def create_responsive_plot(fig_func, **kwargs):
    fig, ax = plt.subplots()
    fig_func(ax, **kwargs)
    st.pyplot(fig, use_container_width=True)

# Navegação principal
st.sidebar.title("Navegação")
page = st.sidebar.radio("Escolha uma seção",
    ["Introdução", "Conceitos Básicos", "Compradores vs. Vendedores", "Galton Board", 
     "Movimento Browniano", "Opções", "Black-Scholes", "Gregas", "Simulador Avançado",])

# Seção: Introdução
if page == "Introdução":
    st.title("Derivativos e Black-Scholes ")

    st.header("Visão Geral")
    st.write("""
    Bem-vindo ao nosso site interativo dedicado ao fascinante mundo dos **derivativos financeiros** e à renomada **equação de Black-Scholes**. Este recurso foi criado para fornecer uma compreensão profunda e intuitiva dos conceitos que moldam os mercados financeiros modernos. Seja você um estudante, um profissional de finanças ou simplesmente alguém curioso sobre como funcionam os mercados de opções, este site oferece ferramentas interativas e explicações detalhadas para enriquecer seu conhecimento.
    """)

    st.subheader("História e Impacto da Equação de Black-Scholes")
    st.write("""
    A equação de Black-Scholes, frequentemente referida como "**The Trillion Dollar Equation**" (A Equação de Trilhões de Dólares), revolucionou a forma como as opções são precificadas e negociadas nos mercados financeiros. Desenvolvida em 1973 por **Fischer Black**, **Myron Scholes** e **Robert Merton**, esta equação forneceu um método matemático robusto para calcular o preço teórico das opções europeias, levando em consideração fatores cruciais como o preço do ativo subjacente, a volatilidade do mercado, o tempo até o vencimento da opção e a taxa de juros livre de risco.
    """)

    st.subheader("Origens da Equação: De Louis Bachelier a Ed Thorpe")
    st.write("""
    A história da equação de Black-Scholes remonta ao início do século XX, quando **Louis Bachelier**, um matemático francês, aplicou conceitos de física, como o movimento aleatório de partículas (**Movimento Browniano**), para modelar os preços das ações. Embora seu trabalho tenha sido pioneiro, foi inicialmente ignorado pela comunidade financeira. Décadas depois, **Ed Thorpe**, um físico, redescobriu o trabalho de Bachelier e desenvolveu estratégias de negociação lucrativas baseadas nessas ideias. Reconhecendo o potencial das modelagens matemáticas para prever padrões de mercado, Thorpe pavimentou o caminho para a formulação da equação de Black-Scholes.
    """)

    st.subheader("A Revolução dos Derivativos")
    st.write("""
    Com a introdução da equação de Black-Scholes, o mercado de derivativos experimentou um crescimento explosivo. A capacidade de calcular preços teóricos permitiu que traders e investidores negociassem opções com maior confiança e precisão, transformando os derivativos em ferramentas financeiras essenciais para gestão de risco e especulação.
    """)

    st.subheader("Limitações e Evoluções")
    st.write("""
    Apesar de seu impacto profundo, a equação de Black-Scholes não está isenta de limitações. Suas suposições, como a constante volatilidade dos ativos e a ausência de custos de transação, nem sempre refletem a realidade dos mercados financeiros. No entanto, essas limitações incentivaram o desenvolvimento de modelos financeiros mais sofisticados e a contínua evolução das teorias de precificação de opções.
    """)

    st.subheader("Objetivos deste Site")
    st.write("""
    - **Aprendizado Interativo:** Explorar conceitos complexos através de simuladores e animações interativas.
    - **Entendimento Profundo:** Compreender a aplicação prática da equação de Black-Scholes e suas Gregas.
    - **Ferramentas Avançadas:** Utilizar simuladores avançados para analisar a sensibilidade das opções a diferentes fatores de risco.
    - **Acessibilidade e Usabilidade:** Oferecer uma interface responsiva e acessível para usuários de todos os níveis.
    """)

    st.subheader("Como Navegar")
    st.write("""
    Utilize o menu lateral para explorar as diferentes seções do site. Cada seção é projetada para construir seu conhecimento de forma progressiva, começando com conceitos básicos de probabilidade e risco, passando por ferramentas interativas como o **Galton Board** e simulações de **Movimento Browniano**, até chegar às aplicações práticas da **equação de Black-Scholes** e às **Gregas** que medem os riscos associados às opções.
    """)

    # Adicionar uma separação visual
    st.markdown('---')

    # Layout em colunas para imagem e texto, centralizado
    col_left, col_center, col_right = st.columns([1, 2, 1])  # Proporção 1:2:1

    with col_center:
        col1, col2 = st.columns([1, 2])  # Proporção 1:2 entre as colunas

        with col1:
            try:
                # Carregar e exibir a imagem
                image = Image.open('images/IMG_1269.jpg')  # Atualize o caminho conforme necessário
                st.image(image, caption='Étore Braga e Santos', use_column_width=True)
            except FileNotFoundError:
                st.error("Imagem não encontrada. Verifique o caminho e o nome do arquivo.")

        with col2:
            st.header("Étore Braga e Santos")
            st.markdown("""
            - **Pesquisador de Inteligência Artificial**  |  USP  
            - **Engenheiro de Machine Learning**  |  Klover.ai 
            - **Summer Tech**  |  BTG Pactual  
            """)
            # Adicionar ícones aos links com padding e quebras de linha
            st.markdown("""
            <div style="display: flex; gap: 25px; justify-content: center; padding: 30px; margin-top: 10px;">
                <a href='https://github.com/Etore-BeS' target='_blank'>
                    <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' alt='GitHub' style='width:40px;height:40px;vertical-align: middle;'/>
                </a>
                <a href='https://www.linkedin.com/in/etore-braga/' target='_blank'>
                    <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' alt='LinkedIn' style='width:40px;height:40px;vertical-align: middle;'/>
                </a>
                <a href='mailto:etorebraga@usp.br'>
                    <img src='https://cdn-icons-png.flaticon.com/512/732/732200.png' alt='Email' style='width:40px;height:40px;vertical-align: middle;'/>
                </a>
            </div>
            """, unsafe_allow_html=True)


# Seção: Conceitos Básicos
elif page == "Conceitos Básicos":
    st.title("Conceitos Básicos de Probabilidade e Risco")

    st.header("Distribuição Normal")
    st.write("""
    A **distribuição normal**, também conhecida como distribuição gaussiana, é fundamental para a modelagem de riscos financeiros. Ela descreve como os valores de uma variável se distribuem em torno de uma média, com uma determinada dispersão.
    """)

    col1, col2 = st.columns(2)
    with col1:
        mu = st.slider("Média (μ)", -5.0, 5.0, 0.0, step=0.1)
    with col2:
        sigma = st.slider("Desvio Padrão (σ)", 0.1, 3.0, 1.0, step=0.1)

    def plot_normal_dist(ax, mu, sigma):
        x = np.linspace(-10, 10, 1000)
        y = norm.pdf(x, mu, sigma)
        ax.plot(x, y)
        ax.set_title("Distribuição Normal")
        ax.set_xlabel("Valor")
        ax.set_ylabel("Densidade de Probabilidade")
        ax.set_xlim(-10, 10)
        ax.set_ylim(0, 0.5)
        ax.grid(True)

    create_responsive_plot(plot_normal_dist, mu=mu, sigma=sigma)
    st.caption("Gráfico da distribuição normal com média e desvio padrão ajustáveis.")

    st.subheader("Importância na Finanças")
    st.write("""
    Na modelagem de preços de ativos, a distribuição normal é utilizada para representar a variabilidade dos retornos dos ativos. Entender como a média e o desvio padrão influenciam essa distribuição é crucial para avaliar riscos e oportunidades de investimento.
    """)

    st.subheader("Quiz de Compreensão")
    question = st.radio("O que representa o desvio padrão na distribuição normal?",
                        ["Média dos dados", "Dispersão dos dados", "Valor máximo"])
    if st.button("Verificar Resposta", key="quiz1"):
        if question == "Dispersão dos dados":
            st.success("Correto! O desvio padrão mede a dispersão dos dados em relação à média.")
        else:
            st.error("Resposta incorreta. O desvio padrão mede a dispersão dos dados.")

# Seção: Galton Board
elif page == "Galton Board":
    st.title("Animação do Galton Board")

    st.write("""
    O **Galton Board** é uma ferramenta visual que demonstra como uma distribuição normal emerge a partir de eventos aleatórios binários. Este experimento ilustra o conceito de probabilidade e como pequenas variações individuais podem levar a um padrão previsível em grande escala.
    """)

    st.subheader("Como Funciona")
    st.write("""
    - **Bolas e Níveis:** Bolas são lançadas em um painel com pinos. Cada pino desvia a bola para a esquerda ou para a direita com igual probabilidade.
    - **Acúmulo:** Após passar por múltiplos níveis, as bolas acumulam-se em diferentes posições na base, formando uma distribuição que se aproxima de uma curva em sino.
    """)

    st.subheader("Aplicação em Finanças")
    st.write("""
    O Galton Board ajuda a entender como a variabilidade nos preços dos ativos pode se somar para formar uma distribuição normal, base para a precificação de derivativos e análise de riscos.
    """)

    st.subheader("Animação Interativa")
    st.write("Observe a animação abaixo para visualizar como a distribuição normal se forma conforme as bolas passam pelos níveis do Galton Board.")

    # Exibir o vídeo da animação
    try:
        video_file = open('videos/galton_board.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
    except FileNotFoundError:
        st.error("Arquivo de vídeo 'galton_board.mp4' não encontrado. Por favor, verifique o caminho e tente novamente.")

# Seção: Movimento Browniano
elif page == "Movimento Browniano":
    st.title("Simulação em Tempo Real do Movimento Browniano")

    st.write("""
    O **Movimento Browniano** é um modelo matemático que descreve o movimento aleatório das partículas em um fluido, aplicável à modelagem dos preços dos ativos financeiros.
    """)

    st.subheader("Características do Movimento Browniano")
    st.write("""
    - **Aleatoriedade:** Os preços dos ativos seguem trajetórias imprevisíveis, influenciadas por múltiplos fatores econômicos e financeiros.
    - **Volatilidade:** A medida de quão rapidamente os preços dos ativos variam ao longo do tempo.
    """)

    st.subheader("Aplicação em Finanças")
    st.write("""
    O Movimento Browniano é a base para o modelo de precificação de opções de Black-Scholes, permitindo a simulação de possíveis futuros preços dos ativos e a avaliação de opções com base nesses cenários.
    """)

    st.subheader("Simulação Interativa")
    st.write("""
    Abaixo, você pode iniciar uma simulação em tempo real do Movimento Browniano, ajustando a volatilidade e observando como o preço do ativo evolui ao longo do tempo.
    """)

    volatilidade = st.slider("Volatilidade (σ): Controle o nível de variação do preço do ativo.", 0.1, 0.5, 0.2, 0.01)
    preco_inicial = st.number_input("Preço Inicial: Defina o ponto de partida para a simulação.", 50.0, 150.0, 100.0, 1.0)

    # Espaço para o gráfico
    brownian_chart = st.empty()

    # Parâmetros iniciais
    precos = [preco_inicial]
    t = [0]

    run_simulation = st.button("Iniciar Simulação")

    if run_simulation:
        for i in range(1, 200):
            delta_t = 1
            delta_preco = np.random.normal(0, volatilidade * np.sqrt(delta_t))
            novo_preco = precos[-1] + delta_preco
            precos.append(novo_preco)
            t.append(i)

            # Criação do gráfico
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=t, y=precos, mode='lines', name='Preço'))
            fig.update_layout(title='Movimento Browniano do Preço do Ativo', xaxis_title='Tempo', yaxis_title='Preço')

            brownian_chart.plotly_chart(fig, use_container_width=True)

            time.sleep(0.1)

        st.success("Simulação concluída.")

# Seção: Opções
elif page == "Opções":
    st.title("Entendendo Opções")

    st.write("""
    **Opções** são contratos financeiros que dão ao titular o direito, mas não a obrigação, de comprar ou vender um ativo subjacente a um preço específico antes ou na data de vencimento.
    """)

    st.subheader("Tipos de Opções")
    st.write("""
    - **Call:** Dá o direito de **comprar** o ativo subjacente.
    - **Put:** Dá o direito de **vender** o ativo subjacente.
    """)

    st.header("Simulador de Lucro de uma Opção")
    st.write("""
    Abaixo, você pode visualizar o lucro ou prejuízo de uma opção conforme o preço do ativo no vencimento. Ajuste os parâmetros para entender como diferentes fatores influenciam o desempenho da opção.
    """)

    option_type = st.selectbox("Tipo de Opção", ["Call", "Put"])
    S = st.slider("Preço Atual do Ativo (S)", 0.0, 200.0, 100.0, 1.0)
    K = st.slider("Preço de Exercício (K)", 0.0, 200.0, 100.0, 1.0)
    premium = st.number_input("Prêmio da Opção", 0.0, 50.0, 10.0, 0.5)

    # Função de payoff
    def option_payoff(S_range, K, premium, option_type):
        if option_type == "Call":
            payoff = np.maximum(S_range - K, 0) - premium
        else:
            payoff = np.maximum(K - S_range, 0) - premium
        return payoff

    # Range de preços no vencimento
    S_range = np.linspace(0, 2*K, 1000)
    payoff = option_payoff(S_range, K, premium, option_type)

    # Criar o gráfico
    fig = go.Figure()

    # Lucro e prejuízo
    profit = np.where(payoff >= 0, payoff, np.nan)
    loss = np.where(payoff < 0, payoff, np.nan)

    fig.add_trace(go.Scatter(x=S_range, y=profit, mode='lines', name='Lucro', fill='tozeroy', fillcolor='rgba(0, 255, 0, 0.3)'))
    fig.add_trace(go.Scatter(x=S_range, y=loss, mode='lines', name='Prejuízo', fill='tozeroy', fillcolor='rgba(255, 0, 0, 0.3)'))

    # Adicionar linha vertical no preço de exercício
    fig.update_layout(
        shapes=[
            dict(
                type="line",
                x0=K,
                y0=min(payoff),
                x1=K,
                y1=max(payoff),
                line=dict(color="gray", dash="dash"),
            )
        ]
    )

    # Adicionar anotação
    fig.add_annotation(
        x=K,
        y=0,
        xref="x",
        yref="y",
        text="Break-Even",
        showarrow=True,
        arrowhead=7,
        ax=0,
        ay=-40
    )

    fig.update_layout(title='Lucro/Prejuízo da Opção', xaxis_title='Preço do Ativo no Vencimento', yaxis_title='Lucro/Prejuízo')
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Gráfico mostrando o lucro ou prejuízo de uma opção conforme o preço do ativo no vencimento.")

# Seção: Black-Scholes
elif page == "Black-Scholes":
    st.title("Visualização Interativa da Fórmula de Black-Scholes")

    st.write("""
    A **equação de Black-Scholes** é um modelo matemático usado para determinar o preço teórico de opções europeias. Este modelo revolucionou a forma como as opções são precificadas, levando em consideração fatores como volatilidade, tempo até o vencimento e taxa de juros livre de risco.
    """)

    st.subheader("Fórmula de Black-Scholes")
    st.write("""
    **Para uma opção de Call:**
    """)
    st.latex(r"""
    C = S \cdot N(d_1) - K e^{-rT} \cdot N(d_2)
    """)

    st.write("""
    **Para uma opção de Put:**
    """)
    st.latex(r"""
    P = K e^{-rT} \cdot N(-d_2) - S \cdot N(-d_1)
    """)

    st.write("""
    **Onde:**
    """)
    st.latex(r"""
    d_1 = \frac{\ln\left(\dfrac{S}{K}\right) + \left(r + \dfrac{\sigma^2}{2}\right) T}{\sigma \sqrt{T}}
    """)
    st.latex(r"""
    d_2 = d_1 - \sigma \sqrt{T}
    """)

    st.write("""
    - $S$: Preço atual do ativo
    - $K$: Preço de exercício da opção
    - $T$: Tempo até o vencimento (em anos)
    - $r$: Taxa de juros livre de risco
    - $\sigma$: Volatilidade do ativo
    - $N(d)$: Função de distribuição acumulada da distribuição normal padrão
    """)

    st.subheader("Cálculos Intermediários")

    # Parâmetros
    col1, col2 = st.columns(2)
    with col1:
        S = st.number_input("Preço do Ativo (S)", 50.0, 150.0, 100.0, 1.0)
        K = st.number_input("Preço de Exercício (K)", 50.0, 150.0, 100.0, 1.0)
        T = st.number_input("Tempo até Vencimento (T) em anos", 0.1, 2.0, 1.0, 0.1)
    with col2:
        r = st.number_input("Taxa de Juros Livre de Risco (r)", 0.0, 0.1, 0.05, 0.01)
        sigma = st.number_input("Volatilidade (σ)", 0.01, 0.5, 0.2, 0.01)
        option_type = st.selectbox("Tipo de Opção", ["Call", "Put"])

    # Cálculo dos parâmetros d1 e d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = calculate_option_price(S, K, T, r, sigma, option_type)

    st.latex(r"""
    \begin{aligned}
    d_1 &= \frac{\ln\left(\dfrac{S}{K}\right) + \left(r + \dfrac{\sigma^2}{2}\right) T}{\sigma \sqrt{T}} \\
        &= \frac{\ln\left(\dfrac{{%0.2f}}{{%0.2f}}\right) + \left(%0.2f + \dfrac{%0.2f^2}{2}\right) \times %0.2f}{%0.2f \sqrt{%0.2f}} \\
        &= %0.4f
    \end{aligned}
    """ % (S, K, r, sigma, T, sigma, T, d1))

    st.latex(r"""
    \begin{aligned}
    d_2 &= d_1 - \sigma \sqrt{T} \\
        &= %0.4f - %0.2f \sqrt{%0.2f} \\
        &= %0.4f
    \end{aligned}
    """ % (d1, sigma, T, d2))

    if option_type == "Call":
        # Fórmula do preço da opção Call com quebras de linha
        st.latex(r"""
        \begin{aligned}
        C &= S \cdot N(d_1) - K e^{-r T} \cdot N(d_2) \\
          &= %0.2f \times N(%0.4f) - %0.2f \times e^{-%0.2f \times %0.2f} \times N(%0.4f) \\
          &= %0.2f
        \end{aligned}
        """ % (S, d1, K, r, T, d2, price))
    else:
        # Fórmula do preço da opção Put com quebras de linha
        st.latex(r"""
        \begin{aligned}
        P &= K e^{-r T} \cdot N(-d_2) - S \cdot N(-d_1) \\
          &= %0.2f \times e^{-%0.2f \times %0.2f} \times N(-%0.4f) - %0.2f \times N(-%0.4f) \\
          &= %0.2f
        \end{aligned}
        """ % (K, r, T, d2, S, d1, price))

    st.metric("Preço da Opção", f"{price:.2f}")

# Seção: Gregas
elif page == "Gregas":
    st.title("Visualização das Gregas")

    st.write("""
    As **Gregas** são medidas de sensibilidade que indicam como o preço de uma opção responde a mudanças em diferentes fatores de risco. Elas são essenciais para a gestão de risco e estratégias de hedge em opções.
    """)

    st.subheader("Principais Gregas")
    st.write("""
    - **Delta (Δ):** Sensibilidade do preço da opção em relação ao preço do ativo subjacente.
    - **Gamma (Γ):** Taxa de variação do Delta em relação ao preço do ativo.
    - **Theta (Θ):** Sensibilidade do preço da opção em relação ao tempo até o vencimento.
    - **Vega (ν):** Sensibilidade do preço da opção em relação à volatilidade do ativo.
    - **Rho (ρ):** Sensibilidade do preço da opção em relação à taxa de juros livre de risco.
    """)

    # Parâmetros
    col1, col2 = st.columns(2)
    with col1:
        S = st.number_input("Preço do Ativo (S)", 50.0, 150.0, 100.0, 1.0)
        K = st.number_input("Preço de Exercício (K)", 50.0, 150.0, 100.0, 1.0)
        T = st.number_input("Tempo até Vencimento (T) em anos", 0.1, 2.0, 1.0, 0.1)
    with col2:
        r = st.number_input("Taxa de Juros Livre de Risco (r)", 0.0, 0.1, 0.05, 0.01)
        sigma = st.number_input("Volatilidade (σ)", 0.01, 0.5, 0.2, 0.01)
        option_type = st.selectbox("Tipo de Opção", ["Call", "Put"])

    # Seleção de uma única Grega
    greek = st.selectbox("Selecione a Grega para visualizar", ["Delta", "Gamma", "Theta", "Vega", "Rho"])

    # Função para plotar a Grega selecionada
    def plot_single_greek(ax, S_range, K, T, r, sigma, option_type, greek):
        values = []
        for S_val in S_range:
            if greek == "Delta":
                value = calculate_delta(S_val, K, T, r, sigma, option_type)
            elif greek == "Gamma":
                value = calculate_gamma(S_val, K, T, r, sigma)
            elif greek == "Theta":
                value = calculate_theta(S_val, K, T, r, sigma, option_type)
            elif greek == "Vega":
                value = calculate_vega(S_val, K, T, r, sigma)
            elif greek == "Rho":
                value = calculate_rho(S_val, K, T, r, sigma, option_type)
            values.append(value)
        ax.plot(S_range, values, label=greek)
        ax.set_title(f"{greek} vs. Preço do Ativo")
        ax.set_xlabel("Preço do Ativo")
        ax.set_ylabel(f"Valor de {greek}")
        ax.legend()
        ax.grid(True)

    S_range = np.linspace(0.5*K, 1.5*K, 100)
    create_responsive_plot(plot_single_greek, S_range=S_range, K=K, T=T, r=r, sigma=sigma, option_type=option_type, greek=greek)
    st.caption(f"Gráfico mostrando a {greek} em função do preço do ativo.")

# Seção: Simulador Avançado
elif page == "Simulador Avançado":
    st.title("Simulador Avançado com Múltiplos Eixos")

    st.write("""
    Este simulador permite uma análise aprofundada das opções, visualizando simultaneamente o preço da opção e uma ou mais **Gregas**. Isso facilita a compreensão de como diferentes fatores de risco interagem para influenciar o valor das opções.
    """)

    st.subheader("Funcionalidades")
    st.write("""
    - **Múltiplos Eixos:** Visualize o preço da opção e uma Grega selecionada em um único gráfico com múltiplos eixos.
    - **Interatividade:** Ajuste os parâmetros da opção e observe como tanto o preço quanto as Gregas respondem em tempo real.
    - **Comparação de Gregas:** Compare diferentes Gregas para entender suas inter-relações e impactos no preço da opção.
    """)

    # Parâmetros
    col1, col2 = st.columns(2)
    with col1:
        S = st.slider("Preço do Ativo (S)", 50.0, 150.0, 100.0, 1.0)
        K = st.slider("Preço de Exercício (K)", 50.0, 150.0, 100.0, 1.0)
        T = st.slider("Tempo até Vencimento (T) em anos", 0.1, 2.0, 1.0, 0.1)
    with col2:
        r = st.slider("Taxa de Juros Livre de Risco (r)", 0.0, 0.1, 0.05, 0.01)
        sigma = st.slider("Volatilidade (σ)", 0.1, 0.5, 0.2, 0.01)
        option_type = st.selectbox("Tipo de Opção", ["Call", "Put"])

    # Seleção da Grega
    greek = st.selectbox("Selecione a Grega para visualizar", ["Delta", "Gamma", "Theta", "Vega", "Rho"])

    # Criação do gráfico com múltiplos eixos
    def plot_greek_and_price(ax, S_range, K, T, r, sigma, option_type, greek):
        # Cálculo do preço
        prices = [calculate_option_price(S_val, K, T, r, sigma, option_type) for S_val in S_range]
        # Cálculo da Grega
        if greek == "Delta":
            values = [calculate_delta(S_val, K, T, r, sigma, option_type) for S_val in S_range]
        elif greek == "Gamma":
            values = [calculate_gamma(S_val, K, T, r, sigma) for S_val in S_range]
        elif greek == "Theta":
            values = [calculate_theta(S_val, K, T, r, sigma, option_type) for S_val in S_range]
        elif greek == "Vega":
            values = [calculate_vega(S_val, K, T, r, sigma) for S_val in S_range]
        elif greek == "Rho":
            values = [calculate_rho(S_val, K, T, r, sigma, option_type) for S_val in S_range]

        color_price = 'tab:blue'
        color_greek = 'tab:red'

        ax.plot(S_range, prices, color=color_price, label='Preço da Opção')
        ax.set_xlabel("Preço do Ativo")
        ax.set_ylabel("Preço da Opção", color=color_price)
        ax.tick_params(axis='y', labelcolor=color_price)

        ax2 = ax.twinx()
        ax2.plot(S_range, values, color=color_greek, label=greek)
        ax2.set_ylabel(f"Valor de {greek}", color=color_greek)
        ax2.tick_params(axis='y', labelcolor=color_greek)

        fig.tight_layout()
        ax.grid(True)

    S_range = np.linspace(0.5*K, 1.5*K, 100)
    fig, ax = plt.subplots()
    plot_greek_and_price(ax, S_range, K, T, r, sigma, option_type, greek)
    st.pyplot(fig)
    st.caption(f"Gráfico mostrando o preço da opção e a {greek} em função do preço do ativo.")

# Seção: Compradores vs. Vendedores
elif page == "Compradores vs. Vendedores":
    st.title("Simulador de Preços com Compradores e Vendedores")

    st.write("""
    Este simulador demonstra como a dinâmica entre **compradores** e **vendedores** pode afetar o preço de um ativo ao longo do tempo. A interação entre a força dos compradores e vendedores cria flutuações no preço, refletindo o equilíbrio entre oferta e demanda no mercado.
    """)

    st.subheader("Como Funciona")
    st.write("""
    - **Força dos Compradores/Vendedores:** Controle deslizante que ajusta a força relativa dos compradores e vendedores.
    - **Rastro do Preço:** O gráfico exibe o movimento do preço do ativo ao longo do tempo, deixando um rastro que mostra como as forças aplicadas influenciam o preço.
    """)

    st.subheader("Simulação Interativa")
    st.write("""
    Ajuste a força dos compradores e vendedores para ver como isso impacta o preço do ativo em tempo real.
    """)

    if 'forca' not in st.session_state:
        st.session_state['forca'] = 0.0

    forca = st.sidebar.slider("Força dos Compradores/Vendedores (-1 a 1)", min_value=-1.0, max_value=1.0, value=st.session_state['forca'], step=0.1)
    st.session_state['forca'] = forca

    price_chart = st.empty()

    preco_inicial = 100
    precos = [preco_inicial]
    forcas = [forca]
    t = [0]

    run_simulation = st.button("Iniciar Simulação")

    if run_simulation:
        for i in range(1, 200):
            forca = st.session_state['forca']
            forcas.append(forca)
            t.append(i)

            delta_preco = np.random.normal(loc=forca, scale=1)
            novo_preco = precos[-1] + delta_preco
            precos.append(novo_preco)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=t, y=precos, mode='lines', name='Preço', yaxis='y1'))
            fig.add_trace(go.Scatter(x=t, y=forcas, mode='lines', name='Força', yaxis='y2'))

            fig.update_layout(
                title='Evolução do Preço do Ativo e Força dos Agentes',
                xaxis=dict(title='Tempo'),
                yaxis=dict(title='Preço', side='left'),
                yaxis2=dict(title='Força', overlaying='y', side='right'),
                showlegend=True
            )

            price_chart.plotly_chart(fig, use_container_width=True)

            time.sleep(0.1)

        st.success("Simulação concluída.")

    st.subheader("Interpretação dos Resultados")
    st.write("""
    - **Força Positiva:** Maior força dos compradores leva a um aumento no preço.
    - **Força Negativa:** Maior força dos vendedores leva a uma diminuição no preço.
    - **Equilíbrio:** Força equilibrada mantém o preço estável.
    """)

# Rodapé
st.sidebar.markdown("---")
st.sidebar.info("Desenvolvido por Etore-BeS")