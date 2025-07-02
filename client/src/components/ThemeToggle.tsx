import React from 'react';
import { Moon, Sun, Palette } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useTheme } from '@/contexts/ThemeContext';

const ThemeToggle = () => {
  const { theme, setTheme } = useTheme();

  const getThemeIcon = () => {
    switch (theme) {
      case 'dark':
        return <Moon className="w-5 h-5" />;
      case 'light':
      default:
        return <Sun className="w-5 h-5" />;
    }
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" className="relative">
          {getThemeIcon()}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-48">
        <DropdownMenuItem
          onClick={() => setTheme('light')}
          className="flex items-center space-x-2 cursor-pointer"
        >
          <Sun className="w-4 h-4" />
          <span>Light Mode</span>
        </DropdownMenuItem>
        <DropdownMenuItem
          onClick={() => setTheme('dark')}
          className="flex items-center space-x-2 cursor-pointer"
        >
          <Moon className="w-4 h-4" />
          <span>Dark Mode</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};

export default ThemeToggle;
