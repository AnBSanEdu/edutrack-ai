"""
pages/Perfil.py
Tela de perfil do usuário — visualização e edição.
"""

import streamlit as st
from utils.api import get_me, edit_profile, request_password_reset

st.set_page_config(page_title="EduTrack AI — Perfil", page_icon="👤", layout="centered")

# ── Guard ─────────────────────────────────────────────────────────────────────
if not st.session_state.get("token"):
    st.switch_page("pages/Login.py")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .profile-header {
    background: linear-gradient(135deg, #7c3aed22, #3b82f622);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 2rem;
  }

  .avatar-circle {
    width: 80px; height: 80px;
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem;
    margin: 0 auto 1rem;
  }

  .profile-name {
    font-size: 1.4rem;
    font-weight: 700;
    color: white;
  }

  .profile-email {
    color: rgba(255,255,255,0.55);
    font-size: 0.9rem;
  }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 EduTrack AI")
    st.markdown("---")
    st.page_link("App.py",               label="🏠 Dashboard")
    st.page_link("pages/Disciplinas.py",  label="📚 Disciplinas")
    st.page_link("pages/Tarefas.py",      label="📝 Tarefas")
    st.page_link("pages/Perfil.py",       label="👤 Perfil")
    st.markdown("---")
    if st.button("🚪 Sair", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("pages/Login.py")

# ── Carregar dados do usuário ─────────────────────────────────────────────────
@st.cache_data(ttl=60)
def _load_me(token):
    return get_me()


me = _load_me(st.session_state.get("token"))
if not me:
    st.error("Não foi possível carregar seus dados. Tente novamente.")
    st.stop()

nome_atual  = me.get("name", "")
email_atual = me.get("email", "")

# ── Header do perfil ──────────────────────────────────────────────────────────
initial = nome_atual[0].upper() if nome_atual else "?"
st.markdown(f"""
<div class="profile-header">
  <div class="avatar-circle">{initial}</div>
  <div class="profile-name">{nome_atual}</div>
  <div class="profile-email">{email_atual}</div>
</div>
""", unsafe_allow_html=True)

# ── Formulário de edição ──────────────────────────────────────────────────────
st.subheader("✏️ Editar informações")

with st.form("form_perfil"):
    novo_nome  = st.text_input("Nome", value=nome_atual)
    novo_email = st.text_input("E-mail", value=email_atual)
    salvar     = st.form_submit_button("💾 Salvar alterações", use_container_width=True)

if salvar:
    if not novo_nome or not novo_email:
        st.warning("Nome e e-mail são obrigatórios.")
    else:
        with st.spinner("Salvando..."):
            result = edit_profile(novo_nome, novo_email)
        if result is not None:
            st.session_state["user_name"]  = novo_nome
            st.session_state["user_email"] = novo_email
            _load_me.clear()
            st.success("Perfil atualizado com sucesso!")
            st.rerun()

st.markdown("---")

# ── Redefinição de senha ──────────────────────────────────────────────────────
st.subheader("🔒 Segurança")
st.markdown("Clique abaixo para receber um link de redefinição de senha no seu e-mail.")

with st.form("form_reset_senha"):
    enviar_reset = st.form_submit_button("📧 Enviar link de redefinição de senha", use_container_width=True)

if enviar_reset:
    with st.spinner("Enviando e-mail..."):
        result = request_password_reset(email_atual)
    if result is not None:
        st.success(f"Link enviado para **{email_atual}**. Verifique sua caixa de entrada.")
