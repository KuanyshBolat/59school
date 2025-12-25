'use client';

import { useEffect, useState } from 'react';
import { apiService, Page, Post } from '@/lib/api';

export default function TestApiPage() {
    const [pages, setPages] = useState<Page[]>([]);
    const [posts, setPosts] = useState<Post[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [pagesResponse, postsResponse] = await Promise.all([
                    apiService.getPages(),
                    apiService.getPosts(),
                ]);

                setPages(pagesResponse.data);
                setPosts(postsResponse.data);
                setLoading(false);
            } catch (err) {
                setError('Ошибка при загрузке данных');
                setLoading(false);
                console.error(err);
            }
        };

        fetchData();
    }, []);

    if (loading) return <div className="p-4">Загрузка...</div>;
    if (error) return <div className="p-4 text-red-500">{error}</div>;

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold mb-4">Тест API подключения</h1>

            <div className="mb-8">
                <h2 className="text-xl font-semibold mb-2">Страницы ({pages.length}):</h2>
                {pages.length === 0 ? (
                    <p className="text-gray-500">Нет страниц. Добавьте через админку Django.</p>
                ) : (
                    <div className="space-y-2">
                        {pages.map(page => (
                            <div key={page.id} className="p-3 border rounded">
                                <h3 className="font-medium">{page.title}</h3>
                                <p className="text-sm text-gray-600">{page.slug}</p>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <div>
                <h2 className="text-xl font-semibold mb-2">Посты ({posts.length}):</h2>
                {posts.length === 0 ? (
                    <p className="text-gray-500">Нет постов. Добавьте через админку Django.</p>
                ) : (
                    <div className="space-y-2">
                        {posts.map(post => (
                            <div key={post.id} className="p-3 border rounded">
                                <h3 className="font-medium">{post.title}</h3>
                                <p className="text-sm text-gray-600">{post.slug}</p>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <div className="mt-8 p-4 bg-blue-50 rounded">
                <h3 className="font-semibold mb-2">Инструкция:</h3>
                <ol className="list-decimal pl-5 space-y-1">
                    <li>Открой <a href="http://localhost:8000/admin" className="text-blue-600 underline">Django админку</a></li>
                    <li>Добавь несколько страниц и постов</li>
                    <li>Обнови эту страницу</li>
                    <li>Данные должны появиться выше</li>
                </ol>
            </div>
        </div>
    );
}