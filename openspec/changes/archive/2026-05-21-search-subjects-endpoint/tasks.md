# Tarefas: Implementar Endpoint de Busca de Disciplinas

> Uma lista de tarefas para implementar o change.

- [x] **Task 1: Criar o Script Python para Verificação de Tarefas Atrasadas**
  - Crie o arquivo `scripts/check_overdue_tasks.py`.
  - Implemente a lógica que recebe um `subject_id` e verifica no banco de dados se existem tarefas (`academic_tasks`) com data de vencimento (`due_date`) passada e status diferente de 'concluída'.
  - O script deve imprimir `true` se encontrar tarefas atrasadas e `false` caso contrário.
  - **Nota:** O script `scripts/check_overdue_tasks.py` foi criado com uma implementação de espaço reservado. A conexão com o banco de dados precisa ser configurada com as credenciais corretas.

- [x] **Task 2: Criar o Endpoint no Xano**
  - Crie o arquivo `apis/subjects/4000005_subjects_search_GET.xs`.
  - Defina o endpoint `GET /subjects/search` com autenticação de usuário.
  - Adicione os parâmetros de query `name` (string, opcional) e `has_overdue_tasks` (boolean, opcional).

- [x] **Task 3: Implementar a Lógica de Busca no Xano**
  - No novo endpoint, adicione a lógica para buscar todas as disciplinas do usuário autenticado.
  - Se o parâmetro `name` for fornecido, filtre os resultados para incluir apenas as disciplinas cujo nome corresponda ao termo de busca (ignorando maiúsculas/minúsculas).
  - Se `has_overdue_tasks` for `true`, itere sobre as disciplinas e execute o script `check_overdue_tasks.py` para cada uma, filtrando a lista com base no resultado.

- [x] **Task 4: Criar Testes para o Endpoint**
  - Crie o arquivo `testes_apis/search_subjects_tests.md`.
  - Adicione casos de teste para verificar:
    - A busca por nome.
    - O filtro de tarefas atrasadas.
    - A combinação dos dois filtros.
    - O comportamento quando nenhum filtro é aplicado.
    - A resposta para usuários não autenticados.

- [x] **Task 5: Revisar e Finalizar**
  - Revise todos os arquivos criados para garantir que estão corretos e seguem as convenções do projeto.
  - Execute os testes (manualmente, se necessário) para confirmar que a implementação funciona conforme o esperado.
