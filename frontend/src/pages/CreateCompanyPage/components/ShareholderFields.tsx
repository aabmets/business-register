import { useState } from 'react';
import { MantineForm } from "@types";
import { getBlankShareholder } from '@utils';
import { SearchCompaniesModal } from '@components';
import { Button, ActionIcon, Space } from '@mantine/core';
import { TextInput, NumberInput, Flex } from '@mantine/core';
import { HiOutlineTrash } from 'react-icons/hi';
import styles from './ShareholderFields.module.css';


type FormProps = { form: MantineForm };

function ShareholderFields({ form }: FormProps): JSX.Element {
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
	function clearShareholders() {
		const sh = getBlankShareholder();
		form.setFieldValue('shareholders', [sh]);
	}

	const shareholders = form.values.shareholders;
	const isSingle = shareholders.length === 1;
	
	return (
		<div className={styles.mainContent}>
			<SearchCompaniesModal 
				key={mountKey} 
				form={form} 
				opened={opened} 
				closeModal={closeModal}
			/>
			{shareholders.map((item, index) => (
				<Flex key={item.field_id} className={styles.inputFields}>
					<TextInput
						className={styles.nameInput}
						placeholder='Osaniku nimi'
						{...form.getInputProps(`shareholders.${index}.name`)}
						sx={{'.mantine-TextInput-error': {
							whiteSpace: 'nowrap',
							wordBreak: 'keep-all',
						}}}
					/>
					<NumberInput
						className={styles.tinInput}
						placeholder='Isikukood'
						maxLength={11}
						hideControls
						{...form.getInputProps(`shareholders.${index}.tin`)}
						sx={{'.mantine-NumberInput-error': {
							whiteSpace: 'nowrap',
							wordBreak: 'keep-all',
						}}}
					/>
					<NumberInput
						className={styles.equityInput}
						placeholder='Osakapital'
						maxLength={5}
						withAsterisk
						hideControls
						icon='€'
						{...form.getInputProps(`shareholders.${index}.equity`)}
						sx={{'.mantine-NumberInput-error': {
							whiteSpace: 'nowrap',
							wordBreak: 'keep-all',
						}}}
					/>
					<div className={styles.actionIcon}>
						<ActionIcon
							onClick={() => form.removeListItem('shareholders', index)}
							disabled={isSingle && index === 0}
							variant='light'
							color='red'>
								<HiOutlineTrash size={18} />
						</ActionIcon>
					</div>
				</Flex>
			))}
			<Flex gap='md'>
				<Button compact color='teal' type='button' onClick={addShareholder}>
					Lisa uus isik
				</Button>
				<Button compact color='yellow' type='button' onClick={clearShareholders} disabled={isSingle}>
					Eemalda kõik
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