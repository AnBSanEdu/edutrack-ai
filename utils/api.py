"""
utils/api.py
Helper centralizado para chamadas à API do Xano (EduTrack AI).
"""

import requests
import streamlit as st

# ──────────────────────────────────────────────
# Configuração da instância Xano
# ──────────────────────────────────────────────
XANO_INSTANCE = "x8ki-letl-twmt"
XANO_BASE = f"https://{XANO_INSTANCE}.execute-api.us-east-1.xano.io/api"

# Canonicals dos grupos de API
API_AUTH     = f"{XANO_BASE}:ZpmjIFgO"
API_SUBJECTS = f"{XANO_BASE}:pC28Ekit"
API_MEMBERS  = f"{XANO_BASE}:{'members_accounts'}"   # atualizar após verificar canonical


# ──────────────────────────────────────────────
# Funções de suporte
# ──────────────────────────────────────────────

def _headers(auth: bool = True) -> dict:
    """Retorna os cabeçalhos HTTP com ou sem token JWT."""
    h = {"Content-Type": "application/json"}
    if auth:
        token = st.session_state.get("token")
        if token:
            h["Authorization"] = f"Bearer {token}"
    return h


def _handle_response(resp: requests.Response) -> dict | None:
    """Trata a resposta HTTP e retorna o JSON ou None em caso de erro."""
    try:
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError:
        try:
            detail = resp.json()
            msg = detail.get("message") or detail.get("error") or resp.text
        except Exception:
            msg = resp.text
        st.error(f"Erro {resp.status_code}: {msg}")
        return None
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
        return None


# ──────────────────────────────────────────────
# 🔐 Autenticação
# ──────────────────────────────────────────────

def login(email: str, password: str) -> dict | None:
    """POST /auth/login → retorna {authToken, user_id} ou None."""
    resp = requests.post(
        f"{API_AUTH}/auth/login",
        json={"email": email, "password": password},
        headers=_headers(auth=False),
    )
    return _handle_response(resp)


def signup(name: str, email: str, password: str) -> dict | None:
    """POST /auth/signup → retorna {authToken, user_id} ou None."""
    resp = requests.post(
        f"{API_AUTH}/auth/signup",
        json={"name": name, "email": email, "password": password},
        headers=_headers(auth=False),
    )
    return _handle_response(resp)


def get_me() -> dict | None:
    """GET /auth/me → dados do usuário autenticado."""
    resp = requests.get(
        f"{API_AUTH}/auth/me",
        headers=_headers(),
    )
    return _handle_response(resp)


def request_password_reset(email: str) -> dict | None:
    """GET /reset/request_reset_link → envia e-mail de redefinição."""
    resp = requests.get(
        f"{API_AUTH}/reset/request_reset_link",
        params={"email": email},
        headers=_headers(auth=False),
    )
    return _handle_response(resp)


def edit_profile(name: str, email: str) -> dict | None:
    """PATCH /user/edit_profile → atualiza perfil do usuário."""
    resp = requests.patch(
        f"{API_AUTH}/user/edit_profile",
        json={"name": name, "email": email},
        headers=_headers(),
    )
    return _handle_response(resp)


# ──────────────────────────────────────────────
# 📚 Disciplinas (Subjects)
# ──────────────────────────────────────────────

def get_subjects(archived: bool = False) -> list | None:
    """GET /subjects → lista todas as disciplinas do usuário."""
    resp = requests.get(
        f"{API_SUBJECTS}/subjects",
        params={"archived": str(archived).lower()},
        headers=_headers(),
    )
    data = _handle_response(resp)
    if isinstance(data, dict):
        return data.get("items") or data.get("data") or []
    return data if isinstance(data, list) else []


def create_subject(nome: str, professor: str, carga_horaria: str = "", semester: str = "", archived: bool = False) -> dict | None:
    """POST /subjects → cadastra nova disciplina."""
    resp = requests.post(
        f"{API_SUBJECTS}/subjects",
        json={"name": nome, "professor": professor, "workload": carga_horaria, "semester": semester, "archived": archived},
        headers=_headers(),
    )
    return _handle_response(resp)


def update_subject(subject_id: int, nome: str, professor: str, carga_horaria: str = "", semester: str = "", archived: bool = False) -> dict | None:
    """PATCH /subjects/{id} → atualiza disciplina."""
    resp = requests.patch(
        f"{API_SUBJECTS}/subjects/{subject_id}",
        json={"name": nome, "professor": professor, "workload": carga_horaria, "semester": semester, "archived": archived},
        headers=_headers(),
    )
    return _handle_response(resp)


