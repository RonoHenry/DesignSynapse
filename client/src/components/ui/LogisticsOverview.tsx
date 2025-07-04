import React from 'react';
import { Truck, Map, Clock, AlertTriangle } from 'lucide-react';

const LogisticsOverview = () => (
  <div className="rounded-xl bg-gradient-to-br from-yellow-900/80 via-yellow-800/80 to-gray-900/80 p-6 shadow-lg border border-yellow-900/30 text-yellow-50 w-full max-w-2xl mx-auto mb-6">
    <div className="flex items-center gap-3 mb-4">
      <Truck className="w-7 h-7 text-yellow-300 animate-bounce" />
      <h3 className="text-xl font-bold tracking-tight">Logistics Overview</h3>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
      <div className="bg-yellow-950/60 rounded-lg p-4 flex flex-col items-center">
        <Map className="w-6 h-6 mb-2 text-yellow-200" />
        <div className="text-lg font-semibold">3 Shipments</div>
        <div className="text-xs text-yellow-100">In Transit</div>
      </div>
      <div className="bg-yellow-950/60 rounded-lg p-4 flex flex-col items-center">
        <Clock className="w-6 h-6 mb-2 text-yellow-200" />
        <div className="text-lg font-semibold">1 Delayed</div>
        <div className="text-xs text-yellow-100">Expected: 2 days</div>
      </div>
      <div className="bg-yellow-950/60 rounded-lg p-4 flex flex-col items-center">
        <AlertTriangle className="w-6 h-6 mb-2 text-orange-300" />
        <div className="text-lg font-semibold">Next: Concrete</div>
        <div className="text-xs text-yellow-100">ETA: 2 days</div>
      </div>
    </div>
    <div className="w-full h-2 bg-yellow-100 rounded-full overflow-hidden mb-2">
      <div className="h-full bg-yellow-400" style={{ width: '70%' }} />
    </div>
    <div className="text-xs text-yellow-200">Live logistics status. <span className="font-semibold">70%</span> of shipments on schedule.</div>
  </div>
);

export default LogisticsOverview;
