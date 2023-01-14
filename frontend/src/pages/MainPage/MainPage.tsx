import { gql, useQuery } from '@apollo/client';

function MainPage(): JSX.Element {
	const SEARCH_COMPANIES = gql`
		query searchCompanies($pattern: String!) {
			searchCompanies(pattern: $pattern) {
				companies {
					name
					tin
					equity
					foundingDate {
						year
						month
						day
					}
					shareholders {
						name
						tin
						equity
						founder
						personType
					}
				}
			}
		}
	`;
	const { loading, error, data } = useQuery(SEARCH_COMPANIES, {
		variables: { pattern: "my-search-string" },
	});
	console.log(loading, error, data);
	return (
		<div>
			Main Page
		</div>
	);
}

export default MainPage;