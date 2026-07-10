```vue
<template>
  <div>
    <h2>Companies</h2>

    <!-- SEARCH -->
    <div class="search-box">
      <input v-model="query" placeholder="Search by name or industry..." />
      <button @click="searchCompanies">Search</button>
      <button class="secondary" @click="loadCompanies">Reset</button>
    </div>

    <!-- TABLE -->
    <div class="table-box">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Industry</th>
            <th>Location</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="c in companies" :key="c.id">
            <td>{{ c.company_name }}</td>
            <td>{{ c.email }}</td>
            <td>{{ c.industry }}</td>
            <td>{{ c.location }}</td>

            <td>
              <span :class="['status', c.is_approved ? 'approved' : 'pending']">
                {{ c.is_approved ? "Approved" : "Pending" }}
              </span>
            </td>

            <td>
              <button v-if="!c.is_approved" @click="approve(c.id)">
                Approve
              </button>
              <button class="danger" @click="removeCompany(c.id)">
                Remove
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../services/api";

const companies = ref([]);
const query = ref("");

// Load all companies (from dashboard API)
const loadCompanies = async () => {
  const res = await api.get("/admin/dashboard");
  companies.value = res.data.companies;
};

onMounted(loadCompanies);

// Approve
const approve = async (id) => {
  await api.put(`/admin/approve-company/${id}`);
  loadCompanies();
};

// Remove
const removeCompany = async (id) => {
  await api.delete(`/admin/remove-company/${id}`);
  loadCompanies();
};

// Search
const searchCompanies = async () => {
  if (!query.value) return loadCompanies();

  const res = await api.get(`/admin/search/companies?q=${query.value}`);

  // backend doesn't return email/location/status → normalize UI
  companies.value = res.data.map((c) => ({
    ...c,
    email: "-",
    location: "-",
    is_approved: false,
  }));
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

/* STATUS */
.status.approved {
  color: green;
}

.status.pending {
  color: orange;
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
