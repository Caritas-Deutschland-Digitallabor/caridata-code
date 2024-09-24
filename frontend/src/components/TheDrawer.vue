<template>
  <v-navigation-drawer permanent>
    <v-list v-if="userStore.isAuthenticated">
      <v-list-item
        :title="userStore.user!.name"
        :subtitle="userStore.user!.email"
      >
        <template #prepend>
          <v-avatar color="primary" rounded="lg">
            {{ "test".charAt(0).toUpperCase() }}
          </v-avatar>
        </template>
      </v-list-item>
      <v-divider />
    </v-list>
    <v-list dense nav>
      <v-list-item title="Datenupload Validierung" link :to="{ name: 'Home' }">
        <template #prepend>
          <v-icon icon="mdi-open-in-app" />
        </template>
      </v-list-item>
    </v-list>
    <v-divider />

    <v-list
      v-if="userStore.isAuthenticated && userStore.isAdmin"
      density="compact"
      nav
    >
      <v-list-subheader>Datenschema</v-list-subheader>
      <v-list-item
        title="Variablen & Kategorien"
        link
        :to="{ name: 'AdminVariables' }"
      >
        <template #prepend>
          <v-icon icon="mdi-format-list-text" />
        </template>
      </v-list-item>
      <v-list-item
        title="Aggregationsregeln"
        link
        :to="{ name: 'AdminAggregations' }"
      >
        <template #prepend>
          <v-icon icon="mdi-shape-outline" />
        </template>
      </v-list-item>
      <v-divider />
    </v-list>

    <v-list
      v-if="userStore.isAuthenticated && userStore.isAdmin"
      density="compact"
      nav
    >
      <v-list-subheader>Beratungsstellen</v-list-subheader>
      <v-list-item
        title="Beratungsstellen"
        link
        :to="{ name: 'AdminOrganisations' }"
      >
        <template #prepend>
          <v-icon icon="mdi-folder-account" />
        </template>
      </v-list-item>
      <v-list-item title="Einladungen" link :to="{ name: 'AdminInvitations' }">
        <template #prepend>
          <v-icon icon="mdi-mail" />
        </template>
      </v-list-item>
      <v-divider />
    </v-list>

    <v-list v-if="userStore.isAuthenticated" density="compact" nav>
      <v-list-subheader>Administration</v-list-subheader>
      <v-list-item
        v-if="userStore.isAdmin"
        title="Admin-Accounts"
        link
        :to="{ name: 'AdminListUsers' }"
      >
        <template #prepend>
          <v-icon icon="mdi-account-multiple-outline" />
        </template>
      </v-list-item>
      <!--
      <v-list-item title="Mein Account" link>
        <template v-slot:prepend>
          <v-icon icon="mdi-account-edit-outline"></v-icon>
        </template>
      </v-list-item>
      -->
      <v-divider />
    </v-list>

    <template #append>
      <v-divider />

      <v-list v-if="userStore.isAuthenticated" dense nav>
        <v-list-item title="Logout" link @click="logout">
          <template #prepend>
            <v-icon icon="mdi-logout" />
          </template>
        </v-list-item>
      </v-list>
      <v-list v-else dense nav>
        <v-list-item title="Login" link @click="login">
          <template #prepend>
            <v-icon icon="mdi-login" />
          </template>
        </v-list-item>
      </v-list>
    </template>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import apiClient from "../plugins/api-client";
import { useUserStore } from "../stores/user";

const userStore = useUserStore();

const router = useRouter();

const login = () => {
  router.push({ name: "Login" });
};

const logout = async () => {
  try {
    router.push({ name: "Home" });
    await apiClient.auth.authDbLogout();
  } finally {
    userStore.user = undefined;
  }
};
</script>
