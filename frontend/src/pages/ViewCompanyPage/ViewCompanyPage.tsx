import { useEffect } from 'react';
import { useLazyQuery } from '@apollo/client';
import { useTranslation } from 'react-i18next';
import { useSearchParams } from 'react-router-dom';
import { Center, Text, Stack, Loader } from '@mantine/core';
import { useCompanyDetails } from '@context';
import { GET_COMPANY_DETAILS } from '@graphql';
import { GetCompanyDetailsResponse } from '@types';
import CompanyDetailsCard from './components/CompanyDetailsCard';
import styles from './ViewCompanyPage.module.css';


function ViewCompanyPage(): JSX.Element {
	const { t } = useTranslation('pages');
	const [searchParams] = useSearchParams();
	const { companyDetails, setCompanyDetails } = useCompanyDetails();
	const [getCompanyDetails, { loading, data }] = useLazyQuery<GetCompanyDetailsResponse>(
		GET_COMPANY_DETAILS, { variables: { tin: searchParams.get('tin') || '' }}
	);

	useEffect(() => {
		if (companyDetails === null) {
			getCompanyDetails()
				.then((resp) => {
					const gql = resp.data?.getCompanyDetails;
					if (gql?.result && gql?.data) {
						setCompanyDetails(gql.data);
					}
				})
				.catch(() => null);
		}
	}, [])

	return (
		<div style={{position: 'relative'}}>
			<Center className={styles.mainContent}>
				{(!companyDetails && !loading && !data) || loading ?
					<Loader color="green" size="xl" />
				: !companyDetails ?
					<Text className={styles.errorMsgStyle}> 
						{t("view.no-results")} 
					</Text>
				: 
					<Stack spacing={0}>
						<Text className={styles.viewCompanyTitle}>
							{t("view.title")}
						</Text>
						<CompanyDetailsCard detailsData={companyDetails}/>
					</Stack>
				}
			</Center>
		</div>
	);
}

export default ViewCompanyPage;