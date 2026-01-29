const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
    // Chat endpoints
    sendMessage: async (message, conversationHistory) => {
        const response = await fetch(`${API_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message,
                conversation_history: conversationHistory,
            }),
        });
        
        if (!response.ok) {
            throw new Error('Failed to send message');
        }
        
        return response.json();
    },

    // HCP endpoints
    searchHCPs: async (query) => {
        const response = await fetch(`${API_URL}/api/hcps/search?query=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error('Failed to search HCPs');
        }
        
        return response.json();
    },

    createHCP: async (hcpData) => {
        const response = await fetch(`${API_URL}/api/hcps`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(hcpData),
        });
        
        if (!response.ok) {
            throw new Error('Failed to create HCP');
        }
        
        return response.json();
    },

    // Interaction endpoints
    createInteraction: async (interactionData) => {
        const response = await fetch(`${API_URL}/api/interactions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(interactionData),
        });
        
        if (!response.ok) {
            throw new Error('Failed to create interaction');
        }
        
        return response.json();
    },

    getInteractions: async () => {
        const response = await fetch(`${API_URL}/api/interactions`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch interactions');
        }
        
        return response.json();
    },

    getInteraction: async (id) => {
        const response = await fetch(`${API_URL}/api/interactions/${id}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch interaction');
        }
        
        return response.json();
    },

    // Health check
    healthCheck: async () => {
        const response = await fetch(`${API_URL}/api/health`);
        
        if (!response.ok) {
            throw new Error('API is not healthy');
        }
        
        return response.json();
    },
};
