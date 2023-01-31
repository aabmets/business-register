import { ErrorResponse, AnyErrors, MantineForm } from "@types";
import { TFunction } from "i18next";


type Translator = TFunction<any[], any, any[]>;

export function getUniqueErrors(apiErrors: ErrorResponse[]): AnyErrors {
	const uniqueErrors: AnyErrors = apiErrors.reduce((acc, error) => {
		if (!acc[error.field_id]) {
			acc[error.field_id] = error.message;
		}
		return acc;
	}, {} as AnyErrors);
	return uniqueErrors;
}

export function getSpecialError(errors: ErrorResponse[]): string | undefined {
	const uniqueErrors = getUniqueErrors(errors);
	const keys = Object.keys(uniqueErrors);
	for (const key of keys) {
		const message = uniqueErrors[key];
		const field = message.split('.')[0];
		if (field === "shareholders") {
			return message;
		}
	}
}

export function setCompanyError(form: MantineForm, errors: ErrorResponse[], t: Translator): void {
	const uniqueErrors = getUniqueErrors(errors);
	const fid = form.values.field_id;
	if (Object.hasOwn(uniqueErrors, fid)) {
		const message = uniqueErrors[fid];
		let field = message.split('.')[0];
		field = (field === 'date' ? 'founding_date' : field);
		form.setFieldError(field, t(message, { ns: 'errors' }));
	}
}

export function setShareholderErrors(form: MantineForm, errors: ErrorResponse[], t: Translator): void {
	const uniqueErrors = getUniqueErrors(errors);
	form.values.shareholders.forEach((item, index) => {
		const message: string | undefined = uniqueErrors[item.field_id];
		if (message) {
			let field = message.split('.')[0];
			field = `shareholders.${index}.${field}`;
			form.setFieldError(field, t(message, { ns: 'errors' }));
		}
	});
}