import { useNavigate } from 'react-router-dom';
import { useMutation } from '@apollo/client';
import { useCompanyDetails } from '@context';
import { UPDATE_COMPANY } from '@graphql';
import { 
	convertOutgoingData, 
	setShareholderErrors,
	setCompanyError,
	getUniqueErrors,
	showSpecialError,
	notifySuccess,
} from '@utils';
import { 
	UpdateCompanyResponse, 
	MantineForm,
} from '@types';
import 'dayjs/locale/et';


type SubmitHandler = (form: MantineForm) => void;

export function useSubmitHandler(): SubmitHandler {
	const [updateCompany] = useMutation<UpdateCompanyResponse>(UPDATE_COMPANY);
	const { setCompanyDetails } = useCompanyDetails();
	const navigate = useNavigate();

	function submitHandler(form: MantineForm): void {
		const dataOut = convertOutgoingData(form.values);
		updateCompany({ variables: { data: dataOut }})
			.then((resp) => {
				const apiResult = resp.data?.updateCompany.result;
				const apiErrors = resp.data?.updateCompany.errors;
				const apiData = resp.data?.updateCompany.data;
				if (apiResult && apiData) {
					setCompanyDetails(apiData);
					navigate(`/view?tin=${apiData.tin}`);
					notifySuccess('Ettevõtte osakapital on uuendatud.');
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