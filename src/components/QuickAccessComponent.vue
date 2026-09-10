<template>
    <section class="quick-access">
        <div class="quick-item" v-for="(opcion, index) in opciones" :key="index">
            <span class="quick-icon">{{ opcion.icono }}</span>
            <span class="quick-label">{{ opcion.nombre }}</span>
            <span class="quick-badge quick-badge--urgente" v-if="opcion.urgente">Urgente</span>
            <span class="quick-badge" v-else>Disponible</span>
        </div>
    </section>
</template>

<script>
export default {
    name: 'QuickAccessComponent',
    data() {
        return {
            opciones: [
                { icono: '🗺️', nombre: 'Explorar', urgente: false },
                { icono: '🛡️', nombre: 'Seguridad', urgente: false },
                { icono: '💰', nombre: 'Presupuesto', urgente: false },
                { icono: '📅', nombre: 'Itinerario', urgente: false },
                { icono: '🚕', nombre: 'Transporte', urgente: false },
                { icono: '🚨', nombre: 'Emergencia', urgente: true }
            ]
        }
    }
}
</script>

<style scoped>
.quick-access {
    width: 80%;
    margin: 1.5rem auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.5rem;
}

.quick-item {
    width: 140px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
    padding: 1rem;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    border-radius: 1rem;
}

.quick-icon {
    font-size: 2rem;
}

.quick-label {
    font-weight: 700;
}

.quick-badge {
    font-size: 0.7rem;
    color: #FFF;
    background-color: gray;
    padding: 0.2rem 0.5rem;
    border-radius: 1rem;
}

.quick-badge--urgente {
    background-color: #c0392b;
}
</style>
