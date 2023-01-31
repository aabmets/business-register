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
				disabled
				className={styles.nameInput}
				label={t("update.cp-name")}
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
				label={t("update.cp-reg-tin")}
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
				placeholder={t("update.cp-equity") + ''}
				label={t("update.cp-equity")}
				maxLength={5}
				withAsterisk
				hideControls
				icon='€'
				{...form.getInputProps('equity')}
			/>
			<DatePicker 
				disabled
				className={styles.datePickerInput}
				label={t("update.cp-founding-date")}
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