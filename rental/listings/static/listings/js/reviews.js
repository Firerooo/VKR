document.addEventListener("DOMContentLoaded", function () {
    const leaveReviewBtn = document.getElementById("leave-review-btn");
    const authModal = document.getElementById("auth-modal");
    const reviewModal = document.getElementById("review-modal");
    const closeModalBtns = document.querySelectorAll(".review-close-modal, #close-modal");
    const confirmAuthBtn = document.getElementById("confirm-auth");

    leaveReviewBtn.addEventListener("click", function () {
        if (reviewModal) {
            reviewModal.style.display = "flex";
        } else {
            authModal.style.display = "flex";
        }
    });
    
    closeModalBtns.forEach(btn => {
        btn.addEventListener("click", function () {
            this.closest(".review-modal").style.display = "none";
        });
    });

    confirmAuthBtn?.addEventListener("click", function () {
        window.location.href = "/users/login/";
    });

    window.addEventListener("click", function (event) {
        if (event.target === authModal) authModal.style.display = "none";
        if (reviewModal && event.target === reviewModal) reviewModal.style.display = "none";
    });
});
