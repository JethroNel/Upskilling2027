const studentForm = document.getElementById("studentForm");

const studentList = document.getElementById("studentList");

const message = document.getElementById("message");

// Load students from Node.js
async function loadStudents() {

    const response = await fetch("/api/students");

    const students = await response.json();

    studentList.innerHTML = "";

    students.forEach(student => {

        const result = student.mark >= 50 ? "PASS" : "FAIL";

        const row = document.createElement("tr");

        row.innerHTML = `
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td><button type="button" class="delete-btn">Delete</button></td>
        `;

        // Safely insert student information
        row.cells[0].textContent = student.name;
        row.cells[1].textContent = student.age;
        row.cells[2].textContent = student.mark;
        row.cells[3].textContent = result;

        row.querySelector("button").addEventListener("click", () => {
            deleteStudent(student.id);
        });

        studentList.appendChild(row);

    });

}

// Add a student
studentForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const student = {

        name: document.getElementById("name").value.trim(),

        age: document.getElementById("age").value,

        mark: document.getElementById("mark").value

    };

    try {

        const response = await fetch("/api/students", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(student)

        });

        const data = await response.json();

        message.textContent = data.message;

        if (!response.ok) {
            return;
        }

        studentForm.reset();

        loadStudents();

    } catch (error) {

        message.textContent = "Unable to connect to the server.";

    }

});

// Delete a student
async function deleteStudent(id) {

    const response = await fetch(`/api/students/${id}`, {

        method: "DELETE"

    });

    const data = await response.json();

    message.textContent = data.message;

    if (response.ok) {
        loadStudents();
    }

}

// Load students when the page opens
loadStudents();
