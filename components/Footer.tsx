'use client';

import Link from 'next/link';
import { Facebook, Instagram, Twitter, Youtube, Mail, Phone, MapPin } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300">
      {/* Newsletter Section */}
      <div className="bg-gradient-to-r from-purple-900 to-orange-500 py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto text-center">
            <h3 className="text-3xl font-bold text-white mb-4">
              Subscribe to Our Newsletter
            </h3>
            <p className="text-white mb-6">
              Get updates on new arrivals, special offers, and exclusive deals
            </p>
            <div className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-white"
              />
              <button className="bg-white text-purple-900 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
                Subscribe
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Footer */}
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* About */}
          <div>
            <h3 className="text-2xl font-bold text-white mb-4">Aathira Trendz</h3>
            <p className="mb-4 text-sm leading-relaxed">
              Your trusted destination for authentic Indian ethnic wear. We bring you
              the finest collection of silk sarees, cotton sarees, and traditional
              dress materials from across India.
            </p>
            <div className="flex gap-4">
              <Link
                href="#"
                className="bg-gray-800 p-2 rounded-full hover:bg-purple-900 transition-colors"
              >
                <Facebook size={20} />
              </Link>
              <Link
                href="#"
                className="bg-gray-800 p-2 rounded-full hover:bg-purple-900 transition-colors"
              >
                <Instagram size={20} />
              </Link>
              <Link
                href="#"
                className="bg-gray-800 p-2 rounded-full hover:bg-purple-900 transition-colors"
              >
                <Twitter size={20} />
              </Link>
              <Link
                href="#"
                className="bg-gray-800 p-2 rounded-full hover:bg-purple-900 transition-colors"
              >
                <Youtube size={20} />
              </Link>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="#" className="hover:text-orange-400 transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-orange-400 transition-colors">
                  New Arrivals
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-orange-400 transition-colors">
                  Best Sellers
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-orange-400 transition-colors">
                  Sale
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-orange-400 transition-colors">
                  Store Locator
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-orange-400 transition-colors">
                  Blog
                </Link>
              </li>
            </ul>
          </div>

          {/* Customer Service */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">
              Customer Service
            </h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link href="#" className="hover:text-orange-400 transition-colors">
                  Contact Us
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-orange-400 transition-colors">
                  Track Order
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-orange-400 transition-colors">
                  Shipping Policy
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-orange-400 transition-colors">
                  Return & Exchange
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-orange-400 transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-orange-400 transition-colors">
                  Terms & Conditions
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Contact Us</h4>
            <ul className="space-y-4 text-sm">
              <li className="flex items-start gap-3">
                <MapPin size={20} className="text-orange-400 flex-shrink-0 mt-1" />
                <span>
                  123 Textile Street, Fashion District
                  <br />
                  Chennai, Tamil Nadu 600001
                </span>
              </li>
              <li className="flex items-center gap-3">
                <Phone size={20} className="text-orange-400 flex-shrink-0" />
                <span>+91 999 999 9999</span>
              </li>
              <li className="flex items-center gap-3">
                <Mail size={20} className="text-orange-400 flex-shrink-0" />
                <span>info@aathiratrendz.com</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-800">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4 text-sm">
            <p>© 2026 Aathira Trendz. All rights reserved.</p>
            <div className="flex gap-6">
              <Link href="#" className="hover:text-orange-400 transition-colors">
                Privacy Policy
              </Link>
              <Link href="#" className="hover:text-orange-400 transition-colors">
                Terms of Service
              </Link>
              <Link href="#" className="hover:text-orange-400 transition-colors">
                Sitemap
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
