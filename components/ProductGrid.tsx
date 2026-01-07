'use client';

import Image from 'next/image';
import { Heart, ShoppingCart, Eye } from 'lucide-react';

export default function ProductGrid() {
  const products = [
    {
      id: 1,
      name: 'Royal Kanchipuram Silk Saree',
      price: 15999,
      originalPrice: 21999,
      image: '/images/WEB_BANNER_02_1.jpg',
      discount: '27% OFF',
      tag: 'Bestseller',
    },
    {
      id: 2,
      name: 'Premium Banarasi Silk Saree',
      price: 18999,
      originalPrice: 24999,
      image: '/images/WEB_BANNER_08_1.jpg',
      discount: '24% OFF',
      tag: 'New',
    },
    {
      id: 3,
      name: 'Designer Wedding Saree',
      price: 22999,
      originalPrice: 29999,
      image: '/images/WEB_BANNER_09_1.jpg',
      discount: '23% OFF',
      tag: 'Premium',
    },
    {
      id: 4,
      name: 'Soft Silk Party Wear Saree',
      price: 12999,
      originalPrice: 17999,
      image: '/images/WEB_BANNER_02_1.jpg',
      discount: '28% OFF',
      tag: 'Trending',
    },
    {
      id: 5,
      name: 'Cotton Silk Casual Saree',
      price: 8999,
      originalPrice: 12999,
      image: '/images/WEB_BANNER_08_1.jpg',
      discount: '31% OFF',
      tag: 'New',
    },
    {
      id: 6,
      name: 'Exclusive Bridal Collection',
      price: 32999,
      originalPrice: 42999,
      image: '/images/WEB_BANNER_09_1.jpg',
      discount: '23% OFF',
      tag: 'Bestseller',
    },
    {
      id: 7,
      name: 'Traditional Temple Border Saree',
      price: 14999,
      originalPrice: 19999,
      image: '/images/WEB_BANNER_02_1.jpg',
      discount: '25% OFF',
      tag: 'Premium',
    },
    {
      id: 8,
      name: 'Handloom Pure Silk Saree',
      price: 19999,
      originalPrice: 26999,
      image: '/images/WEB_BANNER_08_1.jpg',
      discount: '26% OFF',
      tag: 'New',
    },
  ];

  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-900 to-orange-500 bg-clip-text text-transparent">
            Featured Products
          </h2>
          <p className="text-gray-600 text-lg">
            Handpicked collection of our finest sarees and ethnic wear
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {products.map((product) => (
            <div
              key={product.id}
              className="group bg-white rounded-lg overflow-hidden shadow-md hover:shadow-2xl transition-all duration-300 border border-gray-100"
            >
              {/* Product Image */}
              <div className="relative h-80 overflow-hidden bg-gray-100">
                <Image
                  src={product.image}
                  alt={product.name}
                  fill
                  className="object-cover group-hover:scale-110 transition-transform duration-500"
                />

                {/* Tags */}
                <div className="absolute top-3 left-3 flex flex-col gap-2">
                  <span className="bg-orange-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                    {product.discount}
                  </span>
                  <span className="bg-purple-900 text-white text-xs font-bold px-3 py-1 rounded-full">
                    {product.tag}
                  </span>
                </div>

                {/* Quick Actions */}
                <div className="absolute top-3 right-3 flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <button className="bg-white p-2 rounded-full shadow-lg hover:bg-purple-900 hover:text-white transition-colors">
                    <Heart size={18} />
                  </button>
                  <button className="bg-white p-2 rounded-full shadow-lg hover:bg-purple-900 hover:text-white transition-colors">
                    <Eye size={18} />
                  </button>
                </div>

                {/* Add to Cart - Appears on Hover */}
                <div className="absolute bottom-0 left-0 right-0 transform translate-y-full group-hover:translate-y-0 transition-transform duration-300">
                  <button className="w-full bg-purple-900 text-white py-3 font-semibold hover:bg-orange-500 transition-colors flex items-center justify-center gap-2">
                    <ShoppingCart size={18} />
                    Add to Cart
                  </button>
                </div>
              </div>

              {/* Product Details */}
              <div className="p-4">
                <h3 className="text-lg font-semibold text-gray-800 mb-2 line-clamp-2 h-14">
                  {product.name}
                </h3>

                <div className="flex items-center gap-2 mb-3">
                  <span className="text-2xl font-bold text-purple-900">
                    ₹{product.price.toLocaleString()}
                  </span>
                  <span className="text-sm text-gray-400 line-through">
                    ₹{product.originalPrice.toLocaleString()}
                  </span>
                </div>

                <div className="flex items-center gap-1 text-yellow-500 mb-2">
                  {[...Array(5)].map((_, i) => (
                    <svg
                      key={i}
                      className="w-4 h-4 fill-current"
                      viewBox="0 0 20 20"
                    >
                      <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                    </svg>
                  ))}
                  <span className="text-gray-600 text-sm ml-1">(4.8)</span>
                </div>

                <p className="text-green-600 text-sm font-medium">
                  Free Shipping Available
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* View All Button */}
        <div className="text-center mt-12">
          <button className="bg-gradient-to-r from-purple-900 to-orange-500 text-white px-12 py-4 rounded-lg text-lg font-semibold hover:shadow-lg transform hover:scale-105 transition-all duration-300">
            View All Products
          </button>
        </div>
      </div>
    </section>
  );
}
