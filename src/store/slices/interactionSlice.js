import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    // Form fields
    hcpName: '',
    interactionType: 'Meeting',
    date: new Date().toISOString().split('T')[0],
    time: '19:36',
    attendees: '',
    topicsDiscussed: '',

    // Materials and Samples
    materialsShared: [],
    samplesDistributed: [],

    // Sentiment
    sentiment: 'neutral', // 'positive', 'neutral', 'negative'

    // Outcomes and Follow-ups
    outcomes: '',
    followUpActions: '',

    // AI Suggested Follow-ups
    aiSuggestedFollowups: [
        'Schedule follow-up meeting in 2 weeks',
        'Send OncoBoost Phase III PDF',
        'Add Dr. Sharma to advisory board invita list',
    ],

    // Chat messages
    chatMessages: [
        {
            id: 1,
            type: 'system',
            content: 'Log interaction details here (e.g., "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure") or ask for help.',
        },
    ],
    chatInput: '',
};

const interactionSlice = createSlice({
    name: 'interaction',
    initialState,
    reducers: {
        setHcpName: (state, action) => {
            state.hcpName = action.payload;
        },
        setInteractionType: (state, action) => {
            state.interactionType = action.payload;
        },
        setDate: (state, action) => {
            state.date = action.payload;
        },
        setTime: (state, action) => {
            state.time = action.payload;
        },
        setAttendees: (state, action) => {
            state.attendees = action.payload;
        },
        setTopicsDiscussed: (state, action) => {
            state.topicsDiscussed = action.payload;
        },
        addMaterial: (state, action) => {
            // Avoid duplicates
            if (!state.materialsShared.includes(action.payload)) {
                state.materialsShared.push(action.payload);
            }
        },
        removeMaterial: (state, action) => {
            state.materialsShared = state.materialsShared.filter((_, i) => i !== action.payload);
        },
        addSample: (state, action) => {
            // Avoid duplicates
            if (!state.samplesDistributed.includes(action.payload)) {
                state.samplesDistributed.push(action.payload);
            }
        },
        removeSample: (state, action) => {
            state.samplesDistributed = state.samplesDistributed.filter((_, i) => i !== action.payload);
        },
        setSentiment: (state, action) => {
            state.sentiment = action.payload;
        },
        setOutcomes: (state, action) => {
            state.outcomes = action.payload;
        },
        setFollowUpActions: (state, action) => {
            state.followUpActions = action.payload;
        },
        setChatInput: (state, action) => {
            state.chatInput = action.payload;
        },
        addChatMessage: (state, action) => {
            state.chatMessages.push({
                id: state.chatMessages.length + 1,
                ...action.payload,
            });
        },
        resetForm: () => initialState,
    },
});

export const {
    setHcpName,
    setInteractionType,
    setDate,
    setTime,
    setAttendees,
    setTopicsDiscussed,
    addMaterial,
    removeMaterial,
    addSample,
    removeSample,
    setSentiment,
    setOutcomes,
    setFollowUpActions,
    setChatInput,
    addChatMessage,
    resetForm,
} = interactionSlice.actions;

export default interactionSlice.reducer;
