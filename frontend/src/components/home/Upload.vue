<template>
  <div class="py-7 text-left">
    <h2>
      Schritt 3: Aggregierte Daten hochladen
      <v-icon size="sm" class="pb-1" icon="mdi-cloud-sync-outline"></v-icon>
    </h2>
    <p class="text-body-1">
      In diesem Schritt werden ausschließlich die zusammengefassten Daten über
      eine sichere Verbindung an das CariData-System geschickt.
    </p>
  </div>
  <v-btn variant="tonal" @click="uploadAggregatedData"
    ><v-icon class="mr-1">mdi-lock</v-icon>Aggregierte Daten sicher
    hochladen</v-btn
  >
</template>

<script setup lang="ts">
import { useStatisticsStore } from "@/stores/statistics";

const statisticsStore = useStatisticsStore();

const uploadAggregatedData = () => {
  statisticsStore.postStatistics();
};
</script>
