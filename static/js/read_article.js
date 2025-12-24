const likeBtns = document.querySelectorAll(".btn-like");

if (likeBtns) {
  likeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const articleId = btn.getAttribute("data-id");
      const icon = btn.querySelector(".heart-icon");
      const countEl = btn.querySelector(".count-element");

      data = fetch(`/like/article/${articleId}`)
        .then((res) => {
          if (res.redirected) {
            Swal.fire({
              title: "Login Required",
              text: "Please login, so you can like this article.",
              icon: "warning",
              showCancelButton: true,
              confirmButtonText: "Login",
              cancelButtonText: "Later",
              confirmButtonColor: "#9d5aef",
            }).then((result) => {
              if (result.isConfirmed) {
                window.location.href = res.url;
              }
            });
            return;
          }
          return res.json();
        })
        .then((data) => {
          if (data) {
            const isLiked = data.status == "liked";

            if (isLiked) {
              icon.classList.replace("bi-heart", "bi-heart-fill");
            } else {
              icon.classList.replace("bi-heart-fill", "bi-heart");
            }
            countEl.innerText = data.total_likes;
          }
        })
        .catch((err) => console.log(err));
    });
  });
}

const shareBtns = document.querySelectorAll(".share-btn");

if (shareBtns) {
  shareBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const url = btn.dataset.url;

      Swal.fire({
        title: "Share Article",
        html: `
          <p>Share this link to your friend:</p>
          <div class="input-group mb-3">
            <input type="text" id="share-link" class="form-control" value="${url}" readonly>
            <button class="btn btn-primary" style="background-color: #9d5aef;" onclick="copyLink()">
               Copy
            </button>
          </div>
        `,
        showConfirmButton: false,
        showCloseButton: true,
      });
    });
  });
}

function copyLink() {
  const copyText = document.getElementById("share-link");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(copyText.value);

  Swal.fire({
    icon: "success",
    title: "Copied!",
    text: "Link copied, don't forget to share it!",
    timer: 1500,
    showConfirmButton: false,
  });
}
