import React from 'react';

const galleryItems = [
  {
    title: 'Parametric Tower',
    image: '/gallery/tower.jpg',
    author: 'Studio A',
    type: 'BIM Model',
  },
  {
    title: 'Atrium Render',
    image: '/gallery/atrium.jpg',
    author: 'RenderLab',
    type: 'Render',
  },
  {
    title: 'Sustainable Campus',
    image: '/gallery/campus.jpg',
    author: 'EcoDesign',
    type: 'Design',
  },
  {
    title: 'MEP Coordination',
    image: '/gallery/mep.jpg',
    author: 'MEP Team',
    type: 'Draft',
  },
];

const DesignGallery = () => (
  <div className="mb-12">
    <h2 className="text-2xl md:text-3xl font-bold text-white mb-6 tracking-tight">Design Gallery</h2>
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
      {galleryItems.map((item, idx) => (
        <div key={idx} className="bg-card rounded-xl shadow-lg overflow-hidden group border border-border hover:scale-105 transition-transform duration-300">
          <div className="h-40 bg-gray-900 flex items-center justify-center overflow-hidden">
            <img src={item.image} alt={item.title} className="object-cover w-full h-full group-hover:opacity-90 transition-opacity duration-300" />
          </div>
          <div className="p-4">
            <div className="text-lg font-semibold text-foreground mb-1">{item.title}</div>
            <div className="text-sm text-muted-foreground mb-1">{item.type}</div>
            <div className="text-xs text-gray-400">by {item.author}</div>
          </div>
        </div>
      ))}
    </div>
  </div>
);

export default DesignGallery;
