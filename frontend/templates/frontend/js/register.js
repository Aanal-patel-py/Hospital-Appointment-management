console.log("JS LOADED");

document.addEventListener('DOMContentLoaded', function () {
    
    const roleSelect = document.getElementById('role');
    const patientDiv = document.getElementById('patientFields');
    const doctorDiv = document.getElementById('doctorFields');
    const form = document.getElementById('registerForm');
    
    async function loadSpecializations() {
    try {
        const res = await fetch('http://127.0.0.1:8000/specializations/');
        const data = await res.json();

        const select = document.getElementById('specialization');

        data.forEach(spec => {
            const option = document.createElement('option');
            option.value = spec.id; 
            option.textContent = spec.type;
            select.appendChild(option);
        });

    } catch (err) {
        console.error("Failed to load specializations");
    }
}

loadSpecializations();


    function showMessage(type, msg) {
    const el = document.getElementById("responseMessage");
    el.className = `text-${type} mt-3`;
    el.innerText = msg;
}

    roleSelect.addEventListener('change', function () {

        patientDiv.style.display = 'none';
        doctorDiv.style.display = 'none';

        if (this.value === 'PATIENT') {
            patientDiv.style.display = 'block';
        } 
        else if (this.value === 'DOCTOR') {
            doctorDiv.style.display = 'block';
        }
    });


    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const raw = Object.fromEntries(formData.entries());

        console.log("RAW:", raw);

        let data = {
            username: raw.username,
            password: raw.password,
            email: raw.email,
            role: raw.role
        };


        if (raw.role === 'DOCTOR') {
            const select = document.getElementById("specialization");
            const selected = Array.from(select.selectedOptions).map(o => o.value);
            
            data = {
                ...data,
                name: raw.doctor_name,
                years_of_experience: raw.experience,
                gender: raw.doctor_gender,
                phonenumber: raw.doctor_phone,
                specialization: selected 
            };
        } 
        else if (raw.role === 'PATIENT') {
            data = {
                ...data,
                name: raw.patient_name,
                age: raw.age,
                bloodgroup: raw.bloodgroup,
                gender: raw.patient_gender,
                phonenumber: raw.patient_phone,
                height: raw.height,
                weight: raw.weight,
                city: raw.city
            };
        }

        console.log("FINAL PAYLOAD:", data);

       try {
    const response = await fetch('http://127.0.0.1:8000/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    const result = await response.json(); 
    if (response.ok) {
        showMessage('success', "Registration successful! Redirecting...");
        setTimeout(() => {
            window.location.href = "login.html";
        }, 1000);
    } else {
 
        let errorMsg = "";

        if (result.username) {
            errorMsg = result.username[0];
        } else if (result.email) {
            errorMsg = result.email[0];
        } else if (result.detail) {
            errorMsg = result.detail;
        } else {
            errorMsg = Object.values(result).flat().join(", ");
        }

        showMessage('danger', errorMsg);
    }

} catch (error) {
    console.error("FETCH ERROR:", error);
    showMessage('danger', "Something went wrong.");
}
    });

});