<template>
  <div class="home">
    <MenuComponent></MenuComponent>

    <section class="search-section">
      <input
        type="text"
        class="search-input"
        placeholder="🔎 Buscar un lugar..."
        v-model="busqueda"
      >
    </section>

    <section class="quick-access">
      <div class="access-btn" v-for="acceso in accesosRapidos" :key="acceso.etiqueta">
        <span class="access-icon">{{ acceso.icono }}</span>
        <span class="access-label">{{ acceso.etiqueta }}</span>
      </div>
    </section>

    <section class="recommended">
      <h2 class="recommended-title">🌴 Recomendado para ti</h2>
      <article class="content-card" v-if="lugaresFiltrados.length > 0">
        <CardComponent
          v-for="lugar in lugaresFiltrados"
          :key="lugar.name"
          :imagen="require(`../assets/${lugar.nameImage}`)"
          :nombre="lugar.name"
          :parrafo="lugar.parragraf"
        ></CardComponent>
      </article>
      <p class="no-results" v-else>
        No se encontraron lugares que coincidan con "{{ busqueda }}".
      </p>
    </section>
  </div>
</template>

<script>

export default {
  name: 'HomeView',
  data(){
    return{
      busqueda: '',
      accesosRapidos: [
        { icono: "🗺️", etiqueta: "Explorar" },
        { icono: "🛡️", etiqueta: "Seguridad" },
        { icono: "💰", etiqueta: "Presupuesto" },
        { icono: "📅", etiqueta: "Itinerario" },
        { icono: "🚕", etiqueta: "Transporte" },
        { icono: "🚨", etiqueta: "Emergencia" }
      ],
      recomendados: [
        {
          nameImage:  "playa blanca.png",
          name: "Playa Blanca",
          parragraf: "Ideal para descansar en pareja, a pocos minutos del centro."
        },
        {
          nameImage:  "parque tayrona.png",
          name: "Parque Tayrona",
          parragraf: "Naturaleza y senderismo. Lleva agua y protector solar."
        },
        {
          nameImage:  "centro historico.png",
          name: "Centro Histórico",
          parragraf: "Gastronomía típica y cultura samaria en un mismo recorrido."
        }
      ]
    }
  },
  computed: {
    lugaresFiltrados(){
      return this.recomendados.filter(lugar =>
        lugar.name.toLowerCase().includes(this.busqueda.toLowerCase())
      );
    }
  },
  components: {

  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
 
.search-section {
    width: 90%;
    margin: 1.5rem auto;
}

.search-input {
    width: 100%;
    padding: 0.9rem 1rem;
    border-radius: 2rem;
    border: 1px solid #ccc;
    font-size: 1rem;
    outline: none;
}

.quick-access {
    width: 90%;
    margin: 0 auto 1.5rem auto;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}

.access-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    padding: 1rem 0.5rem;
    background-color: #f2f2f2;
    border-radius: 1rem;
    box-shadow: rgba(0, 0, 0, 0.15) 0px 3px 8px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.access-btn:hover {
    background-color: #e0e0e0;
}

.access-icon {
    font-size: 1.6rem;
}

.access-label {
    font-size: 0.85rem;
    font-weight: 600;
    text-align: center;
}

.recommended {
    width: 90%;
    margin: 0 auto 2rem auto;
}

.recommended-title {
    margin-bottom: 1rem;
}

.no-results {
    padding: 2rem 0;
    text-align: center;
    color: #666;
}

.content-card{
    width: 100%;
    height: 350px;
    margin: 1rem auto;
    gap: 2.5rem;
    display: flex;
}

</style>