username=document.getElementById('username')
password=document.getElementById('password')
form=document.getElementById('loginform')


document.addEventListener('DOMContentLoaded',function (){

form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        console.log(formData)
        const raw = Object.fromEntries(formData.entries()); //see boths difference deeply
        let data = {
            username: raw.username,
            password: raw.password,
        }

        console.log("RAW:", raw);
        try {
            const response = await fetch('http://127.0.0.1:8000/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials:'include',
                body: JSON.stringify(data)
            });

            const text = await response.text();

            if (response.ok) {
            window.location.href = 'dashboard.html'; 
           
            }
            
        

        } catch (error) {
            console.error("FETCH ERROR:", error);
        }
    });
});
