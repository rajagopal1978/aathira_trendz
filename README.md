# Aathira Trendz - E-Commerce Website

A beautiful, modern e-commerce website for ethnic wear built with Next.js 15, TypeScript, and Tailwind CSS. Inspired by premium silk saree retailers, this website features a stunning design with smooth animations and a responsive layout.

## Features

- **Modern Design**: Beautiful gradient colors (purple to orange) with smooth animations
- **Responsive Layout**: Optimized for mobile, tablet, and desktop devices
- **Hero Carousel**: Auto-rotating banner with smooth transitions
- **Product Grid**: Stunning product cards with hover effects
- **Category Sections**: Organized shopping by categories
- **Features Section**: Highlighting key services (shipping, support, returns)
- **Newsletter Subscription**: Integrated newsletter signup
- **Sticky Navigation**: Easy-to-use navigation with search functionality
- **Icons**: Beautiful Lucide React icons throughout

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Images**: Next.js Image Optimization

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
aathira-trendz/
├── app/
│   ├── globals.css          # Global styles and animations
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Homepage
├── components/
│   ├── Header.tsx           # Navigation header with search
│   ├── Hero.tsx             # Auto-rotating hero carousel
│   ├── CategorySection.tsx  # Product categories grid
│   ├── ProductGrid.tsx      # Featured products display
│   ├── Features.tsx         # Service features section
│   └── Footer.tsx           # Footer with links and newsletter
├── public/
│   └── images/              # Product and banner images
└── README.md
```

## Color Scheme

- **Primary Purple**: #3F4293 (Deep Blue Purple)
- **Primary Orange**: #ee5330 (Coral Orange)
- **Gradients**: Purple to Orange, Purple to Blue

## Customization

### Update Colors
Edit the color values in the component files or add custom colors to your Tailwind config.

### Add More Products
Edit the `products` array in `components/ProductGrid.tsx` to add your own products.

### Change Categories
Modify the `categories` array in `components/CategorySection.tsx` to update categories.

### Update Contact Info
Edit the contact details in `components/Footer.tsx` and `components/Header.tsx`.

## Build for Production

```bash
npm run build
npm start
```

## Deploy

This website can be easily deployed to:
- Vercel (recommended for Next.js)
- Netlify
- AWS
- Any hosting platform that supports Node.js

## License

This project is open source and available for personal and commercial use.

## Credits

Design inspired by premium Indian ethnic wear retailers. Built with modern web technologies for optimal performance and user experience.
