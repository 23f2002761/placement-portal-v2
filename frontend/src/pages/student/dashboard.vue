```vue
<template>
  <div>
    <!-- PROFILE -->
    <div class="profile">
      <h2>{{ data.student.name }}</h2>
      <p>{{ data.student.email }}</p>
    </div>

    <!-- STATS -->
    <div class="stats">
      <div class="card">
        <h3>{{ data.total_applications }}</h3>
        <p>Applications</p>
      </div>

      <div class="card">
        <h3>{{ shortlistedCount }}</h3>
        <p>Shortlisted</p>
      </div>

      <div class="card">
        <h3>{{ interviewCount }}</h3>
        <p>Interviews</p>
      </div>

      <div class="card">
        <h3>{{ offerCount }}</h3>
        <p>Offers</p>
      </div>
    </div>

    <!-- APPLICATIONS -->
    <div class="applications">
      <h3>My Applications</h3>

      <div v-if="data.applications.length === 0">No applications yet</div>

      <div v-for="app in data.applications" :key="app.id" class="job-card">
        <h4>{{ app.job_title }}</h4>
        <p>{{ app.company_name }}</p>

        <p>
          Status:
          <b>{{ app.status }}</b>
        </p>

        <p>Applied: {{ app.applied_at }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import api from "../../services/api";

const data = ref({
  student: {},
  total_applications: 0,
  applications: [],
});

onMounted(async () => {
  try {
    const res = await api.get("/student/dashboard");
    data.value = res.data;
  } catch (err) {
    alert(err.response?.data?.error || "Failed to load student dashboard");
  }
});

const shortlistedCount = computed(
  () =>
    data.value.applications.filter((a) => a.status === "shortlisted").length,
);

const interviewCount = computed(
  () => data.value.applications.filter((a) => a.status === "interview").length,
);

const offerCount = computed(
  () =>
    data.value.applications.filter(
      (a) => a.status === "selected" || a.status === "placed",
    ).length,
);
</script>

<style scoped>
.profile {
  margin-bottom: 20px;
}

.stats {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.card {
  flex: 1;
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.applications {
  background: white;
  padding: 20px;
  border-radius: 10px;
}

.job-card {
  border-bottom: 1px solid #ddd;
  padding: 10px 0;
}
</style>
```
