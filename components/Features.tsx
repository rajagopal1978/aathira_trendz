'use client';

import { Truck, Shield, Headphones, RefreshCw } from 'lucide-react';

export default function Features() {
  const features = [
    {
      icon: <Truck size={40} />,
      title: 'Worldwide Shipping',
      description: 'Free shipping on orders above ₹2000',
    },
    {
      icon: <Shield size={40} />,
      title: 'Secure Payment',
      description: '100% secure payment gateway',
    },
    {
      icon: <Headphones size={40} />,
      title: '24/7 Support',
      description: 'Dedicated customer support team',
    },
    {
      icon: <RefreshCw size={40} />,
      title: 'Easy Returns',
      description: '7-day hassle-free return policy',
    },
  ];

  return (
    <section className="py-16 bg-gradient-to-r from-purple-900 to-blue-900">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="flex flex-col items-center text-center text-white p-6 rounded-lg hover:bg-white/10 transition-all duration-300"
            >
              <div className="mb-4 text-orange-400">{feature.icon}</div>
              <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
              <p className="text-gray-200 text-sm">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
