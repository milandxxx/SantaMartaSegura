<template>
    <MenuComponent></MenuComponent>
    <main>
        <section class="barra">
            <h1>Lugares de Santa Marta</h1>
            <ButtonPrime severity="danger" variant="outlined" @click="open = true">Nuevo lugar</ButtonPrime>
        </section>

        <DialogPrime v-model:visible="open" modal header="Nuevo lugar" :style="{ width: '24rem' }">
            <div class="flex flex-col gap-4">
                <div class="flex flex-col gap-1.5">
                    <LabelPrime for="name">Nombre</LabelPrime>
                    <InputText id="name" v-model="nuevoLugar.nombre" autoFocus />
                </div>
                <div class="flex flex-col gap-1.5">
                    <LabelPrime for="precio">Precio</LabelPrime>
                    <InputText id="precio" v-model="nuevoLugar.precio" />
                </div>
                <div class="flex flex-col gap-1.5">
                    <LabelPrime for="imagen">Imagen</LabelPrime>
                    <InputText id="imagen" v-model="nuevoLugar.imagen" />
                </div>
            </div>
            <template #footer>
                <ButtonPrime severity="secondary" variant="outlined" :disabled="saving" @click="open = false">Cancel</ButtonPrime>
                <ButtonPrime :disabled="saving" @click="guardarLugar">{{ saving ? 'Guardando...' : 'Guardar' }}</ButtonPrime>
            </template>
        </DialogPrime>

        <p v-if="error" class="msg error">{{ error }}</p>
        <p v-if="success" class="msg ok">{{ success }}</p>

        <article v-show="loading == true" class="contenedor">
            <SkeletonPrime height="14rem"></SkeletonPrime>
            <SkeletonPrime height="14rem"></SkeletonPrime>
            <SkeletonPrime height="14rem"></SkeletonPrime>
            <SkeletonPrime height="14rem"></SkeletonPrime>
            <SkeletonPrime height="14rem"></SkeletonPrime>
            <SkeletonPrime height="14rem"></SkeletonPrime>
        </article>

        <article v-show="loading == false && saving == true" class="contenedor">
            <SkeletonPrime height="14rem"></SkeletonPrime>
            <SkeletonPrime height="14rem"></SkeletonPrime>
            <SkeletonPrime height="14rem"></SkeletonPrime>
        </article>
        <p v-show="saving == true" class="vacio">Guardando lugar...</p>

        <p v-show="loading == false && saving == false && !lugares.length" class="vacio">No hay lugares registrados.</p>

        <section v-show="loading == false && saving == false" class="contenedor">
            <LugarComponent v-for="lugar in lugares" :key="lugar.id" :imagen="lugar.imagen"
                :nombre="lugar.nombre" :precio="lugar.precio" :detalle="lugar.detalle"
                :etiqueta="lugar.categoria">
            </LugarComponent>
        </section>
    </main>

</template>

<script>
const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000';

export default {
    name: 'LugaresView',
    data() {
        return {
            lugares: [],
            loading: false,
            saving: false,
            error: '',
            success: '',
            open: false,
            nuevoLugar: {
                nombre: "",
                imagen: "",
                precio: ""
            }
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
        },

        guardarLugar: async function () {
            this.error = '';
            this.success = '';
            this.saving = true;
            const inicio = Date.now();
            await this.axios
                .post(`${API_URL}/api/lugares`,
                    {
                        nombre: this.nuevoLugar.nombre,
                        imagen: this.nuevoLugar.imagen,
                        precio: Number(this.nuevoLugar.precio) || 0,
                        categoria: "playa",
                        detalle: "Agregado por el turista"
                    }
                )
                .then(response => {
                    if (response.data.status) {
                        this.success = 'Lugar guardado correctamente';
                        this.open = false;
                        this.nuevoLugar = { nombre: "", imagen: "", precio: "" };
                        this.getAllLugares();
                    } else {
                        this.error = "ERROR al guardar";
                        console.log(response.data);
                    }
                })
                .catch(e => {
                    this.error = e.response?.data?.error || 'Error al guardar el lugar';
                })
                .finally(() => {
                    const espera = Math.max(0, 1200 - (Date.now() - inicio));
                    setTimeout(() => {
                        this.saving = false;
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
.msg.ok { background: #dcfce7; color: #166534; }
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
