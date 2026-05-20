
# Proposta: Criação da Tabela `academic_tasks`

## Why

O sistema necessita de uma estrutura para que os alunos possam registrar e gerenciar suas obrigações acadêmicas, como lições de casa, trabalhos e provas. Atualmente, não há uma tabela para armazenar essas informações, o que impede o desenvolvimento de funcionalidades de gerenciamento de tarefas.

## What Changes

A única mudança proposta é a criação de uma nova tabela no banco de dados.

1.  **Nova Tabela `academic_tasks`**: Será criada uma nova tabela para armazenar as tarefas dos alunos, contendo campos para título, descrição, data de entrega, status, e a associação com uma disciplina e com o próprio aluno.

## Impact

- **Backend**: Uma nova tabela será adicionada ao schema do banco de dados. Nenhuma API ou lógica de negócio existente será modificada.
- **Frontend**: Esta mudança não terá impacto direto no frontend. No entanto, ela é um pré-requisito para futuras funcionalidades de interface que permitirão aos alunos gerenciar suas tarefas.
- **Usuários**: Nenhum impacto imediato, mas esta mudança habilita o desenvolvimento futuro de ferramentas de organização para os alunos.
