<!-- // src/components/AddUserModal.vue -->
<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>Add New User</h3>
      <form @submit.prevent="addUser">
        <input v-model="user.f_name" placeholder="First Name" required />
        <input v-model="user.l_name" placeholder="Last Name" required />
        <input v-model="user.email" type="email" placeholder="Email" required />
        <input v-model="user.department" type="text" placeholder="department" required />
        <input v-model="user.phone_number" type="phone" placeholder="Phone_number" required />
        <input v-model="user.password" type="password" placeholder="Password" required />
        <select v-model="user.role">
          <option value="General Admin">General Admin</option>
          <option value="Management">Management</option>
          <option value="Technical Support">Technical Support</option>
          <option value="On-Site Technician">On-Site Technician</option>
        </select>
        <button type="submit">Add User</button>
      </form>
      <button @click="$emit('close')">Close</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      user: { f_name: "", l_name: "", email: "", password: "", role: "General Admin" },
    };
  },
  methods: {
    async addUser() {
      try {
        await axios.post("http://127.0.0.1:5001/admin/users", this.user, {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        console.error("Error adding user:", error);
      }
    },
  },
};
</script>
