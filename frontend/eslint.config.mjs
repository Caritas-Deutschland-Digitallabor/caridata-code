import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import tsParser from "@typescript-eslint/parser";
import pluginVue from "eslint-plugin-vue";

export default [
  {
    files: ["*.ts", "*.tsx", "*.vue"],
    languageOptions: {
      globals: globals.browser,
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 2020,
        sourceType: "module",
        project: "./tsconfig.json",
        extraFileExtensions: [".vue"],
      },
    },
    plugins: {
      "@typescript-eslint": tseslint,
      pluginVue,
    },
    rules: {
      ...pluginJs.configs.recommended.rules,
      ...tseslint.configs.recommended.rules,
      ...pluginVue.configs["flat/recommended"],
      "vue/no-parsing-error": "off", // Turn off no-parsing-error rule
      "@typescript-eslint/no-non-null-assertion": "off", // Turn off no-non-null-assertion rule if necessary
    },
  },
];
