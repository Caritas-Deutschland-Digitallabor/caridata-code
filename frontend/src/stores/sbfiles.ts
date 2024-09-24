import { ParsedData } from "@/types/Data";
import { FileSBType } from "@/types/Schema";
import { defineStore } from "pinia";

export const useSbFilesStore = defineStore({
  id: "sbFiles",
  state: () => ({
    sbkern1: {
      headers: [],
      rows: [],
      hadHeaderInOriginalFile: false,
    } as ParsedData,
    sbkern2: {
      headers: [],
      rows: [],
      hadHeaderInOriginalFile: false,
    } as ParsedData,
    stelle: {
      headers: [],
      rows: [],
      hadHeaderInOriginalFile: false,
    } as ParsedData,
    sbveran: {
      headers: [],
      rows: [],
      hadHeaderInOriginalFile: false,
    } as ParsedData,
    sbkont: {
      headers: [],
      rows: [],
      hadHeaderInOriginalFile: false,
    } as ParsedData,
  }),
  actions: {
    setSbkern1(data: ParsedData) {
      this.sbkern1 = data;
    },
    setSbkern2(data: ParsedData) {
      this.sbkern2 = data;
    },
    setStelle(data: ParsedData) {
      this.stelle = data;
    },
    setSbveran(data: ParsedData) {
      this.sbveran = data;
    },
    setSbkont(data: ParsedData) {
      this.sbkont = data;
    },
    allFilesUploaded(): boolean {
      return (
        this.sbkern1.headers.length > 0 &&
        this.sbkern2.headers.length > 0 &&
        this.stelle.headers.length > 0 &&
        this.sbveran.headers.length > 0 &&
        this.sbkont.headers.length > 0
      );
    },
    missingFiles(): string[] {
      const missingFiles = [];
      if (this.sbkern1.headers.length === 0) {
        missingFiles.push("sbkern1");
      }
      if (this.sbkern2.headers.length === 0) {
        missingFiles.push("sbkern2");
      }
      if (this.stelle.headers.length === 0) {
        missingFiles.push("stelle");
      }
      if (this.sbveran.headers.length === 0) {
        missingFiles.push("sbveran");
      }
      if (this.sbkont.headers.length === 0) {
        missingFiles.push("sbkont");
      }
      return missingFiles;
    },
    self,
  },
  getters: {
    getSbkern1: (state): ParsedData => {
      return state.sbkern1;
    },
    getSbkern2: (state): ParsedData => {
      return state.sbkern2;
    },
    getStelle: (state): ParsedData => {
      return state.stelle;
    },
    getSbveran: (state): ParsedData => {
      return state.sbveran;
    },
    getSbkont: (state): ParsedData => {
      return state.sbkont;
    },
    getSbFile:
      (state) =>
      (sbFile: FileSBType): ParsedData => {
        switch (sbFile) {
          case "SBKERN1":
            return state.sbkern1;
          case "SBKERN2":
            return state.sbkern2;
          case "STELLE":
            return state.stelle;
          case "SBVERAN":
            return state.sbveran;
          case "SBKONT":
            return state.sbkont;
        }
      },
  },
});
