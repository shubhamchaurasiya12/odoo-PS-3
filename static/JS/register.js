document.getElementById('signupForm').addEventListener('submit', async function(e) {
  e.preventDefault();

  const name = document.getElementById('name').value.trim();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirmPassword').value;
  const spinner = document.getElementById('spinner');
  const signupBtn = document.getElementById('signupBtn');

  if (!name || !email || !password || !confirmPassword) {
    alert("All fields are required.");
    return;
  }

  if (password !== confirmPassword) {
    alert("Passwords do not match.");
    return;
  }

  // Show loading spinner
  spinner.style.display = 'inline-block';
  signupBtn.disabled = true;

  try {
    const res = await fetch('/register', {
      method: 'POST',
      body: new URLSearchParams({
        name,
        email,
        password,
        confirmPassword
      })
    });

    const data = await res.json();

    if (res.ok) {
      alert("Signup successful! Redirecting...");
      window.location.href = "/dashboard";
    } else {
      alert(data.error || "Signup failed. Try again.");
    }

  } catch (error) {
    console.error("Signup error:", error);
    alert("Something went wrong. Please try again later.");
  } finally {
    spinner.style.display = 'none';
    signupBtn.disabled = false;
  }
});
