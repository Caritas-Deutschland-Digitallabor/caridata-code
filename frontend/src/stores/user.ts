// Utilities
import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { UserOut } from "../services";

export const useUserStore = defineStore("user", () => {
  const user = ref<UserOut>();

  const isAuthenticated = computed<boolean>(() => !!user.value);

  const isAdmin = computed<boolean>(
    () => user.value?.is_verified === true && user.value?.is_superuser === true
  );

  return { user, isAuthenticated, isAdmin };
});
