import { useSelector, useDispatch } from 'react-redux';
import { setChatInput, addChatMessage, setHcpName, setInteractionType, setDate, setTime, setAttendees, setTopicsDiscussed, addMaterial, addSample, setSentiment, setOutcomes, setFollowUpActions } from '../../../store/slices/interactionSlice';
import { api } from '../../../services/api';
import { useState } from 'react';
import './AIAssistant.css';

const AIAssistant = () => {
    const dispatch = useDispatch();
    const { chatMessages, chatInput } = useSelector((state) => state.interaction);
    const [isLoading, setIsLoading] = useState(false);

    const handleSendMessage = async () => {
        if (chatInput.trim()) {
            const userMessage = chatInput;
            dispatch(addChatMessage({ type: 'user', content: userMessage }));
            dispatch(setChatInput(''));
            setIsLoading(true);

            try {
                // Prepare conversation history for API
                const conversationHistory = chatMessages.map(msg => ({
                    type: msg.type,
                    content: msg.content
                }));

                // Call LangGraph backend through API
                const response = await api.sendMessage(userMessage, conversationHistory);

                // Add AI response to chat
                dispatch(addChatMessage({
                    type: 'assistant',
                    content: response.message,
                }));

                // Update form fields with extracted data
                if (response.extracted_data) {
                    const data = response.extracted_data;
                    
                    if (data.hcp_name) dispatch(setHcpName(data.hcp_name));
                    if (data.interaction_type) dispatch(setInteractionType(data.interaction_type));
                    if (data.date) dispatch(setDate(data.date));
                    if (data.time) dispatch(setTime(data.time));
                    if (data.attendees) dispatch(setAttendees(data.attendees));
                    if (data.topics_discussed) dispatch(setTopicsDiscussed(data.topics_discussed));
                    if (data.sentiment) dispatch(setSentiment(data.sentiment));
                    if (data.outcomes) dispatch(setOutcomes(data.outcomes));
                    if (data.follow_up_actions) dispatch(setFollowUpActions(data.follow_up_actions));
                    
                    // Handle arrays
                    if (data.materials_shared && Array.isArray(data.materials_shared)) {
                        data.materials_shared.forEach(material => dispatch(addMaterial(material)));
                    }
                    if (data.samples_distributed && Array.isArray(data.samples_distributed)) {
                        data.samples_distributed.forEach(sample => dispatch(addSample(sample)));
                    }
                }

            } catch (error) {
                console.error('Error sending message:', error);
                dispatch(addChatMessage({
                    type: 'assistant',
                    content: 'Sorry, I encountered an error. Please make sure the backend server is running.',
                }));
            } finally {
                setIsLoading(false);
            }
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <div className="ai-assistant">
            <div className="assistant-header">
                <div className="header-icon">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                        <rect x="3" y="6" width="14" height="10" rx="2" stroke="currentColor" strokeWidth="1.5" />
                        <circle cx="7" cy="11" r="1.5" fill="currentColor" />
                        <circle cx="13" cy="11" r="1.5" fill="currentColor" />
                        <path d="M6 4H14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                        <path d="M8 2V4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                        <path d="M12 2V4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                    </svg>
                </div>
                <div className="header-text">
                    <h3 className="header-title">AI Assistant</h3>
                    <p className="header-subtitle">Log interaction via chat</p>
                </div>
            </div>

            <div className="chat-container">
                <div className="messages-area">
                    {chatMessages.map((message) => (
                        <div key={message.id} className={`message ${message.type}`}>
                            <p className="message-content">{message.content}</p>
                        </div>
                    ))}
                </div>

                <div className="chat-input-area">
                    <input
                        type="text"
                        className="chat-input"
                        placeholder="Describe interaction..."
                        value={chatInput}
                        onChange={(e) => dispatch(setChatInput(e.target.value))}
                        onKeyPress={handleKeyPress}
                        disabled={isLoading}
                    />
                    <button className="send-btn" onClick={handleSendMessage} disabled={isLoading}>
                        {isLoading ? (
                            <span className="loading-spinner"></span>
                        ) : (
                            <>
                                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                    <path d="M8 3L8 13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                                    <path d="M4 7L8 3L12 7" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                                Log
                            </>
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default AIAssistant;
