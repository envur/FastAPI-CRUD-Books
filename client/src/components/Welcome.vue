<template>
  <div class="my-5 container-fluid">
    <div class="row">
        <div class="col-4"></div>
    </div>
    <div class="row">
      <div class="col-4"></div>
      <div class="col-4">
        <div class="container-fluid my-5">
          <div class="container">
            <h1 class="my-3">
                Bem-vindo(a)!
            </h1><hr>
            <p>Por favor, faça login ou cadastre-se:</p>
            <div>
                <router-link to="register">
                    <b-button>
                        Cadastrar-se
                    </b-button>
                </router-link>
                <router-link to="login">
                    <b-button class="mx-4" variant="primary">
                        Fazer Login
                    </b-button>
                </router-link>
            </div>
          </div>
        </div>
      </div>
      <div class="col-4"></div>
    </div>
  </div>
</template>

<script>
export default {
  mounted() {
    if (JSON.parse(localStorage.getItem('userAccount') !== null)) {
      this.$router.push('home');
    }
  },
};
</script>
