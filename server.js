
const express = require("express");

const app = express();

const PORT = 3000;

// Allow Node.js to receive JSON data
app.use(express.json());

// Connect the HTML, CSS and JavaScript folder
app.use(express.static("public"));

// Temporary student database
let students = [];

// Get all students
app.get("/api/students", (req, res) => {

    res.json(students);

});

// Add a new student
app.post("/api/students", (req, res) => {

    const { name, age, mark } = req.body;

    if (!name || !Number.isFinite(Number(age)) ||
        !Number.isFinite(Number(mark)) ||
        Number(age) <= 0 ||
        Number(mark) < 0 ||
        Number(mark) > 100) {

        return res.status(400).json({
            message: "Please enter valid student details."
        });
    }

    const student = {
        id: Date.now(),
        name: name,
        age: Number(age),
        mark: Number(mark)
    };

    students.push(student);

    res.status(201).json({
        message: "Student added successfully!",
        student: student
    });

});

// Delete a student
app.delete("/api/students/:id", (req, res) => {

    const studentId = Number(req.params.id);

    const originalLength = students.length;

    students = students.filter(student => student.id !== studentId);

    if (students.length === originalLength) {

        return res.status(404).json({
            message: "Student not found."
        });

    }

    res.json({
        message: "Student deleted successfully."
    });

});

// Start the server
app.listen(PORT, () => {

    console.log(`Student Management System running at http://localhost:${PORT}`);

});
