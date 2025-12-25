const API_URL = 'http://127.0.0.1:8000/api';

export interface Certificate {
    id: number;
    title: string;
    year: string;
    image: string;
    category: 'teachers' | 'students';
    level: 'district' | 'city';
    order: number;
}

export const apiService = {
    async getCertificates(category?: string, level?: string): Promise<Certificate[]> {
        const params = new URLSearchParams();
        if (category) params.append('category', category);
        if (level) params.append('level', level);

        const url = `${API_URL}/certificates/?${params.toString()}`;
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('Failed to fetch certificates');
        }

        return response.json();
    },
};