#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import sys

p = Path('app.html')
t = p.read_text(encoding='utf-8')
orig = t

# --- version ---
for v in ("V.Beta.79", "V.Beta.80", "V.Beta.65"):
    t = t.replace("const APP_VERSION = '%s';" % v, "const APP_VERSION = 'V.Beta.81';")

# --- noteResizeChecklistInput: crescer com texto ---
old_resize = """function noteResizeChecklistInput(el){
  if(!el) return;
  el.style.setProperty('height','28px','important');
  el.style.setProperty('min-height','28px','important');
  el.style.setProperty('max-height','28px','important');
  el.style.setProperty('line-height','28px','important');
  el.style.setProperty('overflow','hidden','important');
  const row = el.closest ? el.closest('.keep-check-edit-row') : null;
  if(row){
    row.style.setProperty('height','28px','important');
    row.style.setProperty('min-height','28px','important');
    row.style.setProperty('max-height','28px','important');
    row.style.setProperty('overflow','visible','important');
  }
}"""

new_resize = """function noteResizeChecklistInput(el){
  if(!el) return;
  /* V.Beta.81: cresce com o texto */
  el.style.setProperty('height','auto','important');
  el.style.setProperty('min-height','28px','important');
  el.style.setProperty('max-height','none','important');
  el.style.setProperty('line-height','1.35','important');
  el.style.setProperty('overflow','hidden','important');
  el.style.setProperty('white-space','pre-wrap','important');
  el.style.setProperty('height', Math.max(28, Math.ceil(el.scrollHeight||28))+'px', 'important');
  const row = el.closest ? el.closest('.keep-check-edit-row') : null;
  if(row){
    const h = Math.max(28, Math.ceil(el.getBoundingClientRect().height||el.scrollHeight||28));
    row.style.setProperty('height', h+'px', 'important');
    row.style.setProperty('min-height', h+'px', 'important');
    row.style.setProperty('max-height', 'none', 'important');
    row.style.setProperty('overflow', 'visible', 'important');
  }
}"""

if old_resize in t:
    t = t.replace(old_resize, new_resize, 1)
    print('patched noteResizeChecklistInput')
elif 'V.Beta.81: cresce com o texto' in t:
    print('noteResizeChecklistInput already patched')
else:
    print('WARN: noteResizeChecklistInput not found')

# --- oninput do refresh: usar autosize em vez de resize fixo ---
if "noteSyncRowEmpty(this);noteResizeChecklistInput(this)`);" in t:
    t = t.replace(
        "noteSyncRowEmpty(this);noteResizeChecklistInput(this)`);",
        "noteSyncRowEmpty(this);noteAutosizeTextarea(this);noteAutosizeChecklist(this.closest('.keep-check-edit-wrap'));noteHistoryMaybePush('${safeId}')`);",
        1,
    )
    print('patched refresh oninput')
else:
    print('WARN: refresh oninput pattern not found')

# --- Backspace: so apaga se vazio; senao merge pra cima ---
old_bs = """  if(key==='Backspace'){
    const value=String(el.value||''),s=typeof el.selectionStart==='number'?el.selectionStart:value.length,e=typeof el.selectionEnd==='number'?el.selectionEnd:value.length;
    if(value.length===0||(s===0&&e===0)){
      ev.preventDefault();ev.stopPropagation();
      if(wrap&&currentRow&&wrap.children.length>1){
        const focusIndex=Math.max(0,idx-1);
        currentRow.remove();noteRefreshChecklistDom(noteId);noteCommitChecklistDomToText(noteId);noteAutosizeChecklist(wrap);
        const target=wrap.querySelector('.keep-check-edit-row[data-line-index="'+focusIndex+'"] .keep-check-edit-input');
        if(target){target.focus({preventScroll:true});try{const l=String(target.value||'').length;target.setSelectionRange(l,l);}catch(e){}}
      }
    }
  }
}"""

