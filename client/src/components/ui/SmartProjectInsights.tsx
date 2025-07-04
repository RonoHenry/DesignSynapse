        {/* Logistics Coordination Analytics */}
        <Popover>
          <PopoverTrigger asChild>
            <button className="flex items-center gap-2 px-5 py-3 rounded-xl bg-yellow-900/80 hover:bg-yellow-800/90 text-yellow-100 font-semibold shadow transition focus:outline-none focus:ring-2 focus:ring-yellow-400">
              <Truck className="w-5 h-5 text-yellow-300" />
              Logistics Coordination
            </button>
          </PopoverTrigger>
          <PopoverContent className="bg-card text-card-foreground w-80">
            <div className="flex items-center gap-2 mb-2">
              <Truck className="w-5 h-5 text-yellow-400" />
              <span className="font-bold text-yellow-700">Logistics Status</span>
            </div>
            <div className="text-sm mb-2">Next delivery: <span className="font-semibold text-yellow-600">Concrete - 2 days</span></div>
            <div className="w-full h-2 bg-yellow-100 rounded-full overflow-hidden mb-2">
              <div className="h-full bg-yellow-400" style={{ width: '70%' }} />
            </div>
            <div className="text-xs text-gray-500 mb-1">3 shipments in transit | 1 delayed</div>
            <button className="mt-2 px-3 py-1 bg-yellow-700 text-white rounded hover:bg-yellow-800 text-xs font-semibold transition">View Logistics</button>
          </PopoverContent>
        </Popover>
import React from 'react';
import { AlertTriangle, TrendingUp, Zap, CheckCircle, BarChart2, LineChart, Leaf, DollarSign, Truck, CloudRain, HardHat, Package } from 'lucide-react';
import VendorProductLibrary from '@/components/ui/VendorProductLibrary';
        {/* Vendor Product Library Popover */}
        <Popover>
          <PopoverTrigger asChild>
            <button className="flex items-center gap-2 px-5 py-3 rounded-xl bg-indigo-900/80 hover:bg-indigo-800/90 text-indigo-100 font-semibold shadow transition focus:outline-none focus:ring-2 focus:ring-indigo-400">
              <Package className="w-5 h-5 text-indigo-300" />
              Vendor Product Library
            </button>
          </PopoverTrigger>
          <PopoverContent className="bg-card text-card-foreground w-96 max-w-full">
            <div className="font-bold mb-2 text-lg flex items-center gap-2">
              <Package className="w-5 h-5 text-indigo-400" />
              Vendor Product Library
            </div>
            <div className="mb-2 text-sm text-muted-foreground">Browse and stage products from trusted vendors. Plug items directly into your BIM workflow.</div>
            <div className="flex gap-2 mb-4">
              <button className="px-3 py-1 rounded bg-indigo-700 text-white text-xs font-semibold hover:bg-indigo-800 transition">Vendors</button>
              <button className="px-3 py-1 rounded bg-indigo-700 text-white text-xs font-semibold hover:bg-indigo-800 transition">Categories</button>
              <button className="px-3 py-1 rounded bg-indigo-700 text-white text-xs font-semibold hover:bg-indigo-800 transition">All Products</button>
            </div>
            <div className="flex gap-2 mb-4">
              <button className="px-3 py-1 rounded bg-indigo-700 text-white text-xs font-semibold hover:bg-indigo-800 transition">Vendors</button>
              <button className="px-3 py-1 rounded bg-indigo-700 text-white text-xs font-semibold hover:bg-indigo-800 transition">Categories</button>
              <button className="px-3 py-1 rounded bg-indigo-700 text-white text-xs font-semibold hover:bg-indigo-800 transition">All Products</button>
            </div>
            <div className="max-h-72 overflow-y-auto">
              <VendorProductLibrary />
            </div>
          </PopoverContent>
        </Popover>
import { Popover, PopoverTrigger, PopoverContent } from '@/components/ui/popover';
import LogisticsOverview from '@/components/ui/LogisticsOverview';


