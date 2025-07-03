import React from 'react';
import { BarChart2, Clock, CheckCircle, AlertTriangle } from 'lucide-react';

const ProjectHealth = () => (
  <div className="my-10 rounded-2xl bg-gradient-to-br from-blue-900/80 via-teal-800/80 to-gray-900/80 p-8 shadow-xl flex flex-col md:flex-row items-center justify-between gap-6 border border-blue-900/30">
    <div>
      <h2 className="text-2xl md:text-3xl font-bold text-white mb-2 tracking-tight flex items-center gap-2">
        <BarChart2 className="w-7 h-7 text-synapse-teal" />
        Project Health
      </h2>
      <ul className="text-blue-100 text-lg md:text-xl space-y-2 mt-4">
        <li className="flex items-center gap-2">
          <Clock className="w-5 h-5 text-yellow-300" />
          <span className="font-semibold text-yellow-200">On Track:</span> 85% of milestones met
        </li>
        <li className="flex items-center gap-2">
          <CheckCircle className="w-5 h-5 text-green-300" />
          <span className="font-semibold text-green-200">Quality:</span> 98% of QA checks passed
        </li>
        <li className="flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-orange-300" />
          <span className="font-semibold text-orange-200">Attention:</span> 2 open issues in structural coordination
        </li>
      </ul>
    </div>
  </div>
);

export default ProjectHealth;
