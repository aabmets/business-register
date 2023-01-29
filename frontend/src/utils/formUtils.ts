import { randomId } from '@mantine/hooks';
import { 
	Shareholder, 
	CompanyDetails, 
	ShareholderInput,
	CompanyDetailsInput,
} from '@types';


export function getBlankShareholder(): ShareholderInput {
	return { 
		name: '', 
		tin: null, 
		equity: null, 
		field_id: randomId(),
	}
}

export function getInitShareholder(item: Shareholder): ShareholderInput {
	return {
		name: item.name,
		tin: parseInt(item.tin),
		equity: item.equity,
		field_id: randomId(),
	}
}

export function getBlankCompany(): CompanyDetailsInput {
	return {
		name: '',
		tin: null,
		equity: null,
		founding_date: null,
		shareholders: [getBlankShareholder()],
		field_id: randomId(),
	}
}

export function getInitCompany(company: CompanyDetails): CompanyDetailsInput {
	return {
		name: company.name,
		tin: parseInt(company.tin),
		equity: company.equity,
		founding_date: new Date(company.founding_date),
		shareholders: [],
		field_id: randomId(),
	}
}