const SmartProjectInsights = () => (
  <div className="mb-8 rounded-2xl bg-gradient-to-br from-blue-900/80 via-teal-800/80 to-gray-900/80 p-8 shadow-xl flex flex-col md:flex-row items-center justify-between gap-6 border border-blue-900/30">
    <div className="w-full">
      <h2 className="text-2xl md:text-3xl font-bold text-white mb-2 tracking-tight flex items-center gap-2">
        <Zap className="w-7 h-7 text-yellow-300 animate-pulse" />
        Analytic Insights
      </h2>

      {/* Logistics Overview Section */}
      <LogisticsOverview />

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8 w-full">
        {/* Weather Impact Analytics */}
        <Popover>
          <PopoverTrigger asChild>
            <button className="flex items-center gap-2 px-5 py-3 rounded-xl bg-sky-900/80 hover:bg-sky-800/90 text-sky-100 font-semibold shadow transition focus:outline-none focus:ring-2 focus:ring-sky-400">
              <CloudRain className="w-5 h-5 text-sky-300" />
              Weather Impact
            </button>
          </PopoverTrigger>
          <PopoverContent className="bg-card text-card-foreground w-80">
            <div className="flex items-center gap-2 mb-2">
              <CloudRain className="w-5 h-5 text-sky-400" />
              <span className="font-bold text-sky-700">Weather Risk</span>
            </div>
            <div className="text-sm mb-2">Rain forecasted in <span className="font-semibold text-sky-600">2 days</span>. Site work may be delayed.</div>
            <div className="w-full h-2 bg-sky-100 rounded-full overflow-hidden mb-2">
              <div className="h-full bg-sky-400" style={{ width: '40%' }} />
            </div>
            <div className="text-xs text-gray-500 mb-1">Monitor for schedule changes</div>
            <button className="mt-2 px-3 py-1 bg-sky-700 text-white rounded hover:bg-sky-800 text-xs font-semibold transition">View Weather</button>
          </PopoverContent>
        </Popover>

        {/* Site Safety Analytics */}
        <Popover>
          <PopoverTrigger asChild>
            <button className="flex items-center gap-2 px-5 py-3 rounded-xl bg-red-900/80 hover:bg-red-800/90 text-red-100 font-semibold shadow transition focus:outline-none focus:ring-2 focus:ring-red-400">
              <HardHat className="w-5 h-5 text-red-300" />
              Site Safety
            </button>
          </PopoverTrigger>
          <PopoverContent className="bg-card text-card-foreground w-80">
            <div className="flex items-center gap-2 mb-2">
              <HardHat className="w-5 h-5 text-red-400" />
              <span className="font-bold text-red-700">Safety Status</span>
            </div>
            <div className="text-sm mb-2">No incidents reported this week. <span className="font-semibold text-red-600">Safety score: 98%</span></div>
            <div className="w-full h-2 bg-red-100 rounded-full overflow-hidden mb-2">
              <div className="h-full bg-red-400" style={{ width: '98%' }} />
            </div>
            <div className="text-xs text-gray-500 mb-1">Compliant with all protocols</div>
            <button className="mt-2 px-3 py-1 bg-red-700 text-white rounded hover:bg-red-800 text-xs font-semibold transition">View Safety</button>
          </PopoverContent>
        </Popover>
        {/* Supplier Reliability Analytics */}
        <Popover>
          <PopoverTrigger asChild>
            <button className="flex items-center gap-2 px-5 py-3 rounded-xl bg-purple-900/80 hover:bg-purple-800/90 text-purple-100 font-semibold shadow transition focus:outline-none focus:ring-2 focus:ring-purple-400">
              <Truck className="w-5 h-5 text-purple-300" />
              Supplier Reliability
            </button>
          </PopoverTrigger>
          <PopoverContent className="bg-card text-card-foreground w-80">
            <div className="flex items-center gap-2 mb-2">
              <Truck className="w-5 h-5 text-purple-400" />
              <span className="font-bold text-purple-700">Supplier Score</span>
            </div>
            <div className="text-sm mb-2">Top supplier: <span className="font-semibold text-purple-600">BuildFast Ltd.</span></div>
            <div className="w-full h-2 bg-purple-100 rounded-full overflow-hidden mb-2">
              <div className="h-full bg-purple-500" style={{ width: '82%' }} />
            </div>
            <div className="text-xs text-gray-500 mb-1">On-time delivery: 96% | Avg. lead time: 4 days</div>
            <button className="mt-2 px-3 py-1 bg-purple-700 text-white rounded hover:bg-purple-800 text-xs font-semibold transition">View Suppliers</button>
          </PopoverContent>
        </Popover>
        {/* Material Cost Analytics */}
        <Popover>
          <PopoverTrigger asChild>
            <button className="flex items-center gap-2 px-5 py-3 rounded-xl bg-blue-900/80 hover:bg-blue-800/90 text-blue-100 font-semibold shadow transition focus:outline-none focus:ring-2 focus:ring-blue-400">
              <DollarSign className="w-5 h-5 text-blue-300" />
              Material Cost
            </button>
          </PopoverTrigger>
          <PopoverContent className="bg-card text-card-foreground w-80">
            <div className="flex items-center gap-2 mb-2">
              <BarChart2 className="w-5 h-5 text-blue-400" />
              <span className="font-bold text-blue-700">Material Cost Trends</span>
            </div>
            <div className="text-sm mb-2">Current market value for <span className="font-semibold text-blue-600">Steel</span>: <span className="font-bold">$1,200/ton</span></div>
            <div className="w-full h-20 bg-blue-50 rounded-lg flex items-end gap-1 mb-2 p-2">
              {/* Placeholder for a mini bar chart */}
              <div className="w-3 h-8 bg-blue-300 rounded"></div>
              <div className="w-3 h-12 bg-blue-400 rounded"></div>
              <div className="w-3 h-6 bg-blue-500 rounded"></div>
              <div className="w-3 h-10 bg-blue-600 rounded"></div>
              <div className="w-3 h-7 bg-blue-400 rounded"></div>
            </div>
            <div className="text-xs text-gray-500 mb-1">Last 6 months trend</div>
            <div className="text-xs text-blue-700 font-semibold">Your project: $1,180/ton (below market)</div>
            <button className="mt-2 px-3 py-1 bg-blue-700 text-white rounded hover:bg-blue-800 text-xs font-semibold transition">See All Materials</button>
          </PopoverContent>
        </Popover>
        {/* Risk Alert */}
        <Popover>
          <PopoverTrigger asChild>
            <button className="flex items-center gap-2 px-5 py-3 rounded-xl bg-orange-900/80 hover:bg-orange-800/90 text-orange-100 font-semibold shadow transition focus:outline-none focus:ring-2 focus:ring-orange-400">
              <AlertTriangle className="w-5 h-5 text-orange-300" />
              Risk Alert
            </button>
          </PopoverTrigger>
          <PopoverContent className="bg-card text-card-foreground">
            <div className="flex items-center gap-2 mb-2">
              <BarChart2 className="w-5 h-5 text-orange-400" />
              <span className="font-bold text-orange-700">Potential Delay</span>
            </div>
            <div className="text-sm mb-2">Schedule delay detected in MEP coordination. <span className="font-semibold text-orange-600">3 days behind</span>.</div>
            <div className="w-full h-2 bg-orange-100 rounded-full overflow-hidden mb-2">
              <div className="h-full bg-orange-400" style={{ width: '60%' }} />
            </div>
            <div className="text-xs text-gray-500">Critical path: HVAC, Electrical</div>
          </PopoverContent>
        </Popover>

        {/* Cost Insight */}
        <Popover>
          <PopoverTrigger asChild>
            <button className="flex items-center gap-2 px-5 py-3 rounded-xl bg-teal-900/80 hover:bg-teal-800/90 text-teal-100 font-semibold shadow transition focus:outline-none focus:ring-2 focus:ring-teal-400">
              <TrendingUp className="w-5 h-5 text-teal-300" />
              Cost Insight
            </button>
          </PopoverTrigger>
          <PopoverContent className="bg-card text-card-foreground">
            <div className="flex items-center gap-2 mb-2">
              <LineChart className="w-5 h-5 text-teal-400" />
              <span className="font-bold text-teal-700">Cost Overrun</span>
            </div>
            <div className="text-sm mb-2">Projected cost overrun of <span className="font-semibold text-teal-600">3.2%</span> based on recent design changes.</div>
            <div className="w-full h-2 bg-teal-100 rounded-full overflow-hidden mb-2">
              <div className="h-full bg-teal-400" style={{ width: '32%' }} />
            </div>
            <div className="text-xs text-gray-500">Main driver: Material price increase</div>
          </PopoverContent>
        </Popover>

        {/* Sustainability */}
        <Popover>
          <PopoverTrigger asChild>
            <button className="flex items-center gap-2 px-5 py-3 rounded-xl bg-green-900/80 hover:bg-green-800/90 text-green-100 font-semibold shadow transition focus:outline-none focus:ring-2 focus:ring-green-400">
              <CheckCircle className="w-5 h-5 text-green-300" />
              Sustainability
            </button>
          </PopoverTrigger>
          <PopoverContent className="bg-card text-card-foreground">
            <div className="flex items-center gap-2 mb-2">
              <Leaf className="w-5 h-5 text-green-400" />
              <span className="font-bold text-green-700">LEED Gold</span>
            </div>
            <div className="text-sm mb-2">Model meets <span className="font-semibold text-green-600">LEED Gold</span> requirements.</div>
            <div className="w-full h-2 bg-green-100 rounded-full overflow-hidden mb-2">
              <div className="h-full bg-green-400" style={{ width: '90%' }} />
            </div>
            <div className="text-xs text-gray-500">Energy use: 18% below baseline</div>
          </PopoverContent>
        </Popover>

        {/* Vendor Product Library Popover (moved after Sustainability) */}
        <Popover>
          <PopoverTrigger asChild>
            <button className="flex items-center gap-2 px-5 py-3 rounded-xl bg-indigo-900/80 hover:bg-indigo-800/90 text-indigo-100 font-semibold shadow transition focus:outline-none focus:ring-2 focus:ring-indigo-400">
              <Package className="w-5 h-5 text-indigo-300" />
              Vendor Product Library
            </button>
          </PopoverTrigger>
          <PopoverContent className="bg-card text-card-foreground w-96 max-w-full">
            <div className="font-bold mb-2 text-lg flex items-center gap-2">
              <Package className="w-5 h-5 text-indigo-400" />
              Vendor Product Library
            </div>
            <div className="mb-2 text-sm text-muted-foreground">Browse and stage products from trusted vendors. Plug items directly into your BIM workflow.</div>
            <div className="max-h-72 overflow-y-auto">
              <VendorProductLibrary />
            </div>
          </PopoverContent>
        </Popover>
      </div>
    </div>
  </div>
);

export default SmartProjectInsights;
