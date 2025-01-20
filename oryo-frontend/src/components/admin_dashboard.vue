<template>
    <div class="container">
      <h2 class="mt-4">Admin Dashboard</h2>
  
      <!-- Logout Button -->
      <button class="btn btn-danger mb-3" @click="logout">Logout</button>
  
      <div class="mb-3">
        <button class="btn btn-primary me-2" @click="selectedTab = 'users'">Manage Users</button>
        <button class="btn btn-primary me-2" @click="selectedTab = 'clients'">Manage Clients</button>
        <button class="btn btn-primary" @click="selectedTab = 'projects'">Manage Projects</button>
      </div>
  
      <!-- Users Table -->
      <div v-if="selectedTab === 'users'">
        <h3>Users</h3>
        <button class="btn btn-success mb-2" @click="showAddUserModal = true">Add User</button>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.f_name }} {{ user.l_name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.role }}</td>
              <td>
                <button class="btn btn-warning btn-sm me-2" @click="editUser(user)">Edit</button>
                <button class="btn btn-danger btn-sm" @click="deleteUser(user.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Clients Table -->
      <div v-if="selectedTab === 'clients'">
        <h3>Clients</h3>
        <button class="btn btn-success mb-2" @click="showAddClientModal = true">Add Client</button>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Address</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="client in clients" :key="client.id">
              <td>{{ client.name }}</td>
              <td>{{ client.email }}</td>
              <td>{{ client.address }}</td>
              <td>
                <button class="btn btn-warning btn-sm me-2" @click="editClient(client)">Edit</button>
                <button class="btn btn-danger btn-sm" @click="deleteClient(client.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Projects Table -->
      <div v-if="selectedTab === 'projects'">
        <h3>Projects</h3>
        <button class="btn btn-success mb-2" @click="showAddProjectModal = true">Add Project</button>
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Description</th>
              <th>PO Number</th>
              <th>Client</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="project in projects" :key="project.id">
              <td>{{ project.description }}</td>
              <td>{{ project.po_number }}</td>
              <td>{{ getClientName(project.client_id) }}</td>
              <td>
                <button class="btn btn-warning btn-sm me-2" @click="editProject(project)">Edit</button>
                <button class="btn btn-danger btn-sm" @click="deleteProject(project.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Modals for Adding -->
      <AddUserModal v-if="showAddUserModal" @close="showAddUserModal = false" @refresh="fetchUsers" />
      <AddClientModal v-if="showAddClientModal" @close="showAddClientModal = false" @refresh="fetchClients" />
      <AddProjectModal v-if="showAddProjectModal" @close="showAddProjectModal = false" @refresh="fetchProjects" />
  
      <!-- Edit User Modal -->
      <EditUserModal v-if="showEditUserModal" :user="selectedUser" @close="showEditUserModal = false" @refresh="fetchUsers" />
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import AddUserModal from "../components/add_user_model.vue";
  import EditUserModal from "../components/edit_user_model.vue";
  import AddClientModal from "../components/add_client_model.vue";
  import AddProjectModal from "../components/add_project_model.vue";
  
  export default {
    components: { AddUserModal, EditUserModal, AddClientModal, AddProjectModal },
    data() {
      return {
        selectedTab: "users", 
        users: [],
        clients: [],
        projects: [],
        showAddUserModal: false,
        showEditUserModal: false,
        showAddClientModal: false,
        showAddProjectModal: false,
        selectedUser: null,
      };
    },
    methods: {
      async fetchUsers() {
        try {
          const token = localStorage.getItem("token");
          const response = await axios.get("http://127.0.0.1:5001/admin/users", {
            headers: { Authorization: `Bearer ${token}` },
          });
          this.users = response.data;
        } catch (error) {
          console.error("Error fetching users:", error);
        }
      },
      async fetchClients() {
        try {
          const token = localStorage.getItem("token");
          const response = await axios.get("http://127.0.0.1:5001/admin/clients", {
            headers: { Authorization: `Bearer ${token}` },
          });
          this.clients = response.data;
        } catch (error) {
          console.error("Error fetching clients:", error);
        }
      },
      async fetchProjects() {
        try {
          const token = localStorage.getItem("token");
          const response = await axios.get("http://127.0.0.1:5001/admin/projects", {
            headers: { Authorization: `Bearer ${token}` },
          });
          this.projects = response.data;
        } catch (error) {
          console.error("Error fetching projects:", error);
        }
      },
      async deleteUser(userId) {
        if (confirm("Are you sure you want to delete this user?")) {
          await axios.delete(`http://127.0.0.1:5001/admin/users/${userId}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
          });
          this.fetchUsers();
        }
      },
      async editUser(user) {
        this.selectedUser = user; // Store the selected user for editing
        this.showEditUserModal = true; // Trigger the modal
      },
      async deleteClient(clientId) {
        if (confirm("Are you sure you want to delete this client?")) {
          await axios.delete(`http://127.0.0.1:5001/admin/clients/${clientId}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
          });
          this.fetchClients();
        }
      },
      async deleteProject(projectId) {
        if (confirm("Are you sure you want to delete this project?")) {
          await axios.delete(`http://127.0.0.1:5001/admin/projects/${projectId}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
          });
          this.fetchProjects();
        }
      },
      logout() {
        // Clear localStorage
        localStorage.removeItem("token");
        localStorage.removeItem("Id");
        localStorage.removeItem("role");
        localStorage.removeItem("email");
        localStorage.removeItem("department");
  
        // Redirect to login page
        this.$router.push("/");
      },
      getClientName(clientId) {
        const client = this.clients.find(client => client.id === clientId);
        return client ? client.name : "Unknown";
      },
    },
    mounted() {
      this.fetchUsers();
      this.fetchClients();
      this.fetchProjects();
    },
  };
  </script>
  