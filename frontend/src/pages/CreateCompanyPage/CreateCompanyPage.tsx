import { useTranslation } from 'react-i18next';
import { Button, Text} from '@mantine/core';
import { useForm } from '@mantine/form';
import { getBlankCompany } from '@utils';
import { useFormSubmitHandler } from '@hooks';
import { Center, Stack, Paper } from '@mantine/core';
import { CompanyDetailsInput, Mutation } from '@types';
import CompanyDetailFields from './components/CompanyDetailFields';
import ShareholderFields from './components/ShareholderFields';
import styles from './CreateCompanyPage.module.css';


function CreateCompanyPage(): JSX.Element {
	const { t } = useTranslation('pages');
	const submitHandler = useFormSubmitHandler(Mutation.CREATE);
	const form = useForm<CompanyDetailsInput>({
		initialValues: getBlankCompany(),
	})

	return (
		<div style={{position: 'relative'}}>
			<Center className={styles.mainContent}>
				<Stack spacing={0}>
					<Text className={styles.createCompanyTitle}>
						{t("create.title")}
					</Text>
					<Paper p='lg' radius='sm' withBorder className={styles.createCompanyCard}>
						<CompanyDetailFields form={form}/>
						<Center className={styles.marginLine__1}>
							<Text className={styles.boldText}>
								{t("create.shareholders")}
							</Text>
						</Center>
						<ShareholderFields form={form}/>
						<Center className={styles.marginLine__2}>
							<Button color='red' onClick={() => submitHandler(form)}>
								{t("create.company")}
							</Button>
						</Center>
					</Paper>
				</Stack>
			</Center>
		</div>
	);
}

export default CreateCompanyPage;