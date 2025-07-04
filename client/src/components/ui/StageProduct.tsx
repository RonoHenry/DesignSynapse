import React from 'react';

const StageProduct = () => (
  <div className="mb-8 rounded-2xl bg-gradient-to-br from-orange-900/80 via-yellow-800/80 to-gray-900/80 p-8 shadow-xl flex flex-col gap-6 border border-orange-900/30">
    <h2 className="text-2xl md:text-3xl font-bold text-white mb-2 tracking-tight">Stage Product</h2>
    <p className="text-lg text-yellow-100 max-w-2xl mb-4">
      <span className="font-semibold text-orange-300">Interactive BIM Viewer</span><br />
      Load your <span className="font-semibold text-blue-200">Revit</span>, <span className="font-semibold text-teal-200">ArchiCAD</span>, or other BIM models here. Plug in vendor products and experiment with live integrations.
    </p>
    <div className="flex flex-wrap gap-4">
      <button className="bg-orange-700 hover:bg-orange-800 text-white font-semibold px-6 py-2 rounded-lg shadow transition">Load Model</button>
      <button className="bg-yellow-700 hover:bg-yellow-800 text-white font-semibold px-6 py-2 rounded-lg shadow transition">Zoom Fit</button>
      <button className="bg-gray-700 hover:bg-gray-800 text-white font-semibold px-6 py-2 rounded-lg shadow transition">Measure</button>
      <button className="bg-blue-800 hover:bg-blue-900 text-white font-semibold px-6 py-2 rounded-lg shadow transition">Section</button>
    </div>
    <div className="mt-6 bg-gray-900/60 rounded-xl h-64 flex items-center justify-center border-2 border-dashed border-orange-400">
      <span className="text-orange-200 text-lg font-medium">[ BIM Model Preview Area ]</span>
    </div>
  </div>
);

export default StageProduct;
