// src/components/AddClientModal.vue
<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>Add New Client</h3>
      <form @submit.prevent="addClient">
        <input v-model="client.name" placeholder="Client Name" required />
        <input v-model="client.email" type="email" placeholder="Client Email" required />
        <input v-model="client.address" placeholder="Address" />
        <input v-model="client.project_manager" placeholder="Project Manager" />
        <button type="submit">Add Client</button>
      </form>
      <button @click="$emit('close')">Close</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return { client: { name: "", email: "", address: "", project_manager: "" } };
  },
  methods: {
    async addClient() {
      try {
        await axios.post("http://127.0.0.1:5001/admin/clients", this.client, {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        console.error("Error adding client:", error);
      }
    },
  },
};
</script>