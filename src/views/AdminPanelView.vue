<template>
  <div class="admin-panel">
    <header class="admin-header">
      <div class="header-left">
        <h1>🔐 Panel de Administración</h1>
        <span class="badge">Admin</span>
      </div>
      <div class="header-right">
        <ButtonPrime 
          label="Ver sitio" 
          variant="outlined" 
          @click="goToSite"
          icon="pi pi-external-link"
        />
        <ButtonPrime 
          label="Cerrar sesión" 
          severity="secondary" 
          variant="outlined" 
          @click="logout"
          icon="pi pi-sign-out"
        />
      </div>
    </header>

    <nav class="admin-tabs" role="tablist">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab-btn', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
        role="tab"
        :aria-selected="activeTab === tab.id"
      >
        {{ tab.icon }} {{ tab.label }}
      </button>
    </nav>

    <main class="admin-content">
      <!-- LUGARES TAB -->
      <div v-if="activeTab === 'lugares'" class="tab-panel" role="tabpanel">
        <div class="panel-header">
          <h2>Gestión de Lugares</h2>
          <ButtonPrime 
            label="Nuevo lugar" 
            icon="pi pi-plus" 
            @click="openLugarDialog(null)"
          />
        </div>

        <DataTablePrime 
          :value="lugares" 
          :loading="loadingLugares"
          :paginator="true"
          :rows="10"
          :rowsPerPageOptions="[10, 25, 50]"
          responsiveLayout="scroll"
        >
          <ColumnPrime field="nombre" header="Nombre" :sortable="true" />
          <ColumnPrime field="categoria" header="Categoría" :sortable="true">
            <template #body="slotProps">
              <TagPrime :value="slotProps.data.categoria" :severity="getCategoriaSeverity(slotProps.data.categoria)" />
            </template>
          </ColumnPrime>
          <ColumnPrime field="precio" header="Precio (COP)" :sortable="true">
            <template #body="slotProps">
              ${{ formato(slotProps.data.precio) }}
            </template>
          </ColumnPrime>
          <ColumnPrime field="seguridad" header="Seguridad" :sortable="true">
            <template #body="slotProps">
              <TagPrime :value="slotProps.data.seguridad" :severity="slotProps.data.seguridad === 'verde' ? 'success' : slotProps.data.seguridad === 'amarillo' ? 'warning' : 'danger'" />
            </template>
          </ColumnPrime>
          <ColumnPrime field="detalle" header="Detalle" style="max-width: 300px">
            <template #body="slotProps">
              <span class="text-truncate" style="display: block; max-width: 300px;">{{ slotProps.data.detalle }}</span>
            </template>
          </ColumnPrime>
          <ColumnPrime header="Acciones" style="width: 120px">
            <template #body="slotProps">
              <div class="action-buttons">
                <ButtonPrime 
                  icon="pi pi-pencil" 
                  severity="secondary" 
                  size="small" 
                  @click="openLugarDialog(slotProps.data)"
                />
                <ButtonPrime 
                  icon="pi pi-trash" 
                  severity="danger" 
                  size="small" 
                  @click="confirmDeleteLugar(slotProps.data)"
                />
              </div>
            </template>
          </ColumnPrime>
        </DataTablePrime>
      </div>

      <!-- ALERTAS TAB -->
      <div v-if="activeTab === 'alertas'" class="tab-panel" role="tabpanel">
        <div class="panel-header">
          <h2>Gestión de Alertas</h2>
          <ButtonPrime 
            label="Nueva alerta" 
            icon="pi pi-plus" 
            @click="openAlertaDialog(null)"
          />
        </div>

        <DataTablePrime 
          :value="alertas" 
          :loading="loadingAlertas"
          :paginator="true"
          :rows="10"
          :rowsPerPageOptions="[10, 25, 50]"
          responsiveLayout="scroll"
        >
          <ColumnPrime field="tipo" header="Tipo" :sortable="true">
            <template #body="slotProps">
              <TagPrime :value="slotProps.data.tipo" severity="info" />
            </template>
          </ColumnPrime>
          <ColumnPrime field="titulo" header="Título" :sortable="true" />
          <ColumnPrime field="mensaje" header="Mensaje" style="max-width: 400px">
            <template #body="slotProps">
              <span class="text-truncate" style="display: block; max-width: 400px;">{{ slotProps.data.mensaje }}</span>
            </template>
          </ColumnPrime>
          <ColumnPrime header="Acciones" style="width: 100px">
            <template #body="slotProps">
              <ButtonPrime 
                icon="pi pi-trash" 
                severity="danger" 
                size="small" 
                @click="confirmDeleteAlerta(slotProps.data)"
              />
            </template>
          </ColumnPrime>
        </DataTablePrime>
      </div>

      <!-- EMERGENCIAS TAB -->
      <div v-if="activeTab === 'emergencias'" class="tab-panel" role="tabpanel">
        <div class="panel-header">
          <h2>Contactos de Emergencia</h2>
          <ButtonPrime 
            label="Nuevo contacto" 
            icon="pi pi-plus" 
            @click="openEmergenciaDialog(null)"
          />
        </div>

        <DataTablePrime 
          :value="emergencias" 
          :loading="loadingEmergencias"
          :paginator="true"
          :rows="10"
          :rowsPerPageOptions="[10, 25, 50]"
          responsiveLayout="scroll"
        >
          <ColumnPrime field="nombre" header="Nombre" :sortable="true" />
          <ColumnPrime field="telefono" header="Teléfono" :sortable="true" />
          <ColumnPrime header="Acciones" style="width: 100px">
            <template #body="slotProps">
              <div class="action-buttons">
                <ButtonPrime 
                  icon="pi pi-pencil" 
                  severity="secondary" 
                  size="small" 
                  @click="openEmergenciaDialog(slotProps.data)"
                />
                <ButtonPrime 
                  icon="pi pi-trash" 
                  severity="danger" 
                  size="small" 
                  @click="confirmDeleteEmergencia(slotProps.data)"
                />
              </div>
            </template>
          </ColumnPrime>
        </DataTablePrime>
      </div>
    </main>

    <!-- LUGAR DIALOG -->
    <DialogPrime 
      v-model:visible="lugarDialogVisible" 
      :header="lugarEditing ? 'Editar lugar' : 'Nuevo lugar'" 
      :modal="true" 
      :style="{ width: '500px' }"
    >
      <form @submit.prevent="saveLugar" class="dialog-form">
        <div class="field">
          <LabelPrime for="lugar-nombre">Nombre *</LabelPrime>
          <InputText id="lugar-nombre" v-model="lugarForm.nombre" required autofocus />
        </div>
        <div class="field">
          <LabelPrime for="lugar-categoria">Categoría</LabelPrime>
          <SelectPrime 
            id="lugar-categoria" 
            v-model="lugarForm.categoria" 
            :options="categorias" 
            optionLabel="label" 
            optionValue="value" 
            placeholder="Seleccionar"
          />
        </div>
        <div class="field">
          <LabelPrime for="lugar-imagen">URL Imagen</LabelPrime>
          <InputText id="lugar-imagen" v-model="lugarForm.imagen" placeholder="https://..." />
        </div>
        <div class="field">
          <LabelPrime for="lugar-precio">Precio (COP)</LabelPrime>
          <InputNumber 
            id="lugar-precio" 
            v-model="lugarForm.precio" 
            :min="0" 
            :step="1000"
            placeholder="0"
          />
        </div>
        <div class="field">
          <LabelPrime for="lugar-seguridad">Nivel de seguridad</LabelPrime>
          <SelectPrime 
            id="lugar-seguridad" 
            v-model="lugarForm.seguridad" 
            :options="seguridadOptions" 
            optionLabel="label" 
            optionValue="value" 
            placeholder="Seleccionar"
          />
        </div>
        <div class="field">
          <LabelPrime for="lugar-detalle">Detalle</LabelPrime>
          <Textarea 
            id="lugar-detalle" 
            v-model="lugarForm.detalle" 
            rows="4" 
            placeholder="Descripción del lugar..."
          />
        </div>
        <div class="dialog-footer">
          <ButtonPrime label="Cancelar" variant="outlined" @click="lugarDialogVisible = false" />
          <ButtonPrime 
            :label="lugarEditing ? 'Actualizar' : 'Crear'" 
            type="submit" 
            :loading="savingLugar"
          />
        </div>
      </form>
    </DialogPrime>

    <!-- ALERTA DIALOG -->
    <DialogPrime 
      v-model:visible="alertaDialogVisible" 
      :header="alertaEditing ? 'Editar alerta' : 'Nueva alerta'" 
      :modal="true" 
      :style="{ width: '500px' }"
    >
      <form @submit.prevent="saveAlerta" class="dialog-form">
        <div class="field">
          <LabelPrime for="alerta-tipo">Tipo</LabelPrime>
          <SelectPrime 
            id="alerta-tipo" 
            v-model="alertaForm.tipo" 
            :options="alertaTipos" 
            optionLabel="label" 
            optionValue="value" 
            placeholder="Seleccionar"
          />
        </div>
        <div class="field">
          <LabelPrime for="alerta-titulo">Título *</LabelPrime>
          <InputText id="alerta-titulo" v-model="alertaForm.titulo" required />
        </div>
        <div class="field">
          <LabelPrime for="alerta-mensaje">Mensaje *</LabelPrime>
          <Textarea 
            id="alerta-mensaje" 
            v-model="alertaForm.mensaje" 
            rows="4" 
            required
            placeholder="Descripción de la alerta..."
          />
        </div>
        <div class="dialog-footer">
          <ButtonPrime label="Cancelar" variant="outlined" @click="alertaDialogVisible = false" />
          <ButtonPrime 
            :label="alertaEditing ? 'Actualizar' : 'Crear'" 
            type="submit" 
            :loading="savingAlerta"
          />
        </div>
      </form>
    </DialogPrime>

    <!-- EMERGENCIA DIALOG -->
    <DialogPrime 
      v-model:visible="emergenciaDialogVisible" 
      :header="emergenciaEditing ? 'Editar contacto' : 'Nuevo contacto de emergencia'" 
      :modal="true" 
      :style="{ width: '500px' }"
    >
      <form @submit.prevent="saveEmergencia" class="dialog-form">
        <div class="field">
          <LabelPrime for="emergencia-nombre">Nombre *</LabelPrime>
          <InputText id="emergencia-nombre" v-model="emergenciaForm.nombre" required autofocus />
        </div>
        <div class="field">
          <LabelPrime for="emergencia-telefono">Teléfono *</LabelPrime>
          <InputText id="emergencia-telefono" v-model="emergenciaForm.telefono" required placeholder="Ej: 123" />
        </div>
        <div class="dialog-footer">
          <ButtonPrime label="Cancelar" variant="outlined" @click="emergenciaDialogVisible = false" />
          <ButtonPrime 
            :label="emergenciaEditing ? 'Actualizar' : 'Crear'" 
            type="submit" 
            :loading="savingEmergencia"
          />
        </div>
      </form>
    </DialogPrime>

    <!-- CONFIRM DIALOG -->
    <ConfirmDialogPrime 
      v-model:visible="confirmDialogVisible"
      :message="confirmMessage"
      :header="confirmHeader"
      :icon="confirmIcon"
      @accept="executeConfirmedAction"
    />
  </div>
