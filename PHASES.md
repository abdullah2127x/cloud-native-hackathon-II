# Project Phases

This document describes the project phases and branch management strategy.

## Overview

Using **Git branches** for phase management. Each phase is a separate branch off `main`, with clean separation and easy version tracking.

```
main (Phase 2 - Latest Stable)
  ├── phase-2 (Phase 2 Archive)
  ├── phase-3-development (Phase 3 - Active)
  └── Tags: v1.0.0 (phase-2), v2.0.0 (phase-3), ...
```

---

## Phase 2 ✅ COMPLETE

**Branch**: `phase-2`

**What's Included**:
- ✅ User authentication with Better Auth + JWT
- ✅ Complete CRUD operations for tasks
- ✅ Task filtering, sorting, searching
- ✅ Priority levels and tags
- ✅ Responsive UI with Tailwind CSS
- ✅ Full TypeScript type safety
- ✅ 70%+ test coverage
- ✅ Deployment to Vercel (frontend) and ngrok (backend)

**Key Features**:
- Signup/signin with email & password
- Create, read, update, delete tasks
- Mark tasks complete/incomplete
- Filter by status, priority, tags
- Search by title/description
- Sort by multiple fields
- User data isolation (database-level)

**Technology Stack**:
- Frontend: Next.js 16, TypeScript, Tailwind CSS, Better Auth
- Backend: FastAPI, SQLModel, PostgreSQL (Neon)
- Database: PostgreSQL with Neon Serverless
- Auth: Better Auth with JWT verification via JWKS
- Testing: Jest (frontend), pytest (backend)

**Documentation**:
- `README.md` - Main project overview
- `frontend/README.md` - Frontend setup
- `backend/README.md` - Backend setup
- `frontend/CLAUDE.md` - Frontend development standards
- `backend/CLAUDE.md` - Backend development standards
- `backend/DEPLOYMENT.md` - Deployment checklist

**Git Commands**:
```bash
# View Phase 2 code
git checkout phase-2

# Compare Phase 2 vs Phase 3
git diff phase-2 main

# Return to Phase 3
git checkout main
```

---

## Phase 3 🚀 IN PROGRESS

**Branch**: `main` (work here for Phase 3)

**Planned Features**:
- [ ] Advanced filtering (date ranges, custom filters)
- [ ] Recurring tasks
- [ ] Task dependencies/subtasks
- [ ] Collaboration features (shared tasks)
- [ ] Task templates
- [ ] Custom themes
- [ ] Mobile app (React Native)
- [ ] Export/import tasks (CSV, JSON)
- [ ] Notifications (email, push)
- [ ] Analytics dashboard

**Development Workflow**:
```bash
# Create feature branches from main
git checkout -b feature/phase-3-feature-name

# Work on feature
# ... commit changes ...

# Merge back to main when complete
git checkout main
git merge feature/phase-3-feature-name

# Push to GitHub
git push origin main
```

**Tag Release**:
When Phase 3 is complete:
```bash
git tag -a v2.0.0 -m "Phase 3 Complete: Advanced features"
git push origin main --tags
```

---

## Phase 1 (Reference)

**Status**: Archived (not in repo)

Phase 1 was a CLI todo app in `phase-1-cli-todo/` folder. This was replaced by the web application in Phase 2.

---

## Branch Management Strategy

### Main Branch (`main`)
- Always represents the **latest stable + current development**
- Phase 2 code is the stable base
- Phase 3 features are added here
- Protected: requires PR reviews before merge

### Phase Branches (`phase-2`, `phase-3-development`, etc.)
- Immutable historical record of each phase
- Can checkout to see exact state at phase completion
- Never force-push to these branches

### Feature Branches (`feature/*`, `bugfix/*`, `docs/*`)
- Created from `main` for new work
- Example: `feature/phase-3-recurring-tasks`
- Deleted after merge

### Release Tags (`v1.0.0`, `v2.0.0`, etc.)
- Point to specific commits
- Example: `v1.0.0` = Phase 2 complete
- Used for deployment versioning

---

## Environment Variables by Phase

### Phase 2 (Current)
**Frontend** (`.env.local`):
```env
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...
```

**Backend** (`.env`):
```env
DATABASE_URL=postgresql://...
BETTER_AUTH_URL=http://localhost:3000
CORS_ORIGINS=["http://localhost:3000"]
```

### Phase 3 (Future)
Same as Phase 2, plus new features may require:
- `NOTIFICATION_SERVICE_KEY` (for email/push)
- `STORAGE_BUCKET` (for file uploads)
- `ANALYTICS_KEY` (for analytics)

---

## Testing by Phase

### Phase 2
```bash
# Frontend: 70%+ coverage
cd frontend && npm test -- --coverage

# Backend: 70%+ coverage
cd backend && uv run pytest --cov=src
```

### Phase 3
Same testing strategy, expanding coverage as features are added.

---

## Deployment by Phase

### Phase 2 (Current)
- **Frontend**: Vercel (https://ai-todo-web-app.vercel.app)
- **Backend**: ngrok (local) or Railway/Render

### Phase 3
- **Frontend**: Vercel (same deployment)
- **Backend**: Permanent cloud deployment (Railway/Render recommended)
- Consider: Docker containers, CI/CD pipeline

---

## How to Work on Phase 3

### 1. Start a New Feature
```bash
# Make sure you're on main
git checkout main

# Create feature branch
git checkout -b feature/phase-3-your-feature-name
```

### 2. Make Changes
```bash
# Edit code in frontend/ and/or backend/
# No file movement needed - same structure as Phase 2
```

### 3. Commit Changes
```bash
git add .
git commit -m "feat(phase-3): add your feature description"
```

### 4. Push and Create PR (optional)
```bash
git push origin feature/phase-3-your-feature-name
# Then create PR on GitHub
```

### 5. Merge to Main
```bash
git checkout main
git merge feature/phase-3-your-feature-name
git push origin main
```

### 6. Clean Up Branch
```bash
git branch -d feature/phase-3-your-feature-name
git push origin --delete feature/phase-3-your-feature-name
```

---

## Comparing Phases

```bash
# See differences between Phase 2 and Phase 3
git diff phase-2 main

# See files changed
git diff phase-2 main --name-only

# See specific file diff
git diff phase-2 main -- frontend/src/app/page.tsx
```

---

## Reverting to Phase 2

If needed, you can revert to Phase 2:
```bash
# View Phase 2 state
git checkout phase-2

# Create new branch from Phase 2
git checkout -b bugfix/from-phase-2 phase-2

# Make fixes
# ... commit changes ...

# Merge fixes back to main
git checkout main
git merge bugfix/from-phase-2
```

---

## Summary

| Item | Phase 2 | Phase 3 |
|------|---------|---------|
| Branch | `phase-2` | `main` |
| Status | ✅ Complete | 🚀 Active |
| Folder | `frontend/`, `backend/` | `frontend/`, `backend/` |
| Work Here | No (read-only) | YES |
| Tag | `v1.0.0` | (v2.0.0 when done) |
| Deployment | Vercel + ngrok | Vercel + Cloud |

---

**Last Updated**: February 2026
**Phase 2 Completed**: 2026-02-04
**Phase 3 Started**: 2026-02-04
