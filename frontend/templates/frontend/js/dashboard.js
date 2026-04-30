console.log("Dashboard loaded");

const API = 'http://127.0.0.1:8000';
let currentRole = null;


document.addEventListener('DOMContentLoaded', function() {
    initDashboard();
});

async function initDashboard() {
    try {
        const profile = await fetchJSON(API + '/me/');
        currentRole = profile.role;

        document.getElementById('navbar-username').textContent = profile.username || '';
        document.getElementById('navbar-role').textContent = profile.role;

        if (currentRole === 'DOCTOR') {
            document.getElementById('doctor-nav').classList.remove('d-none');
        } else {
            document.getElementById('patient-nav').classList.remove('d-none');
        }

        loadProfile(null, profile);
    } catch (err) {
        // Not logged in or session expired
        window.location.href = 'login.html';
    }
}




async function fetchJSON(url, options = {}) {
    const method = (options.method || 'GET').toUpperCase();
    const headers = { 'Content-Type': 'application/json' };


    const mutatingMethods = ['POST', 'PUT', 'PATCH', 'DELETE'];
    if (mutatingMethods.includes(method)) {
        const csrf = getCookie('csrftoken');
        if (csrf) headers['X-CSRFToken'] = csrf;
    }

    const res = await fetch(url, {
        credentials: 'include',
        headers,
        ...options
    });

    const text = await res.text();
    let data = {};
    try {
        data = JSON.parse(text);
    } catch (e) {
        data = { detail: text };
    }

    if (!res.ok) throw { status: res.status, data };
    return data;
}




function getCookie(name) {
    const value = '; ' + document.cookie;
    const parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}

function showMessage(type, msg) {
    const area = document.getElementById('message-area');
    area.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show py-2 mb-0" role="alert">
            ${msg}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    area.classList.remove('d-none');

  
    setTimeout(function() {
        const el = area.querySelector('.alert');
        if (el) bootstrap.Alert.getOrCreateInstance(el).close();
    }, 5000);
}

function setLoading(show) {
    document.getElementById('loading').classList.toggle('d-none', !show);
    document.getElementById('content-area').classList.toggle('d-none', show);
}

function setContent(html) {
    document.getElementById('content-area').innerHTML = html;
    setLoading(false);
}


function formatErrors(data) {
    if (!data) return 'Something went wrong.';
    if (typeof data === 'string') return data;

    return Object.entries(data).map(function([field, errors]) {
        const message = Array.isArray(errors) ? errors.join(', ') : errors;
        return `<b>${field}:</b> ${message}`;
    }).join('<br>');
}

function setActive(btn) {
    document.querySelectorAll('.sidebar button').forEach(function(b) {
        b.classList.remove('active');
    });
    if (btn) btn.classList.add('active');
}



async function loadProfile(btn, preloaded) {
    setActive(btn);
    setLoading(true);

    try {
        const p = preloaded || await fetchJSON(API + '/me/');   
        const isDoctor = p.role === 'DOCTOR';
        
        console.log(p)

        let rows = '';

        if (isDoctor) {
            const specs = (p.specialization || []).join(', ') || '—';

            rows = `
                <tr><td class="text-muted">Name</td><td>${p.name || '—'}</td></tr>
                <tr><td class="text-muted">Gender</td><td>${p.gender || '—'}</td></tr>
                <tr><td class="text-muted">Phone</td><td>${p.phonenumber || '—'}</td></tr>
                <tr><td class="text-muted">Experience</td><td>${p.years_of_experience ?? '—'} yrs</td></tr>
                <tr><td class="text-muted">Verified</td><td>${p.is_verified ? 'Yes' : 'No'}</td></tr>
                <tr><td class="text-muted">Specialization</td><td>${specs}</td></tr>
            `;
        } else {
            rows = `
                <tr><td class="text-muted">Name</td><td>${p.name || '—'}</td></tr>
                <tr><td class="text-muted">Age</td><td>${p.age || '—'}</td></tr>
                <tr><td class="text-muted">Gender</td><td>${p.gender || '—'}</td></tr>
                <tr><td class="text-muted">Blood Group</td><td>${p.bloodgroup || '—'}</td></tr>
                <tr><td class="text-muted">Height</td><td>${p.height || '—'} cm</td></tr>
                <tr><td class="text-muted">Weight</td><td>${p.weight || '—'} kg</td></tr>
                <tr><td class="text-muted">City</td><td>${p.city || '—'}</td></tr>
                <tr><td class="text-muted">Phone</td><td>${p.phonenumber || '—'}</td></tr>
            `;
        }

        setContent(`
            <h6 class="mb-3">Profile</h6>
            <table class="table table-sm table-bordered" style="max-width: 420px">
                <tbody>${rows}</tbody>
            </table>
        `);
    } catch (err) {
        setContent('');
        showMessage('danger', 'Failed to load profile.');
    }
}



