import { createGenericContext } from "./GenericContext";
import { CompanyDetails } from "@types";

export interface CompanyDetailsStore {
	setCompanyDetails: React.Dispatch<React.SetStateAction<CompanyDetails | null>>;
	companyDetails: CompanyDetails | null;
}

const { Provider, useContext } = createGenericContext<CompanyDetailsStore>();

export const CompanyDetailsProvider = Provider;
export const useCompanyDetails = useContext;