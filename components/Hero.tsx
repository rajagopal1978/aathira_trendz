'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export default function Hero() {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    {
      image: '/images/hero1.jpg',
      title: 'New Arrivals 2026',
      subtitle: 'Exclusive Collection of Designer Sarees',
      description: 'Handpicked collection featuring traditional craftsmanship',
      cta: 'Explore New Collection',
      position: 'left',
    },
    {
      image: '/images/banner-silk.jpg',
      title: 'Exquisite Silk Sarees',
      subtitle: 'Pure Kanchipuram & Banarasi Collection',
      description: 'Timeless elegance meets contemporary style',
      cta: 'Shop Silk Collection',
      position: 'center',
    },
    {
      image: '/images/banner-wedding.jpg',
      title: 'Wedding Special',
      subtitle: 'Bridal Wear & Festive Collection',
      description: 'Make your special moments unforgettable',
      cta: 'View Bridal Collection',
      position: 'right',
    },
    {
      image: '/images/hero4.jpg',
      title: 'Flat 30% Off',
      subtitle: 'Limited Time Seasonal Sale',
      description: 'Grab your favorites before they are gone',
      cta: 'Shop Now',
      position: 'center',
    },
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 5000);

    return () => clearInterval(timer);
  }, [slides.length]);

  const goToSlide = (index: number) => {
    setCurrentSlide(index);
  };

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  return (
    <div className="relative w-full h-[500px] md:h-[600px] lg:h-[700px] overflow-hidden bg-gray-900">
      {/* Slides */}
      {slides.map((slide, index) => (
        <div
          key={index}
          className={`absolute inset-0 transition-opacity duration-1000 ${
            index === currentSlide ? 'opacity-100' : 'opacity-0'
          }`}
        >
          <Image
            src={slide.image}
            alt={slide.title}
            fill
            className="object-cover"
            priority={index === 0}
            quality={95}
            sizes="100vw"
          />
          {/* Gradient Overlay for text readability */}
          <div className="absolute inset-0 bg-gradient-to-r from-black/70 via-black/40 to-transparent" />

          {/* Content Overlay */}
          <div className={`absolute inset-0 flex items-center ${
            slide.position === 'left' ? 'justify-start' :
            slide.position === 'right' ? 'justify-end' :
            'justify-center'
          }`}>
            <div className={`text-white px-6 md:px-12 lg:px-20 max-w-2xl ${
              slide.position === 'center' ? 'text-center' : 'text-left'
            }`}>
              {/* Animated Title */}
              <h1 className="text-4xl md:text-5xl lg:text-7xl font-bold mb-4 leading-tight animate-fadeIn drop-shadow-lg">
                {slide.title}
              </h1>

              {/* Subtitle */}
              <p className="text-xl md:text-2xl lg:text-3xl mb-3 font-semibold animate-fadeIn text-orange-400 drop-shadow-md">
                {slide.subtitle}
              </p>

              {/* Description */}
              <p className="text-base md:text-lg lg:text-xl mb-8 animate-fadeIn text-gray-200 drop-shadow-md">
                {slide.description}
              </p>

              {/* CTA Button */}
              <button className="bg-gradient-to-r from-purple-900 to-orange-500 text-white px-10 py-4 rounded-full text-base md:text-lg font-bold hover:shadow-2xl transform hover:scale-110 transition-all duration-300 hover:from-orange-500 hover:to-purple-900 uppercase tracking-wide">
                {slide.cta}
              </button>
            </div>
          </div>
        </div>
      ))}

      {/* Navigation Arrows */}
      <button
        onClick={prevSlide}
        className="absolute left-2 md:left-6 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-gradient-to-r hover:from-purple-900 hover:to-orange-500 rounded-full p-3 transition-all hover:scale-110 shadow-lg group"
        aria-label="Previous slide"
      >
        <ChevronLeft size={28} className="text-gray-800 group-hover:text-white transition-colors" />
      </button>
      <button
        onClick={nextSlide}
        className="absolute right-2 md:right-6 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-gradient-to-r hover:from-purple-900 hover:to-orange-500 rounded-full p-3 transition-all hover:scale-110 shadow-lg group"
        aria-label="Next slide"
      >
        <ChevronRight size={28} className="text-gray-800 group-hover:text-white transition-colors" />
      </button>

      {/* Dots Indicator */}
      <div className="absolute bottom-6 md:bottom-8 left-1/2 -translate-x-1/2 flex gap-3 bg-black/30 px-4 py-2 rounded-full backdrop-blur-sm">
        {slides.map((_, index) => (
          <button
            key={index}
            onClick={() => goToSlide(index)}
            className={`rounded-full transition-all ${
              index === currentSlide
                ? 'bg-gradient-to-r from-purple-500 to-orange-500 w-10 h-3'
                : 'bg-white/60 hover:bg-white/90 w-3 h-3'
            }`}
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>
    </div>
  );
}
