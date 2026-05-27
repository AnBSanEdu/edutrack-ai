"""
pages/Disciplinas.py
Gestão de Disciplinas — integração completa com Xano.
"""

import streamlit as st
from utils.api import (
    get_subjects,
    create_subject,
    update_subject,
    delete_subject,
    search_subjects,
)

st.set_page_config(page_title="EduTrack AI — Disciplinas", page_icon="📚", layout="wide")

# ── Guard ─────────────────────────────────────────────────────────────────────
if not st.session_state.get("token"):
    st.switch_page("pages/Login.py")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .subject-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s ease;
  }

  .subject-card:hover {
    border-color: rgba(124,58,237,0.5);
  }

  .subject-card.overdue {
    border-left: 4px solid #ef4444;
  }

  .subject-name {
    font-size: 1.05rem;
    font-weight: 600;
    color: white;
  }

  .subject-meta {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.5);
    margin-top: 0.2rem;
  }

  .badge {
    display: inline-block;
    background: rgba(239,68,68,0.2);
    color: #f87171;
    border-radius: 99px;
    padding: 0.15rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 600;
    margin-left: 0.5rem;
  }

  .stButton > button {
    border-radius: 8px !important;
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

# ── Estado de edição ──────────────────────────────────────────────────────────
if "editing_subject" not in st.session_state:
    st.session_state["editing_subject"] = None

if "confirm_delete_subject" not in st.session_state:
    st.session_state["confirm_delete_subject"] = None

# ── Título ────────────────────────────────────────────────────────────────────
st.title("📚 Gestão de Disciplinas")
st.markdown("Cadastre e gerencie suas matérias do semestre.")

# ── Controles: busca + filtro ─────────────────────────────────────────────────
col_search, col_filter, col_btn = st.columns([4, 2, 2])

with col_search:
    query = st.text_input("🔍 Buscar por nome", placeholder="Ex: Cálculo, Python...", label_visibility="collapsed")

with col_filter:
    filtro_arquivado = st.checkbox("📦 Arquivadas")
    filtro_atraso = st.checkbox("⚠️ Em atraso")

with col_btn:
    nova_disciplina = st.button("➕ Nova Disciplina", use_container_width=True, type="primary")

st.markdown("---")

# ── Formulário: Nova Disciplina ───────────────────────────────────────────────
if nova_disciplina:
    st.session_state["show_form_nova"] = True

if st.session_state.get("show_form_nova"):
    with st.container(border=True):
        st.subheader("➕ Cadastrar nova disciplina")
        with st.form("form_nova_disciplina", clear_on_submit=True):
            c1, c2, c3, c4 = st.columns([3, 3, 2, 2])
            with c1:
                n_nome = st.text_input("Nome da Disciplina*", placeholder="Ex: Cálculo I")
            with c2:
                n_prof = st.text_input("Professor*", placeholder="Ex: Prof. João")
            with c3:
                n_carga = st.text_input("Carga Horária", placeholder="Ex: 60h")
            with c4:
                n_semestre = st.text_input("Semestre", placeholder="Ex: 2024.1")

            col_s, col_c = st.columns(2)
            with col_s:
                salvar_nova = st.form_submit_button("💾 Salvar", use_container_width=True, type="primary")
            with col_c:
                cancelar = st.form_submit_button("✖ Cancelar", use_container_width=True)

        if salvar_nova:
            if not n_nome or not n_prof:
                st.warning("Nome e professor são obrigatórios.")
            else:
                with st.spinner("Salvando..."):
                    result = create_subject(n_nome, n_prof, n_carga, n_semestre, False)
                if result:
                    st.success(f"Disciplina **{n_nome}** cadastrada com sucesso!")
                    st.session_state["show_form_nova"] = False
                    st.rerun()

        if cancelar:
            st.session_state["show_form_nova"] = False
            st.rerun()

# ── Carregar disciplinas ──────────────────────────────────────────────────────
with st.spinner("Carregando disciplinas..."):
    if query:
        subjects = search_subjects(query) or []
    else:
        subjects = get_subjects(archived=filtro_arquivado) or []

# ── Lista de disciplinas ──────────────────────────────────────────────────────
if not subjects:
    st.info("📭 Nenhuma disciplina encontrada. Cadastre a primeira usando o botão acima!")
else:
    st.markdown(f"**{len(subjects)} disciplina(s) encontrada(s)**")

    for subj in subjects:
        sid   = subj.get("id")
        nome  = subj.get("name", "—")
        prof  = subj.get("professor", "—")
        carga = subj.get("workload", "")
        sem   = subj.get("semester", "")
        arch  = subj.get("archived", False)

        # Card da disciplina
        extra_class = "overdue" if arch else ""
        badge_arch = '<span class="badge" style="background:rgba(255,255,255,0.1); color:#fff; border:1px solid #aaa;">Arquivada</span>' if arch else ''
        
        st.markdown(f"""
        <div class="subject-card {extra_class}">
          <span class="subject-name">{nome} {badge_arch}</span>
          <div class="subject-meta">👨‍🏫 {prof}{"  ·  📖 " + carga if carga else ""}{"  ·  📅 " + sem if sem else ""}</div>
        </div>
        """, unsafe_allow_html=True)

        col_edit, col_del, _ = st.columns([1, 1, 6])

        with col_edit:
            if st.button("✏️ Editar", key=f"edit_{sid}"):
                st.session_state["editing_subject"] = sid
                st.session_state["confirm_delete_subject"] = None

        with col_del:
            if st.button("🗑️ Excluir", key=f"del_{sid}"):
                st.session_state["confirm_delete_subject"] = sid
                st.session_state["editing_subject"] = None

        # ── Formulário de edição inline ───────────────────────────────────────
        if st.session_state.get("editing_subject") == sid:
            with st.container(border=True):
                st.caption(f"Editando: **{nome}**")
                with st.form(f"form_edit_{sid}"):
                    e1, e2, e3, e4, e5 = st.columns([3, 3, 2, 2, 2])
                    with e1:
                        e_nome = st.text_input("Nome", value=nome, key=f"en_{sid}")
                    with e2:
                        e_prof = st.text_input("Professor", value=prof, key=f"ep_{sid}")
                    with e3:
                        e_carga = st.text_input("Carga Horária", value=carga, key=f"ec_{sid}")
                    with e4:
                        e_sem = st.text_input("Semestre", value=sem, key=f"es_{sid}")
                    with e5:
                        st.markdown("<br>", unsafe_allow_html=True)
                        e_arch = st.checkbox("Arquivada", value=arch, key=f"ea_{sid}")

                    cs, cc = st.columns(2)
                    with cs:
                        salvar_edit = st.form_submit_button("💾 Salvar", use_container_width=True, type="primary")
                    with cc:
                        cancelar_edit = st.form_submit_button("✖ Cancelar", use_container_width=True)

                if salvar_edit:
                    if not e_nome or not e_prof:
                        st.warning("Nome e professor são obrigatórios.")
                    else:
                        with st.spinner("Salvando..."):
                            result = update_subject(sid, e_nome, e_prof, e_carga, e_sem, e_arch)
                        if result is not None:
                            st.success("Disciplina atualizada!")
                            st.session_state["editing_subject"] = None
                            st.rerun()

                if cancelar_edit:
                    st.session_state["editing_subject"] = None
                    st.rerun()

        # ── Confirmação de exclusão ───────────────────────────────────────────
        if st.session_state.get("confirm_delete_subject") == sid:
            st.warning(f"⚠️ Tem certeza que deseja excluir **{nome}**? Esta ação não pode ser desfeita.")
            cd1, cd2, _ = st.columns([1, 1, 6])
            with cd1:
                if st.button("✅ Confirmar exclusão", key=f"confirm_del_{sid}", type="primary"):
                    with st.spinner("Excluindo..."):
                        ok = delete_subject(sid)
                    if ok:
                        st.success(f"Disciplina **{nome}** excluída.")
                        st.session_state["confirm_delete_subject"] = None
                        st.rerun()
            with cd2:
                if st.button("✖ Cancelar", key=f"cancel_del_{sid}"):
                    st.session_state["confirm_delete_subject"] = None
                    st.rerun()
