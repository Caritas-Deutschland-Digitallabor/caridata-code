import { defineStore } from "pinia";
import { FileSBType } from "@/types/Schema";
import apiClient from "@/plugins/api-client";
import { SchemaOut } from "@/services/models/SchemaOut";

export const useSchemaStore = defineStore({
  id: "schema",
  state: () => ({
    _sbkern1Schema: [] as SchemaOut[],
    _sbkern2Schema: [] as SchemaOut[],
    _stelleSchema: [] as SchemaOut[],
    _sbveranSchema: [] as SchemaOut[],
    _sbkontSchema: [] as SchemaOut[],
  }),
  actions: {
    async fetchSchemas(): Promise<void> {
      const response_sbkern1 = await apiClient.variables.listVariables(
        undefined,
        "sbkern1",
      );
      this._sbkern1Schema = response_sbkern1;
      const response_sbkern2 = await apiClient.variables.listVariables(
        undefined,
        "sbkern2",
      );
      this._sbkern2Schema = response_sbkern2;
      const response_stelle = await apiClient.variables.listVariables(
        undefined,
        "stelle",
      );
      this._stelleSchema = response_stelle;
      const response_sbveran = await apiClient.variables.listVariables(
        undefined,
        "sbveran",
      );
      this._sbveranSchema = response_sbveran;
      const response_sbkont = await apiClient.variables.listVariables(
        undefined,
        "sbkont",
      );
      this._sbkontSchema = response_sbkont;
    },
    getSchema(type: FileSBType): SchemaOut[] {
      if (type === "SBKERN1") {
        return this._sbkern1Schema;
      } else if (type === "SBKERN2") {
        return this._sbkern2Schema;
      } else if (type === "STELLE") {
        return this._stelleSchema;
      } else if (type === "SBVERAN") {
        return this._sbveranSchema;
      } else if (type === "SBKONT") {
        return this._sbkontSchema;
      } else {
        return [];
      }
    },
  },
  getters: {
    sbkern1Schema: (state): SchemaOut[] => {
      return state._sbkern1Schema;
    },
    sbkern2Schema: (state): SchemaOut[] => {
      return state._sbkern2Schema;
    },
    stelleSchema: (state): SchemaOut[] => {
      return state._stelleSchema;
    },
    sbveranSchema: (state): SchemaOut[] => {
      return state._sbveranSchema;
    },
    sbkontSchema: (state): SchemaOut[] => {
      return state._sbkontSchema;
    },
  },
});
