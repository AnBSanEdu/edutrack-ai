"""
pages/Tarefas.py
Gestão de Tarefas Acadêmicas — integração completa com Xano.
"""

import streamlit as st
from datetime import datetime, date, timezone
from utils.api import (
    get_tasks,
    create_task,
    update_task,
    delete_task,
    get_subjects,
)

st.set_page_config(page_title="EduTrack AI — Tarefas", page_icon="📝", layout="wide")

# ── Guard ─────────────────────────────────────────────────────────────────────
if not st.session_state.get("token"):
    st.switch_page("pages/Login.py")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .task-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px;
    padding: 1rem 1.4rem;
    margin-bottom: 0.65rem;
    transition: border-color 0.2s ease;
  }

  .task-card:hover { border-color: rgba(124,58,237,0.45); }

  .task-card.overdue {
    border-left: 4px solid #ef4444;
    background: rgba(239,68,68,0.05);
  }

  .task-card.completed {
    border-left: 4px solid #22c55e;
    opacity: 0.7;
  }

  .task-title {
    font-size: 1rem;
    font-weight: 600;
    color: white;
  }

  .task-title.done {
    text-decoration: line-through;
    color: rgba(255,255,255,0.4);
  }

  .task-meta {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.45);
    margin-top: 0.2rem;
  }

  .status-badge {
    display: inline-block;
    border-radius: 99px;
    padding: 0.15rem 0.65rem;
    font-size: 0.72rem;
    font-weight: 700;
    margin-left: 0.5rem;
    vertical-align: middle;
  }

  .badge-pending    { background: rgba(234,179,8,0.2);  color: #facc15; }
  .badge-in-progress{ background: rgba(59,130,246,0.2); color: #60a5fa; }
  .badge-completed  { background: rgba(34,197,94,0.2);  color: #4ade80; }
  .badge-overdue    { background: rgba(239,68,68,0.2);  color: #f87171; }
  
  .badge-prio {
    display: inline-block;
    border-radius: 99px;
    padding: 0.15rem 0.65rem;
    font-size: 0.72rem;
    font-weight: 700;
    margin-left: 0.5rem;
    vertical-align: middle;
    border: 1px solid rgba(255,255,255,0.2);
  }
  .prio-high { background: rgba(239,68,68,0.1); color: #f87171; border-color: rgba(239,68,68,0.3); }
  .prio-medium { background: rgba(234,179,8,0.1); color: #facc15; border-color: rgba(234,179,8,0.3); }
  .prio-low { background: rgba(59,130,246,0.1); color: #60a5fa; border-color: rgba(59,130,246,0.3); }

  .section-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: rgba(255,255,255,0.75);
    margin: 1.5rem 0 0.75rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    padding-bottom: 0.4rem;
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

# ── Estado ────────────────────────────────────────────────────────────────────
if "editing_task"       not in st.session_state: st.session_state["editing_task"]       = None
if "confirm_delete_task" not in st.session_state: st.session_state["confirm_delete_task"] = None
if "show_form_nova_task" not in st.session_state: st.session_state["show_form_nova_task"] = False

# ── Título ────────────────────────────────────────────────────────────────────
st.title("📝 Minhas Tarefas")
st.markdown("Organize suas atividades acadêmicas por disciplina e prazo.")

# ── Controles de filtro ───────────────────────────────────────────────────────
col_busca, col_status, col_subj, col_btn = st.columns([3, 2, 2, 2])

with col_busca:
    busca = st.text_input("🔍 Buscar tarefa", placeholder="Ex: Trabalho final...", label_visibility="collapsed")

with col_status:
    filtro_status = st.selectbox(
        "Status", ["Todas", "Pendente", "Em andamento", "Concluída", "⚠️ Em atraso"],
        label_visibility="collapsed",
    )

with col_subj:
    subjects_list = get_subjects() or []
    subj_options  = {"Todas as disciplinas": None}
    for s in subjects_list:
        subj_options[s.get("name", "?")] = s.get("id")
    filtro_disciplina = st.selectbox("Disciplina", list(subj_options.keys()), label_visibility="collapsed")

with col_btn:
    if st.button("➕ Nova Tarefa", use_container_width=True, type="primary"):
        st.session_state["show_form_nova_task"] = True

st.markdown("---")

# ── Formulário: Nova Tarefa ───────────────────────────────────────────────────
if st.session_state["show_form_nova_task"]:
    with st.container(border=True):
        st.subheader("➕ Nova Tarefa")
        with st.form("form_nova_tarefa", clear_on_submit=True):
            c1, c2 = st.columns([4, 2])
            with c1:
                nt_titulo = st.text_input("Título da Tarefa*", placeholder="Ex: Entregar relatório de Python")
            with c2:
                if subjects_list:
                    subj_map = {s.get("name", "?"): s.get("id") for s in subjects_list}
                    nt_disciplina_nome = st.selectbox("Disciplina*", list(subj_map.keys()))
                    nt_subject_id = subj_map[nt_disciplina_nome]
                else:
                    st.warning("Cadastre uma disciplina primeiro.")
                    nt_subject_id = None

            nt_descricao = st.text_area("Descrição (opcional)", placeholder="Detalhes da tarefa...")
            c3, c4, c5 = st.columns([2, 2, 2])
            with c3:
                nt_prazo = st.date_input("Prazo", value=None)
            with c4:
                nt_status = st.selectbox("Status", ["pending", "in-progress", "completed"],
                                         format_func=lambda x: {"pending": "Pendente",
                                                                  "in-progress": "Em andamento",
                                                                  "completed": "Concluída"}[x])
            with c5:
                nt_prio = st.selectbox("Prioridade", ["low", "medium", "high"], index=1,
                                       format_func=lambda x: {"low": "Baixa", "medium": "Média", "high": "Alta"}[x])
            cs, cc = st.columns(2)
            with cs:
                salvar_t = st.form_submit_button("💾 Salvar Tarefa", use_container_width=True, type="primary")
            with cc:
                cancelar_t = st.form_submit_button("✖ Cancelar", use_container_width=True)

        if salvar_t:
            if not nt_titulo or not nt_subject_id:
                st.warning("Título e disciplina são obrigatórios.")
            else:
                due_str = nt_prazo.isoformat() if nt_prazo else None
                with st.spinner("Salvando..."):
                    result = create_task(nt_subject_id, nt_titulo, nt_descricao, due_str, nt_status, nt_prio)
                if result:
                    st.success(f"Tarefa **{nt_titulo}** criada!")
                    st.session_state["show_form_nova_task"] = False
                    st.rerun()

        if cancelar_t:
            st.session_state["show_form_nova_task"] = False
            st.rerun()

# ── Carregar tarefas ──────────────────────────────────────────────────────────
STATUS_MAP = {
    "Todas":        None,
    "Pendente":     "pending",
    "Em andamento": "in-progress",
    "Concluída":    "completed",
    "⚠️ Em atraso": None,   # filtrado localmente
}
STATUS_LABEL = {
    "pending":     ("Pendente",     "badge-pending"),
    "in-progress": ("Em andamento", "badge-in-progress"),
    "completed":   ("Concluída",    "badge-completed"),
}

status_filter = STATUS_MAP.get(filtro_status)
subj_filter   = subj_options.get(filtro_disciplina)

with st.spinner("Carregando tarefas..."):
    tasks = get_tasks(status=status_filter, subject_id=subj_filter)

# Mapa de disciplinas para exibir o nome
subj_name_map = {s.get("id"): s.get("name", "?") for s in subjects_list}

# Filtragem local (busca por texto + atraso)
today = date.today()

def _is_overdue(task):
    due = task.get("due_date")
    if not due:
        return False
    try:
        due_dt = datetime.fromisoformat(due.replace("Z", "+00:00")).date()
        return due_dt < today and task.get("status") != "completed"
    except Exception:
        return False

filtered = []
for t in tasks:
    if busca and busca.lower() not in t.get("title", "").lower():
        continue
    if filtro_status == "⚠️ Em atraso" and not _is_overdue(t):
        continue
    filtered.append(t)

# ── Renderizar tarefas ────────────────────────────────────────────────────────
if not filtered:
    st.info("📭 Nenhuma tarefa encontrada. Crie a primeira usando o botão acima!")
else:
    # Agrupar por disciplina
    from collections import defaultdict
    grouped: dict[str, list] = defaultdict(list)
    for t in filtered:
        sid = t.get("subject_id")
        sname = subj_name_map.get(sid, f"Disciplina {sid}")
        grouped[sname].append(t)

    for disciplina_nome, tarefas in grouped.items():
        st.markdown(f'<div class="section-header">📚 {disciplina_nome} &nbsp;·&nbsp; {len(tarefas)} tarefa(s)</div>',
                    unsafe_allow_html=True)

        for task in tarefas:
            tid     = task.get("id")
            titulo  = task.get("title", "—")
            desc    = task.get("description", "")
            status  = task.get("status", "pending")
            due_raw = task.get("due_date")
            overdue = _is_overdue(task)
            done    = status == "completed"

            # Formatar prazo
            prazo_str = ""
            if due_raw:
                try:
                    due_dt    = datetime.fromisoformat(due_raw.replace("Z", "+00:00"))
                    prazo_str = due_dt.strftime("%d/%m/%Y")
                except Exception:
                    prazo_str = due_raw

            # Badge de status
            label_txt, label_cls = STATUS_LABEL.get(status, ("?", "badge-pending"))
            if overdue:
                label_txt, label_cls = "Em atraso", "badge-overdue"

            card_class  = "overdue" if overdue else ("completed" if done else "")
            title_class = "done" if done else ""
            
            prio = task.get("priority", "medium")
            prio_labels = {"low": ("Baixa", "prio-low"), "medium": ("Média", "prio-medium"), "high": ("Alta", "prio-high")}
            prio_txt, prio_cls = prio_labels.get(prio, ("Média", "prio-medium"))

            st.markdown(f"""
            <div class="task-card {card_class}">
              <span class="task-title {title_class}">{titulo}</span>
              <span class="status-badge {label_cls}">{label_txt}</span>
              <span class="badge-prio {prio_cls}">⬆️ {prio_txt}</span>
              <div class="task-meta">
                {'📅 ' + prazo_str + '  ·  ' if prazo_str else ''}
                {desc[:80] + '...' if desc and len(desc) > 80 else desc}
              </div>
            </div>
            """, unsafe_allow_html=True)

            col_done, col_edit, col_del, _ = st.columns([1.5, 1, 1, 5])

            with col_done:
                label_concluir = "↩️ Reabrir" if done else "✅ Concluir"
                if st.button(label_concluir, key=f"done_{tid}"):
                    novo_status = "pending" if done else "completed"
                    with st.spinner("Atualizando..."):
                        update_task(tid, status=novo_status)
                    st.rerun()

            with col_edit:
                if st.button("✏️ Editar", key=f"edit_t_{tid}"):
                    st.session_state["editing_task"]       = tid
                    st.session_state["confirm_delete_task"] = None

            with col_del:
                if st.button("🗑️ Excluir", key=f"del_t_{tid}"):
                    st.session_state["confirm_delete_task"] = tid
                    st.session_state["editing_task"]        = None

            # ── Formulário de edição inline ───────────────────────────────────
            if st.session_state["editing_task"] == tid:
                with st.container(border=True):
                    st.caption(f"Editando: **{titulo}**")
                    with st.form(f"form_edit_t_{tid}"):
                        et1, et2 = st.columns([4, 2])
                        with et1:
                            e_titulo = st.text_input("Título", value=titulo, key=f"et_{tid}")
                        with et2:
                            e_status = st.selectbox(
                                "Status",
                                ["pending", "in-progress", "completed"],
                                index=["pending", "in-progress", "completed"].index(status),
                                format_func=lambda x: {"pending": "Pendente",
                                                        "in-progress": "Em andamento",
                                                        "completed": "Concluída"}[x],
                                key=f"es_{tid}",
                            )
                        e_desc  = st.text_area("Descrição", value=desc or "", key=f"ed_{tid}")
                        try:
                            due_val = datetime.fromisoformat(due_raw.replace("Z", "+00:00")).date() if due_raw else None
                        except Exception:
                            due_val = None
                        
                        ept1, ept2 = st.columns(2)
                        with ept1:
                            e_prazo = st.date_input("Prazo", value=due_val, key=f"ep_{tid}")
                        with ept2:
                            e_prio = st.selectbox(
                                "Prioridade",
                                ["low", "medium", "high"],
                                index=["low", "medium", "high"].index(task.get("priority", "medium")),
                                format_func=lambda x: {"low": "Baixa", "medium": "Média", "high": "Alta"}[x],
                                key=f"eprio_{tid}"
                            )

                        cs2, cc2 = st.columns(2)
                        with cs2:
                            salvar_e = st.form_submit_button("💾 Salvar", use_container_width=True, type="primary")
                        with cc2:
                            cancelar_e = st.form_submit_button("✖ Cancelar", use_container_width=True)

                    if salvar_e:
                        kwargs = {
                            "title":       e_titulo,
                            "description": e_desc,
                            "status":      e_status,
                            "priority":    e_prio,
                            "due_date":    e_prazo.isoformat() if e_prazo else None,
                        }
                        with st.spinner("Salvando..."):
                            update_task(tid, **kwargs)
                        st.session_state["editing_task"] = None
                        st.rerun()

                    if cancelar_e:
                        st.session_state["editing_task"] = None
                        st.rerun()

            # ── Confirmação de exclusão ───────────────────────────────────────
            if st.session_state["confirm_delete_task"] == tid:
                st.warning(f"⚠️ Excluir **{titulo}**? Essa ação não pode ser desfeita.")
                cd1, cd2, _ = st.columns([1.5, 1, 5])
                with cd1:
                    if st.button("✅ Confirmar exclusão", key=f"conf_del_t_{tid}", type="primary"):
                        with st.spinner("Excluindo..."):
                            delete_task(tid)
                        st.session_state["confirm_delete_task"] = None
                        st.rerun()
                with cd2:
                    if st.button("✖ Cancelar", key=f"canc_del_t_{tid}"):
                        st.session_state["confirm_delete_task"] = None
                        st.rerun()