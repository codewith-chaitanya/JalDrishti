import js from '@eslint/js'
import globals from 'globals'
import react from 'eslint-plugin-react'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'

export default [
  // 1. GLOBAL IGNORES (Replaces globalIgnores function for better compatibility)
  { ignores: ['dist', 'node_modules', 'build'] },

  {
    files: ['**/*.{js,jsx}'],
    plugins: {
      // 2. BUG FIX: Explicitly define plugins for Flat Config
      'react': react,
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    languageOptions: {
      ecmaVersion: 'latest', // Consistency: use latest everywhere
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.es2020,
      },
      parserOptions: {
        ecmaFeatures: { jsx: true },
      },
    },
    // 3. FIXED: Proper extension of recommended settings
    rules: {
      ...js.configs.recommended.rules,
      ...react.configs.recommended.rules,
      ...react.configs['jsx-runtime'].rules,
      ...reactHooks.configs.recommended.rules,

      // 4. LOOPHOLE FIX: Strict Unused Variables
      // We only ignore variables starting with underscore (standard convention)
      'no-unused-vars': ['warn', { 
        vars: 'all', 
        args: 'after-used', 
        ignoreRestSiblings: true, 
        varsIgnorePattern: '^_' 
      }],

      // 5. React Refresh safety
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],

      // Additional Best Practices
      'react/prop-types': 'off', // Turn off if using JS, or keep 'warn' if you want prop checks
      'no-console': ['warn', { allow: ['warn', 'error'] }], // Prevent spamming console.log
    },
    settings: {
      react: { version: 'detect' }, // Automatically detect React version
    },
  },
]