import { useState, useRef } from 'react';
import { randomId } from '@mantine/hooks';
import { useLazyQuery } from '@apollo/client';
import { useTranslation } from 'react-i18next';
import { Button, Stack, Modal } from '@mantine/core';
import { Text, Center, ModalProps } from '@mantine/core';
import { MantineForm, CompanyOverview } from "@types";
import { SearchCompaniesResponse } from '@types';
import { useCompanyDetails } from '@context';
import { SEARCH_COMPANIES } from '@graphql';
import SearchField from './SearchField';
import styles from './SearchCompaniesModal.module.css';


interface SearchCompaniesModalProps {
	form: MantineForm;
	closeModal: () => void;
	opened: boolean;
}

function SearchCompaniesModal(props: SearchCompaniesModalProps): JSX.Element {
	const { t } = useTranslation('common');
	const { form, opened, closeModal } = props;
	const { companyDetails } = useCompanyDetails();
	const inputRef = useRef<HTMLInputElement | null>(null);
	const [searchCompanies] = useLazyQuery<SearchCompaniesResponse>(
		SEARCH_COMPANIES, { variables: { pattern: inputRef.current?.value || '' }}
	);
	const [data, setData] = useState<CompanyOverview[] | null | undefined>();
	const [error, setError] = useState<string | null | undefined>();

	function executeSearch() {
		searchCompanies()
			.then((resp) => {
				const gql = resp.data?.searchCompanies;
				let companies = null;
				if (gql?.result && gql?.data) {
					companies = gql.data.filter((entry) => (
						entry.tin !== companyDetails?.tin
					));
				}
				setError(gql?.error);
				setData(companies);
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
		setData((prevState) => {
			const index = data?.findIndex((item) => (item.name === name));
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
		title: t("search.modal-title"),
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
				minHeight: '45px',
			}
		},
	} satisfies ModalProps;

	return (
		<Modal {...modalProps}>
			<SearchField inputRef={inputRef} callback={executeSearch}/>
			{error ?
				<Center className={styles.resultsNotFound}>
					<Text className={styles.searchResultsText}>
						{t("search.modal-no-results")}
					</Text>
				</Center>
			: null}
			{data ?
				<Stack spacing={0}>
					<Center className={styles.resultsFound}>
						<Text className={styles.searchResultsText}>
							{`${t("search.modal-results")} (${data.length})`}
						</Text>
					</Center>
					<div className={styles.line}/>
					{data.map((company) => (
						<div key={company.name} className={styles.foundItem}>
							<Text className={styles.boldText}>
								{company.name}
							</Text>
							<Button 
								compact 
								color="cyan" 
								variant="light" 
								onClick={() => addShareholder(company.name, company.tin)}>
									{t("search.modal-add-sh")}
							</Button>
						</div>
					))}
				</Stack>
			: null}
		</Modal>
	);
}

export default SearchCompaniesModal;