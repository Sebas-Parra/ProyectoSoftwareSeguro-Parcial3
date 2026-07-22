import axios from 'axios';

// Crear instancia de axios
const apiClientAuth = axios.create({
    baseURL: import.meta.env.VITE_API_AUTH_URL,
    timeout: import.meta.env.VITE_API_TIMEOUT,
    headers: {
        'Content-Type': 'application/json'
    }
});

const apiClientSale = axios.create({
    baseURL: import.meta.env.VITE_API_SALE_URL,
    timeout: import.meta.env.VITE_API_TIMEOUT,
    headers: {
        'Content-Type': 'application/json'
    }
});

apiClientAuth.interceptors.request.use(
    (config) => {
        // Verificamos si la petición solicitó explícitamente el token temporal
        const tokenKey = config.useTempToken ? 'tempToken' : 'accessToken';
        const token = localStorage.getItem(tokenKey);

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        // Limpiamos la propiedad para que no se envíe al servidor por error
        delete config.useTempToken;

        return config;
    },
    (error) => Promise.reject(error)
);

apiClientSale.interceptors.request.use(
    (config) => {
        // Verificamos si la petición solicitó explícitamente el token temporal
        const tokenKey = config.useTempToken ? 'tempToken' : 'accessToken';
        const token = localStorage.getItem(tokenKey);

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        // Limpiamos la propiedad para que no se envíe al servidor por error
        delete config.useTempToken;

        return config;
    },
    (error) => Promise.reject(error)
);



// Interceptor para manejar errores de respuesta (especialmente token expirado)
apiClientAuth.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Si el error es 401 (token expirado) y no es un request de refresh
        if (error.response?.status === 401 && !originalRequest._retry && !originalRequest.url.includes('refresh-token')) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refreshToken');
                if (refreshToken) {
                    const { data } = await axios.post(
                        `${import.meta.env.VITE_API_AUTH_URL}/auth/refresh-token`,
                        { token: refreshToken }
                    );

                    localStorage.setItem('accessToken', data.accessToken);
                    originalRequest.headers.Authorization = `Bearer ${data.accessToken}`;
                    return apiClientAuth(originalRequest);
                }
            } catch (refreshError) {
                // Si falla el refresh, limpiar localStorage y redirigir a login
                localStorage.removeItem('accessToken');
                localStorage.removeItem('refreshToken');
                localStorage.removeItem('user');
                localStorage.removeItem('activeRole');
                localStorage.removeItem('tempToken');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

// Interceptor para manejar errores de respuesta (especialmente token expirado)
apiClientSale.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Si el error es 401 (token expirado) y no es un request de refresh
        if (error.response?.status === 401 && !originalRequest._retry && !originalRequest.url.includes('refresh-token')) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refreshToken');
                if (refreshToken) {
                    const { data } = await axios.post(
                        `${import.meta.env.VITE_API_AUTH_URL}/auth/refresh-token`,
                        { token: refreshToken }
                    );

                    localStorage.setItem('accessToken', data.accessToken);
                    originalRequest.headers.Authorization = `Bearer ${data.accessToken}`;
                    return apiClientAuth(originalRequest);
                }
            } catch (refreshError) {
                // Si falla el refresh, limpiar localStorage y redirigir a login
                localStorage.removeItem('accessToken');
                localStorage.removeItem('refreshToken');
                localStorage.removeItem('user');
                localStorage.removeItem('activeRole');
                localStorage.removeItem('tempToken');
                window.location.href = '/login';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);


export { apiClientAuth, apiClientSale };


