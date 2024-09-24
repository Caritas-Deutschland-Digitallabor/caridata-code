<template>
  <div>
    <v-alert
      v-if="!sbFileStore.allFilesUploaded()"
      type="warning"
      variant="outlined"
      class="my-2"
    >
      Bitte alle Dateien hochladen und validieren, um die Aggregation zu starten! Es fehlt noch
      die Validierung folgender Dateien:
      <b> {{ sbFileStore.missingFiles().join(", ").toUpperCase() }}</b
      >.
    </v-alert>
    <v-card
      v-else
      v-for="aggregation in aggregations"
      :key="aggregation.id"
      variant="outlined"
      class="my-2"
    >
      <v-card-title class="text-overline"
        >{{ aggregation.id + 1 }}: {{ aggregation.name }}</v-card-title
      >
      <v-card-text>{{ aggregation.description_aggregation }}</v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer
        ><v-btn @click="testAggregation(aggregation.id)">Testen</v-btn>
      </v-card-actions>
      <v-card-text v-if="results[aggregation.id]?.length > 0">
        <v-data-table-virtual
          :headers="[
            {
              title: aggregation.grouping_variable_1_id,
              value: 'grouping_category_1_value',
            },
            {
              title: aggregation.grouping_variable_2_id || '-',
              value: 'grouping_category_2_value',
            },
            { title: 'Anzahl', value: 'value' },
          ]"
          :items="results[aggregation.id]"
          hide-default-footer
        >
          <!-- Format category values -->
          <template #item.key_primary="{ item }">
            {{
              getCategoryLabel(
                aggregation.grouping_variable_1_id,
                item.key_primary,
              )
            }}
          </template>
          <template #item.key_secondary="{ item }">
            {{
              aggregation.grouping_variable_2_id && item.key_secondary
                ? getCategoryLabel(
                    aggregation.grouping_variable_2_id,
                    item.key_secondary,
                  )
                : ""
            }}
          </template>
        </v-data-table-virtual>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, toRaw, watch } from "vue";
import { DataItem, AggregationResult } from "@/types/Aggregation";
import { useSchemaStore } from "@/stores/schema";
import apiClient from "@/plugins/api-client";
import { AggregationFilterConditions, AggregationOut } from "@/services";
import $_ from "lodash";
import { useSbFilesStore } from "@/stores/sbfiles";
import { FileSBType } from "@/types/Schema";
import { useStatisticsStore } from "@/stores/statistics";

const schemaStore = useSchemaStore();
const sbkern1Schema = ref(schemaStore.getSchema("SBKERN1"));

const sbFileStore = useSbFilesStore();

const statisticsStore = useStatisticsStore();

const aggregations = ref<AggregationOut[]>([]);

const fetchAggregations = async () => {
  aggregations.value = await apiClient.aggregations.listAggregations();
};

onMounted(() => {
  fetchAggregations();
});

const results = ref<{ [id: string]: AggregationResult[] }>({
  "0": [],
  "1": [],
  "2": [],
});

const createFilterConditionExpression = (
  cond: AggregationFilterConditions,
  entry: DataItem,
): boolean => {
  const field = cond.field;
  const value = cond.value;
  const operator = cond.condition;

  switch (operator) {
    case "=":
      return entry[field] == value;
    case ">":
      return entry[field] > value;
    case "<":
      return entry[field] < value;
    case ">=":
      return entry[field] >= value;
    case "<=":
      return entry[field] <= value;
    case "!=":
      return entry[field] != value;
    case "IS":
      if (value === "NULL") {
        return (
          entry[field] === null ||
          entry[field] === undefined ||
          entry[field] === "" ||
          entry[field] === 0
        );
      }
      console.error("IS operator only supports NULL value");
      return false;
    case "IS NOT":
      if (value === "NULL") {
        return (
          entry[field] !== null &&
          entry[field] !== undefined &&
          entry[field] !== "" &&
          entry[field] !== 0
        );
      }
      console.error("IS NOT operator only supports NULL value");
      return false;
    default:
      console.error("Unknown operator");
      return false;
  }
};

