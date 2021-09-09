<template>
    <div>
      <div v-if="userId !== null && username !== null">
        <User :userID="userId" :username="username"></User>
        <Books :userID="userId"></Books>
      </div>
    </div>
</template>

<script>
import User from './Users.vue';
import Books from './Books.vue';

export default {
  data() {
    return {
      userId: null,
      username: null,
      checkedId: '',
      checkedUsername: '',
      loggedUser: [],
      // loggedUser: JSON.parse(localStorage.getItem('userAccount')),
    };
  },
  components: {
    User,
    Books,
  },
  mounted() {
    if (this.$route.params.user) {
      this.getCurrentUserByRoute();
    }
    if (localStorage.getItem('userAccount')) {
      this.getCurrentUserByLocalStorage();
    } else { this.$router.push('login'); }
  },
  methods: {
    getCurrentUserByRoute() {
      this.userId = this.$route.params.user;
      this.username = this.$route.params.username;
      this.checkedUsername = this.username;
      this.checkedId = this.userId;
      localStorage.setItem('userAccount', JSON.stringify({ username: this.checkedUsername, Id: this.checkedId }));
    },
    getCurrentUserByLocalStorage() {
      this.loggedUser = JSON.parse(localStorage.getItem('userAccount'));
      this.userId = this.loggedUser.Id;
      this.username = this.loggedUser.username;
    },
  },
};
</script>
