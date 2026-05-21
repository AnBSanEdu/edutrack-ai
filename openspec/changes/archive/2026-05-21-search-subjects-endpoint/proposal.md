# Proposta: Endpoint de Busca de Disciplinas

## O Quê e Por Quê

**Problema:** Atualmente, não há uma maneira eficiente de buscar disciplinas. Os usuários não podem filtrar suas disciplinas por nome nem identificar rapidamente aquelas que têm tarefas atrasadas.

**Solução:** Este change propõe a criação de um novo endpoint de API (`GET /subjects/search`) que permitirá aos usuários buscar em suas próprias disciplinas. A busca suportará dois tipos de filtros:

1.  **Por Nome:** Encontrar disciplinas cujo nome corresponda a um termo de busca.
2.  **Por Tarefas Atrasadas:** Listar apenas as disciplinas que contêm tarefas acadêmicas com prazo vencido.

A lógica para identificar tarefas atrasadas será encapsulada em um script Python, que será invocado pelo endpoint do Xano, garantindo que a lógica de negócios complexa seja manutenível e separada da definição da API.

## Benefícios

- **Melhora a Experiência do Usuário:** Facilita a localização de disciplinas específicas.
- **Visibilidade Proativa:** Ajuda os usuários a identificar e focar em disciplinas com pendências críticas.
- **Arquitetura Escalável:** Isola a lógica de negócios em Python, permitindo que ela evolua de forma independente da API.
