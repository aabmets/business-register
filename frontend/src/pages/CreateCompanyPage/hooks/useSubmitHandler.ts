import { useNavigate } from 'react-router-dom';
import { useMutation } from '@apollo/client';
import { useCompanyDetails } from '@context';
import { CREATE_COMPANY } from '@graphql';
import { 
	convertOutgoingData, 
	setShareholderErrors,
	setCompanyError,
	getUniqueErrors,
	showSpecialError,
	notifySuccess,
} from '@utils';
import { 
	CreateCompanyResponse, 
	MantineForm,
} from '@types';
import 'dayjs/locale/et';


type SubmitHandler = (form: MantineForm) => void;

export function useSubmitHandler(): SubmitHandler {
	const [createCompany] = useMutation<CreateCompanyResponse>(CREATE_COMPANY);
	const { setCompanyDetails } = useCompanyDetails();
	const navigate = useNavigate();

	function submitHandler(form: MantineForm): void {
		const dataOut = convertOutgoingData(form.values);
		createCompany({ variables: { data: dataOut }})
			.then((resp) => {
				const apiResult = resp.data?.createCompany.result;
				const apiErrors = resp.data?.createCompany.errors;
				const apiData = resp.data?.createCompany.data;
				if (apiResult && apiData) {
					setCompanyDetails(apiData);
					navigate(`/view?tin=${apiData.tin}`);
					notifySuccess('Uus ettevõte on asutatud.');
				} else if (!apiResult && apiErrors) {
					const uniqueErrors = getUniqueErrors(apiErrors);
					form.clearErrors();
					setCompanyError(form, uniqueErrors);
					setShareholderErrors(form, uniqueErrors);
					showSpecialError(uniqueErrors);
				}
			})
			.catch(() => null);
	}
	return submitHandler;
}