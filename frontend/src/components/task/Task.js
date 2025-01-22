export default function Task ({ task }) {
    return (
        <div className="bg-gray-800 rounded-lg my-3 p-4 text-white shadow-md w-full md:w-3/4">
            <p className="text-sm md:text-base">{task}</p>
        </div>
    )
}