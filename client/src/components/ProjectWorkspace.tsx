import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Calendar, Users, Clock } from 'lucide-react';

const ProjectWorkspace = () => {
  const recentProjects = [
    {
      name: 'Eco Office Complex',
      client: 'GreenTech Solutions',
      progress: 75,
      status: 'Rendering',
      lastUpdate: '2 hours ago',
      team: 5,
      deadline: '2024-01-15'
    },
    {
      name: 'Modern Residential Tower',
      client: 'Urban Living Corp',
      progress: 45,
      status: 'Design Phase',
      lastUpdate: '1 day ago',
      team: 8,
      deadline: '2024-02-20'
    },
    {
      name: 'Industrial Warehouse',
      client: 'LogiFlow Industries',
      progress: 90,
      status: 'Final Review',
      lastUpdate: '3 hours ago',
      team: 3,
      deadline: '2024-01-10'
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Rendering': return 'bg-blue-100 text-blue-800';
      case 'Design Phase': return 'bg-yellow-100 text-yellow-800';
      case 'Final Review': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Recent Projects */}
      <div className="lg:col-span-2">
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="text-xl text-synapse-dark">Active Projects</CardTitle>
            <CardDescription>Your current design and construction projects</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentProjects.map((project, index) => (
              <div key={index} className="p-4 border border-gray-100 rounded-xl hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-synapse-dark">{project.name}</h3>
                    <p className="text-sm text-gray-600">{project.client}</p>
                  </div>
                  <Badge className={`${getStatusColor(project.status)} border-0`}>
                    {project.status}
                  </Badge>
                </div>
                
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-sm text-gray-600 mb-1">
                      <span>Progress</span>
                      <span>{project.progress}%</span>
                    </div>
                    <Progress value={project.progress} className="h-2" />
                  </div>
                  
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-1">
                        <Users className="w-4 h-4" />
                        <span>{project.team} members</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Calendar className="w-4 h-4" />
                        <span>{project.deadline}</span>
                      </div>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Clock className="w-4 h-4" />
                      <span>{project.lastUpdate}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
            
            <Button variant="outline" className="w-full mt-4 border-dashed border-2 h-12 text-gray-500 hover:text-synapse-blue hover:border-synapse-blue">
              + Create New Project
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="space-y-6">
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="text-lg text-synapse-dark">Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button className="w-full synapse-gradient text-white border-0 h-12">
              Start New Design
            </Button>
            <Button variant="outline" className="w-full h-12">
              Import BIM Model
            </Button>
            <Button variant="outline" className="w-full h-12">
              Generate BOQ
            </Button>
            <Button variant="outline" className="w-full h-12">
              Schedule Render
            </Button>
          </CardContent>
        </Card>

        <Card className="border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="text-lg text-synapse-dark">AI Assistant</CardTitle>
            <CardDescription>Ready to help with your projects</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="bg-gradient-to-br from-blue-50 to-teal-50 p-4 rounded-xl">
              <div className="w-10 h-10 synapse-gradient rounded-full flex items-center justify-center mb-3">
                <span className="text-white font-bold">AI</span>
              </div>
              <p className="text-sm text-gray-700 mb-3">
                "I can help you optimize your current designs, generate cost estimates, or create new concepts. What would you like to work on?"
              </p>
              <Button size="sm" variant="outline" className="text-xs">
                Ask Assistant
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ProjectWorkspace;
