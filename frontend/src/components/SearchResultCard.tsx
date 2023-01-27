import { useNavigate } from "react-router-dom";
import { Card, Text, Flex } from '@mantine/core';
import styles from './SearchResultCard.module.css';

interface SearchResultCardProps {
	name: string;
	tin: string;
}

function SearchResultCard(props: SearchResultCardProps): JSX.Element {
	const { name, tin } = props;
	const navigate = useNavigate();
	
	return (
		<Card p="lg" radius="sm" withBorder className={styles.card}>
			<Text 
				className={styles.companyName} 
				onClick={() => navigate(`/view?tin=${tin}`)}>
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