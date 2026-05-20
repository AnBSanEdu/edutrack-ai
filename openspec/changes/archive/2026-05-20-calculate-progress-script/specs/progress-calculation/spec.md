## ADDED Requirements

### Requirement: Calcular porcentagem de progresso
O sistema DEVE calcular a porcentagem de progresso com base no número de tarefas concluídas e no total de tarefas.

#### Scenario: Cálculo de progresso padrão
- **WHEN** o script é executado com 5 tarefas concluídas e um total de 10 tarefas.
- **THEN** o script DEVE retornar um JSON com a chave "progress" e o valor 50.0.

#### Scenario: Nenhuma tarefa concluída
- **WHEN** o script é executado com 0 tarefas concluídas e um total de 10 tarefas.
- **THEN** o script DEVE retornar um JSON com a chave "progress" e o valor 0.0.

#### Scenario: Todas as tarefas concluídas
- **WHEN** o script é executado com 10 tarefas concluídas e um total de 10 tarefas.
- **THEN** o script DEVE retornar um JSON com a chave "progress" e o valor 100.0.

#### Scenario: Total de tarefas é zero
- **WHEN** o script é executado com 0 tarefas concluídas e um total de 0 tarefas.
- **THEN** o script DEVE retornar um JSON com a chave "progress" e o valor 0.0.

#### Scenario: Tarefas concluídas excedem o total
- **WHEN** o script é executado com 12 tarefas concluídas e um total de 10 tarefas.
- **THEN** o script DEVE retornar um JSON com a chave "progress" e o valor 100.0.

#### Scenario: Input não numérico
- **WHEN** o script é executado com um valor não numérico para tarefas concluídas ou total.
- **THEN** o script DEVE apresentar um erro e não retornar JSON.
