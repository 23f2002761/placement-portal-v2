```vue id="jobapps"
<template>
  <div>
    <h2>Applications</h2>

    <div class="table-box">
      <table>
        <thead>
          <tr>
            <th>Student</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="app in applications" :key="app.application_id">
            <td>{{ app.student_name }}</td>

            <td>
              <span :class="['status', app.status]">
                {{ app.status }}
              </span>
            </td>

            <td>
              <!-- SHORTLIST -->
              <button
                v-if="app.status === 'applied'"
                @click="updateStatus(app.application_id, 'shortlisted')"
              >
                Shortlist
              </button>

              <!-- REJECT -->
              <button
                v-if="
                  ['applied', 'shortlisted', 'interview'].includes(app.status)
                "
                class="danger"
                @click="updateStatus(app.application_id, 'rejected')"
              >
                Reject
              </button>

              <!-- SCHEDULE -->
              <button
                v-if="app.status === 'shortlisted'"
                @click="schedule(app.application_id)"
              >
                Schedule Interview
              </button>

              <!-- SELECT -->
              <button
                v-if="app.status === 'interview'"
                @click="updateStatus(app.application_id, 'selected')"
              >
                Select
              </button>

              <!-- MARK PLACED -->
              <button
                v-if="app.status === 'selected'"
                @click="updateStatus(app.application_id, 'placed')"
              >
                Mark Placed
              </button>
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
import { useRoute } from "vue-router";

const route = useRoute();
const jobId = route.params.id;

const applications = ref([]);

const loadApplications = async () => {
  const res = await api.get(`/company/job/${jobId}/applications`);
  applications.value = res.data;
};

onMounted(loadApplications);

// update status
const updateStatus = async (appId, status) => {
  await api.put(`/company/application/${appId}/status`, { status });
  loadApplications();
};

// schedule interview
const schedule = async (appId) => {
  const date = prompt("Enter interview date (YYYY-MM-DD):");
  const location = prompt("Enter interview location:");

  if (!date || !location) return;

  await api.put(`/company/application/${appId}/schedule`, {
    interview_date: date,
    interview_location: location,
  });

  loadApplications();
};
</script>

<style scoped>
h2 {
  margin-bottom: 20px;
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

/* STATUS COLORS */
.status.applied {
  color: blue;
}
.status.shortlisted {
  color: orange;
}
.status.interview {
  color: purple;
}
.status.selected {
  color: green;
}
.status.placed {
  color: darkgreen;
}
.status.rejected {
  color: red;
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
