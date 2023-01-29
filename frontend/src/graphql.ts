import { gql } from '@apollo/client';

export const SEARCH_COMPANIES = gql`
	query SearchCompanies($pattern: String!) {
		searchCompanies(pattern: $pattern) {
			result
			error
			data {
				name
				tin
			}
		}
	}
`;

export const GET_COMPANY_DETAILS = gql`
	query GetCompanyDetails($tin: String!) {
		getCompanyDetails(tin: $tin) {
			result
			error
			data {
				name
				tin
				equity
				founding_date
				shareholders {
					name
					tin
					equity
					founder
				}
			}
			
		}
	}
`;

export const CREATE_COMPANY = gql`
	mutation CreateCompany($data: CompanyDetailsInput!) {
		createCompany(data: $data) {
			result
			errors {
				field_id
				message
			}
			data {
				name
				tin
				equity
				founding_date
				shareholders {
					name
					tin
					equity
					founder
				}
			}
		}
	}
`

export const UPDATE_COMPANY = gql`
	mutation UpdateCompany($data: CompanyDetailsInput!) {
		updateCompany(data: $data) {
			result
			errors {
				field_id
				message
			}
			data {
				name
				tin
				equity
				founding_date
				shareholders {
					name
					tin
					equity
					founder
				}
			}
		}
	}
`