<template>
    <MenuComponent></MenuComponent>
    <main>
        <section class="barra">
            <h1>🛡️ Seguridad</h1>
            <ButtonPrime label="Emergencia" severity="danger" @click="irEmergencia"></ButtonPrime>
        </section>

        <p class="aviso">No marcamos "zonas peligrosas" sin contexto. Usamos 🟢 Recomendado, 🟡 Precaución y 🔴 Precaución alta, con el porqué y qué hacer.</p>

        <article v-show="loading == true" class="contenedor">
            <SkeletonPrime height="10rem"></SkeletonPrime>
            <SkeletonPrime height="10rem"></SkeletonPrime>
            <SkeletonPrime height="10rem"></SkeletonPrime>
        </article>

        <section v-show="loading == false" class="contenedor">
            <div v-for="z in zonas" :key="z.id" class="zona-card" :class="z.nivel">
                <strong>{{ z.icono }} {{ z.nombre }}</strong>
                <p>{{ z.porque }}</p>
                <p class="tip">💡 {{ z.recomendacion }}</p>
                <p class="horario">🕐 {{ z.horario }}</p>
            </div>
        </section>

        <div class="card">
            <h2>🚕 Transporte seguro</h2>
            <ul>
                <li>Acuerda el precio del taxi antes de subirte.</li>
                <li>De noche prefiere taxi o app en vez de caminar.</li>
                <li>Guarda el número de emergencias: 123.</li>
            </ul>
        </div>
    </main>
</template>

<script>
const API_URL = 'https://santamartasegura-backend.onrender.com';

export default {
    name: 'SeguridadView',
    data() {
        return {
            loading: false,
            zonas: [
                { id: 1, icono: '🟢', nivel: 'verde', nombre: 'El Rodadero', porque: 'Zona turística con alta afluencia y comercio.', recomendacion: 'Ideal de día y noche temprana. Cuida tus pertenencias en la playa.', horario: 'Recomendado todo el día, precaución después de las 10pm.' },
                { id: 2, icono: '🟢', nivel: 'verde', nombre: 'Centro Histórico', porque: 'Patrullaje turístico y restaurantes.', recomendacion: 'Camina de día, taxi de noche.', horario: 'Recomendado 8am - 9pm.' },
                { id: 3, icono: '🟡', nivel: 'amarillo', nombre: 'Taganga', porque: 'Vida nocturna y callejones oscuros.', recomendacion: 'Evita zonas oscuras de noche, ve en grupo.', horario: 'Precaución de noche.' },
                { id: 4, icono: '🟡', nivel: 'amarillo', nombre: 'Minca / Tayrona', porque: 'Naturaleza con accesos largos y clima cambiante.', recomendacion: 'Sal temprano, verifica acceso y clima en Avisos.', horario: 'Solo de día.' },
                { id: 5, icono: '🔴', nivel: 'rojo', nombre: 'Terminal y mercados de noche', porque: 'Aglomeraciones y poco turismo nocturno.', recomendacion: 'Pasa de día, de noche usa transporte directo.', horario: 'Precaución alta de noche.' }
            ]
        };
    },
    methods: {
        irEmergencia: function () {
            this.$router.push('/emergencia');
        },
        getZonas: function () {
            this.loading = true;
            const inicio = Date.now();
            this.axios
                .get(`${API_URL}/api/lugares`)
                .then(response => {
                    console.log(response.data);
                })
                .catch(() => {})
                .finally(() => {
                    const espera = Math.max(0, 800 - (Date.now() - inicio));
                    setTimeout(() => {
                        this.loading = false;
                    }, espera);
                });
        }
    },
    created() {
        this.getZonas();
    }
}
</script>

<style>
.barra {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 95%;
    margin: 1rem auto;
    color: #134e4a;
}
.aviso {
    width: 95%;
    margin: 0 auto 1rem;
    background: #fef3c7;
    color: #92400e;
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
}
.contenedor {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1rem;
    width: 95%;
    margin: 1rem auto;
}
.zona-card {
    background-color: #ffffff;
    border-radius: 1rem;
    padding: 1rem;
    box-shadow: 0 4px 16px rgba(15, 118, 110, 0.15);
    border-top: 6px solid #14b8a6;
}
.zona-card.amarillo { border-top-color: #f59e0b; }
.zona-card.rojo { border-top-color: #dc2626; }
.tip { background: #dcfce7; padding: 0.5rem; border-radius: 4px; }
.horario { font-size: 0.85rem; color: #555; }
.card {
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin: 1rem auto;
    width: 95%;
    background-color: #ffffff;
}

@media (max-width: 900px) {
    .contenedor { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 576px) {
    .contenedor { grid-template-columns: 1fr; }
}
</style>
