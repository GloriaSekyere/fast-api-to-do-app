import Task from "@/components/task/Task";

export default function TaskList({ tasks }) {
    return (
        <div>
            {tasks.map((task, index) => (
                <Task key={index} task={task} />
            ))}
        </div>
    );
}