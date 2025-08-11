import React from 'react';
import Task from '../Task'

export default function TaskList({ 
        tasks=[],
        onRemove = f => f,
        onRate = f => f,
        onState = f => f,
        onNewTask = f => f
    }) {

        if(!tasks.length) return <div> Brak zadań do wykonania. (Dodaj zadanie)</div>;
        return (
            <div className="task-list">
                {
                    tasks.map(task => (
                        <Task 
                            key={task.id} 
                            {...task} 
                            onRemove={onRemove} 
                            onRate = {onRate}
                            onState={onState}
                            onNewTask={onNewTask}
                        />)
                    )
                }
            </div>
        );
}   



