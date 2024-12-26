import React, { useState, useEffect } from "react";
import { getTasks, updateTask, deleteTask } from "../utils/api";
import "./TaskList.css";

const TaskList = ({ onEdit }) => {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await getTasks();
        setTasks(response.data);
      } catch (err) {
        setError("Failed to load tasks.");
      }
    };

    fetchTasks();
  }, []);

  const handleDelete = async (id) => {
    try {
      await deleteTask(id);
      setTasks(tasks.filter((task) => task.id !== id));
    } catch (err) {
      if (err.response?.status === 403) {
        setError(err.response.data.detail || "You are not authorized to delete this task.");
      } else {
        setError("An error occurred while deleting the task.");
      }
    }
  };

  const toggleCompletion = async (task) => {
    try {
      const updatedTask = { ...task, completed: !task.completed };
      await updateTask(task.id, updatedTask);
      setTasks(tasks.map((t) => (t.id === task.id ? updatedTask : t)));
    } catch (err) {
      if (err.response?.status === 403) {
        setError(err.response.data.detail || "You are not authorized to modify this task.");
      } else {
        setError("An error occurred while updating the task.");
      }
    }
  };

  return (
    <div>
      <h2>Tasks</h2>
      {error && <p className="error-message">{error}</p>} {/* Display error */}
      <div className="task-list">
        {tasks.map((task) => (
          <div key={task.id} className="task-card">
            <h3
              className={`task-title ${task.completed ? "completed" : ""}`}
              onClick={() => toggleCompletion(task)}
            >
              {task.title}
            </h3>
            <p className="task-owner">Owner: {task.owner || "Unknown"}</p>
            <p className="task-description">
              {task.description || "No description provided."}
            </p>
            <div className="task-actions">
              <button className="edit-button" onClick={() => onEdit(task)}>
                Edit
              </button>
              <button
                className="delete-button"
                onClick={() => handleDelete(task.id)}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TaskList;
