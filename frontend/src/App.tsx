import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { CompanyDetailsProvider } from "@context";
import { CompanyDetails } from "@types";
import { SiteHeader } from '@components';
import styles from './App.module.css';
import * as pages from "@pages";

function App() {
	const [companyDetails, setCompanyDetails] = useState<CompanyDetails | null>(null);

	return (
		<CompanyDetailsProvider value={{ companyDetails, setCompanyDetails }}>
			<BrowserRouter>
				<SiteHeader />
				<div className={styles.backgroundImage}/>
				<Routes>
					<Route index element={<pages.MainPage/>}/>
					<Route path='view' element={<pages.ViewCompanyPage/>}/>
					<Route path='create' element={<pages.CreateCompanyPage/>}/>
					<Route path='update' element={<pages.UpdateCompanyPage/>}/>
				</Routes>
			</BrowserRouter>
		</CompanyDetailsProvider>
	);
}

export default App