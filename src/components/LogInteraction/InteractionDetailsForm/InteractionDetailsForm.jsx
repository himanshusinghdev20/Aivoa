import { useSelector, useDispatch } from 'react-redux';
import {
    setHcpName,
    setInteractionType,
    setDate,
    setTime,
    setAttendees,
    setTopicsDiscussed,
    setSentiment,
    setOutcomes,
    setFollowUpActions,
} from '../../../store/slices/interactionSlice';
import SentimentSelector from './SentimentSelector';
import MaterialsSection from './MaterialsSection';
import SamplesSection from './SamplesSection';
import './InteractionDetailsForm.css';

const InteractionDetailsForm = () => {
    const dispatch = useDispatch();
    const {
        hcpName,
        interactionType,
        date,
        time,
        attendees,
        topicsDiscussed,
        outcomes,
        followUpActions,
        aiSuggestedFollowups,
    } = useSelector((state) => state.interaction);

    const interactionTypes = ['Meeting', 'Phone Call', 'Email', 'Video Call', 'Conference', 'Other'];

    return (
        <div className="interaction-details-form">
            <div className="form-header">
                <h2 className="form-title">Interaction Details</h2>
            </div>

            <div className="form-body">
                {/* HCP Name and Interaction Type Row */}
                <div className="form-row two-columns">
                    <div className="form-group">
                        <label className="form-label">HCP Name</label>
                        <input
                            type="text"
                            className="form-input"
                            placeholder="Search or select HCP..."
                            value={hcpName}
                            onChange={(e) => dispatch(setHcpName(e.target.value))}
                        />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Interaction Type</label>
                        <div className="select-wrapper">
                            <select
                                className="form-select"
                                value={interactionType}
                                onChange={(e) => dispatch(setInteractionType(e.target.value))}
                            >
                                {interactionTypes.map((type) => (
                                    <option key={type} value={type}>
                                        {type}
                                    </option>
                                ))}
                            </select>
                            <span className="select-arrow">
                                <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                                    <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                                </svg>
                            </span>
                        </div>
                    </div>
                </div>

                {/* Date and Time Row */}
                <div className="form-row two-columns">
                    <div className="form-group">
                        <label className="form-label">Date</label>
                        <div className="input-with-icon">
                            <input
                                type="date"
                                className="form-input"
                                value={date}
                                onChange={(e) => dispatch(setDate(e.target.value))}
                            />
                            <span className="input-icon">
                                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                    <rect x="2" y="3" width="12" height="11" rx="2" stroke="currentColor" strokeWidth="1.5" />
                                    <path d="M2 6H14" stroke="currentColor" strokeWidth="1.5" />
                                    <path d="M5 1V3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                                    <path d="M11 1V3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                                </svg>
                            </span>
                        </div>
                    </div>
                    <div className="form-group">
                        <label className="form-label">Time</label>
                        <div className="input-with-icon">
                            <input
                                type="time"
                                className="form-input"
                                value={time}
                                onChange={(e) => dispatch(setTime(e.target.value))}
                            />
                            <span className="input-icon">
                                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                    <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="1.5" />
                                    <path d="M8 5V8L10 10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                                </svg>
                            </span>
                        </div>
                    </div>
                </div>

                {/* Attendees */}
                <div className="form-group">
                    <label className="form-label">Attendees</label>
                    <input
                        type="text"
                        className="form-input"
                        placeholder="Enter names or search..."
                        value={attendees}
                        onChange={(e) => dispatch(setAttendees(e.target.value))}
                    />
                </div>

                {/* Topics Discussed */}
                <div className="form-group">
                    <label className="form-label">Topics Discussed</label>
                    <div className="textarea-wrapper">
                        <textarea
                            className="form-textarea"
                            placeholder="Enter key discussion points..."
                            rows={3}
                            value={topicsDiscussed}
                            onChange={(e) => dispatch(setTopicsDiscussed(e.target.value))}
                        />
                        <span className="textarea-icon mic-icon">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                <path d="M8 1C6.89543 1 6 1.89543 6 3V8C6 9.10457 6.89543 10 8 10C9.10457 10 10 9.10457 10 8V3C10 1.89543 9.10457 1 8 1Z" stroke="currentColor" strokeWidth="1.5" />
                                <path d="M4 7V8C4 10.2091 5.79086 12 8 12C10.2091 12 12 10.2091 12 8V7" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                                <path d="M8 12V15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                            </svg>
                        </span>
                    </div>
                    <button className="voice-note-btn">
                        <span className="sparkle-icon">✨</span>
                        Summarize from Voice Note (Requires Consent)
                    </button>
                </div>

                {/* Materials Shared / Samples Distributed */}
                <div className="form-group">
                    <label className="form-label section-label">Materials Shared / Samples Distributed</label>
                    <MaterialsSection />
                    <SamplesSection />
                </div>

                {/* Sentiment */}
                <div className="form-group">
                    <label className="form-label">Observed/Inferred HCP Sentiment</label>
                    <SentimentSelector />
                </div>

                {/* Outcomes */}
                <div className="form-group">
                    <label className="form-label">Outcomes</label>
                    <textarea
                        className="form-textarea"
                        placeholder="Key outcomes or agreements..."
                        rows={2}
                        value={outcomes}
                        onChange={(e) => dispatch(setOutcomes(e.target.value))}
                    />
                </div>

                {/* Follow-up Actions */}
                <div className="form-group">
                    <label className="form-label">Follow-up Actions</label>
                    <textarea
                        className="form-textarea"
                        placeholder="Enter next steps or tasks..."
                        rows={2}
                        value={followUpActions}
                        onChange={(e) => dispatch(setFollowUpActions(e.target.value))}
                    />
                </div>

                {/* AI Suggested Follow-ups */}
                <div className="ai-suggestions">
                    <span className="ai-suggestions-label">AI Suggested Follow-ups:</span>
                    <ul className="suggestions-list">
                        {aiSuggestedFollowups.map((suggestion, index) => (
                            <li key={index} className="suggestion-item">
                                <span className="suggestion-bullet">+</span>
                                {suggestion}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default InteractionDetailsForm;
