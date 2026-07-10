<template>
  <div>
    <h2>Dashboard</h2>

    <!-- STATS -->
    <div class="stats">
      <div class="card">
        <h2>{{ data.total_students }}</h2>
        <p>Total Students</p>
      </div>

      <div class="card">
        <h2>{{ data.total_companies }}</h2>
        <p>Total Companies</p>
      </div>

      <div class="card highlight">
        <h2>{{ data.total_jobs }}</h2>
        <p>Total Jobs</p>
      </div>

      <div class="card">
        <h2>{{ data.total_applications }}</h2>
        <p>Applications</p>
      </div>
    </div>

    <!-- COMPANY APPROVAL -->
    <div class="table-box">
      <h3>Companies</h3>

      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Industry</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="c in data.companies" :key="c.id">
            <td>{{ c.company_name }}</td>
            <td>{{ c.email }}</td>
            <td>{{ c.industry }}</td>

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

const data = ref({
  total_students: 0,
  total_companies: 0,
  total_jobs: 0,
  total_applications: 0,
  companies: [],
});

const loadDashboard = async () => {
  try {
    const res = await api.get("/admin/dashboard");
    data.value = res.data;
  } catch (err) {
    alert(err.response?.data?.error || "Failed to load admin dashboard");
  }
};

onMounted(loadDashboard);

// ✅ Approve company
const approve = async (id) => {
  await api.put(`/admin/approve-company/${id}`);
  loadDashboard();
};

// ✅ Remove company
const removeCompany = async (id) => {
  await api.delete(`/admin/remove-company/${id}`);
  loadDashboard();
};
</script>

<style scoped>
/* STATS */
.stats {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.card {
  flex: 1;
  background: white;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.card:hover {
  transform: translateY(-3px);
  transition: 0.2s;
}

.card.highlight {
  border-left: 5px solid orange;
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
