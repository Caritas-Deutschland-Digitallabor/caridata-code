<template>
  <v-container>
    <v-expand-transition>
      <div>
        <v-alert v-if="error" type="error" rounded="0" closable>
          {{ error }}
        </v-alert>
      </div>
    </v-expand-transition>
    <h1 class="mb-2">Aggregationsregeln</h1>
    <p class="mb-8 text-body-1">
      Hier sind die Aggregationsregeln festgehalten. Sie haben dabei alle das
      gleiche Schema. Es gibt eine
      <strong>zu aggregierende Variable</strong> (z.B. eindeutige Fallnummern).
      Weiterhin kann diese Variable nach maximal zwei Gruppen aggregiert werden
      (<strong>Primäre Gruppierungsvariable</strong> und
      <strong>Sekundäre Gruppierungsvariable</strong>). Es kann auch ein
      <strong>Filter</strong> definiert werden, der auf die Daten angewendet
      wird (z.B. "zähle nur die erste Beratungsepisode").
    </p>
    <div v-if="isLoading">
      <v-skeleton-loader color="transparent" type="heading" class="my-2" />
    </div>
    <div v-else-if="aggregations.length > 0">
      <v-row>
        <v-col cols="12" v-for="agg in aggregations" :key="agg.id">
          <v-card variant="outlined" class="pa-2">
            <div class="d-flex align-center">
              <v-avatar variant="tonal" rounded="lg" class="mr-4 text-body-2">
                {{ agg.id }}
              </v-avatar>

              <div>
                <p class="text-subtitle-2">
                  {{ agg.name }}
                </p>
                <p class="text-caption text-medium-emphasis">
                  {{ agg.description_aggregation }}
                </p>
              </div>
            </div>
            <div>
              <v-card
                variant="tonal"
                color="secondary"
                class="mt-2"
                rounded="lg"
              >
                <v-list>
                  <v-list-item>
                    <v-list-item-title>
                      {{ agg.aggregation_variable_name }}
                      {{ agg.is_distinct ? "(Distinkte Werte)" : "" }}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      Zu aggregierende Variable
                    </v-list-item-subtitle>
                    <v-divider></v-divider>
                  </v-list-item>
                  <v-list-item v-if="agg.grouping_variable_1_id">
                    <v-list-item-title>
                      {{ agg.grouping_variable_1_id }}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      Primäre Gruppierungsvariable
                    </v-list-item-subtitle>
                    <v-divider></v-divider>
                  </v-list-item>
                  <v-list-item v-if="agg.grouping_variable_2_id">
                    <v-list-item-title>
                      {{ agg.grouping_variable_2_id }}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      Sekundäre Gruppierungsvariable
                    </v-list-item-subtitle>
                    <v-divider></v-divider>
                  </v-list-item>
                </v-list>
              </v-card>
              <v-list density="compact">
                <v-list-item>
                  <v-list-item-title>
                    {{ agg.description_schema }}
                  </v-list-item-title>
                  <v-list-item-subtitle> Schema </v-list-item-subtitle>
                  <v-divider></v-divider>
                </v-list-item>
                <v-list-item v-if="agg.filter">
                  <v-list-item-title>
                    <code class="block whitespace-pre overflow-x-scroll">{{
                      agg.filter
                    }}</code>
                  </v-list-item-title>
                  <v-list-item-subtitle> Filter </v-list-item-subtitle>
                  <v-divider></v-divider>
                </v-list-item>
              </v-list>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import apiClient from "../plugins/api-client";
import { useQuery } from "@tanstack/vue-query";

const {
  isLoading,
  data: aggregations,
  error,
} = useQuery({
  queryKey: ["aggregations"],
  queryFn: async () => {
    const response = await apiClient.aggregations.listAggregations();
    return response;
  },
  initialData: [],
});
</script>
