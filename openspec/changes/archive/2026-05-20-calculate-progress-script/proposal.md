## Why

Para acompanhar o progresso de tarefas ou atividades, é necessário um script que possa calcular a porcentagem de conclusão de forma padronizada e fornecer a saída em um formato estruturado (JSON) para fácil integração com outros sistemas.

## What Changes

- Criação de um novo script Python em `scripts/calculate_progress.py`.
- O script receberá como entrada o número de tarefas concluídas e o número total de tarefas.
- O script calculará a porcentagem de progresso.
- O script retornará um objeto JSON contendo a porcentagem calculada.

## Capabilities

### New Capabilities
- `progress-calculation`: Um script para calcular a porcentagem de progresso de tarefas.

### Modified Capabilities


## Impact

- Nenhum impacto em sistemas existentes, pois este é um script novo e independente.
- O script poderá ser utilizado por qualquer outro componente do sistema que precise calcular o progresso.
