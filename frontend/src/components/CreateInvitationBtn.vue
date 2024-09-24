<template>
  <v-btn @click="sendInvitation" color="primary">Einladung erstellen</v-btn>
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
