import { Fragment } from 'react';
import { Center } from '@mantine/core';
import { useQuery } from '@apollo/client';
import { useSearchParams } from 'react-router-dom';
import { CompanyDetailsCard } from '@components';
import { GET_COMPANY_DETAILS } from '@graphql';
import { CompanyDetails } from '@types';
import styles from './ViewCompanyPage.module.css';

function ViewEntityPage(): JSX.Element {
	const [searchParams] = useSearchParams();
	const { data } = useQuery(GET_COMPANY_DETAILS, 
		{ variables: { tin: searchParams.get('tin') || '' }}
	);
	const detailsResult: string | undefined = data?.getCompanyDetails.result
	const detailsData: CompanyDetails | undefined = data?.getCompanyDetails.data
	
	return (
		<Fragment>
			{detailsResult && detailsData ? 
				<div style={{position: 'relative'}}>
					<Center className={styles.mainContent}>
						<CompanyDetailsCard detailsData={detailsData}/>
					</Center>
				</div>
			: null}
		</Fragment>
	);
}

export default ViewEntityPage;