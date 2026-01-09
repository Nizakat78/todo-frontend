# Quickstart Guide: Frontend Todo Web App

## Development Setup

### Prerequisites
- Node.js 18+
- npm or yarn package manager
- Git

### Initial Setup
1. Clone the repository (if not already done)
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   npm install
   ```
4. Set up environment variables (if any):
   ```bash
   cp .env.example .env.local
   # Update values as needed
   ```

### Initialize Tailwind CSS
If not already initialized:
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Update `tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### Run Development Server
```bash
npm run dev
```
Application will be available at `http://localhost:3000`

## Project Structure Overview

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page
│   ├── login/             # Login page
│   │   └── page.tsx
│   ├── signup/            # Signup page
│   │   └── page.tsx
│   ├── dashboard/         # Dashboard page
│   │   └── page.tsx
│   ├── tasks/
│   │   ├── add/           # Add task page
│   │   │   └── page.tsx
│   │   └── edit/
│   │       └── [id]/      # Edit task page (dynamic route)
│   │           └── page.tsx
│   └── globals.css        # Global styles
├── components/            # Reusable components
│   ├── Navbar.tsx
│   ├── TaskCard.tsx
│   ├── TaskForm.tsx
│   ├── FilterSort.tsx
│   └── ui/               # UI primitive components
│       ├── Button.tsx
│       ├── Input.tsx
│       └── Card.tsx
├── lib/                  # Utilities and API client
│   └── api.ts            # Placeholder API client
├── hooks/                # Custom React hooks
│   └── useAuth.ts
├── types/                # TypeScript type definitions
│   └── index.ts
└── public/               # Static assets
    └── favicon.ico
```

## Key Development Commands

### Development
```bash
npm run dev          # Start development server
```

### Build & Production
```bash
npm run build        # Build for production
npm run start        # Start production server
```

### Testing
```bash
npm run test         # Run unit tests
npm run test:e2e     # Run end-to-end tests
```

### Linting & Formatting
```bash
npm run lint         # Check for linting errors
npm run format       # Format code with Prettier
```

## Getting Started with Development

### 1. Start with the API Client
Begin by implementing the placeholder API client at `lib/api.ts`:
```typescript
// Example structure
export const apiClient = {
  auth: {
    login: (credentials: LoginCredentials) => {/* */},
    signup: (userData: SignupData) => {/* */},
    logout: () => {/* */}
  },
  tasks: {
    getAll: () => {/* */},
    getById: (id: string) => {/* */},
    create: (taskData: TaskData) => {/* */},
    update: (id: string, taskData: TaskData) => {/* */},
    delete: (id: string) => {/* */}
  }
};
```

### 2. Create Shared Types
Define TypeScript interfaces in `types/index.ts`:
```typescript
export interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
  userId: string;
}
```

### 3. Build Core Components
Start with the most fundamental components:
1. UI primitives (Button, Input, Card)
2. Main layout components (Navbar)
3. Feature-specific components (TaskCard, TaskForm)

### 4. Implement Pages
Follow the order of user journey:
1. Authentication pages (Login, Signup)
2. Dashboard page
3. Task management pages (Add, Edit)

## Environment Configuration

For development, create a `.env.local` file:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:3001/api
NEXT_PUBLIC_APP_NAME="Todo Web App"
```

## Common Development Tasks

### Adding a New Page
1. Create a new directory in `app/` with the route name
2. Add a `page.tsx` file in that directory
3. Import and use necessary components
4. Add any required API calls using the placeholder client

### Creating a New Component
1. Create a new file in `components/`
2. Export the component as default
3. Add TypeScript interfaces for props
4. Use Tailwind classes for styling
5. Add unit tests

### Adding API Endpoints
1. Add the function to the appropriate section in `lib/api.ts`
2. Define the TypeScript interface for request/response
3. Handle errors appropriately
4. Add loading states in components that use the API

## Troubleshooting

### Common Issues
- **Module not found**: Ensure all dependencies are installed with `npm install`
- **TypeScript errors**: Check that all interfaces are properly defined
- **Tailwind classes not working**: Verify `tailwind.config.js` content paths are correct
- **API calls failing**: Check that the placeholder API client is properly implemented

### Hot Reload Issues
If hot reload stops working:
```bash
rm -rf .next
npm run dev
```

## Next Steps
1. Complete all components as per the specification
2. Implement all pages with proper routing
3. Add comprehensive tests
4. Verify responsive design on different screen sizes
5. Prepare for backend integration