// tools/preview.html の動き:
//   ?src= の HTML を、?w= の幅の iframe に表示し、高さを中身に合わせる。
//   ?y= と ?h= を付けると、上から y px の位置から h px だけを見せる（tools/screenshot.py が縦に分けて撮るのに使う）。
//   ページの高さは body の data-height に書く（tools/screenshot.py が --dump-dom で読む）。
(() => {
  const q = new URLSearchParams(location.search);
  const f = document.getElementById('f');
  const w = Number(q.get('w') || 375);
  const y = Number(q.get('y') || 0);
  const h = q.get('h') ? Number(q.get('h')) : null;
  f.width = w;
  f.height = 900;
  if (h) {
    // 見せる範囲だけの枠を作り、その中で iframe をずらす
    const box = document.createElement('div');
    box.style.cssText = `width:${w}px;height:${h}px;overflow:hidden;`;
    f.parentNode.insertBefore(box, f);
    box.appendChild(f);
    f.style.marginTop = `-${y}px`;
  }
  f.addEventListener('load', () => {
    const fit = () => {
      const ph = f.contentDocument.documentElement.scrollHeight;
      f.height = ph;
      document.body.dataset.height = ph;
    };
    fit();
    setTimeout(fit, 1000); // 画像やフォントの読み込み後にもう一度合わせる
  });
  f.src = q.get('src') || '';
})();
