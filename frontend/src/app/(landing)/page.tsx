import { Hero } from "./components/Hero";
import { Features } from "./components/Features";
import { Navigation } from "./components/Navigation";
import { Footer } from "./components/Footer";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navigation />
      <Hero />
      <Features />
      <Footer />
    </div>
  );
}
