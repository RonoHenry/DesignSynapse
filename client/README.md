# Design Synapse (Vybe Architect Nexus)

A modern, scalable, and beautiful construction intelligence platform that unifies AI, BIM, and professional design tools for next-generation architectural collaboration.

---

## Features
- **Modern Frontend**: Built with React, Vite, TypeScript, shadcn/ui, Radix UI, and Tailwind CSS.
- **Component-Driven**: Modular UI components for rapid development and easy customization.
- **Theming**: Light, dark, and custom theme support.
- **AI Assistant**: Integrated chatbot (Vyber) for design and workflow support.
- **BIM Viewer**: Interactive 3D model workspace and project coordination.
- **Project Workspace**: Manage, track, and visualize active projects.
- **Quick Actions**: Start new designs, import BIM models, generate BOQs, and more.
- **API Ready**: Designed for seamless backend integration (authentication, data, etc.).
- **Developer Experience**: Path aliases, ESLint, Prettier, and full TypeScript support.

## Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation
```bash
npm install
# or
yarn
```

### Development
```bash
npm run dev
# or
yarn dev
```
Visit [http://localhost:5173](http://localhost:5173) in your browser.

### Build for Production
```bash
npm run build
# or
yarn build
```

### Linting
```bash
npm run lint
# or
yarn lint
```

## Project Structure
```
client/
├── src/
│   ├── components/         # App-level and UI components
│   ├── hooks/              # Custom React hooks
│   ├── contexts/           # React context providers
│   ├── lib/                # Utilities and helpers
│   ├── pages/              # App pages/routes
│   ├── assets/             # Styles and static assets
│   └── ...
├── public/                 # Static files
├── index.html              # App entry HTML
├── package.json            # Project metadata and scripts
├── tailwind.config.ts      # Tailwind CSS config
├── postcss.config.js       # PostCSS config
├── tsconfig.json           # TypeScript config
└── ...
```

## Backend Integration
- The frontend is ready for API integration (authentication, data, etc.).
- Use React Query or your preferred data fetching library.
- Add your backend endpoints and connect them to the UI components.

## Security & Production
- Audit dependencies regularly (`npm audit`).
- Harden backend endpoints and validate all user input.
- Set up CI/CD for automated builds, tests, and deploys.

## Contributing
Pull requests and issues are welcome! Please open an issue to discuss your ideas or report bugs.

## License
[MIT](LICENSE)

---

**Made with ❤️ by the Design Synapse team and Lovable.**
