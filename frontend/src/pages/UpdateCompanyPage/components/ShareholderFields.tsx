import { useState } from 'react';
import { Button, Space } from '@mantine/core';
import { useTranslation } from 'react-i18next';
import { HiOutlineTrash } from 'react-icons/hi';
import { Flex, ActionIcon } from '@mantine/core';
import { TextInput, NumberInput } from '@mantine/core';
import { SearchCompaniesModal } from '@components';
import { getBlankShareholder } from '@utils';
import { useCompanyDetails } from '@context';
import { MantineForm } from "@types";
import styles from './ShareholderFields.module.css';


type FormProps = { form: MantineForm };

function ShareholderFields({ form }: FormProps): JSX.Element {
	const { t } = useTranslation('pages');
	const { companyDetails } = useCompanyDetails();
	const [mountKey, setMountKey] = useState(0);
	const [opened, setOpened] = useState(false);
	const openModal = () => setOpened(true);
	const closeModal = () => {
		setTimeout(() => (
			setMountKey(Math.random()
		), 500));
		setOpened(false);
	};

	function addShareholder() {
		const sh = getBlankShareholder();
		form.insertListItem('shareholders', sh);
	}

	return (
		<div className={styles.mainContent}>
			<SearchCompaniesModal 
				key={mountKey} 
				form={form} 
				opened={opened} 
				closeModal={closeModal}
			/>
			{form.values.shareholders.map((item, index) => {
				const db_shds = companyDetails?.shareholders || [];
				const inDatabase = index < db_shds.length;
				return (
					<Flex key={item.field_id} className={styles.inputFields}>
						<TextInput
							disabled={inDatabase}
							className={styles.nameInput}
							placeholder={t("update.sh-name") + ''}
							{...form.getInputProps(`shareholders.${index}.name`)}
							sx={{'.mantine-TextInput-error': {
								whiteSpace: 'nowrap',
								wordBreak: 'keep-all',
							}, '.mantine-TextInput-disabled': {
								'&:disabled': {
									color: 'black',
									opacity: 1,
								}
							}}}
						/>
						<NumberInput
							disabled={inDatabase}
							className={styles.tinInput}
							placeholder={t("update.sh-tin") + ''}
							maxLength={11}
							hideControls
							{...form.getInputProps(`shareholders.${index}.tin`)}
							sx={{'.mantine-NumberInput-error': {
								whiteSpace: 'nowrap',
								wordBreak: 'keep-all',
							}, '.mantine-NumberInput-disabled': {
								'&:disabled': {
									color: 'black',
									opacity: 1,
								}
							}}}
						/>
						<NumberInput
							className={styles.sharesInput}
							placeholder={t("update.sh-shares") + ''}
							maxLength={5}
							withAsterisk
							hideControls
							icon='€'
							{...form.getInputProps(`shareholders.${index}.equity`)}
						/>
						<div className={styles.actionIcon}>
							<ActionIcon
								disabled={inDatabase}
								onClick={() => form.removeListItem('shareholders', index)}
								variant='light'
								color='red'>
									<HiOutlineTrash size={18} />
							</ActionIcon>
						</div>
					</Flex>
				);
			})}
			<Flex gap='md'>
				<Button compact color='teal' type='button' onClick={addShareholder}>
					{t("update.add-new-person")}
				</Button>
				<Button compact color='cyan' type='button' onClick={openModal}>
					{t("update.search-companies")}
				</Button>
			</Flex>
			<Space h="sm"/>
		</div>
	);
}

export default ShareholderFields;