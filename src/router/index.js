import { createRouter, createWebHistory } from 'vue-router'
import InicioView from '../views/InicioView.vue'
import LugaresView from '../views/LugaresView.vue'
import EmergenciaView from '../views/EmergenciaView.vue'
import SeguridadView from '../views/SeguridadView.vue'
import PresupuestoView from '../views/PresupuestoView.vue'
import ItinerarioView from '../views/ItinerarioView.vue'
import TransporteView from '../views/TransporteView.vue'



const routes = [
  {
    path: '/',
    name: 'inicio',
    component: InicioView
  },
  
  {
    path: '/lugares',
    name: 'lugares',
    component: LugaresView
  },
  {
    path: '/emergencia',
    name: 'emergencia',
    component: EmergenciaView
  },
  {
    path: '/seguridad',
    name: 'seguridad',
    component: SeguridadView
  },
  {
    path: '/presupuesto',
    name: 'presupuesto',
    component: PresupuestoView
  },
  {
    path: '/itinerario',
    name: 'itinerario',
    component: ItinerarioView
  },
  {
    path: '/transporte',
    name: 'transporte',
    component: TransporteView
  },

  {
    path: '/inicio',
    name: 'inicio-alt',
    component: InicioView
  },
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
