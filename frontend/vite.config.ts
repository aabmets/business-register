import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import tsconfigPaths from 'vite-tsconfig-paths';
import graphql from '@rollup/plugin-graphql';


// https://vitejs.dev/config/
export default defineConfig({
	plugins: [react(), tsconfigPaths(), graphql()],
	build: {
		outDir: 'build'
	},
	server: {
		port: 8080,
		host: 'localhost',
		hmr: {
			host: 'localhost',
			clientPort: 80
		}
	}
})