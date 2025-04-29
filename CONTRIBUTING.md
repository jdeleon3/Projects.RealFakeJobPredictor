# Contributing Guidelines

Thank you for contributing to this project! To ensure smooth collaboration and avoid accidental overwrites, please follow the process below for making changes and resolving merge conflicts safely — especially when working with Jupyter notebooks.

---

## Branching Workflow

1. **Pull the latest `main` branch:**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create a new feature branch:**
   ```bash
   git checkout -b topics/your-feature-name
   ```

---

## Making Changes

- Work on your feature or fixes within your branch.
- Save your changes regularly.
- Commit only related changes with clear messages:
  ```bash
  git add .
  git commit -m "Describe your changes clearly"
  ```

---

## Syncing with `main` and Conflict Resolution

Before pushing your changes or creating a pull request:

1. **Pull the latest changes from `main`:**
   ```bash
   git pull origin main
   ```

2. If **merge conflicts occur** (especially with `.ipynb` files), resolve them carefully:

   ### Notebook Conflict Resolution
   - We use **`nbdime`** for notebook-aware merge handling.
   - To launch the merge tool:
     ```bash
     git mergetool
     ```
   - This provides a side-by-side interface to review and merge notebook conflicts **cell-by-cell**.
   - After resolving, add the resolved files:
     ```bash
     git add <resolved-files>
     git commit
     ```

3. For **other file types** (e.g., `.py`, `.js`, `.html`, `.md`):
   - Manually resolve conflicts in your text editor or IDE.
   - Look for conflict markers:
     ```
     <<<<<<< HEAD
     Your changes
     =======
     Incoming changes
     >>>>>>> main
     ```
   - Clean up these sections, decide what to keep, then:
     ```bash
     git add <resolved-files>
     git commit
     ```

---

## Notebook PDF Generation

- Our GitHub Actions workflow automatically generates PDFs from notebooks.
- These are saved under:
  ```
  ml/EDA/reports/<notebook-name>.pdf
  ```
- **Do not manually edit files inside `ml/EDA/reports/`.** These are auto-generated and updated as part of the workflow.

---

## Submitting Your Changes

1. Push your branch:
   ```bash
   git push origin topics/your-feature-name
   ```

2. Open a **Pull Request** (PR) on GitHub.
   - Ensure your branch is up to date with `main`.
   - Request review from project collaborators.
   - Check that the GitHub Action for PDF generation passes successfully.

---

## Important Reminders

- Always **pull before pushing**.
- Do **not merge unresolved conflicts** — conflicts must be handled manually.
- Use the **`nbdime` merge tool** for notebooks to prevent losing work.
- Keep commits focused and meaningful.

---

Thank you for following these guidelines and helping maintain clean, conflict-free collaboration!


