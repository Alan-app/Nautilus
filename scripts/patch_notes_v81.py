#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import sys

p = Path('app.html')
t = p.read_text(encoding='utf-8')
orig = t

for v in ("V.Beta.79", "V.Beta.80"):
    t = t.replace("const APP_VERSION = '%s';" % v, "const APP_VERSION = 'V.Beta.81';")

old_resize = (
"function noteResizeChecklistInput(el){\n"
"  if(!el) return;\n"
"  el.style.setProperty('height','28px','important');\n"
"  el.style.setProperty('min-height','28px','important');\n"
"  el.style.setProperty('max-height','28px','important');\n"
"  el.style.setProperty('line-height','28px','important');\n"
"  el.style.setProperty('overflow','hidden','important');\n"
"  const row = el.closest ? el.closest('.keep-check-edit-row') : null;\n"
"  if(row){\n"
"    row.style.setProperty('height','28px','important');\n"
"    row.style.setProperty('min-height','28px','important');\n"
"    row.style.setProperty('max-height','28px','important');\n"
"    row.style.setProperty('overflow','visible','important');\n"
"  }\n"
"}"
)
new_resize = (
"function noteResizeChecklistInput(el){\n"
"  if(!el) return;\n"
"  /* V.Beta.81: cresce com o texto */\n"
"  el.style.setProperty('height','auto','important');\n"
"  el.style.setProperty('min-height','28px','important');\n"
"  el.style.setProperty('max-height','none','important');\n"
"  el.style.setProperty('line-height','1.35','important');\n"
"  el.style.setProperty('overflow','hidden','important');\n"
"  el.style.setProperty('white-space','pre-wrap','important');\n"
"  el.style.setProperty('height', Math.max(28, Math.ceil(el.scrollHeight||28))+'px', 'important');\n"
"  const row = el.closest ? el.closest('.keep-check-edit-row') : null;\n"
"  if(row){\n"
"    const h = Math.max(28, Math.ceil(el.getBoundingClientRect().height||el.scrollHeight||28));\n"
"    row.style.setProperty('height', h+'px', 'important');\n"
"    row.style.setProperty('min-height', h+'px', 'important');\n"
"    row.style.setProperty('max-height', 'none', 'important');\n"
"    row.style.setProperty('overflow', 'visible', 'important');\n"
"  }\n"
"}"
)
if old_resize in t:
    t = t.replace(old_resize, new_resize, 1)
    print('patched noteResizeChecklistInput')
elif 'V.Beta.81: cresce com o texto' in t:
    print('noteResizeChecklistInput already patched')
else:
    print('WARN: noteResizeChecklistInput not found')

if "noteResizeChecklistInput(this)`);" in t:
    t = t.replace(
        "noteSyncRowEmpty(this);noteResizeChecklistInput(this)`);",
        "noteSyncRowEmpty(this);noteAutosizeTextarea(this);noteAutosizeChecklist(this.closest('.keep-check-edit-wrap'));noteHistoryMaybePush('${safeId}')`);",
        1,
    )
    print('patched refresh oninput')

needle = "noteAutosizeChecklist(this.closest('.keep-check-edit-wrap'))\""
repl = "noteAutosizeChecklist(this.closest('.keep-check-edit-wrap'));noteHistoryMaybePush('${safeId}')\""
if needle in t and "noteHistoryMaybePush('${safeId}')\"" not in t:
    t = t.replace(needle, repl)
    print('patched render oninput')

