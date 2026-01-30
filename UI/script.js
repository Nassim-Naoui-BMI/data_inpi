document.addEventListener("DOMContentLoaded", () => {
  // --- Éléments du DOM ---
  // Navigation
  const tabButtons = document.querySelectorAll(".tab-button");
  const tabSections = document.querySelectorAll(".tab-section");

  // Shutdown server
  const shutDownButton = document.getElementById("shutdown-server-button");
  const toolTipShutdown = document.getElementById("tool-tip-shutdown");

  shutDownButton.addEventListener("click", () => {
    shutDownServer();
  });

  shutDownButton.addEventListener("mouseover", () => {
    toolTipShutdown.classList.remove("hidden");
  });

  shutDownButton.addEventListener("mouseout", () => {
    toolTipShutdown.classList.add("hidden");
  });

  // Recherche Unique
  const searchButtonSingle = document.getElementById("search-button");
  const searchInput = document.getElementById("search-input");
  const resultsListSingle = document.getElementById("results-list-single");
  const loaderSingle = document.getElementById("loader-single");
  const errorMessageSingle = document.getElementById("error-message-single");
  const noResultsSingle = document.getElementById("no-results-single");
  const singleExportButton = document.getElementById("single-export-button");
  const singleTokenButton = document.getElementById("single-token-button");
  const singleTokenActif = document.getElementById("single-token-actif");
  const singleTokenInactif = document.getElementById("single-token-inactif");
  let lastSingleResults = []; // Pour l'export

  // Recherche Multiple
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");
  const multipleStatus = document.getElementById("multiple-status");
  const fileNameDisplay = document.getElementById("file-name-display");
  const totalCompaniesDisplay = document.getElementById(
    "total-companies-display"
  );
  const companiesFoundDisplay = document.getElementById(
    "companies-found-display"
  );
  const progressBar = document.getElementById("progress-bar");
  const multipleStartButton = document.getElementById("multiple-start-button");
  const multipleMissingtButton = document.getElementById(
    "multiple-missing-export-button"
  );
  const multipleExportButton = document.getElementById(
    "multiple-export-button"
  );
  const multipleTokenButton = document.getElementById("multiple-token-button");
  const multipleTokenActif = document.getElementById("multiple-token-actif");
  const multipleTokenInactif = document.getElementById(
    "multiple-token-inactif"
  );
  let companiesToSearch = [];
  let multipleSearchResults = [];
  let multipleResultsMissing = [];

  // --- Logique de Navigation (Tabs) ---
  let currentSection = "section-single";
  let isSingleSectionActive =
    currentSection === "section-single" ? true : false;

  function switchTab(targetId) {
    tabSections.forEach((section) => {
      section.classList.add("hidden");
    });
    document.getElementById(targetId).classList.remove("hidden");

    tabButtons.forEach((button) => {
      button.style.borderColor =
        button.dataset.target === targetId ? "#3b82f6" : "transparent";
      button.style.color =
        button.dataset.target === targetId ? "#1f2937" : "#6b7280";
    });
  }

  tabButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      switchTab(e.currentTarget.dataset.target);
      currentSection = e.currentTarget.dataset.target;
      isSingleSectionActive =
        currentSection === "section-single" ? true : false;
      switchTokenStatus(isSingleSectionActive);
    });
  });

  // Initialisation: afficher la première section par défaut
  switchTab(currentSection);

  // --- Fonctions d'Action Globales ---

  // Chargement du statut du token

  const TOKEN_STATUS_KEY = "isTokenActive";
  const LAST_REFRESH_KEY = "lastRefresh";
  const EXPIRATION_HOURS = 1;

  function saveTokenStatusLocalStorage(status) {
    localStorage.setItem(TOKEN_STATUS_KEY, String(status));
    const refreshDate = Date.now();
    const date = new Date(refreshDate);
    localStorage.setItem(LAST_REFRESH_KEY, refreshDate);
    localStorage.setItem("date", date.toUTCString());
  }

  function loadTokenStatusLocalStorage() {
    const statusString = localStorage.getItem(TOKEN_STATUS_KEY);
    const lastRefreshString = localStorage.getItem(LAST_REFRESH_KEY);

    if (statusString === null || lastRefreshString === null) {
      saveTokenStatusLocalStorage(false);
      return false;
    }

    const isTokenActive = statusString === "true";
    const lastRefreshTime = Number(lastRefreshString);

    if (!isTokenActive || isNaN(lastRefreshTime)) {
      return false;
    }

    const expirationLimitMs = EXPIRATION_HOURS * 60 * 60 * 1000;
    const isExpired = Date.now() - lastRefreshTime >= expirationLimitMs;

    if (isExpired) {
      saveTokenStatusLocalStorage(false);
      return false;
    }

    return true;
  }

  function switchTokenStatus(section) {
    const currentTokenStatus = loadTokenStatusLocalStorage();

    if (section) {
      currentTokenStatus
        ? (singleTokenInactif.classList.add("hidden"),
          singleTokenActif.classList.remove("hidden"))
        : (singleTokenActif.classList.add("hidden"),
          singleTokenInactif.classList.remove("hidden"));
    } else {
      currentTokenStatus
        ? (multipleTokenInactif.classList.add("hidden"),
          multipleTokenActif.classList.remove("hidden"))
        : (multipleTokenActif.classList.add("hidden"),
          multipleTokenInactif.classList.remove("hidden"));
    }
  }

  switchTokenStatus(isSingleSectionActive);

  function refreshAuthToken() {
    fetch("http://127.0.0.1:5000/token", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("✅ Token reçu :", data);
        saveTokenStatusLocalStorage(true);
        switchTokenStatus(isSingleSectionActive);
      })
      .catch((error) => {
        console.error("❌ Erreur :", error);
        saveTokenStatusLocalStorage(false);
      });
  }

  // Exporter en Excel (Mock/Utilitaire)
  async function exportToExcel(data) {
    if (data.length === 0) {
      alert("❌ Aucune donnée à exporter.");
      return;
    }

    fetch("http://127.0.0.1:5000/getExcel", {
      method: "POST", // 'POST'
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        // Vérifie si la réponse est OK (statut 200-299)
        if (!response.ok) {
          throw new Error(`Erreur HTTP! Statut: ${response.status}`);
        }
        // Tente de parser la réponse du serveur en JSON (si le serveur renvoie du JSON)
        return response.json();
      })
      .then((data) => {
        console.log("✅ Réponse du serveur (données reçues):", data);
        alert("✅ Exportation terminée avec succès");
      })
      .catch((error) => {
        console.error("Erreur lors de la requête:", error);
      });
  }

  function exportToExcelMissingElement(data, filename) {
    if (data.length === 0) {
      alert("❌ Aucune donnée à exporter.");
      return;
    }
    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Résultats Manquants INPI");
    XLSX.writeFile(wb, filename);
    alert(`✅ Exportation de ${data.length} compte(s) réussie!`);
  }

  singleTokenButton.addEventListener(
    "click",
    () => refreshAuthToken("unique"),
    switchTokenStatus(isSingleSectionActive)
  );
  multipleTokenButton.addEventListener(
    "click",
    () => refreshAuthToken("multiple"),
    switchTokenStatus(isSingleSectionActive)
  );

  // --- Logique de la Recherche Unique ---
  searchButtonSingle.addEventListener("click", performSearchSingle);
  searchInput.addEventListener("keyup", (event) => {
    if (event.key === "Enter") {
      performSearchSingle();
    }
  });
  singleExportButton.addEventListener("click", () => {
    // Utiliser les derniers résultats pour l'export
    exportToExcel(lastSingleResults);
  });

  async function performSearchSingle() {
    const query = searchInput.value.trim();
    const searchType = document.querySelector(
      'input[name="search-type"]:checked'
    ).value;

    if (!query) {
      alert("⚠️ Veuillez entrer un terme de recherche.");
      return;
    }

    // Reset UI
    resultsListSingle.innerHTML = "";
    errorMessageSingle.classList.add("hidden");
    noResultsSingle.classList.add("hidden");
    loaderSingle.classList.remove("hidden");
    lastSingleResults = [];

    try {
      const data = await mockApiCallSingle(query, searchType);

      loaderSingle.classList.add("hidden");

      if (data && data.results && data.total_results > 0) {
        lastSingleResults = data.results;
        displayResultsSingle(data.results);
        singleExportButton.disabled = false;
      } else {
        noResultsSingle.classList.remove("hidden");
        singleExportButton.disabled = true;
      }
    } catch (error) {
      console.error("Search failed:", error);
      loaderSingle.classList.add("hidden");
      errorMessageSingle.classList.remove("hidden");
      singleExportButton.disabled = true;
    }
  }

  function formatAddress(company) {
    let address = "Non disponible";

    address = `${company.voie || ""} ${company.codePostal || ""} ${
      company.commune || ""
    }`.trim();

    return address;
  }

  function displayResultsSingle(companies) {
    companies.forEach((company) => {
      const companyCard = document.createElement("div");
      companyCard.className =
        "bg-gray-50 border border-gray-200 p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300";
      const address = formatAddress(company);

      companyCard.innerHTML = `
                        <div class="flex flex-col sm:flex-row justify-between sm:items-center mb-3">
                            <h3 class="text-xl font-bold text-gray-900">${
                              company.denomination || "Nom Inconnu"
                            }</h3>
                            <span class="text-sm font-mono bg-blue-100 text-blue-800 px-2 py-1 rounded-md mt-2 sm:mt-0">SIREN: ${
                              company.siren
                            }</span>
                        </div>
                        <p class="text-gray-600"><strong class="font-medium text-gray-800">SIRET:</strong> ${
                          company.siret
                        }</p>
                        <p class="text-gray-600"><strong class="font-medium text-gray-800">Forme juridique:</strong> ${
                          company.formeJuridique
                        }</p>
                        <p class="text-gray-600"><strong class="font-medium text-gray-800">Adresse:</strong> ${address}</p>
                    `;
      resultsListSingle.appendChild(companyCard);
    });
  }

  // --- Logique de la Recherche Multiple ---

  // 1. Gestion du Drag and Drop
  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    const files = e.dataTransfer.files;
    if (files.length) {
      processFile(files[0]);
    }
  });

  dropzone.addEventListener("click", () => {
    fileInput.click();
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length) {
      processFile(e.target.files[0]);
    }
  });

  // 2. Traitement du fichier Excel
  function processFile(file) {
    if (!file.name.match(/\.(xlsx|xls)$/)) {
      alert("⚠️ Veuillez déposer un fichier Excel (.xlsx ou .xls).");
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: "array" });
        const firstSheet = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[firstSheet];

        // Convertir la feuille en JSON
        const json = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

        // Assumer que la première ligne contient les en-têtes (Nom ou SIREN)
        const headers = json[0];
        const sirenIndex = headers.findIndex((h) =>
          h.toUpperCase().includes("SIREN")
        );
        const nameIndex = headers.findIndex((h) =>
          h.toUpperCase().includes("NAME")
        );

        if (sirenIndex === -1 && nameIndex === -1) {
          alert(
            "⚠️ Le fichier doit contenir une colonne nommée 'SIREN' ou 'NAME'."
          );
          return;
        }

        // Préparer la liste des entreprises à rechercher (exclure l'en-tête)
        companiesToSearch = json
          .slice(1)
          .map((row) => {
            // On priorise le SIREN s'il est présent
            if (sirenIndex !== -1 && row[sirenIndex]) {
              return { type: "siren", query: String(row[sirenIndex]).trim() };
            }
            if (nameIndex !== -1 && row[nameIndex]) {
              return { type: "name", query: String(row[nameIndex]).trim() };
            }
            return null; // Ligne vide ou sans donnée pertinente
          })
          .filter((item) => item !== null);

        if (companiesToSearch.length === 0) {
          alert(
            "❌ Aucune donnée d'entreprise valide trouvée dans le fichier."
          );
          return;
        }
        console.log(companiesToSearch);

        // Affichage du statut
        fileNameDisplay.textContent = `Fichier traité : ${file.name}`;
        totalCompaniesDisplay.textContent = `${companiesToSearch.length} entreprises prêtes pour la recherche.`;
        multipleStatus.classList.remove("hidden");
        companiesFoundDisplay.textContent = "0 entreprises trouvées";
        progressBar.style.width = "0%";
        multipleStartButton.classList.remove("hidden");
        multipleStartButton.disabled = false;
        multipleExportButton.disabled = true; // Désactiver l'export tant qu'aucune recherche n'est faite
        multipleSearchResults = []; // Réinitialiser les résultats
      } catch (error) {
        console.error("❌ Erreur de lecture du fichier Excel:", error);
        alert(
          "❌ Erreur lors de la lecture du fichier. Assurez-vous qu'il est bien formaté."
        );
      }
    };
    reader.readAsArrayBuffer(file);
  }

  // 3. Lancement de la Recherche Multiple
  multipleStartButton.addEventListener("click", performSearchMultiple);
  multipleExportButton.addEventListener("click", () => {
    exportToExcel(
      multipleSearchResults,
      "Recherche_Multiple_INPI_Resultats.xlsx"
    );
  });
  multipleMissingtButton.addEventListener("click", () => {
    exportToExcelMissingElement(
      multipleResultsMissing,
      "Liste_Des_Manquants.xlsx"
    );
  });

  async function performSearchMultiple() {
    if (companiesToSearch.length === 0) {
      alert("⚠️ Veuillez d'abord charger un fichier avec des entreprises.");
      return;
    }

    multipleStartButton.disabled = true;
    multipleMissingtButton.disabled = true;
    multipleSearchResults = [];
    multipleResultsMissing = [];
    let foundCount = 0;

    for (let i = 0; i < companiesToSearch.length; i++) {
      const company = companiesToSearch[i];

      try {
        const data = await mockApiCallSingle(company.query, company.type)

        if (data && data.results && data.results.length > 0) {
          foundCount++;
          // Ajouter le résultat à la liste pour l'export
          multipleSearchResults.push(data.results[0]);
        } else if (data.results.length === 0) {
          company.type === "siren"
            ? multipleResultsMissing.push({
                SIREN: company.query,
              })
            : multipleResultsMissing.push({
                NAME: company.query,
              });
          console.log(`⚠️ Missing result : ${company.query}`);
        }
      } catch (error) {
        console.error(`❌ Erreur de recherche pour ${company.query}:`, error);
        // Logique pour gérer les erreurs pour une entreprise spécifique si nécessaire
      }

      // Mise à jour de la barre de progression et du compte
      const progress = ((i + 1) / companiesToSearch.length) * 100;
      progressBar.style.width = `${progress}%`;
      companiesFoundDisplay.textContent = `${foundCount} entreprises trouvées`;
    }
    alert(
      `✅ Recherche multiple terminées. ${foundCount} entreprises trouvées sur ${companiesToSearch.length}.`
    );
    multipleStartButton.disabled = false;
    multipleExportButton.disabled = foundCount === 0;
    if (foundCount < companiesToSearch.length) {
      multipleMissingtButton.disabled = false;
    }
  }

  // --- Fonctions Mock (À remplacer par l'API backend) ---

  async function mockApiCallSingle(query, type) {
    console.log(`⏳ Mock searching for "${query}" by "${type}"`);

    // 1. Simuler délai réseau
    await new Promise((resolve) => setTimeout(resolve, 500));

    try {
      // 2. Utiliser await pour attendre la réponse de fetch
      const response = await fetch(
        `http://127.0.0.1:5000/inpi/${type}/${query}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      // Gérer les erreurs HTTP (404, 500, etc.)
      if (!response.ok) {
        // Créer une erreur personnalisée avec le statut
        if (response.status === 429) {
          alert("🟠 Le quota de requêtes journalier a été dépassé. Réessayez dans 24H ⏳")
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      }

      // 3. Utiliser await pour attendre la conversion JSON
      const data = await response.json();

      console.log(`✅ API Call accepted for : ${query}`);

      // 4. La fonction async renvoie cette valeur (elle sera la valeur de la promesse résolue)
      if (type === "siren") {
        return {
          total_results: 1,
          results: [data],
        };
      } else if (type === "name") {
        return {
          total_results: data.length,
          results: data,
        };
      }
    } catch (error) {
      // 5. Gérer les erreurs réseau ou HTTP
      console.error("❌ Erreur lors de l'appel API :", error.message);
      // Retourner un résultat vide en cas d'échec
      return { total_results: 0, results: [] };
    }
  }

  // A lier à un bouton "Quitter l'application"
  function shutDownServer() {
    confirm("Êtes-vous sûr de vouloir fermer le serveur ?");

    console.log("Envoi de l'ordre d'arrêt au serveur...");

    fetch("http://127.0.0.1:5000/shutdown", {
      method: "POST",
    }).catch((error) => {
      console.warn("Connexion au serveur perdue (arrêt normal).");
    });

    // setTimeout(() => {
    //   window.close();
    // }, 500);
  }
});

window.addEventListener("beforeunload", (event) => {
  navigator.sendBeacon("http://127.0.0.1:5000/shutdown");
});
