import React, { useState, useEffect } from "react";
import { createTask, updateTask } from "../utils/api";

const TaskForm = ({ selectedTask, onSave, onCancel, owner }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (selectedTask) {
      setTitle(selectedTask.title);
      setDescription(selectedTask.description || "");
    } else {
      setTitle("");
      setDescription("");
    }
    setError("");
  }, [selectedTask]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const task = { title, description, owner };

    try {
      if (selectedTask) {
        await updateTask(selectedTask.id, task);
      } else {
        await createTask(task);
      }
      onSave();
    } catch (err) {
      if (err.response?.status === 403) {
        setError(err.response.data.detail || "You are not authorized to perform this action.");
      } else {
        setError("An unexpected error occurred.");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>{selectedTask ? "Edit Task" : "New Task"}</h2>
      {error && <p className="error-message">{error}</p>} {/* Display error */}
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Task Title"
        required
      />
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Task Description"
      />
      <button type="submit">Save</button>
      {onCancel && <button type="button" onClick={onCancel}>Cancel</button>}
    </form>
  );
};

export default TaskForm;
