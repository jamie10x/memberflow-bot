import globals from "globals";
import pluginJs from "@eslint/js";
import pluginReact from "eslint-plugin-react";
import pluginReactHooks from "eslint-plugin-react-hooks";
import pluginReactRefresh from "eslint-plugin-react-refresh";

export default [
    // Global configuration
    {
        files: ["**/*.{js,mjs,cjs,jsx}"],
        plugins: {
            react: pluginReact,
            'react-hooks': pluginReactHooks,
            'react-refresh': pluginReactRefresh,
        },
        languageOptions: {
            parserOptions: {
                ecmaFeatures: {
                    jsx: true,
                },
            },
            globals: {
                ...globals.browser,
                // This is the key fix. We declare the entire Telegram object structure.
                Telegram: 'readonly',
            },
        },
        // Rules for all JS/JSX files
        rules: {
            ...pluginReact.configs.recommended.rules,
            ...pluginReactHooks.configs.recommended.rules,
            'react-refresh/only-export-components': 'warn',
            // You can add other rules here if needed
        },
    },
    // Apply JS-specific recommended rules
    pluginJs.configs.recommended,
];