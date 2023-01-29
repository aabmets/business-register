import { showNotification } from '@mantine/notifications';
import { ImCross, ImCheckmark } from "react-icons/im";


export function notifyError(message: string): void {
	showNotification({
		autoClose: 5000,
		icon: <ImCross/>,
		title: 'Tehing ebaõnnestus!',
		color: 'red',
		message,
	});
}

export function notifySuccess(message: string): void {
	showNotification({
		autoClose: 5000,
		icon: <ImCheckmark/>,
		title: 'Tehing õnnestus!',
		color: 'green',
		message,
	});
}