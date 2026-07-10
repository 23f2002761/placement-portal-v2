```vue
<template>
  <div>
    <h2>Students</h2>

    <!-- SEARCH -->
    <div class="search-box">
      <input v-model="query" placeholder="Search by name, email or phone..." />
      <button @click="searchStudents">Search</button>
      <button class="secondary" @click="reset">Reset</button>
    </div>

    <!-- TABLE -->
    <div class="table-box">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="s in students" :key="s.id">
            <td>{{ s.id }}</td>
            <td>{{ s.name }}</td>
            <td>{{ s.email }}</td>
            <td>{{ s.phone }}</td>

            <td>
              <button class="danger" @click="deactivate(s.user_id)">
                Deactivate
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <p v-if="students.length === 0">No students found</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "../../services/api";

const students = ref([]);
const query = ref("");

// search students
const searchStudents = async () => {
  if (!query.value) return;

  const res = await api.get(`/admin/search/students?q=${query.value}`);
  students.value = res.data;
};

// reset list
const reset = () => {
  students.value = [];
  query.value = "";
};

// deactivate user
const deactivate = async (id) => {
  await api.put(`/admin/deactivate-user/${id}`);
  alert("User deactivated");
};
</script>

<style scoped>
h2 {
  margin-bottom: 20px;
}

/* SEARCH */
.search-box {
  margin-bottom: 20px;
}

.search-box input {
  padding: 8px;
  width: 250px;
  margin-right: 10px;
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

/* BUTTONS */
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
