<template>
    <MenuComponent></MenuComponent>
    <main>
        <section class="barra">
            <h1>💰 Presupuesto inteligente</h1>
        </section>

        <form class="card" @submit.prevent="calcular">
            <label>
                Presupuesto total (COP)
                <input v-model="form.presupuesto" type="text" inputmode="numeric" required />
            </label>
            <label>
                Días
                <input v-model="form.dias" type="text" inputmode="numeric" required />
            </label>
            <label>
                Personas
                <input v-model="form.personas" type="text" inputmode="numeric" required />
            </label>
            <label>
                Tipo de viaje
                <select v-model="form.tipo">
                    <option value="economico">Económico</option>
                    <option value="intermedio">Intermedio</option>
                    <option value="premium">Premium</option>
                </select>
            </label>
            <button type="submit">Calcular</button>
        </form>

        <p v-if="error" class="msg error">{{ error }}</p>

        <div v-if="resultado" class="card">
            <h2>Presupuesto total ${{ formato(resultado.total) }} COP</h2>
            <table>
                <tbody>
                    <tr><td>🏨 Alojamiento</td><td>${{ formato(resultado.alojamiento) }}</td></tr>
                    <tr><td>🍽️ Alimentación</td><td>${{ formato(resultado.alimentacion) }}</td></tr>
                    <tr><td>🚕 Transporte</td><td>${{ formato(resultado.transporte) }}</td></tr>
                    <tr><td>🏖️ Actividades</td><td>${{ formato(resultado.actividades) }}</td></tr>
                    <tr><td>🚨 Reserva</td><td>${{ formato(resultado.reserva) }}</td></tr>
                </tbody>
            </table>
            <p v-if="resultado.ok" class="msg ok">✅ Tu presupuesto permite este itinerario ({{ resultado.porPersonaDia }} por persona/día).</p>
            <p v-else class="msg error">⚠️ Tu presupuesto está ajustado para estos lugares ({{ resultado.porPersonaDia }} por persona/día). Considera plan económico.</p>
        </div>
    </main>
</template>

<script>
export default {
    name: 'PresupuestoView',
    data() {
        return {
            error: '',
            resultado: null,
            form: {
                presupuesto: '800000',
                dias: '4',
                personas: '2',
                tipo: 'intermedio'
            }
        };
    },
    methods: {
        formato: function (n) {
            return Number(n).toLocaleString('es-CO');
        },
        calcular: function () {
            this.error = '';
            const total = Number(this.form.presupuesto);
            const dias = Number(this.form.dias);
            const personas = Number(this.form.personas);
            if (!total || !dias || !personas) {
                this.error = 'Completa presupuesto, días y personas con números válidos';
                return;
            }
            let p = { alojamiento: 0.35, alimentacion: 0.25, transporte: 0.125, actividades: 0.2125, reserva: 0.0625 };
            if (this.form.tipo == 'economico') {
                p = { alojamiento: 0.30, alimentacion: 0.25, transporte: 0.15, actividades: 0.20, reserva: 0.10 };
            }
            if (this.form.tipo == 'premium') {
                p = { alojamiento: 0.40, alimentacion: 0.28, transporte: 0.10, actividades: 0.17, reserva: 0.05 };
            }
            const porPersonaDia = Math.round(total / dias / personas);
            this.resultado = {
                total: total,
                alojamiento: Math.round(total * p.alojamiento),
                alimentacion: Math.round(total * p.alimentacion),
                transporte: Math.round(total * p.transporte),
                actividades: Math.round(total * p.actividades),
                reserva: Math.round(total * p.reserva),
                porPersonaDia: '$' + porPersonaDia.toLocaleString('es-CO'),
                ok: porPersonaDia >= 80000
            };
        }
    },
    created() {
        this.calcular();
    }
}
</script>

<style>
.barra {
    width: 95%;
    margin: 1rem auto;
    color: #134e4a;
}
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
input, select { padding: 0.5rem; border: 1px solid #ccc; border-radius: 6px; }
button { padding: 0.6rem 1rem; border: 0; border-radius: 8px; background: #0f766e; color: #fff; cursor: pointer; font-weight: 700; }
table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }
td { padding: 0.5rem; border-bottom: 1px solid #eee; }
.msg { padding: 0.5rem 0.75rem; border-radius: 4px; margin-top: 0.75rem; }
.msg.error { background: #fee2e2; color: #991b1b; }
.msg.ok { background: #dcfce7; color: #166534; }
</style>