function showScheduleForm(btn) {
    setActive(btn);
    const today = new Date().toISOString().split('T')[0];

    setContent(`
        <h6 class="mb-3">Add Schedule</h6>
        <div style="max-width: 400px">
            <div class="mb-2">
                <label class="form-label mb-1 small">Start Date</label>
                <input type="date" id="sf-start-date" class="form-control form-control-sm" min="${today}">
            </div>
            <div class="mb-2">
                <label class="form-label mb-1 small">End Date</label>
                <input type="date" id="sf-end-date" class="form-control form-control-sm" min="${today}">
            </div>
            <div class="mb-2">
                <label class="form-label mb-1 small">Start Time</label>
                <input type="time" id="sf-start-time" class="form-control form-control-sm">
            </div>
            <div class="mb-2">
                <label class="form-label mb-1 small">End Time</label>
                <input type="time" id="sf-end-time" class="form-control form-control-sm">
            </div>
            <div class="mb-3">
                <label class="form-label mb-1 small">Slot Duration (minutes)</label>
                <input type="number" id="sf-slot-duration" class="form-control form-control-sm" min="5" max="120" placeholder="e.g. 30">
            </div>
            <button class="btn btn-primary btn-sm" id="schedule-submit-btn" onclick="submitSchedule()">
                Save Schedule
            </button>
        </div>
    `);
}
 async function showSchedulePage(btn) {
    setActive(btn);
    setLoading(true);

    try {
        const schedules = await fetchJSON(API + '/doctor-schedule/');

        let rows = '';

        if (schedules.length) {
            rows = schedules.map(function(s) {
                return `
                    <tr>
                        <td>${s.start_date || '—'}</td>
                        <td>${s.end_date || '—'}</td>
                        <td>${s.start_time || '—'}</td>
                        <td>${s.end_time || '—'}</td>
                        <td>${s.slot_duration || '—'} mins</td>
                    </tr>
                `;
            }).join('');
        } else {
            rows = `<tr><td colspan="5" class="text-muted text-center small">No schedules found.</td></tr>`;
        }

        setContent(`
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="mb-0">My Schedule</h6>
                <button class="btn btn-sm btn-primary" onclick="showScheduleForm(null)">
                    + Add Schedule
                </button>
            </div>

            <table class="table table-sm table-bordered">
                <thead class="table-light">
                    <tr>
                        <th>Start Date</th>
                        <th>End Date</th>
                        <th>Start Time</th>
                        <th>End Time</th>
                        <th>Slot Duration</th>
                    </tr>
                </thead>
                <tbody>${rows}</tbody>
            </table>
        `);

    }  
     catch (err) {
    setContent('');

    const errorMsg =
        err.data?.detail ||          
        JSON.stringify(err.data) ||  
        err.message || 
        "Failed to load schedules.";

    showMessage('danger', errorMsg);
}
}

async function submitSchedule() {
    const btn = document.getElementById('schedule-submit-btn');

    const startDate = document.getElementById('sf-start-date').value;
    const endDate = document.getElementById('sf-end-date').value;
    const startTime = document.getElementById('sf-start-time').value;
    const endTime = document.getElementById('sf-end-time').value;
    const slotDuration = parseInt(document.getElementById('sf-slot-duration').value, 10);

    if (!startDate || !endDate || !startTime || !endTime || !slotDuration) {
        showMessage('warning', 'Please fill in all fields.');
        return;
    }
    if (endDate < startDate) {
        showMessage('warning', 'End date must be after start date.');
        return;
    }
    if (endTime <= startTime) {
        showMessage('warning', 'End time must be after start time.');
        return;
    }

    btn.disabled = true;
    btn.textContent = 'Saving…';

    try {
        await fetchJSON(API + '/doctor-schedule/', {
            method: 'POST',
            body: JSON.stringify({
                start_date: startDate,
                end_date: endDate,
                start_time: startTime,
                end_time: endTime,
                slot_duration: slotDuration
            })
        });

        showMessage('success', 'Schedule created successfully.');
        showScheduleForm(null); // Reset the form
    } catch (err) {
        showMessage('danger', formatErrors(err.data));
    } finally {
        btn.disabled = false;
        btn.textContent = 'Save Schedule';
    }
}


