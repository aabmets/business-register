import { useForm } from '@mantine/form';
import { getBlankCompany } from '@utils';
import { Button,  Text} from '@mantine/core';
import { CompanyDetailsInput } from '@types';
import { Center, Stack, Paper } from '@mantine/core';
import { useSubmitHandler } from './hooks/useSubmitHandler';
import CompanyDetailFields from './components/CompanyDetailFields';
import ShareholderFields from './components/ShareholderFields';
import styles from './CreateCompanyPage.module.css';


function CreateCompanyPage(): JSX.Element {
	const submitHandler = useSubmitHandler();
	const form = useForm<CompanyDetailsInput>({
		initialValues: getBlankCompany(),
	})

	return (
		<div style={{position: 'relative'}}>
			<Center className={styles.mainContent}>
				<Stack spacing={0}>
					<Text className={styles.createCompanyTitle}>
						Ettevõtte asutamine
					</Text>
					<Paper p='lg' radius='sm' withBorder className={styles.createCompanyCard}>
						<CompanyDetailFields form={form}/>
						<Center className={styles.marginLine__1}>
							<Text className={styles.boldText}>
								Osanikud
							</Text>
						</Center>
						<ShareholderFields form={form}/>
						<Center className={styles.marginLine__2}>
							<Button color='red' onClick={() => submitHandler(form)}>
								Asuta ettevõte
							</Button>
						</Center>
					</Paper>
				</Stack>
			</Center>
		</div>
	);
}

export default CreateCompanyPage;