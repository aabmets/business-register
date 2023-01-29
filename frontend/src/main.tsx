import React from 'react';
import ReactDOM from 'react-dom/client';
import { MantineProvider } from '@mantine/core';
import { NotificationsProvider } from '@mantine/notifications';
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';
import App from './App';
import './main.css';

const client = new ApolloClient({
	uri: 'http://localhost:5678/graphql/',
	cache: new InMemoryCache(),
	connectToDevTools: false,
});

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
	<React.StrictMode>
		<ApolloProvider client={client}>
			<MantineProvider withNormalizeCSS withGlobalStyles>
				<NotificationsProvider position="bottom-center" zIndex={100}>
        			<App />
      			</NotificationsProvider>
			</MantineProvider>
		</ApolloProvider>
	</React.StrictMode>
);