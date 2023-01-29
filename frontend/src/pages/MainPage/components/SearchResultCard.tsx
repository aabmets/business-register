import { useCompanyDetails } from '@context';
import { useNavigate } from "react-router-dom";
import { Card, Text, Flex } from '@mantine/core';
import styles from './SearchResultCard.module.css';


interface SearchResultCardProps {
	name: string;
	tin: string;
}

function SearchResultCard({ name, tin }: SearchResultCardProps): JSX.Element {
	const { companyDetails, setCompanyDetails } = useCompanyDetails();
	const navigate = useNavigate();

	function onClickHandler() {
		if (companyDetails?.tin !== tin) {
			setCompanyDetails(null);
		}
		navigate(`/view?tin=${tin}`);
	}
	
	return (
		<Card p="lg" radius="sm" withBorder className={styles.card}>
			<Text className={styles.companyName} onClick={onClickHandler}>
				{name}
			</Text>
			<Flex justify="flex-start" align="center" direction="row">
				<div className={styles.companyTin}>
					Registrikood
				</div>
				<div className={styles.tinCode}>
					{tin}
				</div>
			</Flex>
		</Card>
	);
}

export default SearchResultCard;