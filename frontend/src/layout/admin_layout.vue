<template>
  <div class="layout">
    <!-- SIDEBAR -->
    <div class="sidebar">
      <h2>Admin</h2>
      <ul>
        <li
          :class="{ active: isActive('/admin/dashboard') }"
          @click="$router.push('/admin/dashboard')"
        >
          Dashboard
        </li>

        <li
          :class="{ active: isActive('/admin/companies') }"
          @click="$router.push('/admin/companies')"
        >
          Companies
        </li>

        <li
          :class="{ active: isActive('/admin/students') }"
          @click="$router.push('/admin/students')"
        >
          Students
        </li>

        <li
          :class="{ active: isActive('/admin/jobs') }"
          @click="$router.push('/admin/jobs')"
        >
          Jobs
        </li>

        <li
          :class="{ active: isActive('/admin/applications') }"
          @click="$router.push('/admin/applications')"
        >
          Applications
        </li>
      </ul>
    </div>

    <!-- MAIN CONTENT -->
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

.sidebar {
  width: 230px;
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
  background: #ff7f6b;
  font-weight: bold;
}

.main {
  flex: 1;
  padding: 20px;
  background: #f5f6fa;
}
</style>
