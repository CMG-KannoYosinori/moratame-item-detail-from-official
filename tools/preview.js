// tools/preview.html の動き: ?src= の HTML を、?w= の幅の iframe に表示し、高さを中身に合わせる
(() => {
  const q = new URLSearchParams(location.search);
  const f = document.getElementById('f');
  f.width = Number(q.get('w') || 375);
  f.height = 900;
  f.addEventListener('load', () => {
    const fit = () => { f.height = f.contentDocument.documentElement.scrollHeight; };
    fit();
    setTimeout(fit, 1000); // 画像やフォントの読み込み後にもう一度合わせる
  });
  f.src = q.get('src') || '';
})();
