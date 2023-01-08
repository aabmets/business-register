import { Button } from '@mantine/core';
import { Link, useLocation, useNavigate  } from "react-router-dom";
import styles from './SiteHeader.module.css';
import logo from '/logo-est.svg';

function SiteHeader(): JSX.Element {
	const navigate = useNavigate();
	const location = useLocation();
	const path = location.pathname;

	function renderButton(path: string, label: string, toggle: boolean): JSX.Element {
		const style = toggle && location.pathname === path ? styles.button__selected : styles.button;
		return (
			<Button variant="default" size='md' radius="xl" className={style} onClick={() => navigate(path)}>
				<span className={styles.button__text}>{label}</span>
			</Button>
		);
	}
	const firstOption = ['/', '/create'].includes(path);
	const secondOption = ['/view', '/update'].includes(path);
	return (
		<div className={styles.center}>
			<div className={styles.header}>
				<Link to='/'>
					<img src={logo} alt='' className={styles.logo}/>
				</Link>
				<Button.Group>
					{renderButton('/', 'AVALEHELE', false)}
					{firstOption ? 
						renderButton('/create', 'UUS OSAÜHING', true) 
					: secondOption ?
						renderButton('/update', 'MUUDA OSAKAPITALI', true)
					: null}
				</Button.Group>
			</div>
		</div>
	);
}

export default SiteHeader;