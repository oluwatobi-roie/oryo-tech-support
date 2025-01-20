<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card shadow p-4" style="width: 350px;">
      <h3 class="text-center mb-3"> Login</h3>
      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            class="form-control"
            placeholder="Enter email"
            required
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            class="form-control"
            placeholder="Enter password"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary w-100">Login</button>
      </form>
      <p v-if="errorMessage" class="text-danger text-center mt-3">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { jwtDecode } from "jwt-decode";

export default {
name: "UserLogin",
data() {
  return {
    email: "",
    password: "",
    errorMessage: "",
  };
},
methods: {
  async login() {
    try {
      const response = await axios.post("http://127.0.0.1:5001/users/login", {
        email: this.email,
        password: this.password,
      });

      const token = response.data.access_token;

      localStorage.setItem("token", token);
      

      // Decode the token to get the user's role
      const decodedToken = jwtDecode(token);
      const userRole = decodedToken.sub.role;
      localStorage.setItem("role", userRole );

      alert("Login successful!");
      console.log(userRole)
      // Redirect user based on role
      if (userRole === "Technical Support") {
        this.$router.push("/tech-support");
      } else if (userRole === "On-Site Technician") {
        this.$router.push("/technician-dashboard");
      } else {
        this.$router.push("/default_page"); // Default dashboard
      }

    } catch (error) {
      this.errorMessage = "Invalid credentials. Please try again.";
    }
  },
},
};
</script>

<style scoped>
.card {
border-radius: 10px;
}
</style>
