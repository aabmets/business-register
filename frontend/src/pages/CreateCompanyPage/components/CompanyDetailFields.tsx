import { MantineForm } from "@types";
import { DatePicker } from '@mantine/dates';
import { useTranslation } from 'react-i18next';
import { TextInput, NumberInput, Flex } from '@mantine/core';
import styles from './CompanyDetailFields.module.css';
import 'dayjs/locale/et';


type FormProps = { form: MantineForm };

function CompanyDetailFields({ form }: FormProps): JSX.Element {
	const { t } = useTranslation('pages');
	return (
		<Flex gap='md'>
			<TextInput
				className={styles.nameInput}
				placeholder={t('create.cp-name') + ''}
				label={t('create.cp-name')}
				withAsterisk
				{...form.getInputProps('name')}
			/>
			<NumberInput
				className={styles.tinInput}
				placeholder={t('create.cp-reg-tin') + ''}
				label={t('create.cp-reg-tin')}
				maxLength={8}
				withAsterisk
				hideControls
				{...form.getInputProps('tin')}
			/>
			<NumberInput
				className={styles.equityInput}
				placeholder={t('create.cp-equity') + ''}
				label={t('create.cp-equity')}
				maxLength={5}
				withAsterisk
				hideControls
				icon='€'
				{...form.getInputProps('equity')}
			/>
			<DatePicker 
				className={styles.datePickerInput}
				dropdownType='modal'
				placeholder={t('create.cp-founding-date') + ''}
				label={t('create.cp-founding-date')}
				inputFormat='D. MMMM YYYY'
				locale='et'
				withAsterisk
				maxDate={new Date()}
				minDate={(() => {
					var date = new Date();
					date.setDate(date.getDate() - 30);
					return date
				})()}
				{...form.getInputProps('founding_date')}
			/>
		</Flex>
	);
}

export default CompanyDetailFields;