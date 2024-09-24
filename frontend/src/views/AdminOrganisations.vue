<template>
  <v-container>
    <v-expand-transition>
      <div>
        <v-alert v-if="error" type="error" rounded="0" closable>
          {{ error }}
        </v-alert>
      </div>
    </v-expand-transition>
    <h1 class="mb-2">Beratungsstellen</h1>
    <p class="mb-8 text-body-1">
      Hier sind alle Beratungsstellen aufgelistet, die in der Zentralstatistik
      hinterlegt sind. Sie können die E-Mail-Adressen der Beratungsstellen
      einsehen. Wenn Einladungen an eine andere E-Mail-Adresse versendet werden
      sollen, bearbeiten Sie die alternative E-Mail-Adresse. Über den
      Synchronisieren-Button können Sie die aktuellen Beratungsstellen aus
      CariNet abrufen (alternative E-Mail-Adressen werden dabei nicht
      überschrieben).
    </p>
    <div v-if="isLoading">
      <v-skeleton-loader color="transparent" type="heading" class="my-2" />
    </div>
    <div v-else-if="organisations.length > 0">
      <v-data-iterator
        :items="organisations"
        :items-per-page="5"
        :search="search"
        item-key="id"
      >
        <template v-slot:header>
          <v-toolbar class="px-2" color="transparent">
            <v-text-field
              v-model="search"
              density="comfortable"
              placeholder="Suche"
              prepend-inner-icon="mdi-magnify"
              style="max-width: 300px"
              variant="outlined"
              clearable
              hide-details
            ></v-text-field>
            <v-spacer></v-spacer>
            <v-btn @click="syncOrganisations" variant="tonal" color="primary"
              >Synchronisieren</v-btn
            >
          </v-toolbar>
        </template>

        <template v-slot:default="{ items }">
          <v-container class="pa-2" fluid>
            <v-row dense>
              <v-col v-for="item in items" :key="item.id" cols="12">
                <v-card class="pb-3" variant="outlined">
                  <!-- make list with both email adresses and set a checkbox for which is used -->
                  <v-list-item class="mb-1">
                    <template v-slot:title>
                      <strong class="text-h6">{{ item.raw.name }}</strong>
                    </template>
                  </v-list-item>
                  <v-card-text class="pt-0">
                    <v-list density="compact">
                      <v-list-item>
                        <v-list-item-title>
                          {{ item.raw.email ? item.raw.email : "-" }}
                        </v-list-item-title>
                        <v-list-item-subtitle
                          >CariNet-Email-Adresse</v-list-item-subtitle
                        >
                      </v-list-item>
                      <v-divider></v-divider>
                      <v-list-item>
                        <v-list-item-title>
                          {{
                            item.raw.invitation_email
                              ? item.raw.invitation_email
                              : "-"
                          }}
                        </v-list-item-title>
                        <template v-slot:append>
                          <UpdateInvitationEmail
                            :organisationId="item.raw.id"
                          ></UpdateInvitationEmail>
                        </template>

                        <v-list-item-subtitle
                          >E-Mail-Adresse für Einladung</v-list-item-subtitle
                        >
                      </v-list-item>
                      <v-divider></v-divider>
                    </v-list>
                  </v-card-text>
                  <v-expand-transition>
                    <div v-if="item.selected">
                      <v-card-text>
                        <v-list-item>
                          <v-list-item-title
                            >Letztes Update:
                            {{ item.raw.updated_at }}</v-list-item-title
                          >
                        </v-list-item>
                      </v-card-text>
                    </div>
                  </v-expand-transition>

                  <div class="d-flex justify-space-between px-4">
                    <div
                      class="d-flex align-center text-caption text-medium-emphasis me-1"
                    >
                      <v-icon
                        icon="mdi-alert"
                        color="error"
                        start
                        v-if="!item.raw.email && !item.raw.invitation_email"
                      ></v-icon>

                      <div
                        class="text-truncate"
                        v-if="!item.raw.email && !item.raw.invitation_email"
                      >
                        Keine E-Mail-Adresse hinterlegt
                      </div>
                    </div>

                    <v-btn
                      class="text-none"
                      size="small"
                      :prepend-icon="
                        !item.selected ? 'mdi-chevron-down' : 'mdi-chevron-up'
                      "
                      text="Details"
                      flat
                      @click="item.selected = !item.selected"
                    >
                    </v-btn>
                  </div>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </template>

        <template v-slot:footer="{ page, pageCount, prevPage, nextPage }">
          <div class="d-flex align-center justify-center pa-4">
            <v-btn
              :disabled="page === 1"
              density="comfortable"
              icon="mdi-arrow-left"
              variant="tonal"
              rounded
              @click="prevPage"
            ></v-btn>

            <div class="mx-2 text-caption">
              Seite {{ page }} von {{ pageCount }}
            </div>

            <v-btn
              :disabled="page >= pageCount"
              density="comfortable"
              icon="mdi-arrow-right"
              variant="tonal"
              rounded
              @click="nextPage"
            ></v-btn>
          </div>
        </template>
      </v-data-iterator>
    </div>
    <div v-else>
      <v-spacer></v-spacer>
      <v-btn @click="syncOrganisations" variant="tonal" color="primary"
        >Synchronisieren</v-btn
      >
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import apiClient from "../plugins/api-client";
import { useQuery } from "@tanstack/vue-query";

const search = ref("");

const {
  isLoading,
  data: organisations,
  error,
} = useQuery({
  queryKey: ["organisations"],
  queryFn: async () => {
    const response = await apiClient.organisations.listOrganisations();
    return response;
  },
  initialData: [],
});

const syncOrganisations = async () => {
  try {
    await apiClient.organisations.synchronizeOrganisations();
  } catch (error) {
    console.error(error);
  }
};
</script>
