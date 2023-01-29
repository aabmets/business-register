import { useState, useRef } from 'react';
import { randomId } from '@mantine/hooks';
import { useLazyQuery } from '@apollo/client';
import { Button, Stack, Modal } from '@mantine/core';
import { Text, Center, ModalProps } from '@mantine/core';
import { MantineForm, CompanyOverview } from "@types";
import { SearchCompaniesResponse } from '@types';
import { SEARCH_COMPANIES } from '@graphql';
import SearchField from './SearchField';
import styles from './SearchCompaniesModal.module.css';


interface SearchCompaniesModalProps {
	form: MantineForm;
	closeModal: () => void;
	opened: boolean;
}

function SearchCompaniesModal(props: SearchCompaniesModalProps): JSX.Element {
	const { form, opened, closeModal } = props;
	const inputRef = useRef<HTMLInputElement | null>(null);
	const [searchCompanies] = useLazyQuery<SearchCompaniesResponse>(SEARCH_COMPANIES, 
		{ variables: { pattern: inputRef.current?.value || '' }}
	);
	const [apiData, setApiData] = useState<CompanyOverview[] | null | undefined>();
	const [apiResult, setApiResult] = useState<boolean | null | undefined>();
	const [apiError, setApiError] = useState<string | null | undefined>();

	function executeSearch() {
		searchCompanies()
			.then((resp) => {
				const result = resp.data?.searchCompanies;
				if (result) {
					setApiData(result.data);
					setApiResult(result.result);
					setApiError(result.error);
				}
			})
			.catch(() => null);
	}

	function addShareholder(name: string, tin: string) {
		form.insertListItem('shareholders', {
			field_id: randomId(),
			tin: parseInt(tin), 
			equity: null, 
			name: name, 
		})
		setApiData((prevState) => {
			const index = apiData?.findIndex((item) => (item.name === name));
			if (prevState && index !== undefined) {
				const copy = [...prevState];
				copy.splice(index, 1);
				return copy.length === 0 ? null : copy;
			}
			return prevState;
		})
	}

	const modalProps = {
		transition: "fade",
		transitionDuration: 400,
		exitTransitionDuration: 400,
		transitionTimingFunction: "ease",
		title: "Ettevõtja osanikuks lisamine",
		onClose: closeModal,
		opened: opened,
		sx: {
			'.mantine-Modal-modal': {
				width: '30%',
				maxWidth: '800px',
				minWidth: '500px', 
				marginTop: '100px',
			},
			'.mantine-Modal-body': {
				paddingBottom: '10px',
			}
		},
	} satisfies ModalProps;

	return (
		<Modal {...modalProps}>
			<SearchField inputRef={inputRef} callback={executeSearch}/>
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
				<Stack spacing={0}>
					<div className={styles.line}/>
					{apiData.map((company) => (
						<div key={company.name} className={styles.foundItem}>
							<Text className={styles.boldText}>
								{company.name}
							</Text>
							<Button 
								compact 
								color="cyan" 
								variant="light" 
								onClick={() => addShareholder(company.name, company.tin)}>
									Lisa osanikuks
							</Button>
						</div>
					))}
				</Stack>
			: null}
		</Modal>
	);
}

export default SearchCompaniesModal;