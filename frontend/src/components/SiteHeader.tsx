import { Button } from '@mantine/core';
import { useTranslation } from 'react-i18next';
import { useLocation, useNavigate } from "react-router-dom";
import { Link, useSearchParams } from "react-router-dom";
import styles from './SiteHeader.module.css';
import logo from '/logo-est.svg';

function SiteHeader(): JSX.Element {
	const { t } = useTranslation('common');
	const [searchParams] = useSearchParams();
	const tin = searchParams.get('tin') || '';
	const navigate = useNavigate();
	const location = useLocation();
	const path = location.pathname;
	
	function renderButton(path: string, label: string, toggle: boolean): JSX.Element {
		const current = location.pathname === path;
		const style = toggle && current ? styles.button__selected : styles.button;
		const callback = () => current ? null : navigate(path);
		return (
			<Button 
				size='md' 
				radius="xl" 
				variant="default" 
				className={style}
				onClick={callback}>
					<span className={styles.button__text}>
						{label}
					</span>
			</Button>
		);
	}
	
	return (
		<div className={styles.center}>
			<div className={styles.header}>
				<Link to='/'>
					<img src={logo} alt='' className={styles.logo}/>
				</Link>
				{path === '/' ?
					renderButton('/create', t('header.new-company'), true) 
				: null}
				{path === '/view' ?
					<Button.Group>
						{renderButton('/', t('header.goto-main-page'), false)}
						{renderButton(`/update?tin=${tin}`, t('header.change-equity'), true)}
					</Button.Group>
				: null}
				{path === '/update' ?
					<Button.Group>
						{renderButton(`/view?tin=${tin}`, t('header.back'), false)}
						{renderButton('/update', t('header.change-equity'), true)}
					</Button.Group>
				: null}
				{path === '/create' ?
					<Button.Group>
						{renderButton('/', t('header.goto-main-page'), false)}
						{renderButton('/create', t('header.new-company'), true)}
					</Button.Group>
				: null}
			</div>
		</div>
	);
}

export default SiteHeader;