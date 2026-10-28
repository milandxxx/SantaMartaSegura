<template>
    <MenuComponent></MenuComponent>
    <main class="home-container">
        <section class="carousel-section" aria-roledescription="carousel" aria-label="Galería de imágenes destacadas"
            @mouseenter="pauseAutoplay" @mouseleave="startAutoplay">
            <!-- Contenedor con overflow oculto -->
            <div class="carousel-viewport">
                <!-- Pista que se desplaza -->
                <div class="carousel-track" :style="trackStyle" @transitionend="handleTransitionEnd">
                    <figure v-for="(imgSrc, index) in displaySlides" :key="`${imgSrc}-${index}`" class="carousel-slide">
                        <img :src="imgSrc" :alt="`Slide ${index}`" loading="lazy" />
                    </figure>
                </div>
            </div>

            <div class="hero-overlay">
                <h1>🌴 SANTA MARTA SEGURO</h1>
                <p>Voy a Santa Marta 4 días, tengo $800.000 COP, viajo con mi pareja y quiero playa, naturaleza y gastronomía.</p>
                <div class="buscador">
                    <InputText v-model="busqueda" placeholder="🔎 Buscar un lugar..." @keyup.enter="buscarLugares" />
                    <ButtonPrime label="Buscar" @click="buscarLugares"></ButtonPrime>
                </div>
            </div>
            
            <!-- Botón anterior (Izquierda) -->
            <button type="button" class="carousel-control prev" @click="prevSlide" aria-label="Imagen anterior">
                &#10094;
            </button>

            <!-- Botón siguiente (Derecha) -->
            <button type="button" class="carousel-control next" @click="nextSlide" aria-label="Imagen siguiente">
                &#10095;
            </button>
        </section>

        <!-- RESULTADOS DE BÚSQUEDA -->
        <section v-if="busqueda.trim()" class="resultados-busqueda">
            <h2>🔍 Resultados para "{{ busqueda }}"</h2>
            <article v-show="loadingBusqueda" class="content-card">
                <SkeletonPrime height="14rem"></SkeletonPrime>
                <SkeletonPrime height="14rem"></SkeletonPrime>
                <SkeletonPrime height="14rem"></SkeletonPrime>
            </article>
            <article v-show="!loadingBusqueda && resultadosBusqueda.length === 0" class="sin-resultados">
                <p>😕 No se encontraron lugares que coincidan con "<strong>{{ busqueda }}</strong>"</p>
                <ButtonPrime label="Ver todos los lugares" @click="irLugares" />
            </article>
            <article v-show="!loadingBusqueda && resultadosBusqueda.length > 0" class="content-card">
                <CardComponent v-for="lugar in resultadosBusqueda" :key="lugar.id" :imagen="lugar.imagen"
                    :nombre="lugar.nombre" :parrafo="lugar.detalle"></CardComponent>
            </article>
        </section>

        <section class="accesos">
            <h2>¿Qué necesitas?</h2>
            <div class="accesos-grid">
                <div class="acceso-card" @click="irLugares">
                    <span class="acceso-emoji">🗺️</span>
                    <span>Explorar</span>
                </div>
                <div class="acceso-card" @click="irSeguridad">
                    <span class="acceso-emoji">🛡️</span>
                    <span>Seguridad</span>
                </div>
                <div class="acceso-card" @click="irPresupuesto">
                    <span class="acceso-emoji">💰</span>
                    <span>Presupuesto</span>
                </div>
                <div class="acceso-card" @click="irItinerario">
                    <span class="acceso-emoji">📅</span>
                    <span>Itinerario</span>
                </div>
                <div class="acceso-card" @click="irTransporte">
                    <span class="acceso-emoji">🚕</span>
                    <span>Transporte</span>
                </div>
                <div class="acceso-card alerta" @click="irEmergencia">
                    <span class="acceso-emoji">🚨</span>
                    <span>Emergencia</span>
                </div>
            </div>
        </section>

        <section class="recomendado">
            <h2>🌴 Recomendado para ti</h2>
            <article v-show="loadingLugares == true" class="content-card">
                <SkeletonPrime height="14rem"></SkeletonPrime>
                <SkeletonPrime height="14rem"></SkeletonPrime>
                <SkeletonPrime height="14rem"></SkeletonPrime>
            </article>
            <article v-show="loadingLugares == false" class="content-card">
                <CardComponent v-for="lugar in destacados" :key="lugar.id" :imagen="lugar.imagen"
                    :nombre="lugar.nombre" :parrafo="lugar.detalle"></CardComponent>
            </article>
        </section>
    </main>
