import { initReactI18next } from 'react-i18next';
import Backend from 'i18next-http-backend';
import i18n from 'i18next';

i18n
	.use(Backend)
	.use(initReactI18next)
	.init({
		lng: 'et',
		fallbackLng: 'et',
		ns: ['common', 'pages', 'errors'],
		defaultNS: 'common',
		interpolation: {
			escapeValue: false,
		},
		keySeparator: '.'
	});

export default i18n;