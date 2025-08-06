import React from 'react';
import { useQuery } from 'react-query';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import {
  Box,
  Grid,
  Heading,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  VStack,
  Spinner,
  Text,
  useToast,
} from '@chakra-ui/react';
import FloorPlanViewer from './viewers/FloorPlanViewer';
import ElevationViewer from './viewers/ElevationViewer';
import SpecificationViewer from './viewers/SpecificationViewer';

const DesignViewer = () => {
  const { designId } = useParams();
  const toast = useToast();

  const { data: design, isLoading, error } = useQuery(
    ['design', designId],
    () => axios.get(`/api/design/${designId}`).then((res) => res.data),
    {
      onError: (err) => {
        toast({
          title: 'Error loading design',
          description: err.message,
          status: 'error',
          duration: 5000,
        });
      },
    }
  );

  if (isLoading) {
    return (
      <Box
        height="100vh"
        width="100%"
        display="flex"
        alignItems="center"
        justifyContent="center"
      >
        <Spinner size="xl" />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={6}>
        <Text color="red.500">Error loading design: {error.message}</Text>
      </Box>
    );
  }

  return (
    <Box p={6}>
      <VStack spacing={6} align="stretch">
        <Heading size="lg">Design Viewer - {designId}</Heading>

        <Tabs variant="enclosed">
          <TabList>
            <Tab>Floor Plans</Tab>
            <Tab>Elevations</Tab>
            <Tab>Specifications</Tab>
          </TabList>

          <TabPanels>
            <TabPanel>
              <FloorPlanViewer data={design.floor_plans} />
            </TabPanel>
            <TabPanel>
              <ElevationViewer data={design.elevations} />
            </TabPanel>
            <TabPanel>
              <SpecificationViewer data={design.specifications} />
            </TabPanel>
          </TabPanels>
        </Tabs>

        <Grid templateColumns="repeat(2, 1fr)" gap={6}>
          {/* Design Metadata */}
          <Box p={4} borderWidth={1} borderRadius="md">
            <Heading size="sm" mb={4}>
              Input Parameters
            </Heading>
            <VStack align="stretch" spacing={2}>
              <Text>
                Area: {design.metadata.input_parameters.area} m²
              </Text>
              <Text>
                Dimensions: {design.metadata.input_parameters.width}m x{' '}
                {design.metadata.input_parameters.length}m
              </Text>
              <Text>
                Style: {design.metadata.input_parameters.style}
              </Text>
            </VStack>
          </Box>

          {/* Generation Info */}
          <Box p={4} borderWidth={1} borderRadius="md">
            <Heading size="sm" mb={4}>
              Generation Details
            </Heading>
            <VStack align="stretch" spacing={2}>
              <Text>
                Generated: {new Date(design.metadata.generation_timestamp).toLocaleString()}
              </Text>
              <Text>
                Model Version: {design.metadata.model_version}
              </Text>
            </VStack>
          </Box>
        </Grid>
      </VStack>
    </Box>
  );
};

export default DesignViewer;
