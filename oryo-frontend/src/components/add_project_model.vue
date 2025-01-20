<template>
    <div class="modal-overlay">
      <div class="modal-content">
        <h3>Add New Project</h3>
        <form @submit.prevent="addProject">
          <input v-model="project.description" placeholder="Project Description" required />
          <input v-model="project.po_number" placeholder="PO Number" required />
          <select v-model="project.client_id">
            <option v-for="client in clients" :key="client.id" :value="client.id">{{ client.name }}</option>
          </select>
          <button type="submit">Add Project</button>
        </form>
        <button @click="$emit('close')">Close</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  export default {
    data() {
      return { project: { description: "", po_number: "", client_id: "" }, clients: [] };
    },
    async mounted() {
      const response = await axios.get("/admin/clients", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });
      this.clients = response.data;
    },
    methods: {
      async addProject() {
        try {
          await axios.post("/admin/projects", this.project, {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
          });
          this.$emit("refresh");
          this.$emit("close");
        } catch (error) {
          console.error("Error adding project:", error);
        }
      },
    },
  };
  </script>
  