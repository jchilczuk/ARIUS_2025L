import React from 'react';
import Star from '../Star';


const createArray = length => [...Array(length)];

export default function StarRating({
    totalStars=10, 
    selectedStars=0,
    currentState = "Oczekujące",
    onRate = f => f
}) 
{
    const isEditable = currentState === "Oczekujące";
    return (
        <>
            {createArray(totalStars).map((n,i) => (
                <Star
                    key={i}
                    selected = {selectedStars > i}
                    onSelect = {() => isEditable ? onRate(selectedStars === i+1 ? 0 : i+1) : null}
                />
            ))}
        </>
    );
};



