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

const VendorProductLibrary = () => (
  <div className="mb-12">
    <div className="flex items-center justify-between mb-6">
      <h2 className="text-2xl md:text-3xl font-bold text-white tracking-tight flex items-center gap-2">
        <ShoppingCart className="w-7 h-7 text-synapse-orange" />
        Vendor Product Library
      </h2>
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-5 h-5" />
        <input
          type="text"
          placeholder="Search products, vendors..."
          className="pl-10 pr-4 py-2 rounded-lg bg-card border border-border text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>
    </div>
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
      {mockProducts.map((item) => (
        <div key={item.id} className="bg-card rounded-xl shadow-lg overflow-hidden group border border-border hover:scale-105 transition-transform duration-300 flex flex-col">
          <div className="h-32 bg-gray-900 flex items-center justify-center overflow-hidden">
            <img src={item.image} alt={item.name} className="object-cover w-full h-full group-hover:opacity-90 transition-opacity duration-300" />
          </div>
          <div className="p-4 flex-1 flex flex-col justify-between">
            <div>
              <div className="text-lg font-semibold text-foreground mb-1 flex items-center gap-2">
                {item.name}
                <span className="inline-flex items-center px-2 py-0.5 rounded bg-muted text-xs text-muted-foreground ml-2">
                  <Tag className="w-3 h-3 mr-1" />{item.category}
                </span>
              </div>
              <div className="text-sm text-muted-foreground mb-1">by {item.vendor}</div>
            </div>
            <div className="flex items-center justify-between mt-2">
              <div className="text-synapse-orange font-bold text-lg">${item.price}</div>
              <button className="px-3 py-1 bg-synapse-orange text-white rounded hover:bg-orange-600 text-xs font-semibold transition flex items-center gap-1">
                <ShoppingCart className="w-4 h-4" /> Stage
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  </div>
);

export default VendorProductLibrary;
