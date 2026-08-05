import streamlit as st
import pandas as pd
import urllib.parse

# 1. Configuração da página
st.set_page_config(
    page_title="J.J Collection - Mostruário", 
    page_icon="💎", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. Injeção de CSS Personalizado
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Great+Vibes&family=Montserrat:wght@300;400;500&display=swap');

body { background-color: #050505; color: #e0e0e0; font-family: 'Montserrat', sans-serif; }
.stApp { background-color: #050505; }
h1, h2, h3 { color: #d4af37 !important; font-family: 'Cinzel', serif !important; font-weight: 400; }
.stSidebar { background-color: #0a0a0a !important; border-right: 1px solid rgba(212, 175, 55, 0.2); }
.stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar p, .stSidebar label { color: #d4af37 !important; font-family: 'Montserrat', sans-serif; }
.markdown-text-container p, .stMarkdown p { font-family: 'Montserrat', sans-serif !important; color: #cccccc !important; font-size: 14px; }
.stButton button { background-color: transparent; color: #d4af37; border: 1px solid #d4af37; border-radius: 0px; font-family: 'Cinzel', serif; letter-spacing: 1px; width: 100%; transition: all 0.4s ease; }
.stButton button:hover { background-color: #d4af37; color: #000000; border: 1px solid #d4af37; box-shadow: 0 0 10px rgba(212, 175, 55, 0.4); }

/* Estilo para o link do WhatsApp se comportar como o botão original */
.stLinkButton a {
    display: block; text-align: center; background-color: transparent; color: #d4af37; 
    border: 1px solid #d4af37; border-radius: 0px; font-family: 'Cinzel', serif; 
    letter-spacing: 1px; width: 100%; padding: 0.5rem 1rem; text-decoration: none; transition: all 0.4s ease;
}
.stLinkButton a:hover {
    background-color: #d4af37; color: #000000; box-shadow: 0 0 10px rgba(212, 175, 55, 0.4);
}

[data-testid="stHeader"] {background-color: transparent;}
[data-testid="stToolbar"] {right: 2rem; background-color: transparent;}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Logo Refinada na Barra Lateral
logo_html = """
<div style="text-align: center; margin-bottom: 20px; margin-top: -20px;">
<div style="display: inline-block; border-radius: 50%; width: 160px; height: 160px; background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); border: 2px solid rgba(212, 175, 55, 0.8); box-shadow: 0 0 20px rgba(212, 175, 55, 0.2), inset 0 0 15px rgba(212, 175, 55, 0.1); display: flex; justify-content: center; align-items: center; flex-direction: column; color: #d4af37; font-family: 'Cinzel', serif;">
<div style="font-size: 60px; font-weight: 700; margin-bottom: -15px; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">J.J</div>
<div style="font-size: 12px; letter-spacing: 4px; font-weight: 400;">COLLECTION</div>
<div style="font-size: 9px; letter-spacing: 2px; color: #a9a9a9; margin-top: 2px;">ACESSÓRIOS</div>
</div>
</div>
<div style="font-family: 'Cinzel', serif; text-align: center; color: #d4af37; font-size: 16px; margin-top: 10px;">
J.J COLLECTION <br> <span style="font-size: 11px; color: #888888; letter-spacing: 2px; font-family: 'Montserrat', sans-serif;">PRATAS & SEMIJOIAS</span>
</div>
<hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(212, 175, 55, 0.5), rgba(0,0,0,0)); margin: 20px 0;">
"""
st.sidebar.markdown(logo_html, unsafe_allow_html=True)


# 4. Banco de Dados da J.J Collection (Apenas as peças disponíveis extraídas do Instagram)
# Troque as URLs pelas suas fotos locais, por exemplo: "imagem": "pulseira_nossa_senhora.jpg"
dados = [
    {
        "id": 1, 
        "categoria": "Pulseiras", 
        "nome": "Pulseira Nossa Senhora", 
        "descricao": "Banhada a ouro 18k com pingente de Nossa Senhora e cruz. Carrega proteção, delicadeza e elegância.", 
        "estoque": 1, 
        "preco": "R$ 70,00", 
        "imagem": "https://via.placeholder.com/400x400/1a1a1a/d4af37?text=Foto+Nossa+Senhora"
    },
    {
        "id": 2, 
        "categoria": "Pulseiras", 
        "nome": "Pulseira Zircônias Brilho", 
        "descricao": "Semijoia banhada a ouro 18K. Detalhes em zircônias de alto brilho, acabamento impecável e design moderno.", 
        "estoque": 1, 
        "preco": "R$ 80,00", 
        "imagem": "https://via.placeholder.com/400x400/1a1a1a/d4af37?text=Foto+Zirconias+Ouro"
    },
    {
        "id": 3, 
        "categoria": "Pulseiras", 
        "nome": "Pulseira Flor Ródio", 
        "descricao": "Semijoia com banho de ródio. Flor delicada com acabamento impecável e zircônias de alto brilho.", 
        "estoque": 1, 
        "preco": "R$ 80,00", 
        "imagem": "https://via.placeholder.com/400x400/1a1a1a/d4af37?text=Foto+Flor+Rodio"
    },
    {
        "id": 4, 
        "categoria": "Pulseiras", 
        "nome": "Pulseira Cruzada Ródio", 
        "descricao": "Semijoia com banho de ródio e acabamento premium. Proteção contra oxidação e brilho espelhado.", 
        "estoque": 1, 
        "preco": "R$ 45,00", 
        "imagem": "https://via.placeholder.com/400x400/1a1a1a/d4af37?text=Foto+Cruzada+Rodio"
    }
]
df_estoque = pd.DataFrame(dados)


# 5. Menu Lateral (Filtro)
st.sidebar.markdown("<p style='text-align: center; color: #d4af37; font-size: 14px; letter-spacing: 1px;'>Navegue pela coleção</p>", unsafe_allow_html=True)
categorias_disponiveis = ["Todas as Peças"] + list(df_estoque["categoria"].unique())
escolha = st.sidebar.radio("", categorias_disponiveis)


# 6. Lógica de Filtragem
if escolha != "Todas as Peças":
    df_filtrado = df_estoque[df_estoque["categoria"] == escolha]
else:
    df_filtrado = df_estoque


# 7. Cabeçalho Principal
header_principal = """
<div style="text-align: center; margin-bottom: 50px; margin-top: 10px;">
<hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(212, 175, 55, 0.7), rgba(0,0,0,0)); margin-bottom: 30px;">
<div style="font-family: 'Cinzel', serif; color: #d4af37; font-size: 26px; letter-spacing: 4px; line-height: 1.4;">
OS <span style="font-weight: 700;">DETALHES</span> FAZEM TODA A <br>
<span style="font-family: 'Great Vibes', cursive; font-size: 70px; color: #e8c678; letter-spacing: 2px; text-transform: lowercase; font-weight: normal; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); display: inline-block; margin-top: -10px;">diferença.</span>
</div>
<hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(212, 175, 55, 0.7), rgba(0,0,0,0)); margin-top: 20px; margin-bottom: 40px;">
</div>
"""
st.markdown(header_principal, unsafe_allow_html=True)

st.markdown(f"<h3 style='text-align: center; margin-bottom: 30px; font-size: 20px; letter-spacing: 2px;'>{escolha.upper()}</h3>", unsafe_allow_html=True)


# 8. Número do WhatsApp da Loja (Substitua pelo número real da loja)
NUMERO_WHATSAPP = "5511933088393"

# 9. Exibição em Grade (Grid)
colunas = st.columns(3)

for index, row in df_filtrado.iterrows():
    with colunas[index % 3]:
        st.markdown("<div style='padding: 10px;'>", unsafe_allow_html=True)
        
        st.image(row["imagem"], use_container_width=True)
        st.markdown(f"<h3 style='font-size: 18px; margin-top: 15px; margin-bottom: 5px; text-align: center;'>{row['nome']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-style: italic; font-size: 13px;'>{row['descricao']}</p>", unsafe_allow_html=True)
        
        info_produto = f"""
<div style='text-align: center; font-family: "Montserrat", sans-serif; margin-bottom: 15px;'>
<span style='color: #d4af37; font-size: 18px; font-weight: 500;'>{row['preco']}</span><br>
<span style='color: #888; font-size: 12px;'>Estoque: {row['estoque']} un.</span>
</div>
"""
        st.markdown(info_produto, unsafe_allow_html=True)
        
        # Botão Inteligente do WhatsApp
        texto_mensagem = f"Olá, J.J Collection! Tenho interesse na peça: {row['nome']} ({row['preco']}). Ainda está disponível?"
        texto_url_segura = urllib.parse.quote(texto_mensagem)
        link_zap = f"https://wa.me/{NUMERO_WHATSAPP}?text={texto_url_segura}"
        
        st.link_button("Comprar pelo WhatsApp 📱", link_zap, use_container_width=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<hr style='border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(212, 175, 55, 0.15), rgba(0,0,0,0));'>", unsafe_allow_html=True)