</template>

<script>
export default {
    name: 'InicioView',
    data() {
        return {
            // Array dinámico de tamaño n
            slides: [
                "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=80",
                "https://images.unsplash.com/photo-1519046904884-53103b34b206?auto=format&fit=crop&w=1600&q=80",
                "https://images.unsplash.com/photo-1502680390469-be75c86b636f?auto=format&fit=crop&w=1600&q=80",
                "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1600&q=80"
            ],
            // Iniciamos en 1 debido al clon del último elemento al inicio
            currentIndex: 1,
            isTransitioning: true,
            autoplayTimer: null,
            transitionDuration: 500, // ms
            busqueda: "",
            destacados: [],
            loadingLugares: false,
            // Búsqueda
            resultadosBusqueda: [],
            loadingBusqueda: false
        };
    },
    computed: {
        // Genera el arreglo con clones para el loop infinito: [Último, ...slides, Primero]
        displaySlides() {
            if (!this.slides || this.slides.length === 0) return [];
            if (this.slides.length === 1) return this.slides;

            const firstClone = this.slides[0];
            const lastClone = this.slides[this.slides.length - 1];
            return [lastClone, ...this.slides, firstClone];
        },
        // Estilos reactivos aplicados al track
        trackStyle() {
            return {
                transform: `translateX(-${this.currentIndex * 100}%)`,
                transition: this.isTransitioning
                    ? `transform ${this.transitionDuration}ms ease-in-out`
                    : 'none'
            };
        }
    },
    methods: {
        nextSlide() {
            if (this.slides.length <= 1) return;
            this.isTransitioning = true;
            this.currentIndex++;
        },
        prevSlide() {
            if (this.slides.length <= 1) return;
            this.isTransitioning = true;
            this.currentIndex--;
        },

        handleTransitionEnd() {
            // Si llega al clon final, salta instantáneamente al primer slide real
            if (this.currentIndex === this.displaySlides.length - 1) {
                this.isTransitioning = false;
                this.currentIndex = 1;
            }
            // Si llega al clon inicial, salta instantáneamente al último slide real
            if (this.currentIndex === 0) {
                this.isTransitioning = false;
                this.currentIndex = this.displaySlides.length - 2;
            }
        },
        
        startAutoplay() {
            if (this.slides.length <= 1) return;
            this.clearAutoplay();
            this.autoplayTimer = setInterval(() => {
                this.nextSlide();
            }, 4000);
        },
        pauseAutoplay() {
            this.clearAutoplay();
        },
        clearAutoplay() {
            if (this.autoplayTimer) {
                clearInterval(this.autoplayTimer);
                this.autoplayTimer = null;
            }
        },
        irLugares: function () {
            this.$router.push('/lugares');
        },
        irEmergencia: function () {
            this.$router.push('/emergencia');
        },
        irSeguridad: function () {
            this.$router.push('/seguridad');
        },
        irPresupuesto: function () {
            this.$router.push('/presupuesto');
        },
        irItinerario: function () {
            this.$router.push('/itinerario');
        },
        irTransporte: function () {
            this.$router.push('/transporte');
        },
        getDestacados: function () {
            this.loadingLugares = true;
            this.axios
                .get('https://santamartasegura-backend.onrender.com/api/lugares')
                .then(response => {
                    this.destacados = response.data.respuesta.slice(0, 3);
                    console.log(this.destacados);
                })
                .catch(() => {
                    this.destacados = [
                        { id: 1, nombre: "Playa El Rodadero", detalle: "Ideal en familia", imagen: this.slides[0] },
                        { id: 2, nombre: "Minca", detalle: "Naturaleza y cafe", imagen: this.slides[3] },
                        { id: 3, nombre: "Centro Historico", detalle: "Cultura y gastronomia", imagen: this.slides[2] }
                    ];
                })
                .finally(() => {
                    this.loadingLugares = false;
                });
        },
        // BÚSQUEDA EN BASE DE DATOS
        buscarLugares: function () {
            const termino = this.busqueda.trim();
            if (!termino) {
                this.resultadosBusqueda = [];
                return;
            }
            this.loadingBusqueda = true;
            this.axios
                .get('https://santamartasegura-backend.onrender.com/api/lugares')
                .then(response => {
                    const todos = response.data.respuesta || [];
                    // Filtrar por nombre, categoría o detalle (case insensitive)
                    this.resultadosBusqueda = todos.filter(lugar => 
                        lugar.nombre.toLowerCase().includes(termino.toLowerCase()) ||
                        lugar.categoria.toLowerCase().includes(termino.toLowerCase()) ||
                        (lugar.detalle && lugar.detalle.toLowerCase().includes(termino.toLowerCase()))
                    );
                })
                .catch(() => {
                    this.resultadosBusqueda = [];
                })
                .finally(() => {
                    this.loadingBusqueda = false;
                });
        },
        limpiarBusqueda: function () {
            this.busqueda = "";
            this.resultadosBusqueda = [];
        }
    },
    mounted() {
        this.startAutoplay();
        this.getDestacados();
    },
    beforeUnmount() {
        this.clearAutoplay();
    }
};
</script>

