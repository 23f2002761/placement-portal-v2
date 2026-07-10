```vue id="0p9l7v"
<template>
  <div>
    <h2>Applications</h2>

    <div class="table-box">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Student</th>
            <th>Email</th>
            <th>Company</th>
            <th>Job</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="app in applications" :key="app.application_id">
            <td>{{ app.application_id }}</td>
            <td>{{ app.student_name }}</td>
            <td>{{ app.student_email }}</td>
            <td>{{ app.company_name }}</td>
            <td>{{ app.job_title }}</td>

            <td>
              <span :class="['status', app.status]">
                {{ app.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <p v-if="applications.length === 0">No applications found</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../services/api";

const applications = ref([]);

const loadApplications = async () => {
  const res = await api.get("/admin/applications");
  applications.value = res.data;
};

onMounted(loadApplications);
</script>

<style scoped>
h2 {
  margin-bottom: 20px;
}

/* TABLE */
table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background: #f1f3f6;
  font-weight: 600;
}

th,
td {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

tr:hover {
  background: #fafafa;
}

/* STATUS COLORS */
.status.applied {
  color: blue;
}

.status.selected {
  color: green;
}

.status.rejected {
  color: red;
}

/* buttons */

button {
  padding: 7px 12px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 13px;
  transition: 0.2s;
}

button:hover {
  opacity: 0.85;
}

button.danger {
  background: #e74c3c;
  color: white;
}

button.reject {
  background: #f39c12;
  color: white;
}
</style>
```