old_bs_start = "  if(key==='Backspace'){\n    const value=String(el.value||''),s=typeof el.selectionStart==='number'?el.selectionStart:value.length,e=typeof el.selectionEnd==='number'?el.selectionEnd:value.length;\n    if(value.length===0||(s===0&&e===0)){"
if old_bs_start in t:
    start = t.find(old_bs_start)
    end_marker = "\n}\n\n\nfunction noteResizeChecklistInput"
    end = t.find(end_marker, start)
    if end < 0:
        end_marker = "\n}\n\nfunction noteResizeChecklistInput"
        end = t.find(end_marker, start)
    if end < 0:
        print('WARN: could not find end of Backspace block')
    else:
        new_bs = (
"  if(key==='Backspace'){\n"
"    const value=String(el.value||'');\n"
"    const s=typeof el.selectionStart==='number'?el.selectionStart:value.length;\n"
"    const e=typeof el.selectionEnd==='number'?el.selectionEnd:value.length;\n"
"    if(s===0&&e===0){\n"
"      ev.preventDefault();ev.stopPropagation();\n"
"      if(!wrap||!currentRow)return;\n"
"      if(String(value).trim()===''){\n"
"        if(wrap.children.length>1){\n"
"          const focusIndex=Math.max(0,idx-1);\n"
"          currentRow.remove();noteRefreshChecklistDom(noteId);noteCommitChecklistDomToText(noteId);noteAutosizeChecklist(wrap);noteHistoryMaybePush(noteId);\n"
"          const target=wrap.querySelector('.keep-check-edit-row[data-line-index="'+focusIndex+'"] .keep-check-edit-input');\n"
"          if(target){target.focus({preventScroll:true});try{const l=String(target.value||'').length;target.setSelectionRange(l,l);}catch(err){}}\n"
"        }\n"
"        return;\n"
"      }\n"
"      const prev=currentRow.previousElementSibling;\n"
"      if(prev&&prev.classList&&prev.classList.contains('keep-check-edit-row')){\n"
"        const prevInp=prev.querySelector('.keep-check-edit-input');\n"
"        if(prevInp){\n"
"          const prevVal=String(prevInp.value||'');\n"
"          const junction=prevVal.length;\n"
"          prevInp.value=prevVal+value;\n"
"          currentRow.remove();\n"
"          noteRefreshChecklistDom(noteId);noteCommitChecklistDomToText(noteId);noteAutosizeChecklist(wrap);noteHistoryMaybePush(noteId);\n"
"          const target=wrap.querySelector('.keep-check-edit-row[data-line-index="'+(idx-1)+'"] .keep-check-edit-input')||prevInp;\n"
"          if(target){target.focus({preventScroll:true});try{target.setSelectionRange(junction,junction);}catch(err){}}\n"
"        }\n"
"      }\n"
"    }\n"
"  }\n"
"}"
        )
        t = t[:start] + new_bs + t[end:]
        print('patched Backspace')
else:
    print('WARN: Backspace start not found')

old_c = "if(n.collapsed){n.collapsed=false;AppState.save();}\n  UI.editingNoteId=id;UI.noteEditLockedHeight=0;UI.noteEditMinHeight=0;"
new_c = old_c + "\n  noteHistoryReset(id, n.titulo, n.texto);"
if old_c in t and 'noteHistoryReset(id, n.titulo, n.texto)' not in t:
    t = t.replace(old_c, new_c, 1)
    print('patched history reset')

old_cls = "article.classList.add('editing');article.onclick=null;"
new_cls = "article.classList.remove('collapsed');article.classList.add('editing');article.onclick=null;"
if "classList.remove('collapsed')" not in t:
    if old_cls in t:
        t = t.replace(old_cls, new_cls, 1)
        print('patched remove collapsed')

hist = '''
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

if 'histBtns' not in t:
    idx = t.find('function noteActionButtons')
    snip = t[idx:idx+1200]
    for line in snip.split('\n'):
        if 'const saveBtn' in line and 'keep-save-inline' in line:
            inject = (
"  let histBtns='';\n"
"  if(editing){\n"
"    const canU=typeof noteHistoryCanUndo==='function'&&noteHistoryCanUndo(n.id);\n"
"    const canR=typeof noteHistoryCanRedo==='function'&&noteHistoryCanRedo(n.id);\n"
"    if(canR){\n"
"      histBtns=`<button class=\"keep-icon keep-undo-inline\" type=\"button\" onclick=\"noteHistoryUndo('${safeId}',event)\" title=\"Desfazer\">\u21b6</button><button class=\"keep-icon keep-redo-inline\" type=\"button\" onclick=\"noteHistoryRedo('${safeId}',event)\" title=\"Refazer\">\u21b7</button>`;\n"
"    }else if(canU){\n"
"      histBtns=`<button class=\"keep-icon keep-undo-inline\" type=\"button\" onclick=\"noteHistoryUndo('${safeId}',event)\" title=\"Desfazer\">\u21b6</button>`;\n"
"    }\n"
"  }\n"
            )
            t = t.replace(line, inject + line, 1)
            print('injected histBtns')
            break
    idx = t.find('function noteActionButtons')
    snip = t[idx:idx+1800]
    for line in snip.split('\n'):
        if line.strip().startswith('return `') and 'togglePinNote' in line and '${histBtns}' not in line:
            t = t.replace(line, line.replace('return `', 'return `${histBtns}', 1), 1)
            print('prefixed return with histBtns')
            break

t = t.replace(
    "updateNoteInline('${safeId}','titulo',this.value)\"",
    "updateNoteInline('${safeId}','titulo',this.value);noteHistoryMaybePush('${safeId}')\"",
)

css = """
<style id="vbeta81-notes-fix">
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
    else:
        t = t + css
    print('added CSS')

if t == orig:
    print('NO CHANGES')
    sys.exit(1)
p.write_text(t, encoding='utf-8')
print('OK wrote app.html', len(t))
