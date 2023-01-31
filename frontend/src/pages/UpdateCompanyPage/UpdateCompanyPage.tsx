import { useEffect } from 'react';
import { useForm } from '@mantine/form';
import { Button, Text, Paper } from '@mantine/core';
import { Center, Stack, Loader } from '@mantine/core';
import { useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useLazyQuery } from '@apollo/client';
import { useCompanyDetails } from '@context';
import { useFormSubmitHandler } from '@hooks';
import { GET_COMPANY_DETAILS } from '@graphql';
import CompanyDetailFields from './components/CompanyDetailFields';
import ShareholderFields from './components/ShareholderFields';
import styles from './UpdateCompanyPage.module.css';
import { 
	GetCompanyDetailsResponse,
	CompanyDetailsInput, 
	CompanyDetails, 
	Mutation,
} from '@types';
import { 
	getInitShareholder,
	getBlankCompany, 
	getInitCompany, 
} from '@utils';


function UpdateCompanyPage(): JSX.Element {
	const { t } = useTranslation('pages');
	const [searchParams] = useSearchParams();
	const submitHandler = useFormSubmitHandler(Mutation.UPDATE);
	const { companyDetails, setCompanyDetails } = useCompanyDetails();
	const [getCompanyDetails, { loading, data }] = useLazyQuery<GetCompanyDetailsResponse>(
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
					const gql = resp.data?.getCompanyDetails;
					if (gql?.result && gql?.data) {
						setCompanyDetails(gql.data);
						updateFormData(gql.data);
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
				{(!companyDetails && !loading && !data) || loading ?
					<Loader color="green" size="xl" />
				: !companyDetails ?
					<Text className={styles.errorMsgStyle}> 
						{t("update.no-results")} 
					</Text>
				: 
					<Stack spacing={0}>
						<Text className={styles.updateCompanyTitle}>
							{t("update.title")}
						</Text>
						<Paper p='lg' radius='sm' withBorder className={styles.updateCompanyCard}>
							<CompanyDetailFields form={form}/>
							<Center className={styles.marginLine__1}>
								<Text className={styles.boldText}>
									{t("update.shareholders")}
								</Text>
							</Center>
							<ShareholderFields form={form}/>
							<Center className={styles.marginLine__2}>
								<Button color='red' onClick={() => submitHandler(form)}>
									{t("update.change-equity")}
								</Button>
							</Center>
						</Paper>
					</Stack>
				}
			</Center>
		</div>
	);
}

export default UpdateCompanyPage;