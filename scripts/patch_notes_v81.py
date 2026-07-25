#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import sys

p = Path('app.html')
t = p.read_text(encoding='utf-8')
orig = t

# APP_VERSION
for v in ("V.Beta.79", "V.Beta.80"):
    t = t.replace(f"const APP_VERSION = '{v}';", "const APP_VERSION = 'V.Beta.81';")

# 1) noteResizeChecklistInput grow
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

# 2) noteRefreshChecklistDom oninput
old1 = "input.setAttribute('oninput',`handleNoteEqualsCalc(this);updateChecklistEditLine('${safeId}',${idx},this.value);noteSyncRowEmpty(this);noteResizeChecklistInput(this)`);"
new1 = "input.setAttribute('oninput',`handleNoteEqualsCalc(this);updateChecklistEditLine('${safeId}',${idx},this.value);noteSyncRowEmpty(this);noteAutosizeTextarea(this);noteAutosizeChecklist(this.closest('.keep-check-edit-wrap'));noteHistoryMaybePush('${safeId}')`);"
if old1 in t:
    t = t.replace(old1, new1, 1)
    print('patched noteRefreshChecklistDom oninput')
else:
    old1b = "input.setAttribute('oninput',`handleNoteEqualsCalc(this);updateChecklistEditLine('${safeId}',${idx},this.value);noteSyncRowEmpty(this);noteAutosizeTextarea(this);noteAutosizeChecklist(this.closest('.keep-check-edit-wrap'))`);"
    if old1b in t:
        t = t.replace(old1b, new1, 1)
        print('patched noteRefreshChecklistDom oninput (alt)')

# renderChecklistEditRows oninput
old_ri = 'oninput="handleNoteEqualsCalc(this);updateChecklistEditLine('${safeId}',${idx},this.value);noteSyncRowEmpty(this);noteAutosizeTextarea(this);noteAutosizeChecklist(this.closest('.keep-check-edit-wrap'))"'
new_ri = 'oninput="handleNoteEqualsCalc(this);updateChecklistEditLine('${safeId}',${idx},this.value);noteSyncRowEmpty(this);noteAutosizeTextarea(this);noteAutosizeChecklist(this.closest('.keep-check-edit-wrap'));noteHistoryMaybePush('${safeId}')"'
c = t.count(old_ri)
if c:
    t = t.replace(old_ri, new_ri)
    print(f'patched render oninput x{c}')

# 3) Backspace merge
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
    print('patched Backspace')
else:
    print('WARN: Backspace block not found')

# 4) editNote: history reset + remove collapsed class
t = t.replace(
    "if(n.collapsed){n.collapsed=false;AppState.save();}\n  UI.editingNoteId=id;UI.noteEditLockedHeight=0;UI.noteEditMinHeight=0;",
    "if(n.collapsed){n.collapsed=false;AppState.save();}\n  UI.editingNoteId=id;UI.noteEditLockedHeight=0;UI.noteEditMinHeight=0;\n  noteHistoryReset(id, n.titulo, n.texto);",
    1,
)
t = t.replace(
    "article.classList.add('editing');article.onclick=null;article.setAttribute('onclick','event.stopPropagation()');",
    "article.classList.remove('collapsed');article.classList.add('editing');article.onclick=null;article.setAttribute('onclick','event.stopPropagation()');",
    1,
)
print('patched editNote')

# 5) noteActionButtons undo/redo
old_save = """  const saveBtn = editing ? `<button class="keep-icon keep-save-inline" type="button" onclick="saveInlineNote('${safeId}',event)" title="Salvar">Salvar</button>` : '';
  return `<button class="keep-icon ${n.pinned?'active':''}" type="button" onclick="togglePinNote('${safeId}')" title="Fixar">\U0001f4cc</button>"""
