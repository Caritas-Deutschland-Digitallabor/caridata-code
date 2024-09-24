<template>
  <v-dialog v-model="isDialog" max-width="500">
    <template v-slot:activator="{ props: activatorProps }">
      <v-list-item v-bind="activatorProps">
        <v-list-item-title class="text-error">
          {{ props.deleteType }} löschen
        </v-list-item-title>
      </v-list-item>
    </template>
    <template v-slot:default>
      <v-card>
        <v-card-title>
          <slot name="title"></slot>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <slot name="default"></slot>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="medium-emphasis"
            variant="tonal"
            @click="isDialog = false"
          >
            Abbrechen
          </v-btn>
          <v-btn
            variant="flat"
            color="error"
            @click="
              emit('delete');
              isDialog = false;
            "
          >
            Löschen
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref } from "vue";

const props = defineProps<{
  deleteType: string;
}>();

const isDialog = ref<boolean>(false);

const emit = defineEmits<{
  (e: "delete"): void;
}>();
</script>
