<template>
  <div class="container">
    <!-- LEFT IMAGE SECTION -->
    <div class="left">
      <h2>Placement Portal</h2>
    </div>

    <!-- RIGHT LOGIN CARD -->
    <div class="right">
      <!-- ROLE TABS -->
      <div class="tabs">
        <button :class="{ active: role === 'admin' }" @click="role = 'admin'">
          Admin
        </button>
        <button
          :class="{ active: role === 'company' }"
          @click="role = 'company'"
        >
          Company
        </button>
        <button
          :class="{ active: role === 'student' }"
          @click="role = 'student'"
        >
          Student
        </button>
      </div>

      <h3>Login</h3>

      <input v-model="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Password" />

      <button class="login-btn" @click="login">Login</button>

      <p class="link" @click="$router.push('/register')">
        Student Self-Registration
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "../services/api";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const role = ref("student"); // default
const router = useRouter();

const login = async () => {
  try {
    const res = await api.post("/login", {
      email: email.value,
      password: password.value,
    });

    const token = res.data.access_token;
    localStorage.setItem("token", token);

    const payload = JSON.parse(atob(token.split(".")[1]));

    // optional: validate role matches selected tab
    if (payload.role !== role.value) {
      alert("Selected role does not match account role");
      return;
    }

    router.push(`/${payload.role}/dashboard`);
  } catch (err) {
    console.log(err);
    alert(JSON.stringify(err.response?.data));
  }
};
</script>

<style scoped>
.container {
  display: flex;
  height: 100vh;
  font-family: Arial, sans-serif;
}

/* LEFT SIDE */
.left {
  flex: 1;
  background: linear-gradient(135deg, #0a1f44, #021027);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* RIGHT SIDE */
.right {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 40px;
  max-width: 400px;
  margin: auto;
}

/* TABS */
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

/* INPUTS */
input {
  margin-bottom: 15px;
  padding: 10px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* BUTTON */
.login-btn {
  padding: 12px;
  background: #00b894;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

/* LINK */
.link {
  margin-top: 15px;
  color: #00b894;
  cursor: pointer;
}
</style>
