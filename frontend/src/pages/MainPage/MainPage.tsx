import { useRef } from 'react';
import { useLazyQuery } from '@apollo/client';
import { Text, Center, Stack } from '@mantine/core';
import { SearchResultCard, SearchInput } from '@components';
import { CompanyDetails } from '@types';
import { SEARCH_COMPANIES } from '@graphql';
import styles from './MainPage.module.css';

function MainPage(): JSX.Element {
	const inputRef = useRef<HTMLInputElement | null>(null);
	const [searchCompanies, { data }] = useLazyQuery(SEARCH_COMPANIES, 
		{ variables: { pattern: inputRef.current?.value || '' }}
	);
	const searchError: string | undefined = data?.searchCompanies.error
	const searchData: CompanyDetails[] | undefined = data?.searchCompanies.data
	
	return (
		<div style={{position: 'relative'}}>
			<Center className={styles.mainContent}>
				<Stack spacing={0}>
					<Center>
						<SearchInput 
							inputRef={inputRef} 
							callback={() => searchCompanies()}
						/>
					</Center>
					{searchData || searchError ?
						<Center>
							<Text className={styles.searchResultsText}>
								{searchData ?
									<span>{`Otsingu tulemused (${searchData.length})`}</span>
								: searchError ?
									<span>{searchError}</span>
								: null}
							</Text>
						</Center>
					: null}
					{searchData ?
						<Stack className={styles.searchResults}>
							{searchData.map((company) => 
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