new_bs = """  if(key==='Backspace'){
    const value=String(el.value||'');
    const s=typeof el.selectionStart==='number'?el.selectionStart:value.length;
    const e=typeof el.selectionEnd==='number'?el.selectionEnd:value.length;
    if(s===0&&e===0){
      ev.preventDefault();ev.stopPropagation();
      if(!wrap||!currentRow)return;
      /* so apaga a linha se estiver vazia (so a caixa); senao faz merge do texto na linha de cima */
      if(String(value).trim()===''){
        if(wrap.children.length>1){
          const focusIndex=Math.max(0,idx-1);
          currentRow.remove();noteRefreshChecklistDom(noteId);noteCommitChecklistDomToText(noteId);noteAutosizeChecklist(wrap);noteHistoryMaybePush(noteId);
          const target=wrap.querySelector('.keep-check-edit-row[data-line-index="'+focusIndex+'"] .keep-check-edit-input');
          if(target){target.focus({preventScroll:true});try{const l=String(target.value||'').length;target.setSelectionRange(l,l);}catch(err){}}
        }
        return;
      }
      const prev=currentRow.previousElementSibling;
      if(prev&&prev.classList&&prev.classList.contains('keep-check-edit-row')){
        const prevInp=prev.querySelector('.keep-check-edit-input');
        if(prevInp){
          const prevVal=String(prevInp.value||'');
          const junction=prevVal.length;
          prevInp.value=prevVal+value;
          currentRow.remove();
          noteRefreshChecklistDom(noteId);noteCommitChecklistDomToText(noteId);noteAutosizeChecklist(wrap);noteHistoryMaybePush(noteId);
          const target=wrap.querySelector('.keep-check-edit-row[data-line-index="'+(idx-1)+'"] .keep-check-edit-input')||prevInp;
          if(target){target.focus({preventScroll:true});try{target.setSelectionRange(junction,junction);}catch(err){}}
        }
      }
    }
  }
}"""

if old_bs in t:
    t = t.replace(old_bs, new_bs, 1)
    print('patched Backspace merge')
elif 'so apaga a linha se estiver vazia' in t:
    print('Backspace already patched')
else:
    print('WARN: Backspace block not found')

# --- editNote: remover classe collapsed + historico ---
old_edit = "if(n.collapsed){n.collapsed=false;AppState.save();}\n  UI.editingNoteId=id;UI.noteEditLockedHeight=0;UI.noteEditMinHeight=0;"
new_edit = old_edit + "\n  noteHistoryReset(id, n.titulo, n.texto);"
if old_edit in t and 'noteHistoryReset(id, n.titulo, n.texto)' not in t:
    t = t.replace(old_edit, new_edit, 1)
    print('patched history reset in editNote')
else:
    print('history reset skip or already')

old_cls = "article.classList.add('editing');article.onclick=null;"
new_cls = "article.classList.remove('collapsed');article.classList.add('editing');article.onclick=null;"
if "classList.remove('collapsed')" not in t:
    if old_cls in t:
        t = t.replace(old_cls, new_cls, 1)
        print('patched remove collapsed class')
    else:
        print('WARN: collapsed class add not found')
else:
    print('collapsed remove already present')

