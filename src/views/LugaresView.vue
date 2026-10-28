<template>
    <MenuComponent></MenuComponent>
    <main>
        <section class="barra">
            <h1>Lugares de Santa Marta</h1>
        </section>

        <p v-if="error" class="msg error">{{ error }}</p>

        <article v-show="loading == true" class="contenedor">
            <SkeletonPrime height="14rem"></SkeletonPrime>
            <SkeletonPrime height="14rem"></SkeletonPrime>
            <SkeletonPrime height="14rem"></SkeletonPrime>
            <SkeletonPrime height="14rem"></SkeletonPrime>
            <SkeletonPrime height="14rem"></SkeletonPrime>
            <SkeletonPrime height="14rem"></SkeletonPrime>
        </article>

        <p v-show="loading == false && !lugares.length" class="vacio">No hay lugares registrados.</p>

        <section v-show="loading == false && lugares.length" class="contenedor">
            <LugarComponent v-for="lugar in lugares" :key="lugar.id" :imagen="lugar.imagen"
                :nombre="lugar.nombre" :precio="lugar.precio" :detalle="lugar.detalle"
                :etiqueta="lugar.categoria">
            </LugarComponent>
        </section>
    </main>

</template>

<script>
const API_URL = 'https://santamartasegura-backend.onrender.com';

export default {
    name: 'LugaresView',
    data() {
        return {
            lugares: [],
            loading: false,
            error: ''
        };
    },

    methods: {
        getAllLugares: function () {
            this.loading = true;
            this.error = '';
            const inicio = Date.now();
            this.axios
                .get(`${API_URL}/api/lugares`)
                .then(response => {
                    this.lugares = response.data.respuesta;
                    console.log(this.lugares);
                })
                .catch(e => {
                    this.error = e.response?.data?.error || 'No se pudo cargar los lugares. Verifica que el backend este corriendo.';
                })
                .finally(() => {
                    const espera = Math.max(0, 1200 - (Date.now() - inicio));
                    setTimeout(() => {
                        this.loading = false;
                    }, espera);
                });
        }
    },
    created() {
        this.getAllLugares();
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
.contenedor {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1rem;
    width: 95%;
    margin: 1rem auto;
}
.msg { padding: 0.5rem 0.75rem; border-radius: 4px; width: 95%; margin: 0.5rem auto; }
.msg.error { background: #fee2e2; color: #991b1b; }
.vacio { text-align: center; margin: 2rem; }

@media (max-width: 900px) {
    .contenedor {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 576px) {
    .contenedor {
        grid-template-columns: 1fr;
    }

    .barra {
        flex-direction: column;
        gap: 0.75rem;
    }
}
</style>