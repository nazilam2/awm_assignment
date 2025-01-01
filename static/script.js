// static/js/script.js

const fetchData = async () => {
    const response = await fetch('http://127.0.0.1:8000/api/v1/gasstations/');

    const data = await response.json();  // Parse the JSON response

    const tableBody = document.getElementById('gas-stations-table-body');
    tableBody.innerHTML = '';  // Clear existing data

    data.forEach(station => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${station.name}</td>
            <td>${station.location}</td>
            <td>${station.fuel_type}</td>
            <td>$${station.price}</td>
            <td>${station.rating}</td>
        `;
        tableBody.appendChild(row);
    });
};

// Call the fetchData function on page load
document.addEventListener("DOMContentLoaded", fetchData);