async function loadAppointments(btn) {
    setActive(btn);
    setLoading(true);

    try {
        const list = await fetchJSON(API + '/appointments/');
        renderAppointments(list);
        console.log(list)
    } catch (err) {
        setContent('');
        showMessage('danger', 'Failed to load appointments.');
    }
}

function renderAppointments(list) {
    const isDoctor = currentRole === 'DOCTOR';
    const title = '<h6 class="mb-3">Appointments</h6>';

    if (!list.length) {
        setContent(title + '<p class="text-muted small">No appointments found.</p>');
        return;
    }

    const statusColors = {
        PENDING: 'warning',
        CONFIRMED: 'success',
        CANCELLED: 'danger',
        COMPLETED: 'primary'
    };

    const rows = list.map(function(appt) {
        const color = statusColors[appt.status] || 'secondary';
        const personName = isDoctor
            ? (appt.patient || '—')
            : (appt.doctor|| '—');
        console.log(personName)
        const date = appt.slot?.date || '—';
        const time = appt.slot ? `${appt.slot.start_time} – ${appt.slot.end_time}` : '—';
        const feedback = appt.feedback || 'Not given yet';

     
        let actionButtons = '';
        if (isDoctor && appt.status === 'PENDING') {
            actionButtons = `
                <button class="btn btn-sm btn-success me-1" id="confirm-btn-${appt.id}" onclick="confirmAppointment(${appt.id})">Confirm</button>
                <button class="btn btn-sm btn-danger" id="reject-btn-${appt.id}" onclick="rejectAppointment(${appt.id})">Reject</button>
            `;
        }

        return `
            <tr id="appt-row-${appt.id}">
                <td>${personName}</td>
                <td>${date}</td>
                <td>${time}</td>
                <td>${feedback}</td>
                <td><span class="badge bg-${color}">${appt.status}</span></td>
                ${isDoctor ? `<td>${actionButtons}</td>` : ''}
            </tr>
        `;
    }).join('');

    setContent(`
        ${title}
        <table class="table table-sm table-bordered">
            <thead class="table-light">
                <tr>
                    <th>${isDoctor ? 'Patient' : 'Doctor'}</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Feedback</th>
                    <th>Status</th>
                    ${isDoctor ? '<th>Action</th>' : ''}
                </tr>
            </thead>
            <tbody>${rows}</tbody>
        </table>
    `);
}

async function confirmAppointment(id) {
    await appointmentAction(id, 'confirm', 'Appointment confirmed.', 'CONFIRMED');
}

async function rejectAppointment(id) {
    await appointmentAction(id, 'reject', 'Appointment rejected.', 'CANCELLED');
}

async function appointmentAction(id, action, successMsg, newStatus) {
    const confirmBtn = document.getElementById('confirm-btn-' + id);
    const rejectBtn = document.getElementById('reject-btn-' + id);

    // Disable buttons while request is in flight
    if (confirmBtn) confirmBtn.disabled = true;
    if (rejectBtn) rejectBtn.disabled = true;

    try {
        await fetchJSON(`${API}/appointments/${id}/${action}/`, { method: 'PATCH' });
        showMessage('success', successMsg);

        const row = document.getElementById('appt-row-' + id);
        if (row) {
            const badge = row.querySelector('.badge');
            if (badge) {
                badge.className = 'badge bg-' + (newStatus === 'CONFIRMED' ? 'success' : 'danger');
                badge.textContent = newStatus;
            }
            const lastCell = row.cells[row.cells.length - 1];
            if (lastCell) lastCell.innerHTML = '';
        }
    } catch (err) {
        showMessage('danger', formatErrors(err.data) || 'Action failed.');
        if (confirmBtn) confirmBtn.disabled = false;
        if (rejectBtn) rejectBtn.disabled = false;
    }
}



