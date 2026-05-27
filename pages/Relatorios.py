"""
pages/Relatorios.py
Relatórios de progresso acadêmico — histórico e exportação CSV.
"""

import streamlit as st
from datetime import datetime, date, timedelta
from collections import defaultdict
import io
from utils.api import get_tasks, get_subjects

st.set_page_config(page_title="EduTrack AI — Relatórios", page_icon="📊", layout="wide")

# ── Guard ─────────────────────────────────────────────────────────────────────
if not st.session_state.get("token"):
    st.switch_page("pages/Login.py")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0c29 0%, #302b63 100%);
  }
  section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }

  .report-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
  }

  .report-title {
    font-size: 1rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.75rem;
  }

  .progress-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.55rem;
  }

  .progress-label {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.7);
    min-width: 160px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .progress-bar-bg {
    flex: 1;
    background: rgba(255,255,255,0.08);
    border-radius: 99px;
    height: 8px;
    overflow: hidden;
  }

  .progress-bar-fill {
    background: linear-gradient(90deg, #7c3aed, #3b82f6);
    height: 100%;
    border-radius: 99px;
  }

  .progress-pct {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.45);
    min-width: 36px;
    text-align: right;
  }

  .stat-chip {
    display: inline-block;
    background: rgba(255,255,255,0.07);
    border-radius: 8px;
    padding: 0.3rem 0.7rem;
    font-size: 0.8rem;
    color: rgba(255,255,255,0.65);
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
  }

  .badge-status {
    display: inline-block;
    border-radius: 99px;
    padding: 0.1rem 0.55rem;
    font-size: 0.7rem;
    font-weight: 700;
  }
  .s-pending    { background:rgba(234,179,8,0.2);  color:#facc15; }
  .s-progress   { background:rgba(59,130,246,0.2); color:#60a5fa; }
  .s-completed  { background:rgba(34,197,94,0.2);  color:#4ade80; }
  .s-overdue    { background:rgba(239,68,68,0.2);  color:#f87171; }
</style>
""", unsafe_allow_html=True)

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
    if st.button("🚪 Sair", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.switch_page("pages/Login.py")

# ── Título ────────────────────────────────────────────────────────────────────
st.title("📊 Relatórios de Progresso")
st.markdown("Acompanhe seu desempenho acadêmico por período e disciplina.")
st.markdown("---")

# ── Filtro de período ─────────────────────────────────────────────────────────
col_f1, col_f2, col_f3 = st.columns([2, 2, 3])

with col_f1:
    data_inicio = st.date_input("De", value=date.today() - timedelta(days=90))
with col_f2:
    data_fim = st.date_input("Até", value=date.today())
with col_f3:
    st.markdown("<br>", unsafe_allow_html=True)
    aplicar = st.button("🔍 Aplicar filtro", type="primary")

# ── Carregar dados ────────────────────────────────────────────────────────────
with st.spinner("Carregando relatórios..."):
    all_tasks    = get_tasks() or []
    all_subjects = get_subjects() or []

subj_name_map = {s.get("id"): s.get("name", "?") for s in all_subjects}

# Filtrar pelo período
def parse_date(raw: str) -> date | None:
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).date()
    except Exception:
        return None

tasks_no_periodo = [
    t for t in all_tasks
    if (cd := parse_date(t.get("created_at"))) and data_inicio <= cd <= data_fim
]

today = date.today()

# Classificar
def classify(t):
    s = t.get("status", "pending")
    due = parse_date(t.get("due_date"))
    if s == "completed":
        return "completed"
    if due and due < today:
        return "overdue"
    if s == "in-progress":
        return "in-progress"
    return "pending"

# ── Seção 1: Resumo do período ────────────────────────────────────────────────
st.subheader(f"📅 Período: {data_inicio.strftime('%d/%m/%Y')} → {data_fim.strftime('%d/%m/%Y')}")

total  = len(tasks_no_periodo)
by_cls = defaultdict(int)
for t in tasks_no_periodo:
    by_cls[classify(t)] += 1

if total == 0:
    st.info("Nenhuma tarefa encontrada nesse período. Ajuste o filtro de datas.")
else:
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    col_s1.metric("Total de Tarefas",   total)
    col_s2.metric("✅ Concluídas",       by_cls["completed"])
    col_s3.metric("⏳ Pendentes",        by_cls["pending"] + by_cls["in-progress"])
    col_s4.metric("⚠️ Em Atraso",        by_cls["overdue"])

st.markdown("<br>", unsafe_allow_html=True)

# ── Seção 2: Progresso por disciplina ─────────────────────────────────────────
st.subheader("📚 Progresso por Disciplina")

tasks_by_subj: dict[str, list] = defaultdict(list)
for t in tasks_no_periodo:
    sid   = t.get("subject_id")
    sname = subj_name_map.get(sid, f"Disciplina {sid}")
    tasks_by_subj[sname].append(t)

if not tasks_by_subj:
    st.info("Sem dados de disciplinas no período selecionado.")
else:
    st.markdown('<div class="report-card"><div class="report-title">Conclusão por Matéria</div>', unsafe_allow_html=True)
    for sname, tarefas in sorted(tasks_by_subj.items()):
        total_s = len(tarefas)
        done_s  = sum(1 for t in tarefas if classify(t) == "completed")
        pct     = round((done_s / total_s) * 100) if total_s > 0 else 0
        st.markdown(f"""
        <div class="progress-row">
          <span class="progress-label" title="{sname}">{sname}</span>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:{pct}%"></div>
          </div>
          <span class="progress-pct">{pct}%</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin-bottom:0.6rem; margin-left:172px;">
          <span class="stat-chip">📋 {total_s} tarefas</span>
          <span class="stat-chip">✅ {done_s} concluídas</span>
          <span class="stat-chip">⚠️ {sum(1 for t in tarefas if classify(t)=='overdue')} em atraso</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Seção 3: Histórico detalhado ──────────────────────────────────────────────
st.subheader("📋 Histórico de Tarefas")

STATUS_LABEL = {
    "completed": ("Concluída",     "s-completed"),
    "overdue":   ("Em Atraso",     "s-overdue"),
    "in-progress":("Em andamento", "s-progress"),
    "pending":   ("Pendente",      "s-pending"),
}

if tasks_no_periodo:
    # Ordenar por data de criação desc
    tasks_sorted = sorted(
        tasks_no_periodo,
        key=lambda t: t.get("created_at", ""),
        reverse=True,
    )

    for t in tasks_sorted:
        sid     = t.get("subject_id")
        sname   = subj_name_map.get(sid, "—")
        titulo  = t.get("title", "—")
        cls     = classify(t)
        lbl, badge_cls = STATUS_LABEL.get(cls, ("?", "s-pending"))
        due_obj = parse_date(t.get("due_date"))
        due_str = due_obj.strftime("%d/%m/%Y") if due_obj else "—"
        cri_obj = parse_date(t.get("created_at"))
        cri_str = cri_obj.strftime("%d/%m/%Y") if cri_obj else "—"

        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:1rem;
                    padding:0.6rem 1rem; border-radius:10px;
                    background:rgba(255,255,255,0.03); margin-bottom:0.35rem;">
          <span style="flex:3; font-size:0.9rem; color:white; font-weight:500;">{titulo}</span>
          <span style="flex:2; font-size:0.78rem; color:rgba(255,255,255,0.45);">📚 {sname}</span>
          <span style="flex:1; font-size:0.78rem; color:rgba(255,255,255,0.35);">📅 {due_str}</span>
          <span style="flex:1; font-size:0.78rem; color:rgba(255,255,255,0.3);">➕ {cri_str}</span>
          <span class="badge-status {badge_cls}">{lbl}</span>
        </div>
        """, unsafe_allow_html=True)

# ── Seção 4: Exportar CSV ─────────────────────────────────────────────────────
st.markdown("---")
st.subheader("⬇️ Exportar Dados")

col_csv, col_info = st.columns([2, 4])

with col_csv:
    if tasks_no_periodo:
        # Montar CSV em memória
        linhas = ["Título,Disciplina,Status,Prazo,Criado em"]
        for t in tasks_no_periodo:
            sid     = t.get("subject_id")
            sname   = subj_name_map.get(sid, "")
            titulo  = t.get("title", "").replace(",", ";")
            cls     = classify(t)
            lbl, _  = STATUS_LABEL.get(cls, ("?", ""))
            due_obj = parse_date(t.get("due_date"))
            cri_obj = parse_date(t.get("created_at"))
            linhas.append(
                f"{titulo},{sname},{lbl},"
                f"{due_obj.strftime('%d/%m/%Y') if due_obj else ''},"
                f"{cri_obj.strftime('%d/%m/%Y') if cri_obj else ''}"
            )

        csv_bytes = "\n".join(linhas).encode("utf-8-sig")   # utf-8-sig para Excel
        st.download_button(
            label="📥 Baixar CSV",
            data=csv_bytes,
            file_name=f"edutrack_tarefas_{data_inicio}_{data_fim}.csv",
            mime="text/csv",
            use_container_width=True,
            type="primary",
        )
    else:
        st.button("📥 Baixar CSV", disabled=True, use_container_width=True)

with col_info:
    st.info(
        "O arquivo CSV é compatível com Excel e Google Sheets. "
        "Contém: Título, Disciplina, Status, Prazo e Data de criação de cada tarefa no período filtrado."
    )
