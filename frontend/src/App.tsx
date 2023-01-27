import { BrowserRouter, Routes, Route } from "react-router-dom";
import { SiteHeader } from '@components';
import styles from './App.module.css';
import * as pages from "@pages";

function App() {
	return (
		<BrowserRouter>
			<SiteHeader />
			<div className={styles.backgroundImage}/>
			<Routes>
				<Route index element={<pages.MainPage/>}/>
				<Route path='view' element={<pages.ViewCompanyPage/>}/>
				<Route path='create' element={<pages.UpdateCompanyPage/>}/>
				<Route path='update' element={<pages.CreateCompanyPage/>}/>
			</Routes>
		</BrowserRouter>
	);
}

export default App