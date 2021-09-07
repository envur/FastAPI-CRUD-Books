<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Bem vindo de volta, {{ this.username }}!</h1>
        <div class="text-right">
          <b-button variant="danger" v-b-modal.modal-3>
            Remover conta
          </b-button>
          <b-button variant="primary" v-b-modal.modal-4>
            Atualizar meus dados
          </b-button>
          <b-button variant="secondary" @click="logoff()">
            Sair
          </b-button>
        </div>
      </div>
    </div>
    <b-modal ref="userUpdateModal" hide-footer id="modal-4" title="Atualizar minhas informações">
      <b-form @submit="onSubmitUserUpdate">
        <b-form-group
          id="input-group-1"
          label="Novo Nome de Usuário:"
          label-for="input-1"
        >
          <b-form-input
            id="input-1"
            v-model="UserFormUpdate.username"
            type="text"
          ></b-form-input>
        </b-form-group>
        <b-form-group
          id="input-group-1"
          label="Novo E-mail:"
          label-for="input-1"
        >
          <b-form-input
            id="input-1"
            v-model="UserFormUpdate.email"
            type="email"
          ></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">
          Atualizar
        </b-button>
      </b-form>
    </b-modal>
    <b-modal ref="userDeleteModal" hide-footer id="modal-3" title="Exclusão de usuário">
      <p>Você tem certeza que deseja excluir sua conta?
        Todos os seus livros cadastrados serão perdidos</p>
      <div class="text-right">
        <b-button variant="danger" @click="deleteUser">Excluir</b-button>
        <b-button>Cancelar</b-button>
      </div>
    </b-modal>
  </div>
</template>
<script>
import axios from 'axios';

export default {
  props: {
    userID: Number,
    username: String,
  },
  data() {
    return {
      UserFormUpdate: {
        username: '',
        email: '',
      },
    };
  },
  created() {
    this.get_user();
    console.log(this.userInfo);
  },
  methods: {
    onSubmitUserUpdate(evt) {
      evt.preventDefault();
      this.$refs.userUpdateModal.hide();
      const userUpdatePayload = {
        items: {
          username: this.UserFormUpdate.username,
          email: this.UserFormUpdate.email,
        },
      };
      this.updateUser(userUpdatePayload);
    },
    get_user() {
      const path = `http://localhost:8000/user/${this.userID}`;
      axios.get(path)
        .then((res) => {
          this.UserFormUpdate.username = res.data.username;
          this.UserFormUpdate.email = res.data.email;
        });
    },
    deleteUser() {
      const path = `http://localhost:8000/user/delete/${this.userID}`;
      axios.delete(path)
        .then(() => {
          this.$refs.userDeleteModal.hide();
          this.$router.push('login');
        });
    },
    updateUser(userUpdatePayload) {
      const path = `http://localhost:8000/user/update/${this.userID}`;
      axios.put(path, userUpdatePayload)
        .then(() => {
          this.$refs.userUpdateModal.hide();
        });
    },
    logoff() {
      localStorage.removeItem('userAccount');
      this.$router.push('login');
    },
  },
};
</script>
