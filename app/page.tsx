import Image from "next/image";
import MapBox from "@/components/MapBox";
import LastUploadHeader from "../components/LastUploadHeader";

export default function Home() {
  return (
    // Changed h-dvh max-h-dvh overflow-hidden -> min-h-dvh
    <div className="flex flex-col min-h-dvh bg-gray-50 text-slate-900">
      
      {/* 1. HEADER (Now sticky so it stays visible while scrolling) */}
      <header className="w-full bg-white border-b border-gray-200 px-6 py-3 shrink-0 sticky top-0 z-50 shadow-sm">
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
      <main className="flex-grow flex flex-col items-center p-4 md:p-6 w-full">
        
        {/* Page Title Section */}
        <div className="text-center max-w-2xl shrink-0 mt-2 mb-4">
          <h1 className="text-xl md:text-3xl font-extrabold tracking-tight text-slate-950">
            Soil measurement dashboard
          </h1>
          <p className="text-xs md:text-sm text-slate-500 mt-0.5 mb-3">
            
            This website shows a visual overview of the soil quality, according to measured data. Hover your mouse over the data points on the map to see the raw measurements. <br /><br />

            Note: The current version of this website uses a test dataset with dummy-coordinates. This website is only used as proof-of-concept of a user interface. Take measurement size, coordinates and content with a grain of salt.
          </p>
        </div>

        <LastUploadHeader/>


        <h1 className="text-l md:text-2xl font-extrabold tracking-tight text-slate-950 mb-4">
          Watering strategy
        </h1>

        <div className="flex flex-col md:flex-row items-center justify-center w-full max-w-5xl gap-6 my-4 mb-15">
          <MapBox 
            filename="Watermap.html" 
            title="Watering advice"
          />
        </div>

        <h1 className="text-l md:text-2xl font-extrabold tracking-tight text-slate-950 mb-4">
          Salinity and moisture overview maps
        </h1>

        <div className="flex flex-col md:flex-row items-center justify-center w-full max-w-5xl gap-6 my-4 mb-15">
          <MapBox 
            filename="Salinitymap.html" 
            title="Salinity spatial overview"
          />
          <MapBox 
            filename="Moisturemap.html" 
            title="Moisture spatial overview"
          />
        </div>



        <h1 className="text-l md:text-2xl font-extrabold tracking-tight text-slate-950 mb-4">
          Raw measurements
        </h1>

        <div className="flex flex-col items-center justify-center w-full max-w-5xl gap-6 my-4 mb-15">
          <MapBox 
            filename="Conductivitymap.html" 
            title="Soil electrical conductivity"
          />
          <MapBox 
            filename="Temperaturemap.html" 
            title="Soil temperature"
          />
          <MapBox 
            filename="Watercontentmap.html" 
            title="Soil volumetric water content"
          />
        </div>

      </main>

      {/* 3. FOOTER */}
      <footer className="w-full bg-slate-900 text-slate-400 border-t border-slate-800 px-6 py-4 shrink-0 mt-auto">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2 text-sm">
          <div>
            <p className="font-medium text-slate-300 text-xs md:text-sm">The ASML2 project group for EE2G1:</p>
            <p className="text-[10px] md:text-xs text-slate-400 mt-0.5 leading-relaxed">
              Zara Cicak, Arne Cuperus, Wessel de Vries, Itai Givony, Anais Glaubitz, Jort Groenendijk, Ilse Janssen, Mart Schaafsma, Stijn ter Huurne & Sanne Uittenbogaard
            </p>
          </div>
        </div>
      </footer>

    </div>
  );
}