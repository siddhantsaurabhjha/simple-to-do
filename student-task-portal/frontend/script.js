// Base API URL pointing to the Flask Backend Server
const API_BASE_URL = 'http://127.0.0.1:5000/api/records';

// Global state arrays & variables
let allRecords = [];
let editingRecordId = null;

// DOM Elements
const recordForm = document.getElementById('record-form');
const recordIdInput = document.getElementById('record-id');
const nameInput = document.getElementById('name');
const rollNumberInput = document.getElementById('roll-number');
const taskInput = document.getElementById('task');
const categorySelect = document.getElementById('category');
const statusSelect = document.getElementById('status');

const submitBtn = document.getElementById('submit-btn');
const cancelBtn = document.getElementById('cancel-btn');
const formTitle = document.getElementById('form-title');

const searchInput = document.getElementById('search-input');
const filterStatusSelect = document.getElementById('filter-status');

const recordsTbody = document.getElementById('records-tbody');
const loadingSpinner = document.getElementById('loading-spinner');
const emptyState = document.getElementById('empty-state');
const recordsTable = document.getElementById('records-table');

const statusBanner = document.getElementById('status-banner');
const bannerMessage = document.getElementById('banner-message');

const statTotal = document.getElementById('stat-total');
const statPending = document.getElementById('stat-pending');
const statCompleted = document.getElementById('stat-completed');
const statCategories = document.getElementById('stat-categories');


// Run initialization code once DOM content is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initial fetch of records from backend
    loadRecords();

    // Event listeners
    recordForm.addEventListener('submit', handleFormSubmit);
    cancelBtn.addEventListener('click', resetForm);
    searchInput.addEventListener('input', renderRecords);
    filterStatusSelect.addEventListener('change', renderRecords);
});


/**
 * Fetch all records from Flask API
 */