def delete_subject(subject_id: int) -> bool:
    """DELETE /subjects/{id} → exclui disciplina. Retorna True se sucesso."""
    resp = requests.delete(
        f"{API_SUBJECTS}/subjects/{subject_id}",
        headers=_headers(),
    )
    if resp.status_code in (200, 204):
        return True
    _handle_response(resp)
    return False


def search_subjects(query: str) -> list | None:
    """GET /subjects/search → busca disciplinas por nome."""
    resp = requests.get(
        f"{API_SUBJECTS}/subjects/search",
        params={"query": query},
        headers=_headers(),
    )
    data = _handle_response(resp)
    if isinstance(data, dict):
        return data.get("items") or data.get("data") or []
    return data if isinstance(data, list) else []


# ──────────────────────────────────────────────
# 📝 Tarefas Acadêmicas (Academic Tasks)
# ──────────────────────────────────────────────

API_TASKS = f"{XANO_BASE}:academic_tasks"  # canonical será atualizado após push


def get_tasks(status: str = None, subject_id: int = None) -> list:
    """GET /academic_tasks → lista tarefas com filtros opcionais."""
    params = {}
    if status:
        params["status"] = status
    if subject_id:
        params["subject_id"] = subject_id
    resp = requests.get(
        f"{API_TASKS}/academic_tasks",
        params=params,
        headers=_headers(),
    )
    data = _handle_response(resp)
    if isinstance(data, dict):
        return data.get("items") or data.get("data") or []
    return data if isinstance(data, list) else []


def create_task(subject_id: int, title: str, description: str = "",
                due_date: str = None, status: str = "pending", priority: str = "medium") -> dict | None:
    """POST /academic_tasks → cria nova tarefa."""
    payload = {
        "subject_id": subject_id,
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
    }
    if due_date:
        payload["due_date"] = due_date
    resp = requests.post(
        f"{API_TASKS}/academic_tasks",
        json=payload,
        headers=_headers(),
    )
    return _handle_response(resp)


def update_task(task_id: int, **kwargs) -> dict | None:
    """PATCH /academic_tasks/{id} → atualiza campos de uma tarefa."""
    resp = requests.patch(
        f"{API_TASKS}/academic_tasks/{task_id}",
        json=kwargs,
        headers=_headers(),
    )
    return _handle_response(resp)


def delete_task(task_id: int) -> bool:
    """DELETE /academic_tasks/{id} → exclui tarefa. Retorna True se sucesso."""
    resp = requests.delete(
        f"{API_TASKS}/academic_tasks/{task_id}",
        headers=_headers(),
    )
    if resp.status_code in (200, 204):
        return True
    _handle_response(resp)
    return False


# ──────────────────────────────────────────────
# 📊 Dashboard — agregação local
# ──────────────────────────────────────────────

def get_dashboard_summary() -> dict:
    """Agrega métricas do dashboard chamando APIs existentes.

    Retorna dict com:
      - total_subjects: int
      - total_pending: int
      - total_overdue: int
      - progress_pct: float (0-100)
      - upcoming: list[dict] — próximas 5 tarefas por prazo
    """
    from datetime import datetime, date

    subjects = get_subjects() or []
    all_tasks = get_tasks() or []

    today = date.today()

    total_subjects = len(subjects)
    total_tasks    = len(all_tasks)
    total_completed = 0
    total_pending   = 0
    total_overdue   = 0
    upcoming        = []

    for t in all_tasks:
        status  = t.get("status", "pending")
        due_raw = t.get("due_date")

        if status == "completed":
            total_completed += 1
            continue

        total_pending += 1

        if due_raw:
            try:
                due_dt = datetime.fromisoformat(due_raw.replace("Z", "+00:00")).date()
                if due_dt < today:
                    total_overdue += 1
                else:
                    t["_due_date_obj"] = due_dt
                    upcoming.append(t)
            except Exception:
                pass

    # Ordenar por prazo e pegar as 5 mais próximas
    upcoming.sort(key=lambda x: x.get("_due_date_obj", date.max))
    upcoming = upcoming[:5]

    progress_pct = round((total_completed / total_tasks) * 100, 1) if total_tasks > 0 else 0.0

    return {
        "total_subjects":   total_subjects,
        "total_pending":    total_pending,
        "total_overdue":    total_overdue,
        "progress_pct":     progress_pct,
        "upcoming":         upcoming,
        "total_tasks":      total_tasks,
        "total_completed":  total_completed,
    }
