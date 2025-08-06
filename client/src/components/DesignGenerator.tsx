import React, { useState } from 'react';
import { useQuery, useMutation } from 'react-query';
import axios from 'axios';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  NumberInput,
  NumberInputField,
  Select,
  Stack,
  Switch,
  Text,
  VStack,
  useToast,
} from '@chakra-ui/react';

const DesignGenerator = () => {
  const toast = useToast();
  const [designParams, setDesignParams] = useState({
    area: 100,
    width: 10,
    length: 10,
    height: 3,
    rooms: {
      bedrooms: 2,
      bathrooms: 1,
      living_rooms: 1,
      kitchens: 1,
    },
    style: 'modern',
    needs_garage: false,
    needs_basement: false,
    sustainable_design: false,
  });

  const generateDesign = useMutation(
    (params) => axios.post('/api/design/generate', params),
    {
      onSuccess: (response) => {
        const designId = response.data.design_id;
        toast({
          title: 'Design Generated',
          description: `Design ID: ${designId}`,
          status: 'success',
          duration: 5000,
        });
        // Navigate to design viewer
        navigate(`/design/${designId}`);
      },
      onError: (error) => {
        toast({
          title: 'Error',
          description: error.message,
          status: 'error',
          duration: 5000,
        });
      },
    }
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    generateDesign.mutate(designParams);
  };

  const handleInputChange = (field, value) => {
    setDesignParams((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleRoomChange = (roomType, value) => {
    setDesignParams((prev) => ({
      ...prev,
      rooms: {
        ...prev.rooms,
        [roomType]: parseInt(value),
      },
    }));
  };

  return (
    <Box p={6} maxW="container.md" mx="auto">
      <form onSubmit={handleSubmit}>
        <VStack spacing={6} align="stretch">
          <Text fontSize="2xl" fontWeight="bold">
            Generate New Design
          </Text>

          {/* Basic Dimensions */}
          <Stack direction={['column', 'row']} spacing={4}>
            <FormControl>
              <FormLabel>Area (m²)</FormLabel>
              <NumberInput
                min={20}
                max={1000}
                value={designParams.area}
                onChange={(value) => handleInputChange('area', parseFloat(value))}
              >
                <NumberInputField />
              </NumberInput>
            </FormControl>

            <FormControl>
              <FormLabel>Width (m)</FormLabel>
              <NumberInput
                min={3}
                max={100}
                value={designParams.width}
                onChange={(value) => handleInputChange('width', parseFloat(value))}
              >
                <NumberInputField />
              </NumberInput>
            </FormControl>

            <FormControl>
              <FormLabel>Length (m)</FormLabel>
              <NumberInput
                min={3}
                max={100}
                value={designParams.length}
                onChange={(value) => handleInputChange('length', parseFloat(value))}
              >
                <NumberInputField />
              </NumberInput>
            </FormControl>
          </Stack>

          {/* Room Configuration */}
          <Stack direction={['column', 'row']} spacing={4}>
            <FormControl>
              <FormLabel>Bedrooms</FormLabel>
              <NumberInput
                min={0}
                max={10}
                value={designParams.rooms.bedrooms}
                onChange={(value) => handleRoomChange('bedrooms', value)}
              >
                <NumberInputField />
              </NumberInput>
            </FormControl>

            <FormControl>
              <FormLabel>Bathrooms</FormLabel>
              <NumberInput
                min={0}
                max={10}
                value={designParams.rooms.bathrooms}
                onChange={(value) => handleRoomChange('bathrooms', value)}
              >
                <NumberInputField />
              </NumberInput>
            </FormControl>

            <FormControl>
              <FormLabel>Living Rooms</FormLabel>
              <NumberInput
                min={0}
                max={5}
                value={designParams.rooms.living_rooms}
                onChange={(value) => handleRoomChange('living_rooms', value)}
              >
                <NumberInputField />
              </NumberInput>
            </FormControl>
          </Stack>

          {/* Style Selection */}
          <FormControl>
            <FormLabel>Style</FormLabel>
            <Select
              value={designParams.style}
              onChange={(e) => handleInputChange('style', e.target.value)}
            >
              <option value="modern">Modern</option>
              <option value="traditional">Traditional</option>
              <option value="minimalist">Minimalist</option>
              <option value="industrial">Industrial</option>
            </Select>
          </FormControl>

          {/* Additional Features */}
          <Stack direction={['column', 'row']} spacing={4}>
            <FormControl display="flex" alignItems="center">
              <FormLabel mb="0">Garage</FormLabel>
              <Switch
                isChecked={designParams.needs_garage}
                onChange={(e) =>
                  handleInputChange('needs_garage', e.target.checked)
                }
              />
            </FormControl>

            <FormControl display="flex" alignItems="center">
              <FormLabel mb="0">Basement</FormLabel>
              <Switch
                isChecked={designParams.needs_basement}
                onChange={(e) =>
                  handleInputChange('needs_basement', e.target.checked)
                }
              />
            </FormControl>

            <FormControl display="flex" alignItems="center">
              <FormLabel mb="0">Sustainable Design</FormLabel>
              <Switch
                isChecked={designParams.sustainable_design}
                onChange={(e) =>
                  handleInputChange('sustainable_design', e.target.checked)
                }
              />
            </FormControl>
          </Stack>

          <Button
            type="submit"
            colorScheme="blue"
            size="lg"
            isLoading={generateDesign.isLoading}
          >
            Generate Design
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default DesignGenerator;
