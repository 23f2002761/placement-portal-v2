<template>
  <div class="layout">
    <!-- SIDEBAR -->
    <div class="sidebar">
      <h2>Student</h2>

      <ul>
        <li
          :class="{ active: isActive('/student/dashboard') }"
          @click="$router.push('/student/dashboard')"
        >
          Dashboard
        </li>

        <li
          :class="{ active: isActive('/student/jobs') }"
          @click="$router.push('/student/jobs')"
        >
          Browse Jobs
        </li>

        <li
          :class="{ active: isActive('/student/interviews') }"
          @click="$router.push('/student/interviews')"
        >
          Interviews
        </li>

        <li
          :class="{ active: isActive('/student/placements') }"
          @click="$router.push('/student/placements')"
        >
          Placements
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
  background: #0b1d3a;
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
  background: #1b2f55;
}

.sidebar .active {
  background: #00b894;
  font-weight: bold;
}

/* MAIN */
.main {
  flex: 1;
  padding: 20px;
  background: #f5f6fa;
}
</style>
