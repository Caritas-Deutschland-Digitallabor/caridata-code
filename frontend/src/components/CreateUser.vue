<template>
  <v-dialog v-model="isDialog" width="500">
    <template v-slot:activator="{ props }">
      <v-btn v-bind="props" class="ml-2" color="primary" variant="flat">
        Account hinzufügen
      </v-btn>
    </template>
    <template v-slot:default>
      <v-card>
        <v-form
          class="pa-2"
          v-model="isValid"
          id="create-form"
          @submit.prevent="inviteUser()"
        >
          <v-card-title>Administrator:in hinzufügen</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            Der User:in wird eine E-Mail mit einem Einladungslink zugeschickt.
            Dort kann das Passwort gesetzt werden.
          </v-card-text>
          <v-card-text>
            <v-text-field
              v-model="newUser.name"
              :rules="nameRules"
              label="Name"
              variant="outlined"
              class="mb-4"
            >
            </v-text-field>
            <v-text-field
              v-model="newUser.email"
              :rules="emailRules"
              label="E-Mail"
              autocomplete="email"
              variant="outlined"
            >
            </v-text-field>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              variant="tonal"
              @click="
                isDialog = false;
                resetUser();
              "
            >
              Abbrechen
            </v-btn>
            <v-btn
              variant="flat"
              color="primary"
              :loading="isPending"
              :disabled="!isValid"
              form="create-form"
              type="submit"
            >
              Speichern
            </v-btn>
          </v-card-actions>
          <v-expand-transition>
            <div>
              <v-alert v-if="error" type="error" rounded="0" closable>
                {{ error }}
              </v-alert>
            </div>
          </v-expand-transition>
        </v-form>
      </v-card>
    </template>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref } from "vue";
import apiClient from "../plugins/api-client";
import { CreateUserIn } from "../services";
import { useMutation } from "@tanstack/vue-query";

const isValid = ref<boolean>(false);
const isDialog = ref(false);
const newUser = ref<CreateUserIn>({
  email: "",
  name: "",
  password: null,
  is_active: true,
  is_superuser: false,
  is_verified: true,
});

const nameRules = [(v: string | undefined) => !!v || "Name ist erforderlich."];
const emailRules = [
  (v: string | undefined) => !!v || "E-Mail ist erforderlich.",
  (v: string | undefined) =>
    (!!v && validateEmail(v)) || "E-Mail muss gültig sein.",
];
const validateEmail = (email: string) => {
  return !!String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
    );
};

const resetUser = () => {
  newUser.value = {
    email: "",
    name: "",
    password: null,
    is_active: true,
    is_superuser: false,
    is_verified: true,
  };
};

const {
  isPending,
  isError,
  error,
  isSuccess,
  mutate: inviteUser,
} = useMutation({
  mutationFn: async () => {
    await apiClient.auth.createUser(newUser.value);
  },
  onSuccess: () => {
    isDialog.value = false;
  },
});
</script>
