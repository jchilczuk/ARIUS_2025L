import React, { useState, useEffect } from 'react';
import { FaCheck, FaTimes } from 'react-icons/fa';

const ChangeState = ({ deadline, state, onState = f => f, onDelete = f => f }) => {
    const [currentState, setCurrentState] = useState(state);

    useEffect(() => {
        setCurrentState(state);
    }, [state]);

    useEffect(() => {
        const parseDate = (dateString) => {
            const [time, date] = dateString.split(' '); 
            const [hours, minutes] = time.split(':').map(Number);
            const [day, month, year] = date.split('.').map(Number);
            return new Date(year, month - 1, day, hours, minutes);
        };
        
        const now = new Date();
        const taskDate = parseDate(deadline);

        if (taskDate < now && currentState === "Oczekujące") {
            setCurrentState("Przeterminowane");
            onState("Przeterminowane");
            onDelete(true);
        }
    }, [deadline, currentState, onState, onDelete]);

    const toggleState = () => {
        if (currentState === "Wykonane") {
            setCurrentState("Oczekujące");
            onState("Oczekujące");
            onDelete(false);
        } 
        else {
            setCurrentState("Wykonane");
            onState("Wykonane");
            onDelete(true);
        }
    };

    return (
        <div>
            {currentState === "Przeterminowane" && (
                <div style={{ marginBottom: "5px", fontWeight: "bold", color: "orange" }}>
                Zadanie po terminie
            </div>
            )}

            {currentState === "Oczekujące" && (
                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <div>Oznacz jako wykonane</div>
                    <button onClick={toggleState}> 
                        <FaCheck color="green" /> 
                    </button>
                </div>
            )}
           
            {currentState === "Wykonane" && (
                <div>
                <div style={{ marginBottom: "5px", fontWeight: "bold", color: "green" }}>
                    Zadanie wykonane!
                </div>
                <br />
                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <div>Oznacz jako niewykonane</div>
                    <button onClick={toggleState}> 
                        <FaTimes color="red" /> 
                    </button>
                </div>
                </div>
            )}
        
        </div>
    );
};

export default ChangeState;
