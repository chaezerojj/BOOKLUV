export function initGA() {
  const id = import.meta.env.VITE_GA_MEASUREMENT_ID;
  if (!id) return;
  if (window.gtag) return;

  const s = document.createElement("script");
  s.async = true;
  s.src = `https://www.googletagmanager.com/gtag/js?id=${id}`;
  document.head.appendChild(s);

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = gtag;

  gtag("js", new Date());

  // 자동 페이지뷰 끄고 라우터에서 직접 쏜다
  gtag("config", id, { send_page_view: false });
}

export function trackPageView(path) {
  const id = import.meta.env.VITE_GA_MEASUREMENT_ID;
  if (!id || !window.gtag) return;

  window.gtag("event", "page_view", {
    page_path: path,
    page_location: window.location.href,
    page_title: document.title,
  });
}
