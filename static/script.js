function searchProducts() {
    const casList = Array.from(document.querySelectorAll('input[name="cas"]'))
        .map(input => input.value.trim())
        .filter(cas => cas !== '');

    fetch("/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ cas: casList }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(data.error);
                return;
            }
            const results = data.results;
            displayResults(results);
        });
}

function displayResults(results) {
    const resultsSection = document.getElementById("results-section");
    const resultsTableBody = document.querySelector("#results-table tbody");
    const paginationControls = document.getElementById("pagination-controls");

    resultsSection.classList.remove("hidden");
    resultsTableBody.innerHTML = '';
    paginationControls.innerHTML = '';

    if (results.length === 0) {
        resultsTableBody.innerHTML = '<tr><td colspan="7">Không tìm thấy kết quả.</td></tr>';
        return;
    }

    results.forEach((result) => {
        const row = document.createElement('tr');

        const cellName = document.createElement('td');
        cellName.textContent = result.Name || '';
        row.appendChild(cellName);

        const cellCode = document.createElement('td');
        cellCode.textContent = result.Code || '';
        row.appendChild(cellCode);

        const cellCAS = document.createElement('td');
        cellCAS.textContent = result.CAS || '';
        row.appendChild(cellCAS);

        const cellBrand = document.createElement('td');
        cellBrand.textContent = result.Brand || '';
        row.appendChild(cellBrand);

        const cellSize = document.createElement('td');
        cellSize.textContent = result.Size || '';
        row.appendChild(cellSize);

        const cellPrice = document.createElement('td');
        cellPrice.textContent = result.Price || '';
        row.appendChild(cellPrice);

        const cellNote = document.createElement('td');
        cellNote.textContent = result.Note || '';
        row.appendChild(cellNote);

        // Tô màu theo Brand
        if (result.Brand === 'Phụ lục I') {
            row.style.backgroundColor = '#ffe4e1'; // Màu đỏ nhạt
        } else if (result.Brand === 'Phụ lục II') {
            row.style.backgroundColor = '#fffacd'; // Màu vàng nhạt
        } else if (result.Brand === 'CẤM NHẬP') {
            row.style.backgroundColor = '#e0ffff'; // Màu xanh nhạt
        }

        resultsTableBody.appendChild(row);
    });
}

function backToSearch() {
    const resultsSection = document.getElementById("results-section");
    resultsSection.classList.add("hidden");

    // Xóa toàn bộ dữ liệu trong các ô tìm kiếm
    const searchInputs = document.querySelectorAll('#search-page input[name="cas"]');
    searchInputs.forEach(input => input.value = '');
}