<style scoped>
/* Reset de caja y contenedor principal */
.home-container {
    width: 100%;
}

.carousel-section {
    position: relative;
    width: 100%;
    height: 500px;
    overflow: hidden;
    user-select: none;
    background-color: #000;
}

.carousel-viewport {
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.carousel-track {
    display: flex;
    width: 100%;
    height: 100%;
    will-change: transform;
}

.carousel-slide {
    flex: 0 0 100%;
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
}

.carousel-slide img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    pointer-events: none;
}

.hero-overlay {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: #FFF;
    background: linear-gradient(135deg, rgba(22, 50, 74, 0.88), rgba(31, 76, 94, 0.55));
    padding: 1.5rem 2rem;
    border-radius: 1.25rem;
    width: 90%;
    max-width: 600px;
    z-index: 5;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(4px);
}

.hero-overlay h1 {
    margin-bottom: 0.5rem;
    letter-spacing: 1px;
}

.hero-overlay p {
    font-size: 0.95rem;
    margin-bottom: 1rem;
}

.buscador {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
}

/* Controles de navegación */
.carousel-control {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: rgba(0, 0, 0, 0.45);
    color: #ffffff;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    z-index: 10;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.carousel-control:hover {
    background-color: rgba(0, 0, 0, 0.8);
    transform: translateY(-50%) scale(1.08);
}

.carousel-control:focus-visible {
    outline: 2px solid #ffffff;
}

.carousel-control.prev {
    left: 15px;
}

.carousel-control.next {
    right: 15px;
}

.accesos {
    width: 95%;
    max-width: 700px;
    margin: 1.5rem auto;
    text-align: center;
    color: #134e4a;
}

.accesos-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1rem;
    margin-top: 1rem;
}

.acceso-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 1.2rem 0.5rem;
    border-radius: 1rem;
    background-color: #ffffff;
    box-shadow: 0 4px 16px rgba(15, 118, 110, 0.15);
    cursor: pointer;
    font-weight: 600;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.acceso-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(15, 118, 110, 0.3);
}

.acceso-card.alerta {
    background-color: #fee2e2;
}

.acceso-emoji {
    font-size: 28px;
}

.recomendado {
    width: 95%;
    margin: 1rem auto;
}

.recomendado h2 {
    text-align: center;
    margin-bottom: 1rem;
}

/* RESULTADOS DE BÚSQUEDA */
.resultados-busqueda {
    width: 95%;
    max-width: 900px;
    margin: 1.5rem auto;
    padding: 1.5rem;
    background: #ffffff;
    border-radius: 1rem;
    box-shadow: 0 4px 16px rgba(15, 118, 110, 0.1);
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.resultados-busqueda h2 {
    color: #134e4a;
    margin-bottom: 1rem;
    font-size: 1.25rem;
    text-align: center;
}

.sin-resultados {
    text-align: center;
    padding: 3rem 2rem;
    color: #6b7280;
}

.sin-resultados p {
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
}

.sin-resultados strong {
    color: #134e4a;
}

.content-card {
    width: 80%;
    height: 350px;
    margin: 1rem auto;
    gap: 2.5rem;
    display: flex;
}

/* Media Queries para Tablet y Móvil */
@media (max-width: 768px) {
    .carousel-section {
        height: 360px;
    }

    .carousel-control {
        width: 42px;
        height: 42px;
        font-size: 20px;
    }

    .content-card {
        width: 95%;
        flex-direction: column;
        height: auto;
    }
}

@media (max-width: 576px) {
    .carousel-section {
        height: 260px;
    }

    .carousel-control {
        width: 36px;
        height: 36px;
        font-size: 16px;
    }

    .carousel-control.prev {
        left: 8px;
    }

    .carousel-control.next {
        right: 8px;
    }

    .hero-overlay {
        padding: 1rem;
    }

    .accesos-grid {
        grid-template-columns: 1fr 1fr 1fr;
        gap: 0.5rem;
    }
}
</style>
