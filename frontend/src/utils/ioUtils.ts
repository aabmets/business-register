import { 
	ShareholderInput, 
	CompanyDetailsInput, 
	OutgoingShareholder, 
	OutgoingCompanyDetails,
} from '@types';


export function convertOutgoingData(company: CompanyDetailsInput): OutgoingCompanyDetails {
	const name = company.name;
	const tin = company.tin;
	const eq = company.equity;
	const fd = company.founding_date;
	const cmpOut: OutgoingCompanyDetails = { 
		field_id: company.field_id 
	};
	if (name.length > 0) {
		Object.assign(cmpOut, { name })
	}
	if (typeof tin === 'number' && isFinite(tin)) {
		Object.assign(cmpOut, { tin: tin.toString() })
	}
	if (typeof eq === 'number' && isFinite(eq)) {
		Object.assign(cmpOut, { equity: eq })
	}
	if (fd instanceof Date) {
		const isoDate = fd.toISOString().split('T')[0]
		Object.assign(cmpOut, { founding_date: isoDate })
	}

	const shdsOut: OutgoingShareholder[] = [];
	company.shareholders.forEach((shareholder: ShareholderInput) => {
		const name = shareholder.name;
		const tin = shareholder.tin;
		const eq = shareholder.equity;
		const shOut: OutgoingShareholder = { 
			field_id: shareholder.field_id 
		};
		if (name.length > 0) {
			Object.assign(shOut, { name })
		}
		if (typeof tin === 'number' && isFinite(tin)) {
			Object.assign(shOut, { tin: tin.toString() })
		}
		if (typeof eq === 'number' && isFinite(eq)) {
			Object.assign(shOut, { equity: eq })
		}
		shdsOut.push(shOut);
	})

	Object.assign(cmpOut, { shareholders: shdsOut });
	return cmpOut;
}