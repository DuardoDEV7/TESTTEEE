import streamlit as st
import pandas as pd
import urllib.parse
import os

# 1. Configuração da página
st.set_page_config(page_title="J.J Collection", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

# 2. CSS de Luxo (Oculto na Área Admin para não atrapalhar os formulários)
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
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Lógica do Banco de Dados (CSV)
ARQUIVO_DADOS = "estoque.csv"

def inicializar_banco():
    """Cria o arquivo CSV inicial se ele não existir na pasta."""
    if not os.path.exists(ARQUIVO_DADOS):
        dados_iniciais = [
            {"id": 1, "categoria": "Pulseiras", "nome": "Pulseira Nossa Senhora", "descricao": "Banhada a ouro 18k com pingente e cruz.", "estoque": 1, "preco": "R$ 70,00", "imagem": "pulseira1.jpg"},
            {"id": 2, "categoria": "Pulseiras", "nome": "Pulseira Zircônias Brilho", "descricao": "Detalhes em zircônias de alto brilho, acabamento impecável.", "estoque": 1, "preco": "R$ 80,00", "imagem": "pulseira2.jpg"},
            {"id": 3, "categoria": "Pulseiras", "nome": "Pulseira Flor Ródio", "descricao": "Flor delicada com acabamento impecável e zircônias.", "estoque": 1, "preco": "R$ 80,00", "imagem": "pulseira3.jpg"},
            {"id": 4, "categoria": "Pulseiras", "nome": "Pulseira Cruzada Ródio", "descricao": "Proteção contra oxidação e brilho espelhado.", "estoque": 1, "preco": "R$ 45,00", "imagem": "pulseira4.jpg"}
        ]
        df = pd.DataFrame(dados_iniciais)
        df.to_csv(ARQUIVO_DADOS, index=False)

def carregar_dados():
    return pd.DataFrame(pd.read_csv(ARQUIVO_DADOS))

def salvar_dados(df):
    df.to_csv(ARQUIVO_DADOS, index=False)

# Inicia o banco de dados
inicializar_banco()
df_estoque = carregar_dados()

# 4. Barra Lateral - Navegação do Sistema
logo_html = """
<div style="text-align: center; margin-bottom: 20px; margin-top: -20px;">
<div style="display: inline-block; border-radius: 50%; width: 140px; height: 140px; background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); border: 2px solid rgba(212, 175, 55, 0.8); display: flex; justify-content: center; align-items: center; flex-direction: column; color: #d4af37; font-family: 'Cinzel', serif;">
<div style="font-size: 50px; font-weight: 700; margin-bottom: -15px;">J.J</div>
<div style="font-size: 10px; letter-spacing: 3px;">COLLECTION</div>
</div>
</div>
"""
st.sidebar.markdown(logo_html, unsafe_allow_html=True)

menu_selecionado = st.sidebar.radio("Navegação do Sistema:", ["💎 Vitrine da Loja", "⚙️ Painel Administrativo"])
st.sidebar.markdown("---")


# ==========================================
# TELA 1: A VITRINE (Para os Clientes)
# ==========================================
if menu_selecionado == "💎 Vitrine da Loja":
    
    # Filtro
    st.sidebar.markdown("<p style='text-align: center; color: #d4af37;'>Filtre por categoria</p>", unsafe_allow_html=True)
    categorias_disponiveis = ["Todas as Peças"] + list(df_estoque["categoria"].unique())
    escolha = st.sidebar.radio("", categorias_disponiveis)

    if escolha != "Todas as Peças":
        df_filtrado = df_estoque[df_estoque["categoria"] == escolha]
    else:
        df_filtrado = df_estoque

    # Cabeçalho
    header_principal = """
    <div style="text-align: center; margin-bottom: 40px; margin-top: 10px;">
    <div style="font-family: 'Cinzel', serif; color: #d4af37; font-size: 26px; letter-spacing: 4px; line-height: 1.4;">
    OS <span style="font-weight: 700;">DETALHES</span> FAZEM TODA A <br>
    <span style="font-family: 'Great Vibes', cursive; font-size: 70px; color: #e8c678; letter-spacing: 2px; text-transform: lowercase; margin-top: -10px; display: inline-block;">diferença.</span>
    </div>
    </div>
    """
    st.markdown(header_principal, unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; margin-bottom: 30px; letter-spacing: 2px;'>{escolha.upper()}</h3>", unsafe_allow_html=True)

    NUMERO_WHATSAPP = "5511999999999"

    # Grid de Produtos
    colunas = st.columns(3)
    # Usamos o 'enumerate' para criar um contador (i) que sempre começa do zero
    for i, (index, row) in enumerate(df_filtrado.iterrows()):
        with colunas[i % 3]:
            st.markdown("<div style='padding: 10px;'>", unsafe_allow_html=True)
            try:
                st.image(row["imagem"], use_container_width=True)
            except:
                st.error("Sem foto")

            st.markdown(f"<h3 style='font-size: 18px; margin-top: 15px; text-align: center;'>{row['nome']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-style: italic; font-size: 13px;'>{row['descricao']}</p>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center;'><span style='color: #d4af37; font-size: 18px; font-weight: 500;'>{row['preco']}</span><br><span style='color: #888; font-size: 12px;'>Estoque: {row['estoque']} un.</span></div><br>", unsafe_allow_html=True)
            
            # Botão Zap
            texto = urllib.parse.quote(f"Olá, J.J Collection! Tenho interesse na peça: {row['nome']} ({row['preco']}).")
            st.link_button("Comprar pelo WhatsApp 📱", f"https://wa.me/{NUMERO_WHATSAPP}?text={texto}", use_container_width=True)
            st.markdown("</div><hr style='border-top: 1px solid rgba(212, 175, 55, 0.2);'>", unsafe_allow_html=True)


# ==========================================
# TELA 2: O PAINEL ADMINISTRATIVO (Para Donos)
# ==========================================
elif menu_selecionado == "⚙️ Painel Administrativo":
    st.title("⚙️ Gestão de Estoque J.J")
    
    # Sistema simples de Senha
    senha = st.text_input("Digite a senha de acesso:", type="password")
    
    if senha == "jj2026": # SENHA DEFINIDA AQUI
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
            
            # Ferramenta para subir foto do PC/Celular
            foto_upload = st.file_uploader("Envie a foto do produto (JPG ou PNG)", type=["jpg", "jpeg", "png"])
            
            if st.button("Salvar Produto no Estoque"):
                if novo_nome and novo_preco and foto_upload:
                    nome_arquivo_foto = foto_upload.name
                    with open(nome_arquivo_foto, "wb") as f:
                        f.write(foto_upload.getbuffer())
                    
                    novo_id = df_estoque['id'].max() + 1 if not df_estoque.empty else 1
                    novo_produto = pd.DataFrame([{
                        "id": novo_id,
                        "categoria": nova_categoria,
                        "nome": novo_nome,
                        "descricao": nova_descricao,
                        "estoque": novo_estoque,
                        "preco": novo_preco,
                        "imagem": nome_arquivo_foto 
                    }])
                    
                    df_atualizado = pd.concat([df_estoque, novo_produto], ignore_index=True)
                    salvar_dados(df_atualizado)
                    
                    st.success(f"{novo_nome} adicionado com sucesso! A vitrine já está atualizada.")
                    st.rerun()
                else:
                    st.error("Por favor, preencha o Nome, Preço e envie uma Foto.")
                    
        with col2:
            st.subheader("📦 Estoque Atual")
            st.dataframe(df_estoque[['id', 'categoria', 'nome', 'preco', 'estoque']], use_container_width=True)
            
            st.markdown("---")
            
            # ---> NOVA FUNÇÃO DE EXCLUIR AQUI <---
            st.subheader("🗑️ Excluir Peça")
            st.write("Olhe o número do **ID** na tabela acima para excluir o produto correto.")
            id_para_excluir = st.number_input("Digite o ID do produto para excluir:", min_value=1, step=1)
            
            if st.button("Excluir Produto"):
                # Verifica se o ID existe no banco de dados
                if id_para_excluir in df_estoque['id'].values:
                    # Filtra o banco de dados mantendo apenas os produtos com ID diferente do digitado
                    df_estoque = df_estoque[df_estoque['id'] != id_para_excluir]
                    salvar_dados(df_estoque) # Salva o CSV atualizado
                    st.success(f"Produto ID {id_para_excluir} excluído com sucesso!")
                    st.rerun() # Atualiza a página
                else:
                    st.error("ID não encontrado no estoque.")
            
    elif senha != "":
        st.error("Senha Incorreta.")