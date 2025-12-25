'use client';

import { useEffect, useState } from 'react';

import Header from "@/components/header"
import Hero from "@/components/hero"
import About from "@/components/about"
import Stats from "@/components/stats"
import Director from "@/components/director"
import { Achievements } from "@/components/achievements"
import Contact from "@/components/contact"
import Footer from "@/components/footer"
import { apiService } from '@/lib/api';
import Link from 'next/link';

export default function Home() {
    const [loading, setLoading] = useState(true);


    return (
        <main className="w-full">
            <Header />
            <Hero />
            <About />
            <Stats />
            <Director />
            <Achievements />
            <Contact />
            <Footer />
        </main>
    )
}