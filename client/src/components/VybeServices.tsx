import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowUp, Edit, Image, Calendar } from 'lucide-react';

const VybeServices = () => {
  const services = [
    {
      name: 'Design',
      description: 'Conceptual design and iteration with AI-powered creativity',
      icon: Edit,
      color: 'synapse-gradient',
      stats: '12 Active Projects',
      action: 'Start Designing'
    },
    {
      name: 'Draft',
      description: 'Technical drawings and BIM models with precision',
      icon: Calendar,
      color: 'synapse-gradient',
      stats: '8 Models in Progress',
      action: 'Open Drafting'
    },
    {
      name: 'Render',
      description: 'Photorealistic visuals and motion graphics',
      icon: Image,
      color: 'synapse-gradient-orange',
      stats: '15 Renders Complete',
      action: 'Create Render'
    },
    {
      name: 'Quote',
      description: 'Instant BOQ and cost estimates with accuracy',
      icon: ArrowUp,
      color: 'synapse-gradient',
      stats: '$2.4M Quoted This Month',
      action: 'Generate Quote'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {services.map((service, index) => (
        <Card key={index} className="hover-lift border-0 shadow-lg overflow-hidden group">
          <CardHeader className="pb-3">
            <div className={`w-12 h-12 ${service.color} rounded-xl flex items-center justify-center mb-3 group-hover:scale-110 transition-transform duration-300`}>
              <service.icon className="w-6 h-6 text-white" />
            </div>
            <CardTitle className="text-lg text-synapse-dark">{service.name}</CardTitle>
            <CardDescription className="text-sm text-gray-600">
              {service.description}
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="space-y-3">
              <div className="text-sm text-gray-500">{service.stats}</div>
              <Button className="w-full synapse-gradient hover:opacity-90 text-white border-0">
                {service.action}
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default VybeServices;
