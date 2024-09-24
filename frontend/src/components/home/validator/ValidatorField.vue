<template>
  <div class="text-left" style="margin-top: 8px !important">
    <v-container fluid style="border: 2px solid #000">
      <v-card
        style="width: 100%"
        variant="text"
        class="mx-auto"
        color="surface-variant"
        :subtitle="'Laden Sie in dieses Feld ihre ' + fileSBType + ' Datei.'"
        :title="fileSBType"
      >
        <v-file-input
          :rules="rules"
          v-model="file"
          :error="hasError"
          label="Dateien hierhin ziehen oder klicken, um Dateisystem zu durchsuchen."
          name="file"
          variant="solo"
          hide-details
          class="no-prepend-icon square-file-input pa-4"
          clearable
          flat
          :prepend-inner-icon="file?.length > 0 ? 'mdi-file' : 'mdi-upload'"
        ></v-file-input>
        <template v-slot:actions>
          <v-btn
            class="ma-4"
            variant="tonal"
            @click="validate"
            :disabled="file?.length === 0 || !file"
            :key="JSON.stringify(file)"
            :color="
              hasError
                ? 'error'
                : dataset?.headers?.length > 0
                  ? 'success'
                  : 'black'
            "
            >{{
              hasError
                ? "Fehler"
                : dataset?.headers?.length > 0
                  ? "Validiert"
                  : "Inhalt Validieren"
            }}</v-btn
          >
          <v-btn
            class="ma-4"
            variant="text"
            :disabled="dataset?.headers?.length <= 0"
            @click="showEval = !showEval"
            >Ergebnis anzeigen</v-btn
          >
        </template>
      </v-card>
      <v-alert
        v-for="error in errorMessages"
        :key="error.message"
        v-if="hasError && dataset?.headers?.length === 0"
        type="error"
        class="mx-4 mb-4"
        :title="error.header"
        icon="$error"
        outlined
        dense
        variant="tonal"
      >
        <div v-html="error.message"></div>
      </v-alert>
      <v-card v-if="showEval" variant="outlined" class="mb-4">
        <v-card-title>Validierungsergebnisse</v-card-title>
        <v-card-text>
          <p v-if="!hasError">
            Die Validierung war erfolgreich. Die Datei konnte gelesen werden und
            alle Informationen stimmen mit dem Datenschema überein. Insgesamt
            enthält die Datei
            {{ dataset.rows.length }} Zeile(n).
          </p>
          <p v-if="hasError">
            <v-icon color="error">mdi-alert-circle-outline</v-icon>
            Die Validierung wurde durchgeführt. Die Daten konnten geladen
            werden, des sind jedoch Fehler aufgetreten. Bitte überprüfen Sie die
            folgenden Fehler:
            <span
              class="font-weight-bold"
              v-for="error in errorMessages"
              :key="error.message"
              >{{ error.message }}</span
            >
          </p>
          <p>
            <v-data-table
              :items="dataset.rows"
              :items-per-page="5"
            ></v-data-table>
          </p>
        </v-card-text>
      </v-card>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import Papa, { ParseResult } from "papaparse";
import { ref, watch } from "vue";
import { Dbf } from "dbf-reader";
import { DataTable } from "dbf-reader/models/dbf-file";
import { FileType, ParsedData, RequiredColumn, Row } from "@/types/Data";
import { ErrorMessages, IncorrectTypes, RequiredTypes } from "@/types/Errors";
import { mimeTypeRule } from "@/utils/fileRules";
import {
  hasRequiredColumns,
  isValidDBF,
  isValidPlainText,
} from "@/utils/fileValidation";
import { useSchemaStore } from "@/stores/schema";
import {
  errorFileTypeNotSupported,
  errorInvalidColumns,
  errorInvalidFileType,
  errorInvalidTypes,
  errorParsingFile,
} from "@/utils/errorMessages";
import { papaParseConfig } from "@/utils/papaParseConfig";
import { hasCorrectTypes } from "@/utils/typeValidation";
import { isSameFile } from "@/utils/utilityFunctions";
import { FileSBType } from "@/types/Schema";

