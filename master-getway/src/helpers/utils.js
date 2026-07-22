import { useToast } from 'primevue/usetoast';


function toggleDarkMode() {
    const element = document.querySelector('html');
    element.classList.toggle('my-app-dark');
};

export function useToastGlobal() {
    const toast = useToast();

    const msjShow = (color, summary, message, life = 3000) => {
        toast.add({ severity: color, summary, detail: message, life });
    };

    return { msjShow };
}

export const toggleDarkModeFacade = () => {
    return toggleDarkMode();
};