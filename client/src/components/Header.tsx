import React from 'react';
import { Search, User, Settings, Bell } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import ThemeToggle from './ThemeToggle';

const Header = () => {
  return (
    <header className="bg-theme border-b border-border px-6 py-4 transition-colors duration-300">
      <div className="flex items-center justify-between">
        {/* Logo and Brand */}
        <div className="flex items-center space-x-4">
          <div className="synapse-gradient w-10 h-10 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-lg">S</span>
          </div>
          <div>
            <h1 className="text-2xl font-bold heading">Design Synapse</h1>
            <p className="text-sm text-foreground">Unified Construction Intelligence</p>
          </div>
        </div>

        {/* Search Bar */}
        <div className="flex-1 max-w-2xl mx-8">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-5 h-5" />
            <Input 
              placeholder="Search projects, tools, or ask me anything..."
              className="pl-10 pr-4 py-3 w-full bg-background border-0 focus:bg-card focus:ring-2 focus:ring-primary transition-all text-foreground placeholder:text-muted-foreground"
            />
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-3">
          <Button variant="ghost" size="icon" className="relative text-foreground">
            <Bell className="w-5 h-5" />
            <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-4 h-4 flex items-center justify-center">3</span>
          </Button>
          <Button variant="ghost" size="icon" className="text-foreground">
            <Settings className="w-5 h-5" />
          </Button>
          <ThemeToggle />
          <Button variant="ghost" size="icon" className="text-foreground">
            <User className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;
