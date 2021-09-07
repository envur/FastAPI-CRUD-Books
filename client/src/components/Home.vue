<template>
    <div>
      <div>
        <User :userID="loggedUser.userId" :username="loggedUser.username"></User>
        <Books :userID="loggedUser.userId"></Books>
      </div>
    </div>
</template>

<script>
import User from './Users.vue';
import Books from './Books.vue';

export default {
  data() {
    return {
      userId: this.$route.params.user,
      username: this.$route.params.username,
      checkedId: '',
      checkedUsername: '',
      loggedUser: JSON.parse(localStorage.getItem('userAccount')),
    };
  },
  components: {
    User,
    Books,
  },
  mounted() {
    this.getCurrentUser();
  },
  methods: {
    getCurrentUser() {
      if (this.userId && this.username) {
        this.checkedId = this.userId;
        this.checkedUsername = this.username;
        localStorage.setItem('userAccount', JSON.stringify({ username: this.checkedUsername, userId: this.checkedId }));
        window.location.reload();
      }
      if (!this.loggedUser.userId) {
        this.$router.push('login');
      }
    },
  },
};
</script>
