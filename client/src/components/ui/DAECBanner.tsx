import React from 'react';
import { Popover, PopoverTrigger, PopoverContent } from '@/components/ui/popover';



const quickLinks = {
  Design: [
    { label: 'Design Gallery', href: '#design-gallery' },
    { label: 'AI Assistant', href: '#ai-assistant' },
    { label: 'Design Review', href: '#design-review' },
  ],
  Architecture: [
    { label: 'BIM Viewer', href: '#bim-viewer' },
    { label: 'Project Workspace', href: '#project-workspace' },
    { label: 'Compliance', href: '#compliance' },
  ],
  Engineering: [
    { label: 'Analytics', href: '#analytics' },
    { label: 'Material Cost', href: '#material-cost' },
    { label: 'Risk Alerts', href: '#risk-alerts' },
  ],
  Construction: [
    { label: 'Logistics', href: '#logistics' },
    { label: 'Site Safety', href: '#site-safety' },
    { label: 'Vendor Library', href: '#vendor-library' },
  ],
};

const DAECBanner = () => (
  <div className="mb-8 rounded-2xl bg-gradient-to-br from-blue-900/80 via-teal-800/80 to-gray-900/80 p-8 shadow-xl flex flex-col gap-8 border border-blue-900/30">
    <div className="w-full flex flex-col items-center justify-center text-center">
      <h1 className="text-3xl md:text-4xl font-bold text-white mb-2 tracking-tight">
        <span className="bg-gradient-to-r from-synapse-blue via-synapse-teal to-synapse-orange bg-clip-text text-transparent animate-gradient-x">
          Design Synapse
        </span>
        <span className="ml-2">— A Unified DAEC Ecosystem</span>
      </h1>
      <p className="text-lg md:text-xl text-blue-100 max-w-2xl mt-2">
        <span className="font-semibold text-teal-300">AI</span>, <span className="font-semibold text-blue-300">BIM</span>, and artistry converge.<br />
        <span className="text-synapse-orange font-semibold">Transform your workflows. Collaborate without boundaries. Build the future, together.</span>
      </p>
    </div>
    <div className="w-full flex justify-center">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full max-w-2xl">
        {(['Design', 'Architecture', 'Engineering', 'Construction'] as const).map((discipline) => (
          <Popover key={discipline}>
            <PopoverTrigger asChild>
              <button
                className={
                  `w-full px-4 py-3 rounded-lg font-semibold text-base tracking-wide shadow transition focus:outline-none focus:ring-2 ` +
                  (discipline === 'Design' ? 'bg-blue-800/80 text-blue-100 hover:bg-blue-700/90 focus:ring-blue-400' :
                  discipline === 'Architecture' ? 'bg-teal-800/80 text-teal-100 hover:bg-teal-700/90 focus:ring-teal-400' :
                  discipline === 'Engineering' ? 'bg-orange-800/80 text-orange-100 hover:bg-orange-700/90 focus:ring-orange-400' :
                  'bg-gray-800/80 text-gray-100 hover:bg-gray-700/90 focus:ring-gray-400')
                }
              >
                {discipline}
              </button>
            </PopoverTrigger>
            <PopoverContent className="bg-card text-card-foreground w-56">
              <div className="font-bold mb-2 text-lg">{discipline} Shortcuts</div>
              <ul className="space-y-2">
                {quickLinks[discipline].map((item) => (
                  <li key={item.label}>
                    <a href={item.href} className="block px-2 py-1 rounded hover:bg-muted transition-colors text-sm font-medium">
                      {item.label}
                    </a>
                  </li>
                ))}
              </ul>
            </PopoverContent>
          </Popover>
        ))}
      </div>
    </div>
  </div>
);

export default DAECBanner;
