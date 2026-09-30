<template>
    <header class="cabecera">
        <div class="container-logo">
            <!-- <img class="logo" src="../assets/flag-fr" alt="LOGO"> -->
        </div>
        <nav class="menu">
            <li class="item-menu" v-for="(opcion, index) in opcionesMenu" :key="index">{{ opcion.nombre }}</li>
        </nav>
    </header>
</template>

<script>
export default {
    name: 'MenuComponent',
    data() {
        return {
            opcionesMenu: [
                { nombre: 'INICIO' },
                { nombre: 'SEGURIDAD' },
                { nombre: 'PRESUPUESTO' },
                { nombre: 'EMERGENCIAS' }
            ]
        }
    }
}
</script>

<style scoped>


.cabecera {
    width: 100%;
    display: flex;
    background-color: #000;
    color: #FFF;
    height: 80px;
    border-bottom: #FFF 1px solid;
}

.container-logo {
    width: 20%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.logo{
    height: 80%;
}

.menu {
    width: 80%;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
}

.item-menu{
    list-style: none;
    background-color: gray;
    color: #000;
    padding: 1rem;
    width: 15%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.item-menu:hover{
    background-color: #FFF;
    cursor: pointer;
    font-weight: 700;
}


</style>