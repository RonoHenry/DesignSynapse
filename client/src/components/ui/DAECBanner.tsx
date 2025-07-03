import React from 'react';


const handleDAECClick = (discipline: string) => {
  // Placeholder: You can replace this with scroll, modal, or filter logic
  alert(`You clicked on ${discipline}`);
};

const DAECBanner = () => (
  <div className="mb-8 rounded-2xl bg-gradient-to-br from-blue-900/80 via-teal-800/80 to-gray-900/80 p-8 shadow-xl flex flex-col md:flex-row items-center justify-between gap-6 border border-blue-900/30">
    <div>
      <h1 className="text-3xl md:text-4xl font-bold text-white mb-2 tracking-tight">Design Synapse: The Unified DAEC Platform</h1>
      <p className="text-lg md:text-xl text-blue-100 max-w-2xl">Integrating <span className="font-semibold text-teal-300">AI</span>, <span className="font-semibold text-blue-300">BIM</span>, and professional design tools to transform your construction and design workflows. <span className="text-orange-200 font-semibold">Experience the future of architectural collaboration.</span></p>
    </div>
    <div className="flex items-center space-x-4">
      <button onClick={() => handleDAECClick('Design')} className="inline-block bg-blue-800/80 text-blue-100 px-4 py-2 rounded-lg font-semibold text-sm tracking-wide shadow hover:bg-blue-700/90 focus:outline-none focus:ring-2 focus:ring-blue-400 transition">
        Design
      </button>
      <button onClick={() => handleDAECClick('Architecture')} className="inline-block bg-teal-800/80 text-teal-100 px-4 py-2 rounded-lg font-semibold text-sm tracking-wide shadow hover:bg-teal-700/90 focus:outline-none focus:ring-2 focus:ring-teal-400 transition">
        Architecture
      </button>
      <button onClick={() => handleDAECClick('Engineering')} className="inline-block bg-orange-800/80 text-orange-100 px-4 py-2 rounded-lg font-semibold text-sm tracking-wide shadow hover:bg-orange-700/90 focus:outline-none focus:ring-2 focus:ring-orange-400 transition">
        Engineering
      </button>
      <button onClick={() => handleDAECClick('Construction')} className="inline-block bg-gray-800/80 text-gray-100 px-4 py-2 rounded-lg font-semibold text-sm tracking-wide shadow hover:bg-gray-700/90 focus:outline-none focus:ring-2 focus:ring-gray-400 transition">
        Construction
      </button>
    </div>
  </div>
);

export default DAECBanner;
