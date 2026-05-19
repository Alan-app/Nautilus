Nautilus v64 / App v64

Alterações desta versão:
- Renomeada a opção “Dados da Ficha” para “Cadastrar/Editar Equipamentos”.
- Adicionado fluxo de cadastro de equipamentos com botão “Adicionar equipamento”.
- O formulário antigo de “Dados da ficha” foi preservado e passa a abrir somente ao adicionar ou editar um equipamento.
- Equipamentos salvos aparecem em lista abaixo do botão principal, com botão “Editar” ao lado de cada item.
- O campo “Equipamento” em “Novo Registro” agora é somente seleção: não permite digitação manual.
- A lista do campo “Equipamento” em “Novo Registro” passa a exibir os equipamentos cadastrados em “Cadastrar/Editar Equipamentos”.
- Ao gerar a Folha 01 / A-1 de um equipamento, os dados cadastrais do equipamento selecionado são usados no cabeçalho da folha.
- Dados antigos de ficha são migrados de forma retrocompatível para a nova lista de equipamentos quando houver equipamento cadastrado.

Módulo alterado:
- Nautilus / Cadastro de Equipamentos / Novo Registro / Documento Oficial.

Módulos preservados:
- LDS offline
- Importação XLSX/XLSM
- Compartilhamento LDS
- Cards LDS
- Modal de progresso LDS
- Launcher/tela inicial
- Horas
- Relatórios
- Dashboard
- Notas / Bloco de notas
- Backup
- PDFs
- Topbar
- Navegação geral
- app_documento_oficial_impressao_direta_forcada.html

Observações técnicas:
- Alteração isolada no módulo de equipamentos e integração do campo “Equipamento”.
- Não houve alteração na base IndexedDB da LDS.
- Persistência continua via dados locais do app, com leitura retrocompatível de fichas antigas.
- O dropdown de equipamentos funciona mesmo quando não há equipamentos cadastrados.
- A versão visual do app/menu foi atualizada para v61.
- Cache offline atualizado para v61.

Histórico recente:
- v48: módulo LDS offline com IndexedDB e busca corrigida.
- v49: Bloco de Notas com altura automática, sem rolagem interna na nota, botão expandir/recolher e persistência individual.
- v50: LDS com botão Compartilhar em cada card de resultado.
- v51: LDS com compartilhamento refinado nos cards.
- v53: LDS com importação única e modal de progresso bloqueante.
- v54: ícone de compartilhar LDS ajustado para estilo ChatGPT.


Registro v56:
- Horas de Funcionamento: atualização de horas agora possui campos Anos, Dias e Horas, com resultado convertido automaticamente para total em horas.
- Quando apenas Horas é preenchido, o resultado replica o mesmo valor em horas.
- Backup/importação corrigidos para preservar e restaurar dados de Horas de Funcionamento.
- README/changelog, cache e versão visual atualizados para v56.

Registro v55:
- “Dados da Ficha” renomeado para “Cadastrar/Editar Equipamentos”.
- Cadastro/listagem/edição de equipamentos implementado.
- “Novo Registro” passa a aceitar somente equipamento selecionado da lista cadastrada.
- Folha 01 / A-1 passa a usar os dados do equipamento selecionado.
- README/changelog, cache e versão visual atualizados para v55.


v57 - Horas de funcionamento: unificação adicionar/editar equipamentos e nova tela adicionar/editar bigramas.

v60 - Correções: restaurado nome Livro Histórico em módulos internos; ajuste menu Bigramas.

v61 - Correção efetiva da v60:
- Restaurada a opção “Adicionar/Editar Bigramas” no menu de Horas de funcionamento, logo abaixo de “Adicionar/Editar Equipamentos”.
- Corrigido o botão “Excluir” da tela “Adicionar/Editar Bigramas”, com remoção do item correto, atualização imediata da lista e persistência.
- Mantido “Nautilus” apenas como branding/nome do app/PWA/instalação.
- Preservado “Livro Histórico” em módulos internos, incluindo “Imprimir Livro Histórico” e relatórios/documentos do módulo.
- Modal de bigramas ajustado para respeitar a topbar/linha amarela.
- Versão visual, README/changelog, service worker/cache e ZIP atualizados para v61.


v62 - Correção do menu Livro Histórico e exclusão de Bigramas.

Nautilus v64 / App v64
Alterações desta versão:
- Adicionado botão “Fechar” no modal “Adicionar/Editar Bigramas” em Horas de funcionamento.
- Ajustado espaçamento no Bloco de Notas para listas de notas arquivadas.
- Ajustado espaçamento no Bloco de Notas para listas de notas excluídas/lixeira.
- Preservados os botões Salvar, Editar e Excluir dos bigramas e demais módulos do app.
- Versão visual, cache e pacote ZIP incrementados para v64.

- v66: removido botão fechar superior duplicado em Adicionar/Editar Bigramas.


v68 - LDS agora exibe 'Aplicação em outros Equipamentos' com associação automática por NSN.

v70 - LDS: corrigida a seção 'Aplicação em outros Equipamentos' para consultar a base real IndexedDB da aba Configured Items Tree, removendo dependência de cache inexistente, normalizando NSN e evitando falso 'Nenhuma outra aplicação encontrada'. Versão visual/cache/ZIP atualizados para v70.


v71 - LDS: otimizada a seção 'Aplicação em outros Equipamentos' com índice/cache por NSN da aba Configured Items Tree, busca limitada à coluna NSN, remoção dos rótulos Functional Mark/Parent Functional Mark nos resultados e versionamento/ZIP atualizados para v71.
v72 - LDS: removidos traços/linhas vazias da seção 'Aplicação em outros Equipamentos' e texto de compartilhamento LDS compactado em formato técnico para WhatsApp, preservando performance e compatibilidade offline/mobile.
v73 - Histórico: cards de Ver Histórico passam a exibir todas as informações diretamente no card, sem botão/ícone Visualizar e sem repetir Equipamento no corpo do card. Versão visual/cache/ZIP atualizados para v73.


v74 - LDS: restaurado o formato anterior do compartilhamento dos cards e ajustada a seção de aplicações relacionadas para exibir o título 'N° DE IDENTIFICAÇÃO' com apenas os valores válidos, sem rótulos Functional Mark/Parent Functional Mark. Versão visual/cache/ZIP atualizados para v74.

v75 - LDS: restaurado o título correto da seção 'Aplicação em outros Equipamentos:' nos cards, desfazendo a substituição indevida por 'N° DE IDENTIFICAÇÃO', mantendo a lista de códigos e a busca NSN otimizada. Versão visual/cache/ZIP atualizados para v75.
