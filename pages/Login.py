"""
pages/Login.py
Tela de autenticação do EduTrack AI — Login e Cadastro.
"""

import streamlit as st
from utils.api import login, signup, request_password_reset

st.set_page_config(page_title="EduTrack AI — Login", page_icon="🎓", layout="centered")

# ── CSS customizado ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  section[data-testid="stMain"] > div {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
    padding: 2rem;
  }

  .login-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    max-width: 460px;
    margin: 3rem auto 0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  }

  .brand-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
  }

  .brand-sub {
    text-align: center;
    color: rgba(255,255,255,0.5);
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
  }

  div[data-testid="stTabs"] button {
    font-weight: 600;
    font-size: 0.95rem;
  }

  .stTextInput input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: white !important;
    border-radius: 10px !important;
  }

  .stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #7c3aed, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: opacity 0.2s ease;
  }

  .stButton > button:hover {
    opacity: 0.88;
  }
</style>
""", unsafe_allow_html=True)

# ── Guard: já logado → redirecionar ─────────────────────────────────────────
if st.session_state.get("token"):
    st.switch_page("App.py")

# ── Layout ───────────────────────────────────────────────────────────────────
st.markdown('<div class="login-card">', unsafe_allow_html=True)
st.markdown('<div class="brand-title">🎓 EduTrack AI</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-sub">Seu assistente acadêmico inteligente</div>', unsafe_allow_html=True)

tab_login, tab_signup, tab_reset = st.tabs(["Entrar", "Criar conta", "Recuperar senha"])

# ── Tab: Login ───────────────────────────────────────────────────────────────
with tab_login:
    with st.form("form_login", clear_on_submit=False):
        email = st.text_input("E-mail", placeholder="seu@email.com", key="login_email")
        password = st.text_input("Senha", type="password", placeholder="••••••••", key="login_pass")
        submitted = st.form_submit_button("Entrar →")

    if submitted:
        if not email or not password:
            st.warning("Preencha e-mail e senha.")
        else:
            with st.spinner("Autenticando..."):
                result = login(email, password)
            if result:
                st.session_state["token"]   = result.get("authToken")
                st.session_state["user_id"] = result.get("user_id")
                st.success("Login realizado! Redirecionando...")
                st.switch_page("App.py")

# ── Tab: Cadastro ────────────────────────────────────────────────────────────
with tab_signup:
    with st.form("form_signup", clear_on_submit=True):
        nome    = st.text_input("Nome completo", placeholder="Ex: Maria Silva", key="signup_name")
        email_s = st.text_input("E-mail", placeholder="seu@email.com", key="signup_email")
        pass_s  = st.text_input("Senha", type="password", placeholder="Mínimo 6 caracteres", key="signup_pass")
        pass_c  = st.text_input("Confirmar senha", type="password", placeholder="Repita a senha", key="signup_confirm")
        submitted_s = st.form_submit_button("Criar minha conta →")

    if submitted_s:
        if not nome or not email_s or not pass_s:
            st.warning("Preencha todos os campos.")
        elif pass_s != pass_c:
            st.error("As senhas não coincidem.")
        elif len(pass_s) < 6:
            st.error("A senha deve ter pelo menos 6 caracteres.")
        else:
            with st.spinner("Criando conta..."):
                result = signup(nome, email_s, pass_s)
            if result:
                st.session_state["token"]   = result.get("authToken")
                st.session_state["user_id"] = result.get("user_id")
                st.success("Conta criada! Redirecionando...")
                st.switch_page("App.py")

# ── Tab: Recuperar senha ─────────────────────────────────────────────────────
with tab_reset:
    with st.form("form_reset", clear_on_submit=True):
        email_r    = st.text_input("E-mail cadastrado", placeholder="seu@email.com", key="reset_email")
        submitted_r = st.form_submit_button("Enviar link de recuperação →")

    if submitted_r:
        if not email_r:
            st.warning("Informe seu e-mail.")
        else:
            with st.spinner("Enviando..."):
                result = request_password_reset(email_r)
            if result is not None:
                st.success("Link enviado! Verifique sua caixa de entrada.")

st.markdown('</div>', unsafe_allow_html=True)
