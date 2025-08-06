import React, { useEffect, useRef, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';
import * as THREE from 'three';
import { useDesignPreview } from '../hooks/usedesignpreview';

const DesignPreview = ({ designId, updateTrigger }) => {
    const containerRef = useRef();
    const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
    const { design, loading, error } = useDesignPreview(designId);
    const [viewMode, setViewMode] = useState('3d'); // '3d', 'top', 'front', 'side'

    useEffect(() => {
        const updateDimensions = () => {
            if (containerRef.current) {
                setDimensions({
                    width: containerRef.current.offsetWidth,
                    height: containerRef.current.offsetHeight
                });
            }
        };

        updateDimensions();
        window.addEventListener('resize', updateDimensions);
        return () => window.removeEventListener('resize', updateDimensions);
    }, []);

    const getCameraPosition = () => {
        switch (viewMode) {
            case 'top':
                return [0, 10, 0];
            case 'front':
                return [0, 0, 10];
            case 'side':
                return [10, 0, 0];
            default:
                return [10, 10, 10];
        }
    };

    if (loading) return <div>Loading design preview...</div>;
    if (error) return <div>Error loading design: {error.message}</div>;
    if (!design) return <div>No design data available</div>;

    return (
        <div className="design-preview" ref={containerRef}>
            <div className="preview-controls">
                <button 
                    onClick={() => setViewMode('3d')}
                    className={viewMode === '3d' ? 'active' : ''}>
                    3D View
                </button>
                <button 
                    onClick={() => setViewMode('top')}
                    className={viewMode === 'top' ? 'active' : ''}>
                    Top View
                </button>
                <button 
                    onClick={() => setViewMode('front')}
                    className={viewMode === 'front' ? 'active' : ''}>
                    Front View
                </button>
                <button 
                    onClick={() => setViewMode('side')}
                    className={viewMode === 'side' ? 'active' : ''}>
                    Side View
                </button>
            </div>

            <Canvas
                camera={{ position: getCameraPosition(), fov: 75 }}
                style={{ width: dimensions.width, height: dimensions.height }}
            >
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} />
                
                <DesignModel design={design} />
                <OrbitControls />
                <Environment preset="sunset" />
                <gridHelper args={[20, 20]} />
            </Canvas>

            <div className="design-info">
                <h3>Design Details</h3>
                <p>Area: {design.metrics?.area} sq ft</p>
                <p>Rooms: {design.metrics?.roomCount}</p>
                <p>Style: {design.style}</p>
            </div>
        </div>
    );
};

const DesignModel = ({ design }) => {
    const groupRef = useRef();

    useEffect(() => {
        if (groupRef.current && design.geometry) {
            // Update geometry based on design data
            // This is a simplified example - actual implementation would depend on your data structure
            const geometry = new THREE.BufferGeometry();
            geometry.setAttribute('position', new THREE.Float32BufferAttribute(design.geometry.vertices, 3));
            geometry.setAttribute('normal', new THREE.Float32BufferAttribute(design.geometry.normals, 3));
            geometry.setIndex(design.geometry.indices);
        }
    }, [design]);

    return (
        <group ref={groupRef}>
            {/* Render walls */}
            {design.walls?.map((wall, index) => (
                <Wall key={index} data={wall} />
            ))}
            
            {/* Render floors */}
            {design.floors?.map((floor, index) => (
                <Floor key={index} data={floor} />
            ))}
            
            {/* Render windows and doors */}
            {design.openings?.map((opening, index) => (
                <Opening key={index} data={opening} />
            ))}
        </group>
    );
};

const Wall = ({ data }) => {
    return (
        <mesh position={data.position} rotation={data.rotation}>
            <boxGeometry args={[data.width, data.height, data.thickness]} />
            <meshStandardMaterial color={data.color || "#cccccc"} />
        </mesh>
    );
};

const Floor = ({ data }) => {
    return (
        <mesh position={data.position} rotation={[Math.PI / 2, 0, 0]}>
            <planeGeometry args={[data.width, data.length]} />
            <meshStandardMaterial color={data.color || "#999999"} side={THREE.DoubleSide} />
        </mesh>
    );
};

const Opening = ({ data }) => {
    const isWindow = data.type === 'window';
    
    return (
        <mesh position={data.position} rotation={data.rotation}>
            <boxGeometry args={[data.width, data.height, 0.1]} />
            <meshStandardMaterial 
                color={isWindow ? "#88ccff" : "#553311"}
                transparent={isWindow}
                opacity={isWindow ? 0.4 : 1}
            />
        </mesh>
    );
};

export default DesignPreview;