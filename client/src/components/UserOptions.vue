<template>
  <div>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css">
    <b-button v-b-toggle.sidebar-right><i class="bi bi-gear-fill"></i></b-button>
    <b-sidebar id="sidebar-right" title="" shadow>
      <div class="px-3 py-2 text-center">
          <b-button variant="light" v-b-modal.modal-4>
            Atualizar meus dados
          </b-button>
          <b-button variant="light" v-b-modal.modal-3>
            Remover conta
          </b-button><br>
          <b-button variant="light" @click="logoff()">
            Sair
          </b-button>
      </div>
    </b-sidebar>
  </div>
</template>

<script>
export default {
  methods: {
    logoff() {
      localStorage.removeItem('userAccount');
      this.$router.push('login');
    },
  },
};
</script>
