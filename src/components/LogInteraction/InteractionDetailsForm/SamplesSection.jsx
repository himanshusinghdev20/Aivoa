import { useSelector, useDispatch } from 'react-redux';
import { addSample, removeSample } from '../../../store/slices/interactionSlice';
import './MaterialsSection.css'; // Reuse same styles

const SamplesSection = () => {
    const dispatch = useDispatch();
    const { samplesDistributed } = useSelector((state) => state.interaction);

    const handleAddSample = () => {
        const sample = prompt('Enter sample name:');
        if (sample) {
            dispatch(addSample(sample));
        }
    };

    return (
        <div className="samples-section">
            <div className="section-header">
                <span className="section-title">Samples Distributed</span>
                <button className="add-btn" onClick={handleAddSample}>
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                        <rect x="2" y="2" width="10" height="10" rx="2" stroke="currentColor" strokeWidth="1.5" />
                        <path d="M7 4.5V9.5M4.5 7H9.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                    </svg>
                    Add Sample
                </button>
            </div>
            <div className="items-list">
                {samplesDistributed.length === 0 ? (
                    <span className="empty-text">No samples added</span>
                ) : (
                    samplesDistributed.map((sample, index) => (
                        <div key={index} className="item-chip">
                            {sample}
                            <button className="remove-btn" onClick={() => dispatch(removeSample(index))}>
                                ×
                            </button>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default SamplesSection;