const props = defineProps<{
  fileSBType: FileSBType;
}>();

const dataset = defineModel<ParsedData>("dataset", { required: true });
const file = ref<any>(null);
const showEval = ref(false);

const schemaStore = useSchemaStore();
const schema = ref(schemaStore.getSchema(props.fileSBType));

const rules = [
  (value: FileList) => {
    return !value || !value[0] || mimeTypeRule(value[0]);
  },
];
const hasError = ref(false);
const errorMessages = ref<ErrorMessages[]>();

const missingColumns = ref<string[] | undefined>([]);
const incorrectTypes = ref<IncorrectTypes[]>([]);
const requiredColumns = ref<RequiredColumn[]>([]);
const requiredTypes = ref<RequiredTypes>({});
const fileType = ref<FileType>();

const readFileContent = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (event: any) => resolve(event.target.result);
    reader.onerror = (error) => reject(error);
    if (fileType.value?.type === "plainText") {
      reader.readAsText(file);
    } else if (fileType.value?.type === "dbf") {
      reader.readAsArrayBuffer(file);
    } else {
      reject(errorFileTypeNotSupported);
    }
  });
};

watch(file, (newVal, oldVal) => {
  if (newVal.length === 0 || (oldVal && !isSameFile(newVal[0], oldVal[0]))) {
    hasError.value = false;
    errorMessages.value = [];
    showEval.value = false;
    dataset.value = {
      headers: [],
      rows: [],
      hadHeaderInOriginalFile: false,
    };
  }
});

const setRequiredValues = () => {
  requiredColumns.value = schema.value.map((item) => {
    return {
      name: item.name,
      mandatory: item.mandatory,
      technical_mandatory: item.technical_mandatory,
    };
  });
  requiredTypes.value = schema.value.reduce<RequiredTypes>((acc, item) => {
    acc[item.name] = item.type ?? "none";
    return acc;
  }, {});
};

const removeIndexColumn = (dataTable: ParseResult<string[]>) => {
  dataTable.data = dataTable.data.map((row) => row.slice(1));
  return dataTable;
};

const transformData = (
  dataTable: ParseResult<string[]> | DataTable,
): ParsedData => {
  // Definition: Headers always to Lower Case
  let transformedTable: ParsedData;
  if (fileType.value?.type === "dbf") {
    dataTable = dataTable as DataTable;
    transformedTable = {
      headers: dataTable.columns.map((item) => item.name.toLowerCase()),
      rows: dataTable.rows.map((row) => {
        let newRow: Row = {};
        for (let key in row) {
          newRow[key.toLowerCase()] = row[key] || "";
        }
        return newRow;
      }),
      hadHeaderInOriginalFile: true,
    };
  } else {
    // Text Based File Cases:
    // 1. CSV with header & index
    // 2. CSV without header & index
    // 3. TXT without header
    // 4. Additional unrelated columns at end of file
    let dataTableTyped = dataTable as ParseResult<string[]>;

    // Assumption: Every value is a string is an indicator for heading
    let hasHeader = dataTableTyped.data[0].every((item, index) => {
      if (index === 0) {
        return (
          isNaN(Number(item)) || item === "" || item === " " || item === null
        );
      } else {
        return isNaN(Number(item));
      }
    });

    if (fileType.value?.subType === "csv" && hasHeader) {
      dataTable = removeIndexColumn(dataTableTyped);
    }

    let headers = hasHeader
      ? dataTableTyped.data[0].map((item) => item.toString().toLowerCase())
      : requiredColumns.value.map((item) => item.name);
    if (hasHeader) {
      // remove header row
      dataTableTyped.data.shift();
    }

    transformedTable = {
      headers: headers,
      rows: dataTableTyped.data.map((row) => {
        let newRow: Row = {};
        for (let i = 0; i < row.length; i++) {
          newRow[headers[i]] = row[i];
        }
        return newRow;
      }),
      hadHeaderInOriginalFile: hasHeader,
    };
  }
  return transformedTable;
};

