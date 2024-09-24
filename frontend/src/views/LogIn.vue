<template>
  <div
    style="
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    "
  >
    <v-card width="500px">
      <v-card-text class="d-flex flex-column align-center">
        <h1>Admin Login CariData</h1>
      </v-card-text>
      <v-card-text>
        <v-text-field
          v-model="email"
          label="E-Mail"
          autocomplete="email"
          autofocus
          variant="outlined"
        />
        <v-text-field
          v-model="password"
          :type="isPasswordVisible ? 'text' : 'password'"
          :append-inner-icon="isPasswordVisible ? 'mdi-eye-off' : 'mdi-eye'"
          label="Passwort"
          autocomplete="current-password"
          variant="outlined"
          @click:append-inner="isPasswordVisible = !isPasswordVisible"
        />
      </v-card-text>

      <v-card-actions class="justify-center">
        <v-btn
          :loading="isLoading"
          variant="flat"
          color="primary"
          @click="handleLogin"
        >
          Anmelden
        </v-btn>
      </v-card-actions>
      <v-card-actions class="d-flex flex-column">
        <v-btn
          variant="tonal"
          size="small"
          @click="router.push({ name: 'ResetPasswordRequest' })"
        >
          Passwort vergessen?
        </v-btn>
      </v-card-actions>
      <v-expand-transition>
        <div>
          <v-alert
            v-if="error?.message"
            type="error"
            rounded="0"
          >
            {{ error?.message }}
          </v-alert>
        </div>
      </v-expand-transition>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useUserStore } from "../stores/user";
import { useRouter } from "vue-router";
import { useMutation } from "@tanstack/vue-query";
import apiClient from "../plugins/api-client";

const userStore = useUserStore();
const router = useRouter();

const email = ref("");
const password = ref("");
const isPasswordVisible = ref(false);

const {
  isPending: isLoading,
  error,
  mutate: login,
} = useMutation({
  mutationFn: async () => {
    await apiClient.auth.authDbLogin({
      username: email.value,
      password: password.value,
    });
    console.log("login");
    userStore.user = await apiClient.users.getMe();
  },
  onSuccess: () => {
    router.push({ name: "AdminHome" });
  },
});

const handleLogin = async () => {
  login();
};
</script>
