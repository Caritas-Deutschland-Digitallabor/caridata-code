import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "../stores/user";
import apiClient from "../plugins/api-client";
import { UserOut } from "../services";

// | routers__organisations__OrganisationOut.type[]
declare module "vue-router" {
  interface RouteMeta {
    allowedRoles: undefined;
  }
}

const routes = [
  {
    path: "/",
    redirect: { name: "Home" },
    meta: {
      allowedRoles: undefined,
      showDrawer: false,
      requiresAuth: false,
    },
  },
  {
    path: "/home",
    name: "Home",
    component: () => import("../views/UploadHome.vue"),
    meta: {
      allowedRoles: undefined,
      showDrawer: false,
      requiresAuth: false,
    },
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/LogIn.vue"),
    meta: {
      showDrawer: false,
      requiresAuth: false,
    },
  },
  {
    path: "/registrieren",
    name: "Registrieren",
    component: () => import("../views/SignUp.vue"),
    meta: {
      showDrawer: false,
      requiresAuth: false,
    },
  },
  {
    path: "/passwort-request",
    name: "ResetPasswordRequest",
    component: () => import("../views/PasswordResetRequest.vue"),
    meta: {
      showDrawer: false,
      requiresAuth: false,
    },
  },
  {
    path: "/passwort",
    name: "ResetPassword",
    component: () => import("../views/PasswordReset.vue"),
    meta: {
      showDrawer: false,
      requiresAuth: false,
    },
  },
  {
    path: "/admin",
    name: "AdminHome",
    component: () => import("../views/AdminHome.vue"),
    meta: {
      allowedRoles: undefined,
      showDrawer: true,
      requiresAuth: true,
    },
  },
  {
    path: "/users",
    name: "AdminListUsers",
    component: () => import("../views/AdminListUsers.vue"),
    meta: {
      allowedRoles: undefined,
      showDrawer: true,
      requiresAuth: true,
    },
  },
  {
    path: "/variables",
    name: "AdminVariables",
    component: () => import("../views/AdminVariables.vue"),
    meta: {
      allowedRoles: undefined,
      showDrawer: true,
      requiresAuth: true,
    },
  },
  {
    path: "/organisations",
    name: "AdminOrganisations",
    component: () => import("../views/AdminOrganisations.vue"),
    meta: {
      allowedRoles: undefined,
      showDrawer: true,
      requiresAuth: true,
    },
  },
  {
    path: "/aggregationen",
    name: "AdminAggregations",
    component: () => import("../views/AdminListAggregations.vue"),
    meta: {
      allowedRoles: undefined,
      showDrawer: true,
      requiresAuth: true,
    },
  },
  {
    path: "/einladungen",
    name: "AdminInvitations",
    component: () => import("../views/AdminListInvitations.vue"),
    meta: {
      allowedRoles: undefined,
      showDrawer: true,
      requiresAuth: true,
    },
  }
  /*
  {
    path: "/organisations",
    name: "ListOrganisations",
    component: () => import("../pages/ListOrganisations.vue"),
    meta: {
      allowedRoles: undefined
    },
  },
  {
    path: "/account",
    name: "ListAccount",
    component: () => import("../pages/ListAccount.vue"),
    meta: {
      allowedRoles: undefined
    },
  },*/
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from) => {
  const userStore = useUserStore();

  try {
    userStore.user = await apiClient.users.getMe();
  } catch (e) {
    userStore.user = undefined;
  }

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    return { name: "Home" };
  }

  if (
    !!to.meta.allowedRoles &&
    userStore.isAuthenticated
  ) {
    return { name: "Home" };
  }

  return true;
});

export default router;