</template>

<script>
export default {
  name: 'AdminPanelView',
  data() {
    return {
      activeTab: 'lugares',
      tabs: [
        { id: 'lugares', label: 'Lugares', icon: '📍' },
        { id: 'alertas', label: 'Alertas', icon: '⚠️' },
        { id: 'emergencias', label: 'Emergencias', icon: '🚨' }
      ],
      
      // Lugares
      lugares: [],
      loadingLugares: false,
      lugarDialogVisible: false,
      lugarEditing: false,
      savingLugar: false,
      lugarForm: { nombre: '', categoria: 'playa', imagen: '', precio: 0, seguridad: 'verde', detalle: '' },
      categorias: [
        { label: 'Playa', value: 'playa' },
        { label: 'Naturaleza', value: 'naturaleza' },
        { label: 'Cultura', value: 'cultura' },
        { label: 'Gastronomía', value: 'gastronomia' }
      ],
      seguridadOptions: [
        { label: '🟢 Verde (Seguro)', value: 'verde' },
        { label: '🟡 Amarillo (Precaución)', value: 'amarillo' },
        { label: '🔴 Rojo (Alto riesgo)', value: 'rojo' }
      ],
      
      // Alertas
      alertas: [],
      loadingAlertas: false,
      alertaDialogVisible: false,
      alertaEditing: false,
      savingAlerta: false,
      alertaForm: { tipo: 'clima', titulo: '', mensaje: '' },
      alertaTipos: [
        { label: 'Clima', value: 'clima' },
        { label: 'Movilidad', value: 'movilidad' },
        { label: 'Seguridad', value: 'seguridad' },
        { label: 'General', value: 'general' }
      ],
      
      // Emergencias
      emergencias: [],
      loadingEmergencias: false,
      emergenciaDialogVisible: false,
      emergenciaEditing: false,
      savingEmergencia: false,
      emergenciaForm: { nombre: '', telefono: '' },
      
      // Confirm dialog
      confirmDialogVisible: false,
      confirmMessage: '',
      confirmHeader: 'Confirmar',
      confirmIcon: 'pi pi-exclamation-triangle',
      confirmAction: null,
      confirmData: null
    };
  },
  mounted() {
    this.checkAuth();
    this.loadAll();
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('admin_token');
      if (!token) {
        this.$router.push('/admin/login');
        return;
      }
      // Verificar token con el backend
      this.axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      this.axios.get('http://localhost:8000/api/admin/verify')
        .catch(() => {
          localStorage.removeItem('admin_token');
          this.$router.push('/admin/login');
        });
    },
    
    async loadAll() {
      await Promise.all([
        this.loadLugares(),
        this.loadAlertas(),
        this.loadEmergencias()
      ]);
    },
    
    // LUGARES
    async loadLugares() {
      this.loadingLugares = true;
      try {
        const response = await this.axios.get('http://localhost:8000/api/lugares');
        this.lugares = response.data.respuesta || [];
      } catch (e) {
        console.error('Error cargando lugares:', e);
      } finally {
        this.loadingLugares = false;
      }
    },
    
    openLugarDialog(lugar) {
      this.lugarEditing = !!lugar;
      if (lugar) {
        this.lugarForm = { ...lugar };
      } else {
        this.lugarForm = { nombre: '', categoria: 'playa', imagen: '', precio: 0, seguridad: 'verde', detalle: '' };
      }
      this.lugarDialogVisible = true;
    },
    
    async saveLugar() {
      this.savingLugar = true;
      try {
        if (this.lugarEditing) {
          await this.axios.put(`http://localhost:8000/api/lugares/${this.lugarForm.id}`, this.lugarForm);
        } else {
          await this.axios.post('http://localhost:8000/api/lugares', this.lugarForm);
        }
        this.lugarDialogVisible = false;
        await this.loadLugares();
      } catch (e) {
        alert(e.response?.data?.detail || 'Error al guardar');
      } finally {
        this.savingLugar = false;
      }
    },
    
    confirmDeleteLugar(lugar) {
      this.confirmHeader = 'Eliminar lugar';
      this.confirmMessage = `¿Eliminar "${lugar.nombre}"? Esta acción no se puede deshacer.`;
      this.confirmIcon = 'pi pi-trash';
      this.confirmAction = 'deleteLugar';
      this.confirmData = lugar;
      this.confirmDialogVisible = true;
    },
    
    // ALERTAS
    async loadAlertas() {
      this.loadingAlertas = true;
      try {
        const response = await this.axios.get('http://localhost:8000/api/alertas');
        this.alertas = response.data.respuesta || [];
      } catch (e) {
        console.error('Error cargando alertas:', e);
      } finally {
        this.loadingAlertas = false;
      }
    },
    
    openAlertaDialog(alerta) {
      this.alertaEditing = !!alerta;
      if (alerta) {
        this.alertaForm = { ...alerta };
      } else {
        this.alertaForm = { tipo: 'clima', titulo: '', mensaje: '' };
      }
      this.alertaDialogVisible = true;
    },
    
    async saveAlerta() {
      this.savingAlerta = true;
      try {
        if (this.alertaEditing) {
          await this.axios.put(`http://localhost:8000/api/alertas/${this.alertaForm.id}`, this.alertaForm);
        } else {
          await this.axios.post('http://localhost:8000/api/alertas', this.alertaForm);
        }
        this.alertaDialogVisible = false;
        await this.loadAlertas();
      } catch (e) {
        alert(e.response?.data?.detail || 'Error al guardar');
      } finally {
        this.savingAlerta = false;
      }
    },
    
    confirmDeleteAlerta(alerta) {
      this.confirmHeader = 'Eliminar alerta';
      this.confirmMessage = `¿Eliminar la alerta "${alerta.titulo}"?`;
      this.confirmIcon = 'pi pi-trash';
      this.confirmAction = 'deleteAlerta';
      this.confirmData = alerta;
      this.confirmDialogVisible = true;
    },
    
    // EMERGENCIAS
    async loadEmergencias() {
      this.loadingEmergencias = true;
      try {
        const response = await this.axios.get('http://localhost:8000/api/emergencias');
        this.emergencias = response.data.respuesta || [];
      } catch (e) {
        console.error('Error cargando emergencias:', e);
      } finally {
        this.loadingEmergencias = false;
      }
    },
    
    openEmergenciaDialog(emergencia) {
      this.emergenciaEditing = !!emergencia;
      if (emergencia) {
        this.emergenciaForm = { ...emergencia };
      } else {
        this.emergenciaForm = { nombre: '', telefono: '' };
      }
      this.emergenciaDialogVisible = true;
    },
    
    async saveEmergencia() {
      this.savingEmergencia = true;
      try {
        if (this.emergenciaEditing) {
          await this.axios.put(`http://localhost:8000/api/emergencias/${this.emergenciaForm.id}`, this.emergenciaForm);
        } else {
          await this.axios.post('http://localhost:8000/api/emergencias', this.emergenciaForm);
        }
        this.emergenciaDialogVisible = false;
        await this.loadEmergencias();
      } catch (e) {
        alert(e.response?.data?.detail || 'Error al guardar');
      } finally {
        this.savingEmergencia = false;
      }
    },
    
    confirmDeleteEmergencia(emergencia) {
      this.confirmHeader = 'Eliminar contacto';
      this.confirmMessage = `¿Eliminar "${emergencia.nombre}" (${emergencia.telefono})?`;
      this.confirmIcon = 'pi pi-trash';
      this.confirmAction = 'deleteEmergencia';
      this.confirmData = emergencia;
      this.confirmDialogVisible = true;
    },
    
    async executeConfirmedAction() {
      try {
        if (this.confirmAction === 'deleteLugar') {
          await this.axios.delete(`http://localhost:8000/api/lugares/${this.confirmData.id}`);
          await this.loadLugares();
        } else if (this.confirmAction === 'deleteAlerta') {
          await this.axios.delete(`http://localhost:8000/api/alertas/${this.confirmData.id}`);
          await this.loadAlertas();
        } else if (this.confirmAction === 'deleteEmergencia') {
          await this.axios.delete(`http://localhost:8000/api/emergencias/${this.confirmData.id}`);
          await this.loadEmergencias();
        }
      } catch (e) {
        alert(e.response?.data?.detail || 'Error al eliminar');
      } finally {
        this.confirmDialogVisible = false;
        this.confirmAction = null;
        this.confirmData = null;
      }
    },
    
    getCategoriaSeverity(cat) {
      const map = { playa: 'info', naturaleza: 'success', cultura: 'warning', gastronomia: 'secondary' };
      return map[cat] || 'info';
    },
    
    formato(n) {
      return Number(n).toLocaleString('es-CO');
    },
    
    goToSite() {
      this.$router.push('/');
    },
    
    logout() {
      localStorage.removeItem('admin_token');
      delete this.axios.defaults.headers.common['Authorization'];
      this.$router.push('/admin/login');
    }
  }
};
</script>

