// ワイヤーフレームの共通スクリプト（全案件で共通）。
// 各案件の wireframe.html の <template id="lp"> にあるブロックを PC/SP の2つのフレームに表示し、
// blocks.md を読み込んで、チェック・並び順・メモ・商品の区分を反映する。
// tools/wireframe-server.py で開いたときは、画面で選んだ内容を blocks.md に保存できる。
// 文字列の中の閉じタグは <\/ と書く（Live Server が body の閉じタグの前にスクリプトを差し込むため）。
(() => {
const BASE = new URL('.', document.currentScript.src).href; // このスクリプトと同じフォルダ（frame.css の場所）
const tpl = document.getElementById('lp').innerHTML;
const frames = [document.getElementById('pc'), document.getElementById('sp')];
const toggle = document.getElementById('toggle-optional');
const status = document.getElementById('status');
const saveBtn = document.getElementById('save');
const copyBtn = document.getElementById('copy');
const dirtyEl = document.getElementById('dirty');
const out = document.getElementById('out');
const ROW = /^\|\s*\[([ xX])\]\s*\|\s*(B\d+)\s*\|(.*)\|\s*$/;
const PROW = /^\|\s*(対象|紹介|載せない)\s*\|\s*(P\d+)\s*\|(.*)\|\s*$/;
const ROLES = [['対象', '対象（今回試せる）'], ['紹介', '紹介のみ'], ['載せない', '載せない']];

let mdText = null;   // 読み込んだときの blocks.md
let canSave = false; // tools/wireframe-server.py で開いているときだけ true
let state = [];      // ブロック [{ id, used, memo, req, open }]（並び順どおり）
let products = [];   // 商品 [{ id, role, role0, name }]（blocks.md の「商品」の表の順）
let dirty = false;

const fit = (f) => { f.style.height = f.contentDocument.documentElement.scrollHeight + 'px'; };
const setStatus = (text, kind) => { status.textContent = text; status.className = 'status' + (kind ? ' is-' + kind : ''); };
const tagId = (el) => { const t = el.querySelector('.tag'); const m = t && t.textContent.match(/B\d+/); return m ? m[0] : null; };

// blocks.md の表から「| [x] | B01 | ... | メモ |」の行を読む。並び順も md のとおり。
const parseBlocks = (md) => md.split('\n').map((line) => {
  const m = line.match(ROW);
  if (!m) return null;
  const cells = m[3].split('|').map((c) => c.trim());
  return { id: m[2], used: m[1].toLowerCase() === 'x', memo: cells[cells.length - 1] || '' };
}).filter(Boolean);

// blocks.md の「商品」の表から「| 対象 | P1 | 商品名 | ... |」の行を読む
const parseProducts = (md) => md.split('\n').map((line) => {
  const m = line.match(PROW);
  return m ? { id: m[2], role: m[1] } : null;
}).filter(Boolean);

// 選んだ内容で blocks.md を作り直す。表の行だけを差し替え、ほかの部分はそのまま残す。
const cleanMemo = (s) => s.replace(/\r?\n/g, ' ').replace(/\|/g, '｜').trim();
const buildMd = () => {
  if (mdText === null) {
    return state.map((s) => (s.used ? '[x] ' : '[ ] ') + s.id + (s.memo ? ' メモ: ' + cleanMemo(s.memo) : '')).join('\n')
      + '\n\n' + products.map((x) => x.role + ' ' + x.id + ' ' + x.name).join('\n') + '\n';
  }
  const eol = mdText.includes('\r\n') ? '\r\n' : '\n';
  const lines = mdText.split(/\r?\n/);
  const rowAt = {};
  lines.forEach((line, i) => { const m = line.match(ROW); if (m) rowAt[m[2]] = i; });
  const idx = Object.values(rowAt);
  const first = Math.min(...idx); const last = Math.max(...idx);
  const rows = state.filter((s) => s.id in rowAt).map((s) => {
    const line = lines[rowAt[s.id]];
    const [orig] = parseBlocks(line);
    const memo = cleanMemo(s.memo);
    if (orig.used === s.used && orig.memo === memo) return line; // 変えていない行はそのまま
    const cells = line.trim().slice(1, -1).split('|');
    cells[0] = s.used ? ' [x] ' : ' [ ] ';
    cells[cells.length - 1] = memo ? ' ' + memo + ' ' : ' ';
    return '|' + cells.join('|') + '|';
  });
  const result = [...lines.slice(0, first), ...rows, ...lines.slice(last + 1)];
  // 商品の表は「区分」の列だけを書き換える
  return result.map((line) => {
    const m = line.match(PROW); if (!m) return line;
    const x = products.find((y) => y.id === m[2]);
    if (!x || x.role === m[1]) return line;
    const cells = line.trim().slice(1, -1).split('|');
    cells[0] = ' ' + x.role + ' ';
    return '|' + cells.join('|') + '|';
  }).join(eol);
};

// 必須ブロックを外すのに、理由のメモがない（空、または外す前からあったメモのまま）
const needsReason = (s) => s.req && !s.used && (!s.memo.trim() || (s.used0 && s.memo.trim() === s.memo0));
const warnings = () => {
  const w = [];
  const req = state.filter(needsReason);
  if (req.length) w.push('必須のブロック ' + req.map((s) => s.id).join('・') + ' を外すときは、メモに外す理由を書き足してください');
  if (products.length && !products.some((x) => x.role === '対象')) w.push('対象商品（今回試せる商品）を1つ以上選んでください');
  return w;
};
const roleOrder = (r) => ROLES.findIndex(([v]) => v === r);

// 状態を2つのフレームと上部の表示に反映する
const render = () => {
  frames.forEach((f) => {
    const doc = f.contentDocument;
    const lp = doc.querySelector('.lp');
    const firstSys = lp.querySelector('.blk.sys');
    const byId = {};
    lp.querySelectorAll('.blk').forEach((el) => { const id = tagId(el); if (id) byId[id] = el; });
    state.forEach((s, i) => {
      const el = byId[s.id]; if (!el) return;
      el.classList.toggle('is-unused', !s.used);
      el.classList.toggle('is-warn', needsReason(s));
      el.querySelector('.tag input').checked = s.used;
      el.querySelector('[data-act="up"]').disabled = i === 0;
      el.querySelector('[data-act="down"]').disabled = i === state.length - 1;
      el.querySelector('[data-act="memo"]').classList.toggle('is-on', !!s.memo.trim());
      const memo = el.querySelector('.memo');
      memo.classList.toggle('is-shown', s.open || !!s.memo.trim());
      const ta = memo.querySelector('textarea');
      if (doc.activeElement !== ta && ta.value !== s.memo) ta.value = s.memo;
    });
    // 商品カード: 区分の反映と、対象 → 紹介 → 載せない の順への並べ替え
    const wrap = lp.querySelector('.prods');
    if (wrap) {
      const cards = {};
      wrap.querySelectorAll('.prod').forEach((c) => { cards[c.dataset.product] = c; });
      const sorted = [...products].sort((a, b) => roleOrder(a.role) - roleOrder(b.role));
      sorted.forEach((x) => {
        const c = cards[x.id]; if (!c) return;
        c.classList.toggle('is-target', x.role === '対象');
        c.classList.toggle('is-unused', x.role === '載せない');
        c.querySelector('.pctl select').value = x.role;
      });
      const nowP = [...wrap.querySelectorAll('.prod')].map((c) => c.dataset.product).join();
      if (nowP !== sorted.map((x) => x.id).join()) sorted.forEach((x) => cards[x.id] && wrap.append(cards[x.id]));
    }
    // 並び順が変わったときだけ動かす（動かすと入力中のメモからフォーカスが外れるため）
    const now = [...lp.querySelectorAll('.blk:not(.sys)')].map(tagId).join();
    if (now !== state.map((s) => s.id).join()) state.forEach((s) => byId[s.id] && lp.insertBefore(byId[s.id], firstSys));
    doc.body.classList.toggle('hide-unused', !toggle.checked);
    fit(f);
  });
  const warn = warnings();
  dirtyEl.textContent = warn.length ? warn.join('。') : dirty ? '保存していない変更があります' : '';
  saveBtn.disabled = !canSave || !dirty || warn.length > 0;
};

const change = (fn) => { fn(); dirty = true; render(); };

// 各ブロックのタグに、チェックボックス・↑↓・メモのボタンを付ける
const setupControls = (f) => {
  const doc = f.contentDocument;
  doc.querySelectorAll('.blk').forEach((el) => {
    const id = tagId(el); if (!id) return;
    const s = state.find((x) => x.id === id); if (!s) return;
    const tag = el.querySelector('.tag');
    const label = doc.createElement('label');
    const cb = doc.createElement('input'); cb.type = 'checkbox'; cb.title = '使う';
    label.append(cb, ...tag.childNodes);
    tag.append(label);
    const btn = (act, text, title) => { const b = doc.createElement('button'); b.type = 'button'; b.dataset.act = act; b.textContent = text; b.title = title; tag.append(b); return b; };
    btn('up', '↑', '上へ').addEventListener('click', () => change(() => { const i = state.indexOf(s); [state[i - 1], state[i]] = [state[i], state[i - 1]]; }));
    btn('down', '↓', '下へ').addEventListener('click', () => change(() => { const i = state.indexOf(s); [state[i + 1], state[i]] = [state[i], state[i + 1]]; }));
    btn('memo', 'メモ', 'メモを書く').addEventListener('click', () => {
      s.open = !(s.open || s.memo.trim()); render();
      if (s.open) el.querySelector('.memo textarea').focus();
    });
    cb.addEventListener('change', () => change(() => { s.used = cb.checked; }));

    const memo = doc.createElement('div'); memo.className = 'memo';
    const ta = doc.createElement('textarea'); ta.placeholder = 'メモ（文言の直し・指示・外す理由など）';
    ta.addEventListener('input', () => change(() => { s.memo = ta.value; }));
    memo.append(ta);
    tag.after(memo);
  });
  // 商品カードに区分のセレクトを付ける
  doc.querySelectorAll('.prod').forEach((c) => {
    const x = products.find((y) => y.id === c.dataset.product); if (!x) return;
    const ctl = doc.createElement('label'); ctl.className = 'pctl'; ctl.textContent = x.id;
    const sel = doc.createElement('select');
    ROLES.forEach(([v, t]) => { const o = doc.createElement('option'); o.value = v; o.textContent = t; sel.append(o); });
    sel.addEventListener('change', () => change(() => { x.role = sel.value; }));
    ctl.append(sel);
    c.prepend(ctl);
  });
  doc.addEventListener('keydown', onKey);
  doc.querySelectorAll('details').forEach((d) => d.addEventListener('toggle', () => fit(f)));
};

const usedList = () => state.filter((s) => s.used).map((s) => s.id).join(' → ');
const prodList = () => ROLES.slice(0, 2).map(([v]) => v + ': ' + (products.filter((x) => x.role === v).map((x) => x.name).join('、') || 'なし')).join(' ／ ');
const summary = () => '使うブロック ' + state.filter((s) => s.used).length + '個: ' + usedList() + (products.length ? '。商品 ' + prodList() : '');

const save = async () => {
  if (saveBtn.disabled) return;
  try {
    const cur = await fetch('blocks.md', { cache: 'no-store' }).then((r) => r.text());
    if (cur !== mdText) {
      setStatus('blocks.md がこのページを開いた後に書き換えられています。上書きしないよう保存を止めました。ページを再読み込みしてから選び直してください。', 'error');
      return;
    }
    const text = buildMd();
    const r = await fetch('blocks.md', { method: 'PUT', headers: { 'Content-Type': 'text/markdown; charset=utf-8' }, body: text });
    if (!r.ok) throw new Error(r.status);
    mdText = text; dirty = false;
    state.forEach((s) => { s.open = false; s.used0 = s.used; s.memo0 = cleanMemo(s.memo); });
    products.forEach((x) => { x.role0 = x.role; });
    render();
    setStatus('blocks.md に保存しました（' + new Date().toLocaleTimeString() + '）。' + summary(), 'ok');
  } catch (e) {
    setStatus('保存できませんでした（' + e.message + '）。サーバー（tools/wireframe-server.py）が止まっていないか確認してください。', 'error');
  }
};

const copy = async () => {
  const text = buildMd();
  out.hidden = false; out.value = text; out.select();
  try {
    await navigator.clipboard.writeText(text);
    setStatus(mdText === null
      ? '選んだ結果をコピーしました。Claude との会話に貼り付けてください。'
      : 'blocks.md の新しい内容をコピーしました。blocks.md の中身をすべて置き換えて貼り付けるか、Claude との会話に貼り付けてください。', 'ok');
  } catch (e) {
    setStatus('自動でコピーできませんでした。下の欄の内容を選んでコピーしてください。', 'error');
  }
};

function onKey(e) {
  if ((e.metaKey || e.ctrlKey) && e.key === 's') { e.preventDefault(); if (canSave) save(); else copy(); }
}

const mdPromise = fetch('blocks.md', { cache: 'no-store' })
  .then((r) => { if (!r.ok) throw new Error(r.status); canSave = r.headers.get('X-Wireframe-Save') === '1'; return r.text(); })
  .then((t) => { const p = parseBlocks(t); if (p.length) mdText = t; p.products = parseProducts(t); return p; })
  .catch(() => null);

const loaded = frames.map((f) => new Promise((resolve) => {
  f.addEventListener('load', resolve, { once: true });
  f.srcdoc = '<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><link rel="stylesheet" href="' + BASE + 'frame.css"><\/head><body>' + tpl + '<\/body><\/html>';
}));

Promise.all([mdPromise, ...loaded]).then(([parsed]) => {
  const doc = frames[0].contentDocument;
  const els = [...doc.querySelectorAll('.blk')].filter(tagId);
  const isReq = (id) => { const el = els.find((x) => tagId(x) === id); return !!el && el.querySelector('.tag').classList.contains('tag--req'); };
  if (parsed && parsed.length) {
    state = parsed.map((b) => ({ ...b, req: isReq(b.id), open: false, used0: b.used, memo0: b.memo }));
  } else {
    // 読めないとき（ファイルを直接開いた場合など）は、最初のおすすめ（任意以外を使う）で表示する
    state = els.filter((el) => !el.classList.contains('sys')).map((el) => ({ id: tagId(el), used: !el.querySelector('.tag').classList.contains('tag--opt'), memo: '', req: isReq(tagId(el)), open: false, used0: true, memo0: '' }));
  }
  // 商品: blocks.md の表がなければ、ワイヤーフレームの最初の区分（data-default）を使う
  const cardEls = [...doc.querySelectorAll('.prod')];
  const nameOf = (id) => { const c = cardEls.find((e) => e.dataset.product === id); return c ? c.querySelector('h3').textContent : id; };
  const fromMd = (parsed && parsed.products) || [];
  products = (fromMd.length ? fromMd : cardEls.map((c) => ({ id: c.dataset.product, role: c.dataset.default || '紹介' })))
    .map((x) => ({ ...x, role0: x.role, name: nameOf(x.id) }));
  frames.forEach(setupControls);
  render();

  if (canSave) {
    setStatus('blocks.md を読み込みました。' + summary());
  } else {
    saveBtn.hidden = true; copyBtn.hidden = false;
    setStatus(mdText !== null
      ? 'このサーバーでは blocks.md に保存できません（Live Server など）。保存したいときは python3 tools/wireframe-server.py で開いてください。選んだ結果は「選んだ結果をコピー」で取り出せます。'
      : 'blocks.md を読み込めませんでした。最初のおすすめで表示しています。python3 tools/wireframe-server.py を起動して、表示された URL で開いてください。', mdText !== null ? '' : 'error');
  }
});

saveBtn.addEventListener('click', save);
copyBtn.addEventListener('click', copy);
document.addEventListener('keydown', onKey);
toggle.addEventListener('change', render);
window.addEventListener('beforeunload', (e) => { if (dirty) { e.preventDefault(); e.returnValue = ''; } });
})();
