import { UseFormReturnType } from '@mantine/form';


// ------------------------------------------------------ //
interface Shareholder {
	name: string;
	tin: string;
	equity: number;
	founder: boolean;
}
interface CompanyDetails {
	name: string;
	tin: string;
	equity: number;
	founding_date: string;
	shareholders: Shareholder[];
}
interface CompanyOverview {
	name: string;
	tin: string;
}
export type { Shareholder }
export type { CompanyDetails }
export type { CompanyOverview }


// ------------------------------------------------------ //
interface ShareholderInput {
	name: string;
	tin: number | null;
	equity: number | null;
	field_id: string;
}
interface CompanyDetailsInput {
    name: string;
    tin: number | null;
    equity: number | null;
    founding_date: Date | null;
    shareholders: ShareholderInput[];
    field_id: string;
}
export type { ShareholderInput }
export type { CompanyDetailsInput }


// ------------------------------------------------------ //
interface OutgoingShareholder {
	name?: string;
	tin?: string;
	equity?: number;
	field_id: string;
}
interface OutgoingCompanyDetails {
	name?: string;
	tin?: string;
	equity?: number;
	founding_date?: string;
	shareholders?: OutgoingShareholder[];
	field_id:string;
}
export type { OutgoingShareholder }
export type { OutgoingCompanyDetails }


// ------------------------------------------------------ //
interface ApiError {
	field_id: string;
	message: string;
}
interface CreateCompanyResponse {
	createCompany: {
		data: CompanyDetails | null;
		result: boolean;
		errors: ApiError[] | null;
	}
}
interface UpdateCompanyResponse {
	updateCompany: {
		data: CompanyDetails | null;
		result: boolean;
		errors: ApiError[] | null;
	}
}
interface SearchCompaniesResponse {
	searchCompanies: {
		error: string | null;
		result: boolean;
		data: CompanyOverview[] | null
	}
}
interface GetCompanyDetailsResponse {
	getCompanyDetails: {
		error: string;
		result: boolean;
		data: CompanyDetails;
	}
}
export type { ApiError };
export type { CreateCompanyResponse };
export type { UpdateCompanyResponse };
export type { SearchCompaniesResponse };
export type { GetCompanyDetailsResponse };


// ------------------------------------------------------ //
type FormFunction = (values: CompanyDetailsInput) => CompanyDetailsInput;
type MantineForm = UseFormReturnType<CompanyDetailsInput, FormFunction>;

export type { FormFunction };
export type { MantineForm };


// ------------------------------------------------------ //
type AnyErrors = {[key: string]: string};
export type { AnyErrors };