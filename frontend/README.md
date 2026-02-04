# Frontend - Todo Web App

Next.js 16 + TypeScript task management application with Better Auth authentication.

## Quick Start

### Prerequisites
- Node.js 18+
- npm 10+

### Setup
```bash
# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local

# Run development server
npm run dev
```

Open http://localhost:3000

### Environment Variables
```env
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret-key
```

## Available Scripts

```bash
npm run dev       # Development server
npm run build     # Production build
npm start         # Start production server
npm test          # Run tests
npm run lint      # Lint code
```

## Features

- User authentication (signup/signin)
- Create, edit, delete tasks
- Filter and sort tasks
- Responsive design
- Full TypeScript support

## Project Structure

```
src/
├── app/          # Next.js pages
├── components/   # React components
├── hooks/        # Custom hooks
├── lib/          # Utilities & config
├── middleware/   # API interceptor
├── types/        # TypeScript types
└── tests/        # Test setup
```

## Technology

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Forms**: React Hook Form + Zod
- **Auth**: Better Auth
- **HTTP**: Axios
- **Testing**: Jest + React Testing Library

## Deployment

Deploy to Vercel:
1. Push to GitHub
2. Connect repo to Vercel
3. Set environment variables
4. Deploy

See root `README.md` for detailed instructions.

## Support

- View API docs: http://localhost:8000/docs
- See `CLAUDE.md` for development standards
