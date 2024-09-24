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
        <h1>Registrierung CariData</h1>
      </v-card-text>
      <v-form
        v-model="isValid"
        id="register-form"
        @submit.prevent="handleRegisterUser"
      >
        <v-card-text>
          <p>
            Legen Sie ein Passwort fest, um Ihre Registrierung abzuschließen.
          </p>

          <v-text-field
            v-model="password"
            :rules="passwordRules"
            :type="isVisiblePassword ? 'text' : 'password'"
            label="Passwort"
            variant="outlined"
            class="pt-6"
          >
            <template v-slot:append>
              <v-icon
                v-if="isVisiblePassword"
                @click="() => (isVisiblePassword = !isVisiblePassword)"
                icon="mdi-eye"
              ></v-icon>
              <v-icon
                v-else
                @click="() => (isVisiblePassword = !isVisiblePassword)"
                icon="mdi-eye-off"
              ></v-icon>
              <v-tooltip bottom max-width="400px">
                <template v-slot:activator="{ props }">
                  <v-icon class="ml-1" v-bind="props" icon="mdi-information">
                  </v-icon>
                </template>
                <v-list class="ma-0 pa-0" bg-color="primary">
                  <p class="text-body-1">Ihr Passwort sollte:</p>

                  <v-list-item class="text-body-2"
                    >- Mindestens 12 Zeichen haben</v-list-item
                  ><v-list-item class="text-body-2"
                    >- Mindestens einen Großbuchstaben haben</v-list-item
                  ><v-list-item class="text-body-2"
                    >- Mindestens einen Kleinbuchstaben haben</v-list-item
                  >
                  <v-list-item class="text-body-2"
                    >- Mindestens eine Zahl enthält</v-list-item
                  >
                  <v-list-item class="text-body-2"
                    >- Mindestens eine Sonderzeichen enthält</v-list-item
                  >
                </v-list>
              </v-tooltip>
            </template>
          </v-text-field>

          <v-text-field
            v-model="confirmPassword"
            :rules="passwordConfirmationRules"
            :type="isVisiblePassword ? 'text' : 'password'"
            label="Passwort bestätigen"
            variant="outlined"
          ></v-text-field>
        </v-card-text>

        <v-card-actions class="justify-center">
          <v-btn
            :loading="isLoading"
            variant="flat"
            color="primary"
            type="submit"
            form="register-form"
          >
            Registrieren
          </v-btn>
        </v-card-actions></v-form
      >

      <v-expand-transition>
        <div>
          <v-alert v-if="error" type="error" rounded="0">
            {{ error }}
          </v-alert>
        </div>
      </v-expand-transition>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useUserStore } from "../stores/user";
import { useRouter, useRoute } from "vue-router";
import { useMutation } from "@tanstack/vue-query";
import apiClient from "../plugins/api-client";

const userStore = useUserStore();
const router = useRouter();
const route = useRoute();

const isVisiblePassword = ref<boolean>(false);
const password = ref<string>("");
const confirmPassword = ref<string>("");

const containCaptialLetter = /^.*[A-Z].*$/;
const containLowerCaseLetter = /^.*[a-z].*$/;
const containNumber = /^.*[0-9].*$/;
const containSymbol = /^.*[^a-zA-Z0-9].*$/;

// Rules for password and confirmation password
const passwordRules = computed(() => [
  (v: string) => !!v || "Passwort wird benötigt",
  (v: string) =>
    (v && v.length >= 12) || "Passwort muss mindestens 12 Zeichen enthalten.",
  (v: string) =>
    containCaptialLetter.test(v) ||
    "Passwort muss mindestens einen Großbuchstaben enthalten.",
  (v: string) =>
    containLowerCaseLetter.test(v) ||
    "Passwort muss mindestens einen Kleinbuchstaben enthalten.",
  (v: string) =>
    containNumber.test(v) || "Passwort muss mindestens eine Zahl enthalten.",
  (v: string) =>
    containSymbol.test(v) || "Passwort muss mindestens ein Symbol enthalten.",
]);

const passwordConfirmationRules = computed(() => [
  () =>
    confirmPassword.value === password.value ||
    "Passwörter müssen identisch sein.",
]);

const registerId = computed(() => route.query.token!.toString());

const {
  mutate: registerUser,
  isPending: isLoading,
  error,
} = useMutation({
  mutationFn: async () => {
    await apiClient.auth.resetResetPassword({
      token: registerId.value,
      password: password.value,
    });
  },
  onSuccess: () => {
    router.push({ name: "Login" });
  },
});

const handleRegisterUser = () => {
  registerUser();
};
</script>
