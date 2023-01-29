import { ApiError, AnyErrors, MantineForm } from "@types";
import { notifyError } from "./alertUtils";


export function getUniqueErrors(apiErrors: ApiError[]): AnyErrors {
	const uniqueErrors: AnyErrors = apiErrors.reduce((acc, error) => {
		if (!acc[error.field_id]) {
			acc[error.field_id] = error.message;
		}
		return acc;
	}, {} as AnyErrors);
	return uniqueErrors;
}

export function setCompanyError(form: MantineForm, errors: AnyErrors): void {
	const fid = form.values.field_id;
	if (errors.hasOwnProperty(fid)) {
		const message = errors[fid];
		let field = message.split('.')[0];
		field = (field === 'date' ? 'founding_date' : field);
		form.setFieldError(field, message);
	}
}

export function setShareholderErrors(form: MantineForm, errors: AnyErrors): void {
	form.values.shareholders.forEach((item, index) => {
		const message: string | undefined = errors[item.field_id];
		if (message) {
			let field = message.split('.')[0];
			form.setFieldError(`shareholders.${index}.${field}`, message);
		}
	});
}

export function showSpecialError(errors: AnyErrors): void {
	const keys = Object.keys(errors);
	for (const key of keys) {
		const message = errors[key];
		const field = message.split('.')[0];
		if (field === "shareholders") {
			notifyError(message);
			break;
		}
	}
}