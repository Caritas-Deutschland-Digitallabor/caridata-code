<template>
  <v-dialog v-model="dialog" width="800px" height="800px" disabled>
    <v-card>
      <v-card-title class="mx-2 mt-6"
        >Herzlich willkommen bei CariData</v-card-title
      >
      <v-card-text
        >Hier können Sie Daten für die Jahresstatistik einreichen. Dafür
        brauchen Sie ein Einmal-Passwort. Dieses können Sie über Ihre
        E-Mail-Adresse anfordern. Sobald Sie das Einmal-Passwort erhalten haben,
        können Sie Ihre Daten einreichen.
      </v-card-text>
      <v-card-actions>
        <v-text-field
          variant="outlined"
          label="Einmal-Passwort"
          hide-details
          class="px-4"
        ></v-text-field>

        <v-btn variant="text" size="small" class="pr-4">
          Passwort per E-Mail anfordern
        </v-btn>
      </v-card-actions>
      <template v-slot:actions>
        <v-btn class="ms-auto" text="Ok" @click="dialog = false"></v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref } from "vue";
const dialog = ref(false);
</script>
