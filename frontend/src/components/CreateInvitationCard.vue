<template>
  <v-card variant="tonal" class="pa-4 pb-2">
    <div class="d-flex d-inline align-center">
      <v-select
        v-model="selectedOrganisation"
        :items="filteredOrganisations"
        item-title="name"
        return-object
        label="Beratungsstelle einladen"
        hide-details
        variant="outlined"
        class="mr-4"
      ></v-select>
      <v-btn
        @click="sendInvitation"
        color="primary"
        :loading="isPendingSend"
        :disabled="!selectedOrganisation"
        >Einladung erstellen</v-btn
      >
    </div>
    <p class="text-overline pt-1">
      {{ filteredOrganisations.length }} Beratungsstellen ohne aktive Einladung
    </p>
  </v-card>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import apiClient from "../plugins/api-client";
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";
import { OrganisationOut } from "@/services";

const queryClient = useQueryClient();

const selectedOrganisation = ref<OrganisationOut | null>(null);

const filteredOrganisations = computed(() => {
  // filter organisations that don't have an active invitation
  return organisations.value.filter((org) => {
    return (
      !org.invitations ||
      !org.invitations.filter((inv) => new Date(inv.expires_at) > new Date())
        .length
    );
  });
});

const {
  isLoading: isLoadingOrganisations,
  data: organisations,
  error: errorOrganisations,
} = useQuery({
  queryKey: ["organisations"],
  queryFn: async () => {
    const response = await apiClient.organisations.listOrganisations();
    return response;
  },
  initialData: [],
});

const {
  isPending: isPendingSend,
  isError: isErrorSend,
  error: errorSend,
  isSuccess: isSuccessSend,
  mutate: sendInvitation,
} = useMutation({
  mutationFn: async () => {
    await apiClient.invitations.sendInvitation(selectedOrganisation.value.id);
  },
  onSuccess: () => {
    // refetch organisations to update the list
    queryClient.invalidateQueries({
      queryKey: ["organisations"],
    });

    queryClient.invalidateQueries({
      queryKey: ["invitations"],
    });

    selectedOrganisation.value = null;
  },
});
</script>
