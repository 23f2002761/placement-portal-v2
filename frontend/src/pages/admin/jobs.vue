```vue id="k3u7dn"
<template>
  <div>
    <h2>Jobs</h2>

    <div class="table-box">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Company ID</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="job in jobs" :key="job.id">
            <td>{{ job.id }}</td>
            <td>{{ job.title }}</td>
            <td>{{ job.company_id }}</td>

            <td>
              <span :class="['status', job.status]">
                {{ job.status }}
              </span>
            </td>

            <td>
              <button
                v-if="job.status === 'pending'"
                @click="updateStatus(job.id, 'approved')"
              >
                Approve
              </button>

              <button
                v-if="job.status === 'pending'"
                class="reject"
                @click="updateStatus(job.id, 'rejected')"
              >
                Reject
              </button>

              <button class="danger" @click="removeJob(job.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>

      <p v-if="jobs.length === 0">No jobs found</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../services/api";

const jobs = ref([]);

const loadJobs = async () => {
  const res = await api.get("/admin/jobs");
  jobs.value = res.data;
};

onMounted(loadJobs);

// approve/reject
const updateStatus = async (id, status) => {
  await api.put(`/admin/job/${id}/status`, { status });
  loadJobs();
};

// delete
const removeJob = async (id) => {
  if (!confirm("Are you sure you want to delete this job?")) return;

  await api.delete(`/admin/remove-job/${id}`);
  loadJobs();
};
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
.status.approved {
  color: green;
}

.status.pending {
  color: orange;
}

.status.rejected {
  color: red;
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
