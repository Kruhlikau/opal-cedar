import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import TaskList from "../components/TaskList";
import TaskForm from "../components/TaskForm";
import { AuthContext } from "../context/AuthContext";
import "./Dashboard.css";

const Dashboard = () => {
  const [selectedTask, setSelectedTask] = useState(null);
  const [refresh, setRefresh] = useState(false);
  const { logout, user } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const handleEdit = (task) => {
    setSelectedTask(task);
  };

  const handleSave = () => {
    setSelectedTask(null);
    setRefresh(!refresh);
  };

  const handleCancel = () => {
    setSelectedTask(null);
  };

  if (!user) {
    return <p>Loading...</p>;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Task Dashboard</h1>
        <div className="user-block">
          <span className="username">Welcome, {user.username}</span>
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </div>
      </div>
      <TaskForm
        selectedTask={selectedTask}
        onSave={handleSave}
        onCancel={handleCancel}
        owner={user.id}
      />
      <TaskList onEdit={handleEdit} key={refresh} />
    </div>
  );
};

export default Dashboard;