async function loadRecords() {
    showLoading(true);
    hideBanner();

    try {
        // Send GET request to Flask backend API
        const response = await fetch(API_BASE_URL);

        if (!response.ok) {
            throw new Error(`Server returned status: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            allRecords = data.records || [];
            renderRecords();
            updateStatistics();
        } else {
            showBanner(data.message || 'Failed to fetch records.', 'error');
        }

    } catch (error) {
        console.error('Error connecting to Flask API:', error);
        showBanner('Unable to connect to the backend. Make sure Flask server is running.', 'error');
        allRecords = [];
        renderRecords();
        updateStatistics();
    } finally {
        showLoading(false);
    }
}


/**
 * Handle form submission for both Create (Add) and Update modes
 */
async function handleFormSubmit(event) {
    event.preventDefault();

    // Extract form values
    const name = nameInput.value.trim();
    const roll_number = rollNumberInput.value.trim();
    const task = taskInput.value.trim();
    const category = categorySelect.value;
    const status = statusSelect.value;

    // Frontend validation
    if (!name || !roll_number || !task || !category || !status) {
        alert('Please fill out all required fields.');
        return;
    }

    const recordData = { name, roll_number, task, category, status };

    if (editingRecordId) {
        // UPDATE Mode
        await updateRecord(editingRecordId, recordData);
    } else {
        // ADD Mode
        await addRecord(recordData);
    }
}


/**
 * Send POST request to backend to create a new record
 */
async function addRecord(recordData) {
    try {
        const response = await fetch(API_BASE_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(recordData)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            resetForm();
            await loadRecords(); // Refresh list from backend
        } else {
            alert(result.message || 'Failed to add record.');
        }
    } catch (error) {
        console.error('Error adding record:', error);
        alert('Error communicating with backend server.');
    }
}


/**
 * Send PUT request to backend to update an existing record
 */
async function updateRecord(id, recordData) {
    try {
        const response = await fetch(`${API_BASE_URL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(recordData)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            resetForm();
            await loadRecords(); // Refresh list from backend
        } else {
            alert(result.message || 'Failed to update record.');
        }
    } catch (error) {
        console.error('Error updating record:', error);
        alert('Error communicating with backend server.');
    }
}


/**
 * Load record info into the form for editing
 */
function editRecord(id) {
    const record = allRecords.find(r => r.id === id);
    if (!record) return;

    editingRecordId = id;
    recordIdInput.value = record.id;
    nameInput.value = record.name;
    rollNumberInput.value = record.roll_number;
    taskInput.value = record.task;
    categorySelect.value = record.category;
    statusSelect.value = record.status;

    // Change button text and UI mode
    submitBtn.textContent = 'Update Record';
    formTitle.textContent = `Edit Record (ID: ${id})`;
    cancelBtn.classList.remove('hidden');

    // Scroll smoothly up to the form
    recordForm.scrollIntoView({ behavior: 'smooth' });
}


/**
 * Send DELETE request to delete a record
 */
async function deleteRecord(id) {
    const confirmed = confirm('Are you sure you want to delete this record?');
    if (!confirmed) return;

    try {
        const response = await fetch(`${API_BASE_URL}/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (response.ok && result.success) {
            await loadRecords(); // Refresh records list
        } else {
            alert(result.message || 'Failed to delete record.');
        }
    } catch (error) {
        console.error('Error deleting record:', error);
        alert('Error communicating with backend server.');
    }
}


/**
 * Quick action to mark a Pending task as Completed
 */
async function markCompleted(id) {
    const record = allRecords.find(r => r.id === id);
    if (!record) return;

    const updatedData = {
        name: record.name,
        roll_number: record.roll_number,
        task: record.task,
        category: record.category,
        status: 'Completed'
    };

    await updateRecord(id, updatedData);
}


/**
 * Filter and render records into the HTML table
 */
function renderRecords() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    const selectedFilter = filterStatusSelect.value;

    // Filter records dynamically based on search and status filter
    const filteredRecords = allRecords.filter(record => {
        // Status filter match
        const matchesStatus = (selectedFilter === 'All') || (record.status === selectedFilter);

        // Search match across Name, Roll Number, Task, Category, Status
        const matchesSearch = 
            record.name.toLowerCase().includes(searchTerm) ||
            record.roll_number.toLowerCase().includes(searchTerm) ||
            record.task.toLowerCase().includes(searchTerm) ||
            record.category.toLowerCase().includes(searchTerm) ||
            record.status.toLowerCase().includes(searchTerm);

        return matchesStatus && matchesSearch;
    });

    // Clear existing table rows
    recordsTbody.innerHTML = '';

    if (filteredRecords.length === 0) {
        recordsTable.classList.add('hidden');
        emptyState.classList.remove('hidden');
    } else {
        recordsTable.classList.remove('hidden');
        emptyState.classList.add('hidden');

        // Populate table rows
        filteredRecords.forEach(record => {
            const tr = document.createElement('tr');

            // Format date for display (e.g. 18 Aug 2026)
            const formattedDate = formatDate(record.created_at);

            // Badge styling class
            const badgeClass = record.status === 'Completed' ? 'status-completed' : 'status-pending';

            // Mark Complete button (only shown if status is Pending)
            const completeBtnHtml = record.status === 'Pending'
                ? `<button class="btn btn-complete" onclick="markCompleted(${record.id})">Mark Complete</button>`
                : '';

            tr.innerHTML = `
                <td><strong>#${record.id}</strong></td>
                <td>${escapeHtml(record.name)}</td>
                <td>${escapeHtml(record.roll_number)}</td>
                <td>${escapeHtml(record.task)}</td>
                <td>${escapeHtml(record.category)}</td>
                <td><span class="status-badge ${badgeClass}">${record.status}</span></td>
                <td>${formattedDate}</td>
                <td>
                    <div class="action-buttons">
                        ${completeBtnHtml}
                        <button class="btn btn-edit" onclick="editRecord(${record.id})">Edit</button>
                        <button class="btn btn-delete" onclick="deleteRecord(${record.id})">Delete</button>
                    </div>
                </td>
            `;

            recordsTbody.appendChild(tr);
        });
    }
}


/**
 * Calculate and display statistics on top cards
 */
function updateStatistics() {
    const total = allRecords.length;
    const pending = allRecords.filter(r => r.status === 'Pending').length;
    const completed = allRecords.filter(r => r.status === 'Completed').length;
    
    // Count unique categories
    const categoriesSet = new Set(allRecords.map(r => r.category));
    const uniqueCategories = categoriesSet.size;

    statTotal.textContent = total;
    statPending.textContent = pending;
    statCompleted.textContent = completed;
    statCategories.textContent = uniqueCategories;
}


/**
 * Reset form back to Add Record mode
 */
function resetForm() {
    editingRecordId = null;
    recordForm.reset();
    recordIdInput.value = '';
    statusSelect.value = 'Pending';
    submitBtn.textContent = 'Add Record';
    formTitle.textContent = 'Add New Record';
    cancelBtn.classList.add('hidden');
}


/**
 * Helper to format date strings into "18 Aug 2026"
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    try {
        const date = new Date(dateString.replace(' ', 'T'));
        if (isNaN(date.getTime())) return dateString;
        return date.toLocaleDateString('en-GB', {
            day: '2-digit',
            month: 'short',
            year: 'numeric'
        });
    } catch {
        return dateString;
    }
}


/**
 * Helper to escape HTML characters to prevent XSS
 */
function escapeHtml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


/**
 * Banner and loading state utilities
 */
function showLoading(isLoading) {
    if (isLoading) {
        loadingSpinner.classList.remove('hidden');
    } else {
        loadingSpinner.classList.add('hidden');
    }
}

function showBanner(message, type = 'error') {
    bannerMessage.textContent = message;
    statusBanner.className = `banner ${type}`;
}

function hideBanner() {
    statusBanner.className = 'banner hidden';
}
