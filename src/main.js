import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import MenuComponent from './components/MenuComponent.vue'
import CardComponent from './components/CardComponent.vue'
import QuickAccessComponent from './components/QuickAccessComponent.vue'
const app = createApp(App).use(router);

app.component("MenuComponent", MenuComponent);
app.component("CardComponent", CardComponent);
app.component("QuickAccessComponent", QuickAccessComponent)
app.mount('#app');
