const BACKEND_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
const API_URL = `${BACKEND_BASE}/api/content`;

function ensureImageUrl(img: string | null | undefined) {
    if (!img) return '';
    if (typeof img !== 'string') return '';
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
        // about may be a list; return first with normalized image
        const item = Array.isArray(data) ? data[0] : data;
        if (item) item.image = ensureImageUrl(item.image);
        return item;
    },

    async getDirector(): Promise<any> {
        const res = await fetch(`${API_URL}/director/`);
        if (!res.ok) throw new Error('Failed to fetch director');
        const data = await res.json();
        const item = Array.isArray(data) ? data[0] : data;
        if (item) item.image = ensureImageUrl(item.image);
        return item;
    },

    async getHeader(): Promise<any> {
        const res = await fetch(`${API_URL}/headers/`);
        if (!res.ok) throw new Error('Failed to fetch header');
        const data = await res.json();
        const item = Array.isArray(data) ? data[0] : data;
        if (item && item.logo) item.logo = ensureImageUrl(item.logo);
        return item;
    },

    async getContact(): Promise<any> {
        const res = await fetch(`${API_URL}/contact/`);
        if (!res.ok) throw new Error('Failed to fetch contact');
        const data = await res.json();
        const item = Array.isArray(data) ? data[0] : data;
        return item;
    },

    async getFooter(): Promise<any> {
        const res = await fetch(`${API_URL}/footers/`);
        if (!res.ok) throw new Error('Failed to fetch footer');
        const data = await res.json();
        const item = Array.isArray(data) ? data[0] : data;
        return item;
    },

    async getPages(): Promise<Page[]> {
        const res = await fetch(`${API_URL}/pages/`);
        if (!res.ok) throw new Error('Failed to fetch pages');
        return res.json();
    }
};