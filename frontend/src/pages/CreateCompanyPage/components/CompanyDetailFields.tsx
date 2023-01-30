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
				className={styles.nameInput}
				placeholder='Ettevõtte nimi'
				label='Ettevõtte nimi'
				withAsterisk
				{...form.getInputProps('name')}
				sx={{'.mantine-TextInput-error': {
					whiteSpace: 'nowrap',
					wordBreak: 'keep-all',
				}}}
			/>
			<NumberInput
				className={styles.tinInput}
				placeholder='Registrikood'
				label='Registrikood'
				maxLength={8}
				withAsterisk
				hideControls
				{...form.getInputProps('tin')}
				sx={{'.mantine-NumberInput-error': {
					whiteSpace: 'nowrap',
					wordBreak: 'keep-all',
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
				className={styles.datePickerInput}
				dropdownType='modal'
				placeholder='Asutamise kuupäev' 
				label='Asutamise kuupäev' 
				locale='et'
				withAsterisk
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
				}}}
			/>
		</Flex>
	);
}

export default CompanyDetailFields;