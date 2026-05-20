## Context

O objetivo é criar um script simples em Python para calcular o progresso. O script será executado a partir da linha de comando, receberá dois argumentos numéricos (concluídas e total) e imprimirá uma string JSON no `stdout`.

## Goals / Non-Goals

**Goals:**
- Implementar a lógica de cálculo de porcentagem em Python.
- Usar a biblioteca padrão `argparse` para lidar com argumentos de linha de comando.
- Usar a biblioteca padrão `json` para formatar a saída.
- Garantir que o script lide com o caso de divisão por zero (total de tarefas = 0).

**Non-Goals:**
- Criar uma interface gráfica.
- Integrar o script com qualquer sistema de banco de dados ou API externa.

## Decisions

- **Linguagem**: Python 3, por sua simplicidade e vasta biblioteca padrão.
- **Tratamento de Input**: `argparse` será usado para uma interface de linha de comando clara e para gerar mensagens de ajuda. Os argumentos serão `completed` e `total`.
- **Formato de Saída**: JSON será usado para a saída, pois é um formato leve e facilmente parsável por outras ferramentas. O JSON de saída terá a chave `progress`.
- **Tratamento de Erros**: Se o total de tarefas for 0, o progresso será considerado 0% para evitar uma exceção de `ZeroDivisionError`. Se as tarefas concluídas forem maiores que o total, o progresso será 100%.

## Risks / Trade-offs

- **Risco**: O script pode receber inputs não numéricos.
  - **Mitigação**: O `argparse` com `type=int` fará a validação e retornará um erro amigável se o input não for um inteiro.
