document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const username = document.getElementById('username');
    const email = document.getElementById('email');
    const firstName = document.getElementById('firstname');
    const lastName = document.getElementById('lastname');
    const contactNumber = document.getElementById('contact_number');
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    const profileImage = document.getElementById('profile_image');

    const usernameError = document.createElement('span');
    const emailError = document.createElement('span');
    const contactError = document.createElement('span');
    const password1Error = document.createElement('span');
    const password2Error = document.createElement('span');
    const imageError = document.createElement('span');

    // Insert error messages after each input field
    username.parentNode.appendChild(usernameError);
    email.parentNode.appendChild(emailError);
    contactNumber.parentNode.appendChild(contactError);
    password1.parentNode.appendChild(password1Error);
    password2.parentNode.appendChild(password2Error);
    profileImage.parentNode.appendChild(imageError);

    // Username validation: Only alphabets, at least 4 characters
    username.addEventListener('input', function() {
        const usernamePattern = /^[A-Za-z]{4,}$/; // Ensures at least 4 alphabetic characters
        if (!usernamePattern.test(username.value)) {
            usernameError.textContent = 'Username must be at least 4 alphabets.';
            usernameError.style.color = 'red';
        } else {
            usernameError.textContent = '';
        }
    });

    // Email validation
    email.addEventListener('input', function() {
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailPattern.test(email.value)) {
            emailError.textContent = 'Please enter a valid email address.';
            emailError.style.color = 'red';
        } else {
            emailError.textContent = '';
        }
    });

    // First Name validation: Only alphabets
    firstName.addEventListener('input', function() {
        const namePattern = /^[A-Za-z]+$/;
        if (!namePattern.test(firstName.value)) {
            firstNameError.textContent = 'First Name must only contain alphabets.';
            firstNameError.style.color = 'red';
        } else {
            firstNameError.textContent = '';
        }
    });

    // Last Name validation: Only alphabets
    lastName.addEventListener('input', function() {
        const namePattern = /^[A-Za-z]+$/;
        if (!namePattern.test(lastName.value)) {
            lastNameError.textContent = 'Last Name must only contain alphabets.';
            lastNameError.style.color = 'red';
        } else {
            lastNameError.textContent = '';
        }
    });

    // Contact Number validation: 10 digits
    contactNumber.addEventListener('input', function() {
        const phonePattern = /^[0-9]{10}$/;
        if (!phonePattern.test(contactNumber.value)) {
            contactError.textContent = 'Contact number must be 10 digits.';
            contactError.style.color = 'red';
        } else {
            contactError.textContent = '';
        }
    });

    // Password validation: At least 8 characters
    password1.addEventListener('input', function() {
        if (password1.value.length < 8) {
            password1Error.textContent = 'Password must be at least 8 characters.';
            password1Error.style.color = 'red';
        } else {
            password1Error.textContent = '';
        }
    });

    // Confirm Password validation: Must match Password
    password2.addEventListener('input', function() {
        if (password2.value !== password1.value) {
            password2Error.textContent = 'Passwords do not match.';
            password2Error.style.color = 'red';
        } else {
            password2Error.textContent = '';
        }
    });

    // Profile Image validation: Only JPEG, PNG, JPG
    profileImage.addEventListener('change', function() {
        const allowedImageTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        if (!allowedImageTypes.includes(profileImage.files[0]?.type)) {
            imageError.textContent = 'Please upload a valid image (JPEG, PNG, JPG).';
            imageError.style.color = 'red';
        } else {
            imageError.textContent = '';
        }
    });

    // Form submission validation
    form.addEventListener('submit', function(event) {
        if (usernameError.textContent || emailError.textContent || contactError.textContent || password1Error.textContent || password2Error.textContent || imageError.textContent) {
            event.preventDefault();
            alert('Please correct the errors before submitting.');
        }
    });
});
