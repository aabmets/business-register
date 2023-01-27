
function UpdateEntityPage(): JSX.Element {
		// const { loading, error, data } = useQuery(SEARCH_COMPANIES, {
	// 	variables: { tin: "13461441" },
	// });
	// if (error) {
	// 	console.log(error.message)
	// } else {
	// 	console.log(loading, data);
	// }
	// const UPDATE_COMPANY = gql`
	// 	mutation UpdateCompany($data: CompanyDetailsInput!) {
	// 		updateCompany(data: $data) {
	// 			result
	// 			errors {
	// 				field_id
	// 				message
	// 			}
	// 			data {
	// 				name
	// 				tin
	// 				equity
	// 				founding_date
	// 				shareholders {
	// 					name
	// 					tin
	// 					equity
	// 					founder
	// 				}
	// 			}
	// 		}
	// 	}
	// `
	// const [createCompany, { data, loading, error }] = useMutation(UPDATE_COMPANY);
	// if (error) {
	// 	console.log(error.message)
	// } else {
	// 	console.log(loading, data)
	// }
	// const details = { 
	// 	name: "Asperon OÜ",
	// 	tin: "16272114",
	// 	equity: 3600,
	// 	founding_date: "2023-01-16",
	// 	field_id: 'company',
	// 	shareholders: [
	// 		{
	// 			name: "Mattias Aabmets",
	// 			tin: "38812132731",
	// 			equity: 2500,
	// 			field_id: 'shareholder_1'
	// 		}, {
	// 			name: "Somebody Else",
	// 			tin: "42509072227",
	// 			equity: 1000,
	// 			field_id: 'shareholder_2'
	// 		}, {
	// 			name: "Third Person",
	// 			tin: "60706060153",
	// 			equity: 100,
	// 			field_id: "shareholder_3"
	// 		}
	// 	]
	// }
	// <button onClick={() => createCompany(
	// 	{ variables: {data: details}})}> Create Company 
	// </button>
	return (
		<div>
			UpdateEntityPage
		</div>
	);
}

export default UpdateEntityPage;