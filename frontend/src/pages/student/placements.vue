```vue
<template>
  <div>
    <h2>My Placements</h2>

    <div v-if="placements.length === 0">No placements yet.</div>

    <div
      v-for="placement in placements"
      :key="placement.company_name + placement.job_title"
      class="placement-card"
    >
      <h3>{{ placement.job_title }}</h3>

      <p><b>Company:</b> {{ placement.company_name }}</p>

      <p><b>Salary:</b> {{ placement.salary }}</p>

      <p>
        <b>Joining Date:</b>
        {{ placement.joining_date }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../services/api";

const placements = ref([]);

const loadPlacements = async () => {
  try {
    const res = await api.get("/student/placements");
    placements.value = res.data;
  } catch (err) {
    alert(err.response?.data?.error || "Failed to load placements");
  }
};

onMounted(loadPlacements);
</script>

<style scoped>
.placement-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 15px;
}
</style>
```
