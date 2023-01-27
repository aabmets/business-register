import { Text, TextInput, Button } from "@mantine/core";
import { useStyles } from './SearchInput.styles';
import { HiSearch } from 'react-icons/hi';

type InputRef = React.MutableRefObject<HTMLInputElement | null>
interface SearchInputProps {
	inputRef: InputRef;
	callback: () => void;
}

function SearchInput(props: SearchInputProps): JSX.Element {
	const { inputRef, callback } = props;
	const { classes } = useStyles();

	return (
		<div>
			<Text className={classes.searchFieldTitle}>
				Juriidilise isiku otsing
			</Text>
			<div className={classes.searchFieldGroup}>
				<TextInput 
					autoComplete="off"
					placeholder="Nimi või registrikoodi number"
					className={classes.searchInput}
					ref={inputRef}
				/>
				<Button className={classes.searchButton} onClick={callback}>
					<HiSearch size={30}/>
				</Button>
			</div>
		</div>
	);

}

export default SearchInput;