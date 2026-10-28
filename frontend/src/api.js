const API = import.meta.env.VITE_API_URL

export async function api(path, options = {}) {
    const token = localStorage.getItem('token');
    const res =  await fetch(`${API}${path}`, {
        ...options, 
        headers: {
            'Content-type': 'application/json', 
            ...(token && {Authorization: `Bearer ${token}`}),
        },
    });
    if (!res.ok){
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || 'Request failed');
    }
    return res.json()
}
    