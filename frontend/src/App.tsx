import { BrowserRouter, Routes, Route } from "react-router-dom";
import { MainPage, ViewEntityPage, CreateEntityPage, UpdateEntityPage } from "@pages";
import { SiteHeader } from '@components';

function App() {
	return (
		<BrowserRouter>
			<SiteHeader />
			<Routes>
				<Route index element={<MainPage/>}/>
				<Route path='view' element={<ViewEntityPage/>}/>
				<Route path='create' element={<CreateEntityPage/>}/>
				<Route path='update' element={<UpdateEntityPage/>}/>
			</Routes>
		</BrowserRouter>
	);
}

export default App