<template>
  <div>
    <h1>Administrationsbereich</h1>
    <p class="pb-8">
      Willkommen im Administrationsbereich. Hier können Sie die verschiedenen
      Funktionen der Anwendung verwalten.
    </p>

    <v-row class="my-4">
      <v-col cols="12" md="6">
        <v-card variant="flat">
          <v-card-title>Variablen & Kategorien</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            Hier sind alle Variablen aus dem Datenschema aufgelistet. Sie können
            hier die Variablen einsehen und Informationen über sie erhalten.
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" link :to="{ name: 'AdminVariables' }">
              Zu den Variablen & Kategorien
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card variant="flat">
          <v-card-title>Aggregationsregeln</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            Hier sind die Aggregationsregeln festgehalten. Derzeit können
            Aggregationsregeln nur angezeigt, aber nicht bearbeitet werden.
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" link :to="{ name: 'AdminAggregations' }">
              Zu den Aggregationsregeln
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card variant="tonal">
          <v-card-title>Beratungsstellen</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            Hier sind alle Beratungsstellen aufgelistet, die in der
            Zentralstatistik hinterlegt sind. Hier können Sie die
            <strong>E-Mail-Adressen der Beratungsstellen verwalten</strong>.
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" link :to="{ name: 'AdminOrganisations' }">
              Beratungsstellen verwalten
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card variant="tonal">
          <v-card-title>Einladungen</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            Hier sind alle Einladungen aufgelistet, die an Beratungsstellen
            verschickt wurden. Hier können Sie außerdem
            <strong>neue Einladungen verschicken</strong>.
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" link :to="{ name: 'AdminInvitations' }">
              Einladungen verwalten
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card variant="flat">
          <v-card-title>Admin-Verwaltung</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            Hier sind alle Administrator:innen aufgelistet, die in der Anwendung
            registriert sind. Sie können hier
            <strong>neue Administrator:innen hinzufügen </strong>.
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" link :to="{ name: 'AdminListUsers' }">
              Benutzer verwalten
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
