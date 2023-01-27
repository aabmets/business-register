import React from 'react';
import ReactDOM from 'react-dom/client';
import { MantineProvider } from '@mantine/core';
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';
import appConfig from '../appConfig';
import App from './App';
import './main.css';

const client = new ApolloClient({
	uri: appConfig.graphql.getUri(),
	cache: new InMemoryCache(),
});

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
	<React.StrictMode>
		<ApolloProvider client={client}>
			<MantineProvider withNormalizeCSS withGlobalStyles>
				<App />
			</MantineProvider>
		</ApolloProvider>
	</React.StrictMode>
);