import { showNotification } from '@mantine/notifications';
import { ImCross, ImCheckmark } from "react-icons/im";
import { useTranslation } from 'react-i18next';


export function useNotifications() {
	const { t } = useTranslation('common');
	
	function notifySuccess(message: string): void {
		showNotification({
			autoClose: 5000,
			icon: <ImCheckmark/>,
			title: t("notifications.success"),
			color: 'green',
			message,
		});
	}

	function notifyFailure(message: string): void {
		showNotification({
			autoClose: 5000,
			icon: <ImCross/>,
			title: t("notifications.failure"),
			color: 'red',
			message,
		});
	}

	return {
		notifySuccess,
		notifyFailure,
	}
}