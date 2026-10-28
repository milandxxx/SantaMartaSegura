<template>
  <div class="admin-login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>🔐 Panel de Administración</h1>
        <p>Ingresa la contraseña para acceder</p>
      </div>
      
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="password">Contraseña</label>
          <InputText 
            id="password" 
            v-model="password" 
            type="password" 
            placeholder="Ingresa la contraseña"
            @keyup.enter="login"
          />
        </div>
        
        <p v-if="error" class="error-message">{{ error }}</p>
        
        <ButtonPrime 
          label="Entrar" 
          type="submit" 
          :loading="loading"
          class="w-full"
        />
      </form>
      
      <div class="login-footer">
        <p>Solo para administradores autorizados</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminLoginView',
  data() {
    return {
      password: '',
      error: '',
      loading: false
    };
  },
  methods: {
    async login() {
      this.error = '';
      this.loading = true;
      
      try {
        const response = await this.axios.post('https://santamartasegura-backend.onrender.com/api/admin/login', {
          password: this.password
        });
        
        if (response.data.access_token) {
          localStorage.setItem('admin_token', response.data.access_token);
          this.$router.push('/admin');
        }
      } catch (e) {
        this.error = e.response?.data?.detail || 'Contraseña incorrecta';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.admin-login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
  padding: 2rem;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 1.5rem;
  padding: 3rem 2.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  color: #134e4a;
  font-size: 1.75rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
}

.login-header p {
  color: #6b7280;
  font-size: 1rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
}

.form-group :deep(.p-inputtext) {
  padding: 0.875rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group :deep(.p-inputtext:focus) {
  border-color: #0f766e;
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.15);
  outline: none;
}

.error-message {
  background: #fef2f2;
  color: #dc2626;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  text-align: center;
}

.login-form :deep(.p-button) {
  padding: 1rem;
  font-size: 1rem;
  font-weight: 700;
  border-radius: 0.75rem;
  background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%);
  border: none;
  transition: transform 0.2s, box-shadow 0.2s;
}

.login-form :deep(.p-button:hover:not(:disabled)) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(15, 118, 110, 0.3);
}

.login-form :deep(.p-button:disabled) {
  opacity: 0.7;
}

.login-footer {
  margin-top: 2rem;
  text-align: center;
}

.login-footer p {
  color: #9ca3af;
  font-size: 0.875rem;
}
</style>