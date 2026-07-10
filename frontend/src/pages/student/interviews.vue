```vue
<template>
  <div>
    <h2>My Interviews</h2>

    <div v-if="interviews.length === 0">No interviews scheduled.</div>

    <div
      v-for="interview in interviews"
      :key="interview.application_id"
      class="interview-card"
    >
      <h3>{{ interview.job_title }}</h3>

      <p><b>Company:</b> {{ interview.company_name }}</p>

      <p>
        <b>Interview Date:</b>
        {{ interview.interview_date }}
      </p>

      <p>
        <b>Location:</b>
        {{ interview.interview_location }}
      </p>

      <p>
        <b>Status:</b>
        {{ interview.status }}
      </p>

      <p v-if="interview.feedback">
        <b>Feedback:</b>
        {{ interview.feedback }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../services/api";

const interviews = ref([]);

const loadInterviews = async () => {
  try {
    const res = await api.get("/student/interviews");
    interviews.value = res.data;
  } catch (err) {
    alert(err.response?.data?.error || "Failed to load interviews");
  }
};

onMounted(loadInterviews);
</script>

<style scoped>
.interview-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 15px;
}
</style>
```
