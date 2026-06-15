console.log("JS Loaded");

function toggleSidebar() {
    let sidebar = document.getElementById("sidebar");
    let content = document.getElementById("mainContent");

    sidebar.classList.toggle("hide");

    if (sidebar.classList.contains("hide")) {
        content.classList.remove("col-md-10");
        content.classList.add("col-md-12");
    } else {
        content.classList.remove("col-md-12");
        content.classList.add("col-md-10");
    }
}
// OTP FUNCTION
function sendOTP() {

    let mobilenumber = document.getElementById("mobile").value;

    fetch("/forgot-password/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: "mobilenumber=" + mobilenumber
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("mobileError").innerHTML = "";
        // OPEN OTP POPUP
          if (data.otp_sent) {

        var modal = new bootstrap.Modal(document.getElementById('otpModal'));
        modal.show();   // ✅ THIS OPENS YOUR POPUP

    } else {
    document.getElementById("mobileError").innerHTML =
        "Wrong Mobile Number";
    }

    });
}


// CSRF FUNCTION (IMPORTANT FOR DJANGO)
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}
function fillDetails() {

    let select = document.getElementById("vehicleType");

    let selected = select.options[select.selectedIndex];

    if (!selected.value) {
        document.getElementById("areaNumber").value = "";
        document.getElementById("parkingCharge").value = "";
        return;
    }

    document.getElementById("areaNumber").value =
        selected.getAttribute("data-area");

    document.getElementById("parkingCharge").value =
        selected.getAttribute("data-charge");
}
function verifyOTP() {

    let otp = document.getElementById("otpInput").value;

    fetch("/verify-otp/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: "otp=" + otp
    })
    .then(res => res.json())
    .then(data => {

        if (data.success) {

            // close OTP modal
            var otpModal = bootstrap.Modal.getInstance(document.getElementById('otpModal'));
            otpModal.hide();

            // open new password modal
            var passModal = new bootstrap.Modal(document.getElementById('passwordModal'));
            passModal.show();

        } else {
            alert("Wrong OTP");
        }
    });
}
function savePassword() {

    let password = document.getElementById("newPassword").value;

    if (!password) {
        alert("Please enter password");
        return;
    }

    fetch("/reset-password/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: "new_password=" + encodeURIComponent(password)
    })
    .then(res => res.json())
    .then(data => {

        if (data.success) {

            alert("Password Updated Successfully");

            var modal = bootstrap.Modal.getInstance(
                document.getElementById('passwordModal')
            );
            modal.hide();

            window.location.href = "/";

        } else {
            alert("Failed to update password");
        }
    });
}
document.addEventListener("DOMContentLoaded", function () {

    const input = document.getElementById("vehicle_number");

    input.addEventListener("keyup", function () {

        let value = this.value;

        fetch(`/search-vehicle/?vehicle_number=${value}`)
        .then(response => response.json())
        .then(data => {

            let tbody = document.getElementById("vehicle-results");

            tbody.innerHTML = "";

            data.forEach(v => {

                tbody.innerHTML += `
                <tr>
                    <td>${v.id}</td>
                    <td>${v.vehicle_number}</td>
                    <td>${v.vehicle_type}</td>
                    <td>${v.area_no}</td>
                    <td>${v.charge}</td>
                    <td>${v.status}</td>
                </tr>`;
            });

        });

    });

});
document.getElementById('vehicleSearch').addEventListener('keyup', function() {

    let value = this.value;

    fetch(`/search-vehicle/?vehicle_number=${value}`)
    .then(response => response.json())
    .then(data => {

        let tbody = document.getElementById('vehicle-results');

        tbody.innerHTML = '';

        data.forEach(v => {

            tbody.innerHTML += `
            <tr>
                <td>${v.id}</td>
                <td>${v.vehicle_number}</td>
                <td>${v.vehicle_type}</td>
                <td>${v.area_no}</td>
                <td>${v.charge}</td>
                <td>${v.status}</td>
                <td>${v.arrival_time}</td>
            </tr>`;
        });

    });

});