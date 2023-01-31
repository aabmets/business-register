import { CompanyDetails } from '@types';
import { useTranslation } from 'react-i18next';
import { Text, Card, Flex } from '@mantine/core';
import styles from './CompanyDetailsCard.module.css';
import dayjs from 'dayjs';


interface CompanyDetailsCardProps {
	detailsData: CompanyDetails;
}

function CompanyDetailsCard(props: CompanyDetailsCardProps): JSX.Element {
	const { name, tin, equity, founding_date, shareholders } = props.detailsData;
	const f_date = dayjs(founding_date).format('DD.MM.YYYY');
	const { t } = useTranslation('pages');

	return (
		<Card p="lg" radius="sm" withBorder className={styles.companyDetailsCard}>
			<Flex justify="flex-start" align="center" className={styles.companyDetails}>
				<div className={styles.regularText}>
					<Text>{t("view.cp-name")}</Text>
					<Text>{t("view.cp-reg-tin")}</Text>
					<Text>{t("view.cp-equity")}</Text>
					<Text>{t("view.cp-founding-date")}</Text>
				</div>
				<div className={styles.boldText}>
					<Text>{name}</Text>
					<Text>{tin}</Text>
					<Text>{`${equity} €`}</Text>
					<Text>{f_date}</Text>
				</div>
			</Flex>

			<Flex className={styles.regularText}>
				<Text className={styles.shPct}>{t("view.sh-pct")}</Text>
				<Text className={styles.shShares}>{t("view.sh-shares")}</Text>
				<Text className={styles.shName}>{t("view.sh-name")}</Text>
				<Text className={styles.shTin}>{t("view.sh-tin")}</Text>
				<Text className={styles.shFounder}>{t("view.sh-founder")}</Text>
				<Text className={styles.shType}>{t("view.sh-type")}</Text>
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
				<Flex direction='column' className={styles.shShares}>
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
							{sh.founder ? t("view.true") : t("view.false")}
						</Text>
					)}
				</Flex>
				<Flex direction='column' className={styles.shType}>
					{shareholders.map((sh, index) => 
						<Text key={'type-' + index} className={styles.regularText}>
							{sh.tin.length == 11 ? t("view.natural") : t("view.judicial")}
						</Text>
					)}
				</Flex>
			</Flex>
		</Card>
	);
}

export default CompanyDetailsCard;