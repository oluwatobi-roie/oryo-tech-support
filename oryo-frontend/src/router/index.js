import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '@/components/UserLogin.vue';
import TechSupportDashboard from '@/components/tech_support.vue';
import admin_dashboard from '@/components/admin_dashboard.vue';
import DefaultPage from '@/components/default_page.vue';



const routes = [
    { path: '/', component: UserLogin },

    { 
        path: '/tech-support', 
        component: TechSupportDashboard,
        meta: { requiresAuth: true, role: 'tech-support' }
     },
     {
        path: '/admin-dashboard',
        component: admin_dashboard,
        meta: { requiresAuth: true, role: 'General Admin' }
     },
    { 
        path: '/default_page',
         component: DefaultPage 
        },
    // { path: '/users', component: UserManagement }
];


const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");
  
    if (to.meta.requiresAuth && !token) {
      next('/');
    } else if (to.meta.role && role !== to.meta.role) {
      next('/'); // Redirect unauthorized users
    } else {
      next();
    }
  });
  
export default router;