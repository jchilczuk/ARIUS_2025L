import React, {useState, useEffect} from 'react';
import StarRating from '../StarRating';
import ChangeState from '../ChangeState';

export default function Task({
        id,
        title,
        description = "",
        deadline = "", 
        state = "",
        rating,
        onRemove = f => f,
        onRate = f => f,
        onState = f => f
    }) {
    
    const [canRemove, setRemovable] = useState(false);
    const [currentState, setCurrentState] = useState(state); 

    useEffect(() => {
        setCurrentState(state);
    }, [state]);

    const handleStateChange = (newState) => {
        setCurrentState(newState); 
        onState(id, newState); 
        setRemovable(newState === "Wykonane" || newState === "Przeterminowane");
    };

    return (
        <section>
            <h1>{id}. {title}</h1>
            
            <ChangeState 
                deadline={deadline}
                state={currentState} 
                onState={handleStateChange}
                onRemove={setRemovable}
            />

            <div>Opis: {description}</div>
            <div>Termin wykonania: {deadline}</div>
            
            <div>Priorytet:   
                <StarRating 
                    selectedStars={rating} 
                    currentState={currentState} 
                    onRate={rating => onRate(id, rating)}
                />
            </div>
            
            {canRemove && (
                <div>
                    <button 
                        onClick={() => onRemove(id)} 
                        style={{ color: "red" }}
                    >
                        Usuń zadanie 
                    </button>
                </div>
            )}
        </section>
    );
}
