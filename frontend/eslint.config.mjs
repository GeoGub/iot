import eslint from '@eslint/js';
import tsParser from '@typescript-eslint/parser';
import reactPlugin from 'eslint-plugin-react';
import reactHooksPlugin from 'eslint-plugin-react-hooks';
import jsxA11yPlugin from 'eslint-plugin-jsx-a11y';
import importPlugin from 'eslint-plugin-import';
import prettierPlugin from 'eslint-plugin-prettier';
import tsPlugin from '@typescript-eslint/eslint-plugin';
import globals from 'globals';

export default [
  // Базовые правила ESLint
  eslint.configs.recommended,
  
  // TypeScript
  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      globals: {
        ...globals.node,
        ...globals.browser,
      },
      parser: tsParser,
      parserOptions: {
        ecmaFeatures: { jsx: true },
        ecmaVersion: 'latest',
        project: './tsconfig.json',
      },
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
    },
    rules: {
      ...tsPlugin.configs.recommended.rules,
      '@typescript-eslint/no-explicit-any': 'warn',
    },
  },
  
  // React
  {
    files: ['**/*.{jsx,tsx}'],
    plugins: {
      react: reactPlugin,
      'react-hooks': reactHooksPlugin,
      'jsx-a11y': jsxA11yPlugin,
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
    rules: {
      ...reactPlugin.configs.recommended.rules,
      ...reactHooksPlugin.configs.recommended.rules,
      ...jsxA11yPlugin.configs.recommended.rules,
      'react/react-in-jsx-scope': 'off',
      'react/prop-types': 'off',
    },
  },
  
  // Импорты
  {
    plugins: { import: importPlugin },
    rules: {
      ...importPlugin.configs.recommended.rules,
      'import/order': [
        'error',
        {
          "groups": [
            "builtin", // Встроенные модули (fs, path)
            "external", // npm-пакеты (react, next, axios)
            "internal", // Алиасы (@/components, @/utils)
            "parent", // Родительские модули (../)
            "sibling", // Соседние файлы (./Component)
            "index" // index.ts файлы
          ],
          "newlines-between": "always", // Отделяет группы пустой строкой
          "alphabetize": { "order": "asc", "caseInsensitive": true } // Сортировка по алфавиту
        },
      ],
    },
    settings: {
      'import/resolver': {
        typescript: {}
      }
    }
  },
  
  // Интеграция с Prettier
  {
    plugins: { prettier: prettierPlugin },
    rules: {
      ...prettierPlugin.configs.recommended.rules,
      'prettier/prettier': 'error',
    },
  },
  {
    ignores: [
      'node_modules',
      'dist',
      'build',
      'next.config.js',
      'postcss.config.js',
      'tailwind.config.js',
      'tsconfig.json',
      'next-env.d.ts',
      '*.css',
      '*.md',
      'src/components/ui/*',
    ]
  },
  // env
];