# Use emoji as in file
old_save = "  const saveBtn = editing ? `<button class=\"keep-icon keep-save-inline\" type=\"button\" onclick=\"saveInlineNote('${safeId}',event)\" title=\"Salvar\">Salvar</button>` : '';\n  return `<button class=\"keep-icon ${n.pinned?'active':''}\" type=\"button\" onclick=\"togglePinNote('${safeId}')\" title=\"Fixar\">\U0001f4cc</button>"

# Simpler match without emoji issues
marker = "const saveBtn = editing ? `<button class=\"keep-icon keep-save-inline\" type=\"button\" onclick=\"saveInlineNote('${safeId}',event)\" title=\"Salvar\">Salvar</button>` : '';"
if marker not in t:
    # try single-quoted style from source - the file uses template literals
    marker = "const saveBtn = editing ? `<button class=\"keep-icon keep-save-inline\" type=\"button\" onclick=\"saveInlineNote('${safeId}',event)\" title=\"Salvar\">Salvar</button>` : '';"
# Actual from file read:
marker = 'const saveBtn = editing ? `<button class="keep-icon keep-save-inline" type="button" onclick="saveInlineNote(\'${safeId}\',event)" title="Salvar">Salvar</button>` : \'\';'
# From tool output line 7615:
marker = "const saveBtn = editing ? `<button class=\"keep-icon keep-save-inline\" type=\"button\" onclick=\"saveInlineNote('${safeId}',event)\" title=\"Salvar\">Salvar</button>` : '';"

# Read exact bytes from file around noteActionButtons
idx = t.find('function noteActionButtons')
if idx < 0:
    print('FATAL: noteActionButtons not found')
    sys.exit(1)
snip = t[idx:idx+900]
print('SNIP:', repr(snip[:400]))

old_btn_line = None
for line in snip.split('\n'):
    if 'saveBtn' in line and 'keep-save-inline' in line:
        old_btn_line = line
        break
if not old_btn_line:
    print('WARN: saveBtn line not found')
else:
    new_btn_block = """  let histBtns='';
  if(editing){
    const canU=typeof noteHistoryCanUndo==='function'&&noteHistoryCanUndo(n.id);
    const canR=typeof noteHistoryCanRedo==='function'&&noteHistoryCanRedo(n.id);
    if(canR){
      histBtns=`<button class="keep-icon keep-undo-inline" type="button" onclick="noteHistoryUndo('${safeId}',event)" title="Desfazer">\u21b6</button><button class="keep-icon keep-redo-inline" type="button" onclick="noteHistoryRedo('${safeId}',event)" title="Refazer">\u21b7</button>`;
    }else if(canU){
      histBtns=`<button class="keep-icon keep-undo-inline" type="button" onclick="noteHistoryUndo('${safeId}',event)" title="Desfazer">\u21b6</button>`;
    }
  }
""" + old_btn_line + "\n"
    # inject before saveBtn line once
    if 'histBtns' not in t[idx:idx+1200]:
        t = t.replace(old_btn_line, new_btn_block.strip('\n'), 1)
        # also prefix return with histBtns
        ret_marker = "return `<button class=\"keep-icon ${n.pinned?'active':''}\""
        # find return in noteActionButtons
        idx2 = t.find('function noteActionButtons')
        chunk = t[idx2:idx2+1500]
        for line in chunk.split('\n'):
            if line.strip().startswith('return `') and 'togglePinNote' in line:
                if '${histBtns}' not in line:
                    new_line = line.replace('return `', 'return `${histBtns}', 1)
                    t = t.replace(line, new_line, 1)
                    print('prefixed histBtns on return')
                break
        print('patched saveBtn block')

# 6) History helpers before noteActionButtons
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

# title oninput history
t = t.replace(
    "oninput=\"handleNoteEqualsCalc(this);updateNoteInline('${safeId}','titulo',this.value)\"",
    "oninput=\"handleNoteEqualsCalc(this);updateNoteInline('${safeId}','titulo',this.value);noteHistoryMaybePush('${safeId}')\"",
)

# CSS
css = '''
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
'''
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
