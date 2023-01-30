import react from '@vitejs/plugin-react-swc';
import tsconfigPaths from 'vite-tsconfig-paths';
import { defineConfig } from 'vite';

import bundleAnalyzer from "rollup-plugin-bundle-analyzer";


// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		react(), 
		tsconfigPaths(),
	],
	build: {
		outDir: 'build',
		rollupOptions: {
			plugins: [
				bundleAnalyzer({}),
			],
			output: {
				manualChunks: {
					mantine: ['@mantine/core'],
					apollo: ['@apollo/client'],
				}
			}
		},
	},
	server: {
		host: 'localhost',
		port: 5173,
		hmr: {
			host: 'localhost',
			clientPort: 80
		}
	},
})