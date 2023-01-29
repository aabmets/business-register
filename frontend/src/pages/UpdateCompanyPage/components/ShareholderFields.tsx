import { useState } from 'react';
import { Button, Space } from '@mantine/core';
import { Flex, ActionIcon } from '@mantine/core';
import { TextInput, NumberInput } from '@mantine/core';
import { TbCurrencyEuro, TbTrash } from 'react-icons/tb';
import { SearchCompaniesModal } from '@components';
import { getBlankShareholder } from '@utils';
import { useCompanyDetails } from '@context';
import { MantineForm } from "@types";
import styles from './ShareholderFields.module.css';


type FormProps = { form: MantineForm };

function ShareholderFields({ form }: FormProps): JSX.Element {
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
							placeholder='Osaniku nimi'
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
							placeholder='Isikukood'
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
							className={styles.equityInput}
							placeholder='Osakapital'
							maxLength={5}
							withAsterisk
							hideControls
							icon={<TbCurrencyEuro size={20} />}
							{...form.getInputProps(`shareholders.${index}.equity`)}
							sx={{'.mantine-NumberInput-error': {
								whiteSpace: 'nowrap',
								wordBreak: 'keep-all',
							}}}
						/>
						<div className={styles.actionIcon}>
							<ActionIcon
								disabled={inDatabase}
								onClick={() => form.removeListItem('shareholders', index)}
								variant='light'
								color='red'>
									<TbTrash size={18} />
							</ActionIcon>
						</div>
					</Flex>
				);
			})}
			<Flex gap='md'>
				<Button compact color='teal' type='button' onClick={addShareholder}>
					Lisa uus isik
				</Button>
				<Button compact color='cyan' type='button' onClick={openModal}>
					Otsi ettevõtteid
				</Button>
			</Flex>
			<Space h="sm"/>
		</div>
	);
}

export default ShareholderFields;