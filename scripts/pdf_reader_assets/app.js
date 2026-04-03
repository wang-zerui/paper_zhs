(() => {
  const body = document.body;

  const normalize = (value) => (value || "").toString().trim().toLowerCase();
  const isTypingTarget = (target) => {
    if (!(target instanceof HTMLElement)) {
      return false;
    }
    return (
      target.tagName === "INPUT" ||
      target.tagName === "TEXTAREA" ||
      target.isContentEditable
    );
  };

  const librarySearch = document.querySelector("[data-library-search]");
  const libraryCards = [...document.querySelectorAll("[data-card]")];
  const filterChips = [...document.querySelectorAll("[data-filter-chip]")];
  const libraryResults = document.querySelector("[data-library-results]");
  const randomButton = document.querySelector("[data-random-open]");

  let activeFilter = "all";

  const visibleLibraryCards = () =>
    libraryCards.filter((card) => !card.classList.contains("is-hidden"));

  const updateLibrary = () => {
    if (!libraryCards.length) {
      return;
    }

    const query = normalize(librarySearch?.value);
    let visible = 0;

    libraryCards.forEach((card) => {
      const matchesQuery =
        !query ||
        normalize(card.dataset.title).includes(query) ||
        normalize(card.dataset.path).includes(query) ||
        normalize(card.dataset.badge).includes(query);
      const matchesFilter =
        activeFilter === "all" || normalize(card.dataset.badge) === activeFilter;
      const shown = matchesQuery && matchesFilter;
      card.classList.toggle("is-hidden", !shown);
      if (shown) {
        visible += 1;
      }
    });

    if (libraryResults) {
      libraryResults.textContent = `显示 ${visible} / ${libraryCards.length} 篇`;
    }
  };

  if (librarySearch) {
    librarySearch.addEventListener("input", updateLibrary);
  }

  filterChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      activeFilter = normalize(chip.dataset.filter) || "all";
      filterChips.forEach((item) => item.classList.toggle("is-active", item === chip));
      updateLibrary();
    });
  });

  if (randomButton) {
    randomButton.addEventListener("click", () => {
      const candidates = visibleLibraryCards();
      if (!candidates.length) {
        return;
      }
      const chosen = candidates[Math.floor(Math.random() * candidates.length)];
      const link = chosen.querySelector("a.button.primary");
      if (link instanceof HTMLAnchorElement) {
        window.location.href = link.href;
      }
    });
  }

  const sidebarSearch = document.querySelector("[data-sidebar-search]");
  const sidebarItems = [...document.querySelectorAll("[data-sidebar-item]")];

  const updateSidebar = () => {
    if (!sidebarItems.length) {
      return;
    }
    const query = normalize(sidebarSearch?.value);
    sidebarItems.forEach((item) => {
      const shown =
        !query ||
        normalize(item.dataset.title).includes(query) ||
        normalize(item.dataset.path).includes(query) ||
        normalize(item.dataset.badge).includes(query);
      item.classList.toggle("is-hidden", !shown);
    });
  };

  if (sidebarSearch) {
    sidebarSearch.addEventListener("input", updateSidebar);
  }

  const drawerToggles = [...document.querySelectorAll("[data-drawer-toggle]")];
  const openDrawer = () => body.classList.add("drawer-open");
  const closeDrawer = () => body.classList.remove("drawer-open");

  drawerToggles.forEach((toggle) => {
    toggle.addEventListener("click", () => {
      body.classList.toggle("drawer-open");
    });
  });

  sidebarItems.forEach((item) => {
    item.addEventListener("click", () => {
      closeDrawer();
    });
  });

  const copyButton = document.querySelector("[data-copy-link]");
  if (copyButton) {
    copyButton.addEventListener("click", async () => {
      const originalLabel = copyButton.textContent;
      try {
        await navigator.clipboard.writeText(window.location.href);
        copyButton.textContent = "已复制";
      } catch {
        copyButton.textContent = "复制失败";
      }
      window.setTimeout(() => {
        copyButton.textContent = originalLabel;
      }, 1400);
    });
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "/" && !isTypingTarget(event.target)) {
      event.preventDefault();
      (sidebarSearch || librarySearch)?.focus();
      return;
    }

    if (event.key === "Escape") {
      closeDrawer();
      return;
    }

    if (isTypingTarget(event.target) || body.dataset.page !== "reader") {
      return;
    }

    if (event.key.toLowerCase() === "j") {
      document.querySelector("[data-nav-next]")?.click();
    }

    if (event.key.toLowerCase() === "k") {
      document.querySelector("[data-nav-prev]")?.click();
    }
  });

  updateLibrary();
  updateSidebar();
})();
