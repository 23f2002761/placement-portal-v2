<template>
  <div class="layout">
    <!-- SIDEBAR -->
    <div class="sidebar">
      <h2>Company</h2>

      <ul>
        <li
          :class="{ active: isActive('/company/dashboard') }"
          @click="$router.push('/company/dashboard')"
        >
          Dashboard
        </li>

        <li
          :class="{ active: isActive('/company/create-job') }"
          @click="$router.push('/company/create-job')"
        >
          Create Job
        </li>
      </ul>
    </div>

    <!-- MAIN -->
    <div class="main">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";

const route = useRoute();

const isActive = (path) => {
  return route.path === path;
};
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}

/* SIDEBAR */
.sidebar {
  width: 220px;
  background: #1e272e;
  color: white;
  padding: 20px;
}

.sidebar h2 {
  margin-bottom: 20px;
}

.sidebar li {
  padding: 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: 0.2s;
}

.sidebar li:hover {
  background: #485460;
}

.sidebar .active {
  background: #0984e3;
  font-weight: bold;
}

/* MAIN */
.main {
  flex: 1;
  padding: 20px;
  background: #f5f6fa;
}
</style>
