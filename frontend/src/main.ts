import { createApp } from 'vue'
import 'element-plus/dist/index.css'
import App from './App.vue'
import { setupElementPlus } from './plugins/element-plus'
import { pinia } from './stores'
import router from './router'
import './assets/styles/reset.css'
import './assets/styles/variables.css'
import './assets/styles/global.css'

const app = createApp(App)

app.use(pinia)
app.use(router)
setupElementPlus(app)

app.mount('#app')