const createFilterExpression = (
  aggregation: AggregationOut,
  entry: DataItem,
): boolean => {
  if (!aggregation.filter) {
    return true;
  }
  if (aggregation.filter.operator === "OR") {
    return aggregation.filter.conditions.some((cond) => {
      return createFilterConditionExpression(cond, entry);
    });
  } else {
    return aggregation.filter.conditions.every((cond) => {
      return createFilterConditionExpression(cond, entry);
    });
  }
};

// Function to perform aggregation
function aggregateData(aggregation: AggregationOut): AggregationResult[] {
  // Step 0: Get file to aggregate
  const dataset = sbFileStore.getSbFile(
    aggregation.source.toUpperCase() as FileSBType,
  ).rows;
  const rawData = toRaw(dataset);
  // Step 1: From clause using source attribute
  // Step 2: Where clause using filter attribute
  const filteredData = $_.filter(rawData, (entry) => {
    return createFilterExpression(aggregation, entry);
  });
  // Step 3: Group by clause using grouping_variable_1_id, grouping_variable_2_id attributes
  let groupedData;
  if (!aggregation.grouping_variable_1_id) {
    groupedData = { "1": filteredData };
  } else {
    if (aggregation.grouping_variable_2_id) {
      groupedData = $_.groupBy(filteredData, (entry) => {
        return (
          entry[aggregation.grouping_variable_1_id as string] +
          "-" +
          entry[aggregation.grouping_variable_2_id as string]
        );
      });
    } else {
      groupedData = $_.groupBy(filteredData, (entry) => {
        return entry[aggregation.grouping_variable_1_id as string];
      });
    }
  }
  // Step 4: Unique
  let distinctData;
  if (aggregation.is_distinct) {
    for (const key in groupedData) {
      groupedData[key] = $_.uniqBy(
        groupedData[key],
        aggregation.aggregation_variable_name,
      );
    }
  }
  distinctData = groupedData;

  // Step 5: Aggregation Function
  // Check aggregation functions needed
  let aggregatedData: AggregationResult[] = [];
  if (aggregation.aggregation_type === "COUNT") {
    const { grouping_variable_1_id, grouping_variable_2_id } = aggregation;
    $_.forEach(distinctData, (items, key) => {
      const firstItem = $_.first(items);
      if (!firstItem) {
        return;
      }

      const aggregatedResult: AggregationResult = {
        aggregation_id: aggregation.id,
        organisation_id: "test_organisation",
        period_level: "test_period_level",
        period: "2024-01-01",
        value: items.length,
        upload_id: "test_upload_id",
      };

      if (grouping_variable_1_id) {
        aggregatedResult["grouping_variable_1_id"] = grouping_variable_1_id;
        aggregatedResult["grouping_category_1_value"] =
          firstItem[grouping_variable_1_id]?.toString();
      }

      if (grouping_variable_2_id) {
        aggregatedResult["grouping_variable_2_id"] = grouping_variable_2_id;
        aggregatedResult["grouping_category_2_value"] =
          firstItem[grouping_variable_2_id]?.toString();
      }
      aggregatedData.push(aggregatedResult);
    });
  }
  return $_.values(aggregatedData);
}

const testAggregation = (index: string) => {
  const aggregation = aggregations.value.find((a) => a.id === index);
  if (!aggregation) {
    return;
  }
  const result = aggregateData(aggregation);
  results.value[aggregation.id] = result;
  for (let aggregation of aggregations.value) {
    statisticsStore.addStatistics(aggregateData(aggregation));
  }
};

watch(
  () => sbFileStore.allFilesUploaded(),
  () => {
    if (sbFileStore.allFilesUploaded()) {
      for (let aggregation of aggregations.value) {
        statisticsStore.addStatistics(aggregateData(aggregation));
      }
    }
  },
);

const getCategoryLabel = (
  variable_name: string | null | undefined,
  value: string,
) => {
  const variableSchema = sbkern1Schema.value.find(
    (s) => s.name === variable_name,
  );
  if (!variableSchema) {
    return value;
  }
  if (!variableSchema.categories) {
    return value;
  }
  const category = variableSchema.categories.find(
    (c) => c.value.toString() === value.toString(),
  );
  return category ? category.name : value;
};
</script>
