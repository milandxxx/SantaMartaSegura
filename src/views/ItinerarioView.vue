<template>
    <MenuComponent></MenuComponent>
    <main>
        <section class="barra">
            <h1>📅 Generador de itinerarios</h1>
        </section>

        <form class="card" @submit.prevent="generar">
            <label>
                Días (1-7)
                <input v-model="form.dias" type="text" inputmode="numeric" />
            </label>
            <div class="checks">
                <label class="check"><input v-model="form.intereses" value="playa" type="checkbox" /> 🏖️ Playa</label>
                <label class="check"><input v-model="form.intereses" value="naturaleza" type="checkbox" /> 🌿 Naturaleza</label>
                <label class="check"><input v-model="form.intereses" value="gastronomia" type="checkbox" /> 🍽️ Gastronomía</label>
                <label class="check"><input v-model="form.intereses" value="cultura" type="checkbox" /> 🏛️ Cultura</label>
            </div>
            <label>
                Nivel
                <select v-model="form.nivel">
                    <option value="relajado">Relajado</option>
                    <option value="equilibrado">Equilibrado</option>
                    <option value="intenso">Intenso</option>
                </select>
            </label>
            <button type="submit">Generar</button>
        </form>

        <p v-if="error" class="msg error">{{ error }}</p>

        <section v-if="plan.length" class="contenedor">
            <div v-for="(d, i) in plan" :key="i" class="dia-card">
                <strong>Día {{ i + 1 }} — {{ d.titulo }}</strong>
                <p>{{ d.detalle }}</p>
                <p>💰 ${{ formato(d.precio) }} · 🕐 {{ d.horario }} · ⏱️ {{ d.duracion }}</p>
                <p class="tip">🛡️ {{ d.seguridad }}</p>
            </div>
        </section>
    </main>
</template>

<script>
const ACTIVIDADES = {
    playa: [
        { titulo: 'Playa El Rodadero', detalle: 'Mañana de playa + almuerzo marino', precio: 60000, horario: '9am - 3pm', duracion: '6h', seguridad: 'Zona 🟢, cuida pertenencias y usa bloqueador.' },
        { titulo: 'Taganga + mirador', detalle: 'Buceo básico y atardecer', precio: 80000, horario: '10am - 6pm', duracion: '8h', seguridad: 'Zona 🟡 de noche, regresa en grupo.' }
    ],
    naturaleza: [
        { titulo: 'Minca', detalle: 'Cascadas + tour de café', precio: 70000, horario: '7am - 4pm', duracion: '9h', seguridad: 'Solo de día, verifica clima en Avisos.' },
        { titulo: 'Parque Tayrona', detalle: 'Senderismo + playa Cabo San Juan', precio: 120000, horario: '6am - 5pm', duracion: '11h', seguridad: 'Verifica acceso antes de ir, lleva agua.' }
    ],
    gastronomia: [
        { titulo: 'Centro + gastronomía', detalle: 'Tour centro histórico y cena típica', precio: 50000, horario: '4pm - 9pm', duracion: '5h', seguridad: 'Zona 🟢, taxi de regreso.' },
        { titulo: 'Mercado gastronómico', detalle: 'Almuerzo típico desde $15.000', precio: 30000, horario: '12pm - 3pm', duracion: '3h', seguridad: 'Pregunta precios antes.' }
    ],
    cultura: [
        { titulo: 'Museos del Centro', detalle: 'Museo del Oro + catedral', precio: 20000, horario: '10am - 2pm', duracion: '4h', seguridad: 'Camina de día.' },
        { titulo: 'Día libre / compras', detalle: 'Artesanías y recuerdos', precio: 40000, horario: 'Libre', duracion: '4h', seguridad: 'Comercio 🟢.' }
    ]
};

export default {
    name: 'ItinerarioView',
    data() {
        return {
            error: '',
            plan: [],
            form: {
                dias: '4',
                intereses: ['playa', 'naturaleza', 'gastronomia'],
                nivel: 'equilibrado'
            }
        };
    },
    methods: {
        formato: function (n) {
            return Number(n).toLocaleString('es-CO');
        },
        generar: function () {
            this.error = '';
            const dias = Number(this.form.dias);
            if (!dias || dias < 1 || dias > 7) {
                this.error = 'Días debe ser entre 1 y 7';
                return;
            }
            if (!this.form.intereses.length) {
                this.error = 'Elige al menos un interés';
                return;
            }
            const bolsa = [];
            this.form.intereses.forEach(k => {
                (ACTIVIDADES[k] || []).forEach(a => bolsa.push(a));
            });
            const porDia = this.form.nivel == 'intenso' ? 2 : 1;
            this.plan = [];
            for (let i = 0; i < dias; i++) {
                const act = bolsa[i % bolsa.length];
                this.plan.push(act);
                if (porDia == 2 && this.plan.length < dias) {
                    const extra = bolsa[(i + 1) % bolsa.length];
                    this.plan[this.plan.length - 1] = {
                        titulo: act.titulo + ' + ' + extra.titulo,
                        detalle: act.detalle + ' / ' + extra.detalle,
                        precio: act.precio + extra.precio,
                        horario: '8am - 8pm',
                        duracion: '12h',
                        seguridad: act.seguridad
                    };
                }
                if (this.form.nivel == 'relajado' && i > 0 && i % 3 == 0) {
                    this.plan[i] = ACTIVIDADES.cultura[1];
                }
            }
        }
    },
    created() {
        this.generar();
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
.checks { display: flex; flex-wrap: wrap; gap: 0.75rem; }
label.check { flex-direction: row; align-items: center; gap: 0.4rem; }
input, select { padding: 0.5rem; border: 1px solid #ccc; border-radius: 6px; }
button { padding: 0.6rem 1rem; border: 0; border-radius: 8px; background: #0f766e; color: #fff; cursor: pointer; font-weight: 700; }
.contenedor { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; width: 95%; margin: 1rem auto; }
.dia-card { background: #ffffff; border-radius: 1rem; padding: 1rem; box-shadow: 0 4px 16px rgba(15,118,110,0.15); border-left: 6px solid #14b8a6; }
.tip { background: #fef3c7; padding: 0.5rem; border-radius: 4px; }
.msg.error { background: #fee2e2; color: #991b1b; padding: 0.5rem; border-radius: 4px; width: 95%; max-width: 560px; margin: 0 auto; }

@media (max-width: 576px) {
    .contenedor { grid-template-columns: 1fr; }
}
</style>
