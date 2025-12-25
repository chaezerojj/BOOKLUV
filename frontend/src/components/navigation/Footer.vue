<template>
  <footer class="site-footer">
    <div class="container">
      <div class="left">
        <div class="logo">Bookluv</div>
        <div class="copyright">© {{ year }} Bookluv</div>
      </div>
      <nav class="links">
        <a href="/about">About</a>
        <a href="/terms">Terms</a>
        <a href="/privacy">Privacy</a>
        <a href="/contact">Contact</a>
      </nav>
      <div class="right">
        <a class="social" href="https://github.com" target="_blank" rel="noopener">GitHub</a>
      </div>
    </div>
  </footer>
</template>

<script setup>
const year = new Date().getFullYear();
</script>

<style scoped>
.site-footer {
  --footer-height: 96px;
  height: var(--footer-height);
  background: #f7f7f7;
  border-top: 1px solid #e6e6e6;
  color: #616161;
  display: flex;
  align-items: center;
  width: 100%;
  box-sizing: border-box;
  margin-top: 32px;
}

.container {
  width: 1300px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.logo {
  font-weight: 700;
  font-size: 18px;
  color: #1f2328;
}

.links a {
  margin: 0 12px;
  color: #616161;
  text-decoration: none;
  font-size: 14px;
}

.links a:hover {
  text-decoration: underline;
}

.right .social {
  color: #616161;
  text-decoration: none;
  margin-left: 8px;
}

@media (max-width: 1400px) {
  .container {
    width: 100%;
    padding: 0 16px;
    box-sizing: border-box;
  }
}

@media (max-width: 600px) {
  .container {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
    height: auto;
    padding: 12px;
  }

  .site-footer {
    height: auto;
    padding: 12px 0;
  }

  .links {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
}
</style>
