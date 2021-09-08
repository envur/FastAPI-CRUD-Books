<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <hr><br>
        <template v-if = "this.books.length === 0">
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
        <div>
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
  </div>
</template>
<script>
import axios from 'axios';

export default {
  props: {
    userID: Number,
  },
  mounted() {
    this.getBooksByUser();
  },
  data() {
    return {
      books: [],
      BookForm: {
        id: null,
        title: '',
        author: '',
        read: false,
      },
      message: '',
      bookId: '',
      showMessage: false,
      dismissCountDown: 0,
      tituloModal: '',
      variant: '',
      botao: '',
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
      const path = `http://localhost:8000/user/${this.userID}/books/get`;
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
      const path = `http://localhost:8000/user/${this.userID}/book/add`;
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
      const path = `http://localhost:8000/user/${this.userID}/book/update/${bookID}`;
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
      const path = `http://localhost:8000/user/${this.userID}/book/delete/${bookID}`;
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
  },
};
</script>
