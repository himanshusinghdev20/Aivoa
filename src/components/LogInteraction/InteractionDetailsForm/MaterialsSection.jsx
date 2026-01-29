import { useSelector, useDispatch } from 'react-redux';
import { addMaterial, removeMaterial } from '../../../store/slices/interactionSlice';
import './MaterialsSection.css';

const MaterialsSection = () => {
    const dispatch = useDispatch();
    const { materialsShared } = useSelector((state) => state.interaction);

    const handleAddMaterial = () => {
        const material = prompt('Enter material name:');
        if (material) {
            dispatch(addMaterial(material));
        }
    };

    return (
        <div className="materials-section">
            <div className="section-header">
                <span className="section-title">Materials Shared</span>
                <button className="add-btn" onClick={handleAddMaterial}>
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                        <circle cx="7" cy="7" r="6" stroke="currentColor" strokeWidth="1.5" />
                        <path d="M7 4V10M4 7H10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                    </svg>
                    Search/Add
                </button>
            </div>
            <div className="items-list">
                {materialsShared.length === 0 ? (
                    <span className="empty-text">No materials added</span>
                ) : (
                    materialsShared.map((material, index) => (
                        <div key={index} className="item-chip">
                            {material}
                            <button className="remove-btn" onClick={() => dispatch(removeMaterial(index))}>
                                ×
                            </button>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default MaterialsSection;
