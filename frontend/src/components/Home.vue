<template>
  <v-container class="fill-height">
    <WelcomeDialog v-model:dialog="dialog" />
    <v-responsive class="align-center text-center fill-height">
      <Hero />
      <v-divider class="my-7"></v-divider>
      <Validator></Validator>
      <v-divider class="my-7"></v-divider>
      <Aggregator></Aggregator>
      <v-divider class="my-7"></v-divider>
      <Upload></Upload>
    </v-responsive>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from "vue";
import WelcomeDialog from "@/components/home/WelcomeDialog.vue";
import Hero from "@/components/home/Hero.vue";
import Validator from "@/components/home/Validator.vue";
import Aggregator from "@/components/home/Aggregator.vue";
import Upload from "@/components/home/Upload.vue";

const dialog = ref(false);
</script>
