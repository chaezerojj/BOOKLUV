import { onCLS, onINP, onLCP } from "web-vitals";

function sendToGA(metric) {
  if (!window.gtag) return;

  const value = 
    metric.name === "CLS" ? Math.round(metric.value * 1000) : Math.round(metric.value);

  window.gtag("event", metric.name, {
    value,
    metric_id: metric.id,
    metric_rating: metric.rating,
    non_interaction: true,
    page_path: window.location.pathname,
  });
}

export function initWebVitals() {
  onCLS(sendToGA);
  onLCP(sendToGA);
  onINP(sendToGA);
}
