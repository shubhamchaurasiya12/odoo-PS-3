document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
  
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
  
    if (!email || !password) {
      alert("Please fill in both fields.");
      return;
    }
  
    try {
      const res = await fetch('https://your-backend-api.com/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });
  
      const data = await res.json();
  
      if (res.ok) {
        localStorage.setItem('authToken', data.token);
        alert("Login Successful!");
        window.location.href = "dashboard.html"; // Change this if needed
      } else {
        alert(data.message || "Login Failed. Please try again.");
      }
  
    } catch (error) {
      console.error("Login error:", error);
      alert("Something went wrong. Please try again later.");
    }
  });
  