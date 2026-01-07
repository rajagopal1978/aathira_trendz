'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { ShoppingCart, User, Heart, Menu, X, Search, Phone } from 'lucide-react';

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const categories = [
    { name: 'New Arrivals', href: '#new-arrivals' },
    { name: 'Silk Collection', href: '#silk' },
    { name: 'Cotton Sarees', href: '#cotton' },
    { name: 'Party Wear', href: '#party-wear' },
    { name: 'Salwar Kameez', href: '#salwar' },
    { name: 'Wedding Collection', href: '#wedding' },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white shadow-md">
      {/* Top Bar */}
      <div className="bg-gradient-to-r from-purple-900 to-blue-900 text-white py-2">
        <div className="container mx-auto px-4 flex justify-between items-center text-sm">
          <div className="flex items-center gap-2">
            <Phone size={16} />
            <span>+91 999 999 9999</span>
          </div>
          <div className="hidden md:block">
            <span>Worldwide Shipping Available | Free Shipping on Orders Above ₹2000</span>
          </div>
          <div className="flex gap-4">
            <select className="bg-transparent border-none outline-none cursor-pointer">
              <option value="INR">INR ₹</option>
              <option value="USD">USD $</option>
              <option value="GBP">GBP £</option>
            </select>
          </div>
        </div>
      </div>

      {/* Main Header */}
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center">
            <div className="text-3xl font-bold bg-gradient-to-r from-purple-900 to-orange-500 bg-clip-text text-transparent">
              Aathira Trendz
            </div>
          </Link>

          {/* Search Bar - Desktop */}
          <div className="hidden md:flex flex-1 max-w-xl mx-8">
            <div className="relative w-full">
              <input
                type="text"
                placeholder="Search for sarees, dress materials..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-900"
              />
              <Search className="absolute right-3 top-2.5 text-gray-400" size={20} />
            </div>
          </div>

          {/* Icons */}
          <div className="flex items-center gap-4">
            <button className="hidden md:flex items-center gap-1 hover:text-purple-900">
              <User size={24} />
              <span className="text-sm">Account</span>
            </button>
            <button className="hidden md:flex items-center gap-1 hover:text-purple-900 relative">
              <Heart size={24} />
              <span className="text-sm">Wishlist</span>
            </button>
            <button className="flex items-center gap-1 hover:text-purple-900 relative">
              <ShoppingCart size={24} />
              <span className="hidden md:inline text-sm">Cart</span>
              <span className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                0
              </span>
            </button>
            <button
              className="md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Search Bar - Mobile */}
        <div className="md:hidden mt-3">
          <div className="relative w-full">
            <input
              type="text"
              placeholder="Search for sarees..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-900"
            />
            <Search className="absolute right-3 top-2.5 text-gray-400" size={20} />
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="bg-gray-50 border-t border-gray-200">
        <div className="container mx-auto px-4">
          {/* Desktop Navigation */}
          <ul className="hidden md:flex justify-center gap-8 py-3">
            {categories.map((category) => (
              <li key={category.name}>
                <Link
                  href={category.href}
                  className="text-gray-700 hover:text-purple-900 font-medium transition-colors"
                >
                  {category.name}
                </Link>
              </li>
            ))}
          </ul>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <ul className="md:hidden py-4 space-y-3">
              {categories.map((category) => (
                <li key={category.name}>
                  <Link
                    href={category.href}
                    className="block text-gray-700 hover:text-purple-900 font-medium py-2"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    {category.name}
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
      </nav>
    </header>
  );
}
