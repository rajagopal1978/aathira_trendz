'use client';

import Image from 'next/image';
import Link from 'next/link';

export default function CategorySection() {
  const categories = [
    {
      name: 'Kanchipuram Silk',
      image: '/images/WEB_BANNER_02_1.jpg',
      count: '150+ Designs',
      href: '#kanchipuram',
    },
    {
      name: 'Banarasi Sarees',
      image: '/images/WEB_BANNER_08_1.jpg',
      count: '200+ Designs',
      href: '#banarasi',
    },
    {
      name: 'Cotton Sarees',
      image: '/images/WEB_BANNER_09_1.jpg',
      count: '180+ Designs',
      href: '#cotton',
    },
    {
      name: 'Wedding Collection',
      image: '/images/WEB_BANNER_02_1.jpg',
      count: '120+ Designs',
      href: '#wedding',
    },
    {
      name: 'Party Wear',
      image: '/images/WEB_BANNER_08_1.jpg',
      count: '90+ Designs',
      href: '#party',
    },
    {
      name: 'Salwar Kameez',
      image: '/images/WEB_BANNER_09_1.jpg',
      count: '140+ Designs',
      href: '#salwar',
    },
  ];

  return (
    <section className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-900 to-orange-500 bg-clip-text text-transparent">
            Shop by Category
          </h2>
          <p className="text-gray-600 text-lg">
            Explore our curated collection of traditional and modern ethnic wear
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {categories.map((category) => (
            <Link
              key={category.name}
              href={category.href}
              className="group relative overflow-hidden rounded-lg shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:scale-105"
            >
              <div className="relative h-80">
                <Image
                  src={category.image}
                  alt={category.name}
                  fill
                  className="object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent opacity-70 group-hover:opacity-80 transition-opacity" />

                <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
                  <h3 className="text-2xl font-bold mb-2">{category.name}</h3>
                  <p className="text-sm text-gray-200 mb-4">{category.count}</p>
                  <span className="inline-block bg-white text-purple-900 px-6 py-2 rounded-full text-sm font-semibold group-hover:bg-orange-500 group-hover:text-white transition-colors">
                    Shop Now
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
