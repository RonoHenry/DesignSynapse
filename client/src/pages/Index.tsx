import React from 'react';
import { Github } from 'lucide-react';
import Header from '@/components/Header';
import VybeServices from '@/components/VybeServices';
import ProjectWorkspace from '@/components/ProjectWorkspace';
import BIMViewer from '@/components/BIMViewer';
import Vyber from '@/components/Vyber';

const Index = () => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 custom:bg-gradient-to-br custom:from-purple-900 custom:via-indigo-900 custom:to-purple-800 transition-colors duration-300">
      <Header />
      
      <main className="container mx-auto px-6 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-synapse-dark dark:text-white custom:text-white mb-4 transition-colors duration-300">
              Welcome to Design Synapse
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 custom:text-purple-100 max-w-3xl mx-auto transition-colors duration-300">
              The unified platform that integrates AI, BIM, and professional design tools to transform your construction and design workflows. 
              Experience the future of architectural collaboration.
            </p>
          </div>
          
          {/* Stats Banner */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
            <div className="text-center p-6 bg-white dark:bg-gray-800 custom:bg-purple-800/30 rounded-xl shadow-sm border dark:border-gray-700 custom:border-purple-500/30 transition-colors duration-300">
              <div className="text-3xl font-bold text-synapse-blue mb-2">15+</div>
              <div className="text-gray-600 dark:text-gray-300 custom:text-purple-200">Integrated Tools</div>
            </div>
            <div className="text-center p-6 bg-white dark:bg-gray-800 custom:bg-purple-800/30 rounded-xl shadow-sm border dark:border-gray-700 custom:border-purple-500/30 transition-colors duration-300">
              <div className="text-3xl font-bold text-synapse-teal mb-2">200%</div>
              <div className="text-gray-600 dark:text-gray-300 custom:text-purple-200">Faster Workflows</div>
            </div>
            <div className="text-center p-6 bg-white dark:bg-gray-800 custom:bg-purple-800/30 rounded-xl shadow-sm border dark:border-gray-700 custom:border-purple-500/30 transition-colors duration-300">
              <div className="text-3xl font-bold text-synapse-orange mb-2">24/7</div>
              <div className="text-gray-600 dark:text-gray-300 custom:text-purple-200">AI Assistant</div>
            </div>
            <div className="text-center p-6 bg-white dark:bg-gray-800 custom:bg-purple-800/30 rounded-xl shadow-sm border dark:border-gray-700 custom:border-purple-500/30 transition-colors duration-300">
              <div className="text-3xl font-bold text-synapse-blue mb-2">∞</div>
              <div className="text-gray-600 dark:text-gray-300 custom:text-purple-200">Possibilities</div>
            </div>
          </div>
        </div>

        {/* Vybe Services */}
        <VybeServices />
        
        {/* Project Workspace */}
        <ProjectWorkspace />
        
        {/* BIM Viewer */}
        <BIMViewer />
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
