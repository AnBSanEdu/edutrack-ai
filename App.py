"""
App.py — EduTrack AI
Dashboard principal com dados reais agregados do Xano.
"""

import streamlit as st
from datetime import datetime
from utils.api import get_me, get_dashboard_summary

# ── Configuração da página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="EduTrack AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS Global ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0c29 0%, #302b63 100%);
  }
  section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }

  .metric-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 18px;
    padding: 1.4rem 1.6rem;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
  }
  .metric-icon  { font-size: 1.8rem; margin-bottom: 0.35rem; }
  .metric-value {
    font-size: 2.6rem; font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }
  .metric-value.red   { background: linear-gradient(90deg,#f87171,#fb923c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .metric-value.green { background: linear-gradient(90deg,#4ade80,#34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .metric-label { font-size: 0.82rem; color: rgba(255,255,255,0.5); margin-top: 0.2rem; }

  .welcome-banner {
    background: linear-gradient(135deg, #7c3aed18, #3b82f618);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 18px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.75rem;
  }
  .welcome-title { font-size: 1.5rem; font-weight: 800; color: white; }
  .welcome-sub   { color: rgba(255,255,255,0.55); font-size: 0.9rem; margin-top: 0.3rem; }

  .progress-bar-bg {
    background: rgba(255,255,255,0.08);
    border-radius: 99px;
    height: 10px;
    margin-top: 0.5rem;
    overflow: hidden;
  }
  .progress-bar-fill {
    background: linear-gradient(90deg, #7c3aed, #3b82f6);
    height: 100%;
    border-radius: 99px;
    transition: width 0.6s ease;
  }

  .upcoming-card {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #7c3aed;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    transition: border-color 0.2s;
  }
  .upcoming-card:hover { border-left-color: #60a5fa; }
  .upcoming-card.overdue { border-left-color: #ef4444; }
  .upcoming-title { font-weight: 600; font-size: 0.95rem; color: white; }
  .upcoming-meta  { font-size: 0.78rem; color: rgba(255,255,255,0.45); margin-top: 0.15rem; }

  .empty-state {
    text-align: center;
    padding: 2.5rem;
    color: rgba(255,255,255,0.35);
    font-size: 0.95rem;
  }
</style>
""", unsafe_allow_html=True)

# ── Proteção de rota ──────────────────────────────────────────────────────────
if not st.session_state.get("token"):
    st.switch_page("pages/Login.py")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 EduTrack AI")
    st.markdown("---")
    st.page_link("App.py",               label="🏠 Dashboard")
    st.page_link("pages/Disciplinas.py",  label="📚 Disciplinas")
    st.page_link("pages/Tarefas.py",      label="📝 Tarefas")
    st.page_link("pages/Relatorios.py",   label="📊 Relatórios")
    st.page_link("pages/Perfil.py",       label="👤 Perfil")
    st.markdown("---")
    user_name = st.session_state.get("user_name", "Usuário")
    st.markdown(f"**{user_name}**")
    if st.button("🚪 Sair", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.switch_page("pages/Login.py")

# ── Carregar nome do usuário ──────────────────────────────────────────────────
if "user_name" not in st.session_state:
    me = get_me()
    if me:
        st.session_state["user_name"]  = me.get("name", "Usuário")
        st.session_state["user_email"] = me.get("email", "")

user_name = st.session_state.get("user_name", "Usuário")

# ── Welcome banner ────────────────────────────────────────────────────────────
hora = datetime.now().hour
saudacao = "Bom dia" if hora < 12 else ("Boa tarde" if hora < 18 else "Boa noite")

st.markdown(f"""
<div class="welcome-banner">
  <div class="welcome-title">👋 {saudacao}, {user_name}!</div>
  <div class="welcome-sub">Aqui está um resumo do seu progresso acadêmico hoje.</div>
</div>
""", unsafe_allow_html=True)

# ── Carregar dados do dashboard ───────────────────────────────────────────────
with st.spinner("Carregando dados..."):
    summary = get_dashboard_summary()

total_subjects  = summary["total_subjects"]
total_pending   = summary["total_pending"]
total_overdue   = summary["total_overdue"]
progress_pct    = summary["progress_pct"]
upcoming        = summary["upcoming"]
total_tasks     = summary["total_tasks"]
total_completed = summary["total_completed"]

# ── Cards de métricas ─────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-icon">📚</div>
      <div class="metric-value">{total_subjects}</div>
      <div class="metric-label">Disciplinas Ativas</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-icon">📝</div>
      <div class="metric-value">{total_pending}</div>
      <div class="metric-label">Tarefas Pendentes</div>
    </div>""", unsafe_allow_html=True)

with c3:
    overdue_cls = "red" if total_overdue > 0 else ""
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-icon">⚠️</div>
      <div class="metric-value {overdue_cls}">{total_overdue}</div>
      <div class="metric-label">Em Atraso</div>
    </div>""", unsafe_allow_html=True)

with c4:
    pct_cls = "green" if progress_pct >= 70 else ("red" if progress_pct < 30 and total_tasks > 0 else "")
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-icon">🎯</div>
      <div class="metric-value {pct_cls}">{progress_pct}%</div>
      <div class="metric-label">Progresso Geral</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Barra de progresso ────────────────────────────────────────────────────────
if total_tasks > 0:
    st.markdown(f"""
    **Progresso:** {total_completed} de {total_tasks} tarefas concluídas
    <div class="progress-bar-bg">
      <div class="progress-bar-fill" style="width:{progress_pct}%"></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ── Próximas tarefas ──────────────────────────────────────────────────────────
col_up, col_tip = st.columns([3, 2])

with col_up:
    st.markdown("### 📅 Próximas Tarefas")
    if not upcoming:
        if total_tasks == 0:
            st.markdown("""
            <div class="empty-state">
              🚀 Nenhuma tarefa ainda.<br>
              Cadastre disciplinas e tarefas para começar!
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state">✅ Sem tarefas futuras pendentes!</div>',
                        unsafe_allow_html=True)
    else:
        for t in upcoming:
            titulo  = t.get("title", "—")
            due_obj = t.get("_due_date_obj")
            due_str = due_obj.strftime("%d/%m/%Y") if due_obj else ""
            from datetime import date
            overdue_cls = "overdue" if (due_obj and due_obj < date.today()) else ""
            st.markdown(f"""
            <div class="upcoming-card {overdue_cls}">
              <div class="upcoming-title">{titulo}</div>
              <div class="upcoming-meta">📅 {due_str}</div>
            </div>""", unsafe_allow_html=True)

with col_tip:
    st.markdown("### 💡 Atalhos Rápidos")
    st.page_link("pages/Disciplinas.py", label="➕ Cadastrar nova disciplina")
    st.page_link("pages/Tarefas.py",     label="➕ Adicionar nova tarefa")
    st.page_link("pages/Relatorios.py",  label="📊 Ver relatório de progresso")

    if total_subjects == 0:
        st.info("💡 Comece cadastrando suas disciplinas do semestre!")
    elif total_overdue > 0:
        st.warning(f"⚠️ Você tem **{total_overdue}** tarefa(s) em atraso!")
    elif progress_pct == 100:
        st.success("🎉 Parabéns! Todas as tarefas concluídas!")