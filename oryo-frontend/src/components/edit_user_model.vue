<template>
    <div class="modal" v-if="user">
      <div class="modal-content">
        <h3>Edit User</h3>
  
        <label>First Name:</label>
        <input v-model="localUser.f_name" class="form-control" />
  
        <label>Last Name:</label>
        <input v-model="localUser.l_name" class="form-control" />
  
        <label>Email:</label>
        <input v-model="localUser.email" class="form-control" disabled />
  
        <label>Department:</label>
        <input v-model="localUser.department" class="form-control" />
  
        <label>Phone Number:</label>
        <input v-model="localUser.phone_number" class="form-control" />
  
        <label>Role:</label>
        <select v-model="localUser.role" class="form-control">
          <option value="General Admin">General Admin</option>
          <option value="Management">Management</option>
          <option value="Technical Support">Technical Support</option>
          <option value="On-Site Technician">On-Site Technician</option>
        </select>
  
        <button class="btn btn-success mt-2" @click="updateUser">Save</button>
        <button class="btn btn-secondary mt-2" @click="$emit('close')">Cancel</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    props: {
      user: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        // Create a local copy of the user prop to avoid direct mutation
        localUser: { ...this.user },
      };
    },
    watch: {
      // Watch for changes in the user prop to update the localUser data
      user(newUser) {
        this.localUser = { ...newUser };
      },
    },
    methods: {
      async updateUser() {
        try {
          const token = localStorage.getItem("token");
          await axios.put(`http://127.0.0.1:5001/admin/users/${this.localUser.id}`, this.localUser, {
            headers: { Authorization: `Bearer ${token}` },
          });
          this.$emit("refresh");
          this.$emit("close");
        } catch (error) {
          console.error("Error updating user:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 10px;
    width: 400px;
  }
  </style>
  