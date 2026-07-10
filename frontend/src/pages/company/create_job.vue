```vue id="createjob"
<template>
  <div>
    <h2>Create Job</h2>

    <div class="form-box">
      <input v-model="form.title" placeholder="Job Title" />
      <textarea v-model="form.description" placeholder="Description"></textarea>

      <input v-model="form.salary" type="number" placeholder="Salary" />
      <input v-model="form.skills" placeholder="Skills (comma separated)" />

      <input v-model="form.eligibility_branch" placeholder="Eligible Branch" />
      <input
        v-model="form.eligibility_cgpa"
        type="number"
        placeholder="Min CGPA"
      />

      <input v-model="form.experience" placeholder="Experience (if any)" />
      <input v-model="form.benefits" placeholder="Benefits" />

      <label>Deadline</label>
      <input v-model="form.deadline" type="date" />

      <button @click="createJob">Create Job</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "../../services/api";
import { useRouter } from "vue-router";

const router = useRouter();

const form = ref({
  title: "",
  description: "",
  salary: "",
  skills: "",
  eligibility_branch: "",
  eligibility_cgpa: "",
  deadline: "",
  experience: "",
  benefits: "",
});

const createJob = async () => {
  if (!form.value.title || !form.value.salary) {
    return alert("Title and Salary are required");
  }
  try {
    await api.post("/company/create-job", form.value);

    alert("Job created! Waiting for admin approval.");
    router.push("/company/dashboard");
  } catch (err) {
    console.log(err);
    alert(err.response?.data?.error || "Failed to create job");
  }
};
</script>

<style scoped>
h2 {
  margin-bottom: 20px;
}

.form-box {
  background: white;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 500px;
}

input,
textarea {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

textarea {
  min-height: 80px;
}

button {
  margin-top: 10px;
  padding: 10px;
  background: #0984e3;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>
```