async function loadDoctors(btn) {
    setActive(btn);
    setLoading(true);

    try {
        const doctors = await fetchJSON(API + '/doctor/list/');
        const verifiedDoctors = doctors.filter(doc => doc.is_verified);
        console.log(verifiedDoctors)

        if (!verifiedDoctors.length) {
            setContent('<h6 class="mb-3">Book Appointment</h6><p class="text-muted small">No verified doctors available.</p>');
            return;
        }

        if (!verifiedDoctors.length) {
            setContent('<h6 class="mb-3">Book Appointment</h6><p class="text-muted small">No doctors available.</p>');
            return;
        }

        const rows = verifiedDoctors.map(function(doc) {
            const specs = (doc.specialization || [])
                .map(s => s.type || s)
                .join(', ') || '—';
            const experience = doc.years_of_experience ?? '—';

            return `
                <tr>
                    <td>${doc.name}</td>
                    <td>${specs}</td>
                    <td>${experience} yrs</td>
                    <td>${doc.phonenumber}</td>
                    <td>${doc.is_verified ? 'Verified' : 'not verified'}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="loadDoctorSlots(${doc.id})">
                            View Slots
                        </button>
                    </td>
                </tr>
            `;
        }).join('');

        setContent(`
            <h6 class="mb-3">Book Appointment – Select Doctor</h6>

            <div class="mb-3" style="max-width:300px;">
                <input 
                    type="text" 
                    id="doctor-search" 
                    class="form-control form-control-sm"
                    placeholder="Search doctor or specialization..."
                    onkeyup="filterDoctors()"
                >
            </div>

            <table class="table table-sm table-bordered">
                <thead class="table-light">
                    <tr>
                        <th>Name</th>
                        <th>Specialization</th>
                        <th>Experience</th>
                        <th>phonenumber</th>
                        <th>Verified</th>
                        <th></th>
                    </tr>
                </thead>

                <tbody id="doctor-table-body">
                    ${rows}
                </tbody>
            </table>

            <div id="slots-section"></div>
        `);


    } catch (err) {
        setContent('');
        showMessage('danger', 'Failed to load doctors.');
    }
}

function filterDoctors() {
    const input = document.getElementById('doctor-search').value.toLowerCase();

    const rows = document.querySelectorAll('#doctor-table-body tr');

    rows.forEach(function(row) {
        const text = row.innerText.toLowerCase();

        if (text.includes(input)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}


async function loadDoctorSlots(doctorId) {
    const section = document.getElementById('slots-section');
    section.innerHTML = '<p class="text-muted small">Loading slots…</p>';

    try {
        const slots = await fetchJSON(API + '/doctor-slots/' + doctorId + '/');
        const available = slots.filter(s => !s.is_booked);

        if (!available.length) {
            section.innerHTML = '<p class="text-muted small mt-2">No slots available for this doctor.</p>';
            return;
        }

        const byDate = {};
        available.forEach(function(slot) {
            const date = slot.date || 'Unknown';
            if (!byDate[date]) byDate[date] = [];
            byDate[date].push(slot);
        });

        let html = '<h6 class="mt-3 mb-2">Available Slots</h6>';

        Object.keys(byDate).forEach(function(date) {
            html += `<p class="mb-1 small text-muted">${date}</p>`;

            byDate[date].forEach(function(slot) {
                html += `
                    <button class="btn btn-sm btn-outline-secondary me-1 mb-1"
                            id="slot-btn-${slot.id}"
                            onclick="bookSlot(${slot.id})">
                        ${slot.start_time} – ${slot.end_time}
                    </button>
                `;
            });

            html += '<br>';
        });

        section.innerHTML = html;
    } catch (err) {
        section.innerHTML = '<p class="text-danger small">Failed to load slots.</p>';
    }
}

async function bookSlot(slotId) {
    const btn = document.getElementById('slot-btn-' + slotId);
    if (btn) {
        btn.disabled = true;
        btn.textContent = 'Booking…';
    }

    try {
        await fetchJSON(`${API}/appointments/${slotId}/book/`, { method: 'PATCH' });
        showMessage('success', 'Appointment booked! Check "My Appointments" for status.');

        if (btn) {
            btn.textContent = 'Booked';
            btn.classList.replace('btn-outline-secondary', 'btn-success');
        }
    } catch (err) {
        showMessage('danger', formatErrors(err.data) || 'Booking failed.');
        if (btn) {
            btn.disabled = false;
            btn.textContent = 'Retry';
        }
    }
}



async function logout() {
    try {
        const csrf = getCookie('csrftoken');
        await fetch(API + '/api/token/blacklist/', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                ...(csrf ? { 'X-CSRFToken': csrf } : {})
            }
        });
    } catch (e) {
        // Logout failed silently still redirect anyway
    }

    window.location.href = 'login.html';
}