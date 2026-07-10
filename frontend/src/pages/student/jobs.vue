```vue
<template>
  <div>
    <h2>Browse Jobs</h2>

    <div class="search-box">
      <input v-model="query" placeholder="Search by title, skill, company..." />
      <button @click="searchJobs">Search</button>
      <button @click="loadJobs">Reset</button>
    </div>

    <div class="jobs">
      <div v-for="job in jobs" :key="job.id" class="job-card">
        <h3>{{ job.title }}</h3>

        <p><b>Company:</b> {{ job.company_name }}</p>
        <p><b>Skills:</b> {{ job.skills }}</p>
        <p><b>Salary:</b> {{ job.salary }}</p>

        <p v-if="job.deadline"><b>Deadline:</b> {{ job.deadline }}</p>

        <button @click="applyJob(job.id)">Apply</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../services/api";

const jobs = ref([]);
const query = ref("");

const loadJobs = async () => {
  try {
    const res = await api.get("/student/jobs");
    jobs.value = res.data;
  } catch (err) {
    alert(err.response?.data?.error || "Failed to load jobs");
  }
};

const searchJobs = async () => {
  try {
    const res = await api.get(`/student/jobs/search?q=${query.value}`);
    jobs.value = res.data;
  } catch (err) {
    alert(err.response?.data?.error || "Search failed");
  }
};

const applyJob = async (jobId) => {
  try {
    await api.post(`/student/apply/${jobId}`);
    alert("Applied successfully");
  } catch (err) {
    alert(err.response?.data?.error || "Application failed");
  }
};

onMounted(loadJobs);
</script>

<style scoped>
.search-box {
  margin-bottom: 20px;
}

.search-box input {
  padding: 10px;
  width: 300px;
  margin-right: 10px;
}

.jobs {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.job-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
}

button {
  margin-top: 10px;
  padding: 8px 12px;
  border: none;
  background: #00b894;
  color: white;
  cursor: pointer;
  border-radius: 5px;
}
</style>
```
