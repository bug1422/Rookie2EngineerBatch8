# Rookie2Engineer Batch 8 Frontend

A React TypeScript frontend application built with modern tools and libraries.

## Introduction

This project serves as the frontend application for the Rookie2Engineer Batch 8 training program. It utilizes React with TypeScript, along with modern tooling like Vite for development and building.

## Getting Started

### Prerequisites
- Node.js (LTS version recommended)
- npm or yarn package manager

### Installation
1. Clone the repository
2. Install dependencies:
```bash
npm install
# or
yarn
```

### Development
To start the development server:
```bash
npm run dev
# or
yarn dev
```

### Production Build
To create a production build:
```bash
npm run build
# or
yarn build
```

## Technology Stack
- React 19
- TypeScript
- Vite
- TailwindCSS
- DaisyUI
- React Router DOM
- React Query
- Zustand
- Axios

## Project Structure
The project uses a modern React stack with:
- TypeScript for type safety
- Vite for fast development and building
- TailwindCSS for styling
- React Query for data fetching
- Zustand for state management
- ESLint for code quality

## Contributing
We follow a Git branching strategy with the following branches:

- `main`: Production-ready code
- `develop`: Main development branch, all features and fixes are merged here first
- `feature/*`: Feature branches for new development (e.g., feature/user-auth)
- `release/*`: Release preparation branches (e.g., release/1.2.0)
- `hotfix/*`: Emergency fixes for production issues (e.g., hotfix/login-fix)

### Development Workflow

1. Create a new feature branch from develop:
   ```bash
   git checkout develop
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

3. Keep your branch updated with develop:
   ```bash
   git checkout develop
   git pull
   git checkout feature/your-feature-name
   git rebase develop
   ```

4. Submit a pull request to the develop branch

### Release Process

1. Create a release branch from develop:
   ```bash
   git checkout develop
   git checkout -b release/version-number
   ```

2. Prepare release (version bumps, final fixes)
3. Merge to main and develop when ready
4. Tag the release on main

### Hotfix Process

1. Create hotfix branch from main:
   ```bash
   git checkout main
   git checkout -b hotfix/issue-description
   ```

2. Fix the issue
3. Merge to both main and develop

## Scripts
- `dev`: Start development server
- `build`: Create production build
- `lint`: Run ESLint
- `preview`: Preview production build
- `test`: Run tests
- `coverage`: Run tests with coverage