<style scoped>
.admin-panel {
  min-height: 100vh;
  background: #f8fafc;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-left h1 {
  margin: 0;
  color: #134e4a;
  font-size: 1.5rem;
  font-weight: 800;
}

.badge {
  background: linear-gradient(135deg, #0f766e, #14b8a6);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.header-right {
  display: flex;
  gap: 0.75rem;
}

.admin-tabs {
  display: flex;
  gap: 0.5rem;
  padding: 0 2rem 1rem;
  background: white;
  border-bottom: 1px solid #e2e8f0;
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: transparent;
  border: none;
  border-radius: 0.75rem;
  color: #6b7280;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-btn:hover {
  background: #f0fdfa;
  color: #0f766e;
}

.tab-btn.active {
  background: linear-gradient(135deg, #0f766e, #14b8a6);
  color: white;
}

.admin-content {
  padding: 2rem;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.panel-header h2 {
  margin: 0;
  color: #134e4a;
  font-size: 1.25rem;
  font-weight: 700;
}

.tab-panel {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

:deep(.p-datatable) {
  border: none;
}

:deep(.p-datatable .p-datatable-header) {
  display: none;
}

:deep(.p-datatable .p-column-title) {
  font-weight: 700;
  color: #374151;
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
  padding: 1rem;
}

:deep(.p-datatable .p-datatable-tbody > tr) {
  transition: background 0.15s;
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
  background: #f0fdfa;
}

:deep(.p-datatable .p-datatable-tbody > tr > td) {
  padding: 1rem;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

:deep(.p-datatable .p-paginator) {
  padding: 1rem;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.dialog-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.field label {
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

:deep(.p-inputtext, .p-inputnumber, .p-select, .p-textarea) {
  width: 100%;
}

:deep(.p-inputtext:focus, .p-inputnumber:focus, .p-select:focus, .p-textarea:focus) {
  border-color: #0f766e;
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.15);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 0.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 768px) {
  .admin-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .admin-tabs {
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }
  
  .admin-content {
    padding: 1rem;
  }
  
  .panel-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
}
</style>