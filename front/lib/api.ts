// Normalize NEXT_PUBLIC_API_URL: remove trailing slashes and accidental "/api" suffix
const _rawBackend = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
let BACKEND_BASE = _rawBackend.replace(/\/+$/g, '');
if (BACKEND_BASE.endsWith('/api')) {
    BACKEND_BASE = BACKEND_BASE.slice(0, -4);
}
const API_URL = `${BACKEND_BASE}/api/content`;

function ensureImageUrl(img: string | null | undefined) {
    if (!img) return '';
    if (img.startsWith('http://') || img.startsWith('https://')) return img;
    // if image already contains /media/ prefix
    if (img.startsWith('/')) img = img.slice(1);
    if (img.startsWith('media/')) return `${BACKEND_BASE}/${img}`;
    return `${BACKEND_BASE}/media/${img}`;
}

export interface Certificate {
    id: number;
    title: string;
    year: string;
    image: string;
    category: 'teachers' | 'students';
    level: 'district' | 'city';
    order: number;
}

export interface HeroSlide {
    id: number;
    title?: string;
    subtitle?: string;
    image: string;
    order: number;
}

export interface Stat {
    id: number;
    number: string;
    label: string;
    order: number;
}

export interface Page {
    id: number;
    slug: string;
    title: string;
    body?: string;
}

export const apiService = {
    async getCertificates(category?: string, level?: string) {
        const params = new URLSearchParams();
        if (category) params.append('category', category);
        if (level) params.append('level', level);

        const url = `${BACKEND_BASE}/api/achievements/certificates/?${params.toString()}`;
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('Failed to fetch certificates');
        }

        const data = await response.json();
        return data.map((d: any) => ({ ...d, image: ensureImageUrl(d.image) }));
    },

    async getHeroSlides(): Promise<HeroSlide[]> {
        const res = await fetch(`${API_URL}/hero-slides/`);
        if (!res.ok) throw new Error('Failed to fetch hero slides');
        const data = await res.json();
        return data.map((d: any) => ({ ...d, image: ensureImageUrl(d.image) }));
    },

    async getStats(): Promise<Stat[]> {
        const res = await fetch(`${API_URL}/stats/`);
        if (!res.ok) throw new Error('Failed to fetch stats');
        return res.json();
    },

    async getAbout(): Promise<any> {
        const res = await fetch(`${API_URL}/about/`);
        if (!res.ok) throw new Error('Failed to fetch about');
        const data = await res.json();
        if (Array.isArray(data)) {
            if (data[0]) data[0].image = ensureImageUrl(data[0].image);
            return data[0];
        }
        if (data) data.image = ensureImageUrl(data.image);
        return data;
    },

    async getDirector(): Promise<any> {
        const res = await fetch(`${API_URL}/director/`);
        if (!res.ok) throw new Error('Failed to fetch director');
        const data = await res.json();
        if (Array.isArray(data)) {
            if (data[0]) data[0].image = ensureImageUrl(data[0].image);
            return data[0];
        }
        if (data) data.image = ensureImageUrl(data.image);
        return data;
    },

    async getHeader(): Promise<any> {
        const res = await fetch(`${API_URL}/headers/`);
        if (!res.ok) throw new Error('Failed to fetch header');
        const data = await res.json();
        if (Array.isArray(data)) {
            if (data[0] && data[0].logo) data[0].logo = ensureImageUrl(data[0].logo);
            return data[0];
        }
        if (data && data.logo) data.logo = ensureImageUrl(data.logo);
        return data;
    },

    async getContact(): Promise<any> {
        const res = await fetch(`${API_URL}/contact/`);
        if (!res.ok) throw new Error('Failed to fetch contact');
        const data = await res.json();
        return Array.isArray(data) ? data[0] : data;
    },

    async getFooter(): Promise<any> {
        const res = await fetch(`${API_URL}/footers/`);
        if (!res.ok) throw new Error('Failed to fetch footer');
        const data = await res.json();
        return Array.isArray(data) ? data[0] : data;
    },

    async getPages(): Promise<Page[]> {
        const res = await fetch(`${API_URL}/pages/`);
        if (!res.ok) throw new Error('Failed to fetch pages');
        return res.json();
    }
};