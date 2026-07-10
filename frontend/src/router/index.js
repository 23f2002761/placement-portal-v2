import { createRouter, createWebHistory } from "vue-router";

import Login from "../pages/login.vue";
import Register from "../pages/register.vue";

import StudentLayout from "../layout/student_layout.vue";
import StudentDashboard from "../pages/student/dashboard.vue";
import JobsPage from "../pages/student/jobs.vue";
import InterviewsPage from "../pages/student/interviews.vue";
import PlacementsPage from "../pages/student/placements.vue";

import CompanyLayout from "../layout/company_layout.vue";
import CompanyDashboard from "../pages/company/dashboard.vue";
import CreateJob from "../pages/company/create_job.vue";
import JobApplications from "../pages/company/job_applications.vue";

import AdminLayout from "../layout/admin_layout.vue";
import AdminDashboard from "../pages/admin/dashboard.vue";
import Companies from "../pages/admin/companies.vue";
import Students from "../pages/admin/student.vue";
import Jobs from "../pages/admin/jobs.vue";
import Applications from "../pages/admin/applications.vue";

const routes = [
  { path: "/", component: Login },
  { path: "/register", component: Register },

  {
  path: "/company",
  component: CompanyLayout,
  children: [
    { path: "dashboard", component: CompanyDashboard },
    { path: "create-job", component: CreateJob },
    { path: "job/:id/applications", component: JobApplications },
  ],
},

  {
    path: "/admin",
    component: AdminLayout,
    children: [
      { path: "", redirect: "dashboard" },
      { path: "dashboard", component: AdminDashboard },
      { path: "companies", component: Companies },
      { path: "students", component: Students },
      { path: "jobs", component: Jobs },
      { path: "applications", component: Applications },
    ],
  },

  {
  path: "/student",
  component: StudentLayout,
  children: [
    { path: "", redirect: "dashboard" },
    { path: "dashboard", component: StudentDashboard },
    { path: "jobs", component: JobsPage },
    { path: "interviews", component: InterviewsPage },
    { path: "placements", component: PlacementsPage },
  ],
},
];

export default createRouter({
  history: createWebHistory(),
  routes,
});