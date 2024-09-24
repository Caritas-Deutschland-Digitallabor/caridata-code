<template>
  <div class="py-7 text-left">
    <h2>
      Schritt 2: Daten zusammenfassen
      <v-icon size="sm" class="pb-1" icon="mdi-book-lock-outline"></v-icon>
    </h2>
    <p class="text-body-1 pb-8">
      In diesem Schritt werden die Daten auf Ihrem System aggregiert. Dafür
      werden nach vordefinierten Fragen die Daten zusammengefasst.
      <i
        >Zum Beispiel: Wie viele Fallnummern gibt es gruppiert nach
        Geschlecht.</i
      >
      <br /><br />
      Die Zusammenfassung passiert automatisch. Um das System zu testen werden
      hier drei Beispiele angezeigt. Zum anzeigen der zusammengefassten Daten
      klicken Sie auf <i>"Testen"</i>.<br />
    </p>
    <AggregatorField />
  </div>
</template>

<script setup lang="ts">
import AggregatorField from "@/components/home/aggregator/AggregatorField.vue";
</script>