const validateContent = (content: string) => {
  if (!fileType.value) {
    errorMessages.value = [errorFileTypeNotSupported("unknown")];
    hasError.value = true;
    return;
  }
  // 0. Parse the file
  let dataTable: DataTable | ParseResult<string[]>;
  let isValid = false;
  if (fileType.value?.type === "plainText") {
    dataTable = Papa.parse(content, papaParseConfig);
    isValid = isValidPlainText(dataTable);
  } else {
    let buffer: any = Buffer.from(content);
    dataTable = Dbf.read(buffer);
    isValid = isValidDBF(dataTable);
  }
  // 1. Check if the file is valid
  if (!isValid) {
    errorMessages.value = [
      errorInvalidFileType(
        fileType.value.subType ? fileType.value.subType : fileType.value.type,
      ),
    ];
    hasError.value = true;
  } else {
    // 2. Transform the data
    let transformedData = transformData(dataTable);
    // 3. Check if the file has the required columns
    const [hasRequiredColumnsResult, missingColumnsResult] = hasRequiredColumns(
      transformedData,
      requiredColumns.value,
    );
    missingColumns.value = missingColumnsResult;
    if (!hasRequiredColumnsResult) {
      errorMessages.value = [
        errorInvalidColumns(missingColumns.value, props.fileSBType),
      ];
      hasError.value = true;
    } else {
      // 4. Check if the file has the correct types
      const [hasCorrectTypesResult, incorrectTypesResult] = hasCorrectTypes(
        transformedData,
        requiredTypes.value,
        schema.value,
      );
      incorrectTypes.value = incorrectTypesResult;
      if (!hasCorrectTypesResult) {
        errorMessages.value = [
          errorInvalidTypes(incorrectTypes.value, props.fileSBType),
        ];
        hasError.value = true;
      } else {
        dataset.value = transformedData;
      }
    }
  }
};

const validateFileExtension = (file: any) => {
  const fileExtension = file[0].name.split(".").pop().toLowerCase();
  if (fileExtension === "dbf") {
    fileType.value = { type: "dbf", subType: undefined };
  } else if (fileExtension === "csv" || fileExtension === "txt") {
    fileType.value = { type: "plainText", subType: fileExtension };
  } else {
    errorMessages.value = [errorFileTypeNotSupported(fileExtension)];
    hasError.value = true;
  }
};

const validateFile = async (file: any) => {
  setRequiredValues();

  // Reset validation states
  missingColumns.value = [];
  incorrectTypes.value = [];
  errorMessages.value = [];
  hasError.value = false;

  if (file.value) {
    validateFileExtension(file.value);
    if (hasError.value) {
      return;
    }
    try {
      const content = await readFileContent(file.value[0]);
      validateContent(content);
    } catch (error: any) {
      errorMessages.value = [errorParsingFile(error)];
      hasError.value = true;
    }
  }
};

const validate = async () => {
  try {
    await validateFile(file);
  } catch (error) {
    console.error("Error during validation:", props.fileSBType, error);
  }
};
</script>

<style>
.no-prepend-icon .v-input__prepend {
  display: none;
}

.square-file-input .v-input__control {
  padding-left: 0;
  margin-left: 2;
  border: 4px dashed #ccc; /* Dashed border with light grey color */
  border-radius: 10px; /* Rounded corners */
  height: 100px; /* Höhe setzen */
  width: 100%; /* Breite setzen */
}

.square-file-input .v-label {
  white-space: normal; /* Textumbruch zulassen */

  transform: none !important;
  transition: none !important;

  top: 0 !important;
  left: 0 !important;
  display: flex; /* Use flexbox for layout */
  align-items: center; /* Center vertically */
  height: 100%; /* Ensure label takes full height */
}
.square-file-input .v-input__control .v-field__clearable {
  width: 100% !important;
}

.square-file-input .v-field--active .v-label.v-field-label--floating {
  color: transparent !important;
}

.square-file-input .v-input__control .v-field__input {
  padding: 0px;
  padding-left: 8px;
  display: flex; /* Use flexbox for layout */
  align-items: center; /* Center vertically */
  height: 100%; /* Ensure label takes full height */
}

ul {
  list-style: none;
  border: 9px solid transparent;
}
</style>
