// import VendorProductLibrary from '@/components/ui/VendorProductLibrary';
import StageProduct from '@/components/ui/StageProduct';
import React from 'react';
import DAECBanner from '@/components/ui/DAECBanner';
import SmartProjectInsights from '@/components/ui/SmartProjectInsights';
// LogisticsOverview is now imported in SmartProjectInsights
import { Github } from 'lucide-react';
import Header from '@/components/Header';
import VybeServices from '@/components/VybeServices';
import ProjectWorkspace from '@/components/ProjectWorkspace';
import BIMViewer from '@/components/bim-viewer';
import Vyber from '@/components/Vyber';
import SustainabilityBadges from '@/components/ui/SustainabilityBadges';
import ProjectHealth from '@/components/ui/ProjectHealth';
import DesignGallery from '@/components/ui/DesignGallery';

const Index = () => {
  return (
    <div className="min-h-screen bg-theme transition-colors duration-300">
      <Header />
      <main className="container mx-auto px-6 py-8">
        {/* DAEC Platform Banner (replaces Welcome Section) */}
        <DAECBanner />
        {/* Smart Project Insights (replaces second DAEC banner) */}
        <SmartProjectInsights />
        {/* Stats Banner */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <div className="text-center p-6 bg-card text-card-foreground rounded-xl shadow-sm border border-border transition-colors duration-300">
            <div className="text-3xl font-bold text-synapse-blue mb-2">15+</div>
            <div className="text-foreground">Integrated Tools</div>
          </div>
          <div className="text-center p-6 bg-card text-card-foreground rounded-xl shadow-sm border border-border transition-colors duration-300">
            <div className="text-3xl font-bold text-synapse-teal mb-2">200%</div>
            <div className="text-foreground">Faster Workflows</div>
          </div>
          <div className="text-center p-6 bg-card text-card-foreground rounded-xl shadow-sm border border-border transition-colors duration-300">
            <div className="text-3xl font-bold text-synapse-orange mb-2">24/7</div>
            <div className="text-foreground">AI Assistant</div>
          </div>
          <div className="text-center p-6 bg-card text-card-foreground rounded-xl shadow-sm border border-border transition-colors duration-300">
            <div className="text-3xl font-bold text-synapse-blue mb-2">∞</div>
            <div className="text-foreground">Possibilities</div>
          </div>
        </div>

        {/* Vybe Services */}
        <VybeServices />

        {/* Project Workspace */}
        <ProjectWorkspace />

        {/* BIM Viewer */}
        <BIMViewer />

        {/* Stage Product - Interactive BIM Product Staging */}
        <StageProduct />



        {/* Design Gallery */}
        <DesignGallery />

        {/* Project Health Section */}
        <ProjectHealth />

        {/* Sustainability & Compliance Badges */}
        <SustainabilityBadges />
      </main>

      {/* GitHub Link - Bottom Left */}
      <div className="fixed bottom-6 left-6 z-50">
        <a
          href="https://github.com/RonoHenry/DesignSynapse"
          target="_blank"
          rel="noopener noreferrer"
          className="group flex items-center space-x-3 bg-white/90 dark:bg-gray-800/90 custom:bg-purple-800/90 backdrop-blur-sm border border-gray-200 dark:border-gray-700 custom:border-purple-500/30 rounded-2xl px-4 py-3 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
        >
          <div className="synapse-gradient w-10 h-10 rounded-xl flex items-center justify-center">
            <Github className="w-5 h-5 text-white" />
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-semibold text-gray-800 dark:text-white custom:text-white">
              Rono
            </span>
            <span className="text-xs text-gray-500 dark:text-gray-400 custom:text-purple-200 group-hover:text-synapse-blue dark:group-hover:text-synapse-teal custom:group-hover:text-purple-300 transition-colors">
              View Source
            </span>
          </div>
        </a>
      </div>

      {/* Vyber Chatbot */}
      <Vyber />
    </div>
  );
};

export default Index;
