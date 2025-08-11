import './App.css';
import TaskList from './components/TaskList';
import {useState} from 'react';
import tasksData from './tasks-data.json';
import AddTaskForm from "./components/AddTaskForm";


function App() {
  const [tasks, setTask] = useState(tasksData);

  const handleRate = (id, rating) => {
    console.log("id, rating ", id, rating)
    const newTask = tasks.map(task => 
      task.id === id ? { ...task, rating } : task
    );
    setTask(newTask);
    console.log("Updated tasks list", newTask)
  };

  const handleRemove = (id) => {
    const newTask = tasks.filter(task => task.id !== id);
    setTask(newTask);
  };

  const handleState = (id, state) => {
    console.log("id, state", id, state)
    const newTask = tasks.map(task => 
      task.id === id ? { ...task, state } : task
    );
    setTask(newTask);
    console.log("Updated tasks list", newTask)
  };

  return (
    <>
      <h1>Lista zadań</h1>
      < AddTaskForm
      onNewTask = {(title, description, deadline) => {
        const maxId = tasks.length > 0 ? Math.max(...tasks.map(task => task.id)) : 0;
        const newTask = {
          id: maxId +1,
          title,
          description,
          deadline,
          state: "Oczekujące",
          rating: 0
        };
      
      setTask([...tasks, newTask]);
      console.log("New task", newTask)
    }}
      />
      <TaskList 
        tasks={tasks}
        onRate={handleRate}
        onRemove={handleRemove}
        onState={handleState}
      />
    </>
  );
}

export default App;
