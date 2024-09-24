<template>
  <v-container>
    <v-expand-transition>
      <div>
        <v-alert v-if="error" type="error" rounded="0" closable>
          {{ error }}
        </v-alert>
      </div>
    </v-expand-transition>
    <h1 class="mb-2">Einladungen</h1>
    <p class="mb-8 text-body-1">
      Hier sind alle Einladungen aufgelistet, die an Beratungsstellen verschickt
      wurden. Wenn Sie eine neue Einladung erstellen möchten, können Sie eine
      Bertungsstelle auswählen und es wird eine neue Einladung erstellt. Wenn
      Sie eine Erinnerung senden möchten, können Sie dies über die
      Aktionen-Spalte tun.
    </p>
    <create-invitation-card></create-invitation-card>
    <div v-if="isLoading">
      <v-skeleton-loader color="transparent" type="heading" class="my-2" />
    </div>
    <v-data-table
      :headers="headers"
      :items="invitations"
      :loading="isLoading"
      :loading-text="loadingText"
      :no-results-text="noResultsText"
      v-model:sort-by="sortBy"
      :sort-desc.sync="false"
    >
      <template v-slot:item.actions="{ item }">
        <resend-invitation-btn :organisationId="item.organisation_id" />
      </template>
      <template v-slot:item.created_at="{ item }">
        {{ new Date(item.created_at).toLocaleDateString() }}
        {{ new Date(item.created_at).toLocaleTimeString() }}
      </template>
      <template v-slot:item.expires_at="{ item }">
        {{ new Date(item.expires_at).toLocaleDateString() }}
      </template>
      <template v-slot:item.status="{ item }">
        <v-chip
          :color="
            item.expires_at < new Date().toISOString() ? 'error' : 'success'
          "
          text-color="white"
          variant="outlined"
        >
          {{
            item.expires_at < new Date().toISOString()
              ? "abgelaufen"
              : "versendet"
          }}
        </v-chip>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import apiClient from "../plugins/api-client";
import { useQuery } from "@tanstack/vue-query";

const search = ref("");
const headers = [
  { title: "Organisation", key: "organisation_id" },
  { title: "E-Mail", key: "email" },
  { title: "Erstellt am", key: "created_at" },
  { title: "Gültig bis", key: "expires_at" },
  { title: "Status", key: "status" },
  { title: "Aktionen", key: "actions" },
];

const sortBy = [{ key: "created_at", order: "desc" }];

const loadingText = "Lade Einladungen...";
const noDataText = "Keine Einladungen gefunden.";
const noResultsText = "Keine Einladungen gefunden.";

const {
  isLoading,
  data: invitations,
  error,
} = useQuery({
  queryKey: ["invitations"],
  queryFn: async () => {
    const response = await apiClient.invitations.listInvitations();
    return response;
  },
  initialData: [],
});
</script>
