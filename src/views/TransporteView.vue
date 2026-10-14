<template>
    <MenuComponent></MenuComponent>
    <main>
        <section class="barra">
            <h1>🚕 Transporte</h1>
        </section>

        <form class="card" @submit.prevent="estimar">
            <label>
                Origen
                <select v-model="form.origen">
                    <option v-for="p in puntos" :key="p" :value="p">{{ p }}</option>
                </select>
            </label>
            <label>
                Destino
                <select v-model="form.destino">
                    <option v-for="p in puntos" :key="p" :value="p">{{ p }}</option>
                </select>
            </label>
            <button type="submit">Ver opciones</button>
        </form>

        <p v-if="error" class="msg error">{{ error }}</p>

        <section v-if="resultado" class="contenedor">
            <div class="op-card">
                <strong>🚕 Taxi</strong>
                <p>⏱️ {{ resultado.taxi.tiempo }}</p>
                <p>💰 ${{ formato(resultado.taxi.costo) }}</p>
            </div>
            <div class="op-card">
                <strong>🚌 Bus</strong>
                <p>⏱️ {{ resultado.bus.tiempo }}</p>
                <p>💰 ${{ formato(resultado.bus.costo) }}</p>
            </div>
            <div class="op-card">
                <strong>🚶 Caminando</strong>
                <p>⏱️ {{ resultado.pie.tiempo }}</p>
                <p>💰 Gratis</p>
            </div>
        </section>

        <div v-if="resultado" class="card">
            <h2>Pedir taxi ahora</h2>
            <div class="pedir-btns">
                <ButtonPrime label="Pedir en Uber" @click="pedirUber"></ButtonPrime>
                <ButtonPrime label="Abrir inDrive" severity="secondary" @click="abrirIndrive"></ButtonPrime>
            </div>
            <p class="nota">Uber abre con origen y destino precargados. inDrive no tiene enlace público para precargar el viaje, así que se abre la app y lo completas ahí.</p>
        </div>

        <div v-if="resultado" class="card">
            <h2>Consejos</h2>
            <ul>
                <li>Acuerda el precio del taxi antes de subirte ({{ resultado.distancia }} km aprox).</li>
                <li>De noche prefiere taxi. De día el bus es económico.</li>
                <li>Si te cobran de más, anota la placa y reporta al 123.</li>
            </ul>
        </div>
    </main>
</template>

<script>
const DISTANCIAS = {
    'Hotel|Playa': 3,
    'Hotel|Minca': 15,
    'Hotel|Centro': 2,
    'Hotel|Tayrona': 35,
    'Playa|Minca': 18,
    'Playa|Centro': 4,
    'Playa|Tayrona': 38,
    'Minca|Centro': 14,
    'Minca|Tayrona': 50,
    'Centro|Tayrona': 34
};

const COORDS = {
    'Hotel': { lat: 11.2033, lon: -74.2365 },
    'Playa': { lat: 11.2050, lon: -74.2280 },
    'Minca': { lat: 11.1406, lon: -74.1186 },
    'Centro': { lat: 11.2408, lon: -74.2119 },
    'Tayrona': { lat: 11.2700, lon: -74.0700 }
};

export default {
    name: 'TransporteView',
    data() {
        return {
            error: '',
            resultado: null,
            puntos: ['Hotel', 'Playa', 'Minca', 'Centro', 'Tayrona'],
            form: {
                origen: 'Hotel',
                destino: 'Playa'
            }
        };
    },
    methods: {
        formato: function (n) {
            return Number(n).toLocaleString('es-CO');
        },
        distanciaKm: function (a, b) {
            if (a == b) return 1;
            return DISTANCIAS[a + '|' + b] || DISTANCIAS[b + '|' + a] || 5;
        },
        estimar: function () {
            this.error = '';
            if (this.form.origen == this.form.destino) {
                this.error = 'Elige un destino distinto al origen';
                return;
            }
            const km = this.distanciaKm(this.form.origen, this.form.destino);
            this.resultado = {
                distancia: km,
                taxi: { tiempo: Math.round(km * 4 + 5) + ' min', costo: Math.round(7000 + km * 1800) },
                bus: { tiempo: Math.round(km * 7 + 10) + ' min', costo: 2600 },
                pie: { tiempo: Math.round(km * 14) + ' min' }
            };
        },
        pedirUber: function () {
            const o = COORDS[this.form.origen];
            const d = COORDS[this.form.destino];
            const url = 'https://m.uber.com/ul/?action=setPickup'
                + '&pickup[latitude]=' + o.lat + '&pickup[longitude]=' + o.lon + '&pickup[nickname]=' + this.form.origen
                + '&dropoff[latitude]=' + d.lat + '&dropoff[longitude]=' + d.lon + '&dropoff[nickname]=' + this.form.destino;
            window.open(url, '_blank');
        },
        abrirIndrive: function () {
            window.open('https://indrive.com', '_blank');
        }
    },
    created() {
        this.estimar();
    }
}
</script>

<style>
.barra { width: 95%; margin: 1rem auto; color: #134e4a; }
.card {
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin: 1rem auto;
    width: 95%;
    max-width: 560px;
    background-color: #ffffff;
}
form { display: flex; flex-direction: column; gap: 0.75rem; }
label { display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.9rem; }
select { padding: 0.5rem; border: 1px solid #ccc; border-radius: 6px; }
button { padding: 0.6rem 1rem; border: 0; border-radius: 8px; background: #0f766e; color: #fff; cursor: pointer; font-weight: 700; }
.contenedor { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; width: 95%; max-width: 700px; margin: 1rem auto; }
.op-card { background: #ffffff; border-radius: 1rem; padding: 1rem; box-shadow: 0 4px 16px rgba(15,118,110,0.15); text-align: center; }
.pedir-btns { display: flex; gap: 0.75rem; margin: 0.75rem 0; flex-wrap: wrap; }
.nota { font-size: 0.85rem; color: #555; }
.msg.error { background: #fee2e2; color: #991b1b; padding: 0.5rem; border-radius: 4px; width: 95%; max-width: 560px; margin: 0 auto; }

@media (max-width: 576px) {
    .contenedor { grid-template-columns: 1fr; }
}
</style>
