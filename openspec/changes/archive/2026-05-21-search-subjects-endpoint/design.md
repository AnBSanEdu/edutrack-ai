# Design: Endpoint de Busca de Disciplinas

## 1. Visão Geral da Arquitetura

O sistema será composto por dois componentes principais:

1.  **Endpoint Xano (`GET /subjects/search`):** O ponto de entrada da API. Ele validará a autenticação, processará os parâmetros de entrada e orquestrará a lógica de busca.
2.  **Script Python (`check_overdue_tasks.py`):** Um script que receberá um ID de disciplina, verificará se existem tarefas atrasadas associadas a ela e retornará um resultado booleano.

O fluxo de trabalho será o seguinte:
- O cliente faz uma requisição para `GET /subjects/search`.
- O endpoint Xano primeiro busca todas as disciplinas do usuário autenticado.
- Dependendo dos parâmetros, ele filtra os resultados por nome ou invoca o script Python para cada disciplina para verificar se há tarefas atrasadas.
- O resultado final é retornado ao cliente.

## 2. Definição da API

### Endpoint: `GET /subjects/search`

- **Autenticação:** Requerida (usuário logado).
- **Grupo da API:** `subjects`.

- **Parâmetros de Query:**
  - `name` (string, opcional): Termo para buscar no nome da disciplina. A busca será *case-insensitive*.
  - `has_overdue_tasks` (boolean, opcional): Se `true`, retorna apenas disciplinas com tarefas atrasadas.

- **Lógica do Endpoint:**
  1.  Verifica se o usuário está autenticado.
  2.  Busca no banco de dados todas as disciplinas (`subjects`) associadas ao `$auth.id`.
  3.  **Se `name` for fornecido:**
      - Filtra a lista de disciplinas, mantendo apenas aquelas cujo nome contém o valor de `name` (ignorando maiúsculas/minúsculas).
  4.  **Se `has_overdue_tasks` for `true`:**
      - Itera sobre as disciplinas restantes.
      - Para cada disciplina, executa o script Python `check_overdue_tasks.py` passando o `subject.id`.
      - Mantém na lista apenas as disciplinas para as quais o script retorna `true`.
  5.  Retorna a lista de disciplinas filtrada.

- **Exemplo de Resposta (200 OK):**
  ```json
  [
    {
      "id": 1,
      "name": "História Antiga",
      "description": "Estudo das civilizações da antiguidade.",
      "user_id": 123,
      "created_at": "2026-05-21T10:00:00Z"
    }
  ]
  ```

## 3. Lógica do Script Python

### Script: `scripts/check_overdue_tasks.py`

- **Função:** Determinar se uma disciplina específica possui tarefas atrasadas.
- **Entrada:** `subject_id` (recebido como argumento de linha de comando).
- **Lógica:**
  1.  Recebe `subject_id` como argumento.
  2.  Conecta-se ao banco de dados (assume-se que as credenciais estão disponíveis como variáveis de ambiente).
  3.  Executa uma query na tabela `academic_tasks`.
  4.  A query busca por tarefas onde `subject_id` corresponde ao ID fornecido E `due_date` é anterior à data e hora atuais E `status` não é 'concluída'.
  5.  Se a query retornar um ou more resultados, o script imprime `true` na saída padrão.
  6.  Caso contrário, imprime `false`.

- **Exemplo de Invocação (dentro do Xano):**
  ```
  shell: python scripts/check_overdue_tasks.py {subject.id}
  ```

## 4. Estrutura de Arquivos

```
.
├── apis/
│   └── subjects/
│       └── ...
│       └── 4000005_subjects_search_GET.xs  <-- NOVO
├── scripts/
│   └── check_overdue_tasks.py             <-- NOVO
└── ...
```
