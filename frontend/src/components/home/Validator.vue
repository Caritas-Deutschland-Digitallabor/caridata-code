<template>
  <div>
    <div class="pb-7 text-left">
      <h2>
        Schritt 1: Dateneingabe
        <v-icon size="sm" class="pb-1" icon="mdi-book-lock-outline"></v-icon>
      </h2>
      <p class="text-body-1">
        Bitte exportieren Sie die Daten aus Ihrem Beratungsstellen-System und
        halten diese bereit. Sie sollten folgende Dateien zur Verfügung haben:
        <b>STELLE, SBKERN1, SBKERN2, SBVERAN, SBKONT.</b> Die Dateien sollten
        eine der folgenden Dateiendungen haben: .csv, .txt oder .dbf.
        <i>Zum Beispiel: "SBKERN1.txt" oder "SBKERN2.csv"</i>.<br /><br />
        In den folgenden Feldern laden Sie bitte die passenden Dateien einzeln
        hoch und bestätigen Sie die Eingabe mit einem Klick auf
        <i>"Validieren"</i>. Mit einem Klick auf
        <i>"Ergebnis anzeigen"</i> sehen sie eine Vorschau der geladenen
        Daten.<br /><br />
        Sind alle Daten geladen können Sie mit Schritt 2 fortfahren.
      </p>
    </div>
    <ValidatorField
      v-model:dataset="stelle"
      fileSBType="STELLE"
    ></ValidatorField>
    <ValidatorField
      v-model:dataset="sbkern1"
      fileSBType="SBKERN1"
    ></ValidatorField>
    <ValidatorField
      v-model:dataset="sbkern2"
      fileSBType="SBKERN2"
    ></ValidatorField>
    <ValidatorField
      v-model:dataset="sbveran"
      fileSBType="SBVERAN"
    ></ValidatorField>
    <ValidatorField
      v-model:dataset="sbkont"
      fileSBType="SBKONT"
    ></ValidatorField>
  </div>
</template>

<script setup lang="ts">
import ValidatorField from "@/components/home/validator/ValidatorField.vue";
import { useSbFilesStore } from "@/stores/sbfiles";
import { ParsedData } from "@/types/Data";
import { ref } from "vue";
import { watch } from "vue";

const sbkern1 = ref<ParsedData>({
  headers: [],
  rows: [],
  hadHeaderInOriginalFile: false,
});

const sbkern2 = ref<ParsedData>({
  headers: [],
  rows: [],
  hadHeaderInOriginalFile: false,
});

const stelle = ref<ParsedData>({
  headers: [],
  rows: [],
  hadHeaderInOriginalFile: false,
});

const sbveran = ref<ParsedData>({
  headers: [],
  rows: [],
  hadHeaderInOriginalFile: false,
});

const sbkont = ref<ParsedData>({
  headers: [],
  rows: [],
  hadHeaderInOriginalFile: false,
});

const sbFilesStore = useSbFilesStore();

watch(sbkern1, (newVal) => {
  sbFilesStore.setSbkern1(newVal);
});
watch(sbkern2, (newVal) => {
  sbFilesStore.setSbkern2(newVal);
});
watch(stelle, (newVal) => {
  sbFilesStore.setStelle(newVal);
});
watch(sbveran, (newVal) => {
  sbFilesStore.setSbveran(newVal);
});
watch(sbkont, (newVal) => {
  sbFilesStore.setSbkont(newVal);
});
</script>
