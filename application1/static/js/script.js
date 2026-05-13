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