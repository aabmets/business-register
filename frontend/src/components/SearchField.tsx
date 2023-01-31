import { useTranslation } from 'react-i18next';
import { TextInput, Button } from "@mantine/core";
import { useStyles } from './SearchField.styles';
import { HiSearch } from 'react-icons/hi';


type InputRef = React.MutableRefObject<HTMLInputElement | null>
interface SearchInputProps {
	inputRef: InputRef;
	callback: () => void;
}

function SearchField(props: SearchInputProps): JSX.Element {
	const { t } = useTranslation('common');
	const { inputRef, callback } = props;
	const { classes } = useStyles();

	return (
		<div className={classes.searchFieldGroup}>
			<TextInput 
				className={classes.searchInput}
				onKeyDown={(e) => (e.key === 'Enter' ? callback() : null)}
				placeholder={t("search.placeholder") + ''}
				autoComplete="off"
				ref={inputRef}
			/>
			<Button className={classes.searchButton} onClick={callback}>
				<HiSearch size={30}/>
			</Button>
		</div>
	);

}

export default SearchField;