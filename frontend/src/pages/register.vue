<template>
  <div class="container">
    <!-- LEFT SIDE -->
    <div class="left">
      <h2>Join Placement Portal</h2>
    </div>

    <!-- RIGHT SIDE -->
    <div class="right">
      <!-- TABS -->
      <div class="tabs">
        <button
          :class="{ active: role === 'student' }"
          @click="role = 'student'"
        >
          Student
        </button>
        <button
          :class="{ active: role === 'company' }"
          @click="role = 'company'"
        >
          Company
        </button>
      </div>

      <h3>Register</h3>

      <input v-model="name" placeholder="Name / Company Name" />
      <input v-model="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Password" />

      <button class="register-btn" @click="register">Register</button>

      <p class="link" @click="goLogin">Already have an account? Login</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "../services/api";
import { useRouter } from "vue-router";

const name = ref("");
const email = ref("");
const password = ref("");
const role = ref("student");

const router = useRouter();
const register = async () => {
  try {
    const endpoint =
      role.value === "student" ? "/register/student" : "/register/company";

    const res = await api.post(endpoint, {
      name: name.value,
      email: email.value,
      password: password.value,
    });

    alert(res.data.message);

    router.push("/"); // go to login
  } catch (err) {
    alert(err.response?.data?.error || "Registration failed");
  }
};

const goLogin = () => {
  router.push("/");
};
</script>

<style scoped>
.container {
  display: flex;
  height: 100vh;
  font-family: Arial, sans-serif;
}

.left {
  flex: 1;
  background: linear-gradient(135deg, #0a1f44, #021027);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.right {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 40px;
  max-width: 400px;
  margin: auto;
}

.tabs {
  display: flex;
  margin-bottom: 20px;
}

.tabs button {
  flex: 1;
  padding: 10px;
  border: none;
  background: #ddd;
  cursor: pointer;
}

.tabs button.active {
  background: #00b894;
  color: white;
}

input {
  margin-bottom: 15px;
  padding: 10px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.register-btn {
  padding: 12px;
  background: #00b894;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

.link {
  margin-top: 15px;
  color: #00b894;
  cursor: pointer;
}
</style>
