import React from 'react';
import { Leaf, ShieldCheck, Globe2 } from 'lucide-react';

const SustainabilityBadges = () => (
  <div className="mt-12 mb-4 flex flex-col md:flex-row items-center justify-center gap-6">
    <div className="flex items-center gap-3 bg-green-900/80 px-6 py-3 rounded-xl shadow border border-green-700">
      <Leaf className="w-6 h-6 text-green-300" />
      <span className="text-green-100 font-semibold text-lg">LEED Gold Certified</span>
    </div>
    <div className="flex items-center gap-3 bg-blue-900/80 px-6 py-3 rounded-xl shadow border border-blue-700">
      <Globe2 className="w-6 h-6 text-blue-200" />
      <span className="text-blue-100 font-semibold text-lg">Net Zero Ready</span>
    </div>
    <div className="flex items-center gap-3 bg-yellow-900/80 px-6 py-3 rounded-xl shadow border border-yellow-700">
      <ShieldCheck className="w-6 h-6 text-yellow-200" />
      <span className="text-yellow-100 font-semibold text-lg">ISO 19650 Compliant</span>
    </div>
  </div>
);

export default SustainabilityBadges;
