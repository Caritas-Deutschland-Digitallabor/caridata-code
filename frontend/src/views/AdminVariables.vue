<template>
  <v-container>
    <v-expand-transition>
      <div>
        <v-alert v-if="error" type="error" rounded="0" closable>
          {{ error }}
        </v-alert>
      </div>
    </v-expand-transition>
    <h1 class="mb-2">Alle Variablen</h1>
    <p class="mb-8 text-body-1">
      Hier sind alle Variablen aufgelistet, die in den Daten enthalten sind. Sie
      können hier die Variablen einsehen und Informationen über sie erhalten.
    </p>

    <div v-if="isLoading">
      <v-skeleton-loader color="transparent" type="heading" class="my-2" />
    </div>
    <div v-else-if="variables.length > 0">
      <!--
      <v-card
        v-for="variable in variables"
        :key="variable.id"
        :border="true"
        variant="flat"
        class="my-2 pa-2 d-flex align-center"
      >
        {{ variable }}
      </v-card>
    </div>
    -->
      <v-data-iterator
        :items="filteredVariables"
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
            <v-select
              :items="sources"
              v-model="selectedSource"
              density="comfortable"
              placeholder="Quelle"
              prepend-inner-icon="mdi-filter"
              style="max-width: 300px"
              variant="outlined"
              clearable
              hide-details
              class="mx-4"
            >
            </v-select>
          </v-toolbar>
        </template>

        <template v-slot:default="{ items }">
          <v-container class="pa-2" fluid>
            <v-row dense>
              <v-col v-for="item in items" :key="item.id" cols="12">
                <v-card class="pb-3" variant="outlined">
                  <v-list-item :subtitle="item.raw.name" class="mb-2">
                    <template v-slot:title>
                      <strong class="text-h6 mb-2">{{ item.raw.text }}</strong>
                    </template>
                    <template v-slot:append>
                      <v-chip color="secondary" class="mb-1 mx-2">{{
                        item.raw.source
                      }}</v-chip>
                    </template>
                  </v-list-item>
                  <v-expand-transition>
                    <div v-if="item.selected">
                      <v-list density="compact">
                        <v-list-item>
                          <v-list-item-title
                            class="text-subtitle-2 font-weight-bold"
                          >
                            Informationen
                          </v-list-item-title>
                        </v-list-item>
                        <v-list-item>
                          <v-list-item-title class="text-caption">
                            Interne ID: <i>{{ item.raw.id }}</i>
                          </v-list-item-title>
                          <v-divider></v-divider>
                        </v-list-item>
                        <v-list-item>
                          <v-list-item-title class="text-caption">
                            Art der Variable: {{ item.raw.type }}
                          </v-list-item-title>
                          <v-divider></v-divider>
                        </v-list-item>
                        <v-list-item>
                          <v-list-item-title class="text-caption">
                            Pflichtvariable im Export:
                            {{ item.raw.technical_mandatory ? "Ja" : "Nein" }}
                          </v-list-item-title>
                          <v-divider></v-divider>
                        </v-list-item>
                        <!--TODO: The API shouldn't return a string here-->
                        <v-list-item v-if="item.raw.value_from != 'None'">
                          <v-list-item-title class="text-caption">
                            Wertbereich: {{ item.raw.value_from }} -
                            {{ item.raw.value_to }}
                          </v-list-item-title>
                        </v-list-item>
                        <v-list-item v-if="item.raw.missing">
                          <v-list-item-title class="text-caption">
                            Fehlende Werte bezeichnet als:
                            {{ item.raw.missing }}
                          </v-list-item-title>

                          <v-divider></v-divider>
                        </v-list-item>
                      </v-list>
                      <v-list
                        density="compact"
                        v-if="item.selected && item.raw.categories"
                      >
                        <v-list-item>
                          <v-list-item-title
                            class="text-subtitle-2 font-weight-bold"
                          >
                            Kategorien
                          </v-list-item-title>
                        </v-list-item>
                        <v-list-item
                          v-for="category in item.raw.categories"
                          :key="category.id"
                        >
                          <v-list-item-title class="text-caption">
                            {{ category.value }} | {{ category.name }}
                          </v-list-item-title>

                          <v-divider></v-divider>
                        </v-list-item>
                      </v-list>
                    </div>
                  </v-expand-transition>

                  <div class="d-flex justify-space-between px-4">
                    <div
                      class="d-flex align-center text-caption text-medium-emphasis me-1"
                    >
                      <v-icon icon="mdi-order-numeric-ascending" start></v-icon>

                      <div class="text-truncate">
                        Spaltennummer: {{ item.raw.file_position }}
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
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import apiClient from "../plugins/api-client";
import { useQuery } from "@tanstack/vue-query";

const search = ref("");

const sources = ref([
  "stelle.json",
  "sbkern1",
  "sbkern2",
  "sbveran.json",
  "sbkont.json",
]);
const selectedSource = ref(null);

// function for filter
const filter = (val) => {
  console.log(val);
};

const filteredVariables = computed(() => {
  return variables.value.filter((variable) => {
    return (
      selectedSource.value === null || variable.source === selectedSource.value
    );
  });
});
const {
  isLoading,
  data: variables,
  error,
} = useQuery({
  queryKey: ["variables"],
  queryFn: async () => {
    const response = await apiClient.variables.listVariables();
    return response;
  },
  initialData: [],
});
</script>
