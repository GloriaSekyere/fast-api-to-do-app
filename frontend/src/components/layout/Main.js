"use client"

import { useState } from "react";
import AddTask from "@/components/task/AddTask";
import TaskList from "@/components/task/TaskList";

export default function Main() {
    // Manage the task list state in the Main component
    const [tasks, setTasks] = useState([
        "Call doctor",
        "Meet with lawyer",
        "Buy groceries"
    ]);

    // Function to add a new task to the list
    const handleAddTask = (task) => {
        if (task) {
            setTasks((prevTasks) => [...prevTasks, task]);
        }
    };

    return (
        <main className="flex flex-col flex-grow m-auto w-4/5 py-20">
            <AddTask onAddTask={handleAddTask} />
            <TaskList tasks={tasks} />
        </main>
    );
}