import { MantineForm } from "@types";
import { DatePicker } from '@mantine/dates';
import { TextInput, NumberInput, Flex } from '@mantine/core';
import styles from './CompanyDetailFields.module.css';
import 'dayjs/locale/et';


type FormProps = { form: MantineForm };

function CompanyDetailFields({ form }: FormProps): JSX.Element {
	return (
		<Flex gap='md'>
			<TextInput
				disabled
				className={styles.nameInput}
				label='Ettevõtte nimi'
				{...form.getInputProps('name')}
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
				disabled
				className={styles.tinInput}
				label='Registrikood'
				maxLength={8}
				hideControls
				{...form.getInputProps('tin')}
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
				label='Osakapital'
				maxLength={5}
				withAsterisk
				hideControls
				icon='€'
				{...form.getInputProps('equity')}
				sx={{'.mantine-NumberInput-error': {
					whiteSpace: 'nowrap',
					wordBreak: 'keep-all',
				}}}
			/>
			<DatePicker 
				disabled
				className={styles.datePickerInput}
				label='Asutamise kuupäev' 
				dropdownType='modal'
				locale='et'
				maxDate={new Date()}
				inputFormat='D. MMMM YYYY'
				minDate={(() => {
					var date = new Date();
					date.setDate(date.getDate() - 30);
					return date
				})()}
				{...form.getInputProps('founding_date')}
				sx={{'.mantine-DatePicker-error': {
					whiteSpace: 'nowrap',
					wordBreak: 'keep-all',
				}, '.mantine-DatePicker-disabled': {
					'&:disabled': {
						color: 'black',
						opacity: 1,
					}
				}}}
			/>
		</Flex>
	);
}

export default CompanyDetailFields;