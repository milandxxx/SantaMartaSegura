<template>
    <MenuComponent></MenuComponent>
    <main>
        <section class="barra">
            <h1>🚨 Centro de Emergencias</h1>
            <ButtonPrime severity="danger" @click="getAllEmergencias">Recargar</ButtonPrime>
        </section>

        <p class="aviso">Esta app no sustituye a los servicios oficiales. Ante peligro llama primero a la línea oficial.</p>

        <h2 class="subtitulo">¿Qué ocurrió?</h2>
        <section class="contenedor">
            <div v-for="t in tipos" :key="t.id" class="tipo-card" :class="{ activo: tipoSeleccionado.id == t.id }"
                @click="seleccionarTipo(t)">
                <span class="tipo-emoji">{{ t.emoji }}</span>
                <span>{{ t.nombre }}</span>
            </div>
        </section>

        <section class="card">
            <h2>{{ tipoSeleccionado.emoji }} {{ tipoSeleccionado.nombre }}</h2>
            <p><strong>Contacto:</strong> {{ tipoSeleccionado.contacto }}</p>
            <p><strong>Qué hacer:</strong></p>
            <ul>
                <li v-for="(paso, i) in tipoSeleccionado.queHacer" :key="i">{{ paso }}</li>
            </ul>
            <p><strong>Dónde ir:</strong> {{ tipoSeleccionado.donde }}</p>
            <p class="tip">💡 {{ tipoSeleccionado.tip }}</p>
        </section>

        <div class="card">
            <div class="header">
                <h2>Contactos oficiales</h2>
            </div>
            <article v-show="loading == true" class="skeleton-list">
                <SkeletonPrime height="3rem"></SkeletonPrime>
                <SkeletonPrime height="3rem"></SkeletonPrime>
                <SkeletonPrime height="3rem"></SkeletonPrime>
            </article>
            <p v-if="error" class="msg error">{{ error }}</p>
            <table v-show="loading == false">
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Teléfono</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="c in contactos" :key="c.id">
                        <td>{{ c.nombre }}</td>
                        <td>{{ c.telefono }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </main>
</template>

<script>
const API_URL = 'https://santamartasegura-backend.onrender.com';

export default {
    name: 'EmergenciaView',
    data() {
        return {
            contactos: [],
            loading: false,
            error: '',
            tipos: [
                { id: 1, emoji: '🚔', nombre: 'Robo', contacto: 'Policía 123', queHacer: ['Mantén la calma y aléjate del lugar', 'Llama al 123 y reporta ubicación', 'Bloquea tarjetas y documentos'], donde: 'Policía y puntos de atención más cercanos', tip: 'Anota hora y lugar para el reporte.' },
                { id: 2, emoji: '🏥', nombre: 'Emergencia médica', contacto: 'Ambulancia 123 / 119', queHacer: ['Llama de inmediato y da tu ubicación', 'No te automediques', 'Pide ayuda al hotel o comercio cercano'], donde: 'Hospitales y centros médicos', tip: 'Guarda tu seguro médico en el celular.' },
                { id: 3, emoji: '📄', nombre: 'Perdí mis documentos', contacto: 'Policía 123', queHacer: ['Reporta la pérdida', 'Contacta tu embajada si eres extranjero', 'Guarda copia digital siempre'], donde: 'Puntos de atención policial', tip: 'Lleva foto de tu pasaporte en el correo.' },
                { id: 4, emoji: '🚕', nombre: 'Problema con transporte', contacto: 'Policía de tránsito 123', queHacer: ['No discutas en vía pública', 'Anota placa y empresa', 'Pide factura o comprobante'], donde: 'Terminal de transporte', tip: 'Acuerda el precio antes de subirte.' },
                { id: 5, emoji: '👤', nombre: 'Persona desaparecida', contacto: 'Policía 123 / 165', queHacer: ['Reporta de inmediato con última ubicación', 'Comparte foto reciente', 'Avisa al hotel'], donde: 'CTI / Fiscalía más cercana', tip: 'Comparte tu ubicación en tiempo real al viajar.' },
                { id: 6, emoji: '📞', nombre: 'Necesito ayuda', contacto: 'Línea turista 123', queHacer: ['Describe tu ubicación con un punto de referencia', 'Mantén el celular con batería', 'Busca un comercio u hotel cercano'], donde: 'Puntos de información turística', tip: 'Descarga el mapa sin conexión.' }
            ],
            tipoSeleccionado: { id: 1, emoji: '🚔', nombre: 'Robo', contacto: 'Policía 123', queHacer: ['Mantén la calma y aléjate del lugar', 'Llama al 123 y reporta ubicación', 'Bloquea tarjetas y documentos'], donde: 'Policía y puntos de atención más cercanos', tip: 'Anota hora y lugar para el reporte.' }
        };
    },
    methods: {
        seleccionarTipo: function (t) {
            this.tipoSeleccionado = t;
        },
        getAllEmergencias: function () {
            this.loading = true;
            this.error = '';
            this.axios
                .get(`${API_URL}/api/emergencias`)
                .then(response => {
                    this.contactos = response.data.respuesta;
                    console.log(this.contactos);
                })
                .catch(() => {
                    this.contactos = [
                        { id: 1, nombre: "Policía Nacional", telefono: "123" },
                        { id: 2, nombre: "Bomberos Santa Marta", telefono: "119" },
                        { id: 3, nombre: "Hospital Central", telefono: "6054211111" }
                    ];
                })
                .finally(() => {
                    this.loading = false;
                });
        }
    },
    created() {
        this.getAllEmergencias();
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
    color: #7f1d1d;
}
.aviso {
    width: 95%;
    margin: 0 auto 1rem;
    background: #fef3c7;
    color: #92400e;
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
}
.subtitulo {
    width: 95%;
    margin: 0 auto;
    color: #134e4a;
}
.contenedor {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1rem;
    width: 95%;
    margin: 1rem auto;
}
.tipo-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem 0.5rem;
    border-radius: 1rem;
    background-color: #ffffff;
    box-shadow: 0 4px 16px rgba(15, 118, 110, 0.15);
    cursor: pointer;
    font-weight: 600;
    transition: transform 0.25s ease;
}
.tipo-card:hover {
    transform: translateY(-3px);
}
.tipo-card.activo {
    border: 2px solid #dc2626;
}
.tipo-emoji {
    font-size: 28px;
}
.card {
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin: 1rem auto;
    width: 95%;
    background-color: #ffffff;
}
.header { display: flex; justify-content: space-between; align-items: center; }
.skeleton-list { display: flex; flex-direction: column; gap: 0.5rem; }
table { width: 100%; border-collapse: collapse; }
th, td { text-align: left; padding: 0.5rem; border-bottom: 1px solid #eee; }
.msg { padding: 0.5rem 0.75rem; border-radius: 4px; }
.msg.error { background: #fee2e2; color: #991b1b; }
.tip { background: #dcfce7; padding: 0.5rem; border-radius: 4px; }

@media (max-width: 768px) {
    .contenedor {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 576px) {
    .contenedor {
        grid-template-columns: 1fr 1fr;
        gap: 0.5rem;
    }

    .barra {
        flex-direction: column;
        gap: 0.75rem;
    }
}
</style>
