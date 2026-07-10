```vue
<template>
  <div>
    <h2>{{ data.company.name }} Dashboard</h2>

    <!-- STATS -->
    <div class="stats">
      <div class="card">
        <h2>{{ data.total_jobs }}</h2>
        <p>Total Jobs</p>
      </div>

      <div class="card">
        <h2>{{ data.total_applications }}</h2>
        <p>Total Applications</p>
      </div>

      <div class="card highlight">
        <h2>{{ data.shortlisted_candidates }}</h2>
        <p>Shortlisted</p>
      </div>
    </div>

    <!-- CREATE JOB BUTTON -->
    <button class="create-btn" @click="$router.push('/company/create-job')">
      + Create Job
    </button>

    <!-- JOB LIST -->
    <div class="table-box">
      <h3>Your Jobs</h3>

      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Skills</th>
            <th>Salary</th>
            <th>Status</th>
            <th>Applicants</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="job in data.jobs" :key="job.id">
            <td>{{ job.title }}</td>
            <td>{{ job.skills }}</td>
            <td>{{ job.salary }}</td>

            <td>
              <span :class="['status', job.status]">
                {{ job.status }}
              </span>
            </td>

            <td>{{ job.applicant_count }}</td>

            <td>
              <button
                @click="viewApplications(job.id)"
                v-if="job.status === 'approved'"
              >
                View Applications
              </button>

              <button
                class="danger"
                v-if="job.status === 'approved'"
                @click="closeJob(job.id)"
              >
                Close
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
import { useRouter } from "vue-router";

const router = useRouter();

const data = ref({
  company: {},
  total_jobs: 0,
  total_applications: 0,
  shortlisted_candidates: 0,
  jobs: [],
});

const loadDashboard = async () => {
  const res = await api.get("/company/dashboard");
  data.value = res.data;
};

onMounted(loadDashboard);

// go to applications page
const viewApplications = (jobId) => {
  router.push(`/company/job/${jobId}/applications`);
};

// close job
const closeJob = async (id) => {
  if (!confirm("Close this job?")) return;

  await api.put(`/company/job/${id}/close`);
  loadDashboard();
};
</script>

<style scoped>
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
}

.card.highlight {
  border-left: 5px solid orange;
}

.create-btn {
  margin-bottom: 20px;
  background: #0984e3;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 6px;
}

/* TABLE */
.table-box {
  background: white;
  padding: 20px;
  border-radius: 10px;
}

table {
  width: 100%;
}

th,
td {
  padding: 10px;
}

/* STATUS */
.status.approved {
  color: green;
}
.status.pending {
  color: orange;
}
.status.closed {
  color: gray;
}

/* BUTTONS */
button {
  padding: 6px 10px;
  margin-right: 5px;
  border: none;
  cursor: pointer;
}

button.danger {
  background: red;
  color: white;
}
</style>
```
