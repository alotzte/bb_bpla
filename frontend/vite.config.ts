import { defineConfig } from 'vite';
import viteTsconfigPaths from 'vite-tsconfig-paths';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    viteTsconfigPaths(),
    react({
      babel: {
        plugins: [['effector/babel-plugin', { addLoc: true }]],
      },
    }),
  ],
  server: {
    port: 3000,
  },
  build: {
    outDir: 'build',
    emptyOutDir: true,
  },
});
