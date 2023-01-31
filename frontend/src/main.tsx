import React from 'react';
import ReactDOM from 'react-dom/client';
import { MantineProvider } from '@mantine/core';
import { NotificationsProvider } from '@mantine/notifications';
import { ApolloClient, InMemoryCache, ApolloProvider } from '@apollo/client';
import { I18nextProvider } from 'react-i18next';
import App from './App';
import i18n from 'i18n';
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
					<I18nextProvider i18n={i18n}>
        				<App />
					</I18nextProvider>
      			</NotificationsProvider>
			</MantineProvider>
		</ApolloProvider>
	</React.StrictMode>
);