import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Settings, Calendar, Users, Image } from 'lucide-react';

const BIMViewer = () => {
  return (
    <div className="mt-8">
      <Card className="border-0 shadow-lg">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-xl text-synapse-dark">BIM Workspace</CardTitle>
              <CardDescription>Interactive 3D model and project coordination</CardDescription>
            </div>
            <div className="flex space-x-2">
              <Badge variant="outline" className="border-green-200 text-green-700">
                Model Sync: Active
              </Badge>
              <Button size="sm" variant="outline">
                <Settings className="w-4 h-4 mr-2" />
                Configure
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="3d-view" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="3d-view">3D View</TabsTrigger>
              <TabsTrigger value="floor-plans">Floor Plans</TabsTrigger>
              <TabsTrigger value="sections">Sections</TabsTrigger>
              <TabsTrigger value="schedules">Schedules</TabsTrigger>
            </TabsList>
            
            <TabsContent value="3d-view" className="mt-6">
              <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl h-96 flex items-center justify-center relative overflow-hidden">
                {/* Mock 3D Viewer */}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-teal-500/10"></div>
                <div className="text-center z-10">
                  <div className="w-20 h-20 synapse-gradient rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Image className="w-10 h-10 text-white" />
                  </div>
                  <h3 className="text-lg font-semibold text-synapse-dark mb-2">Interactive BIM Viewer</h3>
                  <p className="text-gray-600 mb-4">Load your Revit, ArchiCAD, or other BIM models here</p>
                  <Button className="synapse-gradient text-white border-0">
                    Load Model
                  </Button>
                </div>
                
                {/* Mock viewer controls */}
                <div className="absolute bottom-4 left-4 space-y-2">
                  <Button size="sm" variant="outline" className="bg-white/80 backdrop-blur">
                    Zoom Fit
                  </Button>
                  <Button size="sm" variant="outline" className="bg-white/80 backdrop-blur">
                    Measure
                  </Button>
                  <Button size="sm" variant="outline" className="bg-white/80 backdrop-blur">
                    Section
                  </Button>
                </div>
                
                <div className="absolute bottom-4 right-4">
                  <Button size="sm" className="synapse-gradient text-white">
                    Generate Render
                  </Button>
                </div>
              </div>
              
              {/* Model Information */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Calendar className="w-5 h-5 text-blue-600" />
                    <span className="font-medium text-blue-900">Last Modified</span>
                  </div>
                  <p className="text-blue-700">2 hours ago</p>
                  <p className="text-sm text-blue-600">Structural updates by Sarah Chen</p>
                </div>
                
                <div className="bg-teal-50 p-4 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Users className="w-5 h-5 text-teal-600" />
                    <span className="font-medium text-teal-900">Collaborators</span>
                  </div>
                  <p className="text-teal-700">5 active users</p>
                  <p className="text-sm text-teal-600">Architecture, Structure, MEP teams</p>
                </div>
                
                <div className="bg-orange-50 p-4 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Settings className="w-5 h-5 text-orange-600" />
                    <span className="font-medium text-orange-900">Model Status</span>
                  </div>
                  <p className="text-orange-700">Coordination Complete</p>
                  <p className="text-sm text-orange-600">Ready for rendering</p>
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="floor-plans">
              <div className="bg-gray-50 rounded-xl h-96 flex items-center justify-center">
                <div className="text-center">
                  <h3 className="text-lg font-semibold text-gray-700 mb-2">Floor Plans View</h3>
                  <p className="text-gray-500">2D floor plan layouts and annotations</p>
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="sections">
              <div className="bg-gray-50 rounded-xl h-96 flex items-center justify-center">
                <div className="text-center">
                  <h3 className="text-lg font-semibold text-gray-700 mb-2">Building Sections</h3>
                  <p className="text-gray-500">Cross-sectional views and details</p>
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="schedules">
              <div className="bg-gray-50 rounded-xl h-96 flex items-center justify-center">
                <div className="text-center">
                  <h3 className="text-lg font-semibold text-gray-700 mb-2">Project Schedules</h3>
                  <p className="text-gray-500">Material schedules, quantities, and specifications</p>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};

export default BIMViewer;
