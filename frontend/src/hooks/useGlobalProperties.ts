import { getCurrentInstance } from "vue";

export function useGlobalProperties() {
  const instance = getCurrentInstance();
  if (!instance) {
    throw new Error("useGlobalProperties must be used within a setup function");
  }
  return instance.appContext.config.globalProperties;
}
