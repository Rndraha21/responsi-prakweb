const deleteBtn = document.querySelectorAll(".delete-btn");

if (deleteBtn) {
  deleteBtn.forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-id");
      console.log(id);

      Swal.fire({
        title: "Are you sure you want to delete it?",
        text: "Deleted data cannot be recovered!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete!",
      }).then((result) => {
        if (result.isConfirmed) {
          fetch(`/delete/article/${id}`, { method: "POST" })
            .then((res) => res.json())
            .then((data) => {
              if (data.success) {
                btn.closest(".card-featured").remove();
                Swal.fire("Deleted!", "Article has been deleted.", "success");
              }
            });
        }
      });
    });
  });
}

const statusBtn = document.querySelectorAll(".status-btn");
if (statusBtn) {
  statusBtn.forEach((btn) => {
    btn.addEventListener("click", () => {
      const articleId = btn.getAttribute("data-id");
      const action = btn.getAttribute("data-value");

      fetch(`/admin/update/${articleId}/${action}`, { method: "POST" })
        .then((res) => res.json())
        .then((data) => {
          btn.closest(".card-featured").remove();
          Swal.fire("Updated!", "Status has been udpated.", "success");
        });
    });
  });
}

const filterAll = document.querySelector(
  'input[name="filter-all"][type="checkbox"]:not([value])'
);
const gameCheckboxes = document.querySelectorAll('input[name="game"][value]');
const articleCards = document.querySelectorAll(".card-featured");
const empty = document.getElementById("admin-empty-state");

function filterArticles() {
  const activeFilters = Array.from(gameCheckboxes)
    .filter((i) => i.checked)
    .map((i) => i.value);

  let adaYangTampil = false;

  articleCards.forEach((card) => {
    const cardGame = card.dataset.game;

    const isMatched =
      filterAll.checked ||
      activeFilters.length === 0 ||
      activeFilters.includes(cardGame);

    if (isMatched) {
      card.style.display = "block";
      adaYangTampil = true;
    } else {
      card.style.display = "none";
    }
  });

  if (adaYangTampil) {
    empty.classList.add("d-none");
  } else {
    empty.classList.remove("d-none");
  }
}

filterAll.addEventListener("change", () => {
  if (filterAll.checked) {
    gameCheckboxes.forEach((cb) => (cb.checked = false));
  }
  filterArticles();
});

gameCheckboxes.forEach((cb) => {
  cb.addEventListener("change", () => {
    if (cb.checked) {
      filterAll.checked = false;
    }
    filterArticles();
  });
});
