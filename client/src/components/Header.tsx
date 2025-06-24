import React from 'react';
import { Search, User, Settings, Bell } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import ThemeToggle from './ThemeToggle';

const Header = () => {
  return (
    <header className="bg-white dark:bg-gray-900 custom:bg-gradient-to-r custom:from-purple-900 custom:to-indigo-900 border-b border-gray-200 dark:border-gray-700 custom:border-purple-500 px-6 py-4 transition-colors duration-300">
      <div className="flex items-center justify-between">
        {/* Logo and Brand */}
        <div className="flex items-center space-x-4">
          <div className="synapse-gradient w-10 h-10 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-lg">S</span>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-synapse-dark dark:text-white custom:text-white">Design Synapse</h1>
            <p className="text-sm text-gray-500 dark:text-gray-400 custom:text-purple-200">Unified Construction Intelligence</p>
          </div>
        </div>

        {/* Search Bar */}
        <div className="flex-1 max-w-2xl mx-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500 custom:text-purple-300 w-5 h-5" />
            <Input 
              placeholder="Search projects, tools, or ask me anything..."
              className="pl-10 pr-4 py-3 w-full bg-gray-50 dark:bg-gray-800 custom:bg-purple-800/50 border-0 focus:bg-white dark:focus:bg-gray-700 custom:focus:bg-purple-700/70 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 custom:focus:ring-purple-400 transition-all dark:text-white custom:text-white custom:placeholder:text-purple-200"
            />
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-3">
          <Button variant="ghost" size="icon" className="relative dark:text-white custom:text-white">
            <Bell className="w-5 h-5" />
            <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-4 h-4 flex items-center justify-center">3</span>
          </Button>
          <Button variant="ghost" size="icon" className="dark:text-white custom:text-white">
            <Settings className="w-5 h-5" />
          </Button>
          <ThemeToggle />
          <Button variant="ghost" size="icon" className="dark:text-white custom:text-white">
            <User className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;
