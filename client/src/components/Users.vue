<template>
  <div class="container">
    <UserOptions style="float:right"></UserOptions>
    <div class="row">
      <div class="col-sm-10">
        <span style="display: inline;">
        <h1>Bem vindo de volta, {{ this.username }}!</h1>
        </span>
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
            required
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
            required
          ></b-form-input>
        </b-form-group>
        <div class="text-right">
          <b-button v-b-modal.modal-5 variant="secondary">
            Redefinir Senha
          </b-button>
          <b-button type="submit" variant="primary">
            Atualizar
          </b-button>
        </div>
      </b-form>
    </b-modal>
    <b-modal ref="resetPassModal" hide-footer id="modal-5" title="Redefinir Senha">
      <b-form @submit="onSubmitUserChangePass">
        <b-form-group
          id="input-group-1"
          label="Insira sua senha atual:"
          label-for="input-1"
        >
          <b-form-input
            id="input-1"
            v-model="UserFormResetPass.oldPassword"
            type="password"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          id="input-group-1"
          label="Nova senha:"
          label-for="input-1"
        >
          <b-form-input
            id="input-1"
            v-model="UserFormResetPass.newPassword"
            type="password"
            required
          ></b-form-input>
        </b-form-group>
        <div class="text-right">
          <b-button type="submit" variant="primary">
            Redefinir
          </b-button>
        </div>
      </b-form>
    </b-modal>
    <b-modal ref="userDeleteModal" hide-footer id="modal-3" title="Exclusão de usuário">
      <p>Você tem certeza que deseja excluir sua conta?
        Todos os seus livros cadastrados serão perdidos</p>
      <div class="text-right">
        <b-button variant="danger" @click="deleteUser">Excluir</b-button>
      </div>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import UserOptions from './UserOptions.vue';

export default {
  props: {
    userID: Number,
    username: String,
  },
  components: {
    UserOptions,
  },
  data() {
    return {
      UserFormUpdate: {
        username: '',
        email: '',
      },
      UserFormResetPass: {
        oldPassword: '',
        newPassword: '',
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
    onSubmitUserChangePass(evt) {
      evt.preventDefault();
      this.$refs.userUpdateModal.hide();
      this.$refs.resetPassModal.hide();
      const userChangePassPayload = {
        items: {
          old_password: this.UserFormResetPass.oldPassword,
          new_password: this.UserFormResetPass.newPassword,
        },
      };
      this.changeUserPass(userChangePassPayload);
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
          localStorage.removeItem('userAccount');
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
    changeUserPass(userChangePassPayload) {
      const path = `http://localhost:8000/user/update/password/${this.userID}`;
      axios.put(path, userChangePassPayload)
        .then(() => {
          this.$refs.userUpdateModal.hide();
          this.$refs.resetPassModal.hide();
        });
    },
  },
};
</script>
