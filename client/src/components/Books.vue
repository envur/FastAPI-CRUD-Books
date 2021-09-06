<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Livros</h1>
        <div class="text-right" v-if="userID">
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
        <div v-if="!userID" class="text-right">
          <b-button v-b-modal.modal-1>
          Registrar-se
          </b-button>
          <b-button variant="primary" v-b-modal.modal-2>Fazer Login
          </b-button>
        </div>
        <hr><br>
        <template v-if = "this.books.length === 0 && userID">
        <h4>
        Não há livros cadastrados!</h4><br>
        </template>
        <b-alert
            :variant = "variant"
            :show="dismissCountDown"
            dismissible
            @dismissed="dismissCountDown=0"
            @dismiss-count-down="countDownChanged"
            >{{ message }}
        </b-alert>
        <div v-if="userID">
          <button type="button" class="btn btn-success btn-sm" v-b-modal.book-modal
          @click="onShowModalInsert">Adicionar Livro</button>
          <br><br>
        </div>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Título</th>
              <th scope="col">Autor</th>
              <th scope="col">Lido?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr  v-for="(book, index) in books" :key="index">
              <td>{{ book.title }}</td>
              <td>{{ book.author }}</td>
              <td>
                <span v-if="book.read">Sim</span>
                <span v-else>Não</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.book-modal
                          @click="editBook(book)">
                      Editar
                  </button>
                  <b-button type="button" class="btn btn-danger btn-sm"
                      @click="onShowDelete(book.id)">
                      Remover
                  </b-button>
                </div>
              </td>
            </tr>
            <b-modal ref="delBookModal"
                     id="modal-del"
                     title="Remover livro"
                     hide-footer>
                    <template>
                        Excluir Livro?
                    </template>
                    <div class="d-block text-center">
                      <b-button-group>
                        <button type="button" class="btn btn-danger btn-md"
                        @click ="onDeleteBook">
                        Excluir</button>
                        <button type="reset" class="btn btn-secondary btn-md"
                        @click="onReset">
                        Cancelar</button>
                      </b-button-group>
                    </div>
            </b-modal>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="BookModal"
            id="book-modal"
            :title = "tituloModal"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-title-edit-group"
                    label="Título:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="BookForm.title"
                        required
                        placeholder="Insira o título">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Autor:"
                      label-for="form-author-edit-input">
            <b-form-input id="form-author-edit-input"
                          type="text"
                          v-model="BookForm.author"
                          required
                          placeholder="Insira o autor">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-read-edit-group">
            <b-form-checkbox v-model="BookForm.read"
            value="true">Lido?</b-form-checkbox>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">{{ botao }}</b-button>
          <b-button type="reset" variant="secondary">Cancelar</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
    <b-modal ref="userRegisterModal" hide-footer id="modal-1" title="Registrar-se">
      <b-form @submit="onSubmitUser">
        <b-form-group
          id="input-group-1"
          label="Nome de Usuário:"
          label-for="input-1"
        >
          <b-form-input
            id="input-1"
            v-model="UserFormRegister.username"
            type="text"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          id="input-group-1"
          label="E-mail:"
          label-for="input-1"
        >
          <b-form-input
            id="input-1"
            v-model="UserFormRegister.email"
            type="email"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          id="input-group-1"
          label="Senha:"
          label-for="input-1"
          description="Escolha uma senha segura."
        >
          <b-form-input
            id="input-1"
            v-model="UserFormRegister.password"
            type="password"
            required
          ></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">
          Registrar
        </b-button>
      </b-form>
    </b-modal>
    <b-modal ref="userLoginModal" hide-footer id="modal-2" title="Fazer Login">
      <b-form @submit="onSubmitUserCredentials">
        <b-form-group
          id="input-group-1"
          label="Usuário:"
          label-for="input-1"
        >
          <b-form-input
            id="input-1"
            v-model="UserFormLogin.username"
            type="text"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          id="input-group-1"
          label="Senha:"
          label-for="input-1"
        >
          <b-form-input
            id="input-1"
            v-model="UserFormLogin.password"
            type="password"
            required
          ></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">
          Login
        </b-button>
      </b-form>
    </b-modal>
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
  data() {
    return {
      books: [],
      BookForm: {
        id: null,
        title: '',
        author: '',
        read: false,
      },
      user: [],
      UserFormRegister: {
        username: '',
        email: '',
        password: '',
      },
      UserFormLogin: {
        username: '',
        password: '',
      },
      UserFormUpdate: {
        username: '',
        email: '',
      },
      message: '',
      bookId: '',
      showMessage: false,
      dismissCountDown: 0,
      tituloModal: '',
      variant: '',
      botao: '',
      userID: '',
    };
  },
  components: {
  },
  methods: {
    onShowDelete(bookId) {
      this.bookId = bookId;
      this.$bvModal.show('modal-del');
    },
    onShowModalInsert() {
      this.tituloModal = 'Adicionar Livro';
      this.botao = 'Adicionar';
      this.initForm();
    },
    showAlert(message, variant) {
      this.dismissCountDown = 5;
      this.variant = variant;
      this.message = message;
    },
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown;
    },
    getBooksByUser() {
      const path = `http://localhost:8000/${this.userID}/books/get`;
      axios.get(path)
        .then((res) => {
          this.books = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addBook(payload) {
      console.log(payload);
      const path = `http://localhost:8000/${this.userID}/book/add`;
      axios.post(path, payload)
        .then(() => {
          this.getBooksByUser();
          this.showAlert('Livro Adicionado!', 'info');
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBooksByUser();
        });
    },
    updateBook(payload, bookID) {
      const path = `http://localhost:8000/${this.userID}/book/update/${bookID}`;
      axios.put(path, payload)
        .then(() => {
          this.getBooksByUser();
          this.showAlert('Livro Atualizado!', 'primary');
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooksByUser();
        });
    },
    initForm() {
      this.BookForm.title = '';
      this.BookForm.author = '';
      this.BookForm.read = false;
      this.BookForm.id = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.BookModal.hide();
      let read = false;
      if (this.BookForm.read) read = true;
      const payload = {
        book: {
          title: this.BookForm.title,
          author: this.BookForm.author,
          read,
        },
      };
      if (this.tituloModal === 'Adicionar Livro') {
        this.addBook(payload, this.userID);
      } else {
        this.updateBook(payload, this.BookForm.id, this.userID);
      }
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.delBookModal.hide();
      this.initForm();
    },
    editBook(book) {
      this.tituloModal = 'Alterar';
      this.botao = 'Atualizar';
      this.BookForm = book;
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.BookModal.hide();
      this.initForm();
      this.getBooksByUser();
    },
    removeBook(bookID) {
      const path = `http://localhost:8000/${this.userID}/book/delete/${bookID}`;
      axios.delete(path)
        .then(() => {
          this.getBooksByUser();
          this.showAlert('Livro Removido!', 'info');
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooksByUser();
        });
    },
    onDeleteBook() {
      this.removeBook(this.bookId);
      this.$bvModal.hide('modal-del');
    },
    onSubmitUser(evt) {
      evt.preventDefault();
      this.$refs.userRegisterModal.hide();
      const userPayload = {
        user: {
          username: this.UserFormRegister.username,
          email: this.UserFormRegister.email,
          password: this.UserFormRegister.password,
        },
      };
      console.log(userPayload);
      this.addUser(userPayload);
      this.initForm();
    },
    onSubmitUserCredentials(evt) {
      evt.preventDefault();
      this.$refs.userLoginModal.hide();
      const userLoginPayload = {
        username: this.UserFormLogin.username,
        password: this.UserFormLogin.password,
      };
      this.authUser(userLoginPayload);
      this.initForm();
    },
    onSubmitUserUpdate(evt) {
      evt.preventDefault();
      this.$refs.userLoginModal.hide();
      const userUpdatePayload = {
        items: {
          username: this.UserFormUpdate.username,
          email: this.UserFormUpdate.email,
        },
      };
      this.updateUser(userUpdatePayload);
      this.initForm();
    },

    addUser(userPayload) {
      const path = 'http://localhost:8000/user/register';
      axios.post(path, userPayload)
        .then(() => {
          this.showAlert('Usuário adicionado, faça login para adicionar livros', 'primary');
          this.showMessage = true;
        });
      this.UserFormRegister.username = '';
      this.UserFormRegister.email = '';
      this.UserFormRegister.password = '';
    },
    authUser(userLoginPayload) {
      const path = 'http://localhost:8000/user/login';
      axios.post(path, userLoginPayload)
        .then((res) => {
          this.user = res.data;
          if (this.user) {
            this.showAlert('Logado com sucesso!', 'success');
            this.showMessage = true;
            this.userLoggedIn = true;
            this.userID = this.user.id;
            this.getBooksByUser();
          }
          if (!this.user) {
            this.showAlert('Login falhou', 'danger');
            this.showMessage = true;
            this.userLoggedIn = false;
          }
        });
    },
    deleteUser() {
      const path = `http://localhost:8000/user/delete/${this.userID}`;
      axios.delete(path)
        .then(() => {
          this.$refs.userDeleteModal.hide();
          this.showAlert('Usuário Removido!', 'info');
          this.showMessage = true;
          this.user = [];
          this.userID = '';
          window.location.reload();
        });
    },
    updateUser(userUpdatePayload) {
      const path = `http://localhost:8000/user/update/${this.userID}`;
      axios.put(path, userUpdatePayload)
        .then(() => {
          this.$refs.userUpdateModal.hide();
          this.showAlert('Usuário Atualizado!', 'info');
          this.showMessage = true;
        });
    },
    logoff() {
      window.location.reload();
    },
  },
};
</script>
