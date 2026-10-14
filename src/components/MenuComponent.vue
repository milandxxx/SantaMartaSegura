<template>
    <header class="cabecera">
        <div class="container-logo" @click="$router.push('/')">
            <img v-if="logoOk" class="logo-img" src="../assets/logo-santa-marta.png" alt="Mapa Turístico Santa Marta" @error="logoOk = false">
            <span v-else class="logo-emoji">🌴</span>
            <span class="logo-text">SANTA MARTA SEGURO</span>
        </div>
        <nav class="menu">
            <li class="item-menu" @click="$router.push('/')">INICIO</li>
            <li class="item-menu" @click="$router.push('/lugares')">LUGARES</li>
            <li class="item-menu alerta" @click="$router.push('/emergencia')">🚨 EMERGENCIA</li>
        </nav>
    </header>
</template>

<script>
export default {
    data() {
        return {
            logoOk: true
        };
    }
}
</script>

<style scoped>


.cabecera {
    width: 100%;
    display: flex;
    background: linear-gradient(90deg, #16324a, #1f4c5e);
    color: #FFF;
    height: 72px;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.25);
    border-bottom: 3px solid #d9a441;
}

.container-logo {
    width: auto;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    padding-left: 1rem;
}

.logo-emoji{
    font-size: 28px;
}

.logo-img{
    height: 52px;
    width: 52px;
    object-fit: cover;
    border-radius: 50%;
    background-color: #FFF;
    border: 2px solid #d9a441;
}

.logo-text{
    font-weight: 800;
    font-size: 15px;
    letter-spacing: 1px;
}

.logo{
    height: 80%;
}

.menu {
    width: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
}

.item-menu{
    list-style: none;
    background-color: rgba(255, 255, 255, 0.15);
    color: #FFF;
    font-weight: 600;
    padding: 0.7rem 1rem;
    min-width: 110px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 999px;
    transition: all 0.25s ease;
}

.item-menu:hover{
    background-color: #d9a441;
    color: #16324a;
    cursor: pointer;
    font-weight: 700;
    transform: translateY(-1px);
}

.item-menu.alerta{
    background-color: #dc2626;
    color: #FFF;
}

.item-menu.alerta:hover{
    background-color: #FFF;
    color: #dc2626;
}

@media (max-width: 576px) {
    .container-logo {
        width: auto;
        padding-left: 0.5rem;
    }

    .logo-text {
        font-size: 11px;
    }

    .menu {
        position: static;
        transform: none;
        width: auto;
        gap: 0.5rem;
    }

    .item-menu {
        min-width: auto;
        padding: 0.5rem 0.7rem;
        font-size: 12px;
    }
}


</style>