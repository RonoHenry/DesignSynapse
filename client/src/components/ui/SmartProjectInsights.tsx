import React from 'react';
import { AlertTriangle, TrendingUp, Zap, CheckCircle } from 'lucide-react';

const SmartProjectInsights = () => (
  <div className="mb-8 rounded-2xl bg-gradient-to-br from-blue-900/80 via-teal-800/80 to-gray-900/80 p-8 shadow-xl flex flex-col md:flex-row items-center justify-between gap-6 border border-blue-900/30">
    <div>
      <h2 className="text-2xl md:text-3xl font-bold text-white mb-2 tracking-tight flex items-center gap-2">
        <Zap className="w-7 h-7 text-yellow-300 animate-pulse" />
        Smart Project Insights
      </h2>
      <ul className="text-blue-100 text-lg md:text-xl space-y-2 mt-4">
        <li className="flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-orange-300" />
          <span className="font-semibold text-orange-200">Risk Alert:</span> Potential schedule delay detected in MEP coordination.
        </li>
        <li className="flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-teal-300" />
          <span className="font-semibold text-teal-200">Cost Insight:</span> Projected cost overrun of 3.2% based on recent design changes.
        </li>
        <li className="flex items-center gap-2">
          <CheckCircle className="w-5 h-5 text-green-300" />
          <span className="font-semibold text-green-200">Sustainability:</span> Model meets LEED Gold requirements.
        </li>
      </ul>
    </div>
  </div>
);

export default SmartProjectInsights;
