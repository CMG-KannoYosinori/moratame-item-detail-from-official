// use_figma でカンプを組むときの共通の関数。スクリプトの先頭に貼って使う。
// 99901 サポートミートで使ったもの。H（画像の imageHash）と SV（素材ページの SVG の node ID）は案件ごとに差し替える。

const F = 'Zen Kaku Gothic New'; // ブランドの書体。listAvailableFontsAsync で使えるか確かめてから決める
await Promise.all(['Regular', 'Medium', 'Bold', 'Black'].map(s => figma.loadFontAsync({ family: F, style: s })));

const hex = h => ({ r: parseInt(h.slice(0, 2), 16) / 255, g: parseInt(h.slice(2, 4), 16) / 255, b: parseInt(h.slice(4, 6), 16) / 255 });
const sol = (h, o) => o == null ? { type: 'SOLID', color: hex(h) } : { type: 'SOLID', color: hex(h), opacity: o };

// ブランドの色（# なしの6桁）
const COL = { text: '626262', dark: '444444', white: 'ffffff', border: 'cccccc' };
// upload_assets の結果の imageHash
const H = { /* box: '5e00…', */ };
// 素材ページに上げた SVG の node ID
const SV = { /* intro1: '4:18', */ };

// テキスト。w を渡すと幅を固定して折り返す
function T(s, o = {}) {
  const t = figma.createText();
  t.fontName = { family: F, style: o.wt || 'Regular' };
  t.characters = s;
  t.fontSize = o.size || 16;
  t.fills = [sol(o.color || COL.text)];
  t.textAlignHorizontal = o.align || 'LEFT';
  t.lineHeight = { unit: 'PERCENT', value: (o.lh || 1.7) * 100 };
  t.letterSpacing = { unit: 'PERCENT', value: o.ls == null ? 5 : o.ls };
  if (o.w) { t.textAutoResize = 'HEIGHT'; t.resize(o.w, t.height); } else { t.textAutoResize = 'WIDTH_AND_HEIGHT'; }
  return t;
}

// オートレイアウトの枠。w を渡すと幅を固定し、高さは中身に合わせる
// pad は [上下, 左右] か [上, 右, 下, 左]
function AL(dir, o = {}) {
  const f = figma.createAutoLayout(dir);
  f.fills = o.fill ? [sol(o.fill)] : [];
  if (o.name) f.name = o.name;
  f.itemSpacing = o.gap || 0;
  const p = o.pad || [0, 0];
  const [pt, pr, pb, pl] = p.length === 2 ? [p[0], p[1], p[0], p[1]] : p;
  f.paddingTop = pt; f.paddingRight = pr; f.paddingBottom = pb; f.paddingLeft = pl;
  if (o.r) f.cornerRadius = o.r;
  if (o.center) f.counterAxisAlignItems = 'CENTER';
  if (o.cross) f.counterAxisAlignItems = o.cross;
  if (o.main) f.primaryAxisAlignItems = o.main;
  if (o.w) {
    f.resize(o.w, Math.max(f.height, 1));
    if (dir === 'VERTICAL') f.primaryAxisSizingMode = 'AUTO'; else f.counterAxisSizingMode = 'AUTO';
  }
  return f;
}

// 画像（upload_assets で上げた imageHash を塗りに使う）。レイヤー名は img/〜
function IMG(k, w, h, name, mode) {
  const r = figma.createRectangle();
  r.resize(Math.round(w), Math.round(h));
  r.fills = [{ type: 'IMAGE', imageHash: H[k], scaleMode: mode || 'FIT' }];
  r.name = 'img/' + name;
  return r;
}

// 素材ページの SVG を複製して、幅または高さに合わせて拡大縮小する
async function svgW(k, w) { const c = (await figma.getNodeByIdAsync(SV[k])).clone(); c.rescale(w / c.width); c.name = 'svg/' + k; return c; }
async function svgH(k, h) { const c = (await figma.getNodeByIdAsync(SV[k])).clone(); c.rescale(h / c.height); c.name = 'svg/' + k; return c; }

// 三角の矢印など、記号はフォントによって絵文字で表示されることがある（例: ▶）。図形は SVG で作る
function triangle(size, color) {
  return figma.createNodeFromSvg(`<svg width="${size}" height="${Math.round(size * 1.2)}" viewBox="0 0 16 20" xmlns="http://www.w3.org/2000/svg"><path d="M0 0L16 10L0 20Z" fill="#${color}"/></svg>`);
}

// カンプの外枠（PC 640 / SP 375。1px のボーダー込み）。build(true) と build(false) の中で使う
// const root = AL('VERTICAL', { name: `${ID} PC 640`, fill: COL.white, pad: [1, 1, 1, 1], w: 640 });
// root.strokes = [sol(COL.border)]; root.strokeWeight = 1; root.strokeAlign = 'INSIDE'; root.clipsContent = true;
// セクション: AL('VERTICAL', { name: 'B02 リード', fill: 背景色, gap, pad: [上, 左右, 下, 左右], center: true, w: W - 2 }) を root に追加
