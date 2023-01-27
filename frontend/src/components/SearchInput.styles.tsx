import { createStyles } from '@mantine/core';


export const useStyles = createStyles(() => ({
	searchFieldTitle: {
		color: 'white',
		fontSize: '2.0rem',
		fontWeight: 600,
		marginBottom: '22px',
		textShadow: '0 0.2rem 0.4rem rgba(0, 0, 0, 50%)',
	},
	searchFieldGroup: {
		display: 'flex', 
		justifyContent: 'center', 
		paddingBottom: '20px',
		width: '50vw',
		minWidth: '330px',
	},
	searchInput: {
		width: '100%',
		'.mantine-Input-input': {
			paddingLeft: '20px',
			paddingBottom: '5px',
			fontSize: '1.1rem',
			color: '#6E7275',
		},
		'.mantine-TextInput-input': {
			height: '40px',
			borderRadius: 100,
			borderTopRightRadius: 0,
			borderBottomRightRadius: 0,
			'&:focus': {
				borderWidth: '3px',
				borderColor: '#FDC108',
			},
			"&::placeholder": {
				fontSize: '1.1rem',
				color: '#6E7275',
			},
		},
	},
	searchButton: {
		display: 'block',
		height: '40px',
		borderRadius: 100,
		borderTopLeftRadius: 0,
		borderBottomLeftRadius: 0,
		'&:hover': {
			backgroundColor: '#004277',
		},
	}
}));