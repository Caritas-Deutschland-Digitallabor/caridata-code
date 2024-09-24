// src/lodash-plugin.ts
import { App } from "vue";
import _ from "lodash";

export default {
  install(app: App): void {
    app.config.globalProperties.$_ = _;
  },
};
