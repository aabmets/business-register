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