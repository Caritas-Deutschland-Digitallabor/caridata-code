import { defineStore } from "pinia";
import apiClient from "@/plugins/api-client";
import { AggregationResult } from "@/types/Aggregation";
import { toRaw } from "vue";

export const useStatisticsStore = defineStore({
  id: "statistics",
  state: () => ({
    _statistics: [] as AggregationResult[],
  }),
  actions: {
    async postStatistics(): Promise<void> {
      await apiClient.statistics.addStatistics(toRaw(this._statistics));
    },
    addStatistics(statistics: AggregationResult[]): void {
      this._statistics.push(...statistics);
    },
  },
  getters: {
    statistics(): AggregationResult[] {
      return this._statistics;
    },
  },
});
