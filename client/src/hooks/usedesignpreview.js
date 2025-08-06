import { useState, useEffect, useCallback } from 'react';
import api from '../services/api';

export const useDesignPreview = (designId, options = {}) => {
    const [design, setDesign] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [socket, setSocket] = useState(null);

    const { 
        autoUpdate = true,
        updateInterval = 1000,
        enableRealtime = true 
    } = options;

    // Fetch design data
    const fetchDesign = useCallback(async () => {
        try {
            const response = await api.get(`/designs/${designId}`);
            setDesign(response.data);
            setError(null);
        } catch (err) {
            setError(err);
            console.error('Error fetching design:', err);
        } finally {
            setLoading(false);
        }
    }, [designId]);

    // Initialize WebSocket connection for real-time updates
    useEffect(() => {
        if (!enableRealtime) return;

        const wsUrl = `${process.env.REACT_APP_WS_URL}/designs/${designId}`;
        const newSocket = new WebSocket(wsUrl);

        newSocket.onmessage = (event) => {
            const update = JSON.parse(event.data);
            setDesign(prevDesign => ({
                ...prevDesign,
                ...update
            }));
        };

        newSocket.onerror = (error) => {
            console.error('WebSocket error:', error);
            setError(error);
        };

        setSocket(newSocket);

        return () => {
            if (newSocket) {
                newSocket.close();
            }
        };
    }, [designId, enableRealtime]);

    // Set up polling updates if WebSocket isn't available
    useEffect(() => {
        if (!autoUpdate || enableRealtime) return;

        const intervalId = setInterval(fetchDesign, updateInterval);

        return () => clearInterval(intervalId);
    }, [autoUpdate, enableRealtime, fetchDesign, updateInterval]);

    // Initial fetch
    useEffect(() => {
        fetchDesign();
    }, [fetchDesign]);

    // Function to manually trigger an update
    const refresh = useCallback(() => {
        setLoading(true);
        fetchDesign();
    }, [fetchDesign]);

    // Function to update specific design properties
    const updateDesign = useCallback(async (updates) => {
        try {
            const response = await api.patch(`/designs/${designId}`, updates);
            setDesign(response.data);
            return response.data;
        } catch (err) {
            setError(err);
            throw err;
        }
    }, [designId]);

    // Function to validate design changes before applying
    const validateChanges = useCallback(async (changes) => {
        try {
            const response = await api.post(`/designs/${designId}/validate`, changes);
            return response.data;
        } catch (err) {
            setError(err);
            throw err;
        }
    }, [designId]);

    return {
        design,
        loading,
        error,
        refresh,
        updateDesign,
        validateChanges,
        isRealtime: !!socket && socket.readyState === WebSocket.OPEN
    };
};