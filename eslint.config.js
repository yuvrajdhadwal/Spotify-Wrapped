// eslint.config.js

const { ESLint } = require("eslint");

module.exports = [
  {
    files: ["**/*.{js,ts,tsx}"], // Match all JavaScript, TypeScript, and TSX files
    ignores: ["node_modules/", "dist/"], // Ignore common directories
    languageOptions: {
      parser: require("@typescript-eslint/parser"), // Use TypeScript parser
      parserOptions: {
        ecmaVersion: 2020, // Specify ECMAScript version
        sourceType: "module",
      },
    },
    plugins: {
      "@typescript-eslint": require("@typescript-eslint/eslint-plugin"), // Load TypeScript plugin
    },
    rules: {
      // Add ESLint and TypeScript rules
      "no-unused-vars": "warn",
      "no-console": "warn",
      "@typescript-eslint/no-unused-vars": "warn",
      "@typescript-eslint/no-explicit-any": "warn",
    },
  },
];
