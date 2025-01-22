"use client"

import { useState } from 'react';

export default function AddTask({ onAddTask }) {
    const [task, setTask] = useState('');

    const handleAddTask = () => {
        if (task.trim()) {
            onAddTask(task);
            setTask(''); // Clear the input field after adding the task
        }
    };

    return (
        <div className="flex flex-col sm:flex-row items-center gap-4 bg-gray-800 p-4 mb-6 rounded-md">
            <input
                type="text"
                value={task}
                onChange={(e) => setTask(e.target.value)}
                className="w-full sm:flex-grow p-2 rounded-md text-gray-900 placeholder-gray-500 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
                onClick={handleAddTask}
                className="w-full sm:w-auto bg-blue-500 text-white p-2 rounded hover:bg-blue-600 focus:ring-2 focus:ring-blue-400 focus:outline-none"
            >
                Add Task
            </button>
        </div>
    );
}