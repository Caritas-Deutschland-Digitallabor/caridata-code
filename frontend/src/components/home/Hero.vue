<template>
  <div style="min-height: 100vh">
    <div class="py-14" />
    <div class="text-body-2 font-weight-light mb-n1">CariData</div>

    <h1 class="text-h2 font-weight-bold">
      Jahresstatistik <v-chip color="#CC1E1C" class="text-body-1">Test</v-chip>
    </h1>
    <p class="mx-12 pa-12 text-left">
      <b>Willkommen bei CariData!</b> Unsere Plattform erleichtert es den
      Beratungsstellen, ihre Daten einfach und effizient bereitzustellen. Mit
      CariData können Sie Ihre Daten sicher eingeben und zusammenfassen lassen,
      um zur deutschlandweiten Schwangerschaftsstatistik beizutragen.
    </p>

    <p class="text-body-1 font-weight-bold py-6">So funktioniert's:</p>
    <v-row>
      <v-col cols="12" md="4">
        <v-card variant="outlined" height="100%">
          <v-card-title
            ><v-icon>mdi-check</v-icon> 1. Dateneingabe</v-card-title
          >
          <v-card-text>
            Aus ihrem Beratungsstellen-System exportieren Sie die Daten für das
            vergangene Jahr. Diese Daten geben Sie in das CariData-System ein.
          </v-card-text>
          <v-divider></v-divider>
          <v-card-text>
            <v-icon size="sm" icon="mdi-book-lock-outline"></v-icon> Die Daten
            verbleiben auf ihrem System und werden nicht an uns übertragen.
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card variant="outlined" height="100%">
          <v-card-title
            ><v-icon>mdi-check</v-icon> 2. Zusammenfassung</v-card-title
          >
          <v-card-text>
            Das System erstellt eine Statistik. Dabei werden die Daten
            anonymisiert und zusammengefasst.
          </v-card-text>
          <v-spacer></v-spacer>
          <v-divider></v-divider>
          <v-card-text>
            <v-icon size="sm" icon="mdi-book-lock-outline"></v-icon> Die Daten
            verbleiben auf ihrem System und werden nicht an uns übertragen.
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card variant="outlined" height="100%">
          <v-card-title><v-icon>mdi-check</v-icon> 3. Hochladen</v-card-title>
          <v-card-text>
            Die zusammengefassten Daten werden verschlüsselt an das
            CariData-Team übermittelt und für die Jahresstatistik verwendet.
          </v-card-text>
          <v-divider></v-divider>
          <v-card-text>
            <v-icon size="sm" icon="mdi-lock"></v-icon> Die zusammengefassten
            Daten werden verschlüsselt an uns übertragen.
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <p class="py-6 font-weight-bold">
      <v-icon class="mx-2" color="#CC1E1C">mdi-hand-heart</v-icon>Vielen Dank,
      dass sie am Test für das neue System teilnehmen!
    </p>
    <div class="py-14" />
  </div>
</template>
