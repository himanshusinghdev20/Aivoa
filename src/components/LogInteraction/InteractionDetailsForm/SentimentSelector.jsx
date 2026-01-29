import { useSelector, useDispatch } from 'react-redux';
import { setSentiment } from '../../../store/slices/interactionSlice';
import './SentimentSelector.css';

const SentimentSelector = () => {
    const dispatch = useDispatch();
    const { sentiment } = useSelector((state) => state.interaction);

    const sentiments = [
        { value: 'positive', emoji: '😊', label: 'Positive' },
        { value: 'neutral', emoji: '😐', label: 'Neutral' },
        { value: 'negative', emoji: '😞', label: 'Negative' },
    ];

    return (
        <div className="sentiment-selector">
            {sentiments.map((item) => (
                <label key={item.value} className="sentiment-option">
                    <input
                        type="radio"
                        name="sentiment"
                        value={item.value}
                        checked={sentiment === item.value}
                        onChange={(e) => dispatch(setSentiment(e.target.value))}
                        className="sentiment-radio"
                    />
                    <span className={`sentiment-emoji ${sentiment === item.value ? 'active' : ''}`}>
                        {item.emoji}
                    </span>
                    <span className="sentiment-label">{item.label}</span>
                </label>
            ))}
        </div>
    );
};

export default SentimentSelector;
