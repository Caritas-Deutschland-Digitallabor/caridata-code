<template>
  <v-dialog max-width="500">
    <template v-slot:activator="{ props: activatorProps }">
      <v-btn variant="tonal" color="secondary" v-bind="activatorProps"
        ><v-icon class="mr-2">mdi-email-edit</v-icon> Ändern</v-btn
      >
    </template>

    <template v-slot:default="{ isActive }">
      <v-card title="E-Mail-Adresse ändern">
        <v-form
          class="pa-2"
          v-model="isValid"
          id="create-form"
          @submit.prevent="
            updateInvitationEmail();
            isActive.value = false;
          "
        >
          <v-card-text>
            <p>
              Hier können Sie eine E-Mail-Adresse für die Einladung zum Upload
              anlegen oder ändern. Wenn hier eine E-Mail-Adresse hinterlegt ist,
              wird diese für die Einladung zum Upload verwendet. Andernfalls
              wird die CariNet-Email-Adresse verwendet.
            </p>
            <v-text-field
              v-model="newEmail"
              :rules="emailRules"
              label="Neue E-Mail-Adresse"
              autocomplete="email"
              variant="outlined"
              class="pt-4"
            >
            </v-text-field>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              text="Speichern"
              variant="tonal"
              color="secondary"
              :loading="isPending"
              :disabled="!isValid"
              form="create-form"
              type="submit"
            >
            </v-btn>

            <v-btn text="Zurück" @click="isActive.value = false"></v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </template>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, defineProps } from "vue";
import apiClient from "../plugins/api-client";
import { useMutation } from "@tanstack/vue-query";

const props = defineProps({
  organisationId: Number,
});

const newEmail = ref<string>("");
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
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
    );
};

const {
  isPending,
  isError,
  error,
  isSuccess,
  mutate: updateInvitationEmail,
} = useMutation({
  queryKey: ["organisations"],
  mutationFn: async () => {
    await apiClient.organisations.upsertOrganisationInvitationEmail(
      props.organisationId,
      newEmail.value,
    );
  },
  onSuccess: () => {},
});
</script>
