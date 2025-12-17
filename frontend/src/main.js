import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
<<<<<<< HEAD
import router from './router'
import './style.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')

=======
import router from './router.js'
import './main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.mount('#app')


>>>>>>> 694dc7c (the_last_update)
