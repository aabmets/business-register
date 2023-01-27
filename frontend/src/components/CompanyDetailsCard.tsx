import styles from './CompanyDetailsCard.module.css';
import { Text, Card, Flex } from '@mantine/core';
import { CompanyDetails } from '@types';
import dayjs from 'dayjs';

interface CompanyDetailsCardProps {
	detailsData: CompanyDetails;
}

function CompanyDetailsCard(props: CompanyDetailsCardProps): JSX.Element {
	const { name, tin, equity, founding_date, shareholders } = props.detailsData;
	const f_date = dayjs(founding_date).format('DD.MM.YYYY');

	return (
		<Card p="lg" radius="sm" withBorder className={styles.companyDetailsCard}>
			<Flex justify="flex-start" align="center" className={styles.companyDetails}>
				<div className={styles.regularText}>
					<Text>Ettevõtte nimi</Text>
					<Text>Registrikood</Text>
					<Text>Kogukapital</Text>
					<Text>Asutamise kuupäev</Text>
				</div>
				<div className={styles.boldText}>
					<Text>{name}</Text>
					<Text>{tin}</Text>
					<Text>{`${equity} €`}</Text>
					<Text>{f_date}</Text>
				</div>
			</Flex>
			<Flex className={styles.regularText}>
				<Text className={styles.shPct}>Osalus</Text>
				<span className={styles.space}/>
				<Text className={styles.shEquity}>Osamaks</Text>
				<Text className={styles.shName}>Nimi</Text>
				<Text className={styles.shTin}>Isikukood</Text>
				<Text className={styles.shFounder}>Asutaja</Text>
				<Text className={styles.shType}>Tüüp</Text>
			</Flex>
			<div className={styles.line}/>
			<Flex direction='row'>
				<Flex direction='column' className={styles.shPct}>
					{shareholders.map((sh, index) => 
						<Text key={'pct-' + index} className={styles.regularText}>
							{`${(sh.equity / equity * 100).toFixed(2)}%`}
						</Text>
					)}
				</Flex>
				<Flex direction='column' className={styles.space}/>
				<Flex direction='column' className={styles.shEquity}>
					{shareholders.map((sh, index) => 
						<Text key={'equity-' + index} className={styles.regularText}>
							{`${sh.equity} EUR`}
						</Text>
					)}
				</Flex>
				<Flex direction='column' className={styles.shName}>
					{shareholders.map((sh, index) => 
						<Text key={'name-' + index} className={styles.boldText}>
							{sh.name}
						</Text>
					)}
				</Flex>
				<Flex direction='column' className={styles.shTin}>
					{shareholders.map((sh, index) => 
						<Text key={'tin-' + index} className={styles.regularText}>
							{sh.tin}
						</Text>
					)}
				</Flex>
				<Flex direction='column' className={styles.shFounder}>
					{shareholders.map((sh, index) => 
						<Text key={'founder-' + index} className={styles.regularText}>
							{sh.founder ? 'Jah' : 'Ei'}
						</Text>
					)}
				</Flex>
				<Flex direction='column' className={styles.shType}>
					{shareholders.map((sh, index) => 
						<Text key={'type-' + index} className={styles.regularText}>
							{sh.tin.length == 11 ? 'Eraisik' : 'Ettevõte'}
						</Text>
					)}
				</Flex>
			</Flex>
		</Card>
	);
}

export default CompanyDetailsCard;