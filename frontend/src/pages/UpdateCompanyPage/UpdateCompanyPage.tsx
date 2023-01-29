import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Center, Stack, Paper } from '@mantine/core';
import { useLazyQuery } from '@apollo/client';
import { Button, Text } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useCompanyDetails } from '@context';
import { GET_COMPANY_DETAILS } from '@graphql';
import { useSubmitHandler } from './hooks/useSubmitHandler';
import CompanyDetailFields from './components/CompanyDetailFields';
import ShareholderFields from './components/ShareholderFields';
import styles from './UpdateCompanyPage.module.css';
import { 
	CompanyDetailsInput, 
	CompanyDetails, 
	GetCompanyDetailsResponse,
} from '@types';
import { 
	getBlankCompany, 
	getInitCompany, 
	getInitShareholder,
} from '@utils';


function UpdateCompanyPage(): JSX.Element {
	const submitHandler = useSubmitHandler();
	const [searchParams] = useSearchParams();
	const { companyDetails, setCompanyDetails } = useCompanyDetails();
	const [errorMessage, setErrorMessage] = useState<string | null>(null);
	const [getCompanyDetails] = useLazyQuery<GetCompanyDetailsResponse>(
		GET_COMPANY_DETAILS, { variables: { tin: searchParams.get('tin') || '' }}
	);
	const form = useForm<CompanyDetailsInput>({
		initialValues: getBlankCompany(),
	})
	
	function updateFormData(company: CompanyDetails): void {
		form.setValues(getInitCompany(company));
		company.shareholders.forEach((item) => (
			form.insertListItem('shareholders', 
				getInitShareholder(item)
			)
		))
	}

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
						updateFormData(apiData);
					}
				})
				.catch(() => null);
		} else {
			updateFormData(companyDetails);
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
						<Text className={styles.updateCompanyTitle}>
							Osakapitali muutmine
						</Text>
						<Paper p='lg' radius='sm' withBorder className={styles.updateCompanyCard}>
							<CompanyDetailFields form={form}/>
							<Center className={styles.marginLine__1}>
								<Text className={styles.boldText}>
									Osanikud
								</Text>
							</Center>
							<ShareholderFields form={form}/>
							<Center className={styles.marginLine__2}>
								<Button color='red' onClick={() => submitHandler(form)}>
									Muuda osakapitali
								</Button>
							</Center>
						</Paper>
					</Stack>
				: null}
			</Center>
		</div>
	);
}

export default UpdateCompanyPage;