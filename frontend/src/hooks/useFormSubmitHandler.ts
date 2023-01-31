import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@apollo/client';
import { useCompanyDetails } from '@context';
import { useNotifications } from '@hooks';
import { Mutation } from '@types';
import 'dayjs/locale/et';
import { 
	CREATE_COMPANY, 
	UPDATE_COMPANY 
} from '@graphql';
import { 
	convertOutgoingData, 
	setShareholderErrors,
	setCompanyError,
	getSpecialError,
} from '@utils';
import { 
	MutateCompanyResponse, 
	MantineForm,
} from '@types';


type SubmitHandler = (form: MantineForm) => void;

export function useFormSubmitHandler(mutation: Mutation): SubmitHandler {
	const query = (mutation === Mutation.CREATE ? CREATE_COMPANY : UPDATE_COMPANY);
	const [mutate] = useMutation<MutateCompanyResponse>(query);
	const { notifySuccess, notifyFailure } = useNotifications();
	const { t } = useTranslation(['pages', 'errors']);
	const { setCompanyDetails } = useCompanyDetails();
	const navigate = useNavigate();

	function submitHandler(form: MantineForm): void {
		const dataOut = convertOutgoingData(form.values);
		mutate({ variables: { data: dataOut }})
			.then((resp) => {
				if (resp.data) {
					const gql = resp.data[`${mutation}Company`];
					if (gql) {
						const { result, data, errors } = gql;
						if (result && data) {
							setCompanyDetails(data);
							navigate(`/view?tin=${data.tin}`);
							notifySuccess(t(`${mutation}.success`));
						} else if (!result && errors) {
							form.clearErrors();
							setCompanyError(form, errors, t);
							setShareholderErrors(form, errors, t);
							const message = getSpecialError(errors);
							if (message) {
								notifyFailure(t(message, { ns: 'errors' }));
							}
						}
					}
				}
			})
			.catch(() => null);
	}
	return submitHandler;
}