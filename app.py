import streamlit as st
import pandas as pd
import urllib.parse
import os
import base64
import streamlit.components.v1 as components

# 1. Configuração da página
st.set_page_config(page_title="J.J Collection", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# A MÁGICA CONTRA O GOOGLE TRADUTOR
# Muda a raiz do site para Português (pt-BR) e desativa a tradução
# ==========================================
components.html(
    """
    <script>
        window.parent.document.documentElement.lang = 'pt-BR';
        window.parent.document.documentElement.setAttribute('translate', 'no');
    </script>
    """,
    width=0, height=0
)

# 2. CSS de Luxo 
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Great+Vibes&family=Montserrat:wght@300;400;500&display=swap');
body { background-color: #050505; color: #e0e0e0; font-family: 'Montserrat', sans-serif; }
.stApp { background-color: #050505; }
h1, h2, h3 { color: #d4af37 !important; font-family: 'Cinzel', serif !important; font-weight: 400; }
.stSidebar { background-color: #0a0a0a !important; border-right: 1px solid rgba(212, 175, 55, 0.2); }
.stSidebar h1, .stSidebar h2, .stSidebar p, .stSidebar label { color: #d4af37 !important; font-family: 'Montserrat', sans-serif; }
.markdown-text-container p, .stMarkdown p { font-family: 'Montserrat', sans-serif !important; color: #cccccc !important; font-size: 14px; }
.stLinkButton a { display: block; text-align: center; background-color: transparent; color: #d4af37; border: 1px solid #d4af37; border-radius: 0px; font-family: 'Cinzel', serif; letter-spacing: 1px; width: 100%; padding: 0.5rem 1rem; text-decoration: none; transition: all 0.4s ease;}
.stLinkButton a:hover { background-color: #d4af37; color: #000000; box-shadow: 0 0 10px rgba(212, 175, 55, 0.4);}
[data-testid="stHeader"] {background-color: transparent;}
[data-testid="stToolbar"] {right: 2rem; background-color: transparent;}

/* ========================================= */
/* BOTÃO DO MENU/FILTRO SUPER DESTACADO      */
/* ========================================= */
[data-testid="collapsedControl"] {
    background-color: #050505 !important;
    border: 2px solid #d4af37 !important; /* Borda dourada mais grossa */
    border-radius: 8px !important; /* Cantos arredondados */
    margin: 15px !important;
    padding: 5px !important;
    box-shadow: 0px 0px 15px rgba(212, 175, 55, 0.4) !important; /* Efeito de brilho dourado */
    transition: all 0.3s ease !important;
    z-index: 999999 !important; /* Garante que ele fique sempre na frente */
}

/* Efeito quando o cliente passa o dedo ou o mouse por cima */
[data-testid="collapsedControl"]:hover {
    box-shadow: 0px 0px 25px rgba(212, 175, 55, 0.8) !important; 
    background-color: #1a1a1a !important;
}

/* Deixa o ícone (a setinha) maior e dourado */
[data-testid="collapsedControl"] svg {
    fill: #d4af37 !important;
    color: #d4af37 !important;
    width: 35px !important; 
    height: 35px !important;
}
/* ========================================= */

/* Classes inteligentes para não cortar no celular */
.titulo-principal {
    font-family: 'Cinzel', serif; 
    color: #d4af37; 
    font-size: clamp(16px, 4vw, 26px);
    letter-spacing: 4px; 
    line-height: 1.4;
}
.palavra-destaque {
    font-family: 'Great Vibes', cursive; 
    font-size: clamp(40px, 12vw, 70px);
    color: #e8c678; 
    letter-spacing: 2px; 
    text-transform: lowercase; 
    margin-top: -10px; 
    display: inline-block;
    padding: 5px 25px; 
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# GESTÃO DE PASTAS E ARQUIVOS
# ==========================================
ARQUIVO_DADOS = "estoque.csv"
PASTA_MIDIA = "midia_pecas"

# Cria a pasta de fotos se ela não existir
os.makedirs(PASTA_MIDIA, exist_ok=True)

def inicializar_banco():
    if not os.path.exists(ARQUIVO_DADOS):
        dados_iniciais = [
            {"id": 1, "categoria": "Pulseiras", "nome": "Pulseira Nossa Senhora", "descricao": "Banhada a ouro 18k com pingente e cruz.", "estoque": 1, "preco": "R$ 70,00", "imagem": f"{PASTA_MIDIA}/pulseira1.jpg"},
            {"id": 2, "categoria": "Pulseiras", "nome": "Pulseira Zircônias Brilho", "descricao": "Detalhes em zircônias de alto brilho, acabamento impecável.", "estoque": 1, "preco": "R$ 80,00", "imagem": f"{PASTA_MIDIA}/pulseira2.jpg"},
            {"id": 3, "categoria": "Pulseiras", "nome": "Pulseira Flor Ródio", "descricao": "Flor delicada com acabamento impecável e zircônias.", "estoque": 1, "preco": "R$ 80,00", "imagem": f"{PASTA_MIDIA}/pulseira3.jpg"},
            {"id": 4, "categoria": "Pulseiras", "nome": "Pulseira Cruzada Ródio", "descricao": "Proteção contra oxidação e brilho espelhado.", "estoque": 1, "preco": "R$ 45,00", "imagem": f"{PASTA_MIDIA}/pulseira4.jpg"}
        ]
        df = pd.DataFrame(dados_iniciais)
        df.to_csv(ARQUIVO_DADOS, index=False)

def carregar_dados():
    return pd.DataFrame(pd.read_csv(ARQUIVO_DADOS))

def salvar_dados(df):
    df.to_csv(ARQUIVO_DADOS, index=False)

inicializar_banco()
df_estoque = carregar_dados()

# 4. Logo Lateral
logo_html = """
<div style="text-align: center; margin-bottom: 20px; margin-top: -20px;">
<div style="display: inline-block; border-radius: 50%; width: 140px; height: 140px; background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); border: 2px solid rgba(212, 175, 55, 0.8); display: flex; justify-content: center; align-items: center; flex-direction: column; color: #d4af37; font-family: 'Cinzel', serif;">
<div style="font-size: 50px; font-weight: 700; margin-bottom: -15px;">J.J</div>
<div style="font-size: 10px; letter-spacing: 3px;">COLLECTION</div>
</div>
</div>
"""
st.sidebar.markdown(logo_html, unsafe_allow_html=True)
st.sidebar.markdown("---")

# 5. LÓGICA DO LINK SECRETO
modo_admin = st.query_params.get("admin") == "dududev.confg"

# ==========================================
# TELA 2: O PAINEL ADMINISTRATIVO (Para Donos)
# ==========================================
if modo_admin:
    st.title("⚙️ Gestão de Estoque J.J")
    st.info("Você está acessando pelo link administrativo oculto.")
    
    senha = st.text_input("Digite a senha de acesso:", type="password")
    
    # ATENÇÃO: AQUI ESTÁ USANDO O ST.SECRETS. GARANTA QUE A SENHA ESTÁ NO PAINEL DO STREAMLIT!
    if senha == st.secrets["senha_admin"]: 
        st.success("Acesso Liberado!")
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("➕ Adicionar Nova Peça")
            novo_nome = st.text_input("Nome da Joia")
            nova_categoria = st.selectbox("Categoria", ["Pulseiras", "Anéis", "Colares", "Brincos", "Conjuntos"])
            novo_preco = st.text_input("Preço (ex: R$ 50,00)")
            nova_descricao = st.text_area("Descrição do Produto")
            novo_estoque = st.number_input("Quantidade em Estoque", min_value=1, step=1)
            foto_upload = st.file_uploader("Envie a foto do produto (JPG ou PNG)", type=["jpg", "jpeg", "png"])
            
            if st.button("Salvar Produto no Estoque"):
                if novo_nome and novo_preco and foto_upload:
                    # Salva a imagem dentro da nova pasta
                    nome_arquivo_foto = foto_upload.name
                    caminho_salvar = os.path.join(PASTA_MIDIA, nome_arquivo_foto)
                    
                    with open(caminho_salvar, "wb") as f:
                        f.write(foto_upload.getbuffer())
                    
                    novo_id = df_estoque['id'].max() + 1 if not df_estoque.empty else 1
                    novo_produto = pd.DataFrame([{
                        "id": novo_id, "categoria": nova_categoria, "nome": novo_nome,
                        "descricao": nova_descricao, "estoque": novo_estoque, "preco": novo_preco,
                        "imagem": caminho_salvar # Guarda o caminho da pasta no CSV
                    }])
                    df_atualizado = pd.concat([df_estoque, novo_produto], ignore_index=True)
                    salvar_dados(df_atualizado)
                    st.success(f"{novo_nome} adicionado com sucesso na pasta {PASTA_MIDIA}!")
                    st.rerun()
                else:
                    st.error("Por favor, preencha o Nome, Preço e envie uma Foto.")
                    
        with col2:
            st.subheader("📦 Estoque Atual")
            st.dataframe(df_estoque[['id', 'categoria', 'nome', 'preco', 'estoque']], use_container_width=True)
            
            st.markdown("---")
            
            st.subheader("✏️ Editar Preço ou Estoque")
            id_para_editar = st.number_input("Digite o ID do produto para editar:", min_value=1, step=1, key="edit_id")
            
            if id_para_editar in df_estoque['id'].values:
                produto_atual = df_estoque[df_estoque['id'] == id_para_editar].iloc[0]
                
                with st.form("form_edicao"):
                    st.write(f"Editando: **{produto_atual['nome']}**")
                    novo_preco_edit = st.text_input("Novo Preço", value=produto_atual['preco'])
                    novo_estoque_edit = st.number_input("Novo Estoque", min_value=0, step=1, value=int(produto_atual['estoque']))
                    
                    if st.form_submit_button("Atualizar Produto"):
                        df_estoque.loc[df_estoque['id'] == id_para_editar, 'preco'] = novo_preco_edit
                        df_estoque.loc[df_estoque['id'] == id_para_editar, 'estoque'] = novo_estoque_edit
                        salvar_dados(df_estoque)
                        st.success("Atualizado com sucesso!")
                        st.rerun()
            elif id_para_editar > 0 and not df_estoque.empty:
                st.warning("ID não encontrado no estoque.")
            
            st.markdown("---")
            
            st.subheader("🗑️ Excluir Peça")
            id_para_excluir = st.number_input("Digite o ID do produto para excluir:", min_value=1, step=1, key="del_id")
            
            if st.button("Excluir Produto"):
                if id_para_excluir in df_estoque['id'].values:
                    # Descobre o caminho da imagem antes de apagar do banco
                    caminho_imagem = df_estoque[df_estoque['id'] == id_para_excluir]['imagem'].iloc[0]
                    
                    # 1. Apaga do Banco de Dados (CSV)
                    df_estoque = df_estoque[df_estoque['id'] != id_para_excluir]
                    salvar_dados(df_estoque) 
                    
                    # 2. Apaga o arquivo físico da pasta (se ele existir)
                    if pd.notna(caminho_imagem) and os.path.exists(caminho_imagem):
                        os.remove(caminho_imagem)
                        st.success("Produto e foto excluídos com sucesso do servidor!")
                    else:
                        st.success("Produto excluído! (Nenhuma foto física encontrada).")
                        
                    st.rerun() 
                else:
                    st.error("ID não encontrado.")
    elif senha != "":
        st.error("Senha Incorreta.")

# ==========================================
# TELA 1: A VITRINE (Para os Clientes)
# ==========================================
else:
    st.sidebar.markdown("<p style='text-align: center; color: #d4af37;'>Filtre por categoria</p>", unsafe_allow_html=True)
    categorias_disponiveis = ["Todas as Peças"] + list(df_estoque["categoria"].unique())
    escolha = st.sidebar.radio("", categorias_disponiveis)

    if escolha != "Todas as Peças":
        df_filtrado = df_estoque[df_estoque["categoria"] == escolha]
    else:
        df_filtrado = df_estoque

    # ==========================================
    # CSS PARA DIMINUIR E CENTRALIZAR AS FOTOS
    # ==========================================
    st.markdown("""
    <style>
    /* Garante que a caixa da imagem ocupe o espaço inteiro para poder centralizar */
    [data-testid="stImage"] {
        width: 100%;
        display: flex !important;
        justify-content: center !important;
    }
    /* Diminui e empurra a foto exatamente para o meio */
    [data-testid="stImage"] img {
        max-width: 75% !important; /* Aqui você controla o tamanho */
        margin: 0 auto !important; /* Essa é a mágica que centraliza a foto */
        display: block !important;
        border-radius: 8px; 
    }
    </style>
    """, unsafe_allow_html=True)
    # ==========================================

    header_principal = """
    <div style="text-align: center; margin-bottom: 40px; margin-top: 10px;">
        <div class="titulo-principal">
            OS <span style="font-weight: 700;">DETALHES</span> FAZEM TODA A <br>
            <span class="palavra-destaque">diferença.</span>
        </div>
    </div>
    """
    st.markdown(header_principal, unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; margin-bottom: 30px; letter-spacing: 2px;'>{escolha.upper()}</h3>", unsafe_allow_html=True)

    NUMERO_WHATSAPP = "5511976984671"

    colunas = st.columns(3)
    for i, (index, row) in enumerate(df_filtrado.iterrows()):
        with colunas[i % 3]:
            st.markdown("<div style='padding: 10px;'>", unsafe_allow_html=True)
            try:
                # A imagem agora vai respeitar os 75% do CSS acima
                st.image(row["imagem"], use_container_width=True)
            except:
                st.error("Foto não encontrada.")

            st.markdown(f"<h3 style='font-size: 18px; margin-top: 15px; text-align: center;'>{row['nome']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-style: italic; font-size: 13px;'>{row['descricao']}</p>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center;'><span style='color: #d4af37; font-size: 18px; font-weight: 500;'>{row['preco']}</span><br><span style='color: #888; font-size: 12px;'>Estoque: {row['estoque']} un.</span></div><br>", unsafe_allow_html=True)
            
            texto = urllib.parse.quote(f"Olá, J.J Collection! Tenho interesse na peça: {row['nome']} ({row['preco']}). Ainda está disponível?")
            st.link_button("Comprar pelo WhatsApp 📱", f"https://wa.me/{NUMERO_WHATSAPP}?text={texto}", use_container_width=True)
            st.markdown("</div><hr style='border-top: 1px solid rgba(212, 175, 55, 0.2);'>", unsafe_allow_html=True)