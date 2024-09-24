<template>
  <div>
    <v-btn
      @click="sendInvitation"
      color="secondary"
      variant="tonal"
      prepend-icon="mdi-email"
      >Erinnerung senden
    </v-btn>
    <v-badge
      color="secondary"
      inline
      v-if="isSuccess"
      icon="mdi-check"
    ></v-badge>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps } from "vue";
import apiClient from "../plugins/api-client";
import { useMutation } from "@tanstack/vue-query";

const props = defineProps<{
  organisationId: number;
}>();

const {
  isPending,
  isError,
  error,
  isSuccess,
  mutate: sendInvitation,
} = useMutation({
  mutationFn: async () => {
    await apiClient.invitations.sendInvitation(props.organisationId);
  },
  onSuccess: () => {},
});
</script>
