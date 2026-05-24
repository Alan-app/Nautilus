Nautilus v120 / App v120

Alterações desta versão:
- CORREÇÃO: ao clicar em editar uma nota grande, o card não encolhe mais.
- O card editável agora mantém exatamente a mesma altura visual do card de visualização.
- A única diferença ao entrar em edição é que o texto fica editável e o cursor aparece onde clicou.
- Nenhuma alteração em wrappers, checklist, textarea, layout ou disposição visual.

Técnica aplicada:
- A altura real do card é capturada via offsetHeight antes de renderNotes() ser chamado.
- Após o re-render, essa altura é aplicada como min-height no card editável.
- Nenhuma propriedade interna foi alterada.

Módulo alterado:
- Notas (função editNote) — captura e aplica min-height para evitar encolhimento do card.

Módulos preservados:
- LDS offline
- Importação XLSX/XLSM
- Compartilhamento LDS
- Cards LDS
- Checklist de notas
- Layout visual das notas
- Todos os demais módulos da v119

Base: Nautilus-v119-checklist-real-formato-preservado.zip
