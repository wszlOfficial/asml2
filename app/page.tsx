import Image from "next/image";
import MapBox from "@/components/MapBox";

export default function Home() {
  return (
    <div className="flex flex-col h-dvh max-h-dvh overflow-hidden bg-gray-50 text-slate-900">
      
      {/* 1. HEADER */}
      <header className="w-full bg-white border-b border-gray-200 px-6 py-3 shrink-0">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center">
            <Image 
              src="/ASML2.png"       
              alt="Company Logo" 
              width={80}            
              height={80}
              className="object-contain"
              priority
            />
          </div>
        </div>
      </header>

      {/* 2. MAIN CONTENT AREA */}
      <main className="flex-grow flex flex-col items-center justify-between p-4 md:p-6 min-h-0 overflow-hidden">
        
        {/* Page Title Section */}
        <div className="text-center max-w-2xl shrink-0 mt-2">
          <h1 className="text-xl md:text-3xl font-extrabold tracking-tight text-slate-950">
            Soil measurement dashboard
          </h1>
          <p className="text-xs md:text-sm text-slate-500 mt-0.5">
            A spatial visualisation of moisture and salinity data.
          </p>
        </div>

        {/* Responsive Maps Container */}
        {/* FIX: Added 'my-4 md:my-8' to inject crisp vertical padding above and below the maps */}
        <div className="flex flex-col md:flex-row items-center justify-center w-full max-w-5xl gap-4 md:gap-8 flex-grow min-h-0 max-h-full my-4 md:my-8">
          <MapBox 
            filename="Salinitymap.html" 
            title="Salinity spatial overview"
          />
          <MapBox 
            filename="Moisturemap.html" 
            title="Moisture spatial overview"
          />
        </div>

      </main>

      {/* 3. FOOTER */}
      <footer className="w-full bg-slate-900 text-slate-400 border-t border-slate-800 px-6 py-4 shrink-0">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2 text-sm">
          <div>
            <p className="font-medium text-slate-300 text-xs md:text-sm">The ASML2 project group for EE2G1:</p>
            <p className="text-[10px] md:text-xs text-slate-400 mt-0.5 leading-relaxed">
              By Zara Cicak, Arne Cuperus, Wessel de Vries, Itai Givony, Anais Glaubitz, Jort Groenendijk, Ilse Janssen, Mart Schaafsma, Stijn ter Huurne & Sanne Uittenbogaard
            </p>
          </div>
        </div>
      </footer>

    </div>
  );
}