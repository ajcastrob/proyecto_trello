import Sortable from "sortablejs";

function getCookie(name) {
  const m = document.cookie.match(new RegExp("(^|;)\\s*" + name + "=([^;]+)"));
  return m ? m[2] : "";
}

function collectOrder(listEl) {
  return [...listEl.children].map((c) => c.dataset.pk).filter(Boolean);
}

function persistList(listEl) {
  const listId = listEl.dataset.sortable;
  if (!listId) return;

  const order = collectOrder(listEl);
  fetch(`/task/details/${listId}/reorder/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ order }),
  });
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-sortable]").forEach((el) => {
    Sortable.create(el, {
      group: "tasks",
      animation: 150,
      ghostClass: "opacity-40",
      draggable: "[data-pk]",
      emptyInsertThreshold: 24,
      onEnd: (evt) => {
        // Persist destination list (and source if moved across lists)
        if (evt.to) persistList(evt.to);
        if (evt.from && evt.from !== evt.to) persistList(evt.from);
      },
    });
  });
});
