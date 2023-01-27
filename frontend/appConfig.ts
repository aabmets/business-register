// main app configuration

const appConfig = {
	graphql: {
		host: 'localhost',
		port: 8000,
		
		getUri() {
			const { host, port } = appConfig.graphql;
			return `http://${host}:${port}/graphql/`
		}
	}
}

export default appConfig;