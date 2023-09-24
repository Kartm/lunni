/// <reference types="vitest" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import eslint from 'vite-plugin-eslint';

export default defineConfig(() => {
    return {
        build: {
            outDir: 'build',
        },
        plugins: [react(), eslint()],
        test: {
            environment: 'jsdom',
            globals: true,
            setupFiles: './src/setupTests.ts',
        },
    };
});