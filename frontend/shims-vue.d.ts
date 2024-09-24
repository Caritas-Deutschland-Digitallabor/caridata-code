import _ from "lodash";

declare module "@vue/runtime-core" {
  interface ComponentCustomProperties {
    $_: typeof _;
  }
}
