import Button from "@/components/ui/Button";
import TaskList from "@/components/ui/TaskList";

export default function Main () {
    return (
        <main className="">
            <TaskList />
            <Button text={"Deploy Now"} />
        </main>
    )
}