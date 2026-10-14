import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Importar axios
import axios from 'axios'
import VueAxios from 'vue-axios'

//Importar Prime Vue
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';

import Button from 'primevue/button';
import Skeleton from 'primevue/skeleton';

import MenuComponent from './components/MenuComponent.vue'
import CardComponent from './components/CardComponent.vue'
import LugarComponent from './components/LugarComponent.vue'
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Label from 'primevue/label';

const app = createApp(App).use(router);
//Uso de axios
app.use(VueAxios, axios);

//Usar Prime-Vue
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});

app.component("MenuComponent", MenuComponent);
app.component("CardComponent", CardComponent);
app.component("LugarComponent", LugarComponent);
app.component("ButtonPrime", Button);
app.component("InputText", InputText);
app.component("LabelPrime", Label);
app.component("SkeletonPrime", Skeleton);
app.component("DialogPrime", Dialog);

app.mount('#app');
