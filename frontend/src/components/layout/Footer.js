export default function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="p-4 bg-gray-800 text-white">
            <p className="text-center text-sm">
                &copy; {currentYear} Taskit Inc. All rights reserved.
            </p>
        </footer>
    );
}