# --- historico undo/redo helpers ---
hist = r'''
/* V.Beta.81 - historico desfazer/refazer das notas */
var noteEditHistory={id:null,undo:[],redo:[],current:null,applying:false,timer:null};
function noteHistoryReset(id,titulo,texto){
  noteEditHistory.id=String(id);
  noteEditHistory.undo=[];
  noteEditHistory.redo=[];
  noteEditHistory.current={titulo:String(titulo||''),texto:String(texto||'')};
  noteEditHistory.applying=false;
  if(noteEditHistory.timer){clearTimeout(noteEditHistory.timer);noteEditHistory.timer=null;}
}
function noteHistoryCanUndo(id){ return noteEditHistory.id===String(id)&&noteEditHistory.undo.length>0; }
function noteHistoryCanRedo(id){ return noteEditHistory.id===String(id)&&noteEditHistory.redo.length>0; }
function noteHistorySnapshotFromDom(noteId){
  ensureNotas();
  const n=AppState.data.notas.find(x=>String(x.id)===String(noteId));
  if(!n)return null;
  const article=document.querySelector('#screen-notas .keep-note.editing[data-note-id="'+CSS.escape(String(noteId))+'"]');
  let titulo=String(n.titulo||'');
  let texto=String(n.texto||'');
  if(article){
    const ti=article.querySelector('.keep-inline-title');
    if(ti)titulo=String(ti.value||'');
    const live=typeof noteLiveTextFromEditor==='function'?noteLiveTextFromEditor(noteId):null;
    if(live!==null)texto=String(live);
  }
  return {titulo:titulo,texto:texto};
}
function noteHistoryMaybePush(noteId){
  if(noteEditHistory.applying)return;
  if(noteEditHistory.id!==String(noteId))return;
  if(noteEditHistory.timer)clearTimeout(noteEditHistory.timer);
  noteEditHistory.timer=setTimeout(function(){
    noteEditHistory.timer=null;
    const snap=noteHistorySnapshotFromDom(noteId);
    if(!snap)return;
    const cur=noteEditHistory.current;
    if(cur&&cur.titulo===snap.titulo&&cur.texto===snap.texto)return;
    if(cur)noteEditHistory.undo.push(cur);
    if(noteEditHistory.undo.length>40)noteEditHistory.undo.shift();
    noteEditHistory.current=snap;
    noteEditHistory.redo=[];
    noteHistoryRefreshActionButtons(noteId);
  },280);
}
function noteHistoryRefreshActionButtons(noteId){
  ensureNotas();
  const n=AppState.data.notas.find(x=>String(x.id)===String(noteId));
  if(!n)return;
  const article=document.querySelector('#screen-notas .keep-note.editing[data-note-id="'+CSS.escape(String(noteId))+'"]');
  if(!article)return;
  const ag=article.querySelector('.keep-action-group');
  if(ag)ag.innerHTML=noteActionButtons(n,true);
}
function noteHistoryApplyState(noteId,state){
  ensureNotas();
  const n=AppState.data.notas.find(x=>String(x.id)===String(noteId));
  if(!n||!state)return;
  noteEditHistory.applying=true;
  n.titulo=String(state.titulo||'');
  n.texto=String(state.texto||'');
  n.updatedAt=nowIso();
  AppState.save();
  noteEditHistory.current={titulo:n.titulo,texto:n.texto};
  if(typeof noteRebuildEditorInPlace==='function') noteRebuildEditorInPlace(noteId,0);
  else renderNotes();
  noteEditHistory.applying=false;
  noteHistoryRefreshActionButtons(noteId);
}
function noteHistoryUndo(noteId,ev){
  if(ev){ev.preventDefault();ev.stopPropagation();}
  if(!noteHistoryCanUndo(noteId))return;
  const cur=noteHistorySnapshotFromDom(noteId)||noteEditHistory.current;
  const prev=noteEditHistory.undo.pop();
  if(!prev)return;
  if(cur)noteEditHistory.redo.push(cur);
  noteHistoryApplyState(noteId,prev);
}
function noteHistoryRedo(noteId,ev){
  if(ev){ev.preventDefault();ev.stopPropagation();}
  if(!noteHistoryCanRedo(noteId))return;
  const cur=noteHistorySnapshotFromDom(noteId)||noteEditHistory.current;
  const next=noteEditHistory.redo.pop();
  if(!next)return;
  if(cur)noteEditHistory.undo.push(cur);
  noteHistoryApplyState(noteId,next);
}

'''

if 'function noteHistoryReset(' not in t:
    t = t.replace('function noteActionButtons(n, editing=false){', hist + 'function noteActionButtons(n, editing=false){', 1)
    print('inserted history helpers')
else:
    print('history helpers already present')

# --- botoes undo/redo no noteActionButtons ---
if 'histBtns' not in t:
    old_save = "  const saveBtn = editing ? `<button class=\"keep-icon keep-save-inline\" type=\"button\" onclick=\"saveInlineNote('${safeId}',event)\" title=\"Salvar\">Salvar</button>` : '';"
    new_save = """  let histBtns='';
  if(editing){
    const canU=typeof noteHistoryCanUndo==='function'&&noteHistoryCanUndo(n.id);
    const canR=typeof noteHistoryCanRedo==='function'&&noteHistoryCanRedo(n.id);
    if(canR){
      histBtns=`<button class=\"keep-icon keep-undo-inline\" type=\"button\" onclick=\"noteHistoryUndo('${safeId}',event)\" title=\"Desfazer\">\u21b6</button><button class=\"keep-icon keep-redo-inline\" type=\"button\" onclick=\"noteHistoryRedo('${safeId}',event)\" title=\"Refazer\">\u21b7</button>`;
    }else if(canU){
      histBtns=`<button class=\"keep-icon keep-undo-inline\" type=\"button\" onclick=\"noteHistoryUndo('${safeId}',event)\" title=\"Desfazer\">\u21b6</button>`;
    }
  }
  const saveBtn = editing ? `<button class=\"keep-icon keep-save-inline\" type=\"button\" onclick=\"saveInlineNote('${safeId}',event)\" title=\"Salvar\">Salvar</button>` : '';"""
    if old_save in t:
        t = t.replace(old_save, new_save, 1)
        print('injected histBtns')
    else:
        print('WARN: saveBtn line not found')

    # prefix return with histBtns
    old_ret = "  return `<button class=\"keep-icon ${n.pinned?'active':''}\" type=\"button\" onclick=\"togglePinNote('${safeId}')\" title=\"Fixar\">📌</button>"
    new_ret = "  return `${histBtns}<button class=\"keep-icon ${n.pinned?'active':''}\" type=\"button\" onclick=\"togglePinNote('${safeId}')\" title=\"Fixar\">📌</button>"
    if old_ret in t and '${histBtns}' not in t:
        t = t.replace(old_ret, new_ret, 1)
        print('prefixed return with histBtns')
    elif '${histBtns}' in t:
        print('histBtns already in return')
    else:
        print('WARN: return line for histBtns not found')
else:
    print('histBtns already present')

# --- oninput do titulo tambem empurra historico ---
t = t.replace(
    "updateNoteInline('${safeId}','titulo',this.value)\"",
    "updateNoteInline('${safeId}','titulo',this.value);noteHistoryMaybePush('${safeId}')\"",
)

# --- CSS overrides ---
css = """
<style id=\"vbeta81-notes-fix\">
#screen-notas .keep-note.editing.collapsed .keep-actions,
#screen-notas .keep-note.editing .keep-actions{display:flex !important;}
#screen-notas .keep-note.editing.collapsed .keep-note-text,
#screen-notas .keep-note.editing.collapsed .keep-note-meta{display:block !important;}
#screen-notas .keep-note.editing{height:auto !important;min-height:0 !important;max-height:none !important;overflow:visible !important;}
#screen-notas .keep-note.editing .keep-check-edit-input{height:auto !important;min-height:28px !important;max-height:none !important;line-height:1.35 !important;overflow:hidden !important;white-space:pre-wrap !important;word-break:break-word !important;}
#screen-notas .keep-note.editing .keep-check-edit-row{height:auto !important;min-height:28px !important;max-height:none !important;overflow:visible !important;align-items:start !important;}
#screen-notas .keep-undo-inline,#screen-notas .keep-redo-inline,#screen-notas .keep-save-inline{display:inline-flex !important;}
</style>
"""
if 'vbeta81-notes-fix' not in t:
    if '</head>' in t:
        t = t.replace('</head>', css + '</head>', 1)
        print('added CSS')
    else:
        t = t + css
        print('appended CSS')
else:
    print('CSS already present')

if t == orig:
    print('NO CHANGES')
    sys.exit(1)
p.write_text(t, encoding='utf-8')
print('OK wrote app.html', len(t))
