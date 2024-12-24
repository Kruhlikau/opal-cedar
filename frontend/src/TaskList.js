import React, { useEffect, useState } from 'react';
import axios from 'axios';

const TaskList = () => {
    const [tasks, setTasks] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/tasks/')
            .then(response => {
                setTasks(response.data);
            })
            .catch(error => {
                console.error('Error fetching tasks', error);
            });
    }, []);

    return (
        <div>
            <h1>To-Do List</h1>
            <ul>
                {tasks.map(task => (
                    <li key={task.id}>
                        {task.title} - {task.description} (Completed: {task.completed ? 'Yes' : 'No'})
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default TaskList;
