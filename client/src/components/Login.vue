<template>
  <div class="container">
    <div class="row">
      <div class="col-4"></div>
      <div class="col-4">
        <div class="container-fluid border">
          <div class="container">
            <h2 class="my-3">
              Login
            </h2>
            <p>Faça login para continuar:</p>
            <hr>
            <div>
              <b-form class="my-4" @submit="onSubmitUserCredentials">
                <b-form-group
                  id="input-group-1"
                  label="Nome de Usuário:"
                  label-for="input-1"
                >
                  <b-form-input
                    id="input-1"
                    v-model="userLoginForm.username"
                    type="text"
                    required
                  ></b-form-input>
                </b-form-group>

                <b-form-group id="input-group-2" label="Senha:" label-for="input-2">
                  <b-form-input
                    id="input-2"
                    v-model="userLoginForm.password"
                    type="password"
                    required
                  ></b-form-input>
                </b-form-group>
                <div class="text-right my-4">
                  <router-link to="/register">
                    <b-button class="mx-2">Cadastre-se</b-button>
                  </router-link>
                <b-button type="submit" variant="primary">Fazer Login</b-button>
                </div>
              </b-form>
            </div>
          </div>
        </div>
      </div>
      <div class="col-4"></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: [],
      userLoginForm: {
        username: '',
        password: '',
      },
      userLogged: JSON.parse(localStorage.getItem('userAccount')),
    };
  },
  methods: {
    onSubmitUserCredentials(evt) {
      evt.preventDefault();
      const userLoginPayload = {
        username: this.userLoginForm.username,
        password: this.userLoginForm.password,
      };
      this.authUser(userLoginPayload);
    },
    authUser(userLoginPayload) {
      const path = 'http://localhost:8000/user/login';
      axios.post(path, userLoginPayload)
        .then((res) => {
          this.user = res.data;
          if (this.user.id) {
            this.$router.push({ name: 'Home', params: { user: this.user.id, username: this.user.username } });
          }
        });
    },
  },
  mounted() {
    if (this.userLogged) {
      this.$router.push('home');
    }
  },
};
</script>
