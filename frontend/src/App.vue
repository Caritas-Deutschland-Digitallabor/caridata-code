<template>
  <v-app>
    <the-drawer v-if="showDrawer" />
    <v-main>
      <v-container>
        <v-row class="justify-center">
          <v-col cols="12" sm="12" md="12" lg="12" xl="8">
            <router-view />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { onBeforeMount } from "vue";
import apiClient from "./plugins/api-client";
import { useRouter } from "vue-router";
import { useSchemaStore } from "./stores/schema";

const router = useRouter();

const showDrawer = computed(() => {
  return router.currentRoute.value.meta.showDrawer;
});

// Initialize the schema store
const schemaStore = useSchemaStore();
schemaStore.fetchSchemas();

onBeforeMount(async () => {
  try {
    await apiClient.csrf.sendCsrfToken();
    console.log("CSRF token sent");
  } catch (e) {
    console.error(e);
  }
});
</script>
