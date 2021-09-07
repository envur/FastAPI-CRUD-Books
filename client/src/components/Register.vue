<template>
  <div class="container">
    <div class="row">
      <div class="col-4"></div>
      <div class="col-4">
        <div class="container-fluid border">
          <div class="container">
            <h3 class="my-3">
              Cadastrar-se
            </h3>
            <p>Preencha os campos para se registrar:</p>
            <hr>
            <div>
              <b-form class="my-4" @submit="onSubmitUser">
                <b-form-group
                  id="input-group-1"
                  label="Nome de Usuário:"
                  label-for="input-1"
                >
                  <b-form-input
                    id="input-1"
                    v-model="userRegisterForm.username"
                    type="text"
                    required
                  ></b-form-input>
                </b-form-group>

                <b-form-group
                  id="input-group-3"
                  label="Email:"
                  label-for="input-3"
                >
                  <b-form-input
                    id="input-3"
                    v-model="userRegisterForm.email"
                    type="email"
                    required
                  ></b-form-input>
                </b-form-group>

                <b-form-group id="input-group-2" label="Senha:" label-for="input-2"
                            description="Escolha uma senha segura.">
                  <b-form-input
                    id="input-2"
                    v-model="userRegisterForm.password"
                    type="password"
                    required
                  ></b-form-input>
                </b-form-group>
                <div class="text-right my-4">
                    <b-button type="submit" variant="primary">Cadastrar-se</b-button>
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
      userRegisterForm: {
        username: '',
        email: '',
        password: '',
      },
      user: [],
    };
  },

  methods: {
    onSubmitUser(evt) {
      evt.preventDefault();
      const userPayload = {
        user: {
          username: this.userRegisterForm.username,
          email: this.userRegisterForm.email,
          password: this.userRegisterForm.password,
        },
      };
      this.addUser(userPayload);
    },
    addUser(userPayload) {
      const path = 'http://localhost:8000/user/register';
      axios.post(path, userPayload)
        .then(() => {
          this.$router.push('login');
          window.location.reload();
        });
    },
  },
};
</script>
