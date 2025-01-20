<template>
    <div class="container mt-4">
      <h2>Tech Support Dashboard</h2>
      
      <div class="row mt-4">
        <div class="col-md-4">
          <button class="btn btn-primary w-100" @click="showCreateTaskModal">Create New Task</button>
        </div>
        <div class="col-md-4">
          <button class="btn btn-warning w-100" @click="fetchPendingTasks">View Awaiting Confirmation</button>
        </div>
        <div class="col-md-4">
          <button class="btn btn-success w-100" @click="fetchConfirmedTasks">View Confirmed Tasks</button>
        </div>
      </div>
      
      <!-- Task Table -->
      <div class="mt-4" v-if="tasks.length">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Client</th>
              <th>Project</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="task in tasks" :key="task.id">
              <td>{{ task.id }}</td>
              <td>{{ task.client_name }}</td>
              <td>{{ task.project_description }}</td>
              <td>{{ task.status }}</td>
              <td>
                <button class="btn btn-primary btn-sm" @click="confirmTask(task.id)" v-if="task.status === 'Pending'">Confirm</button>
                <button class="btn btn-danger btn-sm" @click="returnTask(task.id)" v-if="task.status === 'Pending'">Return</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        tasks: []
      };
    },
    methods: {
      fetchPendingTasks() {
        axios.get('/api/tasks/pending')
          .then(response => {
            this.tasks = response.data;
          })
          .catch(error => {
            console.error('Error fetching tasks:', error);
          });
      },
      confirmTask(taskId) {
        axios.post(`/api/tasks/${taskId}/confirm`)
          .then(() => {
            this.fetchPendingTasks();
          })
          .catch(error => {
            console.error('Error confirming task:', error);
          });
      },
      returnTask(taskId) {
        axios.post(`/api/tasks/${taskId}/return`)
          .then(() => {
            this.fetchPendingTasks();
          })
          .catch(error => {
            console.error('Error returning task:', error);
          });
      }
    }
  };
  </script>
  
  <style>
  .container {
    max-width: 900px;
  }
  </style>
  