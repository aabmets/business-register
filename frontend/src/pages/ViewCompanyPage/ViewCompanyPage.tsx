import { useState, useEffect } from 'react';
import { Center, Text, Stack } from '@mantine/core';
import { useSearchParams } from 'react-router-dom';
import { useLazyQuery } from '@apollo/client';
import { useCompanyDetails } from '@context';
import { GET_COMPANY_DETAILS } from '@graphql';
import { GetCompanyDetailsResponse } from '@types';
import CompanyDetailsCard from './components/CompanyDetailsCard';
import styles from './ViewCompanyPage.module.css';


function ViewEntityPage(): JSX.Element {
	const [searchParams] = useSearchParams();
	const { companyDetails, setCompanyDetails } = useCompanyDetails();
	const [errorMessage, setErrorMessage] = useState<string | null>(null);
	const [getCompanyDetails] = useLazyQuery<GetCompanyDetailsResponse>(
		GET_COMPANY_DETAILS, { variables: { tin: searchParams.get('tin') || '' }}
	);

	useEffect(() => {
		if (companyDetails === null) {
			getCompanyDetails()
				.then((resp) => {
					const apiResult = resp.data?.getCompanyDetails.result;
					const apiError = resp.data?.getCompanyDetails.error;
					const apiData = resp.data?.getCompanyDetails.data;
					if (!apiResult && apiError) {
						setErrorMessage(apiError);
					} else if (apiResult && apiData) {
						setCompanyDetails(apiData);
					}
				})
				.catch(() => null);
		}
	}, [])
	
	return (
		<div style={{position: 'relative'}}>
			<Center className={styles.mainContent}>
				{errorMessage ? 
					<Text className={styles.errorMsgStyle}> 
						{errorMessage} 
					</Text>
				: null}
				{companyDetails ?
					<Stack spacing={0}>
						<Text className={styles.viewCompanyTitle}>
							Ettevõtte ülevaade
						</Text>
						<CompanyDetailsCard detailsData={companyDetails}/>
					</Stack>
				: null}
			</Center>
		</div>
	);
}

export default ViewEntityPage;