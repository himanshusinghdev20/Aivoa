import InteractionDetailsForm from './InteractionDetailsForm/InteractionDetailsForm';
import AIAssistant from './AIAssistant/AIAssistant';
import './LogInteractionScreen.css';

const LogInteractionScreen = () => {
    return (
        <div className="log-interaction-screen">
            <h1 className="screen-title">Log HCP Interaction</h1>
            <div className="screen-content">
                <InteractionDetailsForm />
                <AIAssistant />
            </div>
        </div>
    );
};

export default LogInteractionScreen;
