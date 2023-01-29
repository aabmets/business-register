import { useRef } from 'react';
import { SearchField } from '@components';
import { SEARCH_COMPANIES } from '@graphql';
import { SearchCompaniesResponse } from '@types';
import { Text, Center, Stack } from '@mantine/core';
import { useLazyQuery } from '@apollo/client';
import SearchResultCard from './components/SearchResultCard';
import styles from './MainPage.module.css';


function MainPage(): JSX.Element {
	const inputRef = useRef<HTMLInputElement | null>(null);
	const [searchCompanies, { data }] = useLazyQuery<SearchCompaniesResponse>(SEARCH_COMPANIES, 
		{ variables: { pattern: inputRef.current?.value || '' }}
	);
	const apiResult = data?.searchCompanies.result;
	const apiError = data?.searchCompanies.error;
	const apiData = data?.searchCompanies.data;
	
	return (
		<div style={{position: 'relative'}}>
			<Center className={styles.mainContent}>
				<Stack spacing={0}>
					<Center>
						<div style={{width: '50vw'}}>
							<Text className={styles.searchFieldTitle}>
								Juriidilise isiku otsing
							</Text>
							<SearchField inputRef={inputRef} callback={searchCompanies}/>
						</div>
					</Center>
					{apiData || apiError ?
						<Center>
							<Text className={styles.searchResultsText}>
								{apiData ?
									<span>{`Otsingu tulemused (${apiData.length})`}</span>
								: apiError ?
									<span>{apiError}</span>
								: null}
							</Text>
						</Center>
					: null}
					{apiResult && apiData ?
						<Stack className={styles.searchResults}>
							{apiData.map((company) => 
								<SearchResultCard 
									key={Math.random()}
									name={company.name} 
									tin={company.tin} 
								/>
							)}
						</Stack>
					: null}
				</Stack>
			</Center>
		</div>
	);
}

export default MainPage;