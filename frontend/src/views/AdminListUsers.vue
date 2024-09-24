<template>
  <v-container>
    <v-expand-transition>
      <div>
        <v-alert v-if="error" type="error" rounded="0" closable>
          {{ error }}
        </v-alert>
      </div>
    </v-expand-transition>
    <h1 class="mb-8">Alle Accounts</h1>
    <v-row>
      <v-col cols="12" class="d-flex flex-row-reverse">
        <create-user />
      </v-col>
    </v-row>

    <div v-if="isLoading">
      <v-skeleton-loader color="transparent" type="heading" class="my-2" />
    </div>
    <div v-else-if="users.length > 0">
      <v-card
        v-for="user in users"
        :key="user.email"
        :user="user"
        variant="outlined"
        class="my-2 pa-2 d-flex align-center"
      >
        <v-avatar variant="tonal" rounded="lg" class="mr-4">
          <strong>{{ user.name.charAt(0) }}</strong>
        </v-avatar>

        <div>
          <p class="text-subtitle-2">
            {{ user.name }}
          </p>
          <p class="text-caption text-medium-emphasis">
            {{ user.email }}
          </p>
        </div>
        <v-spacer />
        <v-menu>
          <template #activator="{ props }">
            <v-btn
              v-if="user.id !== userStore.user?.id"
              v-bind="props"
              icon="mdi-dots-vertical"
              class="ml-2"
              size="small"
              variant="flat"
            />
            <v-btn
              v-else
              icon="mdi-lock"
              class="ml-2"
              size="small"
              variant="text"
              disabled
            />
          </template>
          <v-list class="py-0">
            <app-delete-dialog
              :delete-type="'Account'"
              @delete="deleteUser(user.id)"
            >
              <template #title> Account löschen </template>
              <div>
                Wollen Sie wirklich den Account
                <strong>{{ user.name }}</strong>
                löschen? Dies kann nicht rückgängig gemacht werden.
              </div>
            </app-delete-dialog>
          </v-list>
        </v-menu>
      </v-card>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import apiClient from "../plugins/api-client";
import { useUserStore } from "../stores/user";
import { useQuery, useMutation } from "@tanstack/vue-query";

const userStore = useUserStore();

const {
  isLoading,
  data: users,
  error,
} = useQuery({
  queryKey: ["users"],
  queryFn: async () => {
    const response = await apiClient.users.listUsers();
    return response;
  },
  initialData: [],
});

const { mutate: deleteUser } = useMutation({
  mutationFn: async (id: string) => {
    await apiClient.users.deleteUser(id);
  },
});
</script>
