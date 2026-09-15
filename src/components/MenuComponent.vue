<template>
  <header class="cabecera">
    <router-link class="brand" to="/"><span class="brand-mark">☀</span><span>Santa Marta<br><strong>Segura</strong></span></router-link>
    <nav class="menu" aria-label="Navegación principal">
      <router-link to="/">Inicio</router-link><router-link to="/mapview">Lugares</router-link><a href="#seguridad">Seguridad</a><a class="emergency" href="tel:123">Emergencias</a>
    </nav>
  </header>
</template>
<script>export default { name: 'MenuComponent' }</script>
<style scoped>
.cabecera { min-height: 76px; display: flex; align-items: center; justify-content: space-between; padding: 0 7%; background: #073b4c; color: white; }.brand { display: flex; align-items: center; gap: 10px; color: white; text-decoration: none; font-size: .9rem; line-height: 1; letter-spacing: .04em; }.brand strong { color: #ffd166; font-size: 1.1rem; }.brand-mark { width: 38px; height: 38px; display: grid; place-items: center; border-radius: 50%; background: #ffd166; color: #073b4c; font-size: 1.6rem; }.menu { display: flex; align-items: center; gap: 1.5rem; }.menu a { color: #eaf7f5; text-decoration: none; font-size: .9rem; font-weight: 600; }.menu a:hover, .menu a.router-link-exact-active { color: #ffd166; }.menu .emergency { padding: .55rem .85rem; border: 1px solid #ef476f; border-radius: 99px; color: #fff; } @media (max-width: 680px) { .cabecera { padding: 0 5%; }.menu { gap: .8rem; }.menu a:nth-child(3), .menu .emergency { display: none; } }
</style>
