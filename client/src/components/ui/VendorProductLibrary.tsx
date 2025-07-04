import React from 'react';
import { ShoppingCart, Search, Tag } from 'lucide-react';

const mockProducts = [
  {
    id: 1,
    name: 'Modern Curtain',
    vendor: 'CurtainCo',
    price: 120,
    image: '/vendor/curtain.jpg',
    category: 'Curtains',
  },
  {
    id: 2,
    name: 'Designer Sofa',
    vendor: 'FurniStyle',
    price: 950,
    image: '/vendor/sofa.jpg',
    category: 'Furniture',
  },
  {
    id: 3,
    name: 'Stainless Utensil Set',
    vendor: 'KitchenPro',
    price: 60,
    image: '/vendor/utensils.jpg',
    category: 'Utensils',
  },
  {
    id: 4,
    name: 'Smart Lighting',
    vendor: 'BrightTech',
    price: 80,
    image: '/vendor/lighting.jpg',
    category: 'Lighting',
  },
];

import { useEffect, useState } from 'react';

const FILTERS = [
  { label: 'Vendors', value: 'vendors' },
  { label: 'Categories', value: 'categories' },
  { label: 'All Products', value: 'all' },
];

const VendorProductLibrary = () => {
  const [filter, setFilter] = useState('all');
  const [products, setProducts] = useState(mockProducts);

  useEffect(() => {
    const handler = (e) => {
      const customEvent = e;
      if (customEvent.detail && customEvent.detail.filter) {
        setFilter(customEvent.detail.filter);
      }
    };
    window.addEventListener('vendor-product-filter', handler);
    return () => window.removeEventListener('vendor-product-filter', handler);
  }, []);

  useEffect(() => {
    let filtered;
    if (filter === 'vendors') {
      const seen = new Set();
      filtered = mockProducts.filter((p) => {
        if (seen.has(p.vendor)) return false;
        seen.add(p.vendor);
        return true;
      });
    } else if (filter === 'categories') {
      const seen = new Set();
      filtered = mockProducts.filter((p) => {
        if (seen.has(p.category)) return false;
        seen.add(p.category);
        return true;
      });
    } else {
      filtered = mockProducts;
    }
    setProducts(filtered);
  }, [filter]);

  return (
    <div className="mb-4">
      <div className="flex gap-2 mb-2">
        {FILTERS.map((f) => (
          <button
            key={f.value}
            className={`px-3 py-1 rounded text-xs font-semibold transition ${filter === f.value ? 'bg-indigo-800 text-white' : 'bg-indigo-700 text-white hover:bg-indigo-800'}`}
            onClick={() => setFilter(f.value)}
          >
            {f.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default VendorProductLibrary;
