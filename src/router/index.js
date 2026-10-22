import { createRouter, createWebHistory } from 'vue-router'
import InicioView from '../views/InicioView.vue'
import LugaresView from '../views/LugaresView.vue'
import EmergenciaView from '../views/EmergenciaView.vue'
import SeguridadView from '../views/SeguridadView.vue'
import PresupuestoView from '../views/PresupuestoView.vue'
import ItinerarioView from '../views/ItinerarioView.vue'
import TransporteView from '../views/TransporteView.vue'
import AdminLoginView from '../views/AdminLoginView.vue'
import AdminPanelView from '../views/AdminPanelView.vue'


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

  // Admin routes
  {
    path: '/admin/login',
    name: 'admin-login',
    component: AdminLoginView
  },
  {
    path: '/admin',
    name: 'admin-panel',
    component: AdminPanelView,
    meta: { requiresAuth: true }
  }
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation guard for admin routes
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('admin_token');
    if (!token) {
      return next({ name: 'admin-login' });
    }
  }
  next();
});

export default router