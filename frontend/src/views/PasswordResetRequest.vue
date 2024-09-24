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
        <h1>Passwort vergessen?</h1>
      </v-card-text>
      <v-card-text>
        Sie erhalten eine E-Mail mit einem Link, um ihr Passwort zurückzusetzen.
      </v-card-text>
      <v-card-text>
        <v-form
          v-model="isValid"
          id="request-form"
          @submit.prevent="handleResetPasswordEmail"
        >
          <v-text-field
            v-model="email"
            label="E-Mail"
            variant="outlined"
            :rules="emailRules"
          ></v-text-field>
          <v-expand-transition>
            <div>
              <v-alert v-if="error?.message" type="error">
                {{ error?.message }}
              </v-alert>
            </div>
          </v-expand-transition>
          <v-card-actions class="justify-center">
            <v-btn
              :loading="isLoading"
              :disabled="!isValid || isCountingDown"
              type="submit"
              variant="flat"
              color="primary"
              form="request-form"
            >
              Passwort zurückzusetzen
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card-text>
      <v-expand-transition>
        <div>
          <v-alert
            v-if="isCountingDown"
            type="success"
            rounded="0"
            color="accent"
          >
            Die Email wurde versendet.
          </v-alert>
        </div>
      </v-expand-transition>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useMutation } from "@tanstack/vue-query";
import apiClient from "../plugins/api-client";

const email = ref<string>("");
const isCountingDown = ref(false);
const isValid = ref<boolean>(false);

const emailRules = [
  (v: string | undefined) => !!v || "E-Mail ist erforderlich.",
  (v: string | undefined) =>
    (!!v && validateEmail(v)) || "E-Mail muss gültig sein.",
];

const validateEmail = (email: string) => {
  return !!String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
};

const setTimer = () => {
  isCountingDown.value = true;
  setTimeout(() => {
    isCountingDown.value = false;
  }, 30000);
};

const {
  mutate: resetPasswordEmail,
  isPending: isLoading,
  error,
} = useMutation({
  mutationFn: async () => {
    await apiClient.auth.resetForgotPassword({
      email: email.value,
    });
  },
  onSuccess: () => {
    setTimer();
  },
});

const handleResetPasswordEmail = () => {
  resetPasswordEmail();
